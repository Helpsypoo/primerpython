#import bpy
import imp
from random import random, uniform, randrange
from copy import copy
import pickle

import bobject
imp.reload(bobject)
from bobject import *

import blobject

import helpers
imp.reload(helpers)
from helpers import *

#Sim constants
WORLD_DIMENSIONS = [150, 150]
SIM_RESOLUTION = 0.3
DEFAULT_DAY_LENGTH = 600 * SIM_RESOLUTION
PREDATOR_SIZE_RATIO = 1.2 #Vals close to 1 apply strong pressure toward bigness,
                          #since it becomes possible to eat recent ancestors.
SPEED_ADJUST_FACTOR = 1.0 #Scale speed to keep creature speeds in the 0-2 range
                          #for graphing. Units are arbitrary anyway, so this is
                          #easier than adjusting all the distances.
SIZE_ADJUST_FACTOR = 1.0
HEADING_TARGET_VARIATION = 0.4 #Range for random heading target changes, radians
MAX_TURN_SPEED = 0.07 / SIM_RESOLUTION
TURN_ACCELERATION = 0.005 / SIM_RESOLUTION
BASE_SENSE_DISTANCE = 25
EAT_DISTANCE = 10
MUTATION_CHANCE = 0.1
MUTATION_VARIATION = 0.1
STARTING_ENERGY = 800 #1800
HOMEBOUND_RATIO = 2# 1.5



#Visual constants
DEFAULT_DAY_ANIM_DURATION = 8 #seconds
BLENDER_UNITS_PER_WORLD_UNIT = 1 / 40
FOOD_SCALE = 2 * BLENDER_UNITS_PER_WORLD_UNIT
BASE_CREATURE_SCALE = 0.25
CREATURE_HEIGHT = 0.65 * BASE_CREATURE_SCALE / BLENDER_UNITS_PER_WORLD_UNIT
SPEED_PER_COLOR = 0.3 #Speed change for one color unit change

DEFAULT_ANIM_DURATIONS = {
    'dawn' : 0.5, #Put out food and creatures
    'morning' : 0.25, #pause after setup
    'day' : DEFAULT_DAY_ANIM_DURATION, #creatures go at it
    'evening' : 0.25, #pause before reset
    'night' : 0.5 #reset
}
'''DEFAULT_ANIM_DURATIONS = {
    'dawn' : 1, #Put out food and creatures
    'morning' : 0.5, #pause after setup
    'day' : DEFAULT_DAY_ANIM_DURATION, #creatures go at it
    'evening' : 0.5, #pause before reset
    'night' : 1 #reset
}'''

"""
TODOs
- Arrange sims/graph as it will be in the video
- Work on fast-forward sims (Seems to work fine, actually)
- Rebalance using non-animated sims to get a sense for things more quickly
    - Multiplying to get total cost encourages extreme tradeoffs, making the traits
    that matter less (sense) into dump stats.
    - Speed and size are highly competitive. There doesn't seem to be a way of
    making them bimodal without a change in behavior. A slow creature might be
    able to get by, but the faster creatures will multiply and quickly eat all
    the food. Having small creatures run from big creatures might be a behavioral
    trick to encourage multiple strategies. (You can be small if you have good
    senses and speed.)
- Visual
    - Make food not appear close to edge.
    - Distinguish border, by covering or otherwise. Smoke?


Perhaps unnecessary
- Make creatures run from larger ones. (If can't balance)
- Break eating ties (Not sure if necessary)
- Reuse dead creature objects and old food objects
    (maybe even resize/recolor for extra smoothness)
    Postponing this because the childof constraints add complexity to this task
    And it only affects blender's UI responsiveness (and possibly render time)
    Might try again later, but not necessary now.
- Fix teleportation bugs
    Food sometimes appears below the plane. Could be related to immediate eating?
    Not super common, so might say meh. You can't even see it.

Parameter considerations
- Avg number of creatures. Tradeoff between simplicity/speed and stability
- Creature density. More direct competition.
    - Makes size better, since there are more creature interactions.
    - Makes sense worse, since you're more likely to sense others
      even with low sense.
    - Makes speed better, since there is more predation and direct food
      competition.
- Food density. Effects similar to those of creature density. They should also
  track each other closely.
- Starting energy vs world size.
    - Makes low stats better because of efficiency.
    - May actually make sense more valuable, though, since that adds efficiency.

Learnings:
- It seems like it was a bad call to use bobjects and bobject methods for the
  sim. Bobjects and their methods are made to be easy to use for arranging
  objects manually throughout a scene, but when embedded automated structures,
  they cause two problems. First, methods like bobject.move_to() place a starting
  keyframe and ending keyframe. This can cause durations to overlap, creating
  confused motions. Second, the bobject methods generally use seconds as the
  time unit. This is all well and good when thinking directly about a timeline,
  but using them alongside the blender api creates a need to convert units often,
  giving many chances for confusion, bugs, and ugliness.
- Managing the double-parent relationships has proven difficult. It may have been
  better to have a childof constraint rather than full parenting of the food,
  since the constraints can simply be turned off.
"""

class CreatureDay(object):
    """docstring for CreatureDay."""
    def __init__(
        self,
        creature = None,
        date = 0
    ):
        if creature == None:
            raise Warning("CreatureDay must belong to a creature")
        self.creature = creature
        self.date = date

        #These only need to be lists if animated, and not all will be, but
        #I'm making them all lists in case I decide to animate the value in
        #some way down the road.

        #Lots of heading to make turns smooth
        self.heading_targets = []
        self.d_headings = [] #Turn rate
        self.headings = []
        self.locations = []
        self.has_eaten = []
        self.energies = []
        self.states = []

        self.dead = False
        self.death_time = None
        self.home_time = None

