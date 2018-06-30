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

'''
class Extinction(Scene):
    def __init__(self):
        self.subscenes = collections.OrderedDict([
            ('graph', {'duration': 6}),
            ('ntgraph', {'duration': 19.5}),
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

        graph = graph_bobject.GraphBobject(
            func, func2,
            x_range = [0, 10],
            y_range = [-1, 2],
            tick_step = [5, 1],
            width = 10,
            height = 10,
            x_label = 'N',
            x_label_pos = 'end',
            y_label = '\\Delta',
            y_label_pos = 'end',
            location = (-7.5, -1, 0),
            centered = True,
            arrows = True,
        )
        graph.add_to_blender(appear_time = cues['graph']['start'] - 0.5)

        rhs = tex_bobject.TexBobject(
            "1 + (0.3-0.2) \\times N",
            "0 + (0.3-0.2) \\times N",
            "0 + (0.3-0.2) \\times N",
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
            location = (7.5, 0, 0),
            scale = 1,
            centered = True
        )
        equation.add_annotation(
            targets = [
                2, #tex_bobject
                [
                    [0, 0, 0],  #form, first char, last char
                    [1, 0, 0],
                    [2, 0, 0, None],
                ],
            ],
            labels = [
                ['\\text{Spontaneous}', '\\text{birth rate} \\phantom{blurghh}'],
                ['\\text{Spontaneous}', '\\text{birth rate} \\phantom{blurghh}'],
                [],
            ],
            alignment = 'bottom'
        )
        equation.add_annotation(
            targets = [
                2, #tex_bobject
                [
                    [0, 3, 5, 'arrow'],  #form, first char, last char
                    [1, 3, 5, 'arrow'],
                    [2, 3, 5, None],
                ],
            ],
            labels = [
                ['\\text{Replication chance}', '\\text{per creature}'],
                ['\\text{Replication chance}', '\\text{per creature}'],
                [],
            ],
            alignment = 'top'
        )
        equation.add_annotation(
            targets = [
                2, #tex_bobject
                [
                    [0, 7, 9, 'arrow'],
                    [1, 7, 9, 'arrow'],
                    [2, 7, 9, None],
                ],
            ],
            labels = [
                ['\\text{Death chance}', '\\text{per creature}'],
                ['\\text{Death chance}', '\\text{per creature}'],
                [],
            ],
            alignment = 'bottom'
        )
        equation.add_to_blender(
            appear_time = cues['graph']['start'] - 0.5,
            animate = False
        )

        #Get rid of B
        rhs.morph_figure(1, start_time = cues['graph']['start'])
        graph.morph_curve(1, start_time = cues['graph']['start'])

        appear_coord = [5, 0.5, 0]
        point = graph.add_point_at_coord(
            coord = appear_coord,
            appear_time = cues['graph']['start'] + 0.5,
            axis_projections = True,
            track_curve = None
        )

        num_shifts = 3
        frames_per_shift = 60

        coords = [[5, 0.5, 0]]
        for i in range(num_shifts):
            x = coords[i][0] + coords[i][1]
            y = 0.1 * x
            coords.append([x, y, 0])

        coords.append([0, 0, 0])

        x_of_t = []
        for i, coord in enumerate(coords):
            time = i * frames_per_shift
            x_of_t.append([time, coord])

        #Wiggle
        #time = time + 60

        num_wiggles = 2
        time_per_wiggle = 20
        for i in range(num_wiggles):
            x_of_t.append([time + time_per_wiggle * i, [0.1, 0, 0]])
            x_of_t.append([time + time_per_wiggle * i + time_per_wiggle / 2, [-0.1, 0, 0]])
        x_of_t.append([time + time_per_wiggle * num_wiggles, [0, 0, 0]])
        x_of_t.append([time + time_per_wiggle * num_wiggles + time_per_wiggle / 2, [0, 0, 0]])
        #Last one is here because the last shift (currently) automatically takes
        #the default transition time, regardless of time values. Using the last
        #one to add another keyframe and speed up the final transition.


        graph.multi_animate_point(
            point = point,
            x_of_t = x_of_t,
            #frames_per_time_step = 30,
            start_time = cues['graph']['start'],
            full_coords = True
        )


        extinction = tex_bobject.TexBobject(
            '\\text{Extinction}',
            location = [-7, -5, 0],
            centered = True,
            color = 'color2'
        )
        ex_arrow = gesture.Gesture(
            gesture_series = [
                {
                    'type' : 'arrow',
                    'points' : {
                        'head' : [-10.5, -3, 0],
                        'tail' : [-8, -4.3, 0],
                    }
                }
            ],
            color = 'color2'
        )
        extinction.add_to_blender(appear_time = cues['graph']['start'] + 5)
        ex_arrow.add_to_blender(appear_time = cues['graph']['start'] + 5)

        point.disappear(disappear_time = cues['graph']['start'] + 6)
        point.axis_projections[0].disappear(disappear_time = cues['graph']['start'] + 6)
        point.axis_projections[1].disappear(disappear_time = cues['graph']['start'] + 6)

        extinction.disappear(disappear_time = cues['graph']['start'] + 6)
        ex_arrow.disappear(disappear_time = cues['graph']['start'] + 6)

        #Transition to N-t graph
        def exp_func(x): return 2 * math.exp(0.1 * x)
        #def exp_func(x): return 15 * math.exp(0.1 * x) - 10
        graph2 = graph_bobject.GraphBobject(
            exp_func,
            x_range = [0, 20],
            y_range = [0, 30],
            tick_step = [5, 10],
            width = 10,
            height = 10,
            x_label = 't',
            x_label_pos = 'end',
            y_label = 'N',
            y_label_pos = 'end',
            location = (9, -2.5, 0), #(6.5, -2.5, 0),
            centered = True,
            arrows = True,
            scale = 0.6,
            high_res_curve_indices = [0, 1, 2]
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
            name = 'blob1_sim',
            location = [0, -2.5, 0],
            scale = 0.4,
            #appear_frame = cues['ntgraph']['start'] + 180,
            start_delay = start_delay,
            frames_per_time_step = frames_per_time_step,
            #save = True,
            load = 'ro_not_extinction',
            sim_duration = sim_duration,
            initial_creatures = initial_creatures,
            gene_updates = [
                ['color', 'creature_color_1', 'birth_modifier', 0, 0],
                ['shape', 'shape1', 'birth_modifier', 0, 0],
                ['size', '1', 'birth_modifier', 0, 0],
                ['color', 'creature_color_1', 'mutation_chance', 0, 0],
                ['shape', 'shape1', 'mutation_chance', 0, 0],
                ['size', '1', 'mutation_chance', 0, 0],
                ['color', 'creature_color_1', 'death_modifier', 200, 0],
                ['color', 'creature_color_1', 'replication_modifier', 300, 0],
            ],
            pauses = [
                [0, 1]
            ]
        )
        rhs.morph_figure(2, start_time = cues['ntgraph']['start'])
        equation.move_to(
            start_time = cues['ntgraph']['start'],
            new_location = (0, 5, 0),
            new_scale = 1.5,
        )
        graph.move_to(
            start_time = cues['ntgraph']['start'],
            new_scale = 0.6,
            new_location = (-10, -2.5, 0)
        )
        graph2.add_to_blender(appear_time = cues['ntgraph']['start'])

        sim.add_to_blender(appear_time = cues['ntgraph']['start'])
        """graph2.move_to(
            start_frame = cues['ntgraph']['start'] + 180,
            new_scale = 0.6,
            new_location = (9, -2.5, 0)
        )"""
        """func = sim.get_creature_count_by_t()
        print(func)
        graph2.add_new_function_and_curve(
            func,
            curve_mat_modifier = 'fade',
            z_shift = -0.05
        )"""

        #Predicted curve
        graph2.animate_function_curve(
            start_time = cues['ntgraph']['start'] + 0.5,
            end_time = cues['ntgraph']['start'] + 1.5,
            #uniform_along_x = True,
            index = 0
        )


        #Animate sim data and points
        data = sim.get_creature_count_by_t()
        print(data)
        graph2.add_new_function_and_curve(
            data,
            curve_mat_modifier = 'fade',
            z_shift = -0.05,
        )
        graph2.animate_function_curve(
            start_time = cues['ntgraph']['start'] + 2,
            end_time = cues['ntgraph']['start'] + 7,
            uniform_along_x = True,
            index = 1
        )
        #nt graph highlight point
        appear_coord2 = [0, data[0], 0]
        point2 = graph2.add_point_at_coord(
            coord = appear_coord2,
            appear_time = cues['ntgraph']['start'] + 1.5,
            axis_projections = True,
            track_curve = 1
        )
        graph2.animate_point(
            end_coord = [20, 0, 0],
            start_time = cues['ntgraph']['start'] + 2,
            end_time = cues['ntgraph']['start'] + 7,
            point = point2
        )
        #delta graph highlight point
        appear_coord21 = [data[0], func2(data[0]), 0]
        point21 = graph.add_point_at_coord(
            coord = appear_coord21,
            appear_time = cues['ntgraph']['start'] + 1.5,
            axis_projections = True,
            track_curve = 1
        )
        graph.multi_animate_point(
            start_time = cues['ntgraph']['start'] + 2,
            #end_time = cues['ntgraph']['start'] + 480,
            point = point21,
            frames_per_time_step = frames_per_time_step,
            x_of_t = data, #Not func2. This uses the sim data to inform movements
        )

        sim.disappear(
            disappear_time = cues['ntgraph']['start'] + 7.5 + 1/60,
            #animate = False
        )
        #point 21 shoots off and an arrow appears
        point21.disappear(disappear_time = cues['ntgraph']['start'] + 5)
        point21.axis_projections[0].disappear(disappear_time = cues['ntgraph']['start'] + 5)
        point21.axis_projections[1].disappear(disappear_time = cues['ntgraph']['start'] + 5)
        zoom_arrow = gesture.Gesture(
            gesture_series = [
                {
                    'type' : 'arrow',
                    'points' : {
                        'head' : [-6, -5/6, 0],
                        'tail' : [-8, -1.5, 0],
                    }
                }
            ],
            color = 'color2'
        )
        zoom_arrow.add_to_blender(appear_time = cues['ntgraph']['start'] + 4.5)

        #point 2 disappears after
        point2.disappear(disappear_time = cues['ntgraph']['start'] + 7.5)
        point2.axis_projections[0].disappear(disappear_time = cues['ntgraph']['start'] + 7.5)
        point2.axis_projections[1].disappear(disappear_time = cues['ntgraph']['start'] + 7.5)
        zoom_arrow.disappear(disappear_time = cues['ntgraph']['start'] + 7.5)

        #Second sim
        sim2 = drawn_world.DrawnWorld(
            name = 'blob1_sim',
            location = [0, -2.5, 0],
            scale = 0.4,
            #appear_frame = cues['ntgraph']['start'] + 180,
            start_delay = 0.5,
            frames_per_time_step = frames_per_time_step,
            #save = True,
            load = 'ro_extinction',
            sim_duration = sim_duration,
            initial_creatures = initial_creatures,
            gene_updates = [
                ['color', 'creature_color_1', 'birth_modifier', 0, 0],
                ['shape', 'shape1', 'birth_modifier', 0, 0],
                ['size', '1', 'birth_modifier', 0, 0],
                ['color', 'creature_color_1', 'mutation_chance', 0, 0],
                ['shape', 'shape1', 'mutation_chance', 0, 0],
                ['size', '1', 'mutation_chance', 0, 0],
                ['color', 'creature_color_1', 'death_modifier', 200, 0],
                ['color', 'creature_color_1', 'replication_modifier', 300, 0],
            ] #LIES
        )
        sim2.add_to_blender(
            appear_time = cues['ntgraph']['start'] + 7.5,
            #animate = False
        )

        data2 = sim2.get_creature_count_by_t()
        print(data2)
        graph2.add_new_function_and_curve(
            data2,
            curve_mat_modifier = 'fade',
            z_shift = -0.05,
        )
        graph2.animate_function_curve(
            start_time = cues['ntgraph']['start'] + 8,
            end_time = cues['ntgraph']['start'] + 13,
            uniform_along_x = True,
            index = 2
        )
        #nt graph highlight point
        appear_coord3 = [0, data2[0], 0]
        point3 = graph2.add_point_at_coord(
            coord = appear_coord3,
            appear_time = cues['ntgraph']['start'] + 7.5,
            axis_projections = True,
            track_curve = 2
        )
        graph2.animate_point(
            end_coord = [20, 0, 0],
            start_time = cues['ntgraph']['start'] + 8,
            end_time = cues['ntgraph']['start'] + 13,
            point = point3
        )
        #delta graph highlight point
        appear_coord31 = [data2[0], func2(data2[0]), 0]
        point31 = graph.add_point_at_coord(
            coord = appear_coord31,
            appear_time = cues['ntgraph']['start'] + 7.5,
            axis_projections = True,
            track_curve = 1
        )
        graph.multi_animate_point(
            start_time = cues['ntgraph']['start'] + 8,
            #end_time = cues['ntgraph']['start'] + 480,
            point = point31,
            frames_per_time_step = frames_per_time_step,
            x_of_t = data2, #Not func2. This uses the sim data to inform movements
        )

        point3.disappear(disappear_time = cues['ntgraph']['start'] + 13.5)
        point3.axis_projections[0].disappear(disappear_time = cues['ntgraph']['start'] + 13.5)
        point3.axis_projections[1].disappear(disappear_time = cues['ntgraph']['start'] + 13.5)
        point31.disappear(disappear_time = cues['ntgraph']['start'] + 13.5)
        point31.axis_projections[0].disappear(disappear_time = cues['ntgraph']['start'] + 13.5)
        point31.axis_projections[1].disappear(disappear_time = cues['ntgraph']['start'] + 13.5)

        #data = sim.get_creature_count_by_t()
        #graph2.add_new_function_and_curve(data)

        """graph2.animate_function_curve(
            start_time = cues['ntgraph']['start'] + 240,
            end_time = cues['ntgraph']['start'] + 540,
            uniform_along_x = True,
            index = 1
        )
        appear_coord2 = [0, data[0], 0]
        point2 = graph2.add_point_at_coord(
            coord = appear_coord2,
            appear_time = cues['ntgraph']['start'] + 180,
            axis_projections = True,
            track_curve = 1
        )
        graph2.animate_point(
            end_coord = [100, 0, 0],
            start_time = cues['ntgraph']['start'] + 240,
            end_time = cues['ntgraph']['start'] + 540,
            point = point2
        )"""
        #Many sims
        if RENDER_QUALITY == 'high':
            num_sims = 40
        else:
            num_sims = 1
        for i in range(num_sims):
            sim.simulate()
            func = sim.get_creature_count_by_t()
            #print(func)
            graph2.add_new_function_and_curve(
                func,
                curve_mat_modifier = 'fade',
                z_shift = -0.05
            )
        graph2.animate_all_function_curves(
            start_time = cues['ntgraph']['start'] + 14,
            end_time = cues['ntgraph']['start'] + 19,
            start_window = 0.5,
            uniform_along_x = True,
            skip = 3
        )

        """spread = gesture.Gesture(
            gesture_series = [
                {
                    'type': 'bracket',
                    'points': {
                        'annotation_point': (11.5, -1, 0),
                        'left_point': (10.5, 2, 0),
                        'right_point': (10.5, -4, 0)
                    }
                }
            ]
        )
        spread.add_to_blender(
            appear_time = cues['ntgraph']['start'] + 23
        )"""

        #Prep for next scene
        to_disappear = [equation, graph, sim2, graph2]
        for thing in to_disappear:
            thing.disappear(disappear_time = cues['ntgraph']['end'])
'''

Is there smoother way to organize scene structure and timing?
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
  ever want to split a sim over several scenes, though.
