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
#'''
#'''
class ThereWillBeGraphs(Scene):
    def __init__(self):
        self.subscenes = collections.OrderedDict([
            ('sim', {'duration': 240})
        ])
        super().__init__()

    def play(self):
        super().play()
        cues = self.subscenes
        scene_end = self.duration


#'''