class Food(object):
    """docstring for Food."""
    def __init__(
        self,
        world_location = [0, 0, 0],
        parents = [],
        world = None
        #has_world_as_parent = True
    ):
        self.world_location = world_location
        self.world = world
        self.is_eaten = False

        '''if isinstance(parents, list):
            self.parents = parents
        else:
            self.parents = [parents]'''

        #self.parents.append(self.world)

    def git_ate(
        self,
        eater = None,
        start_time = None,
        time_step = 0.3,
        drawn_world = None
    ):
        if start_time == None:
            raise Warning('Need start time for git_ate')
        #Make sure these are on frames
        #start_time = round(start_time * 60) / 60
        start_frame = math.floor(start_time * 60)
        duration = 50 * time_step * SIM_RESOLUTION
            #50 is duration of eat animation in world time
            #Should really be a constant
        duration_frames = max(math.floor(duration * 60), 3)
        #end_time = start_time + duration
        end_frame = start_frame + duration_frames

        if drawn_world == None:
            raise Warning('Need to define drawn_world for git_ate')

        if eater == None:
            raise Warning("Need to define eater")
        #if eater not in self.parents:
        self.make_child_of_constraint(parent = eater.bobject.ref_obj)

        '''for cons in self.bobject.ref_obj.constraints:
            cons.keyframe_insert(data_path = 'influence', frame = start_frame)
            if cons.target == eater.bobject.ref_obj:
                cons.influence = 1
            else:
                cons.influence = 0
            cons.keyframe_insert(data_path = 'influence', frame = start_frame + 1)'''

        for cons in self.bobject.ref_obj.constraints:
            if cons.target == eater.bobject.ref_obj:
                cons.keyframe_insert(data_path = 'influence', frame = start_frame)
                cons.influence = 1
                cons.keyframe_insert(data_path = 'influence', frame = start_frame + 1)

        #There is almost certainly a more elegant way to do this, but there are
        #several transformation matrices which don't seem to relaiably update,
        #and there's an extra complication because the 'parent' in the childof
        #constraint has the same parent as the food object, making the real parent
        #affect the transform twice.
        #I gave up and did a more manual calculation of the location.
        rel = (self.bobject.ref_obj.location - eater.bobject.ref_obj.location)
        ang = eater.bobject.ref_obj.rotation_euler[2]
        sca = eater.size * BASE_CREATURE_SCALE #eater.bobject.ref_obj.scale
        #Above line refers to creature property rather than object property in
        #blender, since I ran into a bug where the blender object was scaled to
        #zero (not keyframed) when this code executes. The creature property should
        #be the intended value and not change.
        loc_in_new_ref_frame = [
            (rel[0] * math.cos(-ang) - rel[1] * math.sin(-ang)) / sca,#[0],
            (rel[0] * math.sin(-ang) + rel[1] * math.cos(-ang)) / sca,#[1],
            rel[2] / sca,#[2]
        ]

        #Need to correct scale because the child_of constraint doesn't use scale
        #The intent is to not affect the scale of the object itself, but the
        #scale of the eater should be used to determine the position. So that's
        #here.
        for i in range(len(loc_in_new_ref_frame)):
            loc_in_new_ref_frame[i] *= eater.bobject.ref_obj.scale[i]


        #Subtract the contribution of the common parent (so it just contributes once)
        corrected_loc = [
            loc_in_new_ref_frame[0] - eater.bobject.ref_obj.parent.location[0] / eater.bobject.ref_obj.parent.scale[0],
            loc_in_new_ref_frame[1] - eater.bobject.ref_obj.parent.location[1] / eater.bobject.ref_obj.parent.scale[1],
            loc_in_new_ref_frame[2] - eater.bobject.ref_obj.parent.location[2] / eater.bobject.ref_obj.parent.scale[2],
        ]

        #Rotation should be part of the childof constraint for the purpose of
        #updating location, but the object itself shouldn't rotate.
        #So subtract the eater's rotation.
        corrected_rot = [
            self.bobject.ref_obj.rotation_euler[0] - eater.bobject.ref_obj.rotation_euler[0],
            self.bobject.ref_obj.rotation_euler[1] - eater.bobject.ref_obj.rotation_euler[1],
            self.bobject.ref_obj.rotation_euler[2] - eater.bobject.ref_obj.rotation_euler[2],
        ]

        #Store differences to return for subclass implementation
        #When eaten, creatures should correct locations of things they've eaten
        #to avoid those things teleporting. This is a mess, eh?
        loc_diff = add_lists_by_element(
            corrected_loc,
            self.bobject.ref_obj.location,
            subtract = True
        )
        rot_diff = add_lists_by_element(
            corrected_rot,
            self.bobject.ref_obj.rotation_euler,
            subtract = True
        )

        #Change location to be the same in new reference frame
        self.bobject.move_to(
            start_frame = start_frame,
            end_frame = start_frame + 1,
            new_location = corrected_loc,
            new_angle = corrected_rot
        )
        #Move in front of creature
        self.bobject.move_to(
            start_frame = start_frame + 1,
            end_frame = start_frame + math.floor(duration_frames / 2),
            new_location = [
                - eater.bobject.ref_obj.parent.location[0] / eater.bobject.ref_obj.parent.scale[0] + eater.bobject.ref_obj.scale[2],
                - eater.bobject.ref_obj.parent.location[1] / eater.bobject.ref_obj.parent.scale[1],
                eater.bobject.ref_obj.scale[2] / 5
            ]
        )
        #Move into creature and shrink
        self.bobject.move_to(
            start_frame = start_frame + math.ceil(duration_frames / 2),
            end_frame = end_frame,
            new_location = [
                - eater.bobject.ref_obj.parent.location[0] / eater.bobject.ref_obj.parent.scale[0],
                - eater.bobject.ref_obj.parent.location[1] / eater.bobject.ref_obj.parent.scale[1],
                eater.bobject.ref_obj.scale[2] / 5
            ],
            new_scale = 0
        )

        eater.eat_animation(start_time = start_time, time_step = time_step)
        eater.bobject.blob_scoop(start_time = start_time, duration = duration)
        #I don't remember why I'm multiplying things by 50, tbh, but it works.
        #I'm good at coding.

        return loc_diff, rot_diff #, self.bobject.ref_obj

    def make_child_of_constraint(self, parent = None):
        if self.bobject == None:
            raise Warning('Food needs a bobject to get parent')

        constraints = self.bobject.ref_obj.constraints
        make_new = True
        for cons in constraints:
            if cons.type == 'CHILD_OF' and cons.target == parent:
                make_new = False

        if make_new == True:
            new_cons = self.bobject.ref_obj.constraints.new('CHILD_OF')
            new_cons.use_scale_x = False
            new_cons.use_scale_y = False
            new_cons.use_scale_z = False

            new_cons.influence = 0

            if parent == None:
                raise Warning('Need parent for child_of constraint')
            new_cons.target = parent

    def add_to_blender(self):
        self.bobject = import_object(
            'goodicosphere', 'primitives',
            #world_location = [0, 0, 0],
            location = [0, 0, 0],
            scale = FOOD_SCALE
        )
        apply_material(self.bobject.ref_obj.children[0], 'color7')

