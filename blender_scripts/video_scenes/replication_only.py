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
'''
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
'''
'''
class ChickenEgg(Scene):
    def __init__(self):
        self.subscenes = collections.OrderedDict([
            ('scene', {'duration': 720})
        ])
        super().__init__()

    def play(self):
        super().play()
        cues = self.subscenes
        scene_end = self.duration

        chicken = import_object(
            'chicken',
            scale = 4,
            location = (-7, 0, 0)
        )
        chicken.add_to_blender()

        egg = import_object(
            'egg',
            scale = 4,
            location = (7, 0, 0)
        )
        egg.add_to_blender()

        top_arrow = gesture.Gesture(
            gesture_series = [
                {
                    'type': 'arrow',
                    'points': {
                        'tail': (-1.5, 1.5, 0),
                        'head': (1.5, 1.5, 0)
                    }
                }
            ],
            scale = 2
        )
        top_arrow.add_to_blender(appear_frame = 120)

        bottom_arrow = gesture.Gesture(
            gesture_series = [
                {
                    'type': 'arrow',
                    'points': {
                        'head': (-1.5, -1.5, 0),
                        'tail': (1.5, -1.5, 0)
                    }
                }
            ],
            scale = 2
        )
        bottom_arrow.add_to_blender(appear_frame = 120)

        wha = tex_bobject.TexBobject(
            '\\text{?}',
            centered = True,
            location = (0, 0, 0),
            scale = 3
        )
        wha.add_to_blender(appear_frame = 180)
'''
'''
class FirstKindOfGraph(Scene):
    def __init__(self):
        self.subscenes = collections.OrderedDict([
            ('one_sim', {'duration': 420}),
            ('two_sims', {'duration': 420}),
            ('three_sims', {'duration': 420})
        ])
        super().__init__()

    def play(self):
        super().play()
        cues = self.subscenes
        scene_end = self.duration

        frames_per_time_step = 5
        start_delay = 30
        sim_duration = 60

        initial_creature_count = 10
        initial_creatures = []
        for i in range(initial_creature_count):
            new_creature = creature.Creature()
            initial_creatures.append(new_creature)
        sim = drawn_world.DrawnWorld(
            name = 'blob1_sim',
            location = [-7.5, 0, 0],
            scale = 0.6,
            appear_frame = cues['one_sim']['start'],
            start_delay = start_delay,
            frames_per_time_step = frames_per_time_step,
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
            tick_step = [20, 5],
            width = 10,
            height = 10,
            x_label = '\\text{Time}',
            x_label_pos = 'along',
            y_label = '\\text{Number}',
            y_label_pos = 'end',
            location = (7, 0, 0),
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

        sim.move_to(
            new_location = (-9, -4.2, 0),
            new_scale = 0.35,
            end_frame = cues['one_sim']['end']
        )
        graph.move_to(
            new_location = (-9, 3.7, 0),
            new_scale = 0.6,
            end_frame = cues['one_sim']['end']
        )



        #Two sims
        frames_per_time_step = 5
        start_delay = 30
        sim_duration = 60

        initial_creature_count = 10
        initial_creatures = []
        for i in range(initial_creature_count):
            new_creature = creature.Creature()
            initial_creatures.append(new_creature)
        sim2 = drawn_world.DrawnWorld(
            name = 'blob1_sim',
            location = [0, -4.2, 0],
            scale = 0.35,
            appear_frame = cues['two_sims']['start'],
            start_delay = start_delay,
            frames_per_time_step = frames_per_time_step,
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
        sim2.add_to_blender(appear_frame = cues['two_sims']['start'])

        func2 = sim2.get_creature_count_by_t()
        graph2 = graph_bobject.GraphBobject(
            func2,
            x_range = [0, sim_duration],
            y_range = [0, 20],
            tick_step = [20, 5],
            width = 10,
            height = 10,
            x_label = '\\text{Time}',
            x_label_pos = 'along',
            y_label = '\\text{Number}',
            y_label_pos = 'end',
            location = (0, 3.7, 0),
            centered = True,
            arrows = True,
            scale = 0.6
        )
        graph2.add_to_blender(appear_frame = cues['two_sims']['start'])
        graph2.animate_function_curve(
            start_frame = cues['two_sims']['start'] + start_delay,
            end_frame = cues['two_sims']['start'] + start_delay + sim2.sim_duration_in_frames,
            uniform_along_x = True
        )
        appear_coord = [0, func2[0], 0]
        point = graph2.add_point_at_coord(
            coord = appear_coord,
            appear_frame = 0,
            axis_projections = True,
            track_curve = True
        )
        graph2.animate_point(
            end_coord = [sim_duration, 0, 0],
            start_frame = cues['two_sims']['start'] + start_delay,
            end_frame = cues['two_sims']['start'] + start_delay + sim2.sim_duration_in_frames,
            point = point
        )

        #Three sims
        frames_per_time_step = 5
        start_delay = 30
        sim_duration = 60

        initial_creature_count = 10
        initial_creatures = []
        for i in range(initial_creature_count):
            new_creature = creature.Creature()
            initial_creatures.append(new_creature)
        sim3 = drawn_world.DrawnWorld(
            name = 'blob1_sim',
            location = [9, -4.2, 0],
            scale = 0.35,
            appear_frame = cues['three_sims']['start'],
            start_delay = start_delay,
            frames_per_time_step = frames_per_time_step,
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
        sim3.add_to_blender(appear_frame = cues['three_sims']['start'])

        func3 = sim3.get_creature_count_by_t()
        graph3 = graph_bobject.GraphBobject(
            func3,
            x_range = [0, sim_duration],
            y_range = [0, 20],
            tick_step = [20, 5],
            width = 10,
            height = 10,
            x_label = '\\text{Time}',
            x_label_pos = 'along',
            y_label = '\\text{Number}',
            y_label_pos = 'end',
            location = (9, 3.7, 0),
            centered = True,
            arrows = True,
            scale = 0.6
        )
        graph3.add_to_blender(appear_frame = cues['three_sims']['start'])
        graph3.animate_function_curve(
            start_frame = cues['three_sims']['start'] + start_delay,
            end_frame = cues['three_sims']['start'] + start_delay + sim3.sim_duration_in_frames,
            uniform_along_x = True
        )
        appear_coord = [0, func3[0], 0]
        point = graph3.add_point_at_coord(
            coord = appear_coord,
            appear_frame = 0,
            axis_projections = True,
            track_curve = True
        )
        graph3.animate_point(
            end_coord = [sim_duration, 0, 0],
            start_frame = cues['three_sims']['start'] + start_delay,
            end_frame = cues['three_sims']['start'] + start_delay + sim3.sim_duration_in_frames,
            point = point
        )
'''
'''
class FunctionTime(Scene):
    def __init__(self):
        self.subscenes = collections.OrderedDict([
            ('graph', {'duration': 1000}),
        ])
        super().__init__()

    def play(self):
        super().play()
        cues = self.subscenes
        scene_end = self.duration

        def func(x):
            return 3 + 2 * x - x * x / 1.55 + x ** 3 / 20

        graph = graph_bobject.GraphBobject(
            func,
            x_range = [0, 10],
            y_range = [0, 10],
            tick_step = [5, 5],
            width = 10,
            height = 10,
            x_label = 'x',
            x_label_pos = 'end',
            y_label = 'y',
            y_label_pos = 'end',
            location = (0, -1, 0),
            centered = True,
            arrows = True
        )
        graph.add_to_blender(appear_frame = 0)
        arrow = gesture.Gesture(
            gesture_series = [
                {
                    'type': 'arrow',
                    'points': {
                        'head': (-3, 5.3, 0),
                        'tail': (0, 5.3, 0)
                    }
                },
                {
                    'type': 'arrow',
                    'points': {
                        'head': (6.5, -4, 0),
                        'tail': (6.5, -1, 0)
                    }
                }
            ]
        )
        arrow.add_to_blender(appear_frame = 60)
        graph.y_label_bobject.pulse(
            frame = 60,
            duration = 120
        )
        graph.y_label_bobject.subbobjects[0].color_shift(
            start_frame = 60,
            duration = 120,
            color = COLORS_SCALED[3],
            shift_time = OBJECT_APPEARANCE_TIME / 2
        )
        arrow.morph_figure(1, start_frame = 180)
        graph.x_label_bobject.pulse(
            frame = 180,
            duration = 120
        )
        graph.x_label_bobject.subbobjects[0].color_shift(
            start_frame = 180,
            duration = 120,
            color = COLORS_SCALED[3],
            shift_time = OBJECT_APPEARANCE_TIME / 2
        )

        graph.move_to(
            new_location = (-7.5, -1, 0),
            start_frame = 360
        )
        arrow.disappear(
            disappear_frame = 360
        )

        func_eq = tex_bobject.TexBobject(
            'y = f(x)',
            location = (7.5, 3, 0),
            centered = True,
            scale = 2
        )
        func_eq.add_to_blender(
            appear_frame = 420
        )

        x_step = 0.1
        x = 0
        x_values = []
        y_values = []
        while x <= 10:
            x_values.append(str(x))
            x += x_step
            x = round(x, 1)
            y = round(func(x), 1)
            y_values.append(str(y))

        x = tex_bobject.TexBobject(
            *x_values,
            location = (10.2, -3, 0),
            transition_type = 'instant',
            centered = True,
            scale = 2
        )
        x.add_to_blender(
            appear_frame = 480
        )
        x_arrow = gesture.Gesture(
            gesture_series = [
                {
                    'type': 'arrow',
                    'points': {
                        'tail': (10.2, -1.5, 0),
                        'head': (10.2, 1, 0)
                    }
                }
            ]
        )
        x_arrow.add_to_blender(appear_frame = 480)

        y = tex_bobject.TexBobject(
            *y_values,
            location = (4, -3, 0),
            transition_type = 'instant',
            centered = True,
            scale = 2
        )
        y.add_to_blender(
            appear_frame = 540
        )
        y_arrow = gesture.Gesture(
            gesture_series = [
                {
                    'type': 'arrow',
                    'points': {
                        'head': (4, -1.5, 0),
                        'tail': (4, 1, 0)
                    }
                }
            ]
        )
        y_arrow.add_to_blender(appear_frame = 540)

        graph.animate_function_curve(
            start_frame = 600,
            end_frame = 720,
            uniform_along_x = True
        )
        appear_coord = [0, func(0), 0]
        point = graph.add_point_at_coord(
            coord = appear_coord,
            appear_frame = 540,
            axis_projections = True,
            track_curve = True
        )
        graph.animate_point(
            end_coord = [10, 0, 0],
            start_frame = 600,
            end_frame = 720,
            point = point
        )

        start_frame = 600
        end_frame = 720
        time_step = (end_frame - start_frame) / (len(x_values) - 1)
        for i in range(1, len(x_values)):
            x.morph_figure(i, start_frame = start_frame + i * time_step)
            y.morph_figure(i, start_frame = start_frame + i * time_step)
'''
#'''
class EquationToFunction(Scene):
    def __init__(self):
        self.subscenes = collections.OrderedDict([
            ('sim', {'duration': 600}),
            ('equation', {'duration': 600}),
        ])
        super().__init__()

    def play(self):
        super().play()
        cues = self.subscenes
        scene_end = self.duration


        #Equation
        lhs = tex_bobject.TexBobject(
            "\\text{Birth rate}",
            "\\text{Birth rate} - \\text{Death rate}",
            #"B",
            #"\\dfrac{B}{D}",
            centered = True
        )
        equals = tex_bobject.TexBobject(
            "\!=",
            #"\!<",
            #"\!=",
            #"\!>",
            #"\!=",
            centered = True
        )
        rhs = tex_bobject.TexBobject(
            "\\text{Death rate}",
            "0",
            #"\\text{Number} \\times \\text{Death rate per creature}",
            #"\\text{Number} \\times 0.1",
            #"\\text{Number} \\times \\text{Death rate per creature}",
            #N \\times D",
            #"\\dfrac{N \\times D}{D}",
            #"N",
            centered = True
        )

        equation = bobject.TexComplex(
            lhs, equals, rhs,
            centered = True,
            location = (0, 0, 0),
            scale = 1.5
        )

        equation.add_to_blender(
            appear_frame = 0,
            animate = False,
            subbobject_timing = [0, 60, 105]
        )

        equation.move_to(
            new_location = (0, 6.5, 0),
            #new_scale = 1,
            start_frame = 180
        )

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
            location = [0, -1.5, 0],
            scale = 0.6,
            appear_frame = cues['sim']['start'] + 180,
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
                ['color', 'creature_color_1', 'death_modifier', 100, 0],
                ['color', 'creature_color_1', 'replication_modifier', 0, 0],
                ['color', 'creature_color_1', 'birth_modifier', 0, 6],
                ['color', 'creature_color_1', 'death_modifier', 500, 6],
                ['color', 'creature_color_1', 'birth_modifier', 5000, 7],
                ['color', 'creature_color_1', 'death_modifier', 0, 7],
                ['color', 'creature_color_1', 'birth_modifier', 1000, 8],
                ['color', 'creature_color_1', 'death_modifier', 100, 8],
            ],
            pauses = [
                [5, 6],
                [6, 6],
                [7, 6]
            ]
        )
        sim.add_to_blender(appear_frame = cues['sim']['start'] + 180)

        lhs.morph_figure(1, start_frame = cues['equation']['start'])
        rhs.morph_figure(1, start_frame = cues['equation']['start'])

        equals2 = tex_bobject.TexBobject(
            "\!=",
            centered = True
        )
        slhs = tex_bobject.TexBobject(
            "\\Delta",
            centered = True
        )
        equals2.superbobject = equation
        slhs.superbobject = equation
        equals2.ref_obj.parent = equation.ref_obj
        slhs.ref_obj.parent = equation.ref_obj
        equals2.add_to_blender(appear_frame = cues['equation']['start'] + 60)
        slhs.add_to_blender(appear_frame = cues['equation']['start'] + 60)
        equation.subbobjects = [slhs, equals2, lhs, equals, rhs]
        equation.arrange_tex_bobjects(
            start_frame = cues['equation']['start'] + 60,
            end_frame = cues['equation']['start'] + 60 + DEFAULT_MORPH_TIME
        )
        tot = tex_bobject.TexBobject(
            "\\text{Total}",
            centered = True
        )
        exp = tex_bobject.TexBobject(
            "\\text{expected}",
            centered = True
        )
        cha = tex_bobject.TexBobject(
            "\\text{change}",
            centered = True
        )
        total_change_annotation = tex_bobject.TexComplex(
            tot, exp, cha,
            location = (-11.5, 0, 0),
            centered = True,
            scale = 1,
            multiline = True
        )
        total_change_annotation.add_to_blender(
            appear_frame = cues['equation']['start'] + 120
        )
        arrow = gesture.Gesture(
            gesture_series = [
                {
                    'type': 'arrow',
                    'points': {
                        'tail': (-11.5, 2.2, 0),
                        'head': (-11.5, 5.2, 0)
                    }
                },
                {
                    'type': 'arrow',
                    'points': {
                        'tail': (-11, 2.2, 0),
                        'head': (-10.25, 5.2, 0)
                    }
                }
            ]
        )
        arrow.add_to_blender(
            appear_frame = cues['equation']['start'] + 120
        )
        birth_rate_bobjs = []
        for i in range(0, 9):
            birth_rate_bobjs.append(lhs.lookup_table[0][i])
        for bobj in birth_rate_bobjs:
            bobj.color_shift(
                color = COLORS_SCALED[3],
                start_frame = cues['equation']['start'] + 180,
                duration = 60
            )
        death_rate_bobjs = []
        for i in range(10, 19):
            death_rate_bobjs.append(lhs.lookup_table[1][i])
        for bobj in death_rate_bobjs:
            bobj.color_shift(
                color = COLORS_SCALED[3],
                start_frame = cues['equation']['start'] + 240,
                duration = 60
            )
        delta = slhs.lookup_table[0][0]
        delta.color_shift(
            color = COLORS_SCALED[3],
            start_frame = cues['equation']['start'] + 300,
            duration = 60
        )
        eq = equals.lookup_table[0][0]
        eq.color_shift(
            color = COLORS_SCALED[3],
            start_frame = cues['equation']['start'] + 360,
            duration = 60
        )
        zero = rhs.lookup_table[0][0]
        zero.color_shift(
            color = COLORS_SCALED[3],
            start_frame = cues['equation']['start'] + 360,
            duration = 60
        )

        equals.disappear(disappear_frame = cues['equation']['start'] + 420)
        rhs.disappear(disappear_frame = cues['equation']['start'] + 420)

        equation.subbobjects = [slhs, equals2, lhs]
        equation.arrange_tex_bobjects(
            start_frame = cues['equation']['start'] + 420,
            end_frame = cues['equation']['start'] + 420 + DEFAULT_MORPH_TIME
        )
        arrow.morph_figure(1, start_frame = cues['equation']['start'] + 420)

#'''
