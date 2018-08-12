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

#'''
class LastVideoExp(Scene):
    def __init__(self):
        self.subscenes = collections.OrderedDict([
            ('last_video', {'duration': 12}),
            ('sim_summary', {'duration': 12}),
            ('quantitative', {'duration': 40}),
        ])
        super().__init__()

    def play(self):
        super().play()
        #self.subscenes
        #self.duration

        #self.last_video()
        #self.sim_summary()
        self.quantitative()

    def last_video(self):
        #Stretch goal: Make blobs look around in a more directed way

        cues = self.subscenes['last_video']

        sim_duration = 100
        start_delay = 0.5
        frames_per_time_step = 1

        initial_creature_count = 5
        initial_creatures = []
        for i in range(initial_creature_count):
            new_creature = creature.Creature(color = 'creature_color_4', shape = 'shape1')
            initial_creatures.append(new_creature)
        sim = drawn_world.DrawnWorld(
            name = 'limitless_sim',
            location = [-8, -2.5, 0],
            scale = 0.5,
            start_delay = start_delay,
            frames_per_time_step = frames_per_time_step,
            sim_duration = sim_duration,
            initial_creatures = initial_creatures,
            #save = True,
            load = 'o_exponential',
            gene_updates = [
                #Other alleles
                ['shape', 'shape1', 'birth_modifier', 1, 0],
                ['size', '1', 'birth_modifier', 1, 0],
                ['shape', 'shape1', 'mutation_chance', 0, 0],
                ['size', '1', 'mutation_chance', 0, 0],
                #Color 4
                ['color', 'creature_color_4', 'death_modifier', 10, 0],
                ['color', 'creature_color_4', 'replication_modifier', 40, 0],
                ['color', 'creature_color_4', 'mutation_chance', 0, 0],
            ]
        )
        #sim.add_to_blender(appear_time = cues['start'] + 1)

        graph1 = graph_bobject.GraphBobject(
            x_range = [0, sim_duration],
            y_range = [0, 60],
            tick_step = [50, 20],
            width = 15,
            height = 10,
            x_label = 't',
            x_label_pos = 'end',
            y_label = 'N',
            y_label_pos = 'end',
            location = (-4, -1, 0),
            centered = True,
            arrows = 'positive',
            high_res_curve_indices = [0, 1, 2, 3]
        )
        graph1.add_to_blender(appear_time = cues['start'] + 1)

        y_blob = import_object(
            'boerd_blob', 'creatures',
            location = [10, -1, 0],
            rotation_euler = [0, - math.pi / 6, 0],
            scale = 3,
            wiggle = True,
            cycle_length = cues['end'] * FRAME_RATE
        )
        y_blob.ref_obj.children[0].children[0].data.resolution = 0.05
        apply_material(y_blob.ref_obj.children[0].children[0], 'creature_color4')
        y_blob.add_to_blender(appear_time = cues['start'] + 1)

        y_blob.blob_wave(
            start_time = cues['start'] + 3,
            duration = 5,
            end_pause_duration = 2
        )

        func = sim.get_creature_count_by_t(color = 'creature_color_4')
        graph1.add_new_function_and_curve(func, color = 4)

        graph1.animate_function_curve(
            start_time = cues['start'] + 2,
            end_time = cues['start'] + 4,
            uniform_along_x = True,
            index = 0
        )

        initial_creature_count = 5
        initial_creatures = []
        for i in range(initial_creature_count):
            new_creature = creature.Creature(color = 'creature_color_4', shape = 'shape1')
            initial_creatures.append(new_creature)
        sim2 = drawn_world.DrawnWorld(
            name = 'limited_sim',
            location = [-8, -2.5, 0],
            scale = 0.5,
            start_delay = start_delay,
            frames_per_time_step = frames_per_time_step,
            sim_duration = 300,
            initial_creatures = initial_creatures,
            #save = True,
            load = 'o_logistic2',
            overlap_okay = True,
            gene_updates = [
                #Other alleles
                ['shape', 'shape1', 'birth_modifier', 1, 0],
                ['size', '1', 'birth_modifier', 1, 0],
                ['shape', 'shape1', 'mutation_chance', 0, 0],
                ['size', '1', 'mutation_chance', 0, 0],
                #Color 4
                ['color', 'creature_color_4', 'death_modifier', 10, 0],
                ['color', 'creature_color_4', 'replication_modifier', 40, 0],
                ['color', 'creature_color_4', 'mutation_chance', 0, 0],
            ]
        )
        #sim2.simulate()

        #sim.add_to_blender(appear_time = 1)

        graph2 = graph_bobject.GraphBobject(
            x_range = [0, 300],
            y_range = [0, 100],
            tick_step = [100, 50],
            width = 15,
            height = 10,
            x_label = 't',
            x_label_pos = 'end',
            y_label = 'N',
            y_label_pos = 'end',
            location = (-4, -1, 0),
            centered = True,
            arrows = 'positive',
            high_res_curve_indices = [0]
        )

        graph1.disappear(disappear_time = cues['start'] + 5)
        graph2.add_to_blender(appear_time = cues['start'] + 6)


        func = sim2.get_creature_count_by_t(color = 'creature_color_4')
        #print(len(func))
        #print(func)
        graph2.add_new_function_and_curve(func, color = 4)
        graph2.animate_function_curve(
            start_time = cues['start'] + 7,
            end_time = cues['start'] + 9,
            uniform_along_x = True
        )


        #Prep for next scene
        to_disappear = [y_blob, graph2]
        for i, thing in enumerate(to_disappear):
            thing.disappear(disappear_time = cues['end'] - (len(to_disappear) - 1 - i) * 0.05)

    def sim_summary(self):
        #Stretch goal: Make sim pause step by step

        cues = self.subscenes['sim_summary']

        sim_duration = 60
        start_delay = 0.5
        frames_per_time_step = 5

        initial_creature_count = 10
        initial_creatures = []
        for i in range(initial_creature_count):
            new_creature = creature.Creature(color = 'creature_color_1', shape = 'shape1')
            initial_creatures.append(new_creature)
        sim = drawn_world.DrawnWorld(
            name = 'plain_sim',
            location = [-7, 0, 0],
            scale = 0.6,
            start_delay = start_delay,
            frames_per_time_step = frames_per_time_step,
            sim_duration = sim_duration,
            initial_creatures = initial_creatures,
            #save = True,
            #load = 'o_exponential',
            gene_updates = [
                #Other alleles
                ['shape', 'shape1', 'birth_modifier', 1, 0],
                ['size', '1', 'birth_modifier', 1, 0],
                ['shape', 'shape1', 'mutation_chance', 0, 0],
                ['size', '1', 'mutation_chance', 0, 0],
                #Color 4
                ['color', 'creature_color_1', 'death_modifier', 18, 0],
                ['color', 'creature_color_1', 'replication_modifier', 20, 0],
                ['color', 'creature_color_1', 'mutation_chance', 0, 0],
            ]
        )
        sim.add_to_blender(appear_time = cues['start'] + 1)

        graph1 = graph_bobject.GraphBobject(
            x_range = [0, sim_duration],
            y_range = [0, 15],
            tick_step = [20, 5],
            width = 10,
            height = 10,
            x_label = 't',
            x_label_pos = 'end',
            y_label = 'N',
            y_label_pos = 'end',
            location = (7, -1, 0),
            centered = True,
            arrows = 'positive',
            high_res_curve_indices = [0, 1, 2, 3]
        )
        graph1.add_to_blender(appear_time = cues['start'] + 1)

        func = sim.get_creature_count_by_t(color = 'creature_color_1')
        graph1.add_new_function_and_curve(func)#, color = 4)

        graph1.animate_function_curve(
            start_time = cues['start'] + 1.5,
            end_time = cues['start'] + 1.5 + sim_duration * frames_per_time_step / FRAME_RATE,
            uniform_along_x = True,
            index = 0
        )

        #graph1.disappear(disappear_time = cues['start'] + 5)


        #Prep for next scene
        to_disappear = [sim, graph1]
        for i, thing in enumerate(to_disappear):
            thing.disappear(disappear_time = cues['end'] - (len(to_disappear) - 1 - i) * 0.05)

    def quantitative(self):
        cues = self.subscenes['quantitative']

        def make_equation():
            self.rhs1 = tex_bobject.TexBobject(
                "\\big(R-D\\big) \\times N",
                "\\big(R-D\\big) \\times N",
                "\\big(R-D\\big) \\times N",
                "\\big(R-D\\big) \\times N",
                "\\big(0.1-D\\big) \\times N",
                "\\big(0.1-0.05\\big) \\times N",
                centered = True
            )
            self.equals1 = tex_bobject.TexBobject(
                "\!=",
                centered = True
            )
            self.lhs1 = tex_bobject.TexBobject(
                "\\Delta",
                "\\Delta",
                "\\Delta",
                centered = True
            )
            self.equation1 = tex_complex.TexComplex(
                self.lhs1, self.equals1, self.rhs1,
                location = (0, 0, 0),
                scale = 2,
                centered = True
            )
            self.equation1.add_annotation(
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
                gest_scale = 0.7
            )
            self.equation1.add_annotation(
                targets = [
                    2, #tex_bobject
                    [
                        [0, 1, 1, None],  #form, first char, last char
                        [1, 1, 1],
                        [2, 1, 1],
                        [3, 1, 1],
                        [4, 1, 3, 'arrow'],
                        [5, 1, 3, 'arrow'],
                    ],
                ],
                labels = [
                    [],
                    ['\\text{Replication chance}', '\\text{per creature}'],
                    ['\\text{Replication chance}', '\\text{per creature}'],
                    ['\\text{Replication chance}', '\\text{per creature}'],
                    ['\\text{Replication chance}', '\\text{per creature}'],
                    ['\\text{Replication chance}', '\\text{per creature}'],
                ],
                alignment = 'bottom',
                gest_scale = 0.7
            )
            self.equation1.add_annotation(
                targets = [
                    2, #tex_bobject
                    [
                        [0, 3, 3, None],  #form, first char, last char
                        [1, 3, 3, None],
                        [2, 3, 3],
                        [3, 3, 3],
                        [4, 5, 5],
                        [5, 5, 8, 'arrow']
                    ],
                ],
                labels = [
                    [],
                    [],
                    ['\\text{Death chance}', '\\text{per creature}'],
                    ['\\text{Death chance}', '\\text{per creature}'],
                    ['\\text{Death chance}', '\\text{per creature}'],
                    ['\\text{Death chance}', '\\text{per creature}'],
                ],
                alignment = 'top',
                gest_scale = 0.7
            )
            self.equation1.add_annotation(
                targets = [
                    2, #tex_bobject
                    [
                        [0, 6, 6, None],  #form, first char, last char
                        [1, 6, 6, None],
                        [2, 6, 6, None],
                        [3, 6, 6],
                        [4, 8, 8],
                        [5, 11, 11]
                    ],
                ],
                labels = [
                    [],
                    [],
                    [],
                    ['\\text{Current number}', '\\text{of creatures}'],
                    ['\\text{Current number}', '\\text{of creatures}'],
                    ['\\text{Current number}', '\\text{of creatures}'],
                ],
                alignment = 'bottom',
                gest_scale = 0.7
            )

        def manipulate_equation():
            self.equation1.add_to_blender(appear_time = cues['start'])
            self.lhs1.morph_figure(1, start_time = cues['start'] + 2)
            self.rhs1.morph_figure(1, start_time = cues['start'] + 3)
            self.rhs1.morph_figure(2, start_time = cues['start'] + 4)
            self.rhs1.morph_figure(3, start_time = cues['start'] + 5)

            self.equation1.move_to(
                start_time = cues['start'] + 6,
                new_location = [-7, 0, 0],
                new_scale = 1.5
            )

            self.rhs1.morph_figure(4, start_time = cues['start'] + 7)
            self.rhs1.morph_figure(5, start_time = cues['start'] + 8)


            self.equation1.move_to(
                start_time = cues['start'] + 17,
                new_location = [-7, -2, 0]
            )

        #make_equation()
        #manipulate_equation()

        def func(x):
            return 0.05 * x

        dn_graph1 = graph_bobject.GraphBobject(
            func,
            x_range = [0, 40],
            y_range = [0, 1.5],
            tick_step = [5, 0.5],
            width = 10,
            height = 5,
            x_label = 'N',
            x_label_pos = 'end',
            y_label = '\\Delta',
            y_label_pos = 'end',
            location = (7, -1, 0),
            centered = True,
            arrows = True,
        )
        dn_graph1.add_to_blender(appear_time = cues['start'] + 6)

        #Moved these to manipulate_equation
        '''rhs1.morph_figure(4, start_time = cues['start'] + 7)
        rhs1.morph_figure(5, start_time = cues['start'] + 8)'''

        dn_graph1.animate_function_curve(
            start_time = cues['start'] + 8,
            end_time = cues['start'] + 9
        )


        appear_coord = [5, 0.25, 0]
        point = dn_graph1.add_point_at_coord(
            coord = appear_coord,
            appear_time = cues['start'] + 9,
            axis_projections = True,
            track_curve = 0
        )

        x_of_t = []
        #    [0, 5.25],
        #    [1, 5.25 * (1.05)],
        #    [2, 5.25 * (1.05) ** 2],
        #    [3, 5.25 * (1.05) ** 3]
        for x in range(20):
            dn_graph1.animate_point(
                point = point,
                start_time = cues['start'] + 10 + x / 8,
                end_time = cues['start'] + 10.0625 + x / 8,
                end_coord = [5.25 * 1.05 ** x]
            )

        dn_graph1.move_to(
            start_time = cues['start'] + 14,
            new_location = [7, 3.5, 0],
            #new_scale = 0.67
        )
        point.disappear(disappear_time = cues['start'] + 14)
        point.axis_projections[0].disappear(disappear_time = cues['start'] + 14)
        point.axis_projections[1].disappear(disappear_time = cues['start'] + 14)

        start = 5
        r = 0.05
        def func(x):
            return start * (1 + r) ** x
        cap = 40
        def func2(x):
            return start * cap / (start + (cap - start) * math.exp(-r*x))

        nt_graph1 = graph_bobject.GraphBobject(
            func,
            func2,
            x_range = [0, 70],
            y_range = [0, 100],
            tick_step = [10, 20],
            width = 10,
            height = 5,
            x_label = 't',
            x_label_pos = 'end',
            y_label = 'N',
            y_label_pos = 'end',
            location = (7, -4.5, 0),
            centered = True,
            arrows = True,
            #scale = 0.67
        )
        nt_graph1.add_to_blender(appear_time = cues['start'] + 14)

        nt_graph1.animate_function_curve(
            start_time = cues['start'] + 15,
            end_time = cues['start'] + 16
        )

        #Moved to manipulate_equation
        '''equation1.move_to(
            start_time = cues['start'] + 17,
            new_location = [-7, -2, 0]
        )'''

        label = tex_bobject.TexBobject(
            '\\text{Unlimited growth}',
            '\\text{Limited growth?}',
            scale = 2,
            location = [-14.5, 6, 0]
        )
        label.add_to_blender(appear_time = cues['start'] + 17)

        label.morph_figure(1, start_time = cues['start'] + 18)

        cam_bobj = bobject.Bobject(location = CAMERA_LOCATION)
        cam_bobj.add_to_blender(appear_time = 0)
        cam_obj = bpy.data.objects['Camera']
        cam_obj.location = [0, 0, 0]
        cam_obj.parent = cam_bobj.ref_obj

        cam_bobj.move_to(
            new_location = [7.7, -3.7, 15.3],
            start_time = cues['start'] + 20,
            end_time = cues['start'] + 20.5
        )
        '''cam_bobj.move_to(
            new_location = CAMERA_LOCATION,
            start_time = cues['green_stats']['start'] + 27,
            end_time = cues['green_stats']['start'] + 28
        )'''

        #nt_graph1.morph_curve(1, start_time = cues['start'] + 21)
        nt_graph1.active_function_index = 1
        nt_graph1.change_window(
            start_time = cues['start'] + 21,
            new_x_range = [0, 120],
            new_y_range = [0, 40],
            new_tick_step = [20, 20]
        )

        nt_graph1.highlight_region(
            start_time = cues['start'] + 22,
            end_time = cues['start'] + 24,
            x_region = [0, 40],
            y_region = [0, 40]
        )


        #Prep for next scene
        to_disappear = [
            #self.equation1,
            dn_graph1,
            nt_graph1
        ]
        for i, thing in enumerate(to_disappear):
            thing.disappear(disappear_time = cues['end'] - (len(to_disappear) - 1 - i) * 0.05)

#'''
