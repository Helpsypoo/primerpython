#import bpy
import imp
from random import random, uniform
from copy import copy

import bobject
imp.reload(bobject)
from bobject import *

import helpers
imp.reload(helpers)
from helpers import *

DEFAULT_DAY_LENGTH = 400
DEFAULT_DAY_ANIM_DURATION = 5 #seconds
BLENDER_UNITS_PER_WORLD_UNIT = 1 / 20
WORLD_DIMENSIONS = [100, 100]
CREATURE_HEIGHT = 13

HEADING_TARGET_VARIATION = 0.4 #Range for random heading target changes, radians
MAX_TURN_SPEED = 0.07
TURN_ACCELERATION = 0.005

BASE_SENSE_DISTANCE = 50
EAT_DISTANCE = 25

STARTING_ENERGY = 2000

"""
TODOs
- Break eating ties (Not sure if necessary)
- Figure out why food is sometimes underneath
- Make creatures immune to being eaten if they are home
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

        if isinstance(parents, list):
            self.parents = parents
        else:
            self.parents = [parents]

        self.bobject = import_object(
            'goodicosphere', 'primitives',
            #world_location = [0, 0, 0],
            location = [0, 0, 0],
            scale = 0.15
        )
        apply_material(self.bobject.ref_obj.children[0], 'color7')

        for parent in self.parents:
            self.make_child_of_constraint(parent = parent.ref_obj)
        if len(self.parents) > 0:
            cons = self.bobject.ref_obj.constraints[0]
            cons.influence = 1
            """if has_world_as_parent == True:
                cons.use_scale_x = True
                cons.use_scale_y = True
                cons.use_scale_z = True"""

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
        start_time = round(start_time * 60) / 60
        duration = 50 * time_step
        duration = max(round(duration * 60) / 60, 1/30)
        end_time = start_time + duration

        if drawn_world == None:
            raise Warning('Need to define drawn_world for git_ate')

        if eater == None:
            raise Warning("Need to define eater")
        if eater not in self.parents:
            self.make_child_of_constraint(parent = eater.bobject.ref_obj)

        for cons in self.bobject.ref_obj.constraints:
            cons.keyframe_insert(data_path = 'influence', frame = start_time * FRAME_RATE)
            if cons.target == eater.bobject.ref_obj:
                cons.influence = 1
            else:
                cons.influence = 0
            cons.keyframe_insert(data_path = 'influence', frame = start_time * FRAME_RATE + 1)

        bpy.context.scene.update() #needed for matrix_world to be accurate

        loc_in_new_ref_frame = eater.bobject.ref_obj.matrix_local.inverted() * \
                                    self.bobject.ref_obj.location

        #Need to correct scale because the child_of constraint doesn't use scale
        for i in range(len(loc_in_new_ref_frame)):
            loc_in_new_ref_frame[i] *= eater.bobject.ref_obj.scale[i]

        #Change location to be the same in new reference frame
        self.bobject.move_to(
            start_time = start_time,
            end_time = start_time + 1 / FRAME_RATE,
            new_location = loc_in_new_ref_frame
        )
        #Move in front of creature
        self.bobject.move_to(
            start_time = start_time + 1 / FRAME_RATE,
            end_time = start_time + duration / 2,
            new_location = [
                eater.bobject.ref_obj.scale[2],
                0,
                eater.bobject.ref_obj.scale[2] / 5
            ]
        )
        #Move into creature and shrink
        self.bobject.move_to(
            start_time = start_time + duration / 2,
            end_time = end_time,
            new_location = [
                0,
                0,
                eater.bobject.ref_obj.scale[2] / 5
            ],
            new_scale = 0
        )

        eater.eat_animation(start_time = start_time, time_step = time_step)
        eater.bobject.blob_scoop(start_time = start_time, duration = time_step * 50)
        #I don't remember why I'm multiplying things by 50, tbh, but it works.
        #I'm good at coding.

    def make_child_of_constraint(self, parent = None):
        if self.bobject == None:
            raise Warning('Food needs a bobject to get parent')
        cons = self.bobject.ref_obj.constraints.new('CHILD_OF')
        cons.use_scale_x = False
        cons.use_scale_y = False
        cons.use_scale_z = False

        cons.influence = 0

        if parent == None:
            raise Warning('Need parent for child_of constraint')
        cons.target = parent

class Creature(Food):
    def __init__(
        self,
        speed = 1,
        size = 1,
        sense = 1,
        parent = None,
        world = None
    ):
        super().__init__()
        self.speed = speed
        self.size = size
        self.sense = sense
        self.parent = parent

        self.days = []

        self.bobject = None
        self.world = world

    def new_day(self, date = 0):
        new_day = CreatureDay(creature = self, date = date)
        if len(self.days) == 0:
            wall_roll = random()
            if wall_roll < 0.25:
                loc = [
                    uniform(-self.world.dimensions[0], self.world.dimensions[0]),
                    self.world.dimensions[1],
                    CREATURE_HEIGHT * self.size
                ]
                heading_target = - math.pi / 2
                heading = - math.pi / 2
            if wall_roll < 0.5:
                loc = [
                    self.world.dimensions[0],
                    uniform(-self.world.dimensions[1], self.world.dimensions[1]),
                    CREATURE_HEIGHT * self.size
                ]
                heading_target = math.pi
                heading = math.pi
            if wall_roll < 0.75:
                loc = [
                    uniform(-self.world.dimensions[0], self.world.dimensions[0]),
                    -self.world.dimensions[1],
                    CREATURE_HEIGHT * self.size
                ]
                heading_target = math.pi / 2
                heading = math.pi / 2
            else:
                loc = [
                    -self.world.dimensions[0],
                    uniform(-self.world.dimensions[1], self.world.dimensions[1]),
                    CREATURE_HEIGHT * self.size
                ]
                heading_target = 0
                heading = 0

            new_day.locations.append(loc)
            new_day.heading_targets.append(heading_target)
            new_day.d_headings.append(0)
            new_day.headings.append(heading)
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
        new_day.energies.append(STARTING_ENERGY)

        self.days.append(new_day)

    def take_step(self):
        day = self.days[-1]
        has_energy = True
        if day.energies[-1] == None:
            has_energy = False
        else:
            distance_left = day.energies[-1] / (self.size + self.speed + self.sense)
            if distance_left < 1:
                has_energy = False
        if has_energy == False and day.death_time == None and day.home_time == None:
            day.death_time = len(day.locations)

        if self.days[-1].dead == True:
            day.heading_targets.append(None)
            day.d_headings.append(None)
            day.headings.append(None)
            day.locations.append(None)
            day.has_eaten.append(None)
            day.energies.append(None)
        else:
            day.has_eaten.append(copy(day.has_eaten[-1])) #Append new eaten state to fill with food and

            """Update heading"""
            #Sense food
            closest_food = math.inf
            target_food = None
            food_objects = self.world.date_records[day.date]['food_objects']
            creatures = self.world.date_records[day.date]['creatures']
            uneaten = [x for x in food_objects if x.is_eaten == False] + \
                      [x for x in creatures if x.is_eaten == False and x.size < self.size]

            state = None
            distance_out = max(
                self.world.dimensions[0] - abs(day.locations[-1][0]),
                self.world.dimensions[1] - abs(day.locations[-1][1]),
            )
            if len(day.has_eaten[-1]) == 0:
                state = 'foraging'
            elif len(day.has_eaten[-1]) == 1:
                if distance_left > distance_out:
                    state = 'foraging'
                else:
                    state = 'homebound'
            elif len(day.has_eaten[-1]) > 1:
                state = 'homebound'
            else:
                raise Warning('Somehow, the creature has eaten negative food')

            if state == 'foraging':
                for food in uneaten:
                    dist = vec_len(add_lists_by_element(
                        food.world_location,
                        day.locations[-1],
                        subtract = True
                    ))
                    if dist < EAT_DISTANCE:
                        day.has_eaten[-1].append(food)
                        food.is_eaten = True
                        if isinstance(food, Creature):
                            food.days[-1].dead = True
                            food.days[-1].death_time = len(food.days[-1].locations)
                            for nom in food.days[-1].has_eaten[-1]:
                                day.has_eaten[-1].append(nom)
                        #TODO: Remove later to deal with ties.
                    elif dist < BASE_SENSE_DISTANCE * self.sense and dist < closest_food:
                        closest_food = dist
                        target_food = food

                if target_food != None:
                    vec_to_food = add_lists_by_element(
                        food.world_location,
                        day.locations[-1],
                        subtract = True
                    )
                    day.heading_targets.append(math.atan2(vec_to_food[1], vec_to_food[0]))
                else:
                    #Random change to heading target
                    rand = uniform(-HEADING_TARGET_VARIATION, HEADING_TARGET_VARIATION)
                    #Change away from straight out
                    out = get_unit_vec(day.locations[-1])
                    heading_target_vec = [
                        math.cos(day.heading_targets[-1]),
                        math.sin(day.heading_targets[-1]),
                        0
                    ]
                    ht_norm = get_unit_vec(heading_target_vec)
                    dot = dot_product(out, ht_norm)
                    cross = cross_product(out, ht_norm)
                    closeness = vec_len(day.locations[-1]) / \
                                            dot_product(out, self.world.dimensions + [0])
                    inward = 0
                    if dot > 0: #Overall heading out
                        if vec_len(cross) > 0:
                            #Positive angle change
                            #Full size at the barrier and when heading straight out
                            inward = 1.2 * HEADING_TARGET_VARIATION * dot * closeness ** 2
                        else:
                            inward = - 1.2 * HEADING_TARGET_VARIATION * dot * closeness ** 2
                            #The 1.2 is a strengthening tweak


                    day.heading_targets.append(day.heading_targets[-1] + rand + inward)

            elif state == 'homebound': #Creature is full
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
                day.heading_targets.append(target)


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
                d_d_heading = heading_discrepancy / abs(heading_discrepancy) * TURN_ACCELERATION
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

            #No turning if you're out of energy
            if has_energy == False:
                day.d_headings[-1] = 0

            day.headings.append(day.headings[-1] + day.d_headings[-1])

            """Update location"""
            #Go slower when turning, making it look more natural
            effective_speed = self.speed * \
                (1 - pow(abs(day.d_headings[-1]) / MAX_TURN_SPEED, 2) / 2)
            #If outside world, just stop
            heading_vec = [math.cos(day.headings[-1]), math.sin(day.headings[-1]), 0]
            if (abs(day.locations[-1][0]) > self.world.dimensions[0] or \
               abs(day.locations[-1][1]) > self.world.dimensions[1]) and \
               dot_product(heading_vec, day.locations[-1]) > 0:
               effective_speed = 0
               if day.home_time == None:
                   day.home_time = len(day.locations)
            #No moving if you're out of energy
            if has_energy == False:
                effective_speed = 0
            day.locations.append([
                day.locations[-1][0] + math.cos(day.headings[-1]) * effective_speed,
                day.locations[-1][1] + math.sin(day.headings[-1]) * effective_speed,
                day.locations[-1][2]
            ])
            self.world_location = day.locations[-1]
            day.energies.append(day.energies[-1] - self.size - self.speed - self.sense)

    def eat_animation(self, start_time = None, end_time = None, time_step = 0.3):
        if start_time == None:
            raise Warning('Need to define start time and end time for eat animation')
        if end_time == None:
            end_time = start_time + 0.3 #Should make this a constant

        start_time = round(start_time * 60) / 60
        duration = 50 * time_step
        duration = max(round(duration * 60) / 60, 1/30)
        end_time = start_time + duration

        start_frame = start_time * FRAME_RATE
        end_frame = end_time * FRAME_RATE
        #I parented the mouth in a pretty ridicukous way, but it works.
        for child in self.bobject.ref_obj.children[0].children:
            if 'Mouth' in child.name:
                mouth = child

        o_loc = copy(mouth.location)
        o_rot = copy(mouth.rotation_euler)
        o_scale = copy(mouth.scale)

        mouth.keyframe_insert(data_path = 'location', frame = start_frame)
        mouth.keyframe_insert(data_path = 'rotation_euler', frame = start_frame)
        mouth.keyframe_insert(data_path = 'scale', frame = start_frame)

        mouth.location = [-0.04, 0.36, 0.3760]
        mouth.rotation_euler = [
            -8.91 * math.pi / 180,
            -0.003 * math.pi / 180,
            -3.41 * math.pi / 180,
        ]
        mouth.scale = [
            0.853,
            2.34,
            0.889
        ]

        mouth.keyframe_insert(data_path = 'location', frame = (start_frame + end_frame) / 2)
        mouth.keyframe_insert(data_path = 'rotation_euler', frame = (start_frame + end_frame) / 2)
        mouth.keyframe_insert(data_path = 'scale', frame = (start_frame + end_frame) / 2)

        mouth.location = o_loc
        mouth.rotation_euler = o_rot
        mouth.scale = o_scale

        mouth.keyframe_insert(data_path = 'location', frame = end_frame)
        mouth.keyframe_insert(data_path = 'rotation_euler', frame = end_frame)
        mouth.keyframe_insert(data_path = 'scale', frame = end_frame)

    def add_to_blender(self, appear_time = None, world = None):
        #Note that this is not a subclass of bobject
        if appear_time == None:
            raise Warning("Must define appear_time to add creature to Blender")
        if world == None:
            raise Warning("Must define world to add creature to Blender")

        cre_bobj = import_object(
            'boerd_blob', 'creatures',
            location = scalar_mult_vec(
                self.days[0].locations[0],
                world.blender_units_per_world_unit
            ),
            scale = self.size,
            rotation_euler = [0, 0, self.days[0].headings[0]]
        )
        #Rotate creature so a ref_obj rotation_euler of [0, 0, 0] results in
        #an x-facing blob standing in the z direction
        cre_bobj.ref_obj.children[0].rotation_euler = [math.pi / 2, 0, math.pi / 2]

        #TODO: Make color depend on speed
        apply_material(cre_bobj.ref_obj.children[0].children[0], 'color3')

        #TODO: Make eye size depend on sense

        self.bobject = cre_bobj
        cre_bobj.add_to_blender(appear_time = appear_time)

class NaturalSim(object):
    """docstring for NaturalSim."""
    def __init__(
        self,
        food_count = 10,
        dimensions = WORLD_DIMENSIONS,
        day_length = DEFAULT_DAY_LENGTH,
        initial_creatures = None
    ):
        self.food_count = food_count
        self.dimensions = dimensions
        self.day_length = day_length
        self.date_records = []

        self.initial_creatures = initial_creatures
        if self.initial_creatures == None:
            self.initial_creatures = [
                Creature(),
                Creature(size = 0.5),
                Creature(size = 1.5),
                Creature(size = 0.25),
                Creature(size = 2),
            ]
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
                        3
                    ],
                    world = self
                )
            )

        return food

    def sim_next_day(self):
        """Initialize date record"""
        date = len(self.date_records)

        if date == 0:
            creatures = self.initial_creatures
        else:
            creatures = [x for x in self.date_records[-1]['creatures'] if x.days[-1].dead == False]
            #TODO: add new creatures from reproduction

        #Set day length based on how long the longest creature can go
        day_length = 0
        for cre in creatures:
            stamina = STARTING_ENERGY / (cre.size + cre.speed + cre.sense)
            if stamina > day_length:
                day_length = math.ceil(stamina)
        #day_length += 10 #Padding

        date_dict = {
            'date' : date,
            'food_objects' : self.gen_food(),
            'creatures' : creatures,
            'day_length' : day_length, #number of steps in day to show all creatures
            'anim_durations' : {
                'dawn' : 1, #Put out food
                'morning' : 1, #pause after setup
                'day' : DEFAULT_DAY_ANIM_DURATION, #creatures go at it
                'evening' : 1, #pause before reset
                'night' : 1 #reset
            }
        }
        self.date_records.append(date_dict)

        """Conduct sim"""
        for cre in creatures:
            cre.new_day(date = date)

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
                   print(str(cre) + " didn't eat enough")
                   day.dead = True

                #Didn't make it home
                if (abs(day.locations[-1][0]) < self.dimensions[0] and \
                   abs(day.locations[-1][1]) < self.dimensions[1]):
                   print(str(cre) + " didn't make it home")
                   day.dead = True

            #Shorten for animation
            if day.death_time != None and day.death_time > latest_action:
                latest_action = day.death_time
                print('New day length: ' + str(latest_action))
            if day.home_time != None and day.home_time > latest_action:
                latest_action = day.home_time
                print('New day length: ' + str(latest_action))
            print(date_dict['date'], latest_action)
            date_dict['day_length'] = latest_action

        for cre in self.date_records[-1]['creatures']:
            for day in cre.days:
                if day.date == date:
                    print('Date: ' + str(date))
                    print('Dead time: ' + str(day.death_time))
                    print('Home time: ' + str(day.home_time))
                    """print('Locations: ')
                    for loc in day.locations:
                        print(loc)"""
                    print()

class DrawnNaturalSim(Bobject):
    def __init__(
        self,
        *subbobjects,
        sim = None,
        blender_units_per_world_unit = BLENDER_UNITS_PER_WORLD_UNIT,
        day_length_style = 'fixed_speed', #Can also be 'fixed_length'
        **kwargs
    ):
        super().__init__(*subbobjects, **kwargs)
        self.sim = sim
        self.day_length_style = day_length_style
        if self.sim == None:
            sim_kwargs = {}
            for param in ['food_count', 'dimensions', 'day_length']:
                if param in kwargs:
                    sim_kwargs[param] = kwargs[param]
            self.sim = NaturalSim(**sim_kwargs)

        self.blender_units_per_world_unit = blender_units_per_world_unit

    def animate_days(self):
        for i, date_record in enumerate(self.sim.date_records):
            """Place food"""
            for j, food in enumerate(date_record['food_objects']):
                food.bobject.ref_obj.location = scalar_mult_vec(
                    food.world_location,
                    self.blender_units_per_world_unit
                )
                food.bobject.ref_obj.parent = self.ref_obj
                delay = j * date_record['anim_durations']['dawn'] / len(date_record['food_objects'])
                food.bobject.add_to_blender(
                    appear_time = self.start_time + self.elapsed_time + delay
                )

            """Place new creatures"""

            if date_record['date'] == 0:
                for cre in date_record['creatures']:
                    cre.add_to_blender(
                        appear_time = self.start_time + self.elapsed_time,
                        world = self
                    )
                    cre.bobject.ref_obj.parent = self.ref_obj
            else:
                for cre in date_record['creatures']:
                    if cre not in self.sim.date_records[i - 1]['creatures']:
                        cre.add_to_blender(
                            appear_time = self.start_time + self.elapsed_time,
                            world = self
                        )
                        cre.bobject.ref_obj.parent = self.ref_obj

            self.elapsed_time += date_record['anim_durations']['dawn'] + \
                                            date_record['anim_durations']['morning']

            """Step through time for current day"""
            #print(date_record['day_length'])
            if self.day_length_style == 'fixed_speed':
                time_step = 1 / DEFAULT_DAY_LENGTH * DEFAULT_DAY_ANIM_DURATION
            elif self.day_length_style == 'fixed_length':
                time_step = 1 / date_record['day_length'] * date_record['anim_durations']['day']
            for t in range(date_record['day_length']):
                time_of_day = t * time_step
                anim_time = self.start_time + self.elapsed_time + time_of_day
                frame = anim_time * FRAME_RATE

                #TODO: check for food eating ties

                for cre in date_record['creatures']:
                    day = None
                    obj = cre.bobject.ref_obj
                    for candidate_day in cre.days:
                        if candidate_day.date == date_record['date']:
                            day = candidate_day
                            break

                    #If None, the creature was eaten by this point
                    if day.locations[t] != None:
                        obj.location = scalar_mult_vec(
                            day.locations[t],
                            self.blender_units_per_world_unit
                        )
                        obj.keyframe_insert(data_path = 'location', frame = frame)
                        obj.rotation_euler = [0, 0, day.headings[t]]
                        obj.keyframe_insert(data_path = 'rotation_euler', frame = frame)

                        for food in day.has_eaten[t]:
                            if food not in day.has_eaten[t-1]:
                                food.git_ate(
                                    eater = cre,
                                    start_time = anim_time,
                                    drawn_world = self,
                                    time_step = time_step
                                )

            if self.day_length_style == 'fixed_length':
                self.elapsed_time += date_record['anim_durations']['day']
            elif self.day_length_style == 'fixed_speed':
                self.elapsed_time += date_record['day_length'] * time_step
            self.elapsed_time += date_record['anim_durations']['evening']

            """Creatures that die should disappear."""
            """Along with food"""
            for cre in date_record['creatures']:
                day = None
                for candidate_day in cre.days:
                    if candidate_day.date == date_record['date']:
                        day = candidate_day
                        break
                if day.dead == True:
                    cre.bobject.disappear(
                        disappear_time = self.start_time + self.elapsed_time,
                        is_creature = True
                    )

            for food in date_record['food_objects']:
                food.bobject.disappear(
                    disappear_time = self.start_time + self.elapsed_time
                )

            self.elapsed_time += date_record['anim_durations']['night']




    def add_to_blender(
        self,
        start_delay = 1,
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
        self.animate_days()
