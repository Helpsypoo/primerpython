import bpy
import imp
#from random import random, randrange, choice, gauss, uniform
#from copy import copy
import pickle

import bobject
imp.reload(bobject)
from bobject import Bobject

#from graph_bobject import GraphBobject

from blobject import Blobject

import helpers
imp.reload(helpers)
from helpers import *


BASE_CREATURE_SCALE = 0.05
CREATURE_HEIGHT_FACTOR = 0.8
#CREATURE_HOME_DISTANCE = 1.2

BASE_FOOD_SCALE = 0.05
FOOD_PATTERN_MULTIPLE = 6 #Geometry of food pattern
FOOD_PATTERN_ANGLE_OFFSET = 6
FOOD_EDGE_RATIO = 0.8

CREATURE_MOVE_DURATION = 0.5
PAUSE_LENGTH = 0.25

class DrawnCreature(Blobject):
    """docstring for DrawnCreature."""

    def __init__(
        self,
        creature = None,
        **kwargs
    ):
        super().__init__(**kwargs)
        self.creature = creature
        if self.creature == None:
            raise Warning('DrawnCreature needs creature.')

class DrawnFood(Bobject):
    def __init__(self, object_model, **kwargs):
        super().__init__(
            objects = [object_model.copy()],
            name = 'food',
            **kwargs
        )

