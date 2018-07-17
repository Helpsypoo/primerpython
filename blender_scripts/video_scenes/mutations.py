import collections
import math

import imp
import scene
imp.reload(scene)
from scene import Scene

import svg_bobject
imp.reload(svg_bobject)
import tex_bobject
imp.reload(tex_bobject)
import creature
imp.reload(creature)
import drawn_world
imp.reload(drawn_world)
import population
imp.reload(population)
import gesture
imp.reload(gesture)
import graph_bobject
imp.reload(graph_bobject)
import tex_complex
imp.reload(tex_complex)

import helpers
imp.reload(helpers)
from helpers import *

"""Is there smoother way to organize scene structure and timing?
- Objects that are defined and persist from one scene to the next, eliminating
the need to copy parameters or positions from one scene to the next. This would
also make it easier to make shorter scenes, which would render faster, since
they have fewer objects on overage.
- This would mean bobjects are defined outside of the scene. The scene would just
manipulate them and add keyframes.

Object types and thoughts:
- svg/tex. Scripts might take a while to run if a long chain of morphs needs to
be prepared. Probably just eat this cost for now and maybe alter add_to_blender
later on to only use a subset of the figures/expressions if it seems worthwhile.
Hmm. Except initializing one of these objects does interact with blender.
For now...?
- Generic bobjects. Might need to keep track of position and other parameters
more carefully on the python side, since I can't depend on blender when using
this workflow.
- DrawnWorld. The sims can be saved, so this should be fine. I don't think I'll
ever want to split a sim over several scenes, though."""


class MutationScene(object):
    #Intro scene objects
        graph_kwargs = {
            'x_range' : [0, 10],
            'y_range' : [-1, 2],
            'tick_step' : [5, 1],
            'width' : 10,
            'height' : 10,
            'x_label' : 'N',
            'x_label_pos' : 'end',
            'y_label' : '\\Delta',
            'y_label_pos' : 'end',
            'location' : (-10, -3, 0),
            'scale' : 0.6,
            'centered' : True,
            'arrows' : True,
        }
        graph2_kwargs = {
            'x_range' : [0, 20],
            'y_range' : [0, 30],
            'tick_step' : [5, 10],
            'width' : 10,
            'height' : 10,
            'x_label' : 't',
            'x_label_pos' : 'end',
            'y_label' : 'N',
            'y_label_pos' : 'end',
            'location' : (9, -3, 0), #(6.5, -2.5, 0),
            'centered' : True,
            'arrows' : True,
            'scale' : 0.6,
            'high_res_curve_indices' : [0, 1, 2]
        }

        frames_per_time_step = 21
        start_delay = 1
        sim_duration = 20

        initial_creature_count = 2
        initial_creatures = []
        for i in range(initial_creature_count):
            new_creature = creature.Creature()
            initial_creatures.append(new_creature)
        sim_kwargs = {
            'name' : 'blob1_sim',
            'location' : [0, -3, 0],
            'scale' : 0.4,
            'start_delay' : start_delay - 0.2, #To compensate for cute add timing
            'frames_per_time_step' : frames_per_time_step,
            'load' : 'ro_not_extinction',
            'sim_duration' : sim_duration,
            'initial_creatures' : initial_creatures,
            #'gene_updates' : [
            #    ['color', 'creature_color_1', 'birth_modifier', 0, 0],
            #    ['shape', 'shape1', 'birth_modifier', 0, 0],
            #    ['size', '1', 'birth_modifier', 0, 0],
            #    ['color', 'creature_color_1', 'mutation_chance', 0, 0],
            #    ['shape', 'shape1', 'mutation_chance', 0, 0],
            #    ['size', '1', 'mutation_chance', 0, 0],
            #    ['color', 'creature_color_1', 'death_modifier', 200, 0],
            #    ['color', 'creature_color_1', 'replication_modifier', 300, 0],
            #],
            #'pauses' : [
            #    [0, 1]
            #]
        }
        sim2_kwargs = {
            'name' : 'blob1_sim',
            'location' : [0, -3, 0],
            'scale' : 0.4,
            'start_delay' : start_delay,
            'frames_per_time_step' : frames_per_time_step,
            'sim_duration' : sim_duration,
            'initial_creatures' : None,
            'gene_updates' : [
                ['color', 'creature_color_1', 'birth_modifier', 0, 0],
                ['shape', 'shape1', 'birth_modifier', 0, 0],
                ['size', '1', 'birth_modifier', 0, 0],
                ['color', 'creature_color_1', 'mutation_chance', 0, 0],
                ['shape', 'shape1', 'mutation_chance', 0, 0],
                ['size', '1', 'mutation_chance', 0, 0],
                ['color', 'creature_color_1', 'death_modifier', 0, 0],
                ['color', 'creature_color_1', 'replication_modifier', 0, 0],
            ]
        }
        b_birth_chance_args = [
            'B = 100\%',
        ]
        b_death_chance_args = [
            'D = 10\%',
        ]
        b_rep_chance_args = [
            'R = 5\%',
        ]
        b_mut_chance_args = [
            'M = 10\%',
        ]

        g_birth_chance_args = [
            'B = 0\%',
        ]
        g_death_chance_args = [
            'D = 10\%',
        ]
        g_rep_chance_args = [
            'R = 5\%',
        ]

        #labeled args
        b_birth_chance_args_lab = [
            'B_1 = 100\%',
        ]
        b_death_chance_args_lab = [
            'D_1 = 10\%',
        ]
        b_rep_chance_args_lab = [
            'R_1 = 5\%',
        ]
        b_mut_chance_args_lab = [
            'M_1 = 10\%',
            'M_{12} = 10\%',
        ]
        b_mut_chance_args2_lab = [
            'M_1 = 10\%',
            'M_{13} = 10\%',
        ]

        g_birth_chance_args_lab = [
            'B_2 = 0\%',
        ]
        g_death_chance_args_lab = [
            'D_2 = 10\%',
        ]
        g_rep_chance_args_lab = [
            'R_2 = 5\%',
        ]

        r_birth_chance_args_lab = [
            'B_3 = 0\%',
        ]
        r_death_chance_args_lab = [
            'D_3 = 5\%',
        ]
        r_rep_chance_args_lab = [
            'R_3 = 5\%',
        ]
        r_mut_chance_args_lab = [
            'M_{34} = 5\%',
        ]

        y_birth_chance_args_lab = [
            'B_4 = 0\%',
        ]
        y_death_chance_args_lab = [
            'D_4 = 5\%',
        ]
        y_rep_chance_args_lab = [
            'R_4 = 10\%',
        ]

        start_delay = 0.5
        frames_per_time_step = 15
        sim_duration = 120
        first_mutation_sim_kwargs = {
            'name' : 'mutation_sim',
            'location' : [6, 0, 0],
            'scale' : 0.75,
            'start_delay' : start_delay,
            'frames_per_time_step' : frames_per_time_step,
            'sim_duration' : sim_duration,
            'initial_creatures' : None,
            'save' : True,
            'gene_updates' : [
                #Other alleles
                ['shape', 'shape1', 'birth_modifier', 1, 0],
                ['size', '1', 'birth_modifier', 1, 0],
                ['shape', 'shape1', 'mutation_chance', 0, 0],
                ['size', '1', 'mutation_chance', 0, 0],
                #Color 1
                ['color', 'creature_color_1', 'birth_modifier', 1000, 0],
                ['color', 'creature_color_1', 'death_modifier', 100, 0],
                ['color', 'creature_color_1', 'replication_modifier', 50, 0],
                ['color', 'creature_color_1', 'mutation_chance', [0, 0.1, 0, 0], 0],
                #Color 2
                ['color', 'creature_color_2', 'death_modifier', 100, 0],
                ['color', 'creature_color_2', 'replication_modifier', 50, 0],
                ['color', 'creature_color_2', 'mutation_chance', 0, 0],
            ]
        }
        second_mutation_sim_kwargs = {
            'name' : 'mutation_sim',
            'location' : [-8, -2.5, 0],
            'scale' : 0.5,
            'start_delay' : start_delay,
            'frames_per_time_step' : frames_per_time_step,
            'sim_duration' : sim_duration,
            'initial_creatures' : None,
            #'save' : True,
            'load' : 'mut_reasonable_yellow',
            'gene_updates' : [
                #Other alleles
                ['shape', 'shape1', 'birth_modifier', 1, 0],
                ['size', '1', 'birth_modifier', 1, 0],
                ['shape', 'shape1', 'mutation_chance', 0, 0],
                ['size', '1', 'mutation_chance', 0, 0],
                #Color 1
                ['color', 'creature_color_1', 'birth_modifier', 1000, 0],
                ['color', 'creature_color_1', 'death_modifier', 100, 0],
                ['color', 'creature_color_1', 'replication_modifier', 50, 0],
                ['color', 'creature_color_1', 'mutation_chance', [0, 0.1, 0.1, 0], 0],
                #Color 2
                ['color', 'creature_color_2', 'death_modifier', 100, 0],
                ['color', 'creature_color_2', 'replication_modifier', 50, 0],
                ['color', 'creature_color_2', 'mutation_chance', 0, 0],
                #Color 3
                ['color', 'creature_color_3', 'death_modifier', 50, 0],
                ['color', 'creature_color_3', 'replication_modifier', 50, 0],
                ['color', 'creature_color_3', 'mutation_chance', [0, 0, 0, 0.1], 0],
                #Color 4
                ['color', 'creature_color_4', 'death_modifier', 50, 0],
                ['color', 'creature_color_4', 'replication_modifier', 100, 0],
                ['color', 'creature_color_4', 'mutation_chance', 0, 0],
            ]
        }
        second_mutation_sim_graph_kwargs = {
            'x_range' : [0, sim_duration],
            'y_range' : [0, 50],
            'tick_step' : [50, 10],
            'width' : 12,
            'height' : 9,
            'x_label' : 't',
            'x_label_pos' : 'end',
            'y_label' : 'N',
            'y_label_pos' : 'along',
            'location' : (6, -2.5, 0),
            'centered' : True,
            'arrows' : 'positive',
            'high_res_curve_indices' : [0, 1, 2, 3]
        }
        second_mutation_sim_graph_end_kwargs = {
            'x_range' : [0, sim_duration],
            'y_range' : [0, 50],
            'tick_step' : [50, 10],
            'width' : 15,
            'height' : 10,
            'x_label' : 't',
            'x_label_pos' : 'end',
            'y_label' : 'N',
            'y_label_pos' : 'end',
            'location' : (-4, -1, 0),
            'centered' : True,
            'arrows' : 'positive',
            'high_res_curve_indices' : [0, 1, 2, 3]
        }

