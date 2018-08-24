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
            ('last_video', {'duration': 100}),
            ('poop', {'duration': 100}),\
        ])
        super().__init__()

    def play(self):
        super().play()
        #self.subscenes
        #self.duration

        self.nonpoop()

    def nonpoop(self):
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