class Creature(Food):
    def __init__(
        self,
        speed = 1,
        size = 1,
        sense = 1,
        altruist = False,
        kin_radius = 0,
        parent = None,
        world = None
    ):
        super().__init__()
        self.speed = speed
        self.size = size
        self.sense = sense
        self.kin_radius = kin_radius
        self.altruist = altruist
        self.parent = parent

        self.days = []

        self.bobject = None
        self.world = world

        cost = 0
        cost += (self.size * SIZE_ADJUST_FACTOR) ** 3 * (self.speed * SPEED_ADJUST_FACTOR) ** 2 #* 2
        cost += (self.size * SIZE_ADJUST_FACTOR) ** 3 / 2
        cost += self.sense / 2
        self.energy_cost = cost / SIM_RESOLUTION

    def new_day(self, date = 0, parent = None):
        new_day = CreatureDay(creature = self, date = date)
        if len(self.days) == 0: #First day of life, ahhhh.
            if parent == None: #For initial creatures

                loc, heading_target, heading = self.random_wall_placement()

                new_day.locations.append(loc)
                new_day.heading_targets.append(heading_target)
                new_day.d_headings.append(0)
                new_day.headings.append(heading)

            elif parent != None:
                #Perhaps not the most robust way to do it, but using days[-2]
                #here because the parents make their new days before the
                #children, since the children are added to the end of the
                #creature list on their first day
                new_day.locations.append(parent.days[-2].locations[-1])
                new_day.heading_targets.append(
                    parent.days[-2].heading_targets[-1] + math.pi
                )
                new_day.d_headings.append(0)
                new_day.headings.append(
                    parent.days[-2].headings[-1] + math.pi
                )
        else:
            new_day.locations.append(
                self.days[-1].locations[-1]
            )
            new_day.heading_targets.append(
                self.days[-1].heading_targets[-1] + math.pi
            )
            new_day.d_headings.append(0)
            new_day.headings.append(
                self.days[-1].headings[-1] + math.pi
            )

        new_day.has_eaten.append([])
        new_day.energies.append(self.world.initial_energy)

        self.days.append(new_day)

    def random_wall_placement(self):
        wall_roll = random()
        #print()
        #print(wall_roll)
        if wall_roll < 0.25:
            #print('Top')
            loc = [
                uniform(-self.world.dimensions[0], self.world.dimensions[0]),
                self.world.dimensions[1],
                CREATURE_HEIGHT * self.size
            ]
            heading_target = - math.pi / 2
            heading = - math.pi / 2
        elif wall_roll < 0.5:
            #print('Right')
            loc = [
                self.world.dimensions[0],
                uniform(-self.world.dimensions[1], self.world.dimensions[1]),
                CREATURE_HEIGHT * self.size
            ]
            heading_target = math.pi
            heading = math.pi
        elif wall_roll < 0.75:
            #print('Bottom')
            loc = [
                uniform(-self.world.dimensions[0], self.world.dimensions[0]),
                -self.world.dimensions[1],
                CREATURE_HEIGHT * self.size
            ]
            heading_target = math.pi / 2
            heading = math.pi / 2
        else:
            #print('Left')
            loc = [
                -self.world.dimensions[0],
                uniform(-self.world.dimensions[1], self.world.dimensions[1]),
                CREATURE_HEIGHT * self.size
            ]
            heading_target = 0
            heading = 0

        other_cres = [x for x in self.world.date_records[-1]['creatures'] if \
                                                                len(x.days) > 0]
        for cre in other_cres:
            cre_loc = cre.days[-1].locations[-1]
            dist = vec_len(add_lists_by_element(cre_loc, loc, subtract = True))
            if dist < EAT_DISTANCE:
                self.random_wall_placement()

        return loc, heading_target, heading

    def take_step(self):
        day = self.days[-1]

        #This set of conditionals is a bit of a frankenstein monster. Could
        #be streamlined.
        has_energy = True
        if day.energies[-1] == None:
            has_energy = False
            #print('HAS ENERGY IS FALSE')
        else:
            steps_left = math.floor(day.energies[-1] / self.energy_cost)
            #print('Steps left = ' + str(steps_left))
            distance_left = steps_left * self.speed * SPEED_ADJUST_FACTOR
            if steps_left <= 1:
                #For some reason, steps_left is never less than one, at least for
                #integer energy costs. I can't figure out why. So, some creatures
                #are going to take one fewer step than they could have. Meh.
                #print(day.energies[-1])
                #print(self.energy_cost)
                has_energy = False
        if has_energy == False and day.death_time == None and day.home_time == None:
            day.death_time = len(day.locations)
            self.days[-1].dead = True

        if self.days[-1].dead == True:
            day.heading_targets.append(None)
            day.d_headings.append(None)
            day.headings.append(None)
            day.locations.append(None)
            self.world_location = None
            #day.has_eaten.append(None)
            day.has_eaten.append(copy(day.has_eaten[-1]))
            day.energies.append(None)
        else:
            day.has_eaten.append(copy(day.has_eaten[-1])) #Append new eaten state to fill with food

            """Update heading based on state"""
            state = None
            distance_out = min(
                self.world.dimensions[0] - abs(day.locations[-1][0]),
                self.world.dimensions[1] - abs(day.locations[-1][1]),
            )

            if len(day.has_eaten[-1]) == 0:
                state = 'foraging'
            elif len(day.has_eaten[-1]) == 1:
                #print(day.locations[-1])
                #print(distance_out)
                #print(distance_left)
                last_state = None
                try:
                    last_state = day.states[-1]
                except:
                    pass
                #print(last_state)
                if distance_left < distance_out * HOMEBOUND_RATIO or \
                    last_state == 'homebound':
                    state = 'homebound'
                else:
                    state = 'foraging'
                #print(state)
            elif len(day.has_eaten[-1]) > 1:
                state = 'homebound'
            else:
                raise Warning('Somehow, the creature has eaten negative food')



            new_heading = None

            #Sense food. Eat if in eat range. If not, set new_heading toward
            #closest food sensed. (New heading can be overridden if creature
            #is fleeing or homebound)
            closest_food_dist = math.inf
            target_food = None
            food_objects = self.world.date_records[day.date]['food_objects']
            remaining_food = [x for x in food_objects if x.is_eaten == False]
            close_food = [x for x in remaining_food if vec_len(add_lists_by_element(x.world_location, day.locations[-1], subtract = True)) < EAT_DISTANCE + BASE_SENSE_DISTANCE * self.sense]

            creatures = self.world.date_records[day.date]['creatures']
            live_creatures = [x for x in creatures if x.days[-1].dead == False]
            close_creatures = [x for x in live_creatures if vec_len(add_lists_by_element(x.world_location, day.locations[-1], subtract = True)) < EAT_DISTANCE + BASE_SENSE_DISTANCE * self.sense]

            if self.altruist == True:
                to_be_nice_to = close_creatures
            else:
                to_be_nice_to = [x for x in close_creatures if \
                    ((x.size - self.size) ** 2 + (x.speed - self.speed) ** 2 + \
                    (x.sense - self.sense) ** 2) ** (1/2) > self.kin_radius]

            #Forget about food that another slower-but-similar creature is going
            #for,
            #if you're not about to starve
            #if len(day.has_eaten[-1]) > -1:

            for cre in to_be_nice_to:
                if cre.speed < self.speed:
                    claimed_food = None
                    claimed_food_dist = math.inf
                    for food in close_food:
                        dist = vec_len(add_lists_by_element(food.world_location, cre.days[-1].locations[-1], subtract = True))
                        if dist < EAT_DISTANCE + BASE_SENSE_DISTANCE * cre.sense:
                            if dist < claimed_food_dist:
                                claimed_food_dist = dist
                                claimed_food = food
                    #print(" Leaving a food for that creature ")
                    if claimed_food != None:
                        close_food.remove(claimed_food)

            #Who to eat?
            edible_creatures = [x for x in close_creatures if x.is_eaten == False and \
                                x.size * PREDATOR_SIZE_RATIO <= self.size and \
                                x.days[-1].home_time == None] #You're safe when you're home

            #Don't eat similar creatures you're nice to
            #if you're not about to starve
            #if len(day.has_eaten[-1]) > -1:

            edible_creatures = [x for x in edible_creatures if x not in to_be_nice_to]

            visible_food = edible_creatures + close_food

            for food in visible_food:
                try:
                    dist = vec_len(add_lists_by_element(
                        food.world_location,
                        day.locations[-1],
                        subtract = True
                    ))
                except:
                    print(food.world_location)
                    print(day.locations[-1])
                if dist < EAT_DISTANCE and len(day.has_eaten[-1]) < 2:
                    if isinstance(food, Creature):
                        food.days[-1].dead = True
                        food.days[-1].death_time = len(food.days[-1].locations)
                        for nom in food.days[-1].has_eaten[-1]:
                            day.has_eaten[-1].append(nom)
                    day.has_eaten[-1].append(food)
                    food.is_eaten = True
                    #TODO: Remove later to deal with ties.
                elif dist < EAT_DISTANCE + BASE_SENSE_DISTANCE * self.sense \
                    and dist < closest_food_dist:
                    closest_food_dist = dist
                    target_food = food

            #print(state)

            if target_food != None:
                vec_to_food = add_lists_by_element(
                    target_food.world_location,
                    day.locations[-1],
                    subtract = True
                )
                new_heading = math.atan2(vec_to_food[1], vec_to_food[0])

            #Wander around waiting to sense food.
            if state == 'foraging' and target_food == None:
                rand = uniform(-HEADING_TARGET_VARIATION, HEADING_TARGET_VARIATION)

                #Check whether creature is close to edge
                #Could make this more robust for non_square worlds if necessary
                TURN_DISTANCE = 60
                loc = day.locations[-1]
                if max(abs(loc[0]), abs(loc[1])) + TURN_DISTANCE > \
                                                    self.world.dimensions[0]:
                    ht = day.heading_targets[-1] #angle in radians
                    atc = math.atan2(loc[1], loc[0]) + math.pi #angle to center
                    correction = atc - ht

                    rand = correction

                new_heading = day.heading_targets[-1] + rand
                print(new_heading)


            #Check for predators. If one is close, abandon foraging and flee
            closest_pred_dist = math.inf
            threat = None
            #creatures = self.world.date_records[day.date]['creatures']
            predators = [x for x in close_creatures if \
                       x.size >= self.size * PREDATOR_SIZE_RATIO]# and \
                       #x.days[-1].home_time == None
                       #Predators can't eat when home. BUT THEY CAN.
                       #This makes small creatures avoid going to a predator's
                       #home, which would just make them get eaten immediatly
                       #in the morning.

            for pred in predators:
                try:
                    dist = vec_len(
                        add_lists_by_element(
                            pred.days[-1].locations[-1],
                            day.locations[-1],
                            subtract = True
                        )
                    )
                except:
                    print(pred.days[-1].locations[-1]),
                    print(day.locations[-1])
                    raise()
                if dist < closest_pred_dist:
                    closest_pred_dist = dist
                    threat = pred

            if threat != None:
                state = 'fleeing'

            if state == 'fleeing':
                #day.heading_targets.append(day.heading_targets[-1])

                vec_to_pred = add_lists_by_element(
                    threat.world_location,
                    day.locations[-1],
                    subtract = True
                )
                angle_to_pred = math.atan2(vec_to_pred[1], vec_to_pred[0])
                #print(angle_to_pred)
                new_heading = angle_to_pred + math.pi

            if state == 'homebound': #Creature is full or has eaten and is tired
                if self.world.dimensions[0] - abs(day.locations[-1][0]) < \
                   self.world.dimensions[1] - abs(day.locations[-1][1]):
                    #Go in x-direction
                    if day.locations[-1][0] > 0:
                        target = 0
                    else:
                        target = math.pi
                else:
                    if day.locations[-1][1] > 0:
                        target = math.pi / 2
                    else:
                        target = - math.pi / 2
                new_heading = target

            day.states.append(state)

            #Add new_heading to the heading_targets list
            day.heading_targets.append(new_heading)

            #Calculate heading
            #Note that lists are of different lengths in the line below
            heading_discrepancy = day.heading_targets[-1] - day.headings[-1]
            #Make sure abs(heading_discrepancy) <= 2pi
            while heading_discrepancy > math.pi:
                day.heading_targets[-1] -= 2 * math.pi
                heading_discrepancy = day.heading_targets[-1] - day.headings[-1]
            while heading_discrepancy < -math.pi:
                day.heading_targets[-1] += 2 * math.pi
                heading_discrepancy = day.heading_targets[-1] - day.headings[-1]

            if heading_discrepancy == 0:
                d_d_heading = 0
            else:
                d_d_heading = heading_discrepancy / abs(heading_discrepancy) \
                        * TURN_ACCELERATION
            day.d_headings.append(day.d_headings[-1] + d_d_heading)

            #Speed limit
            if day.d_headings[-1] > MAX_TURN_SPEED:
                day.d_headings[-1] = MAX_TURN_SPEED
            elif day.d_headings[-1] < -MAX_TURN_SPEED:
                day.d_headings[-1] = -MAX_TURN_SPEED
            #Prevent overshooting
            if heading_discrepancy == 0:
                day.d_headings[-1] = 0
            elif day.d_headings[-1] / heading_discrepancy > 1:
                day.d_headings[-1] = heading_discrepancy

            #No turning if you're out of energy or have gone home
            if has_energy == False or day.home_time != None:
                day.d_headings[-1] = 0

            day.headings.append(day.headings[-1] + day.d_headings[-1])

            """Update location"""
            #Go slower when turning, making it look more natural
            effective_speed = self.speed * SPEED_ADJUST_FACTOR * \
                (1 - pow(abs(day.d_headings[-1]) / MAX_TURN_SPEED, 2) / 2)
            #If outside world, just stop
            heading_vec = [math.cos(day.headings[-1]), math.sin(day.headings[-1]), 0]
            if (abs(day.locations[-1][0]) >= self.world.dimensions[0] or \
               abs(day.locations[-1][1]) >= self.world.dimensions[1]) and \
               dot_product(heading_vec, day.locations[-1]) > 0:
               effective_speed = 0
               if day.home_time == None and len(day.has_eaten[-1]) > 0:
                   day.home_time = len(day.locations)
            #No moving if you're out of energy
            if has_energy == False:
                effective_speed = 0
            day.locations.append([
                day.locations[-1][0] + math.cos(day.headings[-1]) * effective_speed / SIM_RESOLUTION,
                day.locations[-1][1] + math.sin(day.headings[-1]) * effective_speed / SIM_RESOLUTION,
                day.locations[-1][2]
            ])
            #prevent overshoot
            x_overshoot = abs(day.locations[-1][0]) - self.world.dimensions[0]
            if x_overshoot > 0:
                if day.locations[-1][0] > 0:
                    day.locations[-1][0] -= x_overshoot
                else:
                    day.locations[-1][0] += x_overshoot
            y_overshoot = abs(day.locations[-1][1]) - self.world.dimensions[1]
            if y_overshoot > 0:
                if day.locations[-1][1] > 0:
                    day.locations[-1][1] -= y_overshoot
                else:
                    day.locations[-1][1] += y_overshoot




            self.world_location = day.locations[-1]

            #Update energy
            day.energies.append(day.energies[-1] - self.energy_cost)

            """
            Plan
            - sense, speed^2, size^3
              - No running, 2x pred ratio
                - 100 food - Lots of small, fast creatures. Maybe 1/2 on average
                    with many in the 0.1 range.
                - 200 food - Size about 1 size on average.
                - 300 food - Size about 1.25 on average
              - No running, 1.2x pred ratio
                - 50 food - Size about 1 on average. (few creatures)
                - 100 food - Size about 1.25 on average
                - 200 food -
                - 300 food - 1.5 on average (and seems like it would go further)
              - No running, 1.5x pred ratio (Try if preds can't take hold)
                - 50 food - Size about 0.7 on average
                - 100 food -
                - 200 food -
                - 300 food - Average about 1.3
              - Running (Try if Bigs dominate too much. Not the case so far.)
                - 100 food -
                - 200 food -
                - 300 food -
            - sense, speed^2, size^2 (Try if bigs can't take hold.)
              -
            - sense, speed^2*size^3
              - No running, 1.2x pred ratio
                - 50 food -
                - 100 food -
                - 200 food -
                - 300 food - Over 1.5 size on average
            - sense, speed^2*size^3, size^3
              - No running, 1.2x pred ratio
                - 50 food - 0.75 average size after 15 gens. 0.9 after 30.
                - 100 food -
                - 200 food - Size 1.3-1.4 average after 30
                - 300 food - Size 1.3-1.4 average after 15 (Maybe still trending?)
              - With running, 1.2x pred ratio
                - 50 food - 0.7 avg size. Speed high.
                - 100 food -
                - 200 food -
                - 300 food - Size 1.3-1.4 average after 30. Speed is higher.

            """


    def eat_animation(self, start_time = None, end_time = None, time_step = 0.3):
        if start_time == None:
            raise Warning('Need to define start time and end time for eat animation')
        if end_time == None:
            end_time = start_time + 0.3 #Should make this a constant

        start_time = round(start_time * 60) / 60
        duration = 50 * time_step * SIM_RESOLUTION
        duration = max(round(duration * 60) / 60, 1/30)
        end_time = start_time + duration

        start_frame = start_time * FRAME_RATE
        end_frame = end_time * FRAME_RATE

        self.bobject.eat_animation(start_frame = start_frame, end_frame = end_frame)

    def add_to_blender(self, appear_time = None, world = None, transition_time = None):
        #Note that this is not a subclass of bobject
        if appear_time == None:
            raise Warning("Must define appear_time to add creature to Blender")
        if world == None:
            raise Warning("Must define world to add creature to Blender")

        cre_bobj = blobject.Blobject(
            location = scalar_mult_vec(
                self.days[0].locations[0],
                world.blender_units_per_world_unit
            ),
            scale = self.size * BASE_CREATURE_SCALE,
            rotation_euler = [0, 0, self.days[0].headings[0]],
            wiggle = True
        )
        #Rotate creature so a ref_obj rotation_euler of [0, 0, 0] results in
        #an x-facing blob standing in the z direction
        cre_bobj.ref_obj.children[0].rotation_euler = [math.pi / 2, 0, math.pi / 2]

        eyes = []
        for obj in cre_bobj.ref_obj.children[0].children:
            if 'Eye' in obj.name:
                eyes.append(obj)
        for eye in eyes:
            eye.scale = [
                self.sense,
                self.sense,
                self.sense,
            ]
            eye.keyframe_insert(data_path = 'scale', frame = appear_time * FRAME_RATE)


        self.bobject = cre_bobj
        #apply_material_by_speed(cre_bobj.ref_obj.children[0].children[0], 'creature_color3')
        self.apply_material_by_speed()
        if transition_time == None:
            cre_bobj.add_to_blender(appear_time = appear_time)
        else:
            cre_bobj.add_to_blender(
                appear_time = appear_time,
                transition_time = transition_time
            )

    def apply_material_by_speed(
        self,
        time = 0,
        bobj = None,
        spd = None,
        obj = None
    ):
        #2 -> Blue
        #6 -> Green
        #4 -> Yellow
        #3 -> Orange
        #5 -> Red

        #Kind of ridiculous. Should really just make this a more generalized
        #bobject method.
        if obj == None:
            if bobj == None:
                bobj = self.bobject
                spd = self.speed
                obj = self.bobject.ref_obj.children[0].children[0]
            else:
                obj = bobj.ref_obj.children[0]

        if spd < 1 - 3 * SPEED_PER_COLOR:
            color = COLORS_SCALED[0]
        elif spd < 1 - 2 * SPEED_PER_COLOR:
            #black to purple
            range_floor = 1 - 3 * SPEED_PER_COLOR
            mix = (spd - range_floor) / SPEED_PER_COLOR
            #color = mix_colors(COLORS_SCALED[6], COLORS_SCALED[4], mix)
            color = mix_colors(COLORS_SCALED[0], COLORS_SCALED[7], mix)
        elif spd < 1 - SPEED_PER_COLOR:
            #Purple to blue
            range_floor = 1 - 2 * SPEED_PER_COLOR
            mix = (spd - range_floor) / SPEED_PER_COLOR
            #color = mix_colors(COLORS_SCALED[6], COLORS_SCALED[4], mix)
            color = mix_colors(COLORS_SCALED[7], COLORS_SCALED[2], mix)
        elif spd < 1:
            #Blue to green
            range_floor = 1 - SPEED_PER_COLOR
            mix = (spd - range_floor) / SPEED_PER_COLOR
            #color = mix_colors(COLORS_SCALED[4], COLORS_SCALED[3], mix)
            color = mix_colors(COLORS_SCALED[2], COLORS_SCALED[6], mix)
        elif spd < 1 + SPEED_PER_COLOR:
            #Green to yellow
            range_floor = 1
            mix = (spd - range_floor) / SPEED_PER_COLOR
            color = mix_colors(COLORS_SCALED[6], COLORS_SCALED[4], mix)
            #color = mix_colors(COLORS_SCALED[3], COLORS_SCALED[5], mix)
        elif spd < 1 + 2 * SPEED_PER_COLOR:
            #Yellow to orange
            range_floor = 1 + SPEED_PER_COLOR
            mix = (spd - range_floor) / SPEED_PER_COLOR
            color = mix_colors(COLORS_SCALED[4], COLORS_SCALED[3], mix)
            #color = mix_colors(COLORS_SCALED[3], COLORS_SCALED[5], mix)
        elif spd < 1 + 3 * SPEED_PER_COLOR:
            #Orange to Red
            range_floor = 1 + 2 * SPEED_PER_COLOR
            mix = (spd - range_floor) / SPEED_PER_COLOR
            color = mix_colors(COLORS_SCALED[3], COLORS_SCALED[5], mix)
        elif spd < 1 + 4 * SPEED_PER_COLOR:
            #Red to white
            range_floor = 1 + 3 * SPEED_PER_COLOR
            mix = (spd - range_floor) / SPEED_PER_COLOR
            color = mix_colors(COLORS_SCALED[5], COLORS_SCALED[1], mix)
        else:
            color = COLORS_SCALED[1]


        apply_material(obj, 'creature_color1')
        bobj.color_shift(
            duration_time = None,
            color = color,
            start_time = time - 1 / FRAME_RATE,
            shift_time = 1 / FRAME_RATE,
            obj = obj
        )

        #Add speed property to bobject for reference when reusing bobjects
        bobj.speed = spd
        #Not actually used?

    def git_ate(self, **kwargs):
        diffs = super().git_ate(**kwargs)
        #When a creature is eaten, it corrects the position of the things it has
        #already eaten that day to offset the effect the grandparent relationship
        start_time = kwargs['start_time']

        has_eaten = self.days[-1].has_eaten
        if len(has_eaten) > 0 and has_eaten[-1] is not None:
            for eaten in has_eaten[-1]:
                corrected_loc = []
                for i, x in enumerate(eaten.bobject.ref_obj.location):
                    corrected_loc.append(x - diffs[0][i])

                corrected_rot = []
                for i, x in enumerate(eaten.bobject.ref_obj.rotation_euler):
                    corrected_rot.append(x - diffs[1][i])

                try:
                    #Change location and rotation
                    eaten.bobject.move_to(
                        start_time = start_time,
                        end_time = start_time + 1 / FRAME_RATE,
                        new_location = corrected_loc,
                        new_angle = corrected_rot
                    )
                except:
                    print(corrected_loc)
                    print(corrected_rot)
                    raise()

    def is_ancestor(self, creature):
        x = creature
        while x.parent != None:
            if x.parent == self:
                return True
            x = x.parent
        return False

