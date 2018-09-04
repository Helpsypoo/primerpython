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

class LastVideoExp(Scene):
    def __init__(self):
        self.subscenes = collections.OrderedDict([
            ('pre_transplant', {'duration': 10}),
            ('post_transplant', {'duration': 10}),\
        ])
        super().__init__()

    def play(self):
        super().play()
        #self.subscenes
        #self.duration

        self.pre_transplant()

    def pre_transplant(self):
        #Stretch goal: Make blobs look around in a more directed way

        cues = self.subscenes['pre_transplant']

        sim_duration = 500
        start_delay = 0.5
        frames_per_time_step = 1

        #initial_creature_count = 10
        blue_count = 20
        red_count = 10
        initial_creatures = []
        for i in range(blue_count):
            new_creature = creature.Creature(
                color = 'creature_color_1',
                shape = 'shape1',
                size = '0.5'
            )
            initial_creatures.append(new_creature)
        for i in range(red_count):
            new_creature = creature.Creature(
                color = 'creature_color_3',
                shape = 'shape1',
                size = '0.5'
            )
            initial_creatures.append(new_creature)
        sim = drawn_world.DrawnWorld(
            name = 'limited_sim',
            location = [0, 0, 0],
            scale = 0.7,
            start_delay = start_delay,
            frames_per_time_step = frames_per_time_step,
            sim_duration = sim_duration,
            initial_creatures = initial_creatures,
            creature_model = ['bacteria', 'biochem'],
            #save = True,
            #load = 'o_logistic2',
            overlap_okay = True,
            gene_updates = [
                #Other alleles
                ['shape', 'shape1', 'birth_modifier', 1, 0],
                ['size', '1', 'birth_modifier', 1, 0],
                ['shape', 'shape1', 'mutation_chance', 0, 0],
                ['size', '1', 'mutation_chance', 0, 0],
                #Color 1
                ['color', 'creature_color_1', 'death_modifier', 0, 0],
                ['color', 'creature_color_1', 'replication_modifier', 0, 0],
                ['color', 'creature_color_1', 'mutation_chance', 0, 0],
                #Color 3
                ['color', 'creature_color_3', 'death_modifier', 0, 0],
                ['color', 'creature_color_3', 'replication_modifier', 0, 0],
                ['color', 'creature_color_3', 'mutation_chance', 0, 0],
            ],
            world_bound_points = [
                #Test coords
                #[-10, 10, 0],
                #[10, 10, 0],
                #[10, -10, 0],
                #[0, -10, 0],
                #[0, 0, 0],
                #[-10, 0, 0],
                #Intestine-like shape
                [-10, 10, 0],
                [10, 10, 0],
                [10, -8, 0],
                [2, -8, 0],
                [2, -10, 0],
                [-2, -10, 0],
                [-2, -6, 0],
                [8, -6, 0],
                [8, 8, 0],
                [-8, 8, 0],
                [-8, -8, 0],
                [-10, -10, 0],
                #[0, 0, 0],
            ],
            bound_mode = 'points',
            show_world = False
        )

        sim.add_to_blender(appear_time = 1)

        #Prep for next scene
        to_disappear = []
        for i, thing in enumerate(to_disappear):
            thing.disappear(disappear_time = cues['end'] - (len(to_disappear) - 1 - i) * 0.05)



        print()
        points = [
            [2, 0, 0],
            [0, 0, 0],
            [-0.1, 0.5, 0],
            [-0.4594877792145916, -5.443530545247961, 0.0],
            [-5.066866886029154, -4.334055768904699, 0],
            [5, 4, 0]
        ]
        for point in points:
            print(sim.is_point_in_bounds(point))
            print()
        print()