class DrawnWorld(Bobject):
    """docstring for DrawnWorld."""

    def __init__(
        self,
        sim = None,
        phase_durations = {
            'day_prep' : CREATURE_MOVE_DURATION,
            'creatures_go_out' : CREATURE_MOVE_DURATION,
            'pause_before_contest' : PAUSE_LENGTH,
            'contest' : CREATURE_MOVE_DURATION,
            'pause_before_home' : PAUSE_LENGTH,
            'creatures_go_home' : CREATURE_MOVE_DURATION,
            'pause_before_reset' : PAUSE_LENGTH,
            'food_disappear' : CREATURE_MOVE_DURATION,
        },
        scale = 5,
        creature_scale = None,
        name = 'world',
        loud = False,
        **kwargs
    ):
        super().__init__(scale = scale, name = name)

        if sim == None:
            raise Warning('DrawnWorld needs a market sim to draw')
        elif isinstance(sim, str):
            result = os.path.join(
                SIM_DIR,
                sim
            ) + ".pkl"
            if loud:
                print(result)
            with open(result, 'rb') as input:
                if loud:
                    print(input)
                self.sim = pickle.load(input)
            if loud:
                print("Loaded the world")
        else:
            self.sim = sim

        self.phase_durations = phase_durations

        #Initialize drawn_creature property of creature objects
        for day in sim.calendar:
            for cre in day.creatures:
                cre.drawn_creature = None

        self.drawn_creatures = []
        self.creature_scale = creature_scale
        if self.creature_scale == None:
            self.creature_scale = BASE_CREATURE_SCALE
            ##TODO: make this depend on food count.

        self.elapsed_time = 0

        food_bobject_model = import_object(
            'goodicosphere', 'primitives',
            color = 'color6'
        )
        self.food_object_model = food_bobject_model.ref_obj.children[0]

        self.linked_graph = None

    def add_to_blender(self, appear_time = None, **kwargs):
        if appear_time == None:
            raise Warning('Need appear_time for DrawnWorld.add_to_blender()')

        self.appear_time = appear_time

        floor = import_object(
            'disc', 'primitives',
            location = [0, 0, 0],
            name = 'ground'
        )
        apply_material(floor.ref_obj.children[0], 'color2')
        self.add_subbobject(floor)
        super().add_to_blender(appear_time = self.appear_time, **kwargs)

        '''self.draw_initial_creatures(
            start_time = self.appear_time + OBJECT_APPEARANCE_TIME / FRAME_RATE
        )'''

        '''self.set_food(
            start_time = self.appear_time + OBJECT_APPEARANCE_TIME / FRAME_RATE,
            day = self.sim.calendar[0]
        )'''

    def update_creatures(
        self,
        start_time = None,
        end_time = None,
        day = None
    ):
        if start_time == None:
            raise Warning('Need start_time for update_creatures')
        if end_time == None:
            end_time = start_time + OBJECT_APPEARANCE_TIME / FRAME_RATE

        creatures = day.creatures #self.sim.calendar[0].creatures
        angle_inc = 2 * math.pi / len(creatures)
        radius = 1 - self.creature_scale

        old_creatures = []

        #new creatures
        #doing these first to avoid updating positions of old creatures so new
        #creatures can appear to come from old ones.
        for i, cre in enumerate(creatures):
            angle = i * angle_inc

            if cre.drawn_creature != None:
                old_creatures.append(cre)
            else:
                destination = [
                    radius * math.cos(math.pi / 2 + angle),
                    radius * math.sin(math.pi / 2 + angle),
                    self.creature_scale * CREATURE_HEIGHT_FACTOR
                ]

                if day.date == 0:
                    start_loc = destination
                else:
                    start_loc = cre.parent.drawn_creature.ref_obj.location


                d_cre = DrawnCreature(
                    creature = cre,
                    location = start_loc,
                    rotation_euler = [math.pi / 2, 0, angle],
                    scale = self.creature_scale
                )
                self.add_subbobject(d_cre)
                self.drawn_creatures.append(d_cre)

                cre.drawn_creature = d_cre
                d_cre.add_to_blender(
                    appear_time = start_time,
                    subbobject_timing = OBJECT_APPEARANCE_TIME
                )
                if day.date > 0:
                    d_cre.move_to(
                        new_location = destination,
                        start_time = start_time
                    )

        #old creatures
        for i, cre in enumerate(creatures):
            angle = i * angle_inc

            if cre in old_creatures:
                destination = [
                    radius * math.cos(math.pi / 2 + angle),
                    radius * math.sin(math.pi / 2 + angle),
                    self.creature_scale * CREATURE_HEIGHT_FACTOR
                ]
                cre.drawn_creature.move_to(
                    new_location = destination,
                    start_time = start_time
                )

        #clean up dead creatures
        for d_cre in self.drawn_creatures:
            alive = False
            for cre in creatures:
                if cre.drawn_creature == d_cre:
                    alive = True
                    break
            if alive == False:
                d_cre.disappear(disappear_time = start_time + OBJECT_APPEARANCE_TIME / FRAME_RATE)

    def set_food(
        self,
        start_time = None,
        duration_time = None,
        end_time = None,
        day = None
    ):
        if start_time == None:
            raise Warning('Need start_time for set_food')
        if duration_time != None and end_time != None:
            raise Warning('Cannot set both duration_time and end_time in set_food')
        if duration_time == None and end_time == None:
            duration_time = OBJECT_APPEARANCE_TIME / FRAME_RATE
        if end_time != None:
            duration_time = end_time - start_time

        if day == None:
            raise Warning('Need day for set_food')

        pair_count = len(day.food_objects)
        ring_count = 0
        while pair_count > 0:
            if ring_count == 0:
                pair_count -= 1
            else:
                pair_count -= ring_count * FOOD_PATTERN_MULTIPLE

            ring_count += 1

        locations = helpers.circle_grid(
            num_rings = ring_count,
            dot_count_multiple = FOOD_PATTERN_MULTIPLE,
            rot_add = FOOD_PATTERN_ANGLE_OFFSET,
        )
        for i in range(len(locations)):
            locations[i] = scalar_mult_vec(locations[i], FOOD_EDGE_RATIO)

        delay = (duration_time - OBJECT_APPEARANCE_TIME / FRAME_RATE) / len(day.food_objects)
        for i, pair in enumerate(day.food_objects):
            f_scale = BASE_FOOD_SCALE / ring_count
            pair.location = locations[i]
            pair.angle = math.atan2(locations[i][1], locations[i][0])

            food1 = DrawnFood(
                object_model = self.food_object_model,
                location = [
                    locations[i][0] - 0.9 * f_scale * math.cos(pair.angle + math.pi / 2),
                    locations[i][1] - 0.9 * f_scale * math.sin(pair.angle + math.pi / 2),
                    f_scale,
                ],
                scale = f_scale,
                mat = 'color7'
            )

            constraint = food1.ref_obj.constraints.new('CHILD_OF')
            constraint.target = self.ref_obj

            food1.add_to_blender(appear_time = start_time + i * delay)
            pair.drawn_food = [food1]

            food2 = DrawnFood(
                object_model = self.food_object_model,
                location = [
                    locations[i][0] + 0.9 * f_scale * math.cos(pair.angle + math.pi / 2),
                    locations[i][1] + 0.9 * f_scale * math.sin(pair.angle + math.pi / 2),
                    f_scale,
                ],
                scale = f_scale,
                mat = 'color7'
            )

            constraint = food2.ref_obj.constraints.new('CHILD_OF')
            constraint.target = self.ref_obj

            food2.add_to_blender(appear_time = start_time + i * delay)
            pair.drawn_food.append(food2)

    def animate_day(self, day = None):
        target_food = None
        #creatures go out
        for cre in day.creatures:
            cre.home_loc = list(cre.drawn_creature.ref_obj.location)
            for entry in cre.days_log:
                if entry['date'] == day.date:
                    target_food = entry['morning_food']

            if cre == target_food.interested_creatures[0]:
                cre.drawn_creature.move_to(
                    start_time = self.elapsed_time,
                    end_time = self.elapsed_time + self.phase_durations['creatures_go_out'],
                    new_location = [
                        target_food.location[0] + self.creature_scale * math.cos(target_food.angle),
                        target_food.location[1] + self.creature_scale * math.sin(target_food.angle),
                        cre.drawn_creature.ref_obj.location[2]
                    ],
                    new_angle = [
                        cre.drawn_creature.ref_obj.rotation_euler[0],
                        cre.drawn_creature.ref_obj.rotation_euler[1],
                        target_food.angle - math.pi / 2
                    ]
                )
            elif cre == target_food.interested_creatures[1]:
                cre.drawn_creature.move_to(
                    start_time = self.elapsed_time,
                    end_time = self.elapsed_time + self.phase_durations['creatures_go_out'],
                    new_location = [
                        target_food.location[0] - self.creature_scale * math.cos(target_food.angle),
                        target_food.location[1] - self.creature_scale * math.sin(target_food.angle),
                        cre.drawn_creature.ref_obj.location[2]
                    ],
                    new_angle = [
                        cre.drawn_creature.ref_obj.rotation_euler[0],
                        cre.drawn_creature.ref_obj.rotation_euler[1],
                        target_food.angle + math.pi / 2
                    ]
                )
            else:
                raise Warning('Something is wrong with how interested_creatures is assigned')

        self.elapsed_time += self.phase_durations['creatures_go_out'] + self.phase_durations['pause_before_contest']

        #Resolve contests
        for cre in day.creatures:
            for entry in cre.days_log:
                if entry['date'] == day.date:
                    target_food = entry['morning_food']

            if len(target_food.drawn_food) > 0:
                target_food.drawn_food[0].disappear(disappear_time = self.elapsed_time + self.phase_durations['contest'])
                target_food.drawn_food[1].disappear(disappear_time = self.elapsed_time + self.phase_durations['contest'])
                target_food.drawn_food = []

        self.elapsed_time += self.phase_durations['contest'] + self.phase_durations['pause_before_home']

        #creatures go home
        for cre in day.creatures:
            cre.drawn_creature.move_to(
                start_time = self.elapsed_time,
                end_time = self.elapsed_time + self.phase_durations['creatures_go_home'],
                new_location = cre.home_loc,
                new_angle = [
                    cre.drawn_creature.ref_obj.rotation_euler[0],
                    cre.drawn_creature.ref_obj.rotation_euler[1],
                    math.atan2(cre.home_loc[0], cre.home_loc[1]) - math.pi / 2
                ]
            )
        #TODO: update based on phase durations
        self.elapsed_time += self.phase_durations['creatures_go_home'] + self.phase_durations['pause_before_reset']

    def animate_days(
        self,
        start_time = None,
        phase_duration_updates = [],
        graph_mode_changes = {},
        first_animated_day = 0,
        last_animated_day = math.inf
    ):
        self.elapsed_time = start_time

        for i, day in enumerate(self.sim.calendar):
            if i >= first_animated_day and i < last_animated_day:
                print('Animating day ' + str(i))
                for update in phase_duration_updates:
                    if update[0] == i:
                        for change in update[1]:
                            self.phase_durations[change] = update[1][change]

                update_duration = min(
                    OBJECT_APPEARANCE_TIME / FRAME_RATE,
                    self.phase_durations['day_prep']
                )

                self.set_food(
                    start_time = self.elapsed_time,
                    end_time = self.elapsed_time + update_duration,
                    day = day
                )

                #self.update_agent_scale(day_index = i)
                self.update_creatures(
                    start_time = self.elapsed_time,
                    end_time = self.elapsed_time + update_duration,
                    day = day
                )

                self.elapsed_time += self.phase_durations['day_prep']

                self.animate_day(day = day)

                for food in day.food_objects:
                    for d_food in food.drawn_food:
                        d_food.disappear(disappear_time = self.elapsed_time)

                self.elapsed_time += self.phase_durations['food_disappear']