class NaturalSim(object):
    """docstring for NaturalSim."""
    def __init__(
        self,
        food_count = 10,
        dimensions = WORLD_DIMENSIONS,
        day_length = DEFAULT_DAY_LENGTH,
        initial_creatures = None,
        mutation_switches = [True, True, True, True, False],
        initial_energy = STARTING_ENERGY,
        **kwargs
    ):
        self.food_count = food_count
        self.initial_energy = initial_energy
        self.dimensions = dimensions
        self.day_length = day_length
        self.date_records = []

        self.mutation_switches = mutation_switches
        print(self.mutation_switches)

        self.initial_creatures = []
        if isinstance(initial_creatures, list):
            self.initial_creatures = initial_creatures
        elif isinstance(initial_creatures, int):
            for i in range(initial_creatures):
                self.initial_creatures.append(
                    Creature(
                        size = 1 ,#+ randrange(-5, 6) * MUTATION_VARIATION,
                        speed = 2 ,#+ randrange(-5, 6) * MUTATION_VARIATION,
                        sense = 1 ,#+ randrange(-5, 6) * MUTATION_VARIATION
                    )
                )
        elif initial_creatures == None:
            num_creatures = math.floor(self.food_count * 1 / 2)
            for i in range(num_creatures):
                self.initial_creatures.append(
                    Creature(
                        size = 1 + randrange(-5, 6) * MUTATION_VARIATION,
                        speed = 1 + randrange(-5, 6) * MUTATION_VARIATION,
                        sense = 1 + randrange(-5, 6) * MUTATION_VARIATION
                    )
                )

            #Code for having a distribution of starting stats
            """
            step = 2 #Shortcut for messing with set of initial creatures.
            for i in range(-1, 2, step):
                for j in range(-1, 2, step):
                    for k in range(-1, 2, step):
                        #For some reason, I decided I wanted to make initial
                        #distributions based on colors. /shrug
                        self.initial_creatures.append(
                            Creature(
                                size = 1 + SPEED_PER_COLOR * 0,# * i,
                                speed = 1 + SPEED_PER_COLOR * 0,# * j,
                                sense = 1 + SPEED_PER_COLOR * 0,# * k,
                            )
                        )
                        self.initial_creatures.append(
                            Creature(
                                size = 1 + SPEED_PER_COLOR * 0,# * i,
                                speed = 1 + SPEED_PER_COLOR * 0,# * j,
                                sense = 1 + SPEED_PER_COLOR * 0,# * k,
                            )
                        )
            """
        for creature in self.initial_creatures:
            creature.world = self

    def gen_food(self):
        food = []
        for i in range(self.food_count):
            food.append(
                Food(
                    world_location = [
                        uniform(-self.dimensions[0], self.dimensions[0]),
                        uniform(-self.dimensions[1], self.dimensions[1]),
                        2
                    ],
                    world = self
                )
            )
        return food

    def get_newborn_creatures(self, parents = None):
        if parents == None:
            raise Warning('Must define parents and date for get_newborn_creatures')
        babiiieeesss = []
        for par in parents:
            if len(par.days[-1].has_eaten[-1]) > 1:
                speed_addition = 0
                if self.mutation_switches[0] == True:
                    if random() < MUTATION_CHANCE:
                        speed_addition = randrange(-1, 2, 2) * MUTATION_VARIATION
                size_addition = 0
                if self.mutation_switches[1] == True:
                    if random() < MUTATION_CHANCE:
                        size_addition = randrange(-1, 2, 2) * MUTATION_VARIATION
                sense_addition = 0
                if self.mutation_switches[2] == True:
                    if random() < MUTATION_CHANCE:
                        sense_addition = randrange(-1, 2, 2) * MUTATION_VARIATION
                kin_addition = 0
                if self.mutation_switches[3] == True:
                    if random() < MUTATION_CHANCE:
                        child_altruist = not par.altruist
                    else:
                        child_altruist = par.altruist
                if self.mutation_switches[4] == True:
                    if random() < MUTATION_CHANCE:
                        kin_addition = randrange(-1, 2, 2) * MUTATION_VARIATION
                        if par.kin_radius + kin_addition < 0:
                            kin_addition = 0
                baby = Creature(
                    parent = par,
                    world = par.world,
                    speed = par.speed + speed_addition,
                    size = par.size + size_addition,
                    sense = par.sense + sense_addition,
                    altruist = child_altruist,
                    kin_radius = par.kin_radius + kin_addition,
                )
                babiiieeesss.append(baby)

        return babiiieeesss

    def sim_next_day(
        self,
        save = False,
        filename = None,
        anim_durations = DEFAULT_ANIM_DURATIONS,
        custom_creature_set = None #For stringing separate sims together
    ):
        """Initialize date record"""
        date = len(self.date_records)
        print("Beginning sim for day " + str(date))

        if custom_creature_set == None:
            if date == 0:
                creatures = self.initial_creatures
            else:
                creatures = [x for x in self.date_records[-1]['creatures'] if x.days[-1].dead == False]
                creatures += self.get_newborn_creatures(parents = creatures)
        else:
            creatures = custom_creature_set

        #Set day length based on how long the longest creature can go
        day_length = 0
        for cre in creatures:
            stamina = self.initial_energy / (cre.energy_cost)
            if stamina > day_length:
                day_length = math.ceil(stamina)


        date_dict = {
            'date' : date,
            'food_objects' : self.gen_food(),
            'creatures' : creatures,
            'day_length' : day_length, #number of steps in day to show all creatures
            'anim_durations' : deepcopy(anim_durations)
        }
        self.date_records.append(date_dict)
        """print()
        for food in date_dict['food_objects']:
            print(food.world_location)
        print()"""

        """Conduct sim"""
        for cre in creatures:
            cre.new_day(date = date, parent = cre.parent)

        for t in range(date_dict['day_length']):
            for cre in creatures:
                #take step
                cre.take_step()

        #At end of day, see which creatures die
        #Also shorten day if all creatures are home or dead before the end
        latest_action = 0
        for cre in date_dict['creatures']:
            day = None
            bobj = cre.bobject
            for candidate_day in cre.days:
                if candidate_day.date == date:
                    day = candidate_day
                    break
            if day.dead == False:
                #Not enough food
                if len(day.has_eaten[-1]) == 0:
                   #print(str(cre) + " didn't eat enough")
                   day.dead = True

                #Didn't make it home
                if (abs(day.locations[-1][0]) < self.dimensions[0] and \
                   abs(day.locations[-1][1]) < self.dimensions[1]):
                   #print(str(cre) + " didn't make it home")
                   day.dead = True

            #Shorten for animation
            if day.death_time != None and day.death_time > latest_action:
                latest_action = day.death_time
                #print('New day length: ' + str(latest_action))
            if day.home_time != None and day.home_time > latest_action:
                latest_action = day.home_time
                #print('New day length: ' + str(latest_action))
            #print(date_dict['date'], latest_action)
            date_dict['day_length'] = latest_action

        for cre in self.date_records[-1]['creatures']:
            for day in cre.days:
                if day.date == date:
                    pass
                    #print('Date: ' + str(date))
                    #print('Dead time: ' + str(day.death_time))
                    #print('Home time: ' + str(day.home_time))
                    """print('Locations: ')
                    for loc in day.locations:
                        print(loc)"""
                    #print()

        if save == True:
            self.save_sim_result(filename)

    def save_sim_result(self, filename):
        if filename == None:
            now = datetime.datetime.now()
            name = "NAT" + now.strftime('%Y%m%dT%H%M%S')
        else:
            name = filename
        #name = 'test'
        result = os.path.join(
            SIM_DIR,
            name
        ) + ".pkl"
        if not os.path.exists(result):
            print("Writing simulation to %s" % (result))
            with open(result, "wb") as outfile:
                pickle.dump(self, outfile, pickle.HIGHEST_PROTOCOL)
        else:
            raise Warning(str(result) + " already exists")

