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
import svg_bobject
imp.reload(svg_bobject)
import tex_bobject
imp.reload(tex_bobject)
import tex_complex
imp.reload(tex_complex)
import gesture
imp.reload(gesture)

import graph_bobject
imp.reload(graph_bobject)
import table_bobject
imp.reload(table_bobject)

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

NEW_CREATURE_MOVE_DURATION = 0.5
NEW_PAUSE_LENGTH = 0

class HawkDove(Scene):
    def __init__(self):
        self.subscenes = collections.OrderedDict([
            ('card', {'duration': 100})
        ])
        super().__init__()

    def play(self):
        super().play()
        #self.intro()
        #self.basic_sim()
        #self.hawk_intro()
        #self.hawk_dove_sim()
        #self.hypotheticals()
        #self.hawks_then_dove()
        #self.big_sim()
        #self.payoff_grid()
        #self.building_from_here()
        #self.teaser()
        #self.patreon()
        self.thumb()

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
            world = 'doves_only'

        graph = graph_bobject.GraphBobject(
            #demand_curve, supply_curve,
            location = [-11, -4, 0],
            rotation_euler = [74 * math.pi / 180, 0, 0],
            x_range = 10,
            y_range = 120,
            width = 11,
            height = 11,
            tick_step = [5, 60],
            x_label = "\\text{Days}",
            y_label = "\\text{Creatures}",
            y_label_pos = 'end',
            arrows = 'positive',
            centered = False,
            scale = 1,
            high_res_curve_indices = [],
            discrete_interpolation_style = 'linear',
            show_functions = False
        )

        #drawn_world.linked_graph = graph
        #drawn_food.add_functions_to_graph()

        drawn_world = drawn_contest_world.DrawnWorld(
            sim = world,
            loud = True,
            linked_graph = graph,
            scale = 13,
            wiggle = True
        )

        #phase_durations = {
        #    'day_prep' : CREATURE_MOVE_DURATION,
        #    'creatures_go_out' : CREATURE_MOVE_DURATION,
        #    'pause_before_contest' : 0,
        #    'contest' : CREATURE_MOVE_DURATION,
        #    'pause_before_home' : PAUSE_LENGTH,
        #    'creatures_go_home' : CREATURE_MOVE_DURATION,
        #    'pause_before_reset' : 0,
        #    'food_disappear' : CREATURE_MOVE_DURATION,
        #}
        updates = [
            [
                0,
                {
                    'day_prep' : 3,
                    #'creatures_go_out' : CREATURE_MOVE_DURATION,
                    #'pause_before_contest' : 0,
                    #'contest' : CREATURE_MOVE_DURATION,
                    'pause_before_home' : 0,
                    #'creatures_go_home' : CREATURE_MOVE_DURATION,
                    #'pause_before_reset' : 0,
                    #'food_disappear' : CREATURE_MOVE_DURATION,
                }
            ],
            [
                1,
                {
                    'day_prep' : 17, #ends 41.5
                    #'creatures_go_out' : CREATURE_MOVE_DURATION,
                    'pause_before_contest' : 18, #ends 60
                    'contest' : 1 ,
                    'pause_before_home' : 7.5, #ends 68.5
                    #'creatures_go_home' : CREATURE_MOVE_DURATION,
                    #'pause_before_reset' : 3,
                    #'food_disappear' : CREATURE_MOVE_DURATION,
                }
            ],
            [
                2,
                {
                    'day_prep' : CREATURE_MOVE_DURATION,
                    #'creatures_go_out' : CREATURE_MOVE_DURATION,
                    'pause_before_contest' : 0,
                    'contest' : CREATURE_MOVE_DURATION,
                    'pause_before_home' : 0,
                    #'creatures_go_home' : CREATURE_MOVE_DURATION,
                    #'pause_before_reset' : PAUSE_LENGTH,
                    #'food_disappear' : CREATURE_MOVE_DURATION,
                }
            ],
        ]

        drawn_world.add_to_blender(appear_time = 18.5)
        drawn_world.move_to(
            new_angle = [0, 0, 2 * math.pi],
            start_time = 24,
            end_time = 39
        )

        surv_rule = tex_bobject.TexBobject(
            #'\\text{No food} \\rightarrow \\text{Death}',
            '\\text{One food} \\rightarrow \\text{Survive}',
            #'\\text{Two food} \\rightarrow \\text{Replicate}',
            location = [0, 0, 6.75],
            rotation_euler = [74 * math.pi / 180, 0, 0],
            scale = 1.5,
            centered = True
        )
        surv_rule.add_to_blender(appear_time = 29)
        surv_rule.disappear(disappear_time = 60)

        rep_rule = tex_bobject.TexBobject(
            '\\text{Two food} \\rightarrow \\text{Reproduce}',
            location = [0, 0, 5],
            rotation_euler = [74 * math.pi / 180, 0, 0],
            scale = 1.5,
            centered = True
        )
        rep_rule.add_to_blender(appear_time = 33)
        rep_rule.disappear(disappear_time = 60)

        graph.add_to_blender(appear_time = 69)
        for i in range(len(graph.functions)):
            graph.set_shape_keys_bounded_region(index = i)

        drawn_world.animate_days(
            start_time = 19.5,
            first_animated_day = 2,
            last_animated_day = 4,
            phase_duration_updates = updates
        )

        def zoom_into_blobs():
            cam_bobj.move_to(
                new_location = [0, 0.55, 2.75],
                start_time = 43.5,
            )
            cam_swivel.move_to(
                new_angle = [74 * math.pi / 180, 0, -56.6 * math.pi / 180],
                start_time = 43.5
            )

            two_blobs = [
                drawn_world.drawn_creatures[1],
                drawn_world.drawn_creatures[6],
            ]
            for blob in two_blobs:
                blob.cheer(
                    start_time = 46,
                    end_time = 48
                )

            cam_bobj.move_to(
                new_location = [0, 1/6, 3.75],
                start_time = 48.5,
            )
            cam_swivel.move_to(
                new_angle = [76 * math.pi / 180, 0, -126 * math.pi / 180],
                new_location = [-3.25, -7.25, 0.1],
                start_time = 48.5
            )

            r_blob = drawn_world.drawn_creatures[3]
            l_blob = drawn_world.drawn_creatures[11]

            r_blob.move_head(
                rotation_quaternion = [1, 0.1, 0.1, -0.3],
                start_time = 49.5
            )
            r_blob.move_head(
                rotation_quaternion = [1, 0, 0.8, 0],
                start_time = 51.5
            )
            r_blob.move_head(
                rotation_quaternion = [1, 0.1, 0.1, -0.3],
                start_time = 53
            )
            r_blob.move_head(
                rotation_quaternion = [1, 0, 0.8, 0],
                start_time = 54
            )
            r_blob.move_head(
                rotation_quaternion = [1, 0, 0, 0],
                start_time = 55
            )

            l_blob.move_head(
                rotation_quaternion = [1, 0.1, 0.1, -0.3],
                start_time = 50
            )
            l_blob.move_head(
                rotation_quaternion = [1, 0, 0, 0],
                start_time = 51.2
            )
            l_blob.move_head(
                rotation_quaternion = [1, 0.1, 0.1, -0.3],
                start_time = 53.8
            )
            l_blob.move_head(
                rotation_quaternion = [1, 0, 0, 0],
                start_time = 54.5
            )


            dove = tex_bobject.TexBobject(
                '\\text{"Dove"}',
                rotation_euler = [76 * math.pi / 180, 0, -126 * math.pi / 180],
                location = [2.25, -14.6, 0.5]
            )
            dove.add_to_blender(
                appear_time = 67.5
            )
            dove.disappear(disappear_time = 69)

        zoom_into_blobs()

        cam_bobj.move_to(
            new_location = [0, 0, 34],
            start_time = 69,
            end_time = 70
        )
        cam_swivel.move_to(
            new_angle = [74 * math.pi / 180, 0, 0],
            new_location = [0, 0, 4],
            start_time = 69,
            end_time = 70
        )
        drawn_world.move_to(
            #new_location = [6.5, -9, 0],
            new_location = [7.5, 0, 0],
            new_scale = 6.5,
            start_time = 69
        )

        doves = tex_bobject.TexBobject(
            '\\text{Doves only}',
            rotation_euler = [74 * math.pi / 180, 0, 0],
            location = [7, 0, 8],
            scale = 2,
            centered = True
        )
        doves.add_to_blender(
            appear_time = 69.5
        )
        #doves.disappear(disappear_time = 29)

        disappear_time = 100
        to_disappear = [graph, doves, drawn_world]
        for i, thing in enumerate(to_disappear):
            thing.disappear(
                disappear_time = disappear_time - (len(to_disappear) - i - 1) * 0.05
            )

    def hawk_intro(self):
        hawk_strat = tex_bobject.TexBobject(
            '\\text{New strategy: }',
            '\\text{New strategy: Hawk}',
            centered = False,
            location = [-12.5, 6, 0],
            scale = 3
        )
        hawk_strat.add_to_blender(appear_time = 80.5)
        hawk_strat.morph_figure(1, start_time = 82)

        food1 = import_object(
            'goodicosphere', 'primitives',
            mat = 'color7',
            location = [1, -5, 1]
        )
        food21 = import_object(
            'half_icosphere', 'primitives',
            location = [-1, -5, -1],
            rotation_euler = [0, -math.pi / 2, 0],
            mat = 'color7'
        )
        food22 = import_object(
            'half_icosphere', 'primitives',
            location = [-1, -5, -1],
            rotation_euler = [0, math.pi / 2, 0],
            mat = 'color7'
        )
        food1.add_to_blender(appear_time = 83.5)
        food21.add_to_blender(appear_time = 83.5)
        food22.add_to_blender(appear_time = 83.5)

        dove = blobject.Blobject(
            location = [-32, -2, 0],
            rotation_euler = [0, math.pi / 2, 0],
            scale = 5,
            wiggle = True
        )
        dove.add_to_blender(appear_time = 1)
        dove.walk_to(
            new_location = [-6, -2, 0],
            start_time = 84,
            end_time = 85.5
        )

        hawk = blobject.Blobject(
            location = [32, -2, 0],
            rotation_euler = [0, -math.pi / 2, 0],
            scale = 5
        )
        hawk.add_to_blender(appear_time = 1)
        hawk.walk_to(
            new_location = [6, -2, 0],
            start_time = 84,
            end_time = 85.5
        )

        dove.hello(start_time = 85.5, end_time = 86.5)
        dove.eat_animation(start_frame = 85.5 * FRAME_RATE, end_frame = 86.5 * FRAME_RATE)

        hawk.move_head(
            rotation_quaternion = [1, 0, 0.9, -0.1],
            start_time = 85.5,
            end_time = 87.5
        )
        hawk.color_shift(
            duration_time = None,
            color = COLORS_SCALED[5],
            start_time = 86,
            shift_time = FRAME_RATE / 2,
            obj = hawk.ref_obj.children[0].children[0]
        )
        hawk.angry_eyes(
            start_time = 86,
            attack = 0.5,
            end_time = None
        )

        def eats():
            drawn_contest_world.transfer_food_to_creature(
                food_bobj = food22,
                creature_bobj = hawk,
                start_time = 88,
                ground_plane = 'xz'
            )

            drawn_contest_world.animate_eating(
                food = food22,
                eater = hawk,
                start_time = 88,
                dur = 1.5,
                eat_rotation = [0, -30 * math.pi / 180, 0]
            )

            drawn_contest_world.transfer_food_to_creature(
                food_bobj = food21,
                creature_bobj = dove,
                start_time = 88,
                ground_plane = 'xz'
            )

            drawn_contest_world.animate_eating(
                food = food21,
                eater = dove,
                start_time = 88,
                dur = 1.5,
                eat_rotation = [0, 30 * math.pi / 180, 0]
            )

            drawn_contest_world.transfer_food_to_creature(
                food_bobj = food1,
                creature_bobj = hawk,
                start_time = 89.5,
                ground_plane = 'xz'
            )

            drawn_contest_world.animate_eating(
                food = food1,
                eater = hawk,
                start_time = 89.5,
                dur = 1.5 ,
                eat_rotation = [0, 30 * math.pi / 180, 0]
            )

            dove.surprise_eyes(
                start_time = 89,
                end_time = 92
            )

        eats()

        dove.move_to(
            new_angle = [0, 0, 0],
            start_time = 91
        )
        dove.wince(
            start_time = 91,
            end_time = 112,
            period = 1,
            non_uniform = True
        )
        hawk.move_to(
            new_angle = [0, 0, 0],
            start_time = 91
        )
        hawk.evil_pose(start_time = 91, end_time = 112)

        hawk.move_to(
            new_location = [3.5, -2, 0],
            start_time = 108
        )
        rep_indicator = tex_bobject.TexBobject(
            #'\\substack{\\text{Replication} \\\\ \\text{chance} \\\\ 50\\%}',
            '\\begin{array}{@{}c@{}}\\text{Replication} \\\\ \\text{chance } 50\\% \\end{array}',
            location = [10.25, 1.5, 0],
            scale = 1.5,
            color = 'color2',
            centered = True
        )
        rep_indicator.add_to_blender(appear_time = 108)
        '''for i in range(19, 20):
            char = rep_indicator.lookup_table[0][i]
            char.color_shift(
                color = COLORS_SCALED[4],
                start_time = -1,
                duration_time = None
            )'''

        dove.move_to(
            new_location = [-3.75, -2, 0],
            start_time = 100.5
        )
        surv_indicator = tex_bobject.TexBobject(
            #'\\substack{\\text{Replication} \\\\ \\text{chance} \\\\ 50\\%}',
            '\\begin{array}{@{}c@{}}\\text{Survival} \\\\ \\text{chance } 50\\% \\end{array}',
            location = [-10.25, 1.5, 0],
            scale = 1.5,
            color = 'color2',
            centered = True
        )
        surv_indicator.add_to_blender(appear_time = 100.5)

        to_disappear = [
            dove,
            hawk,
            rep_indicator,
            surv_indicator
        ]
        for thing in to_disappear:
            thing.disappear(disappear_time = 112)

        #Hawk v hawk
        food31 = import_object(
            'half_icosphere', 'primitives',
            mat = 'color7',
            rotation_euler = [0, -math.pi / 2, 0],
            location = [1, -5, 1]
        )
        food32 = import_object(
            'half_icosphere', 'primitives',
            mat = 'color7',
            rotation_euler = [0, math.pi / 2, 0],
            location = [1, -5, 1]
        )
        food41 = import_object(
            'half_icosphere', 'primitives',
            location = [-1, -5, -1],
            rotation_euler = [0, -math.pi / 2, 0],
            mat = 'color7'
        )
        food42 = import_object(
            'half_icosphere', 'primitives',
            location = [-1, -5, -1],
            rotation_euler = [0, math.pi / 2, 0],
            mat = 'color7'
        )
        food31.add_to_blender(appear_time = 113.5)
        food32.add_to_blender(appear_time = 113.5)
        food41.add_to_blender(appear_time = 113.5)
        food42.add_to_blender(appear_time = 113.5)

        hawk2 = blobject.Blobject(
            location = [-32, -2, 0],
            rotation_euler = [0, math.pi / 2, 0],
            scale = 5,
            mat = 'creature_color6'
        )
        hawk2.add_to_blender(appear_time = 113)
        hawk2.walk_to(
            new_location = [-6, -2, 0],
            start_time = 113.5,
            end_time = 115
        )

        hawk3 = blobject.Blobject(
            location = [32, -2, 0],
            rotation_euler = [0, -math.pi / 2, 0],
            scale = 5,
            mat = 'creature_color6'
        )
        hawk3.add_to_blender(appear_time = 113)
        hawk3.walk_to(
            new_location = [6, -2, 0],
            start_time = 113.5,
            end_time = 115
        )

        hawk2.blob_wave(
            start_time = 115,
            duration = 7.5
        )
        hawk2.angry_eyes(start_time = 115, end_time = None)
        hawk3.blob_wave(
            start_time = 115,
            duration = 7.5
        )
        hawk3.angry_eyes(start_time = 115, end_time = None)

        def eats2():
            drawn_contest_world.transfer_food_to_creature(
                food_bobj = food32,
                creature_bobj = hawk3,
                start_time = 122.5,
                ground_plane = 'xz'
            )

            drawn_contest_world.animate_eating(
                food = food32,
                eater = hawk3,
                start_time = 122.5,
                dur = 1.5,
                eat_rotation = [0, 30 * math.pi / 180, 0]
            )

            drawn_contest_world.transfer_food_to_creature(
                food_bobj = food31,
                creature_bobj = hawk2,
                start_time = 122.5,
                ground_plane = 'xz'
            )

            drawn_contest_world.animate_eating(
                food = food31,
                eater = hawk2,
                start_time = 122.5,
                dur = 1.5,
                eat_rotation = [0, -30 * math.pi / 180, 0]
            )

            drawn_contest_world.transfer_food_to_creature(
                food_bobj = food41,
                creature_bobj = hawk3,
                start_time = 124,
                ground_plane = 'xz'
            )

            drawn_contest_world.animate_eating(
                food = food41,
                eater = hawk3,
                start_time = 124,
                dur = 1.5,
                eat_rotation = [0, -30 * math.pi / 180, 0]
            )

            drawn_contest_world.transfer_food_to_creature(
                food_bobj = food42,
                creature_bobj = hawk2,
                start_time = 124,
                ground_plane = 'xz'
            )

            drawn_contest_world.animate_eating(
                food = food42,
                eater = hawk2,
                start_time = 124,
                dur = 1.5,
                eat_rotation = [0, 30 * math.pi / 180, 0]
            )
        eats2()

        hawk2.move_to(
            new_angle = [0, 0, 0],
            start_time = 127
        )
        #hawk2.wince(start_time = 8.5, end_time = 13)
        hawk3.move_to(
            new_angle = [0, 0, 0],
            start_time = 127
        )
        #hawk3.evil_pose(start_time = 8.5, end_time = 13)

        hawk3.move_to(
            new_location = [3.5, -2, 0],
            start_time = 129
        )
        rep_indicator2 = tex_bobject.TexBobject(
            #'\\substack{\\text{Replication} \\\\ \\text{chance} \\\\ 50\\%}',
            '\\begin{array}{@{}c@{}}\\text{Survival} \\\\ \\text{chance } 0\\% \\end{array}',
            location = [10.25, 1.5, 0],
            scale = 1.5,
            color = 'color2',
            centered = True
        )
        rep_indicator2.add_to_blender(appear_time = 129)
        '''for i in range(19, 20):
            char = rep_indicator.lookup_table[0][i]
            char.color_shift(
                color = COLORS_SCALED[4],
                start_time = -1,
                duration_time = None
            )'''

        hawk2.move_to(
            new_location = [-3.5, -2, 0],
            start_time = 129
        )
        surv_indicator2 = tex_bobject.TexBobject(
            #'\\substack{\\text{Replication} \\\\ \\text{chance} \\\\ 50\\%}',
            '\\begin{array}{@{}c@{}}\\text{Survival} \\\\ \\text{chance } 0\\% \\end{array}',
            location = [-10.25, 1.5, 0],
            scale = 1.5,
            color = 'color2',
            centered = True
        )
        surv_indicator2.add_to_blender(appear_time = 129)


        hawk2.wince(start_time = 129, end_time = 133, period = 1, non_uniform = True)
        hawk3.wince(start_time = 129.25, end_time = 134, period = 1, non_uniform = True)

        to_disappear = [
            rep_indicator2,
            surv_indicator2,
            hawk2,
            hawk3,
            hawk_strat
        ]
        disappear_time = 132.5
        for i, thing in enumerate(to_disappear):
            thing.disappear(
                disappear_time = disappear_time - (len(to_disappear) - i - 1) * 0.05
            )

        '''
        Make blob idle movements or fix wiggle conflict
        '''

    def hawk_dove_sim(self):
        cam_bobj, cam_swivel = cam_and_swivel(
            cam_location = [0, 0, 34],
            cam_rotation_euler = [0, 0, 0],
            cam_name = "Camera Bobject",
            swivel_location = [0, 0, 4],
            swivel_rotation_euler = [74 * math.pi / 180, 0, 0],
            swivel_name = 'Cam swivel',
            #control_sun = True
        )
        cam_swivel.add_to_blender(appear_time = -1, animate = False)

        new_sim = False
        if new_sim == True:
            world = hawk_dove.World(food_count = 61)
            num_days = 10

            for i in range(num_days):
                save = False
                if i == num_days - 1:
                    save = True
                try:
                    world.new_day(save = save)
                except:
                    print()
                    print('Saving did not work')
                    print()
                    world.new_day(save = False)

        else:
            world = 'dove10hawk150'#'doves_only'

        if isinstance(world, str):
            result = os.path.join(
                SIM_DIR,
                world
            ) + ".pkl"
            print(result)
            with open(result, 'rb') as input:
                print(input)
                world = pickle.load(input)
                print("Loaded the world")

        #replace one dove with a hawk in the most recent generation
        edit_sim = False
        if edit_sim == True:
            old_cre = world.calendar[-1].next_creatures.pop()
            new_cre = hawk_dove.Creature(
                fight_chance = 1,
                parent = old_cre.parent
            )
            world.calendar[-1].next_creatures.append(new_cre)

        add_to_sim = False
        if add_to_sim == True:
            sys.setrecursionlimit(14500)
            num_days = 150
            for i in range(num_days):
                save = False
                if i == num_days - 1:
                    #print(i)
                    #time.sleep(1)
                    save = True
                world.new_day(save = save)#, filename = 'intro_hawk')

        graph = graph_bobject.GraphBobject(
            location = [-11, -4, 0],
            rotation_euler = [74 * math.pi / 180, 0, 0],
            x_range = 10,
            y_range = 120,
            width = 11,
            height = 11,
            tick_step = [5, 20],
            x_label = "\\text{Days}",
            y_label = "\\text{Creatures}",
            y_label_pos = 'end',
            arrows = 'positive',
            centered = False,
            scale = 1,
            high_res_curve_indices = [],
            discrete_interpolation_style = 'linear',
            show_functions = False
        )

        drawn_world = drawn_contest_world.DrawnWorld(
            sim = world,
            loud = True,
            linked_graph = graph,
            location = [7.5, 0, 0],
            scale = 6.5,
            wiggle = True
        )

        #phase_durations = {
        #    'day_prep' : CREATURE_MOVE_DURATION,
        #    'creatures_go_out' : CREATURE_MOVE_DURATION,
        #    'pause_before_contest' : 0,
        #    'contest' : CREATURE_MOVE_DURATION,
        #    'pause_before_home' : PAUSE_LENGTH,
        #    'creatures_go_home' : CREATURE_MOVE_DURATION,
        #    'pause_before_reset' : 0,
        #    'food_disappear' : CREATURE_MOVE_DURATION,
        #}
        updates = [
            [
                10,
                {
                    'day_prep' : 16,
                    'creatures_go_out' : NEW_CREATURE_MOVE_DURATION,
                    'pause_before_contest' : 0,
                    'contest' : NEW_CREATURE_MOVE_DURATION,
                    'pause_before_home' : 1/4,
                    'creatures_go_home' : NEW_CREATURE_MOVE_DURATION,
                    'pause_before_reset' : 0,
                    'food_disappear' : NEW_CREATURE_MOVE_DURATION,
                }
            ],
            [
                11,
                {
                    'day_prep' : NEW_CREATURE_MOVE_DURATION,
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
                20,
                {
                    'day_prep' : NEW_CREATURE_MOVE_DURATION,
                    'creatures_go_out' : NEW_CREATURE_MOVE_DURATION,
                    #'pause_before_contest' : PAUSE_LENGTH,
                    'contest' : NEW_CREATURE_MOVE_DURATION,
                    #'pause_before_home' : 0,
                    'creatures_go_home' : NEW_CREATURE_MOVE_DURATION,
                    #'pause_before_reset' : PAUSE_LENGTH,
                    'food_disappear' : NEW_CREATURE_MOVE_DURATION,
                }
            ]
        ]

        graph.add_to_blender(appear_time = 133)
        drawn_world.add_to_blender(appear_time = 133)
        for i in range(len(graph.functions)):
            graph.set_shape_keys_bounded_region(index = i)

        hawks_and_doves = tex_bobject.TexBobject(
            '\\text{Doves only}',
            '\\begin{array}{@{}c@{}}\\text{Doves and} \\\\ \\text{Hawks} \\end{array}',
            rotation_euler = [74 * math.pi / 180, 0, 0],
            location = [7, 0, 8],
            scale = 2,
            centered = True
        )

        '''graph.change_window(
            start_time = 3,
            end_time = 4,
            new_x_range = [0, 100],
            new_tick_step = [50, 20]
        )'''





        hawks_and_doves.add_to_blender(appear_time = 133)
        hawks_and_doves.morph_figure(1, start_time = 135)

        scale = 1
        tail1 = [6.69, 4.75]
        head1 = [6.69, 2.75]

        arrow2 = gesture.Gesture(
            gesture_series = [
                {
                    'type': 'arrow',
                    'points': {
                        'tail': (tail1[0] / scale, tail1[1] / scale, 0),
                        'head': (head1[0] / scale, head1[1] / scale, 0)
                    }
                }
            ],
            scale = scale,
            rotation_euler = [74 * math.pi / 180, 0, 0]
        )
        arrow2.add_to_blender(appear_time = 134.5)
        arrow2.disappear(disappear_time = 150)

        scale = 1
        tail1 = [8.75, 11.5]
        head1 = [8.75, 9.5]

        arrow3 = gesture.Gesture(
            gesture_series = [
                {
                    'type': 'arrow',
                    'points': {
                        'tail': (tail1[0] / scale, tail1[1] / scale, 0),
                        'head': (head1[0] / scale, head1[1] / scale, 0)
                    }
                }
            ],
            scale = scale,
        )

        arrow3.ref_obj.parent = graph.ref_obj
        arrow3.add_to_blender(appear_time = 134.5)
        arrow3.disappear(disappear_time = 150)

        scale = 1
        tail1 = [11.5, 4.01]
        head1 = [9.5, 4]
        tail2 = [11.5, 2.01]
        head2 = [9.5, 2]
        tail3 = [9.5 + math.sqrt(2), 8 + math.sqrt(2)]
        head3 = [9.5, 8]
        tail4 = [3, 11]
        head4 = [3, 9]

        arrow1 = gesture.Gesture(
            gesture_series = [
                {
                    'type': 'arrow',
                    'points': {
                        'tail': (tail1[0] / scale, tail1[1] / scale, 0),
                        'head': (head1[0] / scale, head1[1] / scale, 0)
                    }
                },
                {
                    'type': 'arrow',
                    'points': {
                        'tail': (tail2[0] / scale, tail2[1] / scale, 0),
                        'head': (head2[0] / scale, head2[1] / scale, 0)
                    }
                },
                {
                    'type': 'arrow',
                    'points': {
                        'tail': (tail1[0] / scale, tail1[1] / scale, 0),
                        'head': (head1[0] / scale, head1[1] / scale, 0)
                    }
                },
                {
                    'type': 'arrow',
                    'points': {
                        'tail': (tail2[0] / scale, tail2[1] / scale, 0),
                        'head': (head2[0] / scale, head2[1] / scale, 0)
                    }
                },
                {
                    'type': 'arrow',
                    'points': {
                        'tail': (tail3[0] / scale, tail3[1] / scale, 0),
                        'head': (head3[0] / scale, head3[1] / scale, 0)
                    }
                },
            ],
            scale = scale,
        )

        arrow1.ref_obj.parent = graph.ref_obj
        arrow1.add_to_blender(appear_time = 342)
        arrow1.morph_figure(1, start_time = 342.5)
        arrow1.morph_figure(2, start_time = 343)
        arrow1.morph_figure(3, start_time = 343.5)
        arrow1.morph_figure(4, start_time = 346)

        drawn_world.animate_days(
            start_time = 134,
            first_animated_day = 10,
            last_animated_day = 80,
            phase_duration_updates = updates,
            #graph_only = True
        )

        disappear_time = 352
        #to_disappear = [drawn_world]
        to_disappear = [graph, hawks_and_doves, drawn_world]
        for i, thing in enumerate(to_disappear):
            thing.disappear(
                disappear_time = disappear_time - (len(to_disappear) - i - 1) * 0.05
            )

    def hypotheticals(self):
        cam_bobj, cam_swivel = cam_and_swivel(
            cam_location = [0, 0, 34],
            cam_rotation_euler = [0, 0, 0],
            cam_name = "Camera Bobject",
            swivel_location = [0, 0, 4],
            swivel_rotation_euler = [74 * math.pi / 180, 0, 0],
            swivel_name = 'Cam swivel',
            control_sun = True
        )
        cam_swivel.add_to_blender(appear_time = -1, animate = False)

        new_sim = False
        if new_sim == True:
            world = hawk_dove.World(food_count = 1000)
            num_days = 640

            for i in range(num_days):
                save = False
                if i == num_days - 1:
                    save = True
                try:
                    world.new_day(save = save)
                except:
                    print()
                    print('Saving did not work')
                    print()
                    world.new_day(save = False)

        else:
            world = 'doves_only'#'doves_only'

        if isinstance(world, str):
            result = os.path.join(
                SIM_DIR,
                world
            ) + ".pkl"
            print(result)
            with open(result, 'rb') as input:
                print(input)
                world = pickle.load(input)
                print("Loaded the world")

        #replace one dove with a hawk in the most recent generation
        edit_sim = True
        hypothetical_outcome = 'few_doves'
        if edit_sim == True:
            '''old_cre = world.calendar[-1].next_creatures.pop()
            new_cre = hawk_dove.Creature(
                fight_chance = 1,
                parent = old_cre.parent
            )
            world.calendar[-1].next_creatures.append(new_cre)'''

            num_added_days = 10
            target_num_hawks = 70
            for i in range(0, num_added_days):
                '''old_cre = world.calendar[-1].next_creatures.pop()
                new_cre = hawk_dove.Creature(
                    fight_chance = 1,
                    parent = old_cre.parent
                )'''
                #Some nonsense to make a function that wobbles around a target
                old_num_cres = len(world.calendar[-1].creatures)
                old_num_hawks = len([x for x in world.calendar[-1].creatures if x.fight_chance == 1])
                if hypothetical_outcome == 'few_hawks':
                    if old_num_hawks > target_num_hawks:
                        new_num_hawks = old_num_hawks
                        roll = random()
                        if roll < 0.4:
                            new_num_hawks -= 1
                        elif roll < 0.5:
                            new_num_hawks += 1
                    elif old_num_hawks < target_num_hawks:
                        new_num_hawks = old_num_hawks
                        roll = random()
                        if roll < 0.4:
                            new_num_hawks += 1
                        elif roll < 0.5:
                            new_num_hawks -= 1
                    else:
                        new_num_hawks = old_num_hawks
                        roll = random()
                        if roll < 0.25:
                            new_num_hawks += 1
                        elif roll < 0.5:
                            new_num_hawks -= 1
                elif hypothetical_outcome == 'few_doves':
                    if old_num_hawks != target_num_hawks:
                        new_num_hawks = old_num_hawks
                        roll = random()
                        if roll < 0.1:
                            new_num_hawks -= math.ceil((old_num_hawks - target_num_hawks) / 2)
                        elif roll < 0.2:
                            new_num_hawks -= math.ceil((old_num_hawks - target_num_hawks) / 3)
                        elif roll < 0.3:
                            new_num_hawks -= math.ceil((old_num_hawks - target_num_hawks) / 4)
                        elif roll < 0.4:
                            new_num_hawks -= math.ceil((old_num_hawks - target_num_hawks) / 5)
                        elif roll < 0.5:
                            new_num_hawks -= math.ceil((old_num_hawks - target_num_hawks) / 6)
                        elif roll < 0.6:
                            new_num_hawks -= math.ceil((old_num_hawks - target_num_hawks) / 7)
                        elif roll < 0.7:
                            new_num_hawks -= math.ceil((old_num_hawks - target_num_hawks) / 8)
                        elif roll < 0.8:
                            new_num_hawks -= math.ceil((old_num_hawks - target_num_hawks) / 9)
                        elif roll < 0.9:
                            new_num_hawks -= math.ceil((old_num_hawks - target_num_hawks) / 10)
                        else:
                            new_num_hawks += 1
                        '''elif old_num_hawks < target_num_hawks:
                            new_num_hawks = old_num_hawks
                            roll = random()
                            if roll < 0.1:
                                new_num_hawks -= math.ceil((target_num_hawks - old_num_hawks) / 2)
                            elif roll < 0.2:
                                new_num_hawks -= math.ceil((target_num_hawks - old_num_hawks) / 3)
                            elif roll < 0.3:
                                new_num_hawks -= math.ceil((target_num_hawks - old_num_hawks) / 4)
                            elif roll < 0.4:
                                new_num_hawks -= math.ceil((target_num_hawks - old_num_hawks) / 5)
                            elif roll < 0.5:
                                new_num_hawks -= math.ceil((target_num_hawks - old_num_hawks) / 6)
                            elif roll < 0.6:
                                new_num_hawks -= math.ceil((old_num_hawks - target_num_hawks) / 7)
                            elif roll < 0.7:
                                new_num_hawks -= math.ceil((old_num_hawks - target_num_hawks) / 8)
                            elif roll < 0.8:
                                new_num_hawks -= math.ceil((old_num_hawks - target_num_hawks) / 9)
                            elif roll < 0.9:
                                new_num_hawks -= math.ceil((old_num_hawks - target_num_hawks) / 10)
                            else:
                                new_num_hawks += 1'''
                    else:
                        new_num_hawks = old_num_hawks
                        roll = random()
                        if roll < 0.25:
                            new_num_hawks += 1
                        elif roll < 0.5:
                            new_num_hawks -= 1

                #Override on first additional day
                if i == 0:
                    new_num_hawks = 1

                creatures = []
                for j in range(old_num_cres):
                    if j < new_num_hawks:
                        fight_chance = 1
                    else:
                        fight_chance = 0
                    creatures.append(
                        hawk_dove.Creature(
                            fight_chance = fight_chance
                        )
                    )

                if i > 0:
                    world.calendar[-1].next_creatures = creatures
                world.calendar.append(
                    hawk_dove.Day(
                        creatures = creatures,
                        date = len(world.calendar),
                        food_count = 61 #Doesn't matter
                    )
                )
                if i == num_added_days - 1:
                    world.calendar[-1].next_creatures = creatures

        add_to_sim = False
        if add_to_sim == True:
            sys.setrecursionlimit(13000)
            num_days = 160
            for i in range(num_days):
                save = False
                if i == num_days - 1:
                    print(i)
                    #time.sleep(1)
                    #save = True
                world.new_day(save = save)#, filename = 'intro_hawk')

        graph = graph_bobject.GraphBobject(
            #demand_curve, supply_curve,
            location = [-11, -4, 0],
            rotation_euler = [74 * math.pi / 180, 0, 0],
            x_range = 10,
            y_range = 120,
            width = 11,
            height = 11,
            tick_step = [5, 20],
            x_label = "\\text{Days}",
            y_label = "\\text{Creatures}",
            y_label_pos = 'end',
            arrows = 'positive',
            centered = False,
            scale = 1,
            high_res_curve_indices = [],
            discrete_interpolation_style = 'linear',
            show_functions = False
        )

        #drawn_world.linked_graph = graph
        #drawn_food.add_functions_to_graph()

        drawn_world = drawn_contest_world.DrawnWorld(
            sim = world,
            loud = True,
            linked_graph = graph,
            location = [7.5, 0, 0],
            scale = 6.5
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
                9,
                {
                    'day_prep' : NEW_CREATURE_MOVE_DURATION,
                    'creatures_go_out' : NEW_CREATURE_MOVE_DURATION,
                    'pause_before_contest' : NEW_PAUSE_LENGTH,
                    'contest' : NEW_CREATURE_MOVE_DURATION,
                    'pause_before_home' : NEW_PAUSE_LENGTH,
                    'creatures_go_home' : NEW_CREATURE_MOVE_DURATION,
                    'pause_before_reset' : NEW_PAUSE_LENGTH,
                    'food_disappear' : NEW_CREATURE_MOVE_DURATION,
                }
            ]
        ]

        graph.add_to_blender(appear_time = 1)
        #drawn_world.add_to_blender(appear_time = 1)
        for i in range(len(graph.functions)):
            graph.set_shape_keys_bounded_region(index = i)

        hawks_and_doves = tex_bobject.TexBobject(
            #'\\text{Hawks and Doves}',
            '\\begin{array}{@{}c@{}}\\text{Hawks and} \\\\ \\text{Doves} \\end{array}',
            rotation_euler = [74 * math.pi / 180, 0, 0],
            location = [7, 0, 8],
            scale = 2,
            centered = True
        )

        '''graph.change_window(
            start_time = 3,
            end_time = 4,
            new_x_range = [0, 100],
            new_tick_step = [50, 20]
        )'''


        drawn_world.animate_days(
            start_time = 10,
            first_animated_day = 0,
            #last_animated_day = 11,
            phase_duration_updates = updates,
            graph_only = True
        )


        '''hawks_and_doves.add_to_blender(
            appear_time = 1
        )


        scale = 1
        tail1 = [11.5, 4.01]
        head1 = [9.5, 4]
        tail2 = [11.5, 2.01]
        head2 = [9.5, 2]
        tail3 = [9.5 + math.sqrt(2), 8 + math.sqrt(2)]
        head3 = [9.5, 8]
        tail4 = [3, 11]
        head4 = [3, 9]

        arrow1 = gesture.Gesture(
            gesture_series = [
                {
                    'type': 'arrow',
                    'points': {
                        'tail': (tail1[0] / scale, tail1[1] / scale, 0),
                        'head': (head1[0] / scale, head1[1] / scale, 0)
                    }
                },
                {
                    'type': 'arrow',
                    'points': {
                        'tail': (tail2[0] / scale, tail2[1] / scale, 0),
                        'head': (head2[0] / scale, head2[1] / scale, 0)
                    }
                },
                {
                    'type': 'arrow',
                    'points': {
                        'tail': (tail1[0] / scale, tail1[1] / scale, 0),
                        'head': (head1[0] / scale, head1[1] / scale, 0)
                    }
                },
                {
                    'type': 'arrow',
                    'points': {
                        'tail': (tail3[0] / scale, tail3[1] / scale, 0),
                        'head': (head3[0] / scale, head3[1] / scale, 0)
                    }
                },
                {
                    'type': 'arrow',
                    'points': {
                        'tail': (tail4[0] / scale, tail4[1] / scale, 0),
                        'head': (head4[0] / scale, head4[1] / scale, 0)
                    }
                }
            ],
            scale = scale,
        )

        arrow1.ref_obj.parent = graph.ref_obj
        arrow1.add_to_blender(appear_time = 100)
        arrow1.morph_figure(1, start_time = 102)
        arrow1.morph_figure(2, start_time = 104)
        arrow1.morph_figure(3, start_time = 106)
        arrow1.morph_figure(4, start_time = 110)'''


        '''disappear_time = 50
        to_disappear = [graph, hawks_and_doves, drawn_world]
        for i, thing in enumerate(to_disappear):
            thing.disappear(
                disappear_time = disappear_time - (len(to_disappear) - i - 1) * 0.05
            )'''

    def hawks_then_dove(self):
        cam_bobj, cam_swivel = cam_and_swivel(
            cam_location = [0, 0, 34],
            cam_rotation_euler = [0, 0, 0],
            cam_name = "Camera Bobject",
            swivel_location = [0, 0, 4],
            swivel_rotation_euler = [74 * math.pi / 180, 0, 0],
            swivel_name = 'Cam swivel',
            #control_sun = True
        )
        cam_swivel.add_to_blender(appear_time = -1, animate = False)

        new_sim = False
        if new_sim == True:
            world = hawk_dove.World(food_count = 61)
            num_days = 10

            for i in range(num_days):
                save = False
                if i == num_days - 1:
                    save = True
                try:
                    world.new_day(save = save)
                except:
                    print()
                    print('Saving did not work')
                    print()
                    world.new_day(save = False)

        else:
            world = 'hawks_10_then_doves_150'#'hawks_10_then_doves_150_butwait'

        if isinstance(world, str):
            result = os.path.join(
                SIM_DIR,
                world
            ) + ".pkl"
            print(result)
            with open(result, 'rb') as input:
                print(input)
                world = pickle.load(input)
                print("Loaded the world")

        #replace one dove with a hawk in the most recent generation
        edit_sim = False
        if edit_sim == True:
            old_cre = world.calendar[-1].next_creatures.pop()
            new_cre = hawk_dove.Creature(
                fight_chance = 0,
                parent = old_cre.parent
            )
            world.calendar[-1].next_creatures.append(new_cre)

        add_to_sim = False
        if add_to_sim == True:
            sys.setrecursionlimit(14000)
            num_days = 150
            for i in range(num_days):
                save = False
                if i == num_days - 1:
                    #print(i)
                    #time.sleep(1)
                    save = True
                world.new_day(save = save)#, filename = 'intro_hawk')

        graph = graph_bobject.GraphBobject(
            #demand_curve, supply_curve,
            location = [-11, -4, 0],
            rotation_euler = [74 * math.pi / 180, 0, 0],
            x_range = 10,
            y_range = 120,
            width = 11,
            height = 11,
            tick_step = [5, 20],
            x_label = "\\text{Days}",
            y_label = "\\text{Creatures}",
            y_label_pos = 'end',
            arrows = 'positive',
            centered = False,
            scale = 1,
            high_res_curve_indices = [],
            discrete_interpolation_style = 'linear',
            show_functions = False
        )

        #drawn_world.linked_graph = graph
        #drawn_food.add_functions_to_graph()

        drawn_world = drawn_contest_world.DrawnWorld(
            sim = world,
            loud = True,
            linked_graph = graph,
            location = [7.5, 0, 0],
            scale = 6.5,
            wiggle = True
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
                10,
                {
                    #'day_prep' : CREATURE_MOVE_DURATION,
                    #'creatures_go_out' : CREATURE_MOVE_DURATION,
                    #'pause_before_contest' : PAUSE_LENGTH,
                    #'contest' : CREATURE_MOVE_DURATION,
                    #'pause_before_home' : PAUSE_LENGTH,
                    #'creatures_go_home' : CREATURE_MOVE_DURATION,
                    #'pause_before_reset' : PAUSE_LENGTH,
                    'food_disappear' : 8.5,
                }
            ],
            [
                11,
                {
                    'day_prep' : 3.5,
                    #'creatures_go_out' : CREATURE_MOVE_DURATION,
                    #'pause_before_contest' : PAUSE_LENGTH,
                    #'contest' : CREATURE_MOVE_DURATION,
                    #'pause_before_home' : PAUSE_LENGTH,
                    #'creatures_go_home' : CREATURE_MOVE_DURATION,
                    #'pause_before_reset' : PAUSE_LENGTH,
                    'food_disappear' : NEW_CREATURE_MOVE_DURATION,
                }
            ],
            [
                12,
                {
                    'day_prep' : NEW_CREATURE_MOVE_DURATION,
                    #'creatures_go_out' : CREATURE_MOVE_DURATION,
                    #'pause_before_contest' : PAUSE_LENGTH,
                    #'contest' : CREATURE_MOVE_DURATION,
                    #'pause_before_home' : PAUSE_LENGTH,
                    #'creatures_go_home' : CREATURE_MOVE_DURATION,
                    #'pause_before_reset' : PAUSE_LENGTH,
                    'food_disappear' : NEW_CREATURE_MOVE_DURATION,
                }
            ]
        ]

        graph.add_to_blender(appear_time = 180)
        drawn_world.add_to_blender(appear_time = 180)
        for i in range(len(graph.functions)):
            graph.set_shape_keys_bounded_region(index = i)

        hawks_and_doves = tex_bobject.TexBobject(
            '\\text{Hawks only}',
            '\\begin{array}{@{}c@{}}\\text{Hawks first,} \\\\ \\text{then Doves} \\end{array}',
            rotation_euler = [74 * math.pi / 180, 0, 0],
            location = [7, 0, 8],
            scale = 2,
            centered = True
        )
        hawks_and_doves.add_to_blender(
            appear_time = 180
        )
        hawks_and_doves.morph_figure(1, start_time = 217.5)

        scale = 1
        tail1 = [11, 2]
        head1 = [9.2, 0.2]
        #tail2 = [11.5, 2.01]
        #head2 = [9.5, 2]
        #tail3 = [9.5 + math.sqrt(2), 8 + math.sqrt(2)]
        #head3 = [9.5, 8]
        #tail4 = [3, 11]
        #head4 = [3, 9]

        arrow1 = gesture.Gesture(
            gesture_series = [
                {
                    'type': 'arrow',
                    'points': {
                        'tail': (tail1[0] / scale, tail1[1] / scale, 0),
                        'head': (head1[0] / scale, head1[1] / scale, 0)
                    }
                }
            ],
            scale = scale,
        )

        arrow1.ref_obj.parent = graph.ref_obj
        arrow1.add_to_blender(appear_time = 217.5)

        scale = 1
        tail1 = [7.25, 4.75]
        head1 = [7.25, 2.75]

        arrow2 = gesture.Gesture(
            gesture_series = [
                {
                    'type': 'arrow',
                    'points': {
                        'tail': (tail1[0] / scale, tail1[1] / scale, 0),
                        'head': (head1[0] / scale, head1[1] / scale, 0)
                    }
                }
            ],
            scale = scale,
            rotation_euler = [74 * math.pi / 180, 0, 0]
        )
        arrow2.add_to_blender(appear_time = 217.5)
        arrow2.disappear(disappear_time = 221)
        arrow1.disappear(disappear_time = 221)

        sotf = tex_bobject.TexBobject(
            '\\text{Survival of the fittest}',
            '\\text{Survival of the fittest?}',
            location = [1.5, 9.5, 0]
        )
        sotf.ref_obj.parent = graph.ref_obj
        sotf.add_to_blender(appear_time = 605.5)
        sotf.morph_figure(1, start_time = 608.5)

        drawn_world.animate_days(
            start_time = 182,
            first_animated_day = 0,
            last_animated_day = 80,
            phase_duration_updates = updates,
            #graph_only = True
        )

        disappear_time = 621
        to_disappear = [sotf, graph, hawks_and_doves, drawn_world]
        for i, thing in enumerate(to_disappear):
            thing.disappear(
                disappear_time = disappear_time - (len(to_disappear) - i - 1) * 0.05
            )

    def big_sim(self):
        cam_bobj, cam_swivel = cam_and_swivel(
            cam_location = [0, 0, 34],
            cam_rotation_euler = [0, 0, 0],
            cam_name = "Camera Bobject",
            swivel_location = [0, 0, 4],
            swivel_rotation_euler = [74 * math.pi / 180, 0, 0],
            swivel_name = 'Cam swivel',
            control_sun = True
        )
        cam_swivel.add_to_blender(appear_time = -1, animate = False)

        multiple = 30

        is_sim = True
        num_days = 49
        num_creatures = 2 #int(121 * multiple / 2)
        if is_sim == True:
            world = hawk_dove.World(
                food_count = 61 * multiple,
                initial_creatures = num_creatures
            )

            for i in range(num_days):
                save = False
                if i == num_days - 1:
                    save = True
                try:
                    world.new_day(save = save)
                except:
                    print()
                    print('Saving did not work')
                    print()
                    world.new_day(save = False)

        graph = graph_bobject.GraphBobject(
            #demand_curve, supply_curve,
            location = [-10, -4, 0],
            rotation_euler = [74 * math.pi / 180, 0, 0],
            x_range = num_days + 1,
            y_range = 120 * multiple * 0.8,
            width = 23,
            height = 11,
            tick_step = [num_days + 1, 500],
            x_label = "\\text{Days}",
            y_label = "\\text{Creatures}",
            y_label_pos = 'end',
            arrows = 'positive',
            centered = False,
            scale = 1,
            high_res_curve_indices = [],
            discrete_interpolation_style = 'linear',
            show_functions = False
        )

        if is_sim == True:
            drawn_world = drawn_contest_world.DrawnWorld(
                sim = world,
                loud = True,
                linked_graph = graph,
                location = [7.5, 0, 0],
                scale = 6.5,
                bounded_regions = False
            )

            funcs = graph.functions
            save_sim_result(funcs, None, 'big_sim_funcs')

            '''graph.add_to_blender(appear_time = 1)
            for i in range(len(graph.functions)):
                graph.set_shape_keys_bounded_region(index = i)

            drawn_world.animate_days(
                start_time = 10,
                first_animated_day = 0,
                #last_animated_day = 11,
                #phase_duration_updates = updates,
                graph_only = True
            )'''


        elif is_sim == False:
            sim = '50percent_610food'

            #'hawks_first_2000days'
            #'doves_first_2000days'
            #'ess_first_2000days'

            result = os.path.join(
                SIM_DIR,
                sim
            ) + ".pkl"
            with open(result, 'rb') as input:
                funcs = pickle.load(input)

            for func in funcs:
                graph.functions.append(func)
                graph.functions_coords.append( graph.func_to_coords(func_index = -1) )


        reduce = None#10
        if reduce != None:
            '''for func, coords in zip(graph.functions, graph.functions_coords):
                func = func[::reduce]
                coords = coords[::reduce]'''
            for i in range(len(graph.functions)):
                graph.functions[i] = graph.functions[i][::reduce]
                graph.functions_coords[i] = graph.functions_coords[i][::reduce]

        graph.add_all_bounded_regions()#colors = [3, 6])

        graph.add_to_blender(appear_time = 0)
        graph.animate_all_bounded_regions(
            start_time = 1,
            end_time = 4
        )
        graph.disappear(disappear_time = 4.5)

    def payoff_grid(self):

        dd_time = 242
        dh_time = 245.5
        hd_time = 252.5
        hh_time = 256.25


        dd = tex_bobject.TexBobject(
            '1, 1',
            centered = True,
            scale = 1.5
        )
        dh = tex_bobject.TexBobject(
            '\\dfrac{1}{2}, \\dfrac{3}{2}',
            centered = True,
            scale = 1.5
        )
        hd = tex_bobject.TexBobject(
            '\\dfrac{3}{2}, \\dfrac{1}{2}',
            centered = True,
            scale = 1.5
        )
        hh = tex_bobject.TexBobject(
            '0, 0',
            '\\dfrac{1}{4}, \\dfrac{1}{4}',
            #'\\dfrac{1}{2}, \\dfrac{1}{2}',
            '\\dfrac{3}{4}, \\dfrac{3}{4}',
            centered = True,
            scale = 1.5
        )

        def color_elements():
            for pos in [0, 2]:
                dd.lookup_table[0][pos].color_shift(
                    color = COLORS_SCALED[2],
                    start_time = -1,
                    duration_time = None
                )
                hh.lookup_table[0][pos].color_shift(
                    color = COLORS_SCALED[5],
                    start_time = -1,
                    duration_time = None
                )

            for i in range(0, 3):
                dh.lookup_table[0][i].color_shift(
                    color = COLORS_SCALED[2],
                    start_time = -1,
                    duration_time = None
                )
                hd.lookup_table[0][i].color_shift(
                    color = COLORS_SCALED[5],
                    start_time = -1,
                    duration_time = None
                )

            for i in range(4, 7):
                dh.lookup_table[0][i].color_shift(
                    color = COLORS_SCALED[5],
                    start_time = -1,
                    duration_time = None
                )
                hd.lookup_table[0][i].color_shift(
                    color = COLORS_SCALED[2],
                    start_time = -1,
                    duration_time = None
                )

            for pos in [1, 4, 5, 6]:
                hh.lookup_table[1][pos].color_shift(
                    color = COLORS_SCALED[5],
                    start_time = -1,
                    duration_time = None
                )

        color_elements()

        em = [
            [dd, dh],
            [hd, hh]
        ]

        grid = table_bobject.TableBobject(
            width = 10,
            height = 10,
            location = [-3.5, 3, 0],
            cell_padding = 2,
            centered = True,
            element_matrix = em,
            style = 'full_grid',
            scale = 1
        )

        grid.add_to_blender(
            appear_time = 0,
            subbobject_timing = [
                dd_time * FRAME_RATE, dh_time * FRAME_RATE,
                hd_time * FRAME_RATE, hh_time * FRAME_RATE,
                dd_time * FRAME_RATE - 90 + 0,
                dd_time * FRAME_RATE - 90 +  60,
                dd_time * FRAME_RATE - 90 +  30,
                dd_time * FRAME_RATE - 90 +  0,
                dd_time * FRAME_RATE - 90 +  60,
                dd_time * FRAME_RATE - 90 +  30
            ]
        )

        d1 = blobject.Blobject(
            mat = 'creature_color3',
            scale = 2,
            location = [-2, -2.5, 0],
            #wiggle = True
        )
        d1.add_to_blender(appear_time = dd_time)
        d1.ref_obj.parent = grid.ref_obj

        h1 = blobject.Blobject(
            mat = 'creature_color6',
            scale = 2,
            location = [-2, -7.5, 0],
            #wiggle = True
        )
        h1.add_to_blender(appear_time = hd_time)
        h1.angry_eyes(start_time = -1, end_time = None)
        h1.ref_obj.parent = grid.ref_obj

        d2 = blobject.Blobject(
            mat = 'creature_color3',
            scale = 2,
            location = [2.35, 2.5, 0],
            #wiggle = True
        )
        d2.add_to_blender(appear_time = dd_time)
        d2.ref_obj.parent = grid.ref_obj

        h2 = blobject.Blobject(
            mat = 'creature_color6',
            scale = 2,
            location = [7, 2.5, 0],
            #wiggle = True
        )
        h2.add_to_blender(appear_time = dh_time)
        h2.angry_eyes(start_time = -1, end_time = None)
        h2.ref_obj.parent = grid.ref_obj

        def pulses():
            '''times = [dd_time, dh_time, hd_time, hh_time]
            sets = [
                [[d1, dd.lookup_table[0][0]], [d2, dd.lookup_table[0][2]]],
                [[d1, dh.lookup_table[0][0]], [h2, dh.lookup_table[0][2]]],
                [[h1, hd.lookup_table[0][0]], [d2, hd.lookup_table[0][2]]],
                [[h1, hh.lookup_table[0][0]], [h2, hh.lookup_table[0][2]]]
            ]

            for time, set in zip(times, sets):
                for i, pair in enumerate(set):
                    for thing in pair:
                        thing.pulse(
                            start_time = time + 1 + i,
                            duration_time = 1
                        )'''

            #dd pulses
            d1.pulse(start_time = dd_time + 1, duration_time = 1)
            d1.nod_yes(start_time = dd_time + 1, end_time = dd_time + 2)
            dd.lookup_table[0][0].pulse(start_time = dd_time + 1, duration_time = 1)
            d2.pulse(start_time = dd_time + 1.5, duration_time = 1)
            d2.nod_yes(start_time = dd_time + 1.5, end_time = dd_time + 2.5)
            dd.lookup_table[0][2].pulse(start_time = dd_time + 1.5, duration_time = 1)

            #dh pulses
            d1.pulse(start_time = dh_time + 1, duration_time = 1)
            d1.wince(start_time = dh_time + 1, end_time = dh_time + 2.5, period = 0.25)
            dh.lookup_table[0][0].pulse(start_time = dh_time + 1, duration_time = 1)
            dh.lookup_table[0][1].pulse(start_time = dh_time + 1, duration_time = 1)
            dh.lookup_table[0][2].pulse(start_time = dh_time + 1, duration_time = 1)
            h2.pulse(start_time = dh_time + 3, duration_time = 1.5)
            h2.evil_pose(start_time = dh_time + 3, end_time = dh_time + 4.5)
            dh.lookup_table[0][4].pulse(start_time = dh_time + 3, duration_time = 1.5)
            dh.lookup_table[0][5].pulse(start_time = dh_time + 3, duration_time = 1.5)
            dh.lookup_table[0][6].pulse(start_time = dh_time + 3, duration_time = 1.5)

            #hd pulses
            h1.pulse(start_time = hd_time + 1.5, duration_time = 1)
            h1.evil_pose(start_time = hd_time + 1.5, end_time = hd_time + 2.5)
            hd.lookup_table[0][0].pulse(start_time = hd_time + 1.5, duration_time = 1)
            hd.lookup_table[0][1].pulse(start_time = hd_time + 1.5, duration_time = 1)
            hd.lookup_table[0][2].pulse(start_time = hd_time + 1.5, duration_time = 1)
            d2.pulse(start_time = hd_time + 2, duration_time = 1)
            d2.wince(start_time = hd_time + 2, end_time = hd_time + 3.5, period = 0.25)
            hd.lookup_table[0][4].pulse(start_time = hd_time + 2, duration_time = 1)
            hd.lookup_table[0][5].pulse(start_time = hd_time + 2, duration_time = 1)
            hd.lookup_table[0][6].pulse(start_time = hd_time + 2, duration_time = 1)

            #hh pulses
            h1.pulse(start_time = hh_time + 1.5, duration_time = 1)
            h1.blob_wave(start_time = hh_time, duration = 3.5)
            h1.wince(start_time = hh_time + 3.5, end_time = hh_time + 5, period = 0.25)
            hh.lookup_table[0][0].pulse(start_time = hh_time + 1.5, duration_time = 1)
            h2.pulse(start_time = hh_time + 2.25, duration_time = 1)
            h2.blob_wave(start_time = hh_time, duration = 3.5)
            h2.wince(start_time = hh_time + 3.5, end_time = hh_time + 5, period = 0.25)
            hh.lookup_table[0][2].pulse(start_time = hh_time + 2.25, duration_time = 1)

        pulses()

        h1.move_to(new_scale = 0, start_time = 264)
        h2.move_to(new_scale = 0, start_time = 264)

        def go_to_dove_1(blob, start_time):
            blob.move_to(
                new_location = [
                    -2,
                    -2.5,
                    0
                ],
                start_time = start_time
            )
            blob.color_shift(
                color = COLORS_SCALED[2],
                start_time = start_time,
                duration_time = None,
                obj = blob.ref_obj.children[0].children[0]
            )
        def go_to_mid_1(blob, start_time):
            blob.move_to(
                new_location = [
                    -2,
                    -10 / 2,
                    0
                ],
                start_time = start_time
            )
            blob.color_shift(
                color = mix_colors_hsv(COLORS_SCALED[2], COLORS_SCALED[5], 0.5),
                start_time = start_time,
                duration_time = None,
                obj = blob.ref_obj.children[0].children[0]
            )
        def go_to_hawk_1(blob, start_time):
            blob.move_to(
                new_location = [
                    -2,
                    -7.5,
                    0
                ],
                start_time = start_time
            )
            blob.color_shift(
                color = COLORS_SCALED[5],
                start_time = start_time,
                duration_time = None,
                obj = blob.ref_obj.children[0].children[0]
            )

        def go_to_dove_2(blob, start_time):
            blob.walk_to(
                new_location = [
                    2.35,
                    2.5,
                    0
                ],
                start_time = start_time
            )
            blob.color_shift(
                color = COLORS_SCALED[2],
                start_time = start_time,
                duration_time = None,
                obj = blob.ref_obj.children[0].children[0]
            )
        def go_to_mid_2(blob, start_time):
            blob.walk_to(
                new_location = [
                    9.35 / 2,
                    2.5,
                    0
                ],
                start_time = start_time
            )
            blob.color_shift(
                #color = COLORS_SCALED[7],
                color = mix_colors_hsv(COLORS_SCALED[2], COLORS_SCALED[5], 0.5),
                start_time = start_time,
                duration_time = None,
                obj = blob.ref_obj.children[0].children[0]
            )
        def go_to_hawk_2(blob, start_time):
            blob.walk_to(
                new_location = [
                    7,
                    2.5,
                    0
                ],
                start_time = start_time
            )
            blob.color_shift(
                color = COLORS_SCALED[5],
                start_time = start_time,
                duration_time = None,
                obj = blob.ref_obj.children[0].children[0]
            )

        #You control side, and I control top
        go_to_mid_1(d1, 264)
        go_to_mid_2(d2, 264)
        me = tex_bobject.TexBobject(
            '\\text{Me}',
            location = [1.4, 0, 0],
            scale = 0.75,
            centered = True
        )
        constraint = me.ref_obj.constraints.new('CHILD_OF')
        constraint.target = d2.ref_obj
        constraint.use_rotation_x = False
        constraint.use_rotation_y = False
        constraint.use_rotation_z = False
        me.add_to_blender(appear_time = 267)

        you = tex_bobject.TexBobject(
            '\\text{You}',
            location = [-1.5, 0, 0],
            scale = 0.75,
            centered = True
        )
        constraint = you.ref_obj.constraints.new('CHILD_OF')
        constraint.target = d1.ref_obj
        constraint.use_rotation_x = False
        constraint.use_rotation_y = False
        constraint.use_rotation_z = False
        you.add_to_blender(appear_time = 268.5)

        #If I go hawk, you go dove
        go_to_hawk_2(d2, 271)
        d2.angry_eyes(start_time = 271, end_time = None)
        go_to_dove_1(d1, 277.5)
        d1.angry_eyes(start_time = 280.5, end_time = 283, left = False)
        d1.angry_eyes(start_time = 284, end_time = 307)
        go_to_hawk_1(d1, 284.5)
        d1.blob_wave(start_time = 285.75, duration = 1.5)
        d1.move_head(
            start_time = 296,
            end_time = 300,
            rotation_quaternion = [1, 0.2, 0, 0]
        )

        hh.lookup_table[0][0].pulse(start_time = 308.5, duration_time = 2)
        dh.lookup_table[0][0].pulse(start_time = 308.5, duration_time = 2)
        dh.lookup_table[0][2].pulse(start_time = 308.5, duration_time = 2)
        dh.lookup_table[0][3].pulse(start_time = 308.5, duration_time = 2)
        go_to_dove_1(d1, 311)



        scale = 1
        tail1 = [d2.ref_obj.location[0], -6]
        head1 = [d2.ref_obj.location[0], -4.25]
        arrow_42 = gesture.Gesture(
            gesture_series = [
                {
                    'type': 'arrow',
                    'points': {
                        'tail': (tail1[0] / scale, tail1[1] / scale, 0),
                        'head': (head1[0] / scale, head1[1] / scale, 0)
                    }
                },
                {
                    'type': 'arrow',
                    'points': {
                        'tail': (head1[0] / scale, head1[1] / scale, 0),
                        'head': (tail1[0] / scale, tail1[1] / scale, 0)
                    }
                }
            ],
            scale = scale,
        )

        arrow_42.ref_obj.parent = grid.ref_obj
        arrow_42.add_to_blender(appear_time = 315.5)
        arrow_42.subbobjects[0].pulse(start_time = 320, duration_time = 1)

        #Reset
        go_to_mid_2(d2, 323)
        d2.normal_eyes(start_time = 323, end_time = None)
        go_to_mid_1(d1, 323)

        #If I go dove, you go hawk
        go_to_dove_2(d2, 326.5)
        go_to_hawk_1(d1, 330)
        go_to_dove_1(d1, 335.5)
        d1.nod_yes(start_time = 336, end_time = 337.5)
        dd.lookup_table[0][0].pulse(start_time = 343, duration_time = 2)
        hd.lookup_table[0][0].pulse(start_time = 343, duration_time = 2)
        hd.lookup_table[0][2].pulse(start_time = 343, duration_time = 2)
        hd.lookup_table[0][3].pulse(start_time = 343, duration_time = 2)
        go_to_hawk_1(d1, 345)

        scale = 1
        tail1 = [d2.ref_obj.location[0], -4]
        head1 = [d2.ref_obj.location[0], -5.75]
        arrow_13 = gesture.Gesture(
            gesture_series = [
                {
                    'type': 'arrow',
                    'points': {
                        'tail': (tail1[0] / scale, tail1[1] / scale, 0),
                        'head': (head1[0] / scale, head1[1] / scale, 0)
                    }
                }
            ],
            scale = scale,
        )

        arrow_13.ref_obj.parent = grid.ref_obj
        arrow_13.add_to_blender(appear_time = 347)

        #Reset
        go_to_mid_2(d2, 349.5)
        go_to_mid_1(d1, 349.5)

        scale = 1
        tail1 = [4, -2.5]
        head1 = [5.5, -2.5]
        arrow_12 = gesture.Gesture(
            gesture_series = [
                {
                    'type': 'arrow',
                    'points': {
                        'tail': (tail1[0] / scale, tail1[1] / scale, 0),
                        'head': (head1[0] / scale, head1[1] / scale, 0)
                    }
                }
            ],
            scale = scale,
        )

        arrow_12.ref_obj.parent = grid.ref_obj
        arrow_12.add_to_blender(appear_time = 357)

        scale = 1
        tail1 = [5.5, -7.5]
        head1 = [4, -7.5]
        arrow_43 = gesture.Gesture(
            gesture_series = [
                {
                    'type': 'arrow',
                    'points': {
                        'tail': (tail1[0] / scale, tail1[1] / scale, 0),
                        'head': (head1[0] / scale, head1[1] / scale, 0)
                    }
                },
                {
                    'type': 'arrow',
                    'points': {
                        'tail': (head1[0] / scale, head1[1] / scale, 0),
                        'head': (tail1[0] / scale, tail1[1] / scale, 0)
                    }
                }
            ],
            scale = scale,
        )

        arrow_43.ref_obj.parent = grid.ref_obj
        arrow_43.add_to_blender(appear_time = 357)

        #First Nash Equilibrium
        go_to_dove_2(d2, 366.5)
        go_to_hawk_1(d1, 366.5)
        arrow_13.subbobjects[0].pulse(start_time = 366.5, duration_time = 2)
        arrow_43.subbobjects[0].pulse(start_time = 366.5, duration_time = 2)

        #Other Nash Equilibrium
        go_to_hawk_2(d2, 368.5)
        go_to_dove_1(d1, 368.5)
        arrow_12.subbobjects[0].pulse(start_time = 368.5, duration_time = 2)
        arrow_42.subbobjects[0].pulse(start_time = 368.5, duration_time = 2)

        #Reset
        go_to_dove_2(d2, 376)
        h1.move_to(new_scale = 2, start_time = 376)
        h2.move_to(new_scale = 2, start_time = 376)
        you.disappear(disappear_time = 376.5)
        me.disappear(disappear_time = 376.5)



        gt = tex_bobject.TexBobject(
            '\\text{\"Game Theory\"}',
            '\\text{\"Nash Equilibrium\"}',
            location = [-9, 6, 0],
            scale = 1.5,
            centered = True
        )
        gt.add_to_blender(appear_time = 378.75)
        arrow_13.subbobjects[0].pulse(start_time = 382.5, duration_time = 0.5)
        arrow_43.subbobjects[0].pulse(start_time = 382.5, duration_time = 0.5)
        arrow_12.subbobjects[0].pulse(start_time = 382.5, duration_time = 0.5)
        arrow_42.subbobjects[0].pulse(start_time = 382.5, duration_time = 0.5)

        arrow_13.subbobjects[0].pulse(start_time = 383, duration_time = 0.5)
        arrow_43.subbobjects[0].pulse(start_time = 383, duration_time = 0.5)
        arrow_12.subbobjects[0].pulse(start_time = 383, duration_time = 0.5)
        arrow_42.subbobjects[0].pulse(start_time = 383, duration_time = 0.5)
        gt.morph_figure(1, start_time = 385)
        gt.move_to(new_scale = 1.4, start_time = 385)
        gt.disappear(disappear_time = 395.5)

        grid.move_to(
            new_location = [-9.5, 3, 0],
            start_time = 395,
            end_time = 396
        )

        def graph1():
            graph = graph_bobject.GraphBobject(
                #demand_curve, supply_curve,
                location = [30, 1.5, 0],
                #rotation_euler = [74 * math.pi / 180, 0, 0],
                x_range = 160,
                y_range = 120,
                width = 10,
                height = 5,
                tick_step = [40, 30],
                x_label = "\\text{t}",
                y_label = "\\text{N}",
                y_label_pos = 'end',
                x_label_pos = 'end',
                arrows = 'positive',
                centered = False,
                scale = 1,
                high_res_curve_indices = [],
                discrete_interpolation_style = 'linear',
                show_functions = False
            )

            sim = 'dove10hawk150'

            result = os.path.join(
                SIM_DIR,
                sim
            ) + ".pkl"
            with open(result, 'rb') as input:
                world = pickle.load(input)

            doves_by_day = []
            hawks_by_day = []
            for day in world.calendar:
                doves_by_day.append(len([x for x in day.creatures if x.fight_chance == 0]))
                hawks_by_day.append(len([x for x in day.creatures if x.fight_chance == 1]))

            #Add creatures from final update
            doves_by_day.append(len([x for x in world.calendar[-1].next_creatures if x.fight_chance == 0]))
            hawks_by_day.append(len([x for x in world.calendar[-1].next_creatures if x.fight_chance == 1]))

            for func in [doves_by_day, hawks_by_day]:
                graph.functions.append(func)
                graph.functions_coords.append( graph.func_to_coords(func_index = -1) )


            graph.add_all_bounded_regions()#colors = [3, 6])

            graph.add_to_blender(appear_time = 395)
            graph.move_to(
                new_location = [3, 1.5, 0],
                start_time = 396,
                end_time = 397
            )
            graph.animate_all_bounded_regions(
                start_time = 397,
                end_time = 398.5
            )
            graph.move_to(
                new_location = [30, 1.5, 0],
                start_time = 406.8,
                end_time = 407.8
            )
        graph1()

        def graph2():
            graph = graph_bobject.GraphBobject(
                #demand_curve, supply_curve,
                location = [30, -6, 0],
                #rotation_euler = [74 * math.pi / 180, 0, 0],
                x_range = 160,
                y_range = 120,
                width = 10,
                height = 5,
                tick_step = [40, 30],
                x_label = "\\text{t}",
                y_label = "\\text{N}",
                y_label_pos = 'end',
                x_label_pos = 'end',
                arrows = 'positive',
                centered = False,
                scale = 1,
                high_res_curve_indices = [],
                discrete_interpolation_style = 'linear',
                show_functions = False
            )

            sim = 'hawks_10_then_doves_150'

            result = os.path.join(
                SIM_DIR,
                sim
            ) + ".pkl"
            with open(result, 'rb') as input:
                world = pickle.load(input)

            doves_by_day = []
            hawks_by_day = []
            for day in world.calendar:
                doves_by_day.append(len([x for x in day.creatures if x.fight_chance == 0]))
                hawks_by_day.append(len([x for x in day.creatures if x.fight_chance == 1]))

            #Add creatures from final update
            doves_by_day.append(len([x for x in world.calendar[-1].next_creatures if x.fight_chance == 0]))
            hawks_by_day.append(len([x for x in world.calendar[-1].next_creatures if x.fight_chance == 1]))

            for func in [doves_by_day, hawks_by_day]:
                graph.functions.append(func)
                graph.functions_coords.append( graph.func_to_coords(func_index = -1) )


            graph.add_all_bounded_regions()#colors = [3, 6])

            graph.add_to_blender(appear_time = 40)
            graph.move_to(
                new_location = [3, -6, 0],
                start_time = 398.5,
                end_time = 399.5
            )
            graph.animate_all_bounded_regions(
                start_time = 399.5,
                end_time = 401
            )

            graph.move_to(
                new_location = [30, -6, 0],
                start_time = 407,
                end_time = 408
            )
        graph2()

        grid.move_to(
            new_location = [-3.5, 3, 0],
            start_time = 407,
            end_time = 408
        )

        grid.move_to(
            new_location = [-11.5, 4.5, 0],
            new_scale = 0.6,
            start_time = 414.5
        )

        def equations_and_whatnot():
            eq_con_lab = tex_bobject.TexBobject(
                '\\text{Equilibrium is when:}',
                '\\text{Equilibrium:}',#' \\phanton{aah}',
                '\\xcancel{\\text{Equilibrium:}}',#' \\phanton{aah}',
                '\\text{Equilibrium:}',#' \\phanton{aah}',
                location = [4.5, 3, 0],
                scale = 1.5,
                centered = True
            )
            eq_con_lab.add_to_blender(appear_time = 415.5)

            eq_con = tex_bobject.TexBobject(
                '\\text{Dove score} = \\text{Hawk score}',
                '\\text{D} = \\text{H}',
                '\\text{D} < \\text{H}',
                '\\text{D} = \\text{H}',
                location = [4.5, 0.5, 0],
                centered = True,
                scale = 1.5
            )
            eq_con.add_to_blender(appear_time = 416.5)

            eq_con_lab.morph_figure(1, start_time = 431)
            eq_con_lab.move_to(
                new_location = [-10.7, -3.8, 0],
                new_scale = 1,
                start_time = 431
            )
            eq_con.morph_figure(1, start_time = 431)
            eq_con.move_to(
                new_location = [-9.3, -5.6, 0],
                new_scale = 2.3,
                start_time = 431
            )

            dummy = tex_bobject.TexBobject(
                '\\text{HHHHi}',
                scale = 2
            )
            eq_box = table_bobject.TableBobject(
                width = 8,
                height = 7,
                location = [-13.6, -3, 0],
                cell_padding = 1.5,
                centered = True,
                element_matrix = [[dummy]],
                style = 'full_grid',
                scale = 1
            )
            eq_box.add_to_blender(
                appear_time = 432,
                subbobject_timing = [
                    0,
                    0, 30, 0, 30
                ]
            )
            dummy.disappear(disappear_time = 432)

            np_doves = tex_bobject.TexBobject(
                '90\% \\text{ Doves}',
                centered = True,
                location = [5, 0, 0],
                scale = 2
            )
            np_doves.add_to_blender(appear_time = 441.5)
            np_doves.disappear(disappear_time = 444)

            dove_score = tex_bobject.TexBobject(
                '\\text{D}',
                '0.95',
                '\\text{D}',
                '\\text{D}',
                centered = True
            )
            dove_rhs = tex_bobject.TexBobject(
                '\!=',
                '\!=\\,\\, 0.9',
                '\!=\\,\\,  0.9 \\cdot 1',
                '\!=\\,\\,  0.9 \\cdot 1',
                '\!=\\,\\,  0.9 \\cdot 1 + 0.1',
                '\!=\\,\\,  0.9 \\cdot 1 + 0.1 \\cdot\\nicefrac{1}{2}',
                '\!=\\,\\,  0.9 \\cdot 1 + 0.1 \\cdot\\nicefrac{1}{2}',
                '\!=\\,\\,  d \\cdot 1 + h \\cdot\\nicefrac{1}{2}',
                '\!=\\,\\,  d \\cdot 1 + (1-d) \\cdot\\nicefrac{1}{2}',
                '\!=\\,\\,  d \\cdot 1 + (1-d) \\cdot\\nicefrac{1}{2}',
            )
            dove_eq = tex_complex.TexComplex(
                dove_score, dove_rhs,
                location = [4.5, 0, 0],
                centered = True,
                scale = 1.75
            )
            annotations = True
            if annotations == True:
                dove_eq.add_annotation(
                    targets = [
                        0, #tex_bobject
                        [
                            [0, 0, 0, None],  #form, first char, last char
                            [1, 0, 3, 'arrow'],
                            [2, 0, 0, 'arrow'],
                            [3, 0, 0, None]
                        ],
                    ],
                    labels = [
                        [],
                        ['\\text{Expected}\\phantom{a}', '\\text{dove score}'],
                        ['\\text{Expected}\\phantom{a}', '\\text{dove score}'],
                        []
                    ],
                    alignment = 'top',
                    gest_scale = 0.6
                )
                dove_eq.add_annotation(
                    targets = [
                        1, #tex_bobject
                        [
                            [0, 0, 0, None],  #form, first char, last char
                            [1, 1, 3, None],
                            [2, 1, 5, None],
                            [3, 1, 5],
                            [4, 1, 5],
                            [5, 1, 5],
                            [6, 1, 5],
                            [7, 1, 3],
                            [8, 1, 3],
                            [9, 1, 3, None],
                        ],
                    ],
                    labels = [
                        [],
                        [],
                        [],
                        ['\\text{Score from}', '\\text{other doves}'],
                        ['\\text{Score from}', '\\text{other doves}'],
                        ['\\text{Score from}', '\\text{other doves}'],
                        ['\\text{Score from}', '\\text{other doves}'],
                        ['\\text{Score from}', '\\text{other doves}'],
                        ['\\text{Score from}', '\\text{other doves}'],
                        [],
                    ],
                    alignment = 'top',
                    gest_scale = 0.6
                )
                dove_eq.add_annotation(
                    targets = [
                        1, #tex_bobject
                        [
                            [0, 0, 0, None],  #form, first char, last char
                            [1, 0, 0, None],
                            [2, 0, 0, None],
                            [3, 0, 0, None],
                            [4, 0, 0, None],
                            [5, 7, 13, None],
                            [6, 7, 13],
                            [7, 5, 9],
                            [8, 5, 13],
                            [9, 5, 13, None],
                        ],
                    ],
                    labels = [
                        [],
                        [],
                        [],
                        [],
                        [],
                        [],
                        ['\\text{Score from}', '\\text{hawks}'],
                        ['\\text{Score from}', '\\text{hawks}'],
                        ['\\text{Score from}', '\\text{hawks}'],
                        []
                    ],
                    alignment = 'top',
                    gest_scale = 0.6
                )
            dove_eq.add_to_blender(appear_time = 444.5)

            dd_payoff_time = 450
            dh_payoff_time = 457.5

            dove_rhs.morph_figure(1, start_time = 445.25)
            dove_rhs.morph_figure(2, start_time = dd_payoff_time)
            dove_rhs.morph_figure(3, start_time = 451)
            dove_rhs.morph_figure(4, start_time = 452.75)
            dove_rhs.morph_figure(5, start_time = dh_payoff_time)
            dove_rhs.morph_figure(6, start_time = 458.5)
            dove_score.morph_figure(1, start_time = 465.5)

            d_lab = eq_con.lookup_table[1][0]
            h_lab = eq_con.lookup_table[1][2]
            for i in range(2):
                d_lab.pulse(
                    start_time = i + 474,
                    duration_time = 1
                )
                h_lab.pulse(
                    start_time = i + 474.5,
                    duration_time = 1
                )

            hawk_score = tex_bobject.TexBobject(
                '\\text{H}',
                '1.35',
                '\\text{H}',
                '\\text{H}',
                centered = True
            )
            hawk_rhs = tex_bobject.TexBobject(
                '\!=',
                '\!=\\,\\, 0.9',
                '\!=\\,\\, 0.9 \\cdot\\nicefrac{3}{2}',
                '\!=\\,\\, 0.9 \\cdot\\nicefrac{3}{2}',
                '\!=\\,\\, 0.9 \\cdot \\nicefrac{3}{2} + 0.1',
                '\!=\\,\\, 0.9 \\cdot \\nicefrac{3}{2} + 0.1 \\cdot 0',
                '\!=\\,\\, 0.9 \\cdot \\nicefrac{3}{2} + 0.1 \\cdot 0',
                '\!=\\,\\, d \\cdot \\nicefrac{3}{2} + h \\cdot 0',
                '\!=\\,\\, d \\cdot \\nicefrac{3}{2} + (1-d) \\cdot 0',
                '\!=\\,\\, d \\cdot \\nicefrac{3}{2} + (1-d) \\cdot 0',
                '\!=\\,\\, d \\cdot \\nicefrac{3}{2} + (1-d) \\cdot \\nicefrac{1}{4}',
                #'\!=\\,\\, d \\cdot \\nicefrac{3}{2} + (1-d) \\cdot \\nicefrac{1}{2}',
                '\!=\\,\\, d \\cdot \\nicefrac{3}{2} + (1-d) \\cdot \\nicefrac{3}{4}',
            )
            hawk_eq = tex_complex.TexComplex(
                hawk_score, hawk_rhs,
                location = [4.5, -2, 0],
                centered = True,
                scale = 1.75
            )
            annotations = True
            if annotations == True:
                hawk_eq.add_annotation(
                    targets = [
                        0, #tex_bobject
                        [
                            [0, 0, 0, None],  #form, first char, last char
                            [1, 0, 3, 'arrow'],
                            [2, 0, 0, 'arrow'],
                            [3, 0, 0, None],
                        ],
                    ],
                    labels = [
                        [],
                        ['\\text{Expected}\\phantom{a}', '\\text{hawk score}'],
                        ['\\text{Expected}\\phantom{a}', '\\text{hawk score}'],
                        []
                    ],
                    alignment = 'bottom',
                    gest_scale = 0.6
                )
                hawk_eq.add_annotation(
                    targets = [
                        1, #tex_bobject
                        [
                            [0, 0, 0, None],  #form, first char, last char
                            [1, 1, 3, None],
                            [2, 1, 7, None],
                            [3, 1, 7],
                            [4, 1, 7],
                            [5, 1, 7],
                            [6, 1, 7],
                            [7, 1, 5],
                            [8, 1, 5],
                            [9, 1, 5, None],
                            [10, 1, 5, None],
                            #[11, 1, 5, None],
                            [11, 1, 5, None],
                        ],
                    ],
                    labels = [
                        [],
                        [],
                        [],
                        ['\\text{Score from}', '\\text{doves}'],
                        ['\\text{Score from}', '\\text{doves}'],
                        ['\\text{Score from}', '\\text{doves}'],
                        ['\\text{Score from}', '\\text{doves}'],
                        ['\\text{Score from}', '\\text{doves}'],
                        ['\\text{Score from}', '\\text{doves}'],
                        [],
                        [],
                        #[],
                        []
                    ],
                    alignment = 'bottom',
                    gest_scale = 0.6
                )
                hawk_eq.add_annotation(
                    targets = [
                        1, #tex_bobject
                        [
                            [0, 0, 0, None],  #form, first char, last char
                            [1, 0, 0, None],
                            [2, 0, 0, None],
                            [3, 0, 0, None],
                            [4, 0, 0, None],
                            [5, 9, 13, None],
                            [6, 9, 13],
                            [7, 7, 9],
                            [8, 7, 13],
                            [9, 7, 13, None],
                            [10, 7, 13, None],
                            #[11, 7, 13, None],
                            [11, 7, 13, None],
                        ],
                    ],
                    labels = [
                        [],
                        [],
                        [],
                        [],
                        [],
                        [],
                        ['\\text{Score from}', '\\text{other hawks}'],
                        ['\\text{Score from}', '\\text{other hawks}'],
                        ['\\text{Score from}', '\\text{other hawks}'],
                        [],
                        [],
                        #[],
                        []
                    ],
                    alignment = 'bottom',
                    gest_scale = 0.6
                )
            hawk_eq.add_to_blender(appear_time = 478.5)
            dove_eq.move_to(
                new_location = [4.5, 2, 0],
                start_time = 478.5
            )

            hd_payoff_time = 493
            hh_payoff_time = 500
            hawk_rhs.morph_figure(1, start_time = 490)
            hawk_rhs.morph_figure(2, start_time = hd_payoff_time)
            hawk_rhs.morph_figure(3, start_time = 494)
            hawk_rhs.morph_figure(4, start_time = 496)
            hawk_rhs.morph_figure(5, start_time = hh_payoff_time)
            hawk_rhs.morph_figure(6, start_time = 501)
            hawk_score.morph_figure(1, start_time = 502.5)

            def color_equations_and_pulse():
                #Dove dove payoff
                for pos in [5]:
                    dove_rhs.lookup_table[3][pos].color_shift(
                        color = COLORS_SCALED[2],
                        start_time = -1,
                        duration_time = None
                    )
                to_highlight = dd.lookup_table[0][0:3:2]
                for thing in to_highlight:
                    thing.pulse(start_time = dd_payoff_time, duration_time = 1, factor = 1.5)
                    thing.wobble(start_time = dd_payoff_time, end_time = dd_payoff_time + 1)

                #Dove hawk payoff
                for pos in [11, 12, 13]:
                    dove_rhs.lookup_table[5][pos].color_shift(
                        color = COLORS_SCALED[2],
                        start_time = -1,
                        duration_time = None
                    )
                to_highlight = dh.lookup_table[0][0:4] + hd.lookup_table[0][4:7]
                for thing in to_highlight:
                    thing.pulse(start_time = dh_payoff_time, duration_time = 1, factor = 1.5)
                    thing.wobble(start_time = dh_payoff_time, end_time = dh_payoff_time + 1)

                #Hawk dove payoof
                for pos in [5, 6, 7]:
                    hawk_rhs.lookup_table[2][pos].color_shift(
                        color = COLORS_SCALED[5],
                        start_time = -1,
                        duration_time = None
                    )
                to_highlight = dh.lookup_table[0][4:7] + hd.lookup_table[0][0:4]
                for thing in to_highlight:
                    thing.pulse(start_time = hd_payoff_time, duration_time = 1, factor = 1.5)
                    thing.wobble(start_time = hd_payoff_time, end_time = hd_payoff_time + 1)

                #Hawk hawk payoff
                for pos in [13]:
                    hawk_rhs.lookup_table[5][pos].color_shift(
                        color = COLORS_SCALED[5],
                        start_time = -1,
                        duration_time = None
                    )
                for pos in [14, 15]:
                    hawk_rhs.lookup_table[10][pos].color_shift(
                        color = COLORS_SCALED[5],
                        start_time = 595,
                        duration_time = None
                    )
                to_highlight = hh.lookup_table[0][0:3:2]
                for thing in to_highlight:
                    thing.pulse(start_time = hh_payoff_time, duration_time = 1, factor = 1.5)
                    thing.wobble(start_time = hh_payoff_time, end_time = hh_payoff_time + 1)
            color_equations_and_pulse()

            hawk_score.pulse(start_time = 507, duration_time = 1)
            dove_score.pulse(start_time = 508, duration_time = 1)
            eq_con.morph_figure(2, start_time = 507.75)
            eq_con_lab.morph_figure(2, start_time = 507.75)
            eq_con.morph_figure(3, start_time = 522)
            eq_con_lab.morph_figure(3, start_time = 522)

            dove_score.morph_figure(2, start_time = 522)
            dove_rhs.morph_figure(7, start_time = 526)
            hawk_score.morph_figure(2, start_time = 522)
            hawk_rhs.morph_figure(7, start_time = 526)

            dove_rhs.morph_figure(8, start_time = 546.5)
            hawk_rhs.morph_figure(8, start_time = 546.5)

            to_highlight = [
                dove_rhs.lookup_table[8][1],
                dove_rhs.lookup_table[8][8],
                hawk_rhs.lookup_table[8][1],
                hawk_rhs.lookup_table[8][10],
            ]
            for thing in to_highlight:
                thing.pulse(start_time = 552.25, duration_time = 1, factor = 1.2)
                thing.wobble(start_time = 552.25, end_time = 552.25 + 1)

            dove_score.morph_figure(3, start_time = 554.5)
            dove_rhs.morph_figure(9, start_time = 554.5)
            hawk_score.morph_figure(3, start_time = 554.5)
            hawk_rhs.morph_figure(9, start_time = 554.5)
            dove_eq.move_to(
                new_location = [4.5, -3.75, 0],
                start_time = 554.5
            )
            hawk_eq.move_to(
                new_location = [4.5, -6.25, 0],
                start_time = 554.5
            )

            def grid_pulses():
                #Dove dove payoff
                base_time = 583.5
                for pos in [5]:
                    dove_rhs.lookup_table[3][5].pulse(
                        start_time = base_time,
                        duration_time = 0.5
                    )
                to_highlight = dd.lookup_table[0][0:3:2]
                for thing in to_highlight:
                    thing.pulse(start_time = base_time, duration_time = 0.5, factor = 1.2)

                #Dove hawk payoff
                for pos in [11, 12, 13]:
                    dove_rhs.lookup_table[5][pos].pulse(
                        start_time = base_time + 0.25,
                        duration_time = 0.5
                    )
                to_highlight = dh.lookup_table[0][0:4] + hd.lookup_table[0][4:7]
                for thing in to_highlight:
                    thing.pulse(start_time = base_time + 0.25, duration_time = 0.5, factor = 1.2)

                #Hawk dove payoof
                for pos in [5, 6, 7]:
                    hawk_rhs.lookup_table[2][pos].pulse(
                        start_time = base_time + 0.5,
                        duration_time = 0.5
                    )
                to_highlight = dh.lookup_table[0][4:7] + hd.lookup_table[0][0:4]
                for thing in to_highlight:
                    thing.pulse(start_time = base_time + 0.5, duration_time = 0.5, factor = 1.2)

                #Hawk hawk payoff
                for pos in [13]:
                    hawk_rhs.lookup_table[5][pos].pulse(
                        start_time = base_time + 0.75,
                        duration_time = 0.5
                    )
                for pos in [14, 15]:
                    hawk_rhs.lookup_table[10][pos].pulse(
                        start_time = base_time + 0.75,
                        duration_time = 0.5
                    )
                to_highlight = hh.lookup_table[0][0:3:2]
                for thing in to_highlight:
                    thing.pulse(start_time = base_time + 0.75, duration_time = 0.5, factor = 1.2)
            grid_pulses()

            hawk_rhs.morph_figure(10, start_time = 599)
            #hawk_rhs.morph_figure(11, start_time = 692.5)
            hawk_rhs.morph_figure(11, start_time = 694.25)

            to_disappear = [
                eq_con_lab, eq_con, eq_box,
                dove_eq, hawk_eq
            ]
            for thing in to_disappear:
                thing.disappear(disappear_time = 700.25)

        equations_and_whatnot()

        def dove_score_func1(x): return x * 1 + (1-x) * 1/2
        def hawk_score_func1(x): return x * 3/2 + (1-x) * 0
        def hawk_score_func2(x): return x * 3/2 + (1-x) * 1/4
        def hawk_score_func3(x): return x * 3/2 + (1-x) * 2/4
        def hawk_score_func4(x): return x * 3/2 + (1-x) * 3/4


        comparison_graph = graph_bobject.GraphBobject(
            #dove_score_func1, hawk_score_func1,
            #hawk_score_func2, hawk_score_func3,
            location = [-2, -0.75, 0],
            #rotation_euler = [74 * math.pi / 180, 0, 0],
            x_range = 1,
            y_range = 1.5,
            width = 14,
            height = 7,
            tick_step = [0.25, 0.5],
            x_label = "d \\phantom{lowercase}",
            y_label = "\\text{Expected score}",
            y_label_pos = 'end',
            #y_label_rot = True,
            x_label_pos = 'end',
            arrows = 'positive',
            centered = False,
            scale = 1,
            high_res_curve_indices = [],
            #discrete_interpolation_style = 'linear',
            show_functions = False
        )
        comparison_graph.add_to_blender(appear_time = 555)
        comparison_graph.add_new_function_and_curve(dove_score_func1, color = 3)
        comparison_graph.add_new_function_and_curve(hawk_score_func1, color = 6)
        comparison_graph.animate_all_function_curves(
            start_time = 556,
            end_time = 556.75,
            start_window = 0.25
        )
        D_lab = tex_bobject.TexBobject(
            '\\text{D}',
            location = [12.5, 3.5, 0]
        )
        D_lab.ref_obj.parent = comparison_graph.ref_obj
        D_lab.add_to_blender(appear_time = 557)
        H_lab = tex_bobject.TexBobject(
            '\\text{H}',
            location = [12.5, 5.3, 0]
        )
        H_lab.ref_obj.parent = comparison_graph.ref_obj
        H_lab.add_to_blender(appear_time = 557.25)

        scale = 1
        tail1 = [6, 6]
        head1 = [6, 3]
        tail2 = [4, 5.67]
        head2 = [4, 2.67]
        tail3 = [0.4 + 1.5, 2.2 + math.sqrt(9 - 2.25)]
        head3 = [0.4 , 2.2]
        eq_arrow = gesture.Gesture(
            gesture_series = [
                {
                    'type': 'arrow',
                    'points': {
                        'tail': (tail1[0] / scale, tail1[1] / scale, 0),
                        'head': (head1[0] / scale, head1[1] / scale, 0)
                    }
                },
                {
                    'type': 'arrow',
                    'points': {
                        'tail': (tail2[0] / scale, tail2[1] / scale, 0),
                        'head': (head2[0] / scale, head2[1] / scale, 0)
                    }
                }
            ],
            scale = scale,
        )
        eq_arrow.ref_obj.parent = comparison_graph.ref_obj
        eq_arrow.add_to_blender(appear_time = 562.75)



        #My handling of functions in graph bobjects is trash
        comparison_graph.functions.append(hawk_score_func2)
        comparison_graph.functions_coords.append(comparison_graph.func_to_coords(func_index = 2))
        hh.morph_figure(1, start_time = 599)
        comparison_graph.morph_curve(
            2,
            from_curve_index = 1,
            start_time = 601.75,
            end_time = 602.25
        )
        eq_arrow.morph_figure(1, start_time = 601.75)

        '''comparison_graph.functions.append(hawk_score_func3)
        comparison_graph.functions_coords.append(comparison_graph.func_to_coords(func_index = 3))
        hh.morph_figure(2, start_time = 692.5)
        comparison_graph.morph_curve(
            3,
            from_curve_index = 1,
            start_time = 692.5,
            end_time = 693
        )
        eq_arrow.morph_figure(2, start_time = 692.5)'''

        comparison_graph.functions.append(hawk_score_func4)
        comparison_graph.functions_coords.append(comparison_graph.func_to_coords(func_index = 3))
        hh.morph_figure(2, start_time = 694.25) #Was 3
        comparison_graph.morph_curve(
            3, #Was 2
            from_curve_index = 1,
            start_time = 694.25,
            end_time = 694.75
        )
        eq_arrow.disappear(disappear_time = 694.25)

        to_disappear = [
            comparison_graph #Rest in equations_and_whatnot()
        ]
        for thing in to_disappear:
            thing.disappear(disappear_time = 700.25)
        grid.move_to(
            new_location = [-3.5, 3, 0],
            new_scale = 1,
            start_time = 700,
            end_time = 700.5
        )

        #hh pulses
        hh.lookup_table[1][0].pulse(start_time = 701.5, duration_time = 1)
        hh.lookup_table[1][1].pulse(start_time = 701.5, duration_time = 1)
        hh.lookup_table[1][2].pulse(start_time = 701.5, duration_time = 1)
        hh.lookup_table[1][4].pulse(start_time = 701.5, duration_time = 1)
        hh.lookup_table[1][5].pulse(start_time = 701.5, duration_time = 1)
        hh.lookup_table[1][6].pulse(start_time = 701.5, duration_time = 1)

        dh.lookup_table[0][0].pulse(start_time = 704.5, duration_time = 1)
        dh.lookup_table[0][1].pulse(start_time = 704.5, duration_time = 1)
        dh.lookup_table[0][2].pulse(start_time = 704.5, duration_time = 1)
        hd.lookup_table[0][4].pulse(start_time = 704.5, duration_time = 1)
        hd.lookup_table[0][5].pulse(start_time = 704.5, duration_time = 1)
        hd.lookup_table[0][6].pulse(start_time = 704.5, duration_time = 1)

        arrow_42.morph_figure(1, start_time = 707.25)
        arrow_43.morph_figure(1, start_time = 707.25)

        arrow_12.subbobjects[0].pulse(start_time = 708, duration_time = 0.5)
        arrow_42.subbobjects[0].pulse(start_time = 708.25, duration_time = 0.5)
        arrow_13.subbobjects[0].pulse(start_time = 708.75, duration_time = 0.5)
        arrow_43.subbobjects[0].pulse(start_time = 709, duration_time = 0.5)

        #hh pulses
        hh.lookup_table[1][0].pulse(start_time = 712, duration_time = 1)
        hh.lookup_table[1][1].pulse(start_time = 712, duration_time = 1)
        hh.lookup_table[1][2].pulse(start_time = 712, duration_time = 1)
        hh.lookup_table[1][4].pulse(start_time = 712, duration_time = 1)
        hh.lookup_table[1][5].pulse(start_time = 712, duration_time = 1)
        hh.lookup_table[1][6].pulse(start_time = 712, duration_time = 1)
        #dd pulses
        dd.lookup_table[0][0].pulse(start_time = 714.5, duration_time = 1)
        dd.lookup_table[0][2].pulse(start_time = 714.5, duration_time = 1)

    def building_from_here(self):
        building = tex_bobject.TexBobject(
            '\\text{Building from here}',
            location = [-12, 5, 0],
            scale = 1.9
        )
        building.add_to_blender(appear_time = 622)

        mixed = tex_bobject.TexBobject(
            '\\text{Creatures with more than one strategy}',
            '\\text{Mixed strategies}',
            location = [-11, 2.25, 0],
            scale = 1.4
        )
        mixed.add_to_blender(appear_time = 628)

        container1 = bobject.Bobject(
            location = [0, -3.5, 0]
        )
        container1.add_to_blender(appear_time = 630)

        zero_blob = blobject.Blobject(
            location = [-4, 0, 0],
            scale = 4,
            mat = 'creature_color3',
            wiggle = True
        )
        zero_blob.ref_obj.parent = container1.ref_obj
        zero_blob.add_to_blender(appear_time = 631)
        one_blob = blobject.Blobject(
            location = [4, 0, 0],
            scale = 4,
            mat = 'creature_color6',
            wiggle = True
        )
        one_blob.ref_obj.parent = container1.ref_obj
        one_blob.add_to_blender(appear_time = 632)

        zero_blob.move_to(
            new_location = [-10, 0, 0],
            new_scale = 3,
            start_time = 634
        )
        one_blob.move_to(
            new_location = [10, 0, 0],
            new_scale = 3,
            start_time = 634
        )

        for i in range(1, 4):
            bleb = blobject.Blobject(
                location = [(i - 2) * 5, 0, 0],
                scale = 3,
                wiggle = True
            )
            bleb.color_shift(
                color = mix_colors_hsv(COLORS_SCALED[2], COLORS_SCALED[5], i / 4),
                start_time = 0,
                duration_time = None,
                obj = bleb.ref_obj.children[0].children[0]
            )
            bleb.add_to_blender(appear_time = 634)
            bleb.ref_obj.parent = container1.ref_obj
        mixed.morph_figure(1, start_time = 639.5)
        container1.move_to(
            new_location = [2.59351, 2.25, 0],
            new_scale = 0.254,
            start_time = 642
        )

        conditional = tex_bobject.TexBobject(
            '\\text{Conditional strategies}',
            location = [-11, -0.25, 0],
            scale = 1.4
        )
        conditional.add_to_blender(appear_time = 643)

        container2 = bobject.Bobject(
            location = [0, -4.5, 0],
            scale = 0.75
        )
        container2.add_to_blender(appear_time = 0)

        g_blob = blobject.Blobject(
            location = [-4, 0, 0],
            scale = 4,
            mat = 'creature_color7',
            wiggle = True
        )
        g_blob.ref_obj.parent = container2.ref_obj
        g_blob.add_to_blender(appear_time = 648)
        o_blob = blobject.Blobject(
            location = [4, 0, 0],
            scale = 4,
            mat = 'creature_color4',
            wiggle = True
        )
        o_blob.ref_obj.parent = container2.ref_obj
        o_blob.add_to_blender(appear_time = 652)

        container2.move_to(
            new_location = [3.73945, -0.25, 0],
            new_scale = 0.188,
            start_time = 668
        )

        asymmetric = tex_bobject.TexBobject(
            '\\text{Asymmetric contests}',
            location = [-11, -2.75, 0],
            scale = 1.4
        )
        asymmetric.add_to_blender(appear_time = 669.25)
        container3 = bobject.Bobject(
            location = [6.75, -5, 0],
            scale = 0.5
        )
        container3.add_to_blender(appear_time = 0)
        g_blob = blobject.Blobject(
            location = [-4, 0, 0],
            scale = 4,
            mat = 'creature_color6',
            wiggle = True
        )
        g_blob.ref_obj.parent = container3.ref_obj
        g_blob.add_to_blender(appear_time = 672)
        o_blob = blobject.Blobject(
            location = [4, 0, 0],
            scale = 4,
            mat = 'creature_color6',
            wiggle = True
        )
        o_blob.ref_obj.parent = container3.ref_obj
        o_blob.add_to_blender(appear_time = 672.5)

        cube_height = 2
        cube = import_object(
            'cube', 'primitives',
            scale = [
                o_blob.ref_obj.scale[0],
                cube_height / 2,
                o_blob.ref_obj.scale[2]
            ],
            location = [
                o_blob.ref_obj.location[0],
                o_blob.ref_obj.location[1] - o_blob.ref_obj.scale[1] + cube_height / 2,
                o_blob.ref_obj.location[2]
            ],
            mat = 'color2'
        )
        cube.ref_obj.parent = container3.ref_obj
        cube.add_to_blender(appear_time = 677)
        o_blob.move_to(
            displacement = [0, cube_height * 0.9, 0],
            start_time = 677
        )


        container3.move_to(
            new_location = [2.9, -2.75, 0],
            new_scale = 0.188,
            start_time = 682
        )



        pd = tex_bobject.TexBobject(
            '\\text{Prisoner\'s dilemma}',
            location = [-11, -5.25, 0],
            scale = 1.4
        )
        pd.add_to_blender(appear_time = 715)

        to_disappear = [
            building,
            mixed, container1,
            conditional, container2,
            asymmetric, container3,
            pd
        ]
        for i, thing in enumerate(to_disappear):
            thing.disappear(disappear_time = 723.5 - (len(to_disappear) - 1 - i) * 0.05)

    def teaser(self):
        bpy.context.scene.render.resolution_x = 1080
        bpy.context.scene.render.resolution_y = 1920
        bpy.data.cameras[0].type = 'ORTHO'

        #Wave
        def hello():
            me = blobject.Blobject(
                scale = 8,
            )
            me.add_to_blender(appear_time = 0)
            me.hello(start_time = 0.4, end_time = 1.4)

            me.move_to(
                new_location = [0, -6, 0],
                start_time = 4
            )
            me.move_head(
                rotation_quaternion = [1, -0.1, 0, 0.2],
                start_time = 12.5,
                end_time = 15
            )
            me.move_head(
                rotation_quaternion = [1, 0, 0.2, -0.2],
                start_time = 26.5,
                end_time = 28
            )

            me.hello(start_time = 35.5, end_time = 38)


        hello()

        def conflict():

            disp = 8.5#9.75
            scale_fac = 0.7

            food1 = import_object(
                'goodicosphere', 'primitives',
                mat = 'color7',
                location = [1, -5, 1],
                scale = scale_fac
            )
            food21 = import_object(
                'half_icosphere', 'primitives',
                location = [-1, -5, -1],
                rotation_euler = [0, -math.pi / 2, 0],
                mat = 'color7',
                scale = scale_fac
            )
            food22 = import_object(
                'half_icosphere', 'primitives',
                location = [-1, -5, -1],
                rotation_euler = [0, math.pi / 2, 0],
                mat = 'color7',
                scale = scale_fac
            )


            for f in [food1, food21, food22]:
                f.ref_obj.location = scalar_mult_vec(
                    deepcopy(f.ref_obj.location),
                    scale_fac
                )
                f.ref_obj.location[1] += disp

            food1.add_to_blender(appear_time = 6)
            food21.add_to_blender(appear_time = 6)
            food22.add_to_blender(appear_time = 6)

            dove = blobject.Blobject(
                location = [-19, -2, 0],
                rotation_euler = [0, math.pi / 2, 0],
                scale = 5 * scale_fac
            )
            dove.ref_obj.location = scalar_mult_vec(
                deepcopy(dove.ref_obj.location),
                scale_fac
            )
            dove.ref_obj.location[1] += disp
            dove.add_to_blender(appear_time = 5)
            new_loc = [-6, -2, 0]
            new_loc = scalar_mult_vec(deepcopy(new_loc), scale_fac)
            new_loc[1] += disp
            dove.walk_to(
                new_location = new_loc,
                start_time = 2
            )

            hawk = blobject.Blobject(
                location = [19, -2, 0],
                rotation_euler = [0, -math.pi / 2, 0],
                scale = 5 * scale_fac
            )
            hawk.ref_obj.location = scalar_mult_vec(
                deepcopy(hawk.ref_obj.location),
                scale_fac
            )
            hawk.ref_obj.location[1] += disp
            hawk.add_to_blender(appear_time = 5.5)
            new_loc = [6, -2, 0]
            new_loc = scalar_mult_vec(deepcopy(new_loc), scale_fac)
            new_loc[1] += disp
            hawk.walk_to(
                new_location = new_loc,
                start_time = 2
            )

            dove.move_head(
                rotation_quaternion = [1, 0.1, 0, -0.3],
                start_time = 7,
                end_time = 8
            )
            hawk.move_head(
                rotation_quaternion = [1, 00, 0, -0.3],
                start_time = 7,
                end_time = 8
            )

            dove.hello(start_time = 8.5, end_time = 10.5)
            dove.eat_animation(start_frame = 8.5 * FRAME_RATE, end_frame = 10.5 * FRAME_RATE)

            hawk.move_head(
                rotation_quaternion = [1, 0, 0.9, -0.1],
                start_time = 9.5,
                end_time = 10.5
            )
            hawk.color_shift(
                duration_time = None,
                color = COLORS_SCALED[5],
                start_time = 9.5,
                shift_time = FRAME_RATE / 2,
                obj = hawk.ref_obj.children[0].children[0]
            )
            hawk.angry_eyes(
                start_time = 9.5,
                attack = 0.5,
                end_time = None
            )


            def eats():
                drawn_contest_world.transfer_food_to_creature(
                    food_bobj = food22,
                    creature_bobj = hawk,
                    start_time = 10.5,
                    ground_plane = 'xz'
                )

                drawn_contest_world.animate_eating(
                    food = food22,
                    eater = hawk,
                    start_time = 10.5,
                    dur = 0.5,
                    eat_rotation = [0, -30 * math.pi / 180, 0]
                )

                drawn_contest_world.transfer_food_to_creature(
                    food_bobj = food21,
                    creature_bobj = dove,
                    start_time = 10.5,
                    ground_plane = 'xz'
                )

                drawn_contest_world.animate_eating(
                    food = food21,
                    eater = dove,
                    start_time = 10.5,
                    dur = 0.5,
                    eat_rotation = [0, 30 * math.pi / 180, 0]
                )

                drawn_contest_world.transfer_food_to_creature(
                    food_bobj = food1,
                    creature_bobj = hawk,
                    start_time = 11,
                    ground_plane = 'xz'
                )

                drawn_contest_world.animate_eating(
                    food = food1,
                    eater = hawk,
                    start_time = 11,
                    dur = 1,
                    eat_rotation = [0, 30 * math.pi / 180, 0]
                )

                dove.surprise_eyes(
                    start_time = 11,
                    end_time = 12
                )

            eats()

            dove.move_to(
                new_angle = [0, 0, 0],
                start_time = 12
            )
            dove.wince(start_time = 12.5, end_time = 15)
            hawk.move_to(
                new_angle = [0, 0, 0],
                start_time = 12
            )
            hawk.evil_pose(start_time = 12, end_time = 15)

            for thing in [hawk, dove, food1, food21, food22]:
                thing.move_to(
                    displacement = [-31, 0, 0],
                    start_time = 13.5,
                    end_time = 14.5
                )
        conflict()

        def sim():
            cam_bobj, cam_swivel = cam_and_swivel(
                cam_location = [0, 0, 32.8],
                cam_rotation_euler = [0, 0, 0],
                cam_name = "Camera Bobject",
                swivel_location = [0, 0, 0],
                swivel_rotation_euler = [74 * math.pi / 180, 0, 0],
                swivel_name = 'Cam swivel',
                #control_sun = True
            )
            cam_swivel.add_to_blender(appear_time = -1, animate = False)

            new_sim = True
            if new_sim == True:
                world = hawk_dove.World(
                    food_count = 19,
                    initial_creatures = 10
                )
                num_days = 5

                for i in range(num_days):
                    save = False
                    if i == num_days - 1:
                        save = True
                    world.new_day(save = save)
            else:
                world = 'doves_only'

            phase_durations = {
                'day_prep' : CREATURE_MOVE_DURATION,
                'creatures_go_out' : CREATURE_MOVE_DURATION,
                'pause_before_contest' : PAUSE_LENGTH,
                'contest' : CREATURE_MOVE_DURATION,
                'pause_before_home' : PAUSE_LENGTH,
                'creatures_go_home' : CREATURE_MOVE_DURATION,
                'pause_before_reset' : PAUSE_LENGTH,
                'food_disappear' : CREATURE_MOVE_DURATION,
            }
            drawn_world = drawn_contest_world.DrawnWorld(
                sim = world,
                loud = True,
                location = [31, 0, 7.25],
                scale = 7,
                #rotation_euler = [-70 * math.pi / 180, 0, 0],
                #phase_durations = phase_durations
            )
            #drawn_world.ref_obj.rotation_mode = 'ZYX'

            drawn_world.add_to_blender(appear_time = 0)

            drawn_world.move_to(
                displacement = [-31, 0, 0],
                start_time = 13.5 * 2,
                end_time = 14.5 * 2
            )
            '''drawn_world.move_to(
                new_angle = [0, 0, 2 * math.pi],
                start_time = 0,
                end_time = 13
            )'''
            drawn_world.spin(
                spin_rate = 0.02 / 2,
                start_time = 0,
                end_time = 60 * 2,
                axis = 2
            )

            drawn_world.animate_days(
                start_time = 14 * 2,
                first_animated_day = 0,
                #last_animated_day = 2,
                #phase_duration_updates = updates
            )

            drawn_world.move_to(
                displacement = [-31, 0, 0],
                start_time = 20.5 * 2,
                end_time = 21.5 * 2
            )
        #sim()

        def date():
            date1 = tex_bobject.TexBobject(
                '\\text{Saturday}',
                location = [31, 12, 0],
                centered = True,
                scale = 4
            )
            date1.add_to_blender(appear_time = 0)
            date2 = tex_bobject.TexBobject(
                '\\text{July } 27',
                location = [31, 8, 0],
                centered = True,
                scale = 4
            )
            date2.add_to_blender(appear_time = 0)

            time = tex_bobject.TexBobject(
                '10\\text{ am Central}',
                location = [31, 4, 0],
                centered = True,
                scale = 2.5
            )
            time.add_to_blender(appear_time = 0)

            date1.move_to(
                displacement = [-31, 0, 0],
                start_time = 20.5,
                end_time = 21.5
            )
            date2.move_to(
                displacement = [-31, 0, 0],
                start_time = 21.5,
                end_time = 22.5
            )
            time.move_to(
                displacement = [-31, 0, 0],
                start_time = 22.5,
                end_time = 23.5
            )
        date()

    def patreon(self):
        '''pat = svg_bobject.SVGBobject(
            'Patreon_Wordmark_Black',
        )
        pat.add_to_blender(appear_time = 0)'''

        patreon = import_object(
            'patreon_wordmark', 'svgblend',
            scale = 0.367,
            location = [-12, 5.25, 0.5],
            name = 'Patreon'
        )
        patreon.add_to_blender(appear_time = 0)

        names = [
            'Jordan Scales',
            'Kairui Wang',
            'Vladimir Duchenchuk',
            'Victor Anne',
            'Noah Healy',
            'Patrick Gorrell',
            'Josh Levent',
            'StackAbuse.com',
            'Marcial Abrahantes',
            'Feimeng Zheng',
            'Zachariah Richard Fournier'
        ]

        top_right_loc = [-12, 1.5, 0]
        x_disp = 8
        y_disp = -2.5
        tbs = []
        for i in range(len(names)):
            tb = tex_bobject.TexBobject(
                '\\text{' + names[i] + '}',
                centered = False,
                location = [
                    top_right_loc[0] + (i % 3) * x_disp,
                    top_right_loc[1] + (i // 3) * y_disp,
                    top_right_loc[2]
                ]
            )
            tb.add_to_blender(appear_time = (1 + i) / 6)
            for j in range(len(tb.lookup_table[0])):
                tb.lookup_table[0][j].color_shift(
                    color = [
                        0.952941,
                        0.94902,
                        0.941176,
                        1
                    ],
                    start_time = -1,
                    duration_time = None
                )
            tbs.append(tb)

        for i, thing in enumerate([patreon] + tbs):
            thing.disappear(disappear_time = 8 + i / 6)

        colors = [4, 3, 7, 6]
        for i in range(4):
            blob = blobject.Blobject(
                location = [4 * i, 5, 0],
                scale = 2,
                mat = 'creature_color' + str(colors[i])
            )
            blob.add_to_blender(appear_time = 1 + i / 2)
            blob.disappear(
                disappear_time = 8 + i / 4
            )

            if i == 0:
                blob.cheer(
                    start_time = i + 1,
                    end_time = i + 9
                )
            if i == 1:
                blob.nod_yes(
                    start_time = i + 1,
                    end_time = i + 3
                )

                blob.nod_yes(
                    start_time = i + 5,
                    end_time = i + 7
                )

            if i == 2:
                blob.surprise_eyes(
                    start_time = i + 1,
                    end_time = None
                )
                blob.show_mouth(
                    start_time = i + 1,
                    end_time = None
                )

            if i == 3:
                blob.dance(
                    start_time = i + 1,
                    end_time = i + 10
                )

    def thumb(self):
        #5202
        food1 = import_object(
            'goodicosphere', 'primitives',
            mat = 'color7',
            location = [1, -5, 1]
        )
        food21 = import_object(
            'half_icosphere', 'primitives',
            location = [-1, -5, -1],
            rotation_euler = [0, -math.pi / 2, 0],
            mat = 'color7'
        )
        food22 = import_object(
            'half_icosphere', 'primitives',
            location = [-1, -5, -1],
            rotation_euler = [0, math.pi / 2, 0],
            mat = 'color7'
        )
        food1.add_to_blender(appear_time = 83.5)
        food21.add_to_blender(appear_time = 83.5)
        food22.add_to_blender(appear_time = 83.5)

        dove = blobject.Blobject(
            location = [-32, -2, 0],
            rotation_euler = [0, math.pi / 2, 0],
            scale = 5,
            wiggle = True
        )
        dove.add_to_blender(appear_time = 1)
        dove.walk_to(
            new_location = [-6, -2, 0],
            start_time = 84,
            end_time = 85.5
        )

        hawk = blobject.Blobject(
            location = [32, -2, 0],
            rotation_euler = [0, -math.pi / 2, 0],
            scale = 5
        )
        hawk.add_to_blender(appear_time = 1)
        hawk.walk_to(
            new_location = [6, -2, 0],
            start_time = 84,
            end_time = 85.5
        )

        dove.hello(start_time = 85.5, end_time = 88.5)
        dove.eat_animation(start_frame = 85.5 * FRAME_RATE, end_frame = 88.5 * FRAME_RATE)

        hawk.move_head(
            rotation_quaternion = [1, 0, 0.9, -0.1],
            start_time = 85.5,
            end_time = 88.5
        )
        hawk.color_shift(
            duration_time = None,
            color = COLORS_SCALED[5],
            start_time = 86,
            shift_time = FRAME_RATE / 2,
            obj = hawk.ref_obj.children[0].children[0]
        )
        hawk.angry_eyes(
            start_time = 86,
            attack = 0.5,
            end_time = None
        )


        sot = svg_bobject.SVGBobject(
            "ShareOrTake_century",
            location = [0, 5.5, 0],
            scale = 4,
            #color = 'color2',
            centered = True
        )
        sot.add_to_blender(appear_time = 0)
        '''for i in range(3, 10):
            vom.lookup_table[0][i].color_shift(
                color = COLORS_SCALED[6],
                start_time = -1,
                duration_time = None
            )'''
