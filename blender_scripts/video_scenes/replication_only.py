import collections

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
import gesture
imp.reload(gesture)
import graph_bobject
imp.reload(graph_bobject)

import helpers
imp.reload(helpers)
from helpers import *

'''
class IntroImage(Scene):
    def __init__(self):

        self.subscenes = collections.OrderedDict([
            ('logo', {'duration': 240})
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
            appear_frame = cues['logo']['start'],
            #subbobject_timing = [90, 30, 40, 50, 60, 70, 80],
            subbobject_timing = [42, 30, 33, 36, 39, 42, 45],
            animate = True
        )
        logo.disappear(disappear_frame = scene_end)
'''
'''
class TheGoal(Scene):
    def __init__(self):
        self.subscenes = collections.OrderedDict([
            ('sim', {'duration': 240})
        ])
        super().__init__()

    def play(self):
        super().play()
        cues = self.subscenes
        scene_end = self.duration


        rhs = tex_bobject.TexBobject(
            "\\dfrac{B}{D - R}",
            "\\dfrac{\\xcancel{B}}{D - R}",
            centered = True,
            vert_align_centers = False
        )
        equals = tex_bobject.TexBobject(
            "\!=",
            centered = True
        )
        lhs = tex_bobject.TexBobject(
            "N",
            centered = True
        )
        equation = bobject.TexComplex(
            lhs, equals, rhs,
            centered = True,
            scale = 1.5,
            location = (-7.5, 0, 0)
        )

        initial_creature_count = 5
        initial_creatures = []
        for i in range(initial_creature_count):
            new_creature = creature.Creature()
            initial_creatures.append(new_creature)
        sim = drawn_world.DrawnWorld(
            name = 'blob1_sim',
            location = [6, 0, 0],
            scale = 0.8,
            appear_frame = cues['sim']['start'],
            start_delay = 30,
            #save = True,
            #load = 'wte_eq_replication',
            duration = scene_end - cues['sim']['start'],
            initial_creatures = initial_creatures,
            gene_updates = [
                ['color', 'creature_color_1', 'birth_modifier', 30, 0],
                ['shape', 'shape1', 'birth_modifier', 1, 0],
                ['size', '1', 'birth_modifier', 1, 0],
                ['color', 'creature_color_1', 'mutation_chance', 0, 0],
                ['shape', 'shape1', 'mutation_chance', 0, 0],
                ['size', '1', 'mutation_chance', 0, 0],
                ['color', 'creature_color_1', 'death_modifier', 16, 0],
                ['color', 'creature_color_1', 'replication_modifier', 10, 0],
            ],
            #counter_alignment = 'top_left',
            #creature_model = ['stanford_bunny', 'creatures']
        )

        equation.add_to_blender(appear_frame = cues['sim']['start'])
        #rhs.morph_figure(1, start_frame = 60)


        sim.add_to_blender(
            appear_frame = cues['sim']['start'],
            animate = True
        )

        B = rhs.lookup_table[0][0]
        B.pulse(
            frame = 60,
            duration = 2 * OBJECT_APPEARANCE_TIME
        )
        B.color_shift(
            start_frame = 60,
            duration = 2 * OBJECT_APPEARANCE_TIME,
            color = COLORS_SCALED[3]
        )

        spontaneous = tex_bobject.TexBobject(
            '\\substack{\\text{Spontaneous} \\\\ \\text{birth chance}}',
            location = (-5.5, 5.5, 0),
            centered = True
        )
        spontaneous.add_to_blender(appear_frame = 60)

        spont_arrow = gesture.Gesture(
            gesture_series = [
                #{
                #    'type': 'bracket',
                #    'points': {
                #        'annotation_point': (-5.5, 4, 0),
                #        'left_point': (-6.5, 2, 0),
                #        'right_point': (-4.5, 2, 0)
                #    }
                #}
                {
                    'type': 'arrow',
                    'points': {
                        'tail': (-5.5, 4.25, 0),
                        'head': (-5.5, 2.25, 0)
                    }
                }
            ]
        )
        spont_arrow.add_to_blender(appear_frame = 60)
        spont_arrow.subbobjects[0].color_shift(
            start_frame = 60,
            duration = 2 * OBJECT_APPEARANCE_TIME,
            color = COLORS_SCALED[3]
        )
        for bobj in spontaneous.subbobjects:
            bobj.color_shift(
                start_frame = 60,
                duration = 2 * OBJECT_APPEARANCE_TIME,
                color = COLORS_SCALED[3]
            )

        R = rhs.lookup_table[0][4]
        R.pulse(
            frame = 120,
            duration = 2 * OBJECT_APPEARANCE_TIME
        )
        R.color_shift(
            start_frame = 120,
            duration = 2 * OBJECT_APPEARANCE_TIME,
            color = COLORS_SCALED[3]
        )
        replication = tex_bobject.TexBobject(
            '\\substack{\\text{Replication} \\\\ \\text{chance}}',
            location = (-5, -5.5, 0),
            centered = True
        )
        replication.add_to_blender(appear_frame = 120)

        rep_arrow = gesture.Gesture(
            gesture_series = [
                #{
                #    'type': 'bracket',
                #    'points': {
                #        'annotation_point': (-5.5, 4, 0),
                #        'left_point': (-6.5, 2, 0),
                #        'right_point': (-4.5, 2, 0)
                #    }
                #}
                {
                    'type': 'arrow',
                    'points': {
                        'tail': (-5, -4.25, 0),
                        'head': (-4.2, -2.25, 0)
                    }
                }
            ]
        )
        rep_arrow.add_to_blender(appear_frame = 120)
        rep_arrow.subbobjects[0].color_shift(
            start_frame = 120,
            duration = 2 * OBJECT_APPEARANCE_TIME,
            color = COLORS_SCALED[3]
        )
        for bobj in replication.subbobjects:
            bobj.color_shift(
                start_frame = 120,
                duration = 2 * OBJECT_APPEARANCE_TIME,
                color = COLORS_SCALED[3]
            )

        rhs.morph_figure(1, start_frame = 210)
        cross1 = rhs.lookup_table[1][1]
        apply_material(cross1.ref_obj.children[0], 'color6')
        cross2 = rhs.lookup_table[1][0]
        apply_material(cross2.ref_obj.children[0], 'color6')
'''
#'''
class ThereWillBeGraphs(Scene):
    def __init__(self):
        self.subscenes = collections.OrderedDict([
            ('sim', {'duration': 720})
        ])
        super().__init__()

    def play(self):
        super().play()
        cues = self.subscenes
        scene_end = self.duration

        start_delay = 30
        sim_duration = 60
        #frames_per_time_step = 5
        #sim_duration_frames = sim_duration * frames_per_time_step

        initial_creature_count = 10
        initial_creatures = []
        for i in range(initial_creature_count):
            new_creature = creature.Creature()
            initial_creatures.append(new_creature)
        sim = drawn_world.DrawnWorld(
            name = 'blob1_sim',
            location = [-7.5, 0, 0],
            scale = 0.6,
            appear_frame = cues['sim']['start'],
            start_delay = start_delay,
            frames_per_time_step = 10,
            #save = True,
            #load = 'wte_eq_replication',
            sim_duration = sim_duration,
            initial_creatures = initial_creatures,
            gene_updates = [
                ['color', 'creature_color_1', 'birth_modifier', 1000, 0],
                ['shape', 'shape1', 'birth_modifier', 1, 0],
                ['size', '1', 'birth_modifier', 1, 0],
                ['color', 'creature_color_1', 'mutation_chance', 0, 0],
                ['shape', 'shape1', 'mutation_chance', 0, 0],
                ['size', '1', 'mutation_chance', 0, 0],
                ['color', 'creature_color_1', 'death_modifier', 100, 0],
                #['color', 'creature_color_1', 'replication_modifier', 10, 0],
            ]
        )
        sim.add_to_blender(appear_frame = 0)

        func = sim.get_creature_count_by_t()
        graph = graph_bobject.GraphBobject(
            func,
            x_range = [0, sim_duration],
            y_range = [0, 20],
            tick_step = [20, 10],
            width = 10,
            height = 5,
            x_label = 't',
            x_label_pos = 'end',
            y_label = 'N',
            y_label_pos = 'along',
            location = (7, -4.5, 0),
            centered = True,
            arrows = True
        )
        graph.add_to_blender(appear_frame = 0)
        graph.animate_function_curve(
            start_frame = start_delay,
            end_frame = start_delay + sim.sim_duration_in_frames,
            uniform_along_x = True
        )
        appear_coord = [0, func[0], 0]
        point = graph.add_point_at_coord(
            coord = appear_coord,
            appear_frame = 0,
            axis_projections = True,
            track_curve = True
        )
        graph.animate_point(
            end_coord = [sim_duration, 0, 0],
            start_frame = start_delay,
            end_frame = start_delay + sim.sim_duration_in_frames,
            point = point
        )

        #Rate-number graph
        def func2(x): return 1 - x / 10
        graph2 = graph_bobject.GraphBobject(
            func2,
            x_range = [0, 20],
            y_range = [-1, 1],
            tick_step = [5, 1],
            width = 10,
            height = 5,
            x_label = 'N',
            x_label_pos = 'end',
            y_label = '\\Delta',
            y_label_pos = 'end',
            location = (7, 2.5, 0),
            centered = True,
            arrows = True
        )
        graph2.add_to_blender()
        appear_coord = [func[0], func2(func[0]), 0]
        point2 = graph2.add_point_at_coord(
            coord = appear_coord,
            appear_frame = start_delay,
            axis_projections = True,
            track_curve = True
        )
        #This needs to change to account for the new frames_per_time_step
        #parameter. This function assumes it's always 1, but it's not.
        graph2.multi_animate_point(
            start_frame = start_delay,
            point = point2,
            x_of_t = func, #Not func2. This uses the sim data to inform movements
            frames_per_time_step = sim.frames_per_time_step
        )
#'''
