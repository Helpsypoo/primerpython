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
            ('quantitative', {'duration': 100}),
            ('competition', {'duration': 100}),
            ('take_stock', {'duration': 100}),
        ])
        super().__init__()

    def play(self):
        super().play()
        #self.subscenes
        #self.duration

        #self.last_video()
        #self.sim_summary()
        #self.quantitative()
        #self.competition()
        self.take_stock()

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
        #Stretch goal. Make blobs sad about starving
        cues = self.subscenes['quantitative']

        def make_equation():
            plug_Ns = []
            delta_outs = []
            for i in range(0, 51):
                Nstring = "\\big(0.1-0.05 - 0.001" + str(i) + "\\big)" + str(i)
                delta_string = str(( 0.5 - 0.001 * i) * i)

            self.rhs1 = tex_bobject.TexBobject(
                "\\big(R-D\\big)\\times N",
                "\\big(R-D\\big)\\times N",
                "\\big(R-D\\big)\\times N",
                "\\big(R-D\\big)\\times N",
                "\\big(0.1-D\\big)\\times N",
                "\\big(0.1-0.05\\big)\\times N",
                "\\big(0.1-0.05\\big)\\times 0",
                "\\big(0.1-0.05\\big)\\times 50",
                "\\big(0.1-0.05\\big)\\times N",
                "\\big(0.1-0.05 + \\substack{\\text{Crowding} \\\\ \\text{Term}}\\big)\\times N",
                "\\big(0.1-0.05 - C\\times N\\big)\\times N",
                "\\big(0.1-0.05 - 0.001\\times N\\big)\\times N",
                "\\big(0.1-0.05 - 0.001\\times 0\\big)\\times 0",
                "\\big(0.1-0.05 - 0.001\\times 50\\big)\\times 50",
                "\\big(R - D - C\\times N\\big)\\times N",
                centered = True
            )
            self.equals1 = tex_bobject.TexBobject(
                "\!=",
                "\\neq",
                "\!=",
                centered = True
            )
            self.lhs1 = tex_bobject.TexBobject(
                "\\Delta",
                "\\Delta",
                "0",
                "\\Delta",
                str('{0:.2f}'.format(0)),
                "\\Delta",
                centered = True
            )
            self.equation1 = tex_complex.TexComplex(
                self.lhs1, self.equals1, self.rhs1,
                location = (0, 0, 0),
                scale = 2,
                centered = True
            )

            annotations = True
            if annotations == True:
                self.equation1.add_annotation(
                    targets = [
                        0, #tex_bobject
                        [
                            [0, 0, 0, None],  #form, first char, last char
                            [1, 0, 0],
                            [2, 0, 0],
                            [3, 0, 0],
                            [4, 0, 3, 'arrow'],
                            [5, 0, 0],
                        ],
                    ],
                    labels = [
                        [],
                        ['\\text{Total}', '\\text{expected}', '\\text{change}'],
                        ['\\text{Total}', '\\text{expected}', '\\text{change}'],
                        ['\\text{Total}', '\\text{expected}', '\\text{change}'],
                        ['\\text{Total}', '\\text{expected}', '\\text{change}'],
                        ['\\text{Total}', '\\text{expected}', '\\text{change}'],
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
                            [6, 1, 3, 'arrow'],
                            [7, 1, 3, 'arrow'],
                            [8, 1, 3, 'arrow'],
                            [9, 1, 3, 'arrow'],
                            [10, 1, 3, 'arrow'],
                            [11, 1, 3, 'arrow'],
                            [12, 1, 3, 'arrow'],
                            [13, 1, 3, 'arrow'],
                            [14, 1, 1, 'arrow'],
                        ],
                    ],
                    labels = [
                        [],
                        ['\\text{Replication chance}', '\\text{per creature}'],
                        ['\\text{Replication chance}', '\\text{per creature}'],
                        ['\\text{Replication chance}', '\\text{per creature}'],
                        ['\\text{Replication chance}', '\\text{per creature}'],
                        ['\\text{Replication chance}', '\\text{per creature}'],
                        ['\\text{Replication chance}', '\\text{per creature}'],
                        ['\\text{Replication chance}', '\\text{per creature}'],
                        ['\\text{Replication chance}', '\\text{per creature}'],
                        ['\\text{Replication chance}', '\\text{per creature}'],
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
                            [5, 5, 8, 'arrow'],
                            [6, 5, 8, 'arrow'],
                            [7, 5, 8, 'arrow'],
                            [8, 5, 8, 'arrow'],
                            [9, 5, 8, 'arrow'],
                            [10, 5, 8, 'arrow'],
                            [11, 4, 16],
                            [12, 4, 16],
                            [13, 4, 17],
                            [14, 2, 7],
                        ],
                    ],
                    labels = [
                        [],
                        [],
                        ['\\text{Death chance}', '\\text{per creature}'],
                        ['\\text{Death chance}', '\\text{per creature}'],
                        ['\\text{Death chance}', '\\text{per creature}'],
                        ['\\text{Death chance}', '\\text{per creature}'],
                        ['\\text{Death chance}', '\\text{per creature}'],
                        ['\\text{Death chance}', '\\text{per creature}'],
                        ['\\text{Death chance}', '\\text{per creature}'],
                        ['\\text{Death chance}', '\\text{per creature}'],
                        ['\\text{Death chance}', '\\text{per creature}'],
                        ['\\text{Death chance}', '\\text{per creature}',
                            '\\text{adjusted for}', '\\text{crowding}'],
                        ['\\text{Death chance}', '\\text{per creature}',
                            '\\text{adjusted for}', '\\text{crowding}'],
                        ['\\text{Death chance}', '\\text{per creature}',
                            '\\text{adjusted for}', '\\text{crowding}'],
                        ['\\text{Death chance}', '\\text{per creature}',
                            '\\text{adjusted for}', '\\text{crowding}'],
                    ],
                    alignment = 'top',
                    gest_scale = 0.7,
                    angle = [-3 * math.pi / 12] * 9 + [0] * 6
                )
                self.equation1.add_annotation(
                    targets = [
                        2, #tex_bobject
                        [
                            [0, 0, 0, None],  #form, first char, last char
                            [1, 0, 0, None],
                            [2, 0, 0, None],
                            [3, 0, 0, None],
                            [4, 0, 0, None],
                            [5, 0, 0, None],
                            [6, 0, 0, None],
                            [7, 0, 0, None],
                            [8, 0, 0, None],
                            [9, 10, 10, None],
                            [10, 10, 10, 'arrow'],
                            [11, 10, 14, 'arrow'],
                            [12, 10, 14, 'arrow'],
                            [13, 10, 14, 'arrow'],
                            [14, 6, 6, 'arrow'],
                        ],
                    ],
                    labels = [
                        [],
                        [],
                        [],
                        [],
                        [],
                        [],
                        [],
                        [],
                        [],
                        [],
                        ['\\text{\"Crowding \phantom{bleh}}', '\\text{coefficient\"}'],
                        ['\\text{\"Crowding \phantom{bleh}}', '\\text{coefficient\"}'],
                        ['\\text{\"Crowding \phantom{bleh}}', '\\text{coefficient\"}'],
                        ['\\text{\"Crowding \phantom{bleh}}', '\\text{coefficient\"}'],
                        ['\\text{\"Crowding \phantom{bleh}}', '\\text{coefficient\"}'],
                    ],
                    alignment = 'bottom',
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
                            [5, 11, 11],
                            [6, 11, 11],
                            [7, 11, 12, 'arrow'],
                            [8, 11, 11],
                            [9, 24, 24],
                            [10, 14, 14],
                            [11, 19, 19],
                            [12, 19, 19],
                            [13, 20, 21, 'arrow'],
                            [14, 10, 10, 'arrow'],
                        ],
                    ],
                    labels = [
                        [],
                        [],
                        [],
                        ['\\text{Current number}', '\\text{of creatures}'],
                        ['\\text{Current number}', '\\text{of creatures}'],
                        ['\\text{Current number}', '\\text{of creatures}'],
                        ['\\text{Current number}', '\\text{of creatures}'],
                        ['\\text{Current number}', '\\text{of creatures}'],
                        ['\\text{Current number}', '\\text{of creatures}'],
                        ['\\text{Current number}', '\\text{of creatures}'],
                        ['\\text{Current number}', '\\text{of creatures}'],
                        ['\\text{Current number}', '\\text{of creatures}'],
                        ['\\text{Current number}', '\\text{of creatures}'],
                        ['\\text{Current number}', '\\text{of creatures}'],
                        ['\\text{Current number}', '\\text{of creatures}'],
                    ],
                    alignment = 'top',
                    gest_scale = 0.7,
                    #angle = [math.pi / 12] * 9 + [0] * 5
                )

            plug_stuff_in = True
            if plug_stuff_in == True:
                #For showing a range of inputs and outputs
                #Need a new set of objects to make transitions instant, which is
                #necessary for fast transistions
                plug_Ns = []
                delta_outs = []
                self.num_states = 51
                for i in range(0, self.num_states):
                    Nstring = "\\big(0.1-0.05 - 0.001\\times" + str(i) + "\\big) \\times" + str(i)
                    plug_Ns.append(Nstring)
                    delta = (0.05 - 0.001 * i) * i
                    delta_string = str('{0:.2f}'.format(delta))
                    delta_outs.append(delta_string)

                self.rhs2 = tex_bobject.TexBobject(
                    *plug_Ns,
                    transition_type = 'instant',
                    centered = True
                )
                self.equals2 = tex_bobject.TexBobject(
                    "\!=",
                    transition_type = 'instant',
                    centered = True
                )
                self.lhs2 = tex_bobject.TexBobject(
                    *delta_outs,
                    transition_type = 'instant',
                    centered = True
                )
                self.equation2 = tex_complex.TexComplex(
                    self.lhs2, self.equals2, self.rhs2,
                    location = (-7, -2, 0),
                    scale = 0.95,
                    centered = True
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

            self.rhs1.morph_figure(6, start_time = cues['start'] + 38)
            self.lhs1.morph_figure(2, start_time = cues['start'] + 38)

            self.rhs1.morph_figure(7, start_time = cues['start'] + 39)
            self.equals1.morph_figure(1, start_time = cues['start'] + 39)

            self.rhs1.morph_figure(8, start_time = cues['start'] + 40)
            self.equals1.morph_figure(2, start_time = cues['start'] + 40)
            self.lhs1.morph_figure(3, start_time = cues['start'] + 40)

            self.rhs1.morph_figure(9, start_time = cues['start'] + 41)
            self.equation1.move_to(
                new_scale = 0.95,
                start_time = cues['start'] + 41
            )
            #c_term = []
            for i in range (9, 22):
                #c_term.append(self.rhs1.lookup_table[8][i])
                self.rhs1.lookup_table[9][i].color_shift(
                    color = COLORS_SCALED[1],
                    start_time = cues['start'] + 41,
                    duration_time = 1
                )

            self.rhs1.morph_figure(10, start_time = cues['start'] + 42)
            for i in range (9, 13):
                #c_term.append(self.rhs1.lookup_table[8][i])
                self.rhs1.lookup_table[10][i].color_shift(
                    color = COLORS_SCALED[1],
                    start_time = cues['start'] + 42,
                    duration_time = 1
                )
            for N in [self.rhs1.lookup_table[10][12], self.rhs1.lookup_table[10][15]]:
                #Shrink
                N.pulse(
                    start_time = cues['start'] + 43,
                    factor = 0.7,
                    duration_time = 1
                )
                #Grow
                N.pulse(
                    start_time = cues['start'] + 44,
                    duration_time = 1
                )

            self.rhs1.morph_figure(11, start_time = cues['start'] + 45)
            for i in range (9, 17):
                #c_term.append(self.rhs1.lookup_table[8][i])
                self.rhs1.lookup_table[11][i].color_shift(
                    color = COLORS_SCALED[1],
                    start_time = cues['start'] + 45,
                    duration_time = None #permanent
                )

            self.rhs1.morph_figure(12, start_time = cues['start'] + 46)
            self.lhs1.morph_figure(4, start_time = cues['start'] + 46)

            for part in self.equation1.tex_bobjects:
                hide_self_and_descendants(
                    part.ref_obj,
                    keyframes = True,
                    frame = (cues['start'] + 48) * FRAME_RATE
                )
                #part.disappear(disappear_time = cues['start'] + 48, animate = False)
            self.equation2.add_to_blender(appear_time = cues['start'] + 48, animate = False)
            for j in range(9, 16):
                self.rhs2.lookup_table[0][j].color_shift(
                    start_time = 0,
                    duration_time = None,
                    color = COLORS_SCALED[1]
                )

            for i in range(1, self.num_states):
                #print("Number" + str(i))
                if i == 10:
                    arrange_super = True
                    self.rhs1.morph_figure(13, start_time = cues['start'] + 49 + i * 0.05)
                else: arrange_super = False

                if i >= 10:
                    end = 18
                else:
                    end = 17
                for j in range(9, end):
                    self.rhs2.lookup_table[i][j].color_shift(
                        start_time = 0,
                        duration_time = None,
                        color = COLORS_SCALED[1]
                    )

                self.rhs2.morph_figure(
                    i,
                    start_time = cues['start'] + 49 + i * 0.05,
                    arrange_super = arrange_super
                )
                self.lhs2.morph_figure(
                    i,
                    start_time = cues['start'] + 49 + i * 0.05,
                    arrange_super = False
                )

            for part in self.equation1.tex_bobjects:
                hide_self_and_descendants(
                    part.ref_obj,
                    hide = False,
                    keyframes = True,
                    frame = (cues['start'] + 52) * FRAME_RATE
                )
            for j in range(9, 17):
                self.rhs1.lookup_table[13][j].color_shift(
                    start_time = cues['start'] + 52,
                    duration_time = 2,
                    color = COLORS_SCALED[1]
                )


            for part in self.equation2.tex_bobjects:
                hide_self_and_descendants(
                    part.ref_obj,
                    keyframes = True,
                    frame = (cues['start'] + 52) * FRAME_RATE
                )
                #part.disappear(disappear_time = cues['start'] + 52, animate = False)
            #self.equation2.disappear(disappear_time = cues['start'] + 52, animate = False)

            self.rhs1.morph_figure(14, start_time = cues['start'] + 53)
            self.lhs1.morph_figure(5, start_time = cues['start'] + 53)
            for j in range(2, 8):
                self.rhs1.lookup_table[14][j].color_shift(
                    start_time = cues['start'] + 53,
                    duration_time = None,
                    color = COLORS_SCALED[1]
                )
            #Re-yellowify the last char, because it's still white from before, I guess
            self.rhs1.lookup_table[14][10].color_shift(
                start_time = cues['start'] + 53,
                duration_time = None,
                color = COLORS_SCALED[1]
            )
            self.equation1.move_to(
                new_scale = 1.1,
                start_time = cues['start'] + 53,
            )

            #End plug_in range thing

            #Pulse N along with graph highlighing
            """for N in [self.rhs1.lookup_table[14][7], self.rhs1.lookup_table[14][10]]:
                #Shrink
                N.pulse(
                    start_time = cues['start'] + 43,
                    factor = 0.7,
                    duration_time = 1
                )
                #Grow
                N.pulse(
                    start_time = cues['start'] + 44,
                    duration_time = 1
                )"""

            #End manipulate_equation()
            ##############################################################

        """##################"""
        #make_equation()
        #manipulate_equation()
        """##################"""

        def func(x):
            return 0.05 * x

        def func2(x):
            return (0.05 - 0.001 * x) * x

        dn_graph1 = graph_bobject.GraphBobject(
            func,
            func2,
            x_range = [0, 53],
            y_range = [0, 2],
            tick_step = [10, 0.5],
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
        cap = 50
        def func2(x):
            return start * cap / (start + (cap - start) * math.exp(-r*x))

        nt_graph1 = graph_bobject.GraphBobject(
            func,
            func2,
            x_range = [0, 70],
            y_range = [0, 100],
            tick_step = [10, 25],
            width = 10,
            height = 5,
            x_label = 't',
            x_label_pos = 'end',
            y_label = 'N',
            y_label_pos = 'end',
            location = (7, -4.5, 0),
            centered = True,
            arrows = True,
            #scale = 0.67,
            #high_res_curve_indices = [0, 1, 2]
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
            '\\text{Limited growth}',
            scale = 2,
            location = [-14.5, 6, 0]
        )
        label.add_to_blender(appear_time = cues['start'] + 17)
        label.morph_figure(1, start_time = cues['start'] + 18)
        label.morph_figure(2, start_time = cues['start'] + 42)

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
            new_y_range = [0, 50],
            new_tick_step = [20, 25]
        )

        nt_graph1.highlight_region(
            start_time = cues['start'] + 22,
            end_time = cues['start'] + 24,
            x_region = [0, 40],
            y_region = [0, 55]
        )
        nt_graph1.highlight_region(
            start_time = cues['start'] + 24,
            end_time = cues['start'] + 26,
            x_region = [80, 120],
            y_region = [0, 55]
        )

        cam_bobj.move_to(
            new_location = [7.7, 0.3, 32.8],
            start_time = cues['start'] + 27,
            end_time = cues['start'] + 27.5
        )

        cam_bobj.move_to(
            new_location = [7.7, 4.3, 15.3],
            start_time = cues['start'] + 27.5,
            end_time = cues['start'] + 28
        )

        dn_graph1.y_label_bobject.subbobjects[0].pulse(
            start_time = cues['start'] + 29
        )
        dn_graph1.y_label_bobject.subbobjects[0].color_shift(
            start_time = cues['start'] + 29
        )

        #dn_graph1.morph_curve(1, start_time = cues['start'] + 31)
        dn_graph1.active_function_index = 1
        dn_graph1.change_window(
            start_time = cues['start'] + 32,
            #new_x_range = [0, 120],
            new_y_range = [0, 0.7],
            #new_tick_step = [20, 20]
        )

        point = dn_graph1.add_point_at_coord(
            coord = [50, 0, 0],
            appear_time = cues['start'] + 33,
            axis_projections = True,
            #track_curve = 0
        )
        point.pulse(start_time = cues['start'] + 34, duration_time = 1)
        point.pulse(start_time = cues['start'] + 35, duration_time = 1)
        point.disappear(disappear_time = cues['start'] + 36)

        #Move camera to equation
        cam_bobj.move_to(
            new_location = CAMERA_LOCATION,
            start_time = cues['start'] + 36,
            end_time = cues['start'] + 36.5
        )

        #Animate point moving along curve while equation passes through values
        point = dn_graph1.add_point_at_coord(
            coord = [0, 0, 0],
            appear_time = cues['start'] + 48,
            axis_projections = True,
            track_curve = 1
        )
        dn_graph1.animate_point(
            point = point,
            start_time = cues['start'] + 49,
            end_time = cues['start'] + 51.5,
            end_coord = [50, 0, 0],
            track_curve = True
        )
        #point.disappear(disappear_time = cues['start'] + 53)

        carry_cap = tex_bobject.TexBobject(
            '\\text{"Carrying capacity"}',
            scale = 1,
            location = [10, -0.75, 0],
            centered = True,
            color = 'color2'
        )
        arrow_scale = 0.8
        cap_arrow = gesture.Gesture(
            gesture_series = [
                {
                    'type': 'arrow',
                    'points': {
                        'tail': (10 / arrow_scale, -0.25 / arrow_scale, 0),
                        'head': (10.4 / arrow_scale, 1 / arrow_scale, 0)
                    }
                }
            ],
            color = 'color2',
            scale = arrow_scale
        )
        cap_arrow2 = gesture.Gesture(
            gesture_series = [
                {
                    'type': 'arrow',
                    'points': {
                        'tail': (8 / arrow_scale, -1.6 / arrow_scale, 0),
                        'head': (7.5 / arrow_scale, -2.8 / arrow_scale, 0)
                    }
                }
            ],
            color = 'color2',
            scale = arrow_scale
        )

        cap_line = import_object('one_side_cylinder', 'primitives', name = 'cap_line')
        apply_material(cap_line.objects[0], 'color2')
        ref = cap_line.ref_obj
        ref.location = [
            0, #nt_graph1.x_range[1] * nt_graph1.domain_scale_factor,
            nt_graph1.y_range[1] * nt_graph1.range_scale_factor,
            0
        ]
        ref.children[0].rotation_euler = (0, math.pi / 2, 0)
        ref.children[0].scale = [
            AXIS_DEPTH / 4,
            AXIS_DEPTH / 4,
            nt_graph1.x_range[1] * nt_graph1.domain_scale_factor / 2,
        ]
        ref.parent = nt_graph1.ref_obj

        cap_stuff = [carry_cap, cap_arrow, cap_arrow2, cap_line]
        for thing in cap_stuff:
            thing.add_to_blender(appear_time = cues['start'] + 54)


        dn_graph1.animate_point(
            point = point,
            start_time = cues['start'] + 54,
            end_time = cues['start'] + 55,
            end_coord = [0, 0, 0],
            track_curve = True
        )
        #Highlight regions for discussion
        #Low
        dn_graph1.highlight_region(
            start_time = cues['start'] + 55,
            end_time = cues['start'] + 57,
            x_region = [0, 16.7],
            y_region = [0, 0.8]
        )
        nt_graph1.highlight_region(
            start_time = cues['start'] + 55,
            end_time = cues['start'] + 57,
            x_region = [0, 120],
            y_region = [0, 16.7],
            highlight_direction = 'y'
        )
        dn_graph1.animate_point(
            point = point,
            start_time = cues['start'] + 55.5,
            end_time = cues['start'] + 56.5,
            end_coord = [16.7, 0, 0],
            track_curve = True
        )

        #Middle
        dn_graph1.highlight_region(
            start_time = cues['start'] + 57,
            end_time = cues['start'] + 59,
            x_region = [16.7, 33.3],
            y_region = [0, 0.8]
        )
        nt_graph1.highlight_region(
            start_time = cues['start'] + 57,
            end_time = cues['start'] + 59,
            x_region = [0, 120],
            y_region = [16.7, 33.3],
            highlight_direction = 'y'
        )
        dn_graph1.animate_point(
            point = point,
            start_time = cues['start'] + 57.5,
            end_time = cues['start'] + 58.5,
            end_coord = [33.3, 0, 0],
            track_curve = True
        )

        #Middle
        dn_graph1.highlight_region(
            start_time = cues['start'] + 59,
            end_time = cues['start'] + 61,
            x_region = [33.3, 50],
            y_region = [0, 0.8]
        )
        nt_graph1.highlight_region(
            start_time = cues['start'] + 59,
            end_time = cues['start'] + 61,
            x_region = [0, 120],
            y_region = [33.3, 50],
            highlight_direction = 'y'
        )
        dn_graph1.animate_point(
            point = point,
            start_time = cues['start'] + 59.5,
            end_time = cues['start'] + 60.5,
            end_coord = [50, 0, 0],
            track_curve = True
        )

        #Above equilibrium
        dn_graph1.animate_point(
            point = point,
            start_time = cues['start'] + 62,
            end_time = cues['start'] + 62.5,
            end_coord = [53, 0, 0],
            track_curve = True
        )
        dn_graph1.animate_point(
            point = point,
            start_time = cues['start'] + 63,
            end_time = cues['start'] + 63.5,
            end_coord = [50, 0, 0],
            track_curve = True
        )

        #point.disappear(disappear_time = cues['start'] + 65)
        #Back to zero
        dn_graph1.animate_point(
            point = point,
            start_time = cues['start'] + 63,
            end_time = cues['start'] + 63.5,
            end_coord = [0, 0, 0],
            track_curve = True
        )


        #Prep for next scene
        to_disappear = cap_stuff + [
            #self.equation1,
            #label,
            #dn_graph1,
            #nt_graph1
        ]
        for i, thing in enumerate(to_disappear):
            thing.disappear(disappear_time = cues['start'] + 67 - (len(to_disappear) - 1 - i) * 0.05)

        start_delay = 0.5
        frames_per_time_step = 5
        sim_duration = 120
        initial_creature_count = 5
        initial_creatures = []
        for i in range(initial_creature_count):
            new_creature = creature.Creature(color = 'creature_color_1', shape = 'shape1')
            initial_creatures.append(new_creature)
        sim = drawn_world.DrawnWorld(
            name = 'plain_sim',
            location = [-7, -1.75, 0],
            scale = 0.55,
            start_delay = start_delay,
            frames_per_time_step = frames_per_time_step,
            sim_duration = sim_duration,
            initial_creatures = initial_creatures,
            #save = True,
            load = 'b_logistic',
            gene_updates = [
                #Other alleles
                ['shape', 'shape1', 'birth_modifier', 1, 0],
                ['size', '1', 'birth_modifier', 1, 0],
                ['shape', 'shape1', 'mutation_chance', 0, 0],
                ['size', '1', 'mutation_chance', 0, 0],
                #Color 1
                ['color', 'creature_color_1', 'replication_modifier', 100, 0],
                ['color', 'creature_color_1', 'death_modifier', 50, 0],
                ['color', 'creature_color_1', 'mutation_chance', 0, 0],
            ]
        )
        sim.add_to_blender(appear_time = cues['start'] + 68)

        func = sim.get_creature_count_by_t(color = 'creature_color_1')
        nt_graph1.add_new_function_and_curve(
            func,
            color = 3,
            curve_mat_modifier = 'fade',
            z_shift = -0.05
        )

        nt_graph1.animate_function_curve(
            start_time = cues['start'] + 68 + start_delay,
            end_time = cues['start'] + 68 + start_delay + sim_duration * frames_per_time_step / FRAME_RATE,
            uniform_along_x = True,
            index = 1
        )

        dn_graph1.multi_animate_point(
            x_of_t = func,
            frames_per_time_step = frames_per_time_step,
            point = point,
            start_time = cues['start'] + 68 + start_delay,
            #end_time = cues['start'] + 63.5,
        )

        #Many sims
        if RENDER_QUALITY == 'high':
            num_sims = 40
        else:
            num_sims = 40
        for i in range(num_sims):
            sim.simulate()
            func = sim.get_creature_count_by_t()
            #print(func)
            nt_graph1.add_new_function_and_curve(
                func,
                curve_mat_modifier = 'fade',
                z_shift = -0.05
            )
        nt_graph1.animate_all_function_curves(
            start_time = cues['start'] + 81,
            end_time = cues['start'] + 86,
            start_window = 0.5,
            uniform_along_x = True,
            skip = 2
        )

    def competition(self):
        #Stretch goal. Make blobs sad about starving
        cues = self.subscenes['competition']
        scene_end = cues['duration']

        def make():
            self.b_blob = import_object(
                'boerd_blob', 'creatures',
                location = [0, 0, 0],
                scale = 3,
                wiggle = True,
                cycle_length = scene_end * FRAME_RATE
            )
            self.b_blob.ref_obj.children[0].children[0].data.resolution = 0.2
            apply_material(self.b_blob.ref_obj.children[0].children[0], 'creature_color3')


            #blue stats
            self.b_rep_chance = tex_bobject.TexBobject(
                'R = 10\%'
            )
            self.b_death_chance = tex_bobject.TexBobject(
                'D = 5\%'
            )
            self.b_stats = tex_complex.TexComplex(
                self.b_rep_chance, self.b_death_chance,
                multiline = True,
                line_height = 1.2,
                location = [2 / self.b_blob.ref_obj.scale[0], 0, 0],
                scale = 1.5 / self.b_blob.ref_obj.scale[0]
            )
            self.b_stats.ref_obj.parent = self.b_blob.ref_obj

            self.g_arrow = gesture.Gesture(
                gesture_series = [
                    {
                        'type': 'arrow',
                        'points': {
                            'tail': (-2.5 / 1.6, 0 / 1.6, 0),
                            'head': (2.5 / 1.6, 0 / 1.6, 0)
                        }
                    },
                    {
                        'type': 'arrow',
                        'points': {
                            'tail': (-2.5 / 1.6, 1.5 / 1.6, 0),
                            'head': (2.5 / 1.6, 3 / 1.6, 0)
                        }
                    }
                ],
                scale = 1.6,
                color = 'color2'
            )

            self.g_blob = import_object(
                'boerd_blob', 'creatures',
                location = [5.5, 0, 0],
                scale = 3,
                wiggle = True,
                cycle_length = scene_end * FRAME_RATE
            )
            self.g_blob.ref_obj.children[0].children[0].data.resolution = 0.2
            apply_material(self.g_blob.ref_obj.children[0].children[0], 'creature_color7')

            self.g_death_chance = tex_bobject.TexBobject(
                'D = 5\%'
            )
            self.g_rep_chance = tex_bobject.TexBobject(
                'R = 8\%'
            )
            self.g_stats = tex_complex.TexComplex(
                self.g_rep_chance, self.g_death_chance,
                multiline = True,
                line_height = 1.2,
                location = [2 / self.g_blob.ref_obj.scale[0], 0, 0],
                scale = 1.5 / self.g_blob.ref_obj.scale[0]
            )
            self.g_stats.ref_obj.parent = self.g_blob.ref_obj

            self.o_arrow = gesture.Gesture(
                gesture_series = [
                    {
                        'type': 'arrow',
                        'points': {
                            'tail': (-2.5 / 1.6, -1.5 / 1.6, 0),
                            'head': (2.5 / 1.6, -3 / 1.6, 0)
                        }
                    },
                ],
                scale = 1.6,
                color = 'color2'
            )

            self.o_blob = import_object(
                'boerd_blob', 'creatures',
                location = [5.5, -4, 0],
                scale = 3,
                wiggle = True,
                cycle_length = scene_end * FRAME_RATE
            )
            self.o_blob.ref_obj.children[0].children[0].data.resolution = 0.2
            apply_material(self.o_blob.ref_obj.children[0].children[0], 'creature_color4')

            self.o_death_chance = tex_bobject.TexBobject(
                'D = 3\%'
            )
            self.o_rep_chance = tex_bobject.TexBobject(
                'R = 10\%'
            )
            self.o_stats = tex_complex.TexComplex(
                self.o_rep_chance, self.o_death_chance,
                multiline = True,
                line_height = 1.2,
                location = [2 / self.o_blob.ref_obj.scale[0], 0, 0],
                scale = 1.5 / self.o_blob.ref_obj.scale[0]
            )
            self.o_stats.ref_obj.parent = self.o_blob.ref_obj
        def manipulate():
            self.b_blob.add_to_blender(appear_time = cues['start'])
            self.b_stats.add_to_blender(
                appear_time = cues['start'],
                #subbobject_timing = [0, 60, 120, ],
            )

            self.b_blob.move_to(
                start_time = cues['start'] + 1.5,
                new_location = [-11, 0, 0],
            )
            self.g_arrow.add_to_blender(appear_time = cues['start'] + 10.5)
            self.g_blob.add_to_blender(appear_time = cues['start'] + 10.5)
            self.g_stats.add_to_blender(
                appear_time = cues['start'] + 10.5,
                #subbobject_timing = [0, 60, 120, ],
            )
            self.g_rep_chance.pulse(
                start_time = cues['start'] + 12.5
            )

            self.g_blob.move_to(
                new_location = [5.5, 4, 0],
                start_time = cues['start'] + 16.5
            )
            self.g_arrow.morph_figure(1, start_time = cues['start'] + 16.5)
            self.o_arrow.add_to_blender(appear_time = cues['start'] + 16.5)
            self.o_blob.add_to_blender(appear_time = cues['start'] + 16.5)
            self.o_stats.add_to_blender(
                appear_time = cues['start'] + 16.5,
            )
            self.o_death_chance.pulse(
                start_time = cues['start'] + 19.5
            )

            to_disappear = [
                self.b_blob,
                self.g_blob,
                self.g_arrow,
                self.o_blob,
                self.o_arrow
            ]
            for i, thing in enumerate(to_disappear):
                thing.disappear(disappear_time = cues['end'] - (len(to_disappear) - 1 - i) * 0.05)
        def sim():
            start_delay = 0.5
            frames_per_time_step = 1
            sim_duration = 500
            initial_creature_count = 5
            initial_creatures = []
            for i in range(initial_creature_count):
                new_creature = creature.Creature(color = 'creature_color_1', shape = 'shape1')
                initial_creatures.append(new_creature)
            mutation_chance = 0.01
            sim = drawn_world.DrawnWorld(
                name = 'sim',
                location = [-8.5, 0, 0],
                scale = 0.55,
                start_delay = start_delay,
                frames_per_time_step = frames_per_time_step,
                sim_duration = sim_duration,
                initial_creatures = initial_creatures,
                #save = True,
                load = 'competition_best4',
                gene_updates = [
                    #Other alleles
                    ['shape', 'shape1', 'birth_modifier', 1, 0],
                    ['size', '1', 'birth_modifier', 1, 0],
                    ['shape', 'shape1', 'mutation_chance', 0, 0],
                    ['size', '1', 'mutation_chance', 0, 0],
                    #Color 1
                    ['color', 'creature_color_1', 'replication_modifier', 70, 0],
                    ['color', 'creature_color_1', 'death_modifier', 20, 0],
                    ['color', 'creature_color_1', 'mutation_chance', [0, mutation_chance, 0, mutation_chance], 0],
                    #Color 2
                    ['color', 'creature_color_2', 'replication_modifier', 50, 0],
                    ['color', 'creature_color_2', 'death_modifier', 20, 0],
                    ['color', 'creature_color_2', 'mutation_chance', 0, 0],
                    #Color 4
                    ['color', 'creature_color_4', 'replication_modifier', 70, 0],
                    ['color', 'creature_color_4', 'death_modifier', 0, 0],
                    ['color', 'creature_color_4', 'mutation_chance', 0, 0],
                ]
            )
            sim.add_to_blender(appear_time = cues['start'] + 68)

            func = sim.get_creature_count_by_t(color = 'creature_color_1')
            graph = graph_bobject.GraphBobject(
                func,
                x_range = [0, sim_duration],
                y_range = [0, 50],
                tick_step = [int(sim_duration / 5), 25],
                width = 14,
                height = 10,
                x_label = 't',
                x_label_pos = 'end',
                y_label = 'N',
                y_label_pos = 'end',
                location = (5.5, -0.5, 0),
                centered = True,
                arrows = True,
                #scale = 0.67,
                high_res_curve_indices = [0, 1, 2, 3]
            )
            graph.add_to_blender(appear_time = cues['start'] + 68)

            func2 = sim.get_creature_count_by_t(color = 'creature_color_2')
            func3 = sim.get_creature_count_by_t(color = 'creature_color_4')
            func4 = sim.get_creature_count_by_t()
            graph.add_new_function_and_curve(
                func2,
                color = 7
            )
            graph.add_new_function_and_curve(
                func3,
                color = 4
            )
            '''graph.add_new_function_and_curve(
                func4,
                color = 2,
                #curve_mat_modifier = 'fade',
                z_shift = -0.05
            )'''

            for i in range(len(graph.functions_curves)):
                graph.animate_function_curve(
                    start_time = cues['start'] + 68 + start_delay,
                    end_time = cues['start'] + 68 + start_delay + frames_per_time_step * sim_duration / FRAME_RATE,
                    index = i,
                    uniform_along_x = True
                )

        '''#################'''
        make()
        manipulate()
        sim()
        '''#################'''

    def take_stock(self):
        cues = self.subscenes['take_stock']
        scene_end = cues['duration']

        rep = tex_bobject.TexBobject(
            '\\text{Replication}',
            location = [-13, 5, 0],
            scale = 3
        )
        def rep_graph():
            pass

        rep_graph()

        mut = tex_bobject.TexBobject(
            '\\text{Mutation}',
            location = [-13, 0, 0],
            scale = 3
        )
        com = tex_bobject.TexBobject(
            '\\text{Competition}',
            location = [-13, -5, 0],
            scale = 3
        )



        for thing in [rep, mut, com]:
            thing.add_to_blender(appear_time = cues['start'])
#'''
