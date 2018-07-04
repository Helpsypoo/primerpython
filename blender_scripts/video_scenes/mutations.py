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

        frames_per_time_step = 15
        start_delay = 1.5
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
            'start_delay' : start_delay,
            'frames_per_time_step' : frames_per_time_step,
            'load' : 'ro_not_extinction',
            'sim_duration' : sim_duration,
            'initial_creatures' : initial_creatures,
            'gene_updates' : [
                ['color', 'creature_color_1', 'birth_modifier', 0, 0],
                ['shape', 'shape1', 'birth_modifier', 0, 0],
                ['size', '1', 'birth_modifier', 0, 0],
                ['color', 'creature_color_1', 'mutation_chance', 0, 0],
                ['shape', 'shape1', 'mutation_chance', 0, 0],
                ['size', '1', 'mutation_chance', 0, 0],
                ['color', 'creature_color_1', 'death_modifier', 200, 0],
                ['color', 'creature_color_1', 'replication_modifier', 300, 0],
            ],
            'pauses' : [
                [0, 1]
            ]
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

'''
class LastVideoExp(Scene, MutationScene):
    def __init__(self):
        self.subscenes = collections.OrderedDict([
            ('sim', {'duration': 8}),
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
            location = [0, 4.5, 0],
            scale = 2.7
        )
        apply_material(blob.ref_obj.children[0].children[0], 'creature_color3')
        blob.add_to_blender(appear_time = 0)

        graph = graph_bobject.GraphBobject(
            func2,
            **MutationScene.graph_kwargs
        )
        graph.add_to_blender(appear_time = cues['sim']['start'])

        appear_coord = [5, 0.5, 0]


        #Transition to N-t graph
        def exp_func(x): return 2 * math.exp(0.1 * x)
        #def exp_func(x): return 15 * math.exp(0.1 * x) - 10
        graph2 = graph_bobject.GraphBobject(
            exp_func,
            **MutationScene.graph2_kwargs
        )

        frames_per_time_step = 15
        start_delay = 1.5
        sim_duration = 20

        initial_creature_count = 2
        initial_creatures = []
        for i in range(initial_creature_count):
            new_creature = creature.Creature()
            initial_creatures.append(new_creature)
        sim = drawn_world.DrawnWorld(
            **MutationScene.sim_kwargs
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
        point2.disappear(disappear_time = cues['sim']['start'] + 7.5)
        point2.axis_projections[0].disappear(disappear_time = cues['sim']['start'] + 7.5)
        point2.axis_projections[1].disappear(disappear_time = cues['sim']['start'] + 7.5)
        zoom_arrow.disappear(disappear_time = cues['sim']['start'] + 7.5)


        #Prep for next scene
        to_disappear = [blob, graph, sim, graph2]
        for thing in to_disappear:
            thing.disappear(disappear_time = cues['sim']['end'])
'''
'''
class LastVideoChicken(Scene, MutationScene):
    def __init__(self):
        self.subscenes = collections.OrderedDict([
            ('form', {'duration': 8}),
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
        for thing in to_disappear:
            thing.disappear(disappear_time = cues['sim']['end'])
'''
'''
class Logo(Scene):
    def __init__(self):

        self.subscenes = collections.OrderedDict([
            ('logo', {'duration': 4})
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
#'''
class BlueGreenCards(Scene):
    def __init__(self):

        self.subscenes = collections.OrderedDict([
            ('blue', {'duration': 4}),
            ('blue_stats', {'duration': 4}),
            ('green_stats', {'duration': 9})
        ])
        super().__init__()

    def play(self):
        super().play()
        cues = self.subscenes
        scene_end = self.duration

        b_blob = import_object(
            'boerd_blob', 'creatures',
            location = [0, 0, 0],
            scale = 4,
            wiggle = True
        )
        b_blob.ref_obj.children[0].children[0].data.resolution = 0.2
        apply_material(b_blob.ref_obj.children[0].children[0], 'creature_color3')
        b_blob.add_to_blender(appear_time = cues['blue']['start'])

        b_blob2 = import_object(
            'boerd_blob', 'creatures',
            location = [0, 0, 0],
            scale = 4,
            wiggle = True
        )
        b_blob2.ref_obj.children[0].children[0].data.resolution = 0.2
        apply_material(b_blob2.ref_obj.children[0].children[0], 'creature_color3')
        b_blob2.add_to_blender(appear_time = cues['blue']['start'] + 1)

        b_blob.move_to(
            new_location = [-8, 0, 0],
            start_time = cues['blue']['start'] + 1
        )
        b_blob2.move_to(
            new_location = [8, 0, 0],
            start_time = cues['blue']['start'] + 1
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
        arrow.add_to_blender(appear_time = cues['blue']['start'] + 1)


        #Second blue blob disappears to make way for the green blob
        arrow.disappear(disappear_time = cues['blue']['start'] + 2.5)
        b_blob2.disappear(disappear_time = cues['blue']['start'] + 2.5)
        b_blob.move_to(
            new_location = [0, 0, 0],
            start_time = cues['blue']['start'] + 2
        )

        #Green blob appears
        g_blob = import_object(
            'boerd_blob', 'creatures',
            location = [0, 0, 0],
            scale = 4,
            wiggle = True
        )
        g_blob.ref_obj.children[0].children[0].data.resolution = 0.2
        apply_material(g_blob.ref_obj.children[0].children[0], 'creature_color7')
        g_blob.add_to_blender(appear_time = cues['blue']['start'] + 3)

        b_blob.move_to(
            new_location = [-8, 0, 0],
            start_time = cues['blue']['start'] + 3
        )
        g_blob.move_to(
            new_location = [8, 0, 0],
            start_time = cues['blue']['start'] + 3
        )
        arrow.add_to_blender(appear_time = cues['blue']['start'] + 3 + 1/60)


        #blue stats

        b_blob.move_to(
            new_location = [-11, 0, 0],
            new_scale = 2.5,
            start_time = cues['blue_stats']['start']
        )
        b_birth_chance = tex_bobject.TexBobject(
            'B = 100\%',
            scale = 1,
        )
        b_death_chance = tex_bobject.TexBobject(
            'D = 10\%',
            scale = 1,
        )
        b_rep_chance = tex_bobject.TexBobject(
            'R = 5\%',
            scale = 1,
        )
        b_stats = tex_complex.TexComplex(
            b_birth_chance, b_death_chance, b_rep_chance,
            multiline = True,
            line_height = 1.4,
            location = [-9, 0, 0]
        )
        b_stats.add_to_blender(
            appear_time = cues['blue_stats']['start'],
            subbobject_timing = [0, 60, 120],
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
            start_time = cues['green_stats']['start'] + 1
        )
        cam_bobj.move_to(
            new_location = CAMERA_LOCATION,
            start_time = cues['green_stats']['start'] + 3
        )

        #cam_obj.keyframe_insert(data_path = 'location', frame = 540)
        #cam_obj.location = [5, 1.2, 3]
        #cam_obj.keyframe_insert(data_path = 'location', frame = 600)
        #cam_obj.keyframe_insert(data_path = 'location', frame = 660)
        #cam_obj.location = [5, 1.2, 3]
        #am_obj.keyframe_insert(data_path = 'location', frame = 720)
        #cam = bpy.data.cameras[0]

        g_birth_chance = tex_bobject.TexBobject(
            'B = 100\%',
            scale = 1,
        )
        g_death_chance = tex_bobject.TexBobject(
            'D = 10\%',
            scale = 1,
        )
        g_rep_chance = tex_bobject.TexBobject(
            'R = 5\%',
            scale = 1,
        )
        g_stats = tex_complex.TexComplex(
            g_birth_chance, g_death_chance, g_rep_chance,
            multiline = True,
            line_height = 1.4,
            location = [7, 0, 0]
        )
        g_stats.add_to_blender(
            appear_time = cues['green_stats']['start'] + 5,
            subbobject_timing = [0, 60, 120],
        )

        b_mut_chance = tex_bobject.TexBobject(
            'M = 10\%',
            scale = 1,
        )
        b_stats.add_tex_bobject(b_mut_chance)
        b_mut_chance.add_to_blender(
            appear_time = cues['green_stats']['start'] + 8
        )
        b_stats.arrange_tex_bobjects(
            start_time = cues['green_stats']['start'] + 8
        )



#'''

"""def play_scenes():
    last = LastVideo()
    last.play()
    #ext = Extinction()
    #ext.play()
"""
