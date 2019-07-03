import collections
#import math
#from random import random, uniform, randrange
import bpy

import imp
#import scene
#imp.reload(scene)
from scene import Scene

import bobject
imp.reload(bobject)
#import svg_bobject
#imp.reload(svg_bobject)
import tex_bobject
imp.reload(tex_bobject)
#import tex_complex
#imp.reload(tex_complex)
#import gesture
#imp.reload(gesture)
import graph_bobject
imp.reload(graph_bobject)

import blobject
imp.reload(blobject)
#from blobject import Blobject

import hawk_dove
imp.reload(hawk_dove)
import drawn_contest_world
imp.reload(drawn_contest_world)


import helpers
imp.reload(helpers)
from helpers import *

import constants
imp.reload(constants)
#from constants import SIM_DIR

CREATURE_MOVE_DURATION = 0.5
PAUSE_LENGTH = 0.25

class HawkDove(Scene):
    def __init__(self):
        self.subscenes = collections.OrderedDict([
            ('card', {'duration': 10000})
        ])
        super().__init__()

    def play(self):
        super().play()
        #self.intro()
        self.basic_sim()

    def intro(self):
        pass

    def basic_sim(self):
        cam_bobj, cam_swivel = cam_and_swivel(
            cam_location = [0, 0, 34],
            cam_rotation_euler = [0, 0, 0],
            cam_name = "Camera Bobject",
            swivel_location = [0, 0, 0],
            swivel_rotation_euler = [74 * math.pi / 180, 0, 0],
            swivel_name = 'Cam swivel',
            #control_sun = True
        )
        cam_swivel.add_to_blender(appear_time = -1, animate = False)

        new_sim = False
        if new_sim == True:
            world = hawk_dove.World(food_count = 61)
            num_days = 1

            for i in range(num_days):
                save = False
                if i == num_days - 1:
                    save = True
                world.new_day(save = save)
        else:
            world = 'HAWKDOVE20190702T084149'

        drawn_world = drawn_contest_world.DrawnWorld(
            sim = world,
            loud = True,
            scale = 13
        )

        #phase_durations = {
        #    'day_prep' : CREATURE_MOVE_DURATION,
        #    'creatures_go_out' : CREATURE_MOVE_DURATION,
        #    'pause_before_contest' : PAUSE_LENGTH,
        #    'contest' : CREATURE_MOVE_DURATION,
        #    'pause_before_home' : PAUSE_LENGTH,
        #    'creatures_go_home' : CREATURE_MOVE_DURATION,
        #    'pause_before_reset' : PAUSE_LENGTH,
        #    'food_disappear' : CREATURE_MOVE_DURATION,
        #}
        updates = [
            [
                0,
                {
                    'day_prep' : 10,
                    #'creatures_go_out' : CREATURE_MOVE_DURATION,
                    #'pause_before_contest' : PAUSE_LENGTH,
                    #'contest' : CREATURE_MOVE_DURATION,
                    #'pause_before_home' : PAUSE_LENGTH,
                    #'creatures_go_home' : CREATURE_MOVE_DURATION,
                    #'pause_before_reset' : PAUSE_LENGTH,
                    #'food_disappear' : CREATURE_MOVE_DURATION,
                }
            ],
            [
                1,
                {
                    'day_prep' : CREATURE_MOVE_DURATION,
                    #'creatures_go_out' : CREATURE_MOVE_DURATION,
                    'pause_before_contest' : 10,
                    #'contest' : CREATURE_MOVE_DURATION,
                    'pause_before_home' : 2,
                    #'creatures_go_home' : CREATURE_MOVE_DURATION,
                    #'pause_before_reset' : PAUSE_LENGTH,
                    #'food_disappear' : CREATURE_MOVE_DURATION,
                }
            ]
        ]

        drawn_world.add_to_blender(appear_time = 1)
        drawn_world.move_to(
            new_angle = [0, 0, 2 * math.pi],
            start_time = 0,
            end_time = 13
        )
        drawn_world.animate_days(
            start_time = 2,
            first_animated_day = 0,
            last_animated_day = 2,
            phase_duration_updates = updates
        )

        def zoom_into_blobs():
            cam_bobj.move_to(
                new_location = [0, 0.55, 2.75],
                start_time = 17,
            )
            cam_swivel.move_to(
                new_angle = [74 * math.pi / 180, 0, -56.6 * math.pi / 180],
                start_time = 17
            )

            two_blobs = [
                drawn_world.drawn_creatures[1],
                drawn_world.drawn_creatures[6],
            ]
            for blob in two_blobs:
                blob.cheer(
                    start_time = 18,
                    end_time = 19
                )

            cam_bobj.move_to(
                new_location = [0, 1/6, 3.75],
                start_time = 20,
            )
            cam_swivel.move_to(
                new_angle = [76 * math.pi / 180, 0, -126 * math.pi / 180],
                new_location = [-3.25, -7.25, 0.1],
                start_time = 20
            )

            r_blob = drawn_world.drawn_creatures[3]
            l_blob = drawn_world.drawn_creatures[11]

            r_blob.move_head(
                rotation_quaternion = [1, 0.1, 0.1, -0.3],
                start_time = 21
            )
            r_blob.move_head(
                rotation_quaternion = [1, 0, 0.8, 0],
                start_time = 22
            )
            r_blob.move_head(
                rotation_quaternion = [1, 0.1, 0.1, -0.3],
                start_time = 23
            )
            r_blob.move_head(
                rotation_quaternion = [1, 0, 0.8, 0],
                start_time = 23.5
            )
            r_blob.move_head(
                rotation_quaternion = [1, 0, 0, 0],
                start_time = 24.5
            )

            dove = tex_bobject.TexBobject(
                '\\text{"Dove"}',
                rotation_euler = [76 * math.pi / 180, 0, -126 * math.pi / 180],
                location = [2.25, -14.6, 0.5]
            )
            dove.add_to_blender(
                appear_time = 26.5
            )
            dove.disappear(disappear_time = 29)

        zoom_into_blobs()

        cam_bobj.move_to(
            new_location = [0, 0, 34],
            start_time = 28.5,
        )
        cam_swivel.move_to(
            new_angle = [74 * math.pi / 180, 0, 0],
            new_location = [0, 0, 0],
            start_time = 28.5
        )
        drawn_world.move_to(
            new_location = [5, -9, 0],
            new_scale = 5,
            start_time = 28.5
        )

        graph = graph_bobject.GraphBobject(
            #demand_curve, supply_curve,
            arrows = 'positive',
            x_range = 100,
            y_range = 60,
            tick_step = [20, 10],
            x_label = "\\text{Quantity}",
            y_label = "\\text{Price}",
            y_label_pos = 'end',
            #padding = 0,
            centered = False,
            #sim = sim,
            location = [3, -5.5, 0],
            rotation_euler = [0, -45 * math.pi / 180, 0],
            scale = 1,
            #display_arrangement = 'superimposed',
            #overlay_functions = True,
        )

        graph.add_to_blender(appear_time = 29)
