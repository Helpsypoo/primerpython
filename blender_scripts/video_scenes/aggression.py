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

CREATURE_MOVE_DURATION = 0.25
PAUSE_LENGTH = 0.125

class HawkDove(Scene):
    def __init__(self):
        self.subscenes = collections.OrderedDict([
            ('card', {'duration': 1000})
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
        self.building_from_here()

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
                    'pause_before_reset' : 3,
                    #'food_disappear' : CREATURE_MOVE_DURATION,
                }
            ],
            [
                2,
                {
                    #'day_prep' : CREATURE_MOVE_DURATION,
                    #'creatures_go_out' : CREATURE_MOVE_DURATION,
                    'pause_before_contest' : PAUSE_LENGTH,
                    #'contest' : CREATURE_MOVE_DURATION,
                    'pause_before_home' : PAUSE_LENGTH,
                    #'creatures_go_home' : CREATURE_MOVE_DURATION,
                    'pause_before_reset' : PAUSE_LENGTH,
                    #'food_disappear' : CREATURE_MOVE_DURATION,
                }
            ],
        ]

        drawn_world.add_to_blender(appear_time = 1)
        drawn_world.move_to(
            new_angle = [0, 0, 2 * math.pi],
            start_time = 0,
            end_time = 13
        )

        graph.add_to_blender(appear_time = 29)
        for i in range(len(graph.functions)):
            graph.set_shape_keys_bounded_region(index = i)

        drawn_world.animate_days(
            start_time = 2,
            first_animated_day = 0,
            #last_animated_day = 2,
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
            new_location = [0, 0, 4],
            start_time = 28.5
        )
        drawn_world.move_to(
            #new_location = [6.5, -9, 0],
            new_location = [7.5, 0, 0],
            new_scale = 6.5,
            start_time = 28.5
        )

        doves = tex_bobject.TexBobject(
            '\\text{Doves only}',
            rotation_euler = [74 * math.pi / 180, 0, 0],
            location = [7, 0, 8],
            scale = 2,
            centered = True
        )
        doves.add_to_blender(
            appear_time = 29
        )
        #doves.disappear(disappear_time = 29)

        disappear_time = 50
        to_disappear = [graph, doves, drawn_world]
        for i, thing in enumerate(to_disappear):
            thing.disappear(
                disappear_time = disappear_time - (len(to_disappear) - i - 1) * 0.05
            )

    def hawk_intro(self):
        hawk_strat = tex_bobject.TexBobject(
            '\\text{New strategy: Hawk}',
            centered = True,
            location = [0, 6, 0],
            scale = 3
        )
        hawk_strat.add_to_blender(appear_time = 1)

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
        food1.add_to_blender(appear_time = 1)
        food21.add_to_blender(appear_time = 1)
        food22.add_to_blender(appear_time = 1)

        dove = blobject.Blobject(
            location = [-19, -2, 0],
            rotation_euler = [0, math.pi / 2, 0],
            scale = 5
        )
        dove.add_to_blender(appear_time = 1)
        dove.walk_to(
            new_location = [-6, -2, 0],
            start_time = 2
        )

        hawk = blobject.Blobject(
            location = [19, -2, 0],
            rotation_euler = [0, -math.pi / 2, 0],
            scale = 5
        )
        hawk.add_to_blender(appear_time = 1)
        hawk.walk_to(
            new_location = [6, -2, 0],
            start_time = 2
        )

        dove.hello(start_time = 3, end_time = 4)
        dove.eat_animation(start_frame = 3 * FRAME_RATE, end_frame = 4 * FRAME_RATE)

        hawk.move_head(
            rotation_quaternion = [1, 0, 0.9, -0.1],
            start_time = 3,
            end_time = 5
        )
        hawk.color_shift(
            duration_time = None,
            color = COLORS_SCALED[5],
            start_time = 3.5,
            shift_time = FRAME_RATE / 2,
            obj = hawk.ref_obj.children[0].children[0]
        )
        hawk.angry_eyes(
            start_time = 3.5,
            attack = 0.5,
            end_time = None
        )

        def eats():
            drawn_contest_world.transfer_food_to_creature(
                food_bobj = food22,
                creature_bobj = hawk,
                start_time = 6,
                ground_plane = 'xz'
            )

            drawn_contest_world.animate_eating(
                food = food22,
                eater = hawk,
                start_time = 6,
                dur = 1,
                eat_rotation = [0, -30 * math.pi / 180, 0]
            )

            drawn_contest_world.transfer_food_to_creature(
                food_bobj = food21,
                creature_bobj = dove,
                start_time = 6,
                ground_plane = 'xz'
            )

            drawn_contest_world.animate_eating(
                food = food21,
                eater = dove,
                start_time = 6,
                dur = 1,
                eat_rotation = [0, 30 * math.pi / 180, 0]
            )

            drawn_contest_world.transfer_food_to_creature(
                food_bobj = food1,
                creature_bobj = hawk,
                start_time = 7,
                ground_plane = 'xz'
            )

            drawn_contest_world.animate_eating(
                food = food1,
                eater = hawk,
                start_time = 7,
                dur = 1,
                eat_rotation = [0, 30 * math.pi / 180, 0]
            )

            dove.surprise_eyes(
                start_time = 7,
                end_time = 9
            )

        eats()

        dove.move_to(
            new_angle = [0, 0, 0],
            start_time = 8.5
        )
        dove.wince(start_time = 8.5, end_time = 13)
        hawk.move_to(
            new_angle = [0, 0, 0],
            start_time = 8.5
        )
        hawk.evil_pose(start_time = 8.5, end_time = 13)

        hawk.move_to(
            new_location = [3.5, -2, 0],
            start_time = 12
        )
        rep_indicator = tex_bobject.TexBobject(
            #'\\substack{\\text{Replication} \\\\ \\text{chance} \\\\ 50\\%}',
            '\\begin{array}{@{}c@{}}\\text{Replication} \\\\ \\text{chance } 50\\% \\end{array}',
            location = [10.25, 1.5, 0],
            scale = 1.5,
            color = 'color2',
            centered = True
        )
        rep_indicator.add_to_blender(appear_time = 12)
        '''for i in range(19, 20):
            char = rep_indicator.lookup_table[0][i]
            char.color_shift(
                color = COLORS_SCALED[4],
                start_time = -1,
                duration_time = None
            )'''

        dove.move_to(
            new_location = [-3.5, -2, 0],
            start_time = 12
        )
        surv_indicator = tex_bobject.TexBobject(
            #'\\substack{\\text{Replication} \\\\ \\text{chance} \\\\ 50\\%}',
            '\\begin{array}{@{}c@{}}\\text{Survival} \\\\ \\text{chance } 50\\% \\end{array}',
            location = [-10.25, 1.5, 0],
            scale = 1.5,
            color = 'color2',
            centered = True
        )
        surv_indicator.add_to_blender(appear_time = 12)

        to_disappear = [
            dove,
            hawk,
            rep_indicator,
            surv_indicator
        ]
        for thing in to_disappear:
            thing.disappear(disappear_time = 16)



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
        food31.add_to_blender(appear_time = 17)
        food32.add_to_blender(appear_time = 17)
        food41.add_to_blender(appear_time = 17)
        food42.add_to_blender(appear_time = 17)

        hawk2 = blobject.Blobject(
            location = [-19, -2, 0],
            rotation_euler = [0, math.pi / 2, 0],
            scale = 5,
            mat = 'creature_color6'
        )
        hawk2.add_to_blender(appear_time = 17)
        hawk2.walk_to(
            new_location = [-6, -2, 0],
            start_time = 18
        )

        hawk3 = blobject.Blobject(
            location = [19, -2, 0],
            rotation_euler = [0, -math.pi / 2, 0],
            scale = 5,
            mat = 'creature_color6'
        )
        hawk3.add_to_blender(appear_time = 17)
        hawk3.walk_to(
            new_location = [6, -2, 0],
            start_time = 18
        )

        hawk2.blob_wave(
            start_time = 18,
            duration = 2
        )
        hawk2.angry_eyes(start_time = 18, end_time = 2)
        hawk3.blob_wave(
            start_time = 18,
            duration = 2
        )
        hawk3.angry_eyes(start_time = 18, end_time = 2)

        def eats2():
            drawn_contest_world.transfer_food_to_creature(
                food_bobj = food32,
                creature_bobj = hawk3,
                start_time = 20,
                ground_plane = 'xz'
            )

            drawn_contest_world.animate_eating(
                food = food32,
                eater = hawk3,
                start_time = 20,
                dur = 1,
                eat_rotation = [0, 30 * math.pi / 180, 0]
            )

            drawn_contest_world.transfer_food_to_creature(
                food_bobj = food31,
                creature_bobj = hawk2,
                start_time = 20,
                ground_plane = 'xz'
            )

            drawn_contest_world.animate_eating(
                food = food31,
                eater = hawk2,
                start_time = 20,
                dur = 1,
                eat_rotation = [0, -30 * math.pi / 180, 0]
            )

            drawn_contest_world.transfer_food_to_creature(
                food_bobj = food41,
                creature_bobj = hawk3,
                start_time = 21,
                ground_plane = 'xz'
            )

            drawn_contest_world.animate_eating(
                food = food41,
                eater = hawk3,
                start_time = 21,
                dur = 1,
                eat_rotation = [0, -30 * math.pi / 180, 0]
            )

            drawn_contest_world.transfer_food_to_creature(
                food_bobj = food42,
                creature_bobj = hawk2,
                start_time = 21,
                ground_plane = 'xz'
            )

            drawn_contest_world.animate_eating(
                food = food42,
                eater = hawk2,
                start_time = 21,
                dur = 1,
                eat_rotation = [0, 30 * math.pi / 180, 0]
            )

        eats2()

        hawk2.move_to(
            new_angle = [0, 0, 0],
            start_time = 23
        )
        #hawk2.wince(start_time = 8.5, end_time = 13)
        hawk3.move_to(
            new_angle = [0, 0, 0],
            start_time = 23
        )
        #hawk3.evil_pose(start_time = 8.5, end_time = 13)

        hawk3.move_to(
            new_location = [3.5, -2, 0],
            start_time = 26
        )
        rep_indicator2 = tex_bobject.TexBobject(
            #'\\substack{\\text{Replication} \\\\ \\text{chance} \\\\ 50\\%}',
            '\\begin{array}{@{}c@{}}\\text{Survival} \\\\ \\text{chance } 0\\% \\end{array}',
            location = [10.25, 1.5, 0],
            scale = 1.5,
            color = 'color2',
            centered = True
        )
        rep_indicator2.add_to_blender(appear_time = 26)
        '''for i in range(19, 20):
            char = rep_indicator.lookup_table[0][i]
            char.color_shift(
                color = COLORS_SCALED[4],
                start_time = -1,
                duration_time = None
            )'''

        hawk2.move_to(
            new_location = [-3.5, -2, 0],
            start_time = 26
        )
        surv_indicator2 = tex_bobject.TexBobject(
            #'\\substack{\\text{Replication} \\\\ \\text{chance} \\\\ 50\\%}',
            '\\begin{array}{@{}c@{}}\\text{Survival} \\\\ \\text{chance } 0\\% \\end{array}',
            location = [-10.25, 1.5, 0],
            scale = 1.5,
            color = 'color2',
            centered = True
        )
        surv_indicator2.add_to_blender(appear_time = 26)


        hawk2.wince(start_time = 26, end_time = 29)
        hawk3.wince(start_time = 26.25, end_time = 29.25)

        to_disappear = [
            rep_indicator2,
            surv_indicator2,
            hawk2,
            #hawk3,
            hawk_strat
        ]
        disappear_time = 40
        for i, thing in enumerate(to_disappear):
            thing.disappear(
                disappear_time = disappear_time - (len(to_disappear) - i - 1) * 0.05
            )


        hawk3.move_to(
            new_location = [5, -0.5, 0],
            start_time = 42
        )

        dove2 = blobject.Blobject(
            location = [-5, -0.5, 0],
            scale = 5
        )
        dove2.add_to_blender(appear_time = 42)

        def show_dna():
            ###########################
            #Turn Hawk clear and back
            ###########################
            meta = hawk3.ref_obj.children[0].children[0]
            #apply_material(meta, 'creature_color3')
            #blob1.add_to_blender(appear_time = 0, animate = False)

            #All these nodes are a bit overkill since I'm not fading from the
            #solid surface material
            mat_copy = meta.material_slots[0].material.copy()
            meta.active_material = mat_copy
            node_tree = mat_copy.node_tree
            out = node_tree.nodes['Material Output']
            princ = node_tree.nodes['Principled BSDF']
            trans = node_tree.nodes.new(type = 'ShaderNodeBsdfTransparent')
            mix = node_tree.nodes.new(type = 'ShaderNodeMixShader')

            scat = node_tree.nodes.new(type = 'ShaderNodeVolumeScatter')
            absorb = node_tree.nodes.new(type = 'ShaderNodeVolumeAbsorption')
            emit = node_tree.nodes.new(type = 'ShaderNodeEmission')
            add1 = node_tree.nodes.new(type = 'ShaderNodeAddShader')
            add2 = node_tree.nodes.new(type = 'ShaderNodeAddShader')

            node_tree.links.new(mix.outputs[0], out.inputs[0])
            node_tree.links.new(princ.outputs[0], mix.inputs[1])
            node_tree.links.new(trans.outputs[0], mix.inputs[2])

            node_tree.links.new(add1.outputs[0], out.inputs[1])
            node_tree.links.new(emit.outputs[0], add1.inputs[0])
            node_tree.links.new(add2.outputs[0], add1.inputs[1])
            node_tree.links.new(scat.outputs[0], add2.inputs[0])
            node_tree.links.new(absorb.outputs[0], add2.inputs[1])

            #Make another copy before adding keyframes
            mat_copy2 = mat_copy.copy()
            #mat_copy3 = mat_copy.copy()

            mix.inputs[0].default_value = 0
            for node in [scat, absorb, emit]:
                node.inputs[0].default_value = princ.inputs[0].default_value
                node.inputs[1].default_value = 0
                node.inputs[1].keyframe_insert(data_path = 'default_value', frame = 43.5 * FRAME_RATE)
                node.inputs[1].default_value = BLOB_VOLUME_DENSITY
                node.inputs[1].keyframe_insert(data_path = 'default_value', frame = 44 * FRAME_RATE)

            mix.inputs[0].keyframe_insert(data_path = 'default_value', frame = 46.5 * FRAME_RATE)
            mix.inputs[0].default_value = 1
            mix.inputs[0].keyframe_insert(data_path = 'default_value', frame = 47 * FRAME_RATE)

            mix.inputs[0].keyframe_insert(data_path = 'default_value', frame = 49.5 * FRAME_RATE)
            mix.inputs[0].default_value = 0
            mix.inputs[0].keyframe_insert(data_path = 'default_value', frame = 50 * FRAME_RATE)

            ###########################
            #Turn Dove clear and back
            ###########################
            meta2 = dove2.ref_obj.children[0].children[0]


            meta2.active_material = mat_copy2
            node_tree = mat_copy2.node_tree
            princ = node_tree.nodes['Principled BSDF']
            princ.inputs[0].default_value = COLORS_SCALED[2]
            mix2 = node_tree.nodes['Mix Shader']


            scat2 = node_tree.nodes['Volume Scatter']
            absorb2 = node_tree.nodes['Volume Absorption']
            emit2 = node_tree.nodes['Emission']

            mix2.inputs[0].default_value = 0
            for node in [scat2, absorb2, emit2]:
                node.inputs[0].default_value = princ.inputs[0].default_value
                node.inputs[1].default_value = 0
                node.inputs[1].keyframe_insert(data_path = 'default_value', frame = 43.5 * FRAME_RATE)
                node.inputs[1].default_value = BLOB_VOLUME_DENSITY
                node.inputs[1].keyframe_insert(data_path = 'default_value', frame = 44 * FRAME_RATE)

            mix2.inputs[0].keyframe_insert(data_path = 'default_value', frame = 46.5 * FRAME_RATE)
            mix2.inputs[0].default_value = 1
            mix2.inputs[0].keyframe_insert(data_path = 'default_value', frame = 47 * FRAME_RATE)

            mix2.inputs[0].keyframe_insert(data_path = 'default_value', frame = 49.5 * FRAME_RATE)
            mix2.inputs[0].default_value = 0
            mix2.inputs[0].keyframe_insert(data_path = 'default_value', frame = 50 * FRAME_RATE)

            dna_1 = import_object(
                'dna_two_strand', 'biochem',
                scale = 1.4,
                location = [-5, -1.4, 0]
            )
            dna_1.add_to_blender(appear_time = 44)
            dna_1.disappear(disappear_time = 50.5)

            def make_blue_recursive(obj):
                apply_material(obj, 'color3')
                for child in obj.children:
                    make_blue_recursive(child)

            make_blue_recursive(dna_1.ref_obj.children[0])

            dna_2 = import_object(
                'dna_two_strand', 'biochem',
                scale = 1.4,
                location = [5, -1.4, 0]
            )
            dna_2.add_to_blender(appear_time = 44)
            dna_2.disappear(disappear_time = 50.5)

            def make_red_recursive(obj):
                apply_material(obj, 'color6')
                for child in obj.children:
                    make_red_recursive(child)

            make_red_recursive(dna_2.ref_obj.children[0])

            for strand in [dna_1, dna_2]:
                '''print(strand)
                strand.tweak_colors_recursive()
                strand.move_to(
                    displacement = [0, 1.5, 0],
                    start_time = 176.5
                )'''
                strand.spin(
                    start_time = 40,
                    end_time = 60,
                    spin_rate = 0.05
                )
        show_dna()

        dove2.hello(start_time = 50, end_time = 52)

        dove2.move_to(
            start_time = 54,
            new_location = [-6, 4, 0],
            new_scale = 2.5
        )
        hawk3.move_to(
            start_time = 54.25,
            new_location = [6, 4, 0],
            new_scale = 2.5
        )

        dove3 = blobject.Blobject(
            location = [-9, -4, 0],
            scale = 2.5,
            mat = 'creature_color3'
        )
        hawk4 = blobject.Blobject(
            location = [-3, -4, 0],
            scale = 2.5,
            mat = 'creature_color6'
        )
        hawk5 = blobject.Blobject(
            location = [3, -4, 0],
            scale = 2.5,
            mat = 'creature_color6'
        )
        dove4 = blobject.Blobject(
            location = [9, -4, 0],
            scale = 2.5,
            mat = 'creature_color3'
        )

        new_cres = [dove3, hawk4, hawk5, dove4]
        for i, cre in enumerate(new_cres):
            cre.add_to_blender(
                appear_time = 56 + i / 4
            )


        '''scale = 1
        tail1 = [-7, 1.3]
        head1 = [-8.25, -1.5]
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
        )'''

        l99 = tex_bobject.TexBobject(
            '99\\%',
            location = [-9, 0.5, 0],
            scale = 1,
            centered = True
        )
        l1 = tex_bobject.TexBobject(
            '1\\%',
            location = [-3, 0.5, 0],
            scale = 1,
            centered = True
        )
        r99 = tex_bobject.TexBobject(
            '99\\%',
            location = [3, 0.5, 0],
            scale = 1,
            centered = True
        )
        r1 = tex_bobject.TexBobject(
            '1\\%',
            location = [9, 0.5, 0],
            scale = 1,
            centered = True
        )
        labels = [l99, l1, r99, r1]
        arrows = []
        scale = 1
        for i in range(4):
            mid = 6
            dir = -1
            if i > 1:
                dir = 1

            disp_dir = -1 * (-1) ** i

            tail = [mid * dir + disp_dir, 1.3]
            head = [mid * dir + disp_dir * 2.25, -1.5]

            arrow = gesture.Gesture(
                gesture_series = [
                    {
                        'type': 'arrow',
                        'points': {
                            'tail': (tail[0] / scale, tail[1] / scale, 0),
                            'head': (head[0] / scale, head[1] / scale, 0)
                        }
                    }
                ],
                scale = scale,
            )
            arrows.append(arrow)
            arrow.add_to_blender(
                appear_time = 56.125 + i / 4
            )
            labels[i].add_to_blender(
                appear_time = 56.25 + i / 4
            )

        to_disappear = [dove2, hawk3] + labels + arrows + new_cres
        disappear_time = 60
        for i, thing in enumerate(to_disappear):
            thing.disappear(
                disappear_time = disappear_time - (len(to_disappear) - i - 1) * 0.03
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
                    #'day_prep' : CREATURE_MOVE_DURATION,
                    #'creatures_go_out' : CREATURE_MOVE_DURATION,
                    #'pause_before_contest' : PAUSE_LENGTH,
                    #'contest' : CREATURE_MOVE_DURATION,
                    #'pause_before_home' : PAUSE_LENGTH,
                    #'creatures_go_home' : CREATURE_MOVE_DURATION,
                    #'pause_before_reset' : PAUSE_LENGTH,
                    'food_disappear' : CREATURE_MOVE_DURATION,
                }
            ],
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
                    'food_disappear' : CREATURE_MOVE_DURATION,
                }
            ]
        ]

        graph.add_to_blender(appear_time = 1)
        drawn_world.add_to_blender(appear_time = 1)
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


        hawks_and_doves.add_to_blender(
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
        arrow1.morph_figure(4, start_time = 110)


        '''disappear_time = 50
        to_disappear = [graph, hawks_and_doves, drawn_world]
        for i, thing in enumerate(to_disappear):
            thing.disappear(
                disappear_time = disappear_time - (len(to_disappear) - i - 1) * 0.05
            )'''

    def hypotheticals(self):
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
            num_added_days = 10
            target_num_hawks = 115
            for i in range(num_added_days):
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
                    #'day_prep' : CREATURE_MOVE_DURATION,
                    #'creatures_go_out' : CREATURE_MOVE_DURATION,
                    #'pause_before_contest' : PAUSE_LENGTH,
                    #'contest' : CREATURE_MOVE_DURATION,
                    #'pause_before_home' : PAUSE_LENGTH,
                    #'creatures_go_home' : CREATURE_MOVE_DURATION,
                    #'pause_before_reset' : PAUSE_LENGTH,
                    'food_disappear' : CREATURE_MOVE_DURATION,
                }
            ],
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
                    'food_disappear' : CREATURE_MOVE_DURATION,
                }
            ]
        ]

        graph.add_to_blender(appear_time = 1)
        drawn_world.add_to_blender(appear_time = 1)
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


        hawks_and_doves.add_to_blender(
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
        arrow1.morph_figure(4, start_time = 110)


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
                10,
                {
                    #'day_prep' : CREATURE_MOVE_DURATION,
                    #'creatures_go_out' : CREATURE_MOVE_DURATION,
                    #'pause_before_contest' : PAUSE_LENGTH,
                    #'contest' : CREATURE_MOVE_DURATION,
                    #'pause_before_home' : PAUSE_LENGTH,
                    #'creatures_go_home' : CREATURE_MOVE_DURATION,
                    #'pause_before_reset' : PAUSE_LENGTH,
                    'food_disappear' : 10,
                }
            ],
            [
                11,
                {
                    #'day_prep' : CREATURE_MOVE_DURATION,
                    #'creatures_go_out' : CREATURE_MOVE_DURATION,
                    #'pause_before_contest' : PAUSE_LENGTH,
                    #'contest' : CREATURE_MOVE_DURATION,
                    #'pause_before_home' : PAUSE_LENGTH,
                    #'creatures_go_home' : CREATURE_MOVE_DURATION,
                    #'pause_before_reset' : PAUSE_LENGTH,
                    'food_disappear' : CREATURE_MOVE_DURATION,
                }
            ]
        ]

        graph.add_to_blender(appear_time = 1)
        drawn_world.add_to_blender(appear_time = 1)
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

        hawks_and_doves.add_to_blender(
            appear_time = 1
        )
        hawks_and_doves.morph_figure(1, start_time = 31)

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
        arrow1.add_to_blender(appear_time = 22)
        '''arrow1.morph_figure(1, start_time = 102)
        arrow1.morph_figure(2, start_time = 104)
        arrow1.morph_figure(3, start_time = 106)
        arrow1.morph_figure(4, start_time = 110)'''

        sotf = tex_bobject.TexBobject(
            '\\text{Survival of the fittest}',
            '\\text{Survival of the fittest?}',
            location = [1.5, 9.5, 0]
        )
        sotf.ref_obj.parent = graph.ref_obj
        sotf.add_to_blender(appear_time = 75)
        sotf.morph_figure(1, start_time = 76)

        '''disappear_time = 50
        to_disappear = [graph, hawks_and_doves, drawn_world]
        for i, thing in enumerate(to_disappear):
            thing.disappear(
                disappear_time = disappear_time - (len(to_disappear) - i - 1) * 0.05
            )'''

    def big_sim(self):
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

        multiple = 30

        is_sim = True
        num_days = 50
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
            x_range = num_days,
            y_range = 120 * multiple * 0.8,
            width = 23,
            height = 11,
            tick_step = [num_days, 500],
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

        graph.add_to_blender(appear_time = 1)
        graph.animate_all_bounded_regions(
            start_time = 4,
            end_time = 15
        )


        #drawn_world.add_to_blender(appear_time = 1)


        '''hawks_and_doves = tex_bobject.TexBobject(
            #'\\text{Hawks and Doves}',
            '\\begin{array}{@{}c@{}}\\text{Hawks and} \\\\ \\text{Doves} \\end{array}',
            rotation_euler = [74 * math.pi / 180, 0, 0],
            location = [7, 0, 8],
            scale = 2,
            centered = True
        )'''

        '''graph.change_window(
            start_time = 3,
            end_time = 4,
            new_x_range = [0, 100],
            new_tick_step = [50, 20]
        )'''




        '''hawks_and_doves.add_to_blender(
            appear_time = 1
        )'''



        '''disappear_time = 50
        to_disappear = [graph, hawks_and_doves, drawn_world]
        for i, thing in enumerate(to_disappear):
            thing.disappear(
                disappear_time = disappear_time - (len(to_disappear) - i - 1) * 0.05
            )'''

    def payoff_grid(self):

        dd_time = 2
        dh_time = 5
        hd_time = 8
        hh_time = 11


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
            '\\dfrac{1}{2}, \\dfrac{1}{2}',
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
                0, 60, 30, 0, 60, 30
            ]
        )

        d1 = blobject.Blobject(
            mat = 'creature_color3',
            scale = 2,
            location = [-2, -2.5, 0],
            wiggle = True
        )
        d1.add_to_blender(appear_time = dd_time)
        d1.ref_obj.parent = grid.ref_obj

        h1 = blobject.Blobject(
            mat = 'creature_color6',
            scale = 2,
            location = [-2, -7.5, 0],
            wiggle = True
        )
        h1.add_to_blender(appear_time = hd_time)
        h1.ref_obj.parent = grid.ref_obj

        d2 = blobject.Blobject(
            mat = 'creature_color3',
            scale = 2,
            location = [2.35, 2.5, 0],
            wiggle = True
        )
        d2.add_to_blender(appear_time = dd_time)
        d2.ref_obj.parent = grid.ref_obj

        h2 = blobject.Blobject(
            mat = 'creature_color6',
            scale = 2,
            location = [7, 2.5, 0],
            wiggle = True
        )
        h2.add_to_blender(appear_time = dh_time)
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
            dd.lookup_table[0][0].pulse(start_time = dd_time + 1, duration_time = 1)
            d2.pulse(start_time = dd_time + 2, duration_time = 1)
            dd.lookup_table[0][2].pulse(start_time = dd_time + 2, duration_time = 1)

            #dh pulses
            d1.pulse(start_time = dh_time + 1, duration_time = 1)
            dh.lookup_table[0][0].pulse(start_time = dh_time + 1, duration_time = 1)
            dh.lookup_table[0][1].pulse(start_time = dh_time + 1, duration_time = 1)
            dh.lookup_table[0][2].pulse(start_time = dh_time + 1, duration_time = 1)
            h2.pulse(start_time = dh_time + 2, duration_time = 1)
            dh.lookup_table[0][4].pulse(start_time = dh_time + 2, duration_time = 1)
            dh.lookup_table[0][5].pulse(start_time = dh_time + 2, duration_time = 1)
            dh.lookup_table[0][6].pulse(start_time = dh_time + 2, duration_time = 1)

            #hd pulses
            h1.pulse(start_time = hd_time + 1, duration_time = 1)
            hd.lookup_table[0][0].pulse(start_time = hd_time + 1, duration_time = 1)
            hd.lookup_table[0][1].pulse(start_time = hd_time + 1, duration_time = 1)
            hd.lookup_table[0][2].pulse(start_time = hd_time + 1, duration_time = 1)
            d2.pulse(start_time = hd_time + 2, duration_time = 1)
            hd.lookup_table[0][4].pulse(start_time = hd_time + 2, duration_time = 1)
            hd.lookup_table[0][5].pulse(start_time = hd_time + 2, duration_time = 1)
            hd.lookup_table[0][6].pulse(start_time = hd_time + 2, duration_time = 1)

            #hh pulses
            h1.pulse(start_time = hh_time + 1, duration_time = 1)
            hh.lookup_table[0][0].pulse(start_time = hh_time + 1, duration_time = 1)
            h2.pulse(start_time = hh_time + 2, duration_time = 1)
            hh.lookup_table[0][2].pulse(start_time = hh_time + 2, duration_time = 1)

        pulses()

        h1.move_to(new_scale = 0, start_time = 20)
        h2.move_to(new_scale = 0, start_time = 20)

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
        go_to_mid_1(d1, 20)
        go_to_mid_2(d2, 20)
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
        me.add_to_blender(appear_time = 22)

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
        you.add_to_blender(appear_time = 22)

        #If I go hawk, you go dove
        go_to_hawk_2(d2, 25)
        go_to_hawk_1(d1, 26)
        hh.lookup_table[0][0].pulse(start_time = 26, duration_time = 1)
        go_to_dove_1(d1, 27)
        dh.lookup_table[0][0].pulse(start_time = 27, duration_time = 1)
        dh.lookup_table[0][2].pulse(start_time = 27, duration_time = 1)
        dh.lookup_table[0][3].pulse(start_time = 27, duration_time = 1)


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
        arrow_42.add_to_blender(appear_time = 27.5)

        #Reset
        go_to_mid_2(d2, 28)
        go_to_mid_1(d1, 28)

        #If I go dove, you go hawk
        go_to_dove_2(d2, 30)
        go_to_dove_1(d1, 31)
        dd.lookup_table[0][0].pulse(start_time = 31, duration_time = 1)
        go_to_hawk_1(d1, 32)
        hd.lookup_table[0][0].pulse(start_time = 32, duration_time = 1)
        hd.lookup_table[0][2].pulse(start_time = 32, duration_time = 1)
        hd.lookup_table[0][3].pulse(start_time = 32, duration_time = 1)

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
        arrow_13.add_to_blender(appear_time = 32.5)

        #Reset
        go_to_mid_2(d2, 35)
        go_to_mid_1(d1, 35)

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
        arrow_12.add_to_blender(appear_time = 36)

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
        arrow_43.add_to_blender(appear_time = 36)

        #First Nash Equilibrium
        go_to_dove_2(d2, 37)
        go_to_hawk_1(d1, 37)
        arrow_13.subbobjects[0].pulse(start_time = 37, duration_time = 1)
        arrow_43.subbobjects[0].pulse(start_time = 37, duration_time = 1)

        #Other Nash Equilibrium
        go_to_hawk_2(d2, 38)
        go_to_dove_1(d1, 38)
        arrow_12.subbobjects[0].pulse(start_time = 38, duration_time = 1)
        arrow_42.subbobjects[0].pulse(start_time = 38, duration_time = 1)

        #Reset
        go_to_dove_2(d2, 40)
        h1.move_to(new_scale = 2, start_time = 40)
        h2.move_to(new_scale = 2, start_time = 40)
        you.disappear(disappear_time = 40.5)
        me.disappear(disappear_time = 40.5)

        arrow_13.subbobjects[0].pulse(start_time = 41, duration_time = 1)
        arrow_43.subbobjects[0].pulse(start_time = 41, duration_time = 1)

        arrow_12.subbobjects[0].pulse(start_time = 42, duration_time = 1)
        arrow_42.subbobjects[0].pulse(start_time = 42, duration_time = 1)

        gt = tex_bobject.TexBobject(
            '\\text{\"Game Theory\"}',
            '\\text{\"Nash Equilibrium\"}',
            location = [-9, 6, 0],
            scale = 1.5,
            centered = True
        )
        gt.add_to_blender(appear_time = 41)
        gt.morph_figure(1, start_time = 42)
        gt.move_to(new_scale = 1.4, start_time = 42)
        gt.disappear(disappear_time = 43.5)

        grid.move_to(
            new_location = [-9.5, 3, 0],
            start_time = 43
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

            graph.add_to_blender(appear_time = 40)
            graph.move_to(
                new_location = [3, 1.5, 0],
                start_time = 43.5,
                end_time = 44.5
            )
            graph.animate_all_bounded_regions(
                start_time = 44,
                end_time = 47
            )
            graph.move_to(
                new_location = [30, 1.5, 0],
                start_time = 55,
                end_time = 56
            )
        #graph1()

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
                start_time = 43.5,
                end_time = 44.5
            )
            graph.animate_all_bounded_regions(
                start_time = 48,
                end_time = 51
            )

            graph.move_to(
                new_location = [30, -6, 0],
                start_time = 55,
                end_time = 56
            )
        #graph2()

        grid.move_to(
            new_location = [-11.5, 4.5, 0],
            new_scale = 0.6,
            start_time = 59
        )

        def equations_and_whatnot():

            eq_con_lab = tex_bobject.TexBobject(
                '\\text{Equilibrium is when:}',
                '\\text{Equilibrium:}',#' \\phanton{aah}',
                location = [4.5, 3, 0],
                scale = 1.5,
                centered = True
            )
            eq_con_lab.add_to_blender(appear_time = 60)

            eq_con = tex_bobject.TexBobject(
                '\\text{Dove score} = \\text{Hawk score}',
                '\\text{D} = \\text{H}',
                '\\text{D} < \\text{H}',
                '\\text{D} = \\text{H}',
                location = [4.5, 0.5, 0],
                centered = True,
                scale = 1.5
            )
            eq_con.add_to_blender(appear_time = 61)

            eq_con_lab.morph_figure(1, start_time = 63)
            eq_con_lab.move_to(
                new_location = [-10.7, -3.8, 0],
                new_scale = 1,
                start_time = 63
            )
            eq_con.morph_figure(1, start_time = 63)
            eq_con.move_to(
                new_location = [-9.3, -5.6, 0],
                new_scale = 2.3,
                start_time = 63
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
                appear_time = 64,
                subbobject_timing = [
                    0,
                    0, 30, 0, 30
                ]
            )
            dummy.disappear(disappear_time = 64)


            '''np_doves = tex_bobject.TexBobject(
                '90\% \\text{ Doves}',
                centered = True,
                location = [5, 5, 0],
                scale = 2
            )
            np_doves.add_to_blender(appear_time = 66)'''

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
            dove_eq.add_to_blender(appear_time = 65)

            dd_payoff_time = 67
            dh_payoff_time = 70

            dove_rhs.morph_figure(1, start_time = 66)
            dove_rhs.morph_figure(2, start_time = dd_payoff_time)
            dove_rhs.morph_figure(3, start_time = 68)
            dove_rhs.morph_figure(4, start_time = 69)
            dove_rhs.morph_figure(5, start_time = dh_payoff_time)
            dove_rhs.morph_figure(6, start_time = 71)
            dove_score.morph_figure(1, start_time = 72)

            #dove_eq.add_to_blender(appear_time = 373)
            #dove_score.morph_figure(1, start_time = 375.5)
            #rule.morph_figure(2, start_time = 377.5)
            #rule.morph_figure(3, start_time = 379)

            d_lab = eq_con.lookup_table[1][0]
            h_lab = eq_con.lookup_table[1][2]
            for i in range(2):
                d_lab.pulse(
                    start_time = i + 73,
                    duration_time = 1
                )
                h_lab.pulse(
                    start_time = i + 73.5,
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
                '\!=\\,\\, d \\cdot \\nicefrac{3}{2} + (1-d) \\cdot \\nicefrac{1}{2}',
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
                            [11, 1, 5, None],
                            [12, 1, 5, None],
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
                        [],
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
                            [11, 7, 13, None],
                            [12, 7, 13, None],
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
                        [],
                        []
                    ],
                    alignment = 'bottom',
                    gest_scale = 0.6
                )
            hawk_eq.add_to_blender(appear_time = 75)
            dove_eq.move_to(
                new_location = [4.5, 2, 0],
                start_time = 75
            )

            hd_payoff_time = 77
            hh_payoff_time = 80
            hawk_rhs.morph_figure(1, start_time = 76)
            hawk_rhs.morph_figure(2, start_time = hd_payoff_time)
            hawk_rhs.morph_figure(3, start_time = 78)
            hawk_rhs.morph_figure(4, start_time = 79)
            hawk_rhs.morph_figure(5, start_time = hh_payoff_time)
            hawk_rhs.morph_figure(6, start_time = 81)
            hawk_score.morph_figure(1, start_time = 82)

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
                        start_time = 100,
                        duration_time = None
                    )
                to_highlight = hh.lookup_table[0][0:3:2]
                for thing in to_highlight:
                    thing.pulse(start_time = hh_payoff_time, duration_time = 1, factor = 1.5)
                    thing.wobble(start_time = hh_payoff_time, end_time = hh_payoff_time + 1)
            color_equations_and_pulse()

            hawk_score.pulse(start_time = 85, duration_time = 1)
            dove_score.pulse(start_time = 86, duration_time = 1)
            eq_con.morph_figure(2, start_time = 87)
            eq_con.morph_figure(3, start_time = 88)

            dove_score.morph_figure(2, start_time = 90)
            dove_rhs.morph_figure(7, start_time = 91)
            hawk_score.morph_figure(2, start_time = 90)
            hawk_rhs.morph_figure(7, start_time = 91)

            dove_rhs.morph_figure(8, start_time = 95)
            hawk_rhs.morph_figure(8, start_time = 95)

            dove_score.morph_figure(3, start_time = 99)
            dove_rhs.morph_figure(9, start_time = 99)
            hawk_score.morph_figure(3, start_time = 99)
            hawk_rhs.morph_figure(9, start_time = 99)
            dove_eq.move_to(
                new_location = [4.5, -3.75, 0],
                start_time = 99
            )
            hawk_eq.move_to(
                new_location = [4.5, -6.25, 0],
                start_time = 99
            )

            hawk_rhs.morph_figure(10, start_time = 115)
            hawk_rhs.morph_figure(11, start_time = 117)
            hawk_rhs.morph_figure(12, start_time = 118)

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
        comparison_graph.add_to_blender(appear_time = 110)
        comparison_graph.add_new_function_and_curve(dove_score_func1, color = 3)
        comparison_graph.add_new_function_and_curve(hawk_score_func1, color = 6)
        comparison_graph.animate_all_function_curves(
            start_time = 111,
            end_time = 111.75,
            start_window = 0.25
        )
        D_lab = tex_bobject.TexBobject(
            '\\text{D}',
            location = [12.5, 3.5, 0]
        )
        D_lab.ref_obj.parent = comparison_graph.ref_obj
        D_lab.add_to_blender(appear_time = 111.25)
        H_lab = tex_bobject.TexBobject(
            '\\text{H}',
            location = [12.5, 5.3, 0]
        )
        H_lab.ref_obj.parent = comparison_graph.ref_obj
        H_lab.add_to_blender(appear_time = 111.5)

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
        eq_arrow.ref_obj.parent = comparison_graph.ref_obj
        eq_arrow.add_to_blender(appear_time = 113)

        #My handling of functions in graph bobjects is trash
        comparison_graph.functions.append(hawk_score_func2)
        comparison_graph.functions_coords.append(comparison_graph.func_to_coords(func_index = 2))
        hh.morph_figure(1, start_time = 115)
        comparison_graph.morph_curve(
            2,
            from_curve_index = 1,
            start_time = 115,
            end_time = 115.5
        )
        eq_arrow.morph_figure(1, start_time = 115)

        comparison_graph.functions.append(hawk_score_func3)
        comparison_graph.functions_coords.append(comparison_graph.func_to_coords(func_index = 3))
        hh.morph_figure(2, start_time = 117)
        comparison_graph.morph_curve(
            3,
            from_curve_index = 1,
            start_time = 117,
            end_time = 117.5
        )
        eq_arrow.morph_figure(2, start_time = 117)

        comparison_graph.functions.append(hawk_score_func4)
        comparison_graph.functions_coords.append(comparison_graph.func_to_coords(func_index = 4))
        hh.morph_figure(3, start_time = 118)
        comparison_graph.morph_curve(
            4,
            from_curve_index = 1,
            start_time = 118,
            end_time = 118.5
        )
        eq_arrow.disappear(disappear_time = 118.5)

        #hh pulses
        hh.lookup_table[1][0].pulse(start_time = 122, duration_time = 1)
        hh.lookup_table[1][1].pulse(start_time = 122, duration_time = 1)
        hh.lookup_table[1][2].pulse(start_time = 122, duration_time = 1)
        hh.lookup_table[1][4].pulse(start_time = 122, duration_time = 1)
        hh.lookup_table[1][5].pulse(start_time = 122, duration_time = 1)
        hh.lookup_table[1][6].pulse(start_time = 122, duration_time = 1)

        dh.lookup_table[0][0].pulse(start_time = 125, duration_time = 1)
        dh.lookup_table[0][1].pulse(start_time = 125, duration_time = 1)
        dh.lookup_table[0][2].pulse(start_time = 125, duration_time = 1)
        hd.lookup_table[0][4].pulse(start_time = 125, duration_time = 1)
        hd.lookup_table[0][5].pulse(start_time = 125, duration_time = 1)
        hd.lookup_table[0][6].pulse(start_time = 125, duration_time = 1)

        arrow_42.morph_figure(1, start_time = 128)
        arrow_43.morph_figure(1, start_time = 128)

        arrow_12.subbobjects[0].pulse(start_time = 130, duration_time = 0.5)
        arrow_42.subbobjects[0].pulse(start_time = 130.25, duration_time = 0.5)
        arrow_13.subbobjects[0].pulse(start_time = 130.75, duration_time = 0.5)
        arrow_43.subbobjects[0].pulse(start_time = 131, duration_time = 0.5)

        #hh pulses
        hh.lookup_table[1][0].pulse(start_time = 132, duration_time = 1)
        hh.lookup_table[1][1].pulse(start_time = 132, duration_time = 1)
        hh.lookup_table[1][2].pulse(start_time = 132, duration_time = 1)
        hh.lookup_table[1][4].pulse(start_time = 132, duration_time = 1)
        hh.lookup_table[1][5].pulse(start_time = 132, duration_time = 1)
        hh.lookup_table[1][6].pulse(start_time = 132, duration_time = 1)
        #dd pulses
        dd.lookup_table[0][0].pulse(start_time = 133, duration_time = 1)
        dd.lookup_table[0][2].pulse(start_time = 133, duration_time = 1)

    def building_from_here(self):
        building = tex_bobject.TexBobject(
            '\\text{Building from here}',
            location = [-12, 5, 0],
            scale = 1.9
        )
        building.add_to_blender(appear_time = 32)

        mixed = tex_bobject.TexBobject(
            '\\text{Creatures with more than one strategy}',
            '\\text{Mixed strategies}',
            location = [-11, 2.25, 0],
            scale = 1.4
        )
        mixed.add_to_blender(appear_time = 35.5)

        container = bobject.Bobject(
            location = [0, -4, 0]
        )
        container.add_to_blender(appear_time = 0)

        zero_blob = blobject.Blobject(
            location = [-4, 0, 0],
            scale = 4,
            mat = 'creature_color3'
        )
        zero_blob.ref_obj.parent = container.ref_obj
        zero_blob.add_to_blender(appear_time = 36)
        one_blob = blobject.Blobject(
            location = [4, 0, 0],
            scale = 4,
            mat = 'creature_color6'
        )
        one_blob.ref_obj.parent = container.ref_obj
        one_blob.add_to_blender(appear_time = 37)

        zero_blob.move_to(
            new_location = [-10, 0, 0],
            new_scale = 2,
            start_time = 38
        )
        one_blob.move_to(
            new_location = [10, 0, 0],
            new_scale = 2,
            start_time = 38
        )

        for i in range(1, 4):
            bleb = blobject.Blobject(
                location = [(i - 2) * 5, 0, 0],
                scale = 2,
            )
            bleb.color_shift(
                color = mix_colors_hsv(COLORS_SCALED[2], COLORS_SCALED[5], i / 10),
                start_time = 0,
                duration_time = None,
                obj = bleb.ref_obj.children[0].children[0]
            )
            bleb.add_to_blender(appear_time = 38)
            bleb.ref_obj.parent = container.ref_obj


        mixed.morph_figure(1, start_time = 46.5)


        conditional = tex_bobject.TexBobject(
            '\\text{Conditional strategies}',
            location = [-11, -0.25, 0],
            scale = 1.4
        )
        conditional.add_to_blender(appear_time = 57.5)

        asymmetric = tex_bobject.TexBobject(
            '\\text{Asymmetric contests}',
            location = [-11, -2.75, 0],
            scale = 1.4
        )
        asymmetric.add_to_blender(appear_time = 61)

        pd = tex_bobject.TexBobject(
            '\\text{Prisoner\'s dilemma}',
            location = [-11, -5.25, 0],
            scale = 1.4
        )
        pd.add_to_blender(appear_time = 77)

        to_disappear = [
            building,
            mixed,
            conditional,
            asymmetric,
            pd
        ]
        for i, thing in enumerate(to_disappear):
            thing.disappear(disappear_time = 58.5 - (len(to_disappear) - 1 - i) * 0.05)