'''
class LastVideoExp(Scene, MutationScene):
    def __init__(self):
        self.subscenes = collections.OrderedDict([
            ('sim', {'duration': 9}),
        ])
        super().__init__()

    def play(self):
        super().play()
        cues = self.subscenes
        scene_end = self.duration

        def func(x):
            return 1 + 0.1 * x

        def func2(x):
            return 0.1 * x

        blob = import_object(
            'boerd_blob', 'creatures',
            location = [-7.5, 5, 0],
            scale = 2.7,
            wiggle = True,
            cycle_length = scene_end * FRAME_RATE
        )
        apply_material(blob.ref_obj.children[0].children[0], 'creature_color3')
        blob.add_to_blender(appear_time = cues['sim']['start'] + 1)

        rhs = tex_bobject.TexBobject(
            "B + \\big(R-D\\big) \\times N",
            centered = True
        )
        equals = tex_bobject.TexBobject(
            "\!=",
            centered = True
        )
        lhs = tex_bobject.TexBobject(
            "\\Delta",
            centered = True
        )
        equation = tex_complex.TexComplex(
            lhs, equals, rhs,
            location = (2.5, 5, 0),
            scale = 1.2,
            centered = True
        )
        equation.add_to_blender(appear_time = cues['sim']['start'] + 1)

        graph = graph_bobject.GraphBobject(
            func2,
            **MutationScene.graph_kwargs
        )
        graph.add_to_blender(appear_time = cues['sim']['start'] + 1.1)

        appear_coord = [5, 0.5, 0]

        def exp_func(x): return 2 * math.exp(0.1 * x)
        #def exp_func(x): return 15 * math.exp(0.1 * x) - 10
        graph2 = graph_bobject.GraphBobject(
            exp_func,
            **MutationScene.graph2_kwargs
        )

        frames_per_time_step = 15
        start_delay = 1
        sim_duration = 20

        initial_creature_count = 2
        initial_creatures = []
        for i in range(initial_creature_count):
            new_creature = creature.Creature()
            initial_creatures.append(new_creature)
        sim = drawn_world.DrawnWorld(
            **MutationScene.sim_kwargs
        )

        graph2.add_to_blender(appear_time = cues['sim']['start'] + 1.3)

        sim.add_to_blender(appear_time = cues['sim']['start'] + 1.2)



        #Animate sim data and points
        data = sim.get_creature_count_by_t()
        print(data)
        graph2.add_new_function_and_curve(
            data,
            #curve_mat_modifier = 'fade',
            z_shift = -0.05,
        )
        graph2.animate_function_curve(
            start_time = cues['sim']['start'] + 2,
            end_time = cues['sim']['start'] + 7,
            uniform_along_x = True,
            index = 1
        )
        #nt graph highlight point
        appear_coord2 = [0, data[0], 0]
        point2 = graph2.add_point_at_coord(
            coord = appear_coord2,
            appear_time = cues['sim']['start'] + 2,
            axis_projections = True,
            track_curve = 1
        )
        graph2.animate_point(
            end_coord = [20, 0, 0],
            start_time = cues['sim']['start'] + 2,
            end_time = cues['sim']['start'] + 7,
            point = point2
        )
        #delta graph highlight point
        appear_coord21 = [data[0], func2(data[0]), 0]
        point21 = graph.add_point_at_coord(
            coord = appear_coord21,
            appear_time = cues['sim']['start'] + 2,
            axis_projections = True,
            track_curve = 0
        )
        graph.multi_animate_point(
            start_time = cues['sim']['start'] + 2,
            #end_time = cues['sim']['start'] + 480,
            point = point21,
            frames_per_time_step = frames_per_time_step,
            x_of_t = data, #Not func2. This uses the sim data to inform movements
        )

        #point 21 shoots off and an arrow appears
        point21.disappear(disappear_time = cues['sim']['start'] + 5)
        point21.axis_projections[0].disappear(disappear_time = cues['sim']['start'] + 5)
        point21.axis_projections[1].disappear(disappear_time = cues['sim']['start'] + 5)
        zoom_arrow = gesture.Gesture(
            gesture_series = [
                {
                    'type' : 'arrow',
                    'points' : {
                        'head' : [-6, -5/6 - 0.5, 0],
                        'tail' : [-8, -2, 0],
                    }
                }
            ],
            color = 'color2'
        )
        zoom_arrow.add_to_blender(appear_time = cues['sim']['start'] + 4.5)

        #point 2 disappears after
        #point2.disappear(disappear_time = cues['sim']['start'] + 8.5)
        #point2.axis_projections[0].disappear(disappear_time = cues['sim']['start'] + 8.5)
        #point2.axis_projections[1].disappear(disappear_time = cues['sim']['start'] + 8.5)
        #zoom_arrow.disappear(disappear_time = cues['sim']['start'] + 8.5)

        #Prep for next scene
        to_disappear = [blob, equation, zoom_arrow, graph, sim, graph2]
        for i, thing in enumerate(to_disappear):
            thing.disappear(disappear_time = cues['sim']['end'] - (len(to_disappear) - 1 - i) * 0.05)
'''
'''
class LastVideoChicken(Scene, MutationScene):
    def __init__(self):
        self.subscenes = collections.OrderedDict([
            ('form', {'duration': 4}),
            ('sim', {'duration': 8}),
        ])
        super().__init__()

    def play(self):
        super().play()
        cues = self.subscenes
        scene_end = self.duration

        chik = import_object('chicken', 'creatures', scale = 4)
        tele = import_object('teleporter', 'primitives', scale = 10)
        tele.ref_obj.rotation_euler = (math.pi / 2, 0, 0)
        form_chik = bobject.MeshMorphBobject(name = 'form_chik')
        form_chik.add_subbobject_to_series(tele)
        form_chik.add_subbobject_to_series(chik)

        form_chik.add_to_blender(
            appear_frame = cues['form']['start'],
            animate = False
        )

        form_chik.morph_bobject(
            0, 1, cues['form']['start'], cues['form']['end'] - 1,
            dissolve_time = 120
        )

        #Spiiiiiiiin
        form_chik.ref_obj.rotation_euler = (0, 0, 0)
        form_chik.ref_obj.keyframe_insert(data_path="rotation_euler", frame = 0)
        form_chik.ref_obj.rotation_euler = (0, 8 * math.pi, 0)
        form_chik.ref_obj.keyframe_insert(
            data_path="rotation_euler",
            frame = cues['form']['end'] - 1
        )


        form_chik.move_to(
            new_location = [0, 4.5, 0],
            new_scale = 2.7 / 4,
            start_time = cues['sim']['start']
        )

        def func2(x):
            return 0.1 * x


        graph = graph_bobject.GraphBobject(
            func2,
            **MutationScene.graph_kwargs
        )
        graph.add_to_blender(appear_time = cues['sim']['start'])

        #appear_coord = [5, 0.5, 0]


        #Transition to N-t graph
        def exp_func(x): return 2 * math.exp(0.1 * x)
        #def exp_func(x): return 15 * math.exp(0.1 * x) - 10
        graph2 = graph_bobject.GraphBobject(
            exp_func,
            **MutationScene.graph2_kwargs
        )

        sim = drawn_world.DrawnWorld(
            **MutationScene.sim2_kwargs
        )

        graph2.add_to_blender(appear_time = cues['sim']['start'])

        sim.add_to_blender(appear_time = cues['sim']['start'])



        #Animate sim data and points
        data = sim.get_creature_count_by_t()
        print(data)
        graph2.add_new_function_and_curve(
            data,
            curve_mat_modifier = 'fade',
            z_shift = -0.05,
        )
        graph2.animate_function_curve(
            start_time = cues['sim']['start'] + 2,
            end_time = cues['sim']['start'] + 7,
            uniform_along_x = True,
            index = 1
        )
        #nt graph highlight point
        appear_coord2 = [0, data[0], 0]
        point2 = graph2.add_point_at_coord(
            coord = appear_coord2,
            appear_time = cues['sim']['start'] + 1.5,
            axis_projections = True,
            track_curve = 1
        )
        graph2.animate_point(
            end_coord = [20, 0, 0],
            start_time = cues['sim']['start'] + 2,
            end_time = cues['sim']['start'] + 7,
            point = point2
        )
        #delta graph highlight point
        appear_coord21 = [data[0], func2(data[0]), 0]
        point21 = graph.add_point_at_coord(
            coord = appear_coord21,
            appear_time = cues['sim']['start'] + 1.5,
            axis_projections = True,
            track_curve = 0
        )
        graph.multi_animate_point(
            start_time = cues['sim']['start'] + 2,
            #end_time = cues['sim']['start'] + 480,
            point = point21,
            frames_per_time_step = sim.frames_per_time_step,
            x_of_t = data, #Not func2. This uses the sim data to inform movements
        )

        #Prep for next scene
        to_disappear = [form_chik, graph, sim, graph2]
        for i, thing in enumerate(to_disappear):
            thing.disappear(disappear_time = cues['sim']['end'] - (len(to_disappear) - 1 - i) * 0.05)
'''
'''
class Logo(Scene):
    def __init__(self):

        self.subscenes = collections.OrderedDict([
            ('logo', {'duration': 2})
        ])
        super().__init__()

    def play(self):
        super().play()
        cues = self.subscenes
        scene_end = self.duration

        logo = svg_bobject.SVGBobject(
            "Layer",
            #file_name = "PrimerLogoWhite",
            location = (-7.45, 1.5, 0),
            scale = 2
        )
        for bobj in logo.rendered_curve_bobjects:
            apply_material(bobj.ref_obj.children[0], 'color2')
        stroke = logo.rendered_curve_bobjects[0]
        apply_material(stroke.ref_obj.children[0], 'color3')
        logo.morph_chains[0][0].ref_obj.location[2] = -1
        logo.add_to_blender(
            appear_time = cues['logo']['start'],
            #subbobject_timing = [90, 30, 40, 50, 60, 70, 80],
            subbobject_timing = [42, 30, 33, 36, 39, 42, 45],
            animate = True
        )
        logo.disappear(disappear_time = scene_end)
'''
'''
class BlueGreenCards(Scene):
    def __init__(self):

        self.subscenes = collections.OrderedDict([
            ('blue', {'duration': 26}),
            ('blue_stats', {'duration': 12}),
            ('green_stats', {'duration': 63}),
            #('sim', {'duration': 12}),
        ])
        super().__init__()

    def play(self):
        super().play()
        cues = self.subscenes
        scene_end = self.duration
        print('Scene end is ' + str(scene_end))

        b_blob = import_object(
            'boerd_blob', 'creatures',
            location = [0, 0, 0],
            scale = 4,
            wiggle = True,
            cycle_length = scene_end * FRAME_RATE
        )
        b_blob.ref_obj.children[0].children[0].data.resolution = 0.2
        apply_material(b_blob.ref_obj.children[0].children[0], 'creature_color3')
        b_blob.add_to_blender(appear_time = cues['blue']['start'] + 1)

        b_blob2 = import_object(
            'boerd_blob', 'creatures',
            location = [0, 0, 0],
            scale = 4,
            wiggle = True
        )
        b_blob2.ref_obj.children[0].children[0].data.resolution = 0.2
        apply_material(b_blob2.ref_obj.children[0].children[0], 'creature_color3')
        b_blob2.add_to_blender(appear_time = cues['blue']['start'] + 3.5)

        b_blob.move_to(
            new_location = [-8, 0, 0],
            start_time = cues['blue']['start'] + 3.5
        )
        b_blob2.move_to(
            new_location = [8, 0, 0],
            start_time = cues['blue']['start'] + 3.5
        )

        arrow = gesture.Gesture(
            gesture_series = [
                {
                    'type': 'arrow',
                    'points': {
                        'tail': (-1.5, 0, 0),
                        'head': (1.5, 0, 0)
                    }
                },
            ],
            scale = 2,
            color = 'color2'
        )
        arrow.add_to_blender(appear_time = cues['blue']['start'] + 3.5)


        #Second blue blob disappears to make way for the green blob
        arrow.disappear(disappear_time = cues['blue']['start'] + 7.5)
        b_blob2.disappear(disappear_time = cues['blue']['start'] + 7.5)
        b_blob.move_to(
            new_location = [0, 0, 0],
            start_time = cues['blue']['start'] + 7
        )

        #Green blob appears
        g_blob = import_object(
            'boerd_blob', 'creatures',
            location = [0, 0, 0],
            scale = 4,
            wiggle = True,
            cycle_length = scene_end * FRAME_RATE
        )
        g_blob.ref_obj.children[0].children[0].data.resolution = 0.2
        apply_material(g_blob.ref_obj.children[0].children[0], 'creature_color7')
        g_blob.add_to_blender(appear_time = cues['blue']['start'] + 12)

        b_blob.move_to(
            new_location = [-8, 0, 0],
            start_time = cues['blue']['start'] + 12
        )
        g_blob.move_to(
            new_location = [8, 0, 0],
            start_time = cues['blue']['start'] + 12
        )
        arrow.add_to_blender(appear_time = cues['blue']['start'] + 12 + 1/60)

        mutations = tex_bobject.TexBobject(
            '\\text{"Mutation"} \\phantom{shmehhh}', #Shmeh to differentiate
                                                     #from other tex file with
                                                     #no quotes
            scale = 1.5,
            location = [0, 3, 0],
            centered = True
        )
        mutations.add_to_blender(appear_time = cues['blue']['start'] + 15)
        mutations.disappear(disappear_time = cues['blue']['end'])

        #blue stats
        b_blob.move_to(
            new_location = [-11, 0, 0],
            new_scale = 2.5,
            start_time = cues['blue_stats']['start']
        )
        b_birth_chance = tex_bobject.TexBobject(
            *MutationScene.b_birth_chance_args,
            #**MutationScene.b_birth_chance_kwargs,
        )
        b_death_chance = tex_bobject.TexBobject(
            *MutationScene.b_death_chance_args,
            scale = 1,
        )
        b_rep_chance = tex_bobject.TexBobject(
            *MutationScene.b_rep_chance_args,
        )
        b_stats = tex_complex.TexComplex(
            b_birth_chance, b_death_chance, b_rep_chance,
            multiline = True,
            line_height = 1.4,
            location = [2 / b_blob.ref_obj.scale[0], 0, 0],
            scale = 1 / b_blob.ref_obj.scale[0]
        )
        b_stats.ref_obj.parent = b_blob.ref_obj
        b_stats.add_to_blender(
            appear_time = cues['blue_stats']['start'],
            subbobject_timing = [0, 390, 480],
        )


        #green stats
        g_blob.move_to(
            new_location = [5, 0, 0],
            new_scale = 2.5,
            start_time = cues['green_stats']['start']
        )
        arrow.move_to(
            new_scale = 1.6,
            start_time = cues['green_stats']['start'],
        )

        cam_bobj = bobject.Bobject(location = CAMERA_LOCATION)
        cam_bobj.add_to_blender(appear_time = 0)
        cam_obj = bpy.data.objects['Camera']
        cam_obj.location = [0, 0, 0]
        cam_obj.parent = cam_bobj.ref_obj

        cam_bobj.move_to(
            new_location = [5, 1.2, 3],
            start_time = cues['green_stats']['start'] + 5,
            end_time = cues['green_stats']['start'] + 23.5
        )
        cam_bobj.move_to(
            new_location = CAMERA_LOCATION,
            start_time = cues['green_stats']['start'] + 27,
            end_time = cues['green_stats']['start'] + 28
        )

        g_birth_chance = tex_bobject.TexBobject(
            *MutationScene.g_birth_chance_args,
            #**MutationScene.b_birth_chance_kwargs,
        )
        g_death_chance = tex_bobject.TexBobject(
            *MutationScene.g_death_chance_args,
            scale = 1,
        )
        g_rep_chance = tex_bobject.TexBobject(
            *MutationScene.g_rep_chance_args,
        )
        g_stats = tex_complex.TexComplex(
            g_birth_chance, g_death_chance, g_rep_chance,
            multiline = True,
            line_height = 1.4,
            location = [2 / g_blob.ref_obj.scale[0], 0, 0],
            scale = 1 / g_blob.ref_obj.scale[0]
        )
        g_stats.ref_obj.parent = g_blob.ref_obj
        g_stats.add_to_blender(
            appear_time = cues['green_stats']['start'] + 36,
            subbobject_timing = [180, 0, 30],
        )

        b_mut_chance = tex_bobject.TexBobject(
            *MutationScene.b_mut_chance_args,
        )
        b_stats.add_tex_bobject(b_mut_chance)
        b_mut_chance.add_to_blender(
            appear_time = cues['green_stats']['start'] + 54.5
        )
        b_stats.arrange_tex_bobjects(
            start_time = cues['green_stats']['start'] + 54.5
        )

        #Prep for sim
        b_blob.move_to(
            displacement = [0, 3.5, 0],
            start_time = cues['green_stats']['end'] - 0.5
        )
        g_blob.move_to(
            displacement = [-16, -3.5, 0],
            start_time = cues['green_stats']['end'] - 0.5
        )
        arrow.disappear(disappear_time = cues['green_stats']['end'])
'''
#'''
class FirstMutationSim(Scene):
    def __init__(self):
        self.subscenes = collections.OrderedDict([
            ('sim', {'duration': 29}),
        ])
        super().__init__()

    def play(self):
        super().play()
        cues = self.subscenes
        scene_end = self.duration

        b_blob = import_object(
            'boerd_blob', 'creatures',
            location = [-11, 3.5, 0],
            scale = 2.5,
            wiggle = True,
            cycle_length = scene_end * FRAME_RATE
        )
        b_blob.ref_obj.children[0].children[0].data.resolution = 0.2
        apply_material(b_blob.ref_obj.children[0].children[0], 'creature_color3')
        b_blob.add_to_blender(
            appear_frame = cues['sim']['start'],
            animate = False
        )
        b_birth_chance = tex_bobject.TexBobject(
            *MutationScene.b_birth_chance_args,
        )
        b_death_chance = tex_bobject.TexBobject(
            *MutationScene.b_death_chance_args,
        )
        b_rep_chance = tex_bobject.TexBobject(
            *MutationScene.b_rep_chance_args,
        )
        b_mut_chance = tex_bobject.TexBobject(
            *MutationScene.b_mut_chance_args,
        )
        b_stats = tex_complex.TexComplex(
            b_birth_chance, b_death_chance, b_rep_chance, b_mut_chance,
            multiline = True,
            line_height = 1.4,
            location = [2 / b_blob.ref_obj.scale[0], 0, 0],
            scale = 1 / b_blob.ref_obj.scale[0]
        )
        b_stats.ref_obj.parent = b_blob.ref_obj
        b_stats.add_to_blender(
            appear_time = cues['sim']['start'] - 0.5,
            animate = False
        )

        g_blob = import_object(
            'boerd_blob', 'creatures',
            location = [-11, -3.5, 0],
            scale = 2.5,
            wiggle = True,
            cycle_length = scene_end * FRAME_RATE
        )
        g_blob.ref_obj.children[0].children[0].data.resolution = 0.2
        apply_material(g_blob.ref_obj.children[0].children[0], 'creature_color7')
        g_blob.add_to_blender(
            appear_frame = cues['sim']['start'],
            animate = False
        )
        g_birth_chance = tex_bobject.TexBobject(
            *MutationScene.g_birth_chance_args,
        )
        g_death_chance = tex_bobject.TexBobject(
            *MutationScene.g_death_chance_args,
        )
        g_rep_chance = tex_bobject.TexBobject(
            *MutationScene.g_rep_chance_args,
        )
        g_stats = tex_complex.TexComplex(
            g_birth_chance, g_death_chance, g_rep_chance,
            multiline = True,
            line_height = 1.4,
            location = [2 / g_blob.ref_obj.scale[0], 0, 0],
            scale = 1 / g_blob.ref_obj.scale[0]
        )
        g_stats.ref_obj.parent = g_blob.ref_obj
        g_stats.add_to_blender(
            appear_time = cues['sim']['start'] - 0.5,
            animate = False
        )

        sim = drawn_world.DrawnWorld(
            **MutationScene.first_mutation_sim_kwargs
        )
        sim.add_to_blender(
            appear_time = cues['sim']['start']
        )

        b_blob.move_to(
            new_location = [-11, 0, 0],
            start_time = scene_end - 0.5,
            new_scale = 2.5
        )

        to_disappear = [b_stats, g_blob, g_stats, sim]
        for thing in to_disappear:
            thing.disappear(disappear_time = cues['sim']['end'])