class DrawnNaturalSim(Bobject):
    def __init__(
        self,
        *subbobjects,
        sim = None,
        save = False,
        blender_units_per_world_unit = BLENDER_UNITS_PER_WORLD_UNIT,
        day_length_style = 'fixed_speed', #Can also be 'fixed_length'
        **kwargs
    ):
        super().__init__(*subbobjects, **kwargs)
        self.day_length_style = day_length_style

        if isinstance(sim, NaturalSim):
            self.sim = sim
        elif isinstance(sim, str):
            result = os.path.join(
                SIM_DIR,
                sim
            ) + ".pkl"
            print(result)
            with open(result, 'rb') as input:
                print(input)
                self.sim = pickle.load(input)
            print("Loaded the world")
        elif sim == None:
            #I was previously passing on only certain kwargs, but I'm not sure
            #why I don't send them all. Makes it easier to use a new kwarg.
            """sim_kwargs = {}
            for param in ['food_count', 'dimensions', 'day_length']:
                if param in kwargs:
                    sim_kwargs[param] = kwargs[param]"""
            self.sim = NaturalSim(**kwargs)

        self.blender_units_per_world_unit = blender_units_per_world_unit
        #As written, changing this will change some proportions, since some
        #other constants depend on the default value

        self.reusable_food_bobjs = []
        self.reusable_cre_bobjs = []

    def animate_days(self, start_day, end_day):
        if end_day == None:
            end_day = len(self.sim.date_records) - 1
        for i in range(start_day, end_day + 1):
            date_record = self.sim.date_records[i]
            print("Animating day " + str(i))
            """Place food"""
            print(" Placing food")
            def place_food():
                for j, food in enumerate(date_record['food_objects']):
                    delay = j * date_record['anim_durations']['dawn'] / len(date_record['food_objects'])
                    duration_frames = min(
                        OBJECT_APPEARANCE_TIME,
                        date_record['anim_durations']['dawn'] * FRAME_RATE - delay * FRAME_RATE
                    )
                    if len(self.reusable_food_bobjs) == 0:
                        food.add_to_blender()
                        food.bobject.ref_obj.parent = self.ref_obj
                    else:
                        bobj = self.reusable_food_bobjs.pop()
                        bobj.scale = [FOOD_SCALE, FOOD_SCALE, FOOD_SCALE]
                        '''for cons in bobj.ref_obj.constraints:
                            cons.keyframe_insert(
                                data_path = 'influence',
                                frame = (self.start_time + self.elapsed_time + delay) * FRAME_RATE - 1
                            )
                            cons.influence = 0
                            cons.keyframe_insert(
                                data_path = 'influence',
                                frame = (self.start_time + self.elapsed_time + delay) * FRAME_RATE
                            )'''

                        food.bobject = bobj

                    starting_loc = scalar_mult_vec(
                        food.world_location,
                        self.blender_units_per_world_unit
                    )
                    #This line primes move_to to have food on first day start
                    #in the right place
                    if i == 0:
                        food.bobject.ref_obj.location = starting_loc
                    food.bobject.move_to(
                        new_location = starting_loc,
                        start_time = self.start_time + self.elapsed_time + delay - 1 / FRAME_RATE,
                        end_time = self.start_time + self.elapsed_time + delay
                    )

                    food.bobject.add_to_blender(
                        appear_time = self.start_time + self.elapsed_time + delay,
                        transition_time = duration_frames
                    )

            place_food()

            """Place new creatures"""
            print(" Placing creatures")
            def place_creatures():
                duration_frames = min(
                    OBJECT_APPEARANCE_TIME,
                    date_record['anim_durations']['dawn'] * FRAME_RATE
                )
                if date_record['date'] == start_day:
                    #print("  Adding new creatures on initial day")
                    for cre in date_record['creatures']:
                        cre.add_to_blender(
                            appear_time = self.start_time + self.elapsed_time,
                            world = self,
                            transition_time = duration_frames
                        )
                        cre.bobject.ref_obj.parent = self.ref_obj
                else:
                    #print("  Looking to reuse creature objects")
                    for cre in date_record['creatures']:
                        if cre not in self.sim.date_records[i - 1]['creatures']:
                            #print('   Found a creature that isn\'t in previous day')

                            reusables = [x for x in self.reusable_cre_bobjs if x.speed == cre.speed]
                            #if len(self.reusable_cre_bobjs) > 0:
                            if len(reusables) > 0:
                                #print('    Reusing a bobject')
                                bobj = reusables[-1]
                                #bobj = self.reusable_cre_bobjs[-1]
                                #print()
                                #print(bobj.name)
                                #print([x.name for x in self.reusable_cre_bobjs])
                                self.reusable_cre_bobjs.remove(bobj)
                                #print([x.name for x in self.reusable_cre_bobjs])
                                #print()


                                location = scalar_mult_vec(
                                    cre.days[0].locations[0],
                                    self.blender_units_per_world_unit
                                )
                                rotation_euler = [0, 0, cre.days[0].headings[0]]
                                bobj.move_to(
                                    new_location = location,
                                    new_angle = rotation_euler,
                                    start_time = self.start_time + self.elapsed_time - 1 / FRAME_RATE,
                                    end_time = self.start_time + self.elapsed_time
                                )

                                bobj.scale = [cre.size * BASE_CREATURE_SCALE] * 3
                                bobj.add_to_blender(
                                    appear_time = self.start_time + self.elapsed_time,
                                    transition_time = duration_frames
                                )

                                eyes = []
                                for obj in bobj.ref_obj.children[0].children:
                                    if 'Eye' in obj.name:
                                        eyes.append(obj)
                                for eye in eyes:
                                    eye.keyframe_insert(data_path = 'scale', frame = (self.start_time + self.elapsed_time) * FRAME_RATE - 1)
                                    eye.scale = [
                                        cre.sense,
                                        cre.sense,
                                        cre.sense,
                                    ]
                                    eye.keyframe_insert(data_path = 'scale', frame = (self.start_time + self.elapsed_time) * FRAME_RATE)

                                cre.bobject = bobj

                                #For some reason, this produces broken matertials
                                #So above, we just choose bobjects from creatures
                                #with the same speed. This takes more memory.
                                if cre.bobject.speed != cre.speed:
                                    cre.apply_material_by_speed(time = self.start_time + self.elapsed_time)

                            else:
                                #print('    Just making a new one')
                                cre.add_to_blender(
                                    appear_time = self.start_time + self.elapsed_time,
                                    world = self,
                                    transition_time = duration_frames
                                )
                                cre.bobject.ref_obj.parent = self.ref_obj

                    """cres = date_record['creatures']
                    for k in range(len(cres)):
                        for j in range(k):
                            if cres[k].bobject == cres[j].bobject:
                                #print(cres[k].bobject.name)
                                raise Warning('Two creatures are sharing a bobject')"""

                self.elapsed_time += date_record['anim_durations']['dawn'] + \
                                                date_record['anim_durations']['morning']


            place_creatures()

            """Step through time for current day"""
            print(" Animating movements")
            #print(date_record['day_length'])
            def step_through_day():
                if self.day_length_style == 'fixed_speed':
                    time_step = DEFAULT_DAY_ANIM_DURATION / DEFAULT_DAY_LENGTH
                elif self.day_length_style == 'fixed_length':
                    if date_record['day_length'] == 0:
                        self.elapsed_time += date_record['anim_durations']['day']
                        self.elapsed_time += date_record['anim_durations']['evening']
                        return
                    time_step = 1 / date_record['day_length'] * date_record['anim_durations']['day']

                #Reduce number of keyframes when there's two or more per frame.
                #Number of time steps in one frame
                key_every_n_t = math.floor(1 / FRAME_RATE / time_step)
                if key_every_n_t < 1:
                    key_every_n_t = 1
                #print(str(date_record['date']) + ' ' + str(len(date_record['creatures'])))
                for t in range(date_record['day_length']):
                    time_of_day = t * time_step
                    anim_time = self.start_time + self.elapsed_time + time_of_day
                    frame = anim_time * FRAME_RATE

                    #TODO: check for food eating ties. Eh, maybe not.

                    for cre in date_record['creatures']:
                        day = None
                        obj = cre.bobject.ref_obj

                        day = [x for x in cre.days if x.date == date_record['date']][0]
                        #The [0] is just a way of plucking the value from a list
                        #which should be of length 1

                        #If None, the creature was eaten by this point
                        if day.locations[t] != None:
                            if t % key_every_n_t == 0:
                                obj.location = scalar_mult_vec(
                                    day.locations[t],
                                    self.blender_units_per_world_unit
                                )
                                obj.keyframe_insert(data_path = 'location', frame = frame)
                                obj.rotation_euler = [0, 0, day.headings[t]]
                                obj.keyframe_insert(data_path = 'rotation_euler', frame = frame)

                            #Old version that called git_ate on all new food,
                            #Even if it's food that was actually eaten previously
                            #by the creature currently being eaten. Resulted in
                            #unnecessary and problematic position corrections.
                            #Keeping as comment for now in case new version is
                            #problematic too.
                            """for food in day.has_eaten[t]:
                                if food not in day.has_eaten[t-1]:
                                    food.git_ate(
                                        eater = cre,
                                        start_time = anim_time,
                                        drawn_world = self,
                                        time_step = time_step
                                    )"""
                            #May cause bugs if a creature eats two things on the
                            #same time step.
                            if len(day.has_eaten[t]) > 0:
                                last_eaten = day.has_eaten[t][-1]
                                if last_eaten not in day.has_eaten[t-1]:
                                    last_eaten.git_ate(
                                        eater = cre,
                                        start_time = anim_time,
                                        drawn_world = self,
                                        time_step = time_step
                                    )
                                    if isinstance(last_eaten, Creature):
                                        pass
                                        #There's another place where creatures are
                                        #added to the reusable pile.
                                        #self.reusable_cre_bobjs.append(last_eaten.bobject)
                                    else:
                                        self.reusable_food_bobjs.append(last_eaten.bobject)

                ''' Older version that didn't update date record if speed is fixed
                if self.day_length_style == 'fixed_length':
                    self.elapsed_time += date_record['anim_durations']['day']
                elif self.day_length_style == 'fixed_speed':
                    self.elapsed_time += date_record['day_length'] * time_step'''
                if self.day_length_style == 'fixed_speed':
                    date_record['anim_durations']['day'] = date_record['day_length'] * time_step
                self.elapsed_time += date_record['anim_durations']['day']

                self.elapsed_time += date_record['anim_durations']['evening']


            step_through_day()

            """Creatures that die should disappear."""
            """Along with food"""
            print(" Cleaning up")
            def clean_up():
                duration_frames = min(
                    OBJECT_APPEARANCE_TIME,
                    date_record['anim_durations']['night'] * FRAME_RATE
                )
                for cre in date_record['creatures']:
                    day = None
                    for cons in cre.bobject.ref_obj.constraints:
                        if cons.influence == 1:
                            cons.keyframe_insert(
                                data_path = 'influence',
                                frame = (self.start_time + self.elapsed_time + date_record['anim_durations']['night']) * FRAME_RATE - 1
                            )
                            cons.influence = 0
                            cons.keyframe_insert(
                                data_path = 'influence',
                                frame = (self.start_time + self.elapsed_time + date_record['anim_durations']['night']) * FRAME_RATE
                            )
                    for candidate_day in cre.days:
                        if candidate_day.date == date_record['date']:
                            day = candidate_day
                            break
                    if day.dead == True:
                        cre.bobject.disappear(
                            disappear_time = self.start_time + self.elapsed_time + date_record['anim_durations']['night'],
                            #is_creature = True,
                            duration_frames = duration_frames
                        )
                        #if cre.is_eaten = False:
                        self.reusable_cre_bobjs.append(cre.bobject)
                    else:
                        cre.bobject.move_to(
                            new_angle = [
                                cre.bobject.ref_obj.rotation_euler[0],
                                cre.bobject.ref_obj.rotation_euler[1],
                                cre.bobject.ref_obj.rotation_euler[2] + math.pi
                            ],
                            start_time = self.start_time + self.elapsed_time,
                            end_time = self.start_time + self.elapsed_time + date_record['anim_durations']['night']
                        )
                        try: #This is for putting surviving creatures away if the
                             #next day is actually another sim.
                            next_day = self.sim.date_records[i + 1]
                            if cre not in next_day['creatures']:
                                cre.bobject.disappear(
                                    disappear_time = self.start_time + self.elapsed_time + date_record['anim_durations']['night'],
                                    #is_creature = True,
                                    duration_frames = duration_frames
                                )
                                self.reusable_cre_bobjs.append(cre.bobject)

                        except:
                            pass

                for food in date_record['food_objects']:
                    for cons in food.bobject.ref_obj.constraints:
                        cons.keyframe_insert(
                            data_path = 'influence',
                            frame = (self.start_time + self.elapsed_time + date_record['anim_durations']['night']) * FRAME_RATE - 1
                        )
                        cons.influence = 0
                        cons.keyframe_insert(
                            data_path = 'influence',
                            frame = (self.start_time + self.elapsed_time + date_record['anim_durations']['night']) * FRAME_RATE
                        )
                    if food.is_eaten == False:
                        food.bobject.disappear(
                            disappear_time = self.start_time + self.elapsed_time + date_record['anim_durations']['night'],
                            duration_frames = duration_frames / 2
                        )
                        self.reusable_food_bobjs.append(food.bobject)

                self.elapsed_time += date_record['anim_durations']['night']

            clean_up()

    def add_to_blender(
        self,
        start_delay = 1,
        start_day = 0,
        end_day = None,
        **kwargs
    ):
        if 'appear_time' not in kwargs:
            raise Warning('Need appear_time to add natural sim.')
        self.start_time = kwargs['appear_time']

        self.elapsed_time = start_delay #Will add to this as phases are
                                             #animated to keep them sequential

        plane = import_object(
            'xyplane', 'primitives',
            scale = [
                self.sim.dimensions[0] * self.blender_units_per_world_unit,
                self.sim.dimensions[1] * self.blender_units_per_world_unit,
                0
            ],
            location = (0, 0, 0),
            name = 'sim_plane'
        )
        apply_material(plane.ref_obj.children[0], 'color2')
        self.add_subbobject(plane)

        super().add_to_blender(**kwargs)
        #execute_and_time(
        #    'Animated day',
        self.animate_days(start_day, end_day),
        #
