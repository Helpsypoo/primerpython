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
#'''
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
            centered = True
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




        bracket = svg_bobject.SVGFromBlend(['bracket', 'svgblend'])
        bracket.add_to_blender(appear_frame = 0)


#'''