#'''
'''
class BlueEquation(Scene):
    def __init__(self):
        self.subscenes = collections.OrderedDict([
            ('blue', {'duration': 18}),
        ])
        super().__init__()

    def play(self):
        super().play()
        cues = self.subscenes
        scene_end = self.duration

        b_blob_start_location = [-11, 0, 0]
        b_blob = import_object(
            'boerd_blob', 'creatures',
            location = b_blob_start_location,
            scale = 2.5,
            wiggle = True,
            cycle_length = scene_end * FRAME_RATE
        )
        b_blob.ref_obj.children[0].children[0].data.resolution = 0.2
        apply_material(b_blob.ref_obj.children[0].children[0], 'creature_color3')
        b_blob.add_to_blender(
            appear_frame = cues['blue']['start'],
            animate = False
        )

        rhs = tex_bobject.TexBobject(
            "B + \\big(R-D\\big) \\times N",
            "B + \\big(R-D\\big) \\times N",
            "B + \\big(R-D\\big) \\times N",
            "B + \\big(R(1-M)-D\\big) \\times N",
            "B + \\big(R(1-M)-D\\big) \\times N",

            centered = True
        )
        equals = tex_bobject.TexBobject(
            "\!=",
            centered = True
        )
        lhs = tex_bobject.TexBobject(
            "\\Delta",
            "\\Delta",
            "\\Delta",
            centered = True
        )
        equation = tex_complex.TexComplex(
            lhs, equals, rhs,
            location = (2, 0, 0),
            scale = 1.2,
            centered = True
        )
        equation.add_annotation(
            targets = [
                0, #tex_bobject
                [
                    [0, 0, 0, None],  #form, first char, last char
                    [1, 0, 0],
                    [2, 0, 0, None]
                ],
            ],
            labels = [
                [],
                ['\\text{Total}', '\\text{expected}', '\\text{change}'],
                [],
            ],
            alignment = 'top',
        )
        equation.add_annotation(
            targets = [
                2, #tex_bobject
                [
                    [0, 0, 0, None],  #form, first char, last char
                    [1, 0, 0],
                    [2, 0, 0],
                    [3, 0, 0],
                    [4, 0, 0, None]
                ],
            ],
            labels = [
                [],
                ['\\text{Spontaneous}', '\\text{birth rate} \\phantom{blurghh}'],
                ['\\text{Spontaneous}', '\\text{birth rate} \\phantom{blurghh}'],
                ['\\text{Spontaneous}', '\\text{birth rate} \\phantom{blurghh}'],
                [],
            ],
            alignment = 'bottom',
            #angle = math.pi / 4
        )
        equation.add_annotation(
            targets = [
                2, #tex_bobject
                [
                    [0, 3, 3, None],  #form, first char, last char
                    [1, 3, 3, None],
                    [2, 3, 3],
                    [3, 3, 8],
                    [4, 3, 8, None],
                ],
            ],
            labels = [
                [],
                [],
                ['\\text{Replication chance}', '\\text{per creature}'],
                ['\\text{Adjusted}', '\\text{replication chance} \\phantom{blurghh}', '\\text{per creature}'],
                [],
            ],
            alignment = 'top'
        )
        equation.add_annotation(
            targets = [
                2, #tex_bobject
                [
                    [0, 5, 5, None],  #form, first char, last char
                    [1, 5, 5, None],
                    [2, 5, 5],
                    [3, 10, 10],
                    [4, 10, 10, None],
                ],
            ],
            labels = [
                [],
                [],
                ['\\text{Death chance}', '\\text{per creature}'],
                ['\\text{Death chance}', '\\text{per creature}'],
                [],
            ],
            alignment = 'bottom',
            angle = [0, 0, 0, - math.pi / 6, 0]
        )
        equation.add_annotation(
            targets = [
                2, #tex_bobject
                [
                    [0, 4, 4, None],  #form, first char, last char
                    [1, 4, 4, None],
                    [2, 4, 4, None],
                    [3, 7, 7],
                    [4, 7, 7, None],
                ],
            ],
            labels = [
                [],
                [],
                [],
                ['\\text{Mutation}', '\\text{chance}'],
                [],
            ],
            alignment = 'bottom',
            angle = math.pi / 6
        )
        equation.add_to_blender(
            appear_time = cues['blue']['start']
        )
        lhs.morph_figure(1, start_time = cues['blue']['start'] + 1)
        rhs.morph_figure(1, start_time = cues['blue']['start'] + 2)
        rhs.morph_figure(2, start_time = cues['blue']['start'] + 3)
        per_creature_term = []
        for i in range(2, 9):
            per_creature_term.append(rhs.lookup_table[2][i])
        for char in per_creature_term:
            char.pulse(time = cues['blue']['start'] + 3)
            char.color_shift(start_time = cues['blue']['start'] + 3)

        R = rhs.lookup_table[2][3]
        R.pulse(time = cues['blue']['start'] + 5)
        R.color_shift(start_time = cues['blue']['start'] + 5)

        #Show blue blobs replicate
        b_blob.move_to(
            new_location = [-13, 0.75, 0],
            new_scale = 0.5,
            start_time = cues['blue']['start'] + 6
        )
        rep_anim_bobjs = []
        for i in range(10):
            if i != 4:
                blob = import_object(
                    'boerd_blob', 'creatures',
                    location = [-13, 6.75 - i * 1.5, 0],
                    scale = 0.5,
                    wiggle = True,
                    cycle_length = scene_end * FRAME_RATE
                )
                apply_material(
                    blob.ref_obj.children[0].children[0],
                    'creature_color3'
                )
                blob.add_to_blender(appear_time = cues['blue']['start'] + 6)
                rep_anim_bobjs.append(blob)

            arrow = gesture.Gesture(
                gesture_series = [{
                    'type' : 'arrow',
                    'points' : {
                        'head' : [-10, 6.75 - i * 1.5, 0],
                        'tail' : [-12, 6.75 - i * 1.5, 0],
                    }
                }],
                color = 'color2'
            )
            arrow.add_to_blender(appear_time = cues['blue']['start'] + 7 + 0.1 * i)
            rep_anim_bobjs.append(arrow)

            blob = import_object(
                'boerd_blob', 'creatures',
                location = [-9, 6.75 - i * 1.5, 0],
                scale = 0.5,
                wiggle = True,
                cycle_length = scene_end * FRAME_RATE
            )
            apply_material(
                blob.ref_obj.children[0].children[0],
                'creature_color3'
            )
            """if i == 9:
                apply_material(
                    blob.ref_obj.children[0].children[0],
                    'creature_color7'
                )"""
            blob.add_to_blender(appear_time = cues['blue']['start'] + 7 + 0.1 * i)
            rep_anim_bobjs.append(blob)

        blob.color_shift(
            color = COLORS_SCALED[6],
            start_time = cues['blue']['start'] + 9,
            duration = None,
            obj = blob.ref_obj.children[0].children[0]
        )

        bracket = gesture.Gesture(
            gesture_series = [
                {
                    'type' : 'bracket',
                    'points' : {
                        'annotation_point': (-5, 0, 0),
                        'left_point': (-8, 7.5, 0),
                        'right_point': (-8, -7.5, 0)
                    }
                },
                {
                    'type' : 'bracket',
                    'points' : {
                        'annotation_point': (-5, 0, 0),
                        'left_point': (-8, 7.5, 0),
                        'right_point': (-8, -6, 0)
                    }
                }
            ],
            color = 'color2'
        )
        bracket.add_to_blender(appear_time = cues['blue']['start'] + 8)
        bracket.morph_figure(1, start_time = cues['blue']['start'] + 9)
        bracket.disappear(disappear_time = cues['blue']['start'] + 10)

        #Put things back after showing replication diagram thing
        for bobj in rep_anim_bobjs:
            bobj.disappear(disappear_time = cues['blue']['start'] + 11)
        b_blob.move_to(
            new_location = b_blob_start_location,
            new_scale = 2.5,
            start_time = cues['blue']['start'] + 11
        )

        rhs.morph_figure(3, start_time = cues['blue']['start'] + 15)

        rhs.morph_figure(4, start_time = cues['blue']['start'] + 17)
        lhs.morph_figure(2, start_time = cues['blue']['start'] + 17)
'''
'''
class GreenEquation(Scene):
    def __init__(self):
        self.subscenes = collections.OrderedDict([
            ('green', {'duration': 18}),
        ])
        super().__init__()

    def play(self):
        super().play()
        cues = self.subscenes
        scene_end = self.duration

        b_blob_start_location = [-11, 0, 0]
        b_blob = import_object(
            'boerd_blob', 'creatures',
            location = b_blob_start_location,
            scale = 2.5,
            wiggle = True,
            cycle_length = scene_end * FRAME_RATE
        )
        b_blob.ref_obj.children[0].children[0].data.resolution = 0.2
        apply_material(b_blob.ref_obj.children[0].children[0], 'creature_color3')
        b_blob.add_to_blender(
            appear_frame = cues['green']['start'],
            animate = False
        )

        brhs = tex_bobject.TexBobject(
            "B + \\big(R(1-M)-D\\big) \\times N",
            "B_1 + \\big(R_1(1-M_1)-D_1\\big) \\times N_1",
            "B_1 + R_1N_1 - R_1M_1N_1 -D_1N_1",
            centered = True
        )
        bequals = tex_bobject.TexBobject(
            "\!=",
            centered = True
        )
        blhs = tex_bobject.TexBobject(
            "\\Delta",
            centered = True
        )
        bequation = tex_complex.TexComplex(
            blhs, bequals, brhs,
            location = (2, 0, 0),
            scale = 1.2,
            centered = True
        )
        bequation.add_to_blender(
            appear_time = cues['green']['start'] - 0.5,
            animate = False
        )

        #Green stuff appears
        b_blob.move_to(
            displacement = [0, 4, 0],
            start_time = cues['green']['start']
        )
        bequation.move_to(
            displacement = [0, 4, 0],
            start_time = cues['green']['start']
        )

        g_blob_start_location = [-11, -4, 0]
        g_blob = import_object(
            'boerd_blob', 'creatures',
            location = g_blob_start_location,
            scale = 2.5,
            wiggle = True,
            cycle_length = scene_end * FRAME_RATE
        )
        g_blob.ref_obj.children[0].children[0].data.resolution = 0.2
        apply_material(g_blob.ref_obj.children[0].children[0], 'creature_color7')
        g_blob.add_to_blender(
            appear_frame = cues['green']['start']
        )


        grhs = tex_bobject.TexBobject(
            "B + \\big(R-D\\big) \\times N",
            "B_2 + \\big(R_2-D_2\\big) \\times N_2",
            "B_2 + \\big(R_2-D_2\\big) \\times N_2 + \\substack{\\text{From} \\\\ \\text{Mutation}}",
            "B_2 + \\big(R_2-D_2\\big) \\times N_2 - R_1M_1N_1",
            centered = True
        )
        gequals = tex_bobject.TexBobject(
            "\!=",
            centered = True
        )
        glhs = tex_bobject.TexBobject(
            "\\Delta",
            centered = True
        )
        gequation = tex_complex.TexComplex(
            glhs, gequals, grhs,
            location = (2, -4, 0),
            scale = 1.2,
            centered = True
        )
        gequation.add_to_blender(
            appear_time = cues['green']['start'] + 1,
            animate = False
        )

        #Make mutation terms white
        for i in range(6, 12):
            char = brhs.lookup_table[1][i]
            if i == 6:
                duration = 5.5 * FRAME_RATE
            else:
                duration = None
            char.color_shift(
                start_time = cues['green']['start'] - 1,
                duration = duration,
                color = COLORS_SCALED[1]
            )
        for i in range(12, 14):
            char = brhs.lookup_table[2][i]
            char.color_shift(
                start_time = cues['green']['start'] + 4,
                duration = None,
                color = COLORS_SCALED[1]
            )
        for i in range(13, len(grhs.lookup_table[2])):
            char = grhs.lookup_table[2][i]
            char.color_shift(
                start_time = cues['green']['start'] - 1,
                duration = None,
                color = COLORS_SCALED[1]
            )

        brhs.morph_figure(1, start_time = cues['green']['start'] + 2)
        grhs.morph_figure(1, start_time = cues['green']['start'] + 2)
        grhs.morph_figure('next', start_time = cues['green']['start'] + 3)
        brhs.morph_figure(2, start_time = cues['green']['start'] + 4)

        bg_arrow = gesture.Gesture(
            gesture_series = [{
                'type' : 'arrow',
                'points' : {
                    'head' : [4.5, -1.25, 0],
                    'tail' : [2.5, 1.25, 0],
                }
            }],
            color = 'color2',
            scale = 2
        )
        bg_arrow.add_to_blender(appear_time = cues['green']['start'] + 5)
        arrow_curve = bg_arrow.lookup_table[0][0]
        arrow_curve.color_shift(
            color_gradient = {
                'color_1' : COLORS_SCALED[2],
                'color_2' : COLORS_SCALED[6]
            }
        )

        grhs.morph_figure('next', start_time = cues['green']['start'] + 6)

        sg = import_object(
            'sunglasses',
            location = [1.17, -1.03 + 3, 0.44],
            rotation_euler = [0, 68.4 * math.pi / 180, 0],
            scale = 1,
        )
        sg.ref_obj.parent = g_blob.ref_obj.children[0]
        sg.ref_obj.parent_bone = g_blob.ref_obj.children[0].pose.bones["brd_bone_neck"].name
        sg.ref_obj.parent_type = 'BONE'
        sg.add_to_blender(
            appear_time = cues['green']['start'] + 7
        )
        sg.move_to(
            start_time = cues['green']['start'] + 7,
            displacement = [0, -3, 0]
        )
'''
'''
class RedYellow(Scene):
    def __init__(self):
        self.subscenes = collections.OrderedDict([
            ('rad', {'duration': 10}),
            ('yallow', {'duration': 10}),
        ])
        super().__init__()

    def play(self):
        super().play()
        cues = self.subscenes
        scene_end = self.duration
        print('Scene end is ' + str(scene_end))

        #Blue blob and stats
        b_blob = import_object(
            'boerd_blob', 'creatures',
            location = [-11, 0, 0],
            scale = 2.5,
            wiggle = True,
            cycle_length = scene_end * FRAME_RATE
        )
        b_blob.ref_obj.children[0].children[0].data.resolution = 0.2
        apply_material(b_blob.ref_obj.children[0].children[0], 'creature_color3')
        b_blob.add_to_blender(appear_time = cues['rad']['start'])

        #blue stats
        b_birth_chance = tex_bobject.TexBobject(
            *MutationScene.b_birth_chance_args_lab,
            #**MutationScene.b_birth_chance_kwargs,
        )
        b_death_chance = tex_bobject.TexBobject(
            *MutationScene.b_death_chance_args_lab,
            scale = 1,
        )
        b_rep_chance = tex_bobject.TexBobject(
            *MutationScene.b_rep_chance_args_lab,
        )
        b_mut_chance = tex_bobject.TexBobject(
            *MutationScene.b_mut_chance_args_lab,
        )
        b_stats = tex_complex.TexComplex(
            b_birth_chance, b_death_chance, b_rep_chance, b_mut_chance,
            multiline = True,
            line_height = 1.4,
            location = [2 / b_blob.ref_obj.scale[0], 0, 0],
            scale = 1 / b_blob.ref_obj.scale[0]
        )
        b_stats.ref_obj.parent = b_blob.ref_obj
        b_stats.add_to_blender(
            appear_time = cues['rad']['start'],
            #subbobject_timing = [0, 60, 120, ],
        )


        g_arrow = gesture.Gesture(
            gesture_series = [
                {
                    'type': 'arrow',
                    'points': {
                        'tail': (-1.5, 0, 0),
                        'head': (1.5, 0, 0)
                    }
                },
                {
                    'type': 'arrow',
                    'points': {
                        'tail': (-1.5, 0.5, 0),
                        'head': (1.5, 1.5, 0)
                    }
                },
                {
                    'type': 'arrow',
                    'points': {
                        'tail': (-3.5/1.6, 4/1.6, 0),
                        'head': (2.5/1.6, 4/1.6, 0)
                    }
                }
            ],
            scale = 1.6,
            color = 'color2'
        )
        g_arrow.add_to_blender(appear_time = cues['rad']['start'] + 1)

        #Green blob and stats
        g_blob = import_object(
            'boerd_blob', 'creatures',
            location = [5, 0, 0],
            scale = 2.5,
            wiggle = True,
            cycle_length = scene_end * FRAME_RATE
        )
        g_blob.ref_obj.children[0].children[0].data.resolution = 0.2
        apply_material(g_blob.ref_obj.children[0].children[0], 'creature_color7')
        g_blob.add_to_blender(appear_time = cues['rad']['start'] + 2)

        g_birth_chance = tex_bobject.TexBobject(
            *MutationScene.g_birth_chance_args_lab,
            #**MutationScene.b_birth_chance_kwargs,
        )
        g_death_chance = tex_bobject.TexBobject(
            *MutationScene.g_death_chance_args_lab,
            scale = 1,
        )
        g_rep_chance = tex_bobject.TexBobject(
            *MutationScene.g_rep_chance_args_lab,
        )
        g_stats = tex_complex.TexComplex(
            g_birth_chance, g_death_chance, g_rep_chance,
            multiline = True,
            line_height = 1.4,
            location = [2 / g_blob.ref_obj.scale[0], 0, 0],
            scale = 1 / g_blob.ref_obj.scale[0]
        )
        g_stats.ref_obj.parent = g_blob.ref_obj
        g_stats.add_to_blender(
            appear_time = cues['rad']['start'] + 2,
        )

        #Red
        #Move the green blob
        g_blob.move_to(
            new_location = [5, 4, 0],
            start_time = cues['rad']['start'] + 3
        )

        g_arrow.morph_figure(1, start_time = cues['rad']['start'] + 3)

        r_arrow = gesture.Gesture(
            gesture_series = [
                {
                    'type': 'arrow',
                    'points': {
                        'tail': (-1.5, -0.5, 0),
                        'head': (1.5, -1.5, 0)
                    }
                },
                {
                    'type': 'arrow',
                    'points': {
                        'tail': (-11/1.6, 1/1.6, 0),
                        'head': (-11/1.6, -1/1.6, 0)
                    }
                },
            ],
            scale = 1.6,
            color = 'color2'
        )
        r_arrow.add_to_blender(appear_time = cues['rad']['start'] + 3)

        #Red blob and stats
        r_blob = import_object(
            'boerd_blob', 'creatures',
            location = [5, -4, 0],
            scale = 2.5,
            wiggle = True,
            cycle_length = scene_end * FRAME_RATE
        )
        r_blob.ref_obj.children[0].children[0].data.resolution = 0.2
        apply_material(r_blob.ref_obj.children[0].children[0], 'creature_color6')
        r_blob.add_to_blender(appear_time = cues['rad']['start'] + 3)

        r_birth_chance = tex_bobject.TexBobject(
            *MutationScene.r_birth_chance_args_lab,
            #**MutationScene.b_birth_chance_kwargs,
        )
        r_death_chance = tex_bobject.TexBobject(
            *MutationScene.r_death_chance_args_lab,
            scale = 1,
        )
        r_rep_chance = tex_bobject.TexBobject(
            *MutationScene.r_rep_chance_args_lab,
        )
        r_stats = tex_complex.TexComplex(
            r_birth_chance, r_death_chance, r_rep_chance,
            multiline = True,
            line_height = 1.4,
            location = [2 / r_blob.ref_obj.scale[0], 0, 0],
            scale = 1 / r_blob.ref_obj.scale[0]
        )
        r_stats.ref_obj.parent = r_blob.ref_obj
        r_stats.add_to_blender(
            appear_time = cues['rad']['start'] + 3,
        )


        b_mut_chance2 = tex_bobject.TexBobject(
            *MutationScene.b_mut_chance_args2_lab,
        )
        b_stats.add_tex_bobject(b_mut_chance2)
        b_mut_chance2.add_to_blender(
            appear_time = cues['rad']['start'] + 4
        )
        b_stats.arrange_tex_bobjects(
            start_time = cues['rad']['start'] + 4
        )
        b_mut_chance.morph_figure(1, start_time = cues['rad']['start'] + 5)
        b_mut_chance2.morph_figure(1, start_time = cues['rad']['start'] + 6)







        """cam_bobj = bobject.Bobject(location = CAMERA_LOCATION)
        cam_bobj.add_to_blender(appear_time = 0)
        cam_obj = bpy.data.objects['Camera']
        cam_obj.location = [0, 0, 0]
        cam_obj.parent = cam_bobj.ref_obj

        cam_bobj.move_to(
            new_location = [5, 1.2, 3],
            start_time = cues['rad']['start']
        )
        cam_bobj.move_to(
            new_location = CAMERA_LOCATION,
            start_time = cues['rad']['start']
        )"""

        b_blob.move_to(
            displacement = [0, 4, 0],
            start_time = cues['yallow']['start']
        )
        """b_stats.move_to(
            new_scale = 0.3,
            start_time = cues['yallow']['start']
        )"""
        """g_blob.move_to(
            new_location = [-2.5, 4, 0],
            start_time = cues['yallow']['start']
        )"""
        g_arrow.morph_figure(2, start_time = cues['yallow']['start'])
        r_blob.move_to(
            new_location = [-11, -4, 0],
            start_time = cues['yallow']['start']
        )
        r_arrow.morph_figure(1, start_time = cues['yallow']['start'])


        r_mut_chance = tex_bobject.TexBobject(
            *MutationScene.r_mut_chance_args_lab,
        )
        r_stats.add_tex_bobject(r_mut_chance)
        r_mut_chance.add_to_blender(
            appear_time = cues['yallow']['start'] + 3
        )
        r_stats.arrange_tex_bobjects(
            start_time = cues['yallow']['start'] + 3
        )

        #Red blob and stats
        y_blob = import_object(
            'boerd_blob', 'creatures',
            location = [5, -4, 0],
            scale = 2.5,
            wiggle = True,
            cycle_length = scene_end * FRAME_RATE
        )
        y_blob.ref_obj.children[0].children[0].data.resolution = 0.2
        apply_material(y_blob.ref_obj.children[0].children[0], 'creature_color4')
        y_blob.add_to_blender(appear_time = cues['yallow']['start'] + 3)

        y_birth_chance = tex_bobject.TexBobject(
            *MutationScene.y_birth_chance_args_lab,
            #**MutationScene.b_birth_chance_kwargs,
        )
        y_death_chance = tex_bobject.TexBobject(
            *MutationScene.y_death_chance_args_lab,
            scale = 1,
        )
        y_rep_chance = tex_bobject.TexBobject(
            *MutationScene.y_rep_chance_args_lab,
        )
        y_stats = tex_complex.TexComplex(
            y_birth_chance, y_death_chance, y_rep_chance,
            multiline = True,
            line_height = 1.4,
            location = [2 / y_blob.ref_obj.scale[0], 0, 0],
            scale = 1 / y_blob.ref_obj.scale[0]
        )
        y_stats.ref_obj.parent = y_blob.ref_obj
        y_stats.add_to_blender(
            appear_time = cues['yallow']['start'] + 1,
        )

        y_arrow = gesture.Gesture(
            gesture_series = [
                {
                    'type': 'arrow',
                    'points': {
                        'tail': (-3.5/1.6, -4/1.6, 0),
                        'head': (2.5/1.6, -4/1.6, 0)
                    }
                }
            ],
            scale = 1.6,
            color = 'color2'
        )
        y_arrow.add_to_blender(appear_time = cues['yallow']['start'] + 1)

        #This somehow get set to zero messed up somewhere above.
        y_blob.ref_obj.scale = [2.5, 2.5, 2.5]

        b_blob.move_to(
            new_location = [-12.1, 5.5, 0],
            new_scale = 1.5,
            start_time = scene_end - 0.5
        )
        """b_stats.move_to(
            displacement = [
                0,
                -0.7 * 0.4,
                0
            ],
            start_time = scene_end - 0.5
        )"""
        g_blob.move_to(
            new_location = [-5.1, 5.5, 0],
            new_scale = 1.5,
            start_time = scene_end - 0.5
        )
        """g_stats.move_to(
            displacement = [
                0,
                0.7 * 0.4,
                0
            ],
            start_time = scene_end - 0.5
        )"""
        r_blob.move_to(
            new_location = [1.9, 5.5, 0],
            new_scale = 1.5,
            start_time = scene_end - 0.5
        )
        y_blob.move_to(
            new_location = [8.9, 5.5, 0],
            new_scale = 1.5,
            start_time = scene_end - 0.5
        )
        """y_stats.move_to(
            displacement = [
                0,
                0.7 * 0.4,
                0
            ],
            start_time = scene_end - 0.5
        )"""

        remaining = [
            g_arrow, r_arrow, y_arrow
        ]
        for thing in remaining:
            thing.disappear(disappear_time = scene_end)
'''
'''
class RedYellowSim(Scene):
    def __init__(self):
        self.subscenes = collections.OrderedDict([
            ('sim', {'duration': 24}),
        ])
        super().__init__()

    def play(self):
        super().play()
        print('Scene end is ' + str(self.duration))

        self.set_up()
        self.sim()
        #self.graph()

    def set_up(self):
        cues = self.subscenes
        scene_end = self.duration

        #Blue blob and stats
        b_blob = import_object(
            'boerd_blob', 'creatures',
            location = [-12.1, 5.5, 0],
            scale = 1.5,
            wiggle = True,
            cycle_length = scene_end * FRAME_RATE
        )
        b_blob.ref_obj.children[0].children[0].data.resolution = 0.2
        apply_material(b_blob.ref_obj.children[0].children[0], 'creature_color3')
        b_blob.add_to_blender(appear_time = cues['sim']['start'] - 0.5)

        #blue stats
        b_birth_chance = tex_bobject.TexBobject(
            *MutationScene.b_birth_chance_args_lab,
            #**MutationScene.b_birth_chance_kwargs,
        )
        b_death_chance = tex_bobject.TexBobject(
            *MutationScene.b_death_chance_args_lab,
            scale = 1,
        )
        b_rep_chance = tex_bobject.TexBobject(
            *MutationScene.b_rep_chance_args_lab,
        )
        b_mut_chance = tex_bobject.TexBobject(
            *MutationScene.b_mut_chance_args_lab,
        )
        b_mut_chance2 = tex_bobject.TexBobject(
            *MutationScene.b_mut_chance_args2_lab,
        )
        b_stats = tex_complex.TexComplex(
            b_birth_chance, b_death_chance, b_rep_chance,
            b_mut_chance, b_mut_chance2,
            multiline = True,
            line_height = 1.4,
            location = [0.8, 0, 0],
            scale = 0.4
        )
        b_stats.ref_obj.parent = b_blob.ref_obj
        b_stats.add_to_blender(
            appear_time = cues['sim']['start'] - 0.5,
        )
        b_mut_chance.morph_figure(1, start_time = cues['sim']['start'] - 0.5)
        b_mut_chance2.morph_figure(1, start_time = cues['sim']['start'] - 0.5)

        #Green blob and stats
        g_blob = import_object(
            'boerd_blob', 'creatures',
            location = [-5.1, 5.5, 0],
            scale = 1.5,
            wiggle = True,
            cycle_length = scene_end * FRAME_RATE
        )
        g_blob.ref_obj.children[0].children[0].data.resolution = 0.2
        apply_material(g_blob.ref_obj.children[0].children[0], 'creature_color7')
        g_blob.add_to_blender(appear_time = cues['sim']['start'] - 0.5)

        g_birth_chance = tex_bobject.TexBobject(
            *MutationScene.g_birth_chance_args_lab,
            #**MutationScene.b_birth_chance_kwargs,
        )
        g_death_chance = tex_bobject.TexBobject(
            *MutationScene.g_death_chance_args_lab,
            scale = 1,
        )
        g_rep_chance = tex_bobject.TexBobject(
            *MutationScene.g_rep_chance_args_lab,
        )
        g_stats = tex_complex.TexComplex(
            g_birth_chance, g_death_chance, g_rep_chance,
            multiline = True,
            line_height = 1.4,
            location = [0.8, 0, 0],
            scale = 0.4
        )
        g_stats.ref_obj.parent = g_blob.ref_obj
        g_stats.add_to_blender(
            appear_time = cues['sim']['start'] - 0.5,
        )

        #Red blob and stats
        r_blob = import_object(
            'boerd_blob', 'creatures',
            location = [1.9, 5.5, 0],
            scale = 1.5,
            wiggle = True,
            cycle_length = scene_end * FRAME_RATE
        )
        r_blob.ref_obj.children[0].children[0].data.resolution = 0.2
        apply_material(r_blob.ref_obj.children[0].children[0], 'creature_color6')
        r_blob.add_to_blender(appear_time = cues['sim']['start'] - 0.5)

        r_birth_chance = tex_bobject.TexBobject(
            *MutationScene.r_birth_chance_args_lab,
            #**MutationScene.b_birth_chance_kwargs,
        )
        r_death_chance = tex_bobject.TexBobject(
            *MutationScene.r_death_chance_args_lab,
            scale = 1,
        )
        r_rep_chance = tex_bobject.TexBobject(
            *MutationScene.r_rep_chance_args_lab,
        )
        r_mut_chance = tex_bobject.TexBobject(
            *MutationScene.r_mut_chance_args_lab,
        )
        r_stats = tex_complex.TexComplex(
            r_birth_chance, r_death_chance, r_rep_chance, r_mut_chance,
            multiline = True,
            line_height = 1.4,
            location = [0.8, 0, 0],
            scale = 0.4
        )
        r_stats.ref_obj.parent = r_blob.ref_obj
        r_stats.add_to_blender(
            appear_time = cues['sim']['start'] - 0.5,
        )

        #Yellow blob
        y_blob = import_object(
            'boerd_blob', 'creatures',
            location = [8.9, 5.5, 0],
            scale = 1.5,
            wiggle = True,
            cycle_length = scene_end * FRAME_RATE
        )
        y_blob.ref_obj.children[0].children[0].data.resolution = 0.2
        apply_material(y_blob.ref_obj.children[0].children[0], 'creature_color4')
        y_blob.add_to_blender(appear_time = cues['sim']['start'] - 0.5)

        y_birth_chance = tex_bobject.TexBobject(
            *MutationScene.y_birth_chance_args_lab,
            #**MutationScene.b_birth_chance_kwargs,
        )
        y_death_chance = tex_bobject.TexBobject(
            *MutationScene.y_death_chance_args_lab,
            scale = 1,
        )
        y_rep_chance = tex_bobject.TexBobject(
            *MutationScene.y_rep_chance_args_lab,
        )
        y_stats = tex_complex.TexComplex(
            y_birth_chance, y_death_chance, y_rep_chance,
            multiline = True,
            line_height = 1.4,
            location = [0.8, 0, 0],
            scale = 0.4
        )
        y_stats.ref_obj.parent = y_blob.ref_obj
        y_stats.add_to_blender(
            appear_time = cues['sim']['start'] - 0.5,
        )

    def sim(self):
        cues = self.subscenes
        scene_end = self.duration

        sim = drawn_world.DrawnWorld(
            **MutationScene.second_mutation_sim_kwargs
        )
        sim.add_to_blender(
            appear_time = cues['sim']['start']
        )

        """def graph(self):
        cues = self.subscenes
        scene_end = self.duration"""

        graph = graph_bobject.GraphBobject(
            **MutationScene.second_mutation_sim_graph_kwargs
        )
        graph.add_to_blender(appear_time = cues['sim']['start'])
        func = sim.get_creature_count_by_t(color = 'creature_color_1')
        graph.add_new_function_and_curve(func, color = 3)

        func = sim.get_creature_count_by_t(color = 'creature_color_2')
        graph.add_new_function_and_curve(func, color = 7)

        func = sim.get_creature_count_by_t(color = 'creature_color_3')
        graph.add_new_function_and_curve(func, color = 6)

        func = sim.get_creature_count_by_t(color = 'creature_color_4')
        graph.add_new_function_and_curve(func, color = 4)

        graph.animate_function_curve(
            start_time = cues['sim']['start'] + sim.start_delay / FRAME_RATE,
            end_time = cues['sim']['start'] + (sim.start_delay + sim.sim_duration * sim.frames_per_time_step) / FRAME_RATE,
            uniform_along_x = True,
            index = 0
        )
        graph.animate_function_curve(
            start_time = cues['sim']['start'] + sim.start_delay / FRAME_RATE,
            end_time = cues['sim']['start'] + (sim.start_delay + sim.sim_duration * sim.frames_per_time_step) / FRAME_RATE,
            uniform_along_x = True,
            index = 1
        )
        graph.animate_function_curve(
            start_time = cues['sim']['start'] + sim.start_delay / FRAME_RATE,
            end_time = cues['sim']['start'] + (sim.start_delay + sim.sim_duration * sim.frames_per_time_step) / FRAME_RATE,
            uniform_along_x = True,
            index = 2
        )
        graph.animate_function_curve(
            start_time = cues['sim']['start'] + sim.start_delay / FRAME_RATE,
            end_time = cues['sim']['start'] + (sim.start_delay + sim.sim_duration * sim.frames_per_time_step) / FRAME_RATE,
            uniform_along_x = True,
            index = 3
        )

        #I messed up and rendered without the disappear code, so I did it all manually.
        """to_disappear = [b_blob, g_blob, r_blob, sim, graph]
        for i, thing in enumerate(to_disappear):
            thing.disappear(
                disappear_time = cues['sim']['end'] - (len(to_disappear) - 1 - i) * 0.05
            )"""
'''
'''
class TheDoorIsOpen(Scene):
    def __init__(self):
        self.subscenes = collections.OrderedDict([
            ('blob_tree', {'duration': 6}),
            ('big_tree', {'duration': 6}),
            ('tree_swap', {'duration': 10}),
        ])
        super().__init__()

    def play(self):
        super().play()
        cues = self.subscenes
        scene_end = self.duration
        print('Scene end is ' + str(scene_end))

        #Blue blob
        b_blob = import_object(
            'boerd_blob', 'creatures',
            location = [-11, 0, 0],
            scale = 2.5,
            wiggle = True,
            cycle_length = scene_end * FRAME_RATE
        )
        b_blob.ref_obj.children[0].children[0].data.resolution = 0.2
        apply_material(b_blob.ref_obj.children[0].children[0], 'creature_color3')

        g_arrow = gesture.Gesture(
            gesture_series = [
                {
                    'type': 'arrow',
                    'points': {
                        'tail': (-8/1.6, 1/1.6, 0),
                        'head': (-3/1.6, 3/1.6, 0)
                    }
                },
                {
                    'type': 'arrow',
                    'points': {
                        'tail': (-9/1, 4/1, 0),
                        'head': (-6.67/1, 4/1, 0)
                    }
                },
            ],
            scale = 1.6,
            color = 'color2'
        )

        #Green blob
        g_blob = import_object(
            'boerd_blob', 'creatures',
            location = [0, 4, 0],
            scale = 2.5,
            wiggle = True,
            cycle_length = scene_end * FRAME_RATE
        )
        g_blob.ref_obj.children[0].children[0].data.resolution = 0.2
        apply_material(g_blob.ref_obj.children[0].children[0], 'creature_color7')

        r_arrow = gesture.Gesture(
            gesture_series = [
                {
                    'type': 'arrow',
                    'points': {
                        'tail': (-8/1.6, -1/1.6, 0),
                        'head': (-3/1.6, -3/1.6, 0)
                    }
                },
                {
                    'type': 'arrow',
                    'points': {
                        'tail': (-10/1, 1/1, 0),
                        'head': (-9/1, -1/1, 0)
                    }
                },
                {
                    'type': 'arrow',
                    'points': {
                        'tail': (-1.5, 0, 0),
                        'head': (1.5, 0, 0)
                    }
                },
                {
                    'type': 'arrow',
                    'points': {
                        'tail': (-8/1.6, -1/1.6, 0),
                        'head': (-3/1.6, -3/1.6, 0)
                    }
                },
            ],
            scale = 1.6,
            color = 'color2'
        )

        #Red blob
        r_blob = import_object(
            'boerd_blob', 'creatures',
            location = [0, -4, 0],
            scale = 2.5,
            wiggle = True,
            cycle_length = scene_end * FRAME_RATE
        )
        r_blob.ref_obj.children[0].children[0].data.resolution = 0.2
        apply_material(r_blob.ref_obj.children[0].children[0], 'creature_color6')

        #Red blob
        y_blob = import_object(
            'boerd_blob', 'creatures',
            location = [11, 0, 0],
            scale = 2.5,
            wiggle = True,
            cycle_length = scene_end * FRAME_RATE
        )
        y_blob.ref_obj.children[0].children[0].data.resolution = 0.2
        apply_material(y_blob.ref_obj.children[0].children[0], 'creature_color4')

        y_arrow = gesture.Gesture(
            gesture_series = [
                {
                    'type': 'arrow',
                    'points': {
                        'head': (8/1.6, -1/1.6, 0),
                        'tail': (3/1.6, -3/1.6, 0)
                    }
                },
                {
                    'type': 'arrow',
                    'points': {
                        'head': (-3.5/1, -4/1, 0),
                        'tail': (-5.833/1, -4/1, 0)
                    }
                }
            ],
            scale = 1.6,
            color = 'color2'
        )

        b_blob.add_to_blender(appear_time = cues['blob_tree']['start'])
        g_arrow.add_to_blender(appear_time = cues['blob_tree']['start'] + 0.1)
        g_blob.add_to_blender(appear_time = cues['blob_tree']['start'] + 0.2)
        r_arrow.add_to_blender(appear_time = cues['blob_tree']['start'] + 0.3)
        r_blob.add_to_blender(appear_time = cues['blob_tree']['start'] + 0.4)
        y_arrow.add_to_blender(appear_time = cues['blob_tree']['start'] + 0.5)
        y_blob.add_to_blender(appear_time = cues['blob_tree']['start'] + 0.6)

        """y_blob.pulse(
            time = cues['blob_tree']['start'] + 2,
            duration_time = 2
        )"""
        y_blob.blob_wave(
            start_time = cues['blob_tree']['start'] + 2,
            duration = 2
        )
        b_blob.pulse(
            time = cues['blob_tree']['start'] + 4,
            duration_time = 2
        )

        #big_tree
        b_blob.move_to(
            new_location = [-11, 4, 0],
            start_time = cues['big_tree']['start'] + 2
        )
        g_blob.move_to(
            new_location = [-11 / 3 - 1, 4, 0],
            start_time = cues['big_tree']['start'] + 2
        )
        g_arrow.morph_figure(1, start_time = cues['big_tree']['start'] + 2)
        g_arrow.move_to(new_scale = 1, start_time = cues['big_tree']['start'] + 2)
        r_blob.move_to(
            new_location = [-11 * 2 / 3 - 0.5, -4, 0],
            start_time = cues['big_tree']['start'] + 2
        )
        r_arrow.morph_figure(1, start_time = cues['big_tree']['start'] + 2)
        r_arrow.move_to(new_scale = 1, start_time = cues['big_tree']['start'] + 2)
        y_blob.move_to(
            new_location = [-1.5, -4, 0],
            start_time = cues['big_tree']['start'] + 2
        )
        y_arrow.morph_figure(1, start_time = cues['big_tree']['start'] + 2)
        y_arrow.move_to(new_scale = 1, start_time = cues['big_tree']['start'] + 2)

        q1 = tex_bobject.TexBobject(
            '\\text{?}',
            location = [0, 2, 0],
            scale = 2,
            centered = True
        )
        q2 = tex_bobject.TexBobject(
            '\\text{?}',
            location = [3, -1, 0],
            scale = 2,
            centered = True
        )
        q3 = tex_bobject.TexBobject(
            '\\text{?}',
            location = [4.5, -5, 0],
            scale = 2,
            centered = True
        )
        q1_arrow = gesture.Gesture(
            gesture_series = [
                {
                    'type': 'arrow',
                    'points': {
                        'head': (-0.33, 0.67, 0),
                        'tail': (-1, -1.33, 0)
                    }
                }
            ],
            color = 'color2'
        )
        q2_arrow = gesture.Gesture(
            gesture_series = [
                {
                    'type': 'arrow',
                    'points': {
                        'head': (2.1, -1.8, 0),
                        'tail': (0.2, -3.3, 0)
                    }
                }
            ],
            color = 'color2'
        )
        q3_arrow = gesture.Gesture(
            gesture_series = [
                {
                    'type': 'arrow',
                    'points': {
                        'head': (3.4, -5, 0),
                        'tail': (0.7, -5, 0)
                    }
                }
            ],
            color = 'color2'
        )
        qs = [q1_arrow, q1, q2_arrow, q2, q3_arrow, q3]
        for i, q in enumerate(qs):
            q.add_to_blender(appear_time = cues['big_tree']['start'] + 3 + 0.1 * i)

        q4 = tex_bobject.TexBobject(
            '\\text{?}',
            location = [4.5, 4, 0],
            scale = 2,
            centered = True
        )
        q4_arrow = gesture.Gesture(
            gesture_series = [
                {
                    'type': 'arrow',
                    'points': {
                        'head': (4.2, 2.6, 0),
                        'tail': (3.5, 0.4, 0)
                    }
                }
            ],
            color = 'color2'
        )
        dotdotdot = tex_bobject.TexBobject(
            '\\text{...}',
            location = [7.25, 1, 0],
            scale = 2,
            centered = True
        )
        dot_arrow = gesture.Gesture(
            gesture_series = [
                {
                    'type': 'arrow',
                    'points': {
                        'head': (6, -0.1, 0),
                        'tail': (4, -1, 0)
                    }
                }
            ],
            color = 'color2'
        )

        qs2 = [q4_arrow, q4, dot_arrow, dotdotdot]
        for i, q in enumerate(qs2):
            q.add_to_blender(appear_time = cues['big_tree']['start'] + 4 + 0.1 * i)

        chick = import_object(
            'chicken', 'creatures',
            location = [11, 5, 0],
            scale = 2
        )
        chk_arrow = gesture.Gesture(
            gesture_series = [
                {
                    'type': 'arrow',
                    'points': {
                        'head': (9, 3, 0),
                        'tail': (7.7, 1.2, 0)
                    }
                }
            ],
            color = 'color2'
        )
        bun = import_object(
            'stanford_bunny', 'creatures',
            location = [11, -4.5, 0],
            scale = 2
        )
        bun_arrow = gesture.Gesture(
            gesture_series = [
                {
                    'type': 'arrow',
                    'points': {
                        'head': (8.6, -2, 0),
                        'tail': (7.7, -1.2 + 0.67, 0)
                    }
                }
            ],
            color = 'color2'
        )
        ams = [chk_arrow, chick, bun_arrow, bun]
        for i, q in enumerate(ams):
            q.add_to_blender(appear_time = cues['big_tree']['start'] + 5 + 0.1 * i)

        #tree_swap
        #Just blue and yellow
        to_hide = [
            q1, q2, q3, q4, q1_arrow, q2_arrow, q3_arrow, q4_arrow,
            chick, bun, dotdotdot, chk_arrow, bun_arrow, dot_arrow,
            g_blob, g_arrow, r_blob, y_arrow
        ]
        for thing in to_hide:
            thing.disappear(disappear_time = cues['tree_swap']['start'] + 7.5 - 1/60)

        b_blob.move_to(
            new_location = [-8, 0, 0],
            new_scale = 4,
            start_time = cues['tree_swap']['start'] + 7
        )
        y_blob.move_to(
            new_location = [8, 0, 0],
            new_scale = 4,
            start_time = cues['tree_swap']['start'] + 7
        )
        r_arrow.morph_figure(2, start_time = cues['tree_swap']['start'] + 7)
        r_arrow.move_to(new_scale = 2, start_time = cues['tree_swap']['start'] + 7)

        #put things back to original small tree
        b_blob.move_to(
            new_location = [-11, 0, 0],
            new_scale = 2.5,
            start_time = cues['tree_swap']['start'] + 8
        )
        g_blob.move_to(
            new_location = [0, 4, 0],
            start_time = cues['tree_swap']['start'] + 8
        )
        r_blob.move_to(
            new_location = [0, -4, 0],
            start_time = cues['tree_swap']['start'] + 8
        )
        y_blob.move_to(
            new_location = [11, 0, 0],
            new_scale = 2.5,
            start_time = cues['tree_swap']['start'] + 8
        )

        to_unhide = [g_arrow, y_arrow, g_blob, r_blob]
        for thing in to_unhide:
            thing.add_to_blender(appear_time = cues['tree_swap']['start'] + 8)
        g_arrow.move_to(new_scale = 1.6, start_time = cues['tree_swap']['start'] + 8)
        y_arrow.move_to(new_scale = 1.6, start_time = cues['tree_swap']['start'] + 8)
        r_arrow.morph_figure(3, start_time = cues['tree_swap']['start'] + 8)
        r_arrow.move_to(new_scale = 1.6, start_time = cues['tree_swap']['start'] + 8)

        #Okay, now back to the complex one
        to_unhide = [
            q1, q2, q3, q4, q1_arrow, q2_arrow, q3_arrow, q4_arrow,
            chick, bun, dotdotdot, chk_arrow, bun_arrow, dot_arrow,
        ]
        for thing in to_unhide:
            thing.add_to_blender(appear_time = cues['tree_swap']['start'] + 9)

        b_blob.move_to(
            new_location = [-11, 4, 0],
            start_time = cues['tree_swap']['start'] + 9
        )
        g_blob.move_to(
            new_location = [-11 / 3 - 1, 4, 0],
            start_time = cues['tree_swap']['start'] + 9
        )
        g_arrow.morph_figure(1, start_time = cues['tree_swap']['start'] + 9)
        g_arrow.move_to(new_scale = 1, start_time = cues['tree_swap']['start'] + 9)
        r_blob.move_to(
            new_location = [-11 * 2 / 3 - 0.5, -4, 0],
            start_time = cues['tree_swap']['start'] + 9
        )
        r_arrow.morph_figure(1, start_time = cues['tree_swap']['start'] + 9)
        r_arrow.move_to(new_scale = 1, start_time = cues['tree_swap']['start'] + 9)
        y_blob.move_to(
            new_location = [-1.5, -4, 0],
            start_time = cues['tree_swap']['start'] + 9
        )
        y_arrow.morph_figure(1, start_time = cues['tree_swap']['start'] + 9)
        y_arrow.move_to(new_scale = 1, start_time = cues['tree_swap']['start'] + 9)



        """remaining = [
            g_arrow, r_arrow, y_arrow
        ]
        for thing in remaining:
            thing.disappear(disappear_time = scene_end)"""
'''
'''
class RNA(Scene):
    def __init__(self):
        self.subscenes = collections.OrderedDict([
            ('blob_tree', {'duration': 11}),
        ])
        super().__init__()

    def play(self):
        super().play()
        cues = self.subscenes
        scene_end = self.duration

        rna = import_object(
            'rna', 'biochem',
            scale = 50,
            location = [0, 2, 0]
        )
        rna.add_to_blender(
            appear_time = 0,
        )
        rna.de_explode(
            start_time = 0.5,
            duration = 2,
            delay_step = 5
        )
        rna.move_to(
            new_scale = 8,
            new_location = [0, 0, 0],
            start_time = 0.5,
            end_time = 7
        )
        """rna.spiny(
            start_time = 1,
            end_time = scene_end,
            spin_rate = 0.2
        )"""
'''
'''
class NextVideo(Scene):
    def __init__(self):
        self.subscenes = collections.OrderedDict([
            ('graph', {'duration': 16}),
        ])
        super().__init__()

    def play(self):
        super().play()
        cues = self.subscenes
        scene_end = self.duration

        sim = drawn_world.DrawnWorld(
            **MutationScene.second_mutation_sim_kwargs
        )

        graph = graph_bobject.GraphBobject(
            **MutationScene.second_mutation_sim_graph_end_kwargs
        )
        graph.add_to_blender(appear_time = cues['graph']['start'])
        func = sim.get_creature_count_by_t(color = 'creature_color_1')
        graph.add_new_function_and_curve(func, color = 3)

        func = sim.get_creature_count_by_t(color = 'creature_color_2')
        graph.add_new_function_and_curve(func, color = 7)

        func = sim.get_creature_count_by_t(color = 'creature_color_3')
        graph.add_new_function_and_curve(func, color = 6)

        func = sim.get_creature_count_by_t(color = 'creature_color_4')
        graph.add_new_function_and_curve(func, color = 4)


        y_blob = import_object(
            'boerd_blob', 'creatures',
            location = [10, -1, 0],
            scale = 3,
            wiggle = True,
            cycle_length = scene_end * FRAME_RATE
        )
        y_blob.ref_obj.children[0].children[0].data.resolution = 0.2
        apply_material(y_blob.ref_obj.children[0].children[0], 'creature_color4')
        y_blob.add_to_blender(appear_time = cues['graph']['start'])

'''

"""def play_scenes():
    last = LastVideo()
    last.play()
    #ext = Extinction()
    #ext.play()
"""
