import sys
import os
import imp
import bpy
import mathutils
import math
import pickle
from copy import deepcopy
from random import random, uniform
import collections

import drawn_world
import tex_bobject
import constants
import creature

#import alone doesn't check for changes in cached files
imp.reload(drawn_world)
imp.reload(tex_bobject)
from tex_bobject import *

imp.reload(creature)
from creature import *

imp.reload(constants)
from constants import *

import helpers
imp.reload(helpers)
from helpers import *

import bobject
imp.reload(bobject)
from bobject import *

import graph_bobject
imp.reload(graph_bobject)

import scene
imp.reload(scene)
from scene import Scene

'''
inspect.getmembers is used in draw_scenes.py to get all these classes, then
the scenes are put into blender one after another.
After setting it up this way, I realized that very often, scenes take too much
memory in blender for it to make sense to run more than one at a time. So I just
comment out all but the one I'm working on or want to run.
'''

'''
class IntroImage(Scene):
    def __init__(self):
        super().__init__()
        #self.equation_duration = 340

        self.subscenes = collections.OrderedDict([
            ('logo', {'duration': 240})
        ])

        total_duration = 0
        for sub, attrs in self.subscenes.items():
            total_duration += attrs['duration']

        self.duration = total_duration

    def set_subscene_timing(self, frame):
        start = frame
        for sub, attrs in self.subscenes.items():
            attrs['start'] = start
            attrs['end'] = start + attrs['duration']
            start = attrs['end']

    def play_from_frame(self, frame):
        #super().play_from_frame(frame)

        #Define flow
        self.set_subscene_timing(frame)
        cues = self.subscenes
        #equation_start = frame
        #equation_end = equation_start + self.equation_duration

        scene_end = frame + self.duration

        #tex_bobject isn't really meant for svgs.
        #Might want to broaden the class
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
        #stroke.ref_obj.location[2] = -1
        logo.morph_chains[0][0].ref_obj.location[2] = -1
        logo.add_to_blender(
            appear_frame = cues['logo']['start'],
            #subbobject_timing = [90, 30, 40, 50, 60, 70, 80],
            subbobject_timing = [42, 30, 33, 36, 39, 42, 45],
            animate = True
        )
        logo.disappear(disappear_frame = scene_end)
        #logo2.disappear(disappear_frame = scene_end)
        #text.disappear(disappear_frame = scene_end)

        bobj = import_object('boerd_blob_squat', 'creatures', scale = 2)
        bobj.ref_obj.children[0].children[2].data.resolution = 0.1
        bobj.add_to_blender(
            appear_frame = cues['logo']['start'],
        )
        apply_material(
            bobj.ref_obj,
            'creature_color4',
            recursive = True,
            type_req = 'META'
        )

        bobj.disappear(disappear_frame = scene_end)
'''
'''
class BlobMotivation(Scene):
    def __init__(self):
        super().__init__()
        #self.equation_duration = 340

        self.subscenes = collections.OrderedDict([
            ('blob', {'duration': 120})
        ])

        total_duration = 0
        for sub, attrs in self.subscenes.items():
            total_duration += attrs['duration']

        self.duration = total_duration

    def set_subscene_timing(self, frame):
        start = frame
        for sub, attrs in self.subscenes.items():
            attrs['start'] = start
            attrs['end'] = start + attrs['duration']
            start = attrs['end']

    def play_from_frame(self, frame):
        #super().play_from_frame(frame)

        #Define flow
        self.set_subscene_timing(frame)
        cues = self.subscenes
        #equation_start = frame
        #equation_end = equation_start + self.equation_duration

        scene_end = frame + self.duration

        bobj = import_object('boerd_blob', 'creatures', scale = 2)
        bobj.ref_obj.children[0].children[2].data.resolution = 0.1
        bobj.add_to_blender(
            appear_frame = frame,
        )
        apply_material(
            bobj.ref_obj,
            'creature_color3',
            recursive = True,
            type_req = 'META'
        )

        bobj.disappear(disappear_frame = scene_end)
'''
'''
class MostBioCourses(Scene):
    def __init__(self):
        super().__init__()
        #self.equation_duration = 340

        self.subscenes = collections.OrderedDict([
            ('wait', {'duration': 0}),
            ('morph', {'duration': 660}),
            ('wait2', {'duration': 0}),
        ])

        total_duration = 0
        for sub, attrs in self.subscenes.items():
            total_duration += attrs['duration']

        self.duration = total_duration

    def set_subscene_timing(self, frame):
        start = frame
        for sub, attrs in self.subscenes.items():
            attrs['start'] = start
            attrs['end'] = start + attrs['duration']
            start = attrs['end']

    def play_from_frame(self, frame):
        #super().play_from_frame(frame)
        #Define flow
        self.set_subscene_timing(frame)
        cues = self.subscenes
        #equation_start = frame
        #equation_end = equation_start + self.equation_duration

        scene_end = frame + self.duration

        bobj = bobject.MeshMorphBobject(scale = 1, name = 'morphing_object')
        bobj.add_subbobject_to_series(import_object('H2O', 'biochem', scale = 6))
        bobj.series[0].ref_obj.location = (0, -1.5, 0)
        bobj.add_subbobject_to_series(import_object('sucrose', 'biochem', scale = 1.2))
        bobj.series[1].ref_obj.location = (0, 0.5, -1)
        bobj.add_subbobject_to_series(import_object('bacteria', 'biochem', scale = 4))

        bobj.add_to_blender(
            appear_frame = cues['morph']['start']
        )
        bobj.morph_bobject(
            0, 1,
            cues['morph']['start'] + 120,
            cues['morph']['start'] + 120 + DEFAULT_MORPH_TIME
        )
        bobj.morph_bobject(
            1, 2,
            cues['morph']['start'] + 300,
            cues['morph']['start'] + 300 + DEFAULT_MORPH_TIME
        )

        ##Spiiiiiiiin
        bobj.ref_obj.rotation_euler = (0, 0, 0)
        bobj.ref_obj.keyframe_insert(data_path="rotation_euler", frame = cues['morph']['start'])
        bobj.ref_obj.rotation_euler = (0, 3*math.pi, 0)
        bobj.ref_obj.keyframe_insert(data_path="rotation_euler", frame = cues['morph']['end'])

        bobj.disappear(disappear_frame = cues['morph']['end'])
'''
''' Placeholder
class WeStartWithEvolution(Scene):
    def __init__(self):
        super().__init__()
        #self.equation_duration = 340

        self.subscenes = collections.OrderedDict([
            ('evolution_why', {'duration': 540}),
            ('sims_math', {'duration': 780}),
        ])

        total_duration = 0
        for sub, attrs in self.subscenes.items():
            total_duration += attrs['duration']

        self.duration = total_duration

    def set_subscene_timing(self, frame):
        start = frame
        for sub, attrs in self.subscenes.items():
            attrs['start'] = start
            attrs['end'] = start + attrs['duration']
            start = attrs['end']

    def play_from_frame(self, frame):
        self.set_subscene_timing(frame)
        cues = self.subscenes
        scene_end = frame + self.duration

        evo = tex_bobject.TexBobject(
            '\\text{Evolution}',
            scale = 3,
            centered = True
        )

        why_evo = tex_bobject.TexBobject(
            '\\text{Why?}',
            '\\text{Evolution}',
            location = (0, -12, 0),
            scale = 3,
            centered = True
        )

        """blob = import_object(
            'boerd_blob',
            'creatures',
            location = (0, -12, 0),
            scale = 4
        )"""
        eqn = tex_bobject.TexBobject(
            'N = \dfrac{B}{D}',
            'N = \dfrac{B}{D-R}',
            'N = \dfrac{B}{D-R} \\rightarrow \\infty',
            location = (6, -2, 0),
            centered = True
        )

        initial_creature_count = 10
        initial_creatures = []
        for i in range(initial_creature_count):
            new_creature = creature.Creature()
            initial_creatures.append(new_creature)
        blob_sim = drawn_world.DrawnWorld(
            name = 'blob_sim',
            location = [0, -2.5, 0],
            scale = 0.6,
            appear_frame = cues['sims_math']['start'] + 60,
            start_delay = 60,
            #save = True,
            load = 'wte_intro',
            duration = scene_end - cues['sims_math']['start'],
            initial_creatures = initial_creatures,
            gene_updates = [
                ['shape', 'shape1', 'birth_modifier', 1, 0],
                ['size', '1', 'birth_modifier', 1, 0],
                ['color', 'creature_color_1', 'birth_modifier', 100, 0],
                ['color', 'creature_color_1', 'death_modifier', 10, 0],
                ['color', 'creature_color_1', 'replication_modifier', 0, 0],
                ['color', 'creature_color_1', 'replication_modifier', 15, 120],
            ],
            counter_alignment = 'top_left'
        )



        #Add to blender and manipulate

        ###evolution_why
        evo.add_to_blender(appear_frame = cues['evolution_why']['start'] + 105)
        why_evo.add_to_blender(appear_frame = cues['evolution_why']['start'] + 105)

        evo.move_to(
            new_location = (0, 12, 0),
            start_frame = cues['evolution_why']['start'] + 240
        )
        why_evo.move_to(
            new_location = (0, 0, 0),
            start_frame = cues['evolution_why']['start'] + 240
        )
        why_evo.morph_figure(1, start_frame = cues['evolution_why']['start'] + 435)

        ###sims and math
        #blob.add_to_blender(appear_frame = cues['sims_math']['start'])
        why_evo.move_to(
            new_location = (0, 5, 0),
            start_frame = cues['sims_math']['start'] + 60
        )
        blob_sim.add_to_blender(
            appear_frame = cues['sims_math']['start'] + 60
        )


        #Math appears
        blob_sim.move_to(
            new_location = (-6, -2.5, 0),
            start_frame = cues['sims_math']['start'] + 240
        )
        eqn.add_to_blender(
            appear_frame = cues['sims_math']['start'] + 240
        )
        eqn.morph_figure(1, start_frame = cues['sims_math']['start'] + 300)
        eqn.morph_figure(2, start_frame = cues['sims_math']['start'] + 360)

        remaining = [why_evo, blob_sim, eqn]
        for bobj in remaining:
            bobj.disappear(disappear_frame = scene_end)
'''
'''
class RaindropsAndPlanets(Scene):
    def __init__(self):
        super().__init__()
        self.blank = 0
        self.things_duration = 1470
        self.raindrops_duration = 900
        self.planets_duration = 1080
        self.end_duration = 540

        total_duration = self.blank + \
                         self.things_duration + \
                         self.raindrops_duration + \
                         self.planets_duration + \
                         self.end_duration

        self.duration = total_duration

    def play_from_frame(self, frame):
        #Define flow
        things_start = frame + self.blank
        things_end = things_start + self.things_duration
        raindrops_start = things_end
        raindrops_end = raindrops_start + self.raindrops_duration
        planets_start = raindrops_end
        planets_end = planets_start + self.planets_duration
        end_start = planets_end
        end_end = end_start + self.end_duration

        scene_end = frame + self.duration

        #Create python-side objects
        whydo = tex_bobject.TexBobject(
            "\\text{Why do}",
            name = "Why Do",
            centered = True
        )
        things = tex_bobject.TexBobject(
            "\\text{things}",
            "\\text{raindrops}",
            "\\text{planets}",
            "\\text{things}",
            name = "things",
            centered = True
        )
        exist = tex_bobject.TexBobject(
            "\\text{exist?}",
            name = "exist",
            centered = True
        )
        text = bobject.TexComplex(
            whydo, things, exist,
            name = 'Why do things exist',
            location = (0, 0.5, 0),
            scale = 2.5,
            centered = True
        )

        birth_text = tex_bobject.TexBobject(
            "1. \\text{ They started existing}",
            "1. \\text{ They were born}",
            scale = 1.5,
            location = (-12, 0.5, 0),
            name = "Birth"
        )
        death_text = tex_bobject.TexBobject(
            "2. \\text{ They haven't stopped existing}",
            "2. \\text{ They haven't died}",
            scale = 1.5,
            location = (-12, -3, 0),
            name = "Death"
        )

        ##Things
        text.add_to_blender(
            appear_frame = things_start,
            animate = False
        )
        text.move_to(
            start_frame = things_start + 60,
            new_location = (0, 5, 0)
        )
        birth_text.add_to_blender(appear_frame = things_start + 450)
        birth_text.morph_figure(1, start_frame = things_start + 630)
        death_text.add_to_blender(appear_frame = things_start + 840)
        death_text.morph_figure(1, start_frame = things_start + 990)
        birth_text.move_to(
            new_location = (-9, 0.5, 0),
            start_frame = things_start + 1050
        )
        death_text.move_to(
            new_location = (-9, -3, 0),
            start_frame = things_start + 1050
        )
        #birth_text.disappear(disappear_frame = raindrops_start)
        #death_text.disappear(disappear_frame = raindrops_start)



        ##Rain
        """text.move_to(
            new_location = (0, 0.5, 0),
            new_scale = 2,
            start_frame = raindrops_start
        )"""



        things.morph_figure(1, start_frame = raindrops_start)
        text.move_to(
            start_frame = raindrops_start,
            new_scale = text.ref_obj.scale[0] * 0.9
        )
        rain = bobject.RainBobject(
            start_raining = raindrops_start + 60 + OBJECT_APPEARANCE_TIME,
            stop_raining = raindrops_end,
            name = 'rain'
        )
        collision_bobjects = whydo.subbobjects + \
                            things.subbobjects + \
                            whydo.subbobjects + \
                            birth_text.subbobjects + \
                            death_text.subbobjects

        rain.add_collision_objects(
            collision_bobjects,
            text = True,
            frame = raindrops_start + 60 + DEFAULT_MORPH_TIME)
        rain.add_to_blender(
            appear_frame = raindrops_start + 60 + OBJECT_APPEARANCE_TIME,
            animate = False
        )
        birth_text.pulse(
            frame = raindrops_start + 240,
            duration = raindrops_end - raindrops_start - 240
        )
        #Some fiddly stuff to make the pulse not look like displacement
        loc = birth_text.ref_obj.location
        birth_text.move_to(
            start_frame = raindrops_start + 240,
            end_frame = raindrops_start + 240 + OBJECT_APPEARANCE_TIME / 2,
            new_location = [loc[0] - 0.2, loc[1], loc[2]]
        )
        birth_text.move_to(
            start_frame = raindrops_end - OBJECT_APPEARANCE_TIME / 2,
            end_frame = raindrops_end,
            new_location = [loc[0] + 0.2, loc[1], loc[2]]
        )
        death_text.pulse(
            frame = raindrops_start + 390,
            duration = raindrops_end - raindrops_start - 390,
            factor = 0.8
        )
        loc = death_text.ref_obj.location
        death_text.move_to(
            start_frame = raindrops_start + 390,
            end_frame = raindrops_start + 390 + OBJECT_APPEARANCE_TIME / 2,
            new_location = [loc[0] + 0.2, loc[1], loc[2]]
        )
        death_text.move_to(
            start_frame = raindrops_end - OBJECT_APPEARANCE_TIME / 2,
            end_frame = raindrops_end,
            new_location = [loc[0] - 0.2, loc[1], loc[2]]
        )
        rain.disappear(disappear_frame = raindrops_end, animate = False)


        ##Planets
        things.morph_figure(2, start_frame = planets_start)
        text.arrange_tex_bobjects(
            start_frame = planets_start,
            end_frame = planets_start + DEFAULT_MORPH_TIME
        )

        birth_text.pulse(
            frame = planets_start + 210,
            duration = planets_end - planets_start - 210,
            factor = 0.8
        )
        #Some fiddly stuff to make the pulse not look like displacement
        loc = birth_text.ref_obj.location
        birth_text.move_to(
            start_frame = planets_start + 210,
            end_frame = planets_start + 210 + OBJECT_APPEARANCE_TIME / 2,
            new_location = [loc[0] + 0.2, loc[1], loc[2]]
        )
        birth_text.move_to(
            start_frame = planets_end - OBJECT_APPEARANCE_TIME / 2,
            end_frame = planets_end,
            new_location = [loc[0] - 0.2, loc[1], loc[2]]
        )
        death_text.pulse(
            frame = planets_start + 420,
            duration = planets_end - planets_start - 420
        )
        loc = death_text.ref_obj.location
        death_text.move_to(
            start_frame = planets_start + 420,
            end_frame = planets_start + 420 + OBJECT_APPEARANCE_TIME / 2,
            new_location = [loc[0] - 0.2, loc[1], loc[2]]
        )
        death_text.move_to(
            start_frame = planets_end - OBJECT_APPEARANCE_TIME / 2,
            end_frame = planets_end,
            new_location = [loc[0] + 0.2, loc[1], loc[2]]
        )




        world = bpy.context.scene.world
        nodes = world.node_tree.nodes
        nodes.new(type = 'ShaderNodeMixRGB')
        nodes.new(type = 'ShaderNodeTexImage')
        nodes.new(type = 'ShaderNodeTexCoord')

        path_mix_input = nodes[2].inputs[2]

        for l in world.node_tree.links:
            if l.to_socket == path_mix_input:
               world.node_tree.links.remove(l)

        world.node_tree.links.new(nodes[5].outputs[0], nodes[2].inputs[2])
        world.node_tree.links.new(nodes[4].outputs[0], nodes[5].inputs[1])
        world.node_tree.links.new(nodes[6].outputs[0], nodes[5].inputs[2])
        world.node_tree.links.new(nodes[7].outputs[5], nodes[6].inputs[0])

        stars_path = os.path.join(IMG_DIR, 'milky-way-and-starry-night-sky.jpg')
        try:
            img = bpy.data.images.load(stars_path)
        except:
            raise NameError("Cannot load image %s" % path)
        nodes[6].image = img

        nodes[5].inputs[0].default_value = 0


        #Keyframes for background transition
        nodes[4].outputs[0].keyframe_insert(data_path = 'default_value', frame = planets_start)
        nodes[4].outputs[0].default_value = (0, 0, 0, 1)
        nodes[4].outputs[0].keyframe_insert(data_path = 'default_value', frame = planets_start + 60)

        nodes[5].inputs[0].keyframe_insert(data_path = 'default_value', frame = planets_start + 60)
        nodes[5].inputs[0].default_value = 1
        nodes[5].inputs[0].keyframe_insert(data_path = 'default_value', frame = planets_start + 120)
        nodes[5].inputs[0].keyframe_insert(data_path = 'default_value', frame = planets_end - 90)
        nodes[5].inputs[0].default_value = 0
        nodes[5].inputs[0].keyframe_insert(data_path = 'default_value', frame = planets_end - 30)

        nodes[4].outputs[0].keyframe_insert(data_path = 'default_value', frame = planets_end - 30)
        nodes[4].outputs[0].default_value = COLORS_SCALED[0]
        nodes[4].outputs[0].keyframe_insert(data_path = 'default_value', frame = planets_end + 30)








        """background = world.node_tree.nodes["Background"].inputs[0]
        background.keyframe_insert(data_path = 'default_value', frame = planets_start)
        background.default_value = \
            (0, 0, 0, 1)
            #(0.477, 0.679215, 0.787412, 1)
        background.keyframe_insert(data_path = 'default_value', frame = planets_start + DEFAULT_MORPH_TIME)
        background.keyframe_insert(data_path = 'default_value', frame = scene_end)
        background.default_value = COLORS_SCALED[0]
        background.keyframe_insert(data_path = 'default_value', frame = scene_end + DEFAULT_SCENE_BUFFER)
        """

        planet_scale = 100
        earth = import_object(
            'earth', 'planets',
            location = (0, -115, -20),
            scale = planet_scale,
            name = 'earth'
        )
        earth.ref_obj.rotation_euler = (0, 0, math.pi / 2)
        earth.add_to_blender(
            appear_frame = planets_start,
            animate = True
        )
        earth.spiny(
            start_frame = planets_start,
            end_frame = scene_end,
            spin_rate = -1/20
        )

        #Make animations so far linear so earth doesn't change rotation speed
        for fc in earth.ref_obj.animation_data.action.fcurves:
            fc.extrapolation = 'LINEAR' # Set extrapolation type
            # Iterate over this fcurve's keyframes and set handles to vector
            for kp in fc.keyframe_points:
                kp.handle_left_type  = 'VECTOR'
                kp.handle_right_type = 'VECTOR'

        earth.move_to(
            new_location = (0, -105, -20),
            start_frame = planets_start,
            end_frame = planets_start + 60
        )

        """mars = import_object(
            'mars', 'planets',
            location = (-6, -5, 0),
            scale = planet_scale * 3397 / 6378,
            name = 'mars'
        )
        mars.add_to_blender(
            appear_frame = planets_start + 168,
            animate = True
        )
        mars.spiny(
            start_frame = planets_start + 168,
            end_frame = scene_end,
            spin_rate = -1440/1479
        )
        venus = import_object(
            'venus', 'planets',
            location = (7, -4, 0),
            scale = planet_scale * 6052 / 6378,
            name = 'venus'
        )
        venus.add_to_blender(
            appear_frame = planets_start + 240,
            animate = True
        )
        venus.spiny(
            start_frame = planets_start + 168,
            end_frame = scene_end,
            spin_rate = 1/242
        )
        jupiter = import_object(
            'jupiter', 'planets',
            location = (-9 * planet_scale, 8 * planet_scale, -20 * planet_scale),
            scale = planet_scale * 71492 / 6378,
            name = 'jupiter'
        )
        jupiter.add_to_blender(
            appear_frame = planets_start + 312,
            animate = True
        )
        jupiter.spiny(
            start_frame = planets_start + 312,
            end_frame = scene_end,
            spin_rate = -24/10
        )
        neptune = import_object(
            'neptune', 'planets',
            location = (11, 6, -30),
            scale = planet_scale * 24766 / 6378,
            name = 'neptune'
        )
        neptune.add_to_blender(
            appear_frame = planets_start + 384,
            animate = True
        )
        neptune.spiny(
            start_frame = planets_start + 384,
            end_frame = scene_end,
            spin_rate = -24/16
        )"""


        earth.disappear(disappear_frame = planets_end)
        #venus.disappear(disappear_frame = planets_end)
        #mars.disappear(disappear_frame = planets_end)
        #jupiter.disappear(disappear_frame = planets_end)
        #neptune.disappear(disappear_frame = planets_end)


        #End
        things.morph_figure(3, start_frame = end_start)

        birth_text.pulse(
            frame = end_start + 240,
            duration = 60,
            attack = 30,
            decay = 30
        )
        #Some fiddly stuff to make the pulse not look like displacement
        loc = birth_text.ref_obj.location
        birth_text.move_to(
            start_frame = end_start + 240,
            end_frame = end_start + 240 + 30,
            new_location = [loc[0] - 0.2, loc[1], loc[2]]
        )
        birth_text.move_to(
            start_frame = end_start + 240 + 30,
            end_frame = end_start + 240 + 30 + 30,
            new_location = [loc[0] + 0.2, loc[1], loc[2]]
        )

        death_text.pulse(
            frame = end_start + 270,
            duration = 60,
            attack = 30,
            decay = 30
        )
        #Some fiddly stuff to make the pulse not look like displacement
        loc = death_text.ref_obj.location
        death_text.move_to(
            start_frame = end_start + 270,
            end_frame = end_start + 270 + 30,
            new_location = [loc[0] - 0.2, loc[1], loc[2]]
        )
        death_text.move_to(
            start_frame = end_start + 270 + 30,
            end_frame = end_start + 270 + 30 + 30,
            new_location = [loc[0] + 0.2, loc[1], loc[2]]
        )
        #Second pulses
        birth_text.pulse(
            frame = end_start + 300,
            duration = 60,
            attack = 30,
            decay = 30
        )
        #Some fiddly stuff to make the pulse not look like displacement
        loc = birth_text.ref_obj.location
        birth_text.move_to(
            start_frame = end_start + 300,
            end_frame = end_start + 300 + 30,
            new_location = [loc[0] - 0.2, loc[1], loc[2]]
        )
        birth_text.move_to(
            start_frame = end_start + 300 + 30,
            end_frame = end_start + 300 + 30 + 30,
            new_location = [loc[0] + 0.2, loc[1], loc[2]]
        )

        death_text.pulse(
            frame = end_start + 330,
            duration = 60,
            attack = 30,
            decay = 30
        )
        #Some fiddly stuff to make the pulse not look like displacement
        loc = death_text.ref_obj.location
        death_text.move_to(
            start_frame = end_start + 330,
            end_frame = end_start + 330 + 30,
            new_location = [loc[0] - 0.2, loc[1], loc[2]]
        )
        death_text.move_to(
            start_frame = end_start + 330 + 30,
            end_frame = end_start + 330 + 30 + 30,
            new_location = [loc[0] + 0.2, loc[1], loc[2]]
        )


        text.disappear(disappear_frame = scene_end, animate = False)
        birth_text.disappear(disappear_frame = scene_end, animate = False)
        death_text.disappear(disappear_frame = scene_end, animate = False)
'''
'''
class HowToBeGoodAtExisting(Scene):
    """docstring for HowToBeGoodAtExisting."""
    def __init__(self):
        super().__init__()
        self.blank_duration = 240
        self.how_to_be_good_duration = 480

        total_duration = self.blank_duration + \
                         self.how_to_be_good_duration

        self.duration = total_duration

    def play_from_frame(self, frame):
        #Define flow
        how_to_be_good_start = frame + self.blank_duration
        how_to_be_good_end = how_to_be_good_start + self.how_to_be_good_duration

        scene_end = frame + self.duration

        #Create python-side objects
        how_text = tex_bobject.TexBobject(
            "\\text{How to be good at existing}",
            name = "How to",
            centered = True
        )
        how_container = bobject.TexComplex(
            how_text,
            name = 'How to container',
            location = (0, 5, 0),
            scale = 2,
            centered = True
        )
        birth_text = tex_bobject.TexBobject(
            "\\text{- Have a high birth rate}",
            scale = 1.5,
            location = (-10, 0, 0),
            name = "Birth"
        )
        death_text = tex_bobject.TexBobject(
            "\\text{- Have a low death rate}",
            scale = 1.5,
            location = (-10, -4, 0),
            name = "How to"
        )

        #Create blender-side objects and manipulate them
        how_container.add_to_blender(
            appear_frame = how_to_be_good_start,
            animate = True
        )
        birth_text.add_to_blender(
            appear_frame = how_to_be_good_start + 120,
            animate = True
        )
        death_text.add_to_blender(
            appear_frame = how_to_be_good_start + 216,
            animate = True
        )
        how_container.disappear(disappear_frame = scene_end)
        birth_text.disappear(disappear_frame = scene_end)
        death_text.disappear(disappear_frame = scene_end)
'''
'''
class FirstBlobSims(Scene):
    """docstring for ."""
    def __init__(self):
        super().__init__()
        self.blob1_intro_duration = 600
        self.blob1_sim_duration = 300
        self.blob2_intro_duration = 1110
        self.blob2_sim_duration = 930
        self.two_d_transition_duration = 180
        self.blob3_sim_duration = 660
        self.blob4_sim_duration = 1320

        total_duration = self.blob1_intro_duration + \
                         self.blob1_sim_duration + \
                         self.blob2_intro_duration + \
                         self.blob2_sim_duration + \
                         self.two_d_transition_duration + \
                         self.blob3_sim_duration + \
                         self.blob4_sim_duration

        self.duration = total_duration

    def play_from_frame(self, frame):

        #Define flow
        blob1_intro_start = frame
        blob1_intro_end = blob1_intro_start + self.blob1_intro_duration

        blob1_sim_start = blob1_intro_end
        blob1_sim_end = blob1_sim_start + self.blob1_sim_duration

        blob2_intro_start = blob1_sim_end
        blob2_intro_end = blob2_intro_start + self.blob2_intro_duration

        blob2_sim_start = blob2_intro_end
        blob2_sim_end = blob2_sim_start + self.blob2_sim_duration

        two_d_transition_start = blob2_sim_end
        two_d_transition_end = two_d_transition_start + self.two_d_transition_duration

        blob3_sim_start = two_d_transition_end
        blob3_sim_end = blob3_sim_start + self.blob3_sim_duration

        blob4_sim_start = blob3_sim_end
        blob4_sim_end = blob4_sim_start + self.blob4_sim_duration

        scene_end = frame + self.duration

        #Blob sim 1
        ##Create python-side objects
        birth_chance_tex1 = tex_bobject.TexBobject(
            '\\text{Birth chance each frame} = 100\\%',
            centered = True,
            location = (0, -4, 0)
        )
        death_chance_tex1 = tex_bobject.TexBobject(
            '\\text{Death chance each frame} = 10\\%',
            centered = True,
            location = (0, -5.5, 0)
        )

        initial_creature_count = 10
        initial_creatures = []
        for i in range(initial_creature_count):
            new_creature = creature.Creature()
            initial_creatures.append(new_creature)
        blob1_sim = drawn_world.DrawnWorld(
            name = 'blob1_sim',
            location = [-5, 0, 0],
            scale = 0.9,
            appear_frame = blob1_sim_start,
            start_delay = 50,
            duration = scene_end - blob1_sim_start,
            #load = 'raindrops',
            initial_creatures = initial_creatures,
            gene_updates = [
                ['color', 'creature_color_1', 'birth_modifier', 1000, 0],
                ['shape', 'shape1', 'birth_modifier', 1, 0],
                ['size', '1', 'birth_modifier', 1, 0],
                ['color', 'creature_color_1', 'replication_modifier', 0, 0],
                ['color', 'creature_color_1', 'death_modifier', 100, 0],
            ],
            counter_alignment = 'right_top'
        )

        blob1_sim.add_counter(
            color = 'creature_color_1',
            label = '\\text{Total: }'
        )
        blob1_sim.add_counter(
            color = 'creature_color_1',
            label = '\\text{Average: }',
            average = True
        )
        birth_chance_info1 = tex_bobject.TexBobject('\\text{Birth chance: } 100\\%')
        blob1_sim.add_info(birth_chance_info1)
        death_chance_info1 = tex_bobject.TexBobject('\\text{Death chance: } 10\\%')
        blob1_sim.add_info(death_chance_info1)

        birth_chance_tex2 = tex_bobject.TexBobject(
            '\\text{Birth chance each frame} = 10\\%',
            centered= True,
            location = (6.5, -4, 0),
            scale = 0.67
        )
        death_chance_tex2 = tex_bobject.TexBobject(
            '\\text{Death chance each frame} = 1\\%',
            centered= True,
            location = (6.5, -5, 0),
            scale = 0.67
        )

        """
        #Commented out because this loads a saved sim
        initial_creature_count = 10
        initial_creatures = []
        for i in range(initial_creature_count):
            new_creature = creature.Creature(color = 'creature_color_2', shape = 'shape2')
            initial_creatures.append(new_creature)"""
        blob2_sim = drawn_world.DrawnWorld(
            name = 'blob2_sim',
            location = [7, -2, 0],
            scale = 0.6,
            appear_frame = blob2_sim_start,
            start_delay = 50,
            duration = scene_end - blob2_sim_start,
            load = 'wte_sim2',
            #initial_creatures = initial_creatures,
            gene_updates = [
                ['color', 'creature_color_2', 'birth_modifier', 100, 0],
                ['shape', 'shape2', 'birth_modifier', 1, 0],
                ['size', '1', 'birth_modifier', 1, 0],
                ['color', 'creature_color_2', 'replication_modifier', 0, 0],
                ['color', 'creature_color_2', 'death_modifier', 10, 0],
            ],
            counter_alignment = 'top_left'
        )
        blob2_sim.add_counter(
            color = 'creature_color_2',
            label = '\\text{Total: }'
        )
        blob2_sim.add_counter(
            color = 'creature_color_2',
            label = '\\text{Average: }',
            average = True
        )

        birth_chance_info2 = tex_bobject.TexBobject('\\text{Birth chance: } 10\\%')
        blob2_sim.add_info(birth_chance_info2)
        death_chance_info2 = tex_bobject.TexBobject('\\text{Death chance: } 1\\%')
        blob2_sim.add_info(death_chance_info2)

        axes = graph_bobject.GraphBobject(
            name = 'axes',
            x_range = 26,
            x_label = '\\text{Death chance}',
            x_label_pos = 'along',
            y_range = 16,
            y_label = '\\text{Birth chance}',
            y_label_pos = 'along',
            y_label_rot = True,
            centered= True,
            arrows = 'positive'
        )

        """initial_creature_count = 1
        initial_creatures = []
        for i in range(initial_creature_count):
            new_creature = creature.Creature(shape = 'shape2')
            initial_creatures.append(new_creature)"""
        blob3_sim = drawn_world.DrawnWorld(
            name = 'blob3_sim',
            location = [4.5, -4, 0],
            scale = 0.4,
            appear_frame = blob3_sim_start,
            start_delay = 300,
            duration = scene_end - blob3_sim_start,
            load = 'wte_sim3',
            #initial_creatures = initial_creatures, #Number of default creatures
            gene_updates = [
                ['color', 'creature_color_1', 'birth_modifier', 100, 0],
                ['shape', 'shape2', 'birth_modifier', 1, 0],
                ['size', '1', 'birth_modifier', 1, 0],
                ['color', 'creature_color_1', 'replication_modifier', 0, 0],
                ['color', 'creature_color_1', 'death_modifier', 100, 0],
            ],
            counter_alignment = 'right_top'
        )
        blob3_sim.add_counter(
            color = 'creature_color_1',
            label = '\\text{Total: }'
        )
        blob3_sim.add_counter(
            color = 'creature_color_1',
            label = '\\text{Average: }',
            average = True
        )

        birth_chance_info3 = tex_bobject.TexBobject('\\text{Birth chance: } 10\\%')
        blob3_sim.add_info(birth_chance_info3)
        death_chance_info3 = tex_bobject.TexBobject('\\text{Death chance: } 10\\%')
        blob3_sim.add_info(death_chance_info3)

        initial_creature_count = 100
        initial_creatures = []
        for i in range(initial_creature_count):
            new_creature = creature.Creature(color = 'creature_color_2')
            initial_creatures.append(new_creature)
        blob4_sim = drawn_world.DrawnWorld(
            name = 'blob4_sim',
            location = [-8.5, 4, 0],
            scale = 0.4,
            appear_frame = blob4_sim_start,
            start_delay = 240,
            duration = scene_end - blob4_sim_start,
            overlap_okay = True,
            initial_creatures = initial_creatures, #Number of default creatures
            gene_updates = [
                ['color', 'creature_color_2', 'birth_modifier', 1000, 0],
                ['shape', 'shape1', 'birth_modifier', 1, 0],
                ['size', '1', 'birth_modifier', 1, 0],
                ['color', 'creature_color_2', 'replication_modifier', 0, 0],
                ['color', 'creature_color_2', 'death_modifier', 10, 0],
            ],
            counter_alignment = 'right_top'
        )

        blob4_sim.add_counter(
            label = '\\text{Total: }'
        )
        blob4_sim.add_counter(
            label = '\\text{Average: }',
            average = True
        )
        birth_chance_info4 = tex_bobject.TexBobject('\\text{Birth chance: } 100\\%')
        blob4_sim.add_info(birth_chance_info4)
        death_chance_info4 = tex_bobject.TexBobject('\\text{Death chance: } 1\\%')
        blob4_sim.add_info(death_chance_info4)

        blob1 = import_object(
            'boerd_blob',
            'creatures',
            location = (0, 2, 0),
            scale = 4
        )
        for child in blob1.ref_obj.children[0].children:
            if child.type == 'META':
                if len(child.material_slots) > 0:
                    child.data.resolution = 0.1
                    apply_material(child, 'creature_color3')

        ##Create blender-side objects and manipulate
        birth_chance_tex1.add_to_blender(
            appear_frame = blob1_intro_start + 300,
            animate = False
        )
        death_chance_tex1.add_to_blender(
            appear_frame = blob1_intro_start + 450,
            animate = False
        )
        birth_chance_tex1.disappear(disappear_frame = blob1_intro_end)
        death_chance_tex1.disappear(disappear_frame = blob1_intro_end)


        blob1.add_to_blender(
            appear_frame = blob1_intro_start,
            animate = True
        )
        blob1.move_to(
            start_frame = blob1_intro_end - OBJECT_APPEARANCE_TIME,
            end_frame = blob1_intro_end,
            new_location = (8, -3, 0)
        )
        execute_and_time(
            'Adding sim1 to blender',
            blob1_sim.add_to_blender(
                appear_frame = blob1_sim_start,
                animate = True
            )
        )

        blob1.move_to(
            start_frame = blob1_sim_end - OBJECT_APPEARANCE_TIME,
            end_frame = blob1_sim_end,
            new_scale = [2] * 3,
            new_location = (-3.5, 5, 0)
        )
        blob1_sim.move_to(
            start_frame = blob1_sim_end - OBJECT_APPEARANCE_TIME,
            end_frame = blob1_sim_end,
            new_scale = [0.6] * 3,
            new_location = (-7, -2, 0),
            new_counter_alignment = 'top_left'
        )

        #Blob sim 2
        ##Create python-side objects
        blob2 = import_object(
            'boerd_blob_squat',
            'creatures',
            location = (6.5, 1, 0),
            scale = 4
        )
        for child in blob2.ref_obj.children[0].children:
            if child.type == 'META':
                if len(child.material_slots) > 0:
                    child.data.resolution = 0.1
                    apply_material(child, 'creature_color4')

        blob2.add_to_blender(
            appear_frame = blob2_intro_start + 120,
            animate = True
        )
        birth_chance_tex2.add_to_blender(
            appear_frame = blob2_intro_start + 690,
            animate = False
        )
        death_chance_tex2.add_to_blender(
            appear_frame = blob2_intro_start + 930,
            animate = False
        )
        birth_chance_tex2.disappear(disappear_frame = blob2_intro_end)
        death_chance_tex2.disappear(disappear_frame = blob2_intro_end)



        ##Create blender-side objects and manipulate
        blob2.move_to(
            start_frame = blob2_intro_end - OBJECT_APPEARANCE_TIME,
            end_frame = blob2_intro_end,
            new_location = (10, 4.75, 0),
            new_scale = [2] * 3,
        )

        execute_and_time(
            'Adding sim2 to blender',
            blob2_sim.add_to_blender(
                appear_frame = blob2_sim_start,
                animate = True
            )
        )

        #two_d-transition
        ##Create axes and move existing sims


        axes.add_to_blender(
            appear_frame = two_d_transition_start + OBJECT_APPEARANCE_TIME,
            animate = True
        )

        collection = bobject.Bobject()
        collection.add_to_blender()
        bobjs_so_far = [blob1, blob1_sim, blob2, blob2_sim, axes]
        for bobj in bobjs_so_far:
            bobj.ref_obj.parent = collection.ref_obj
            bobj.ref_obj.matrix_parent_inverse = bobj.ref_obj.parent.matrix_world.inverted()

        collection.move_to(
            start_frame = two_d_transition_start,
            end_frame = two_d_transition_start + OBJECT_APPEARANCE_TIME,
            new_scale = [6/8] * 3,
        )
        blob1_sim.move_to(
            start_frame = two_d_transition_start,
            end_frame = two_d_transition_start + OBJECT_APPEARANCE_TIME,
            new_scale = [0.4] * 3,
            new_location = (4.5, 4, 0),
            new_counter_alignment = 'right_top'
        )
        blob1.move_to(
            start_frame = two_d_transition_start,
            end_frame = two_d_transition_start + OBJECT_APPEARANCE_TIME,
            new_scale = [2] * 3,
            new_location = (10.5, 2.5, 0)
        )
        blob2_sim.move_to(
            start_frame = two_d_transition_start,
            end_frame = two_d_transition_start + OBJECT_APPEARANCE_TIME,
            new_scale = [0.4] * 3,
            new_location = (-8.5, -4, 0),
            new_counter_alignment = 'right_top'
        )
        blob2.move_to(
            start_frame = two_d_transition_start,
            end_frame = two_d_transition_start + OBJECT_APPEARANCE_TIME,
            new_scale = [2] * 3,
            new_location = (-2.5, -5.5, 0)
        )



        ##Add sim3 and blob3
        blob3 = import_object(
            'boerd_blob_squat',
            'creatures',
            location = (10.5, -5.5, 0),
            scale = 2
        )
        for child in blob3.ref_obj.children[0].children:
            if child.type == 'META':
                if len(child.material_slots) > 0:
                    child.data.resolution = 0.1
                    apply_material(child, 'creature_color3')



        ##Create blender-side objects and manipulate
        blob3.add_to_blender(
            appear_frame = blob3_sim_start,
            animate = True
        )
        execute_and_time(
            'Adding sim3 to blender',
            blob3_sim.add_to_blender(
                appear_frame = blob3_sim_start,
                animate = True
            )
        )
        blob3.ref_obj.parent = collection.ref_obj
        blob3_sim.ref_obj.parent = collection.ref_obj

        #Add sim4 and blob4
        blob4 = import_object(
            'boerd_blob',
            'creatures',
            location = (-2.5, 2.5, 0),
            scale = 2
        )
        for child in blob4.ref_obj.children[0].children:
            if child.type == 'META':
                if len(child.material_slots) > 0:
                    child.data.resolution = 0.1
                    apply_material(child, 'creature_color4')


        ##Create blender-side objects and manipulate
        blob4.add_to_blender(
            appear_frame = blob4_sim_start,
            animate = True
        )

        execute_and_time(
            'Adding sim4 to blender',
            blob4_sim.add_to_blender(
                appear_frame = blob4_sim_start,
                animate = True
            )
        )
        blob4.ref_obj.parent = collection.ref_obj
        blob4_sim.ref_obj.parent = collection.ref_obj

        remaining = [blob1, blob1_sim, blob2, blob2_sim, blob3, blob3_sim, blob4, blob4_sim, axes]
        for bobj in remaining:
            bobj.disappear(disappear_frame = scene_end)
'''
'''
class Equation(Scene):
    """docstring for [object Object]."""
    def __init__(self):
        super().__init__()
        #self.equation_duration = 340

        self.subscenes = collections.OrderedDict([
            ('creature', {'duration': 60}),
            ('add_equation', {'duration': 960}),
            ('explore_equilibrium', {'duration': 4200}),
            ('solve_for_number', {'duration': 720}),
            ('example', {'duration': 1200}),
        ])

        total_duration = 0
        for sub, attrs in self.subscenes.items():
            total_duration += attrs['duration']

        self.duration = total_duration

    def set_subscene_timing(self, frame):
        start = frame
        for sub, attrs in self.subscenes.items():
            attrs['start'] = start
            attrs['end'] = start + attrs['duration']
            start = attrs['end']


    def play_from_frame(self, frame):
        #Define flow
        self.set_subscene_timing(frame)
        cues = self.subscenes
        #equation_start = frame
        #equation_end = equation_start + self.equation_duration

        scene_end = frame + self.duration

        blob1 = import_object(
            'boerd_blob',
            'creatures',
            location = (8, -12, 0),
            scale = 4
        )
        for child in blob1.ref_obj.children[0].children:
            if child.type == 'META':
                if len(child.material_slots) > 0:
                    child.data.resolution = 0.1
                    apply_material(child, 'creature_color3')

        blob1.add_to_blender(
            appear_frame = cues['creature']['start'] - 60,
            animate = True
        )
        blob1.move_to(
            new_location = (8, -7, 0),
            start_frame = cues['creature']['start']
        )

        #Equation
        lhs = tex_bobject.TexBobject(
            "\\text{Birth rate}",
            "1",
            "\\text{Birth rate}",
            "B",
            "\\dfrac{B}{D}",
            "\\dfrac{0.8}{D}",
            "\\dfrac{0.8}{0.02}",
            "40",
            centered = True
        )
        equals = tex_bobject.TexBobject(
            "\!=",
            "\!<",
            "\!=",
            "\!>",
            "\!=",
            centered = True
        )
        rhs = tex_bobject.TexBobject(
            "\\text{Death rate}",
            "\\text{Number} \\times \\text{Death rate per creature}",
            "\\text{Number} \\times 0.1",
            "10 \\times 0.1",
            "11 \\times 0.1",
            "12 \\times 0.1",
            "13 \\times 0.1",
            "10 \\times 0.1",
            "9 \\times 0.1",
            "8 \\times 0.1",
            "10 \\times 0.1",
            "\\text{Number} \\times \\text{Death rate per creature}",
            "N \\times D",
            "\\dfrac{N \\times D}{D}",
            "N",
            centered = True
        )

        equation = bobject.TexComplex(
            lhs, equals, rhs,
            centered = True,
            scale = 1.5
        )

        equation.add_to_blender(
            appear_frame = cues['add_equation']['start'] + 15,
            animate = False,
            subbobject_timing = [0, 60, 105]
        )

        rhs.morph_figure(1, start_frame = cues['add_equation']['start'] + 720)
        equation.move_to(
            new_scale = 1,
            start_frame = cues['add_equation']['start'] + 720,
        )


        lhs.morph_figure(1, start_frame = cues['explore_equilibrium']['start'] + 150)
        rhs.morph_figure(2, start_frame = cues['explore_equilibrium']['start'] + 330)
        equation.move_to(
            new_scale = 1.5,
            start_frame = cues['explore_equilibrium']['start'] + 330,
        )
        rhs.morph_figure(3, start_frame = cues['explore_equilibrium']['start'] + 705)
        equals.morph_figure(1, start_frame = cues['explore_equilibrium']['start'] + 1710)
        rhs.move_to(
            new_scale = 11 / 10,
            start_frame = cues['explore_equilibrium']['start'] + 1710,
            end_frame = cues['explore_equilibrium']['start'] + 1710 + OBJECT_APPEARANCE_TIME
        )
        rhs.morph_figure(4, start_frame = cues['explore_equilibrium']['start'] + 1710)
        rhs.move_to(
            new_scale = 12 / 10,
            start_frame = cues['explore_equilibrium']['start'] + 2520,
            end_frame = cues['explore_equilibrium']['start'] + 2520 + OBJECT_APPEARANCE_TIME
        )
        rhs.morph_figure(5, start_frame = cues['explore_equilibrium']['start'] + 2520)
        rhs.move_to(
            new_scale = 13 / 10,
            start_frame = cues['explore_equilibrium']['start'] + 2580,
            end_frame = cues['explore_equilibrium']['start'] + 2580 + OBJECT_APPEARANCE_TIME
        )
        rhs.morph_figure(6, start_frame = cues['explore_equilibrium']['start'] + 2580)

        rhs.move_to(
            new_scale = 10 / 10,
            start_frame = cues['explore_equilibrium']['start'] + 2700,
            end_frame = cues['explore_equilibrium']['start'] + 2700 + OBJECT_APPEARANCE_TIME
        )
        rhs.morph_figure(7, start_frame = cues['explore_equilibrium']['start'] + 2700)
        equals.morph_figure(2, start_frame = cues['explore_equilibrium']['start'] + 2700)

        equals.morph_figure(3, start_frame = cues['explore_equilibrium']['start'] + 3000)
        rhs.move_to(
            new_scale = 9 / 10,
            start_frame = cues['explore_equilibrium']['start'] + 3000,
            end_frame = cues['explore_equilibrium']['start'] + 3000 + OBJECT_APPEARANCE_TIME
        )
        rhs.morph_figure(8, start_frame = cues['explore_equilibrium']['start'] + 3000)
        rhs.move_to(
            new_scale = 8 / 10,
            start_frame = cues['explore_equilibrium']['start'] + 3060,
            end_frame = cues['explore_equilibrium']['start'] + 3060 + OBJECT_APPEARANCE_TIME
        )
        rhs.morph_figure(9, start_frame = cues['explore_equilibrium']['start'] + 3060)
        equals.morph_figure(4, start_frame = cues['explore_equilibrium']['start'] + 3600)
        rhs.move_to(
            new_scale = 10 / 10,
            start_frame = cues['explore_equilibrium']['start'] + 3600,
            end_frame = cues['explore_equilibrium']['start'] + 3600 + OBJECT_APPEARANCE_TIME
        )
        rhs.morph_figure(10, start_frame = cues['explore_equilibrium']['start'] + 3600)

        equilibrium = tex_bobject.TexBobject(
            '\\text{``Equilibrium``}',
            location = (0, 5, 0),
            centered = True,
            scale = 2
        )
        equilibrium.add_to_blender(
            appear_frame = cues['explore_equilibrium']['start'] + 3870,
            animate = True
        )
        equilibrium.disappear(disappear_frame = cues['explore_equilibrium']['end'])


        #Solve for N
        lhs.morph_figure(2, start_frame = cues['solve_for_number']['start'] + 60)
        #equals.morph_figure(4, start_frame = cues['solve_for_number']['start'])
        rhs.morph_figure(11, start_frame = cues['solve_for_number']['start'] + 60)
        equation.move_to(
            new_scale = 1,
            start_frame = cues['solve_for_number']['start'] + 60,
        )

        lhs.morph_figure(3, start_frame = cues['solve_for_number']['start'] + 240)
        rhs.morph_figure(12, start_frame = cues['solve_for_number']['start'] + 240)
        equation.move_to(
            new_scale = 1.5,
            start_frame = cues['solve_for_number']['start'] + 240,
        )

        lhs.morph_figure(4, start_frame = cues['solve_for_number']['start'] + 420)
        rhs.morph_figure(13, start_frame = cues['solve_for_number']['start'] + 420)

        rhs.morph_figure(14, start_frame = cues['solve_for_number']['start'] + 540)

        equation.subbobjects = [rhs, equals, lhs]
        equation.arrange_tex_bobjects(
            start_frame = cues['solve_for_number']['start'] + 660,
            end_frame = cues['solve_for_number']['start'] + 660 + DEFAULT_MORPH_TIME
        )

        #Example
        equation.move_to(
            new_location = (-7, 0, 0),
            start_frame = cues['example']['start'],
            end_frame = cues['example']['start'] + OBJECT_APPEARANCE_TIME
        )

        blob1.move_to(
            new_location = (9, 5, 0),
            new_scale = 2,
            start_frame = cues['example']['start'],
            end_frame = cues['example']['start'] + OBJECT_APPEARANCE_TIME
        )

        initial_creature_count = 40
        initial_creatures = []
        for i in range(initial_creature_count):
            new_creature = creature.Creature()
            initial_creatures.append(new_creature)
        blob1_sim = drawn_world.DrawnWorld(
            name = 'blob1_sim',
            location = [5.5, -2, 0],
            scale = 0.6,
            appear_frame = cues['example']['start'],
            start_delay = 810,
            duration = scene_end - cues['example']['start'],
            initial_creatures = initial_creatures,
            #save = True,
            load = 'equation_example',
            gene_updates = [
                ['color', 'creature_color_1', 'birth_modifier', 800, 0],
                ['shape', 'shape1', 'birth_modifier', 1, 0],
                ['size', '1', 'birth_modifier', 1, 0],
                ['color', 'creature_color_1', 'replication_modifier', 0, 0],
                ['color', 'creature_color_1', 'death_modifier', 20, 0],
            ],
            counter_alignment = 'top_left'
        )

        lhs.morph_figure(5, start_frame = cues['example']['start'] + 120)
        lhs.morph_figure(6, start_frame = cues['example']['start'] + 240)
        lhs.morph_figure(7, start_frame = cues['example']['start'] + 630)


        execute_and_time(
            'Adding sim1 total counter',
            blob1_sim.add_counter(
                        color = 'creature_color_1',
                        label = '\\text{Total: }'
            )
        )
        execute_and_time(
            'Adding sim1 average counter',
            blob1_sim.add_counter(
                        color = 'creature_color_1',
                        label = '\\text{Average: }',
                        average = True
            )
        )
        birth_chance_info = tex_bobject.TexBobject('\\text{Birth chance: } 80\\%')
        blob1_sim.add_info(birth_chance_info)
        birth_chance_info.pulse(
            frame = cues['example']['start'] + 120,
            duration = 120
        )

        death_chance_info = tex_bobject.TexBobject('\\text{Death chance: } 2\\%')
        blob1_sim.add_info(death_chance_info)
        death_chance_info.pulse(
            frame = cues['example']['start'] + 240,
            duration = 120
        )

        execute_and_time(
            'Adding sim1 to blender',
            blob1_sim.add_to_blender(
                appear_frame = cues['example']['start'],
                animate = True
            )
        )

        equation.disappear(disappear_frame = scene_end)
        blob1.disappear(disappear_frame = scene_end)
        blob1_sim.disappear(disappear_frame = scene_end)
'''
'''
class LifeIsDifferent(Scene):
    """docstring for [object Object]."""
    def __init__(self):
        super().__init__()
        #self.equation_duration = 340

        self.subscenes = collections.OrderedDict([
            ('living_things', {'duration': 600}),
            ('form_bunny', {'duration': 360}),
            ('living_things2', {'duration': 900}),
            ('sim_setup', {'duration': 300}),
            ('replication', {'duration': 420})
        ])

        total_duration = 0
        for sub, attrs in self.subscenes.items():
            total_duration += attrs['duration']

        self.duration = total_duration

    def set_subscene_timing(self, frame):
        start = frame
        for sub, attrs in self.subscenes.items():
            attrs['start'] = start
            attrs['end'] = start + attrs['duration']
            start = attrs['end']

    def play_from_frame(self, frame):
        self.set_subscene_timing(frame)
        cues = self.subscenes
        scene_end = frame + self.duration


        why = tex_bobject.TexBobject(
            '\\text{Why do living things exist?}',
            location = (0, 5, 0),
            scale = 2,
            centered = True
        )

        birth_text = tex_bobject.TexBobject(
            "1. \\text{ They were born}",
            scale = 1.5,
            location = (-9, 0.5, 0),
            name = "Birth"
        )
        death_text = tex_bobject.TexBobject(
            "2. \\text{ They haven't died}",
            scale = 1.5,
            location = (-9, -3, 0),
            name = "Death"
        )

        why.add_to_blender(
            appear_frame = cues['living_things']['start'],
        )
        birth_text.add_to_blender(
            appear_frame = cues['living_things']['start'],
        )
        death_text.add_to_blender(
            appear_frame = cues['living_things']['start'],
        )




        #Some fiddly stuff to make the pulse not look like displacement
        loc = birth_text.ref_obj.location
        birth_text.move_to(
            start_frame = cues['living_things']['start'] + 420,
            end_frame = cues['living_things']['start'] + 420 + OBJECT_APPEARANCE_TIME,
            new_location = [loc[0] + 0.3, loc[1], loc[2]],
            new_scale = 0.6 * birth_text.ref_obj.scale[0]
        )

        why.disappear(
            disappear_frame = cues['living_things']['end']
        )
        birth_text.disappear(
            disappear_frame = cues['living_things']['end']
        )
        death_text.disappear(
            disappear_frame = cues['living_things']['end']
        )


        bun = import_object('stanford_bunny', 'creatures', scale = 4)
        tele = import_object('teleporter', 'primitives', scale = 10)
        tele.ref_obj.rotation_euler = (math.pi / 2, 0, 0)
        form_bun = bobject.MeshMorphBobject(name = 'form_bun')
        form_bun.add_subbobject_to_series(tele)
        form_bun.add_subbobject_to_series(bun)

        form_bun.add_to_blender(
            appear_frame = cues['form_bunny']['start'],
            animate = False
        )

        form_bun.morph_bobject(
            0, 1, cues['form_bunny']['start'], cues['form_bunny']['end'] - 60,
            dissolve_time = 120
        )

        #Spiiiiiiiin
        form_bun.ref_obj.rotation_euler = (0, 0, 0)
        form_bun.ref_obj.keyframe_insert(data_path="rotation_euler", frame = 0)
        form_bun.ref_obj.rotation_euler = (0, 8 * math.pi, 0)
        form_bun.ref_obj.keyframe_insert(
            data_path="rotation_euler",
            frame = cues['form_bunny']['end'] - 60
        )

        form_bun.move_to(
            start_frame = cues['form_bunny']['end'] - OBJECT_APPEARANCE_TIME,
            end_frame = cues['form_bunny']['end'],
            #new_location = (8, -4, 0),
            new_location = (12, -7, 0)
        )


        why.add_to_blender(
            appear_frame = cues['living_things2']['start'],
        )
        birth_text.add_to_blender(
            appear_frame = cues['living_things2']['start'],
        )
        death_text.add_to_blender(
            appear_frame = cues['living_things2']['start'],
        )

        loc = death_text.ref_obj.location
        death_text.move_to(
            start_frame = cues['living_things2']['start'] + 120,
            end_frame = cues['living_things2']['start'] + 120 + OBJECT_APPEARANCE_TIME,
            new_location = [loc[0] + 0.3, loc[1], loc[2]],
            new_scale = 0.6 * death_text.ref_obj.scale[0]
        )
        loc = birth_text.ref_obj.location
        birth_text.move_to(
            start_frame = cues['living_things2']['start'] + 180,
            end_frame = cues['living_things2']['start'] + 180 + OBJECT_APPEARANCE_TIME,
            new_location = [loc[0] + 3, loc[1], loc[2]]
        )
        loc = death_text.ref_obj.location
        death_text.move_to(
            start_frame = cues['living_things2']['start'] + 180,
            end_frame = cues['living_things2']['start'] + 180 + OBJECT_APPEARANCE_TIME,
            new_location = [loc[0] + 3, loc[1], loc[2]]
        )

        why.disappear(
            disappear_frame = cues['living_things2']['end']
        )
        birth_text.disappear(
            disappear_frame = cues['living_things2']['end']
        )
        death_text.disappear(
            disappear_frame = cues['living_things2']['end']
        )




        form_bun.move_to(
            start_frame = cues['sim_setup']['start'] - OBJECT_APPEARANCE_TIME,
            end_frame = cues['sim_setup']['start'],
            new_location = (8, -3, 0),
        )


        initial_creature_count = 1
        initial_creatures = []
        for i in range(initial_creature_count):
            new_creature = creature.Creature()
            initial_creatures.append(new_creature)
        bun_sim = drawn_world.DrawnWorld(
            name = 'blob1_sim',
            location = [-6, 0, 0],
            scale = 0.9,
            appear_frame = cues['sim_setup']['start'],
            start_delay = 0,
            duration = scene_end - cues['sim_setup']['start'],
            load = 'wte_first_replication',
            initial_creatures = initial_creatures,
            gene_updates = [
                ['color', 'creature_color_1', 'death_modifier', 0, 0],
                ['shape', 'shape1', 'mutation_chance', 0, 0],
                ['size', '1', 'mutation_chance', 0, 0],
                ['color', 'creature_color_1', 'mutation_chance', 0, 0],
                ['color', 'creature_color_1', 'replication_modifier', 20, cues['sim_setup']['duration'] / 2 ],
                ['color', 'creature_color_1', 'death_modifier', 10, cues['sim_setup']['duration'] / 2 ],
            ],
            counter_alignment = 'right_top',
            creature_model = ['stanford_bunny', 'creatures']
        )

        execute_and_time(
            'Adding sim1 to blender',
            bun_sim.add_to_blender(
                appear_frame = cues['sim_setup']['start'],
                animate = True
            )
        )
        spontaneous = tex_bobject.TexBobject('\\text{Spontaneous}')
        bun_sim.add_info(spontaneous)
        birth_chance_info = tex_bobject.TexBobject('\\text{birth chance: Low}')
        bun_sim.add_info(birth_chance_info)
        death_chance_info = tex_bobject.TexBobject('\\text{Death chance: High}')
        bun_sim.add_info(death_chance_info)
        bun_sim.align_info(frame = cues['sim_setup']['start'] + 50)

        rep_chance_info = tex_bobject.TexBobject('\\text{Replication chance: High}')
        bun_sim.add_info(rep_chance_info)
        bun_sim.align_info(frame = cues['replication']['start'])


        bun_sim.disappear(disappear_frame = scene_end)
        #form_bun.disappear(disappear_frame = scene_end)
'''
'''
class EquationWithReplication(Scene):
    """docstring for [object Object]."""
    def __init__(self):
        super().__init__()
        #self.equation_duration = 340

        self.subscenes = collections.OrderedDict([
            ('add_equation', {'duration': 2700}),
            ('solve_for_number', {'duration': 960}),
            ('example', {'duration': 4410}),
        ])

        total_duration = 0
        for sub, attrs in self.subscenes.items():
            total_duration += attrs['duration']

        self.duration = total_duration

    def set_subscene_timing(self, frame):
        start = frame
        for sub, attrs in self.subscenes.items():
            attrs['start'] = start
            attrs['end'] = start + attrs['duration']
            start = attrs['end']


    def play_from_frame(self, frame):
        #Define flow
        self.set_subscene_timing(frame)
        cues = self.subscenes
        #equation_start = frame
        #equation_end = equation_start + self.equation_duration

        scene_end = frame + self.duration

        blob1 = import_object(
            'stanford_bunny',
            'creatures',
            location = (8, -3, 0),
            scale = 4
        )
        for child in blob1.ref_obj.children[0].children:
            if child.type == 'META':
                if len(child.material_slots) > 0:
                    child.data.resolution = 0.1
                    apply_material(child, 'creature_color3')


        #Equation
        lhs = tex_bobject.TexBobject(
            "\\text{Birth rate}",
            "B + N \\times R",
            "B + N \\times R - (N \\times R)",
            "B",
            "\\dfrac{B}{(D - R)}",
            "\\dfrac{B}{D - R}",
            "\\dfrac{0.1}{D - R}",
            "\\dfrac{0.1}{0.05 - R}",
            "\\dfrac{0.1}{0.05 - 0}",
            "\\dfrac{0.1}{0.05 - 0.01}",
            "\\dfrac{0.1}{0.05 - 0.02}",
            "\\dfrac{0.1}{0.05 - 0.03}",
            "\\dfrac{0.1}{0.05 - 0.04}",
            "\\dfrac{0.1}{0.05 - 0.05}",
            "\\dfrac{0.1}{0.05 - 0.06}",
            centered = True
        )
        equals = tex_bobject.TexBobject(
            "\!=",
            centered = True
        )
        rhs = tex_bobject.TexBobject(
            "\\text{Death rate}",
            "N \\times D",
            "N \\times D - (N \\times R)",
            "N \\times (D - R)",
            "\\dfrac{N \\times (D - R)}{(D - R)}",
            "N",
            centered = True
        )

        equation = bobject.TexComplex(
            lhs, equals, rhs,
            centered = True,
            scale = 1.5
        )

        initial_creature_count = 2
        initial_creatures = []
        for i in range(initial_creature_count):
            new_creature = creature.Creature()
            initial_creatures.append(new_creature)
        blob1_sim = drawn_world.DrawnWorld(
            name = 'blob1_sim',
            location = [5.5, -2, 0],
            scale = 0.6,
            appear_frame = cues['example']['start'],
            start_delay = 0,
            #save = True,
            load = 'wte_eq_replication',
            duration = scene_end - cues['example']['start'],
            initial_creatures = initial_creatures,
            gene_updates = [
                ['color', 'creature_color_1', 'birth_modifier', 100, 0],
                ['shape', 'shape1', 'birth_modifier', 1, 0],
                ['size', '1', 'birth_modifier', 1, 0],
                ['color', 'creature_color_1', 'mutation_chance', 0, 0],
                ['shape', 'shape1', 'mutation_chance', 0, 0],
                ['size', '1', 'mutation_chance', 0, 0],
                ['color', 'creature_color_1', 'death_modifier', 50, 0],
                ['color', 'creature_color_1', 'replication_modifier', 0, 0],
                ['color', 'creature_color_1', 'replication_modifier', 10, 1680 / 2],
                ['color', 'creature_color_1', 'replication_modifier', 20, 2040 / 2],
                ['color', 'creature_color_1', 'replication_modifier', 30, 2160 / 2],
                ['color', 'creature_color_1', 'replication_modifier', 40, 2280 / 2],
                ['color', 'creature_color_1', 'replication_modifier', 50, 2790 / 2],
                #['color', 'creature_color_1', 'replication_modifier', 50, 500],
                ['color', 'creature_color_1', 'replication_modifier', 54.5, 3330 / 2],
            ],
            counter_alignment = 'top_left',
            creature_model = ['stanford_bunny', 'creatures']
        )

        execute_and_time(
            'Adding sim1 total counter',
            blob1_sim.add_counter(
                        color = 'creature_color_1',
                        label = '\\text{Total: }'
            )
        )


        equals2 = tex_bobject.TexBobject(
            "\!=",
            "\\approx",
            "\!=",
            "\\rightarrow",
            "\!=",
            centered = True
        )
        srhs = tex_bobject.TexBobject(
            "2",
            "2.5",
            "3.3",
            "5",
            "10",
            "\\infty",
            "-10",
            "-10\\text{?}",
            centered = True
        )

        #Add calculated result
        equals2.ref_obj.parent = equation.ref_obj
        srhs.ref_obj.parent = equation.ref_obj
        equals2.superbobject = equation
        equals2.superbobject = equation

        blob1.add_to_blender(
            appear_frame = cues['add_equation']['start'] - 60,
            animate = True
        )
        blob1.move_to(
            new_location = (8, -7, 0),
            start_frame = cues['add_equation']['start']
        )

        equation.add_to_blender(
            appear_frame = cues['add_equation']['start'] + 120,
            animate = False,
        )

        rhs.morph_figure(1, start_frame = cues['add_equation']['start'] + 420)
        equation.arrange_tex_bobjects(
            start_frame = cues['add_equation']['start'] + 420,
            end_frame = cues['add_equation']['start'] + 420 + DEFAULT_MORPH_TIME
        )
        lhs.morph_figure(1, start_frame = cues['add_equation']['start'] + 720)
        equation.arrange_tex_bobjects(
            start_frame = cues['add_equation']['start'] + 720,
            end_frame = cues['add_equation']['start'] + 720 + DEFAULT_MORPH_TIME
        )

        B = lhs.lookup_table[1][0]
        B.pulse(
            frame = cues['add_equation']['start'] + 840,
            duration = 300,
            attack = OBJECT_APPEARANCE_TIME,
            decay = OBJECT_APPEARANCE_TIME
        )
        B.color_shift(
            start_frame = cues['add_equation']['start'] + 840,
            duration = 300,
            color = COLORS_SCALED[3]
        )

        N = lhs.lookup_table[1][2]
        N.pulse(
            frame = cues['add_equation']['start'] + 1230,
            duration = 150,
            attack = OBJECT_APPEARANCE_TIME,
            decay = OBJECT_APPEARANCE_TIME
        )
        N.color_shift(
            start_frame = cues['add_equation']['start'] + 1230,
            duration = 150,
            color = COLORS_SCALED[3]
        )
        times = lhs.lookup_table[1][3]
        times.pulse(
            frame = cues['add_equation']['start'] + 1230,
            duration = 150,
            attack = OBJECT_APPEARANCE_TIME,
            decay = OBJECT_APPEARANCE_TIME
        )
        times.color_shift(
            start_frame = cues['add_equation']['start'] + 1230,
            duration = 150,
            color = COLORS_SCALED[3]
        )
        R = lhs.lookup_table[1][4]
        R.pulse(
            frame = cues['add_equation']['start'] + 1230,
            duration = 150,
            attack = OBJECT_APPEARANCE_TIME,
            decay = OBJECT_APPEARANCE_TIME
        )
        R.color_shift(
            start_frame = cues['add_equation']['start'] + 1230,
            duration = 150,
            color = COLORS_SCALED[3]
        )

        R.pulse(
            frame = cues['add_equation']['start'] + 1530,
            duration = 90,
            attack = OBJECT_APPEARANCE_TIME,
            decay = OBJECT_APPEARANCE_TIME
        )
        R.color_shift(
            start_frame = cues['add_equation']['start'] + 1530,
            duration = 90,
            color = COLORS_SCALED[3]
        )

        N.pulse(
            frame = cues['add_equation']['start'] + 1710,
            duration = 300,
            attack = OBJECT_APPEARANCE_TIME,
            decay = OBJECT_APPEARANCE_TIME
        )
        N.color_shift(
            start_frame = cues['add_equation']['start'] + 1710,
            duration = 300,
            color = COLORS_SCALED[3]
        )

        times.pulse(
            frame = cues['add_equation']['start'] + 1830,
            duration = 180,
            attack = OBJECT_APPEARANCE_TIME,
            decay = OBJECT_APPEARANCE_TIME
        )
        times.color_shift(
            start_frame = cues['add_equation']['start'] + 1830,
            duration = 180,
            color = COLORS_SCALED[3]
        )
        R.pulse(
            frame = cues['add_equation']['start'] + 1830,
            duration = 180,
            attack = OBJECT_APPEARANCE_TIME,
            decay = OBJECT_APPEARANCE_TIME
        )
        R.color_shift(
            start_frame = cues['add_equation']['start'] + 1830,
            duration = 180,
            color = COLORS_SCALED[3]
        )

        #Waggle
        N.pulse(
            frame = cues['add_equation']['start'] + 2220,
            duration = 60,
            attack = OBJECT_APPEARANCE_TIME,
            decay = OBJECT_APPEARANCE_TIME
        )
        N.color_shift(
            start_frame = cues['add_equation']['start'] + 2220,
            duration = 60,
            color = COLORS_SCALED[3]
        )
        N2 = rhs.lookup_table[1][0]
        N2.pulse(
            frame = cues['add_equation']['start'] + 2250,
            duration = 60,
            attack = OBJECT_APPEARANCE_TIME,
            decay = OBJECT_APPEARANCE_TIME
        )
        N2.color_shift(
            start_frame = cues['add_equation']['start'] + 2250,
            duration = 60,
            color = COLORS_SCALED[3]
        )
        N.pulse(
            frame = cues['add_equation']['start'] + 2280,
            duration = 60,
            attack = OBJECT_APPEARANCE_TIME,
            decay = OBJECT_APPEARANCE_TIME
        )
        N.color_shift(
            start_frame = cues['add_equation']['start'] + 2280,
            duration = 60,
            color = COLORS_SCALED[3]
        )
        N2.pulse(
            frame = cues['add_equation']['start'] + 2310,
            duration = 60,
            attack = OBJECT_APPEARANCE_TIME,
            decay = OBJECT_APPEARANCE_TIME
        )
        N2.color_shift(
            start_frame = cues['add_equation']['start'] + 2310,
            duration = 60,
            color = COLORS_SCALED[3]
        )


        #Solve equation
        equation.move_to(
            new_scale = 1.2,
            start_frame = cues['solve_for_number']['start'] + 240
        )
        lhs.morph_figure(2, start_frame = cues['solve_for_number']['start'] + 240)
        rhs.morph_figure(2, start_frame = cues['solve_for_number']['start'] + 240)

        equation.move_to(
            new_scale = 1.5,
            start_frame = cues['solve_for_number']['start'] + 360
        )
        lhs.morph_figure(3, start_frame = cues['solve_for_number']['start'] + 360)

        rhs.morph_figure(3, start_frame = cues['solve_for_number']['start'] + 480)

        lhs.morph_figure(4, start_frame = cues['solve_for_number']['start'] + 600)
        rhs.morph_figure(4, start_frame = cues['solve_for_number']['start'] + 600)

        rhs.morph_figure(5, start_frame = cues['solve_for_number']['start'] + 720)
        lhs.morph_figure(5, start_frame = cues['solve_for_number']['start'] + 720)

        equation.subbobjects = [rhs, equals, lhs]
        equation.arrange_tex_bobjects(
            start_frame = cues['solve_for_number']['start'] + 840,
            end_frame = cues['solve_for_number']['start'] + 840 + DEFAULT_MORPH_TIME
        )

        #Example
        equation.move_to(
            new_location = (-7, 0, 0),
            start_frame = cues['example']['start'],
            end_frame = cues['example']['start'] + OBJECT_APPEARANCE_TIME
        )

        blob1.move_to(
            new_location = (10, 5, 0),
            new_scale = 2,
            new_angle = [5.5 * math.pi / 180, 0, 0],
            start_frame = cues['example']['start'],
            end_frame = cues['example']['start'] + OBJECT_APPEARANCE_TIME
        )

        lhs.morph_figure(6, start_frame = cues['example']['start'] + 180)
        lhs.morph_figure(7, start_frame = cues['example']['start'] + 750)
        lhs.morph_figure(8, start_frame = cues['example']['start'] + 960)

        equation.subbobjects = [rhs, equals, lhs, equals2, srhs]
        equals2.superbobject = equation
        srhs.superbobject = equation
        equation.arrange_tex_bobjects(
            start_frame = cues['example']['start'] + 1200,
            end_frame = cues['example']['start'] + 1200 + DEFAULT_MORPH_TIME
        )
        equation.move_to(
            new_scale = 1,
            start_frame = cues['example']['start'] + 1200
        )
        equals2.add_to_blender(
            appear_frame = cues['example']['start'] + 1230,
            animate = True,
        )
        srhs.add_to_blender(
            appear_frame = cues['example']['start'] + 1230,
            animate = True,
        )

        lhs.morph_figure(9, start_frame = cues['example']['start'] + 1680)
        srhs.morph_figure(1, start_frame = cues['example']['start'] + 1680)
        """equation.arrange_tex_bobjects(
            start_frame = cues['example']['start'] + 1680,
            end_frame = cues['example']['start'] + 1680 + DEFAULT_MORPH_TIME
        )"""

        lhs.morph_figure(10, start_frame = cues['example']['start'] + 2040)
        srhs.morph_figure(2, start_frame = cues['example']['start'] + 2040)
        equals2.morph_figure(1, start_frame = cues['example']['start'] + 2040)

        lhs.morph_figure(11, start_frame = cues['example']['start'] + 2160)
        srhs.morph_figure(3, start_frame = cues['example']['start'] + 2160)
        equals2.morph_figure(2, start_frame = cues['example']['start'] + 2160)
        """equation.arrange_tex_bobjects(
            start_frame = cues['example']['start'] + 350,
            end_frame = cues['example']['start'] + 350 + DEFAULT_MORPH_TIME
        )"""
        lhs.morph_figure(12, start_frame = cues['example']['start'] + 2280)
        srhs.morph_figure(4, start_frame = cues['example']['start'] + 2280)

        lhs.morph_figure(13, start_frame = cues['example']['start'] + 2790)
        srhs.morph_figure(5, start_frame = cues['example']['start'] + 2790)
        equals2.morph_figure(3, start_frame = cues['example']['start'] + 2790)

        lhs.morph_figure(14, start_frame = cues['example']['start'] + 3330)
        srhs.morph_figure(6, start_frame = cues['example']['start'] + 3330)
        equals2.morph_figure(4, start_frame = cues['example']['start'] + 3330)

        srhs.morph_figure(7, start_frame = cues['example']['start'] + 3600)
        """equation.arrange_tex_bobjects(
            start_frame = cues['example']['start'] + 550,
            end_frame = cues['example']['start'] + 550 + DEFAULT_MORPH_TIME
        )"""

        execute_and_time(
            'Adding sim1 to blender',
            blob1_sim.add_to_blender(
                appear_frame = cues['example']['start'],
                animate = True
            )
        )
        spontaneous = tex_bobject.TexBobject('\\text{Spontaneous}')
        blob1_sim.add_info(spontaneous)
        birth_chance_info = tex_bobject.TexBobject('\\text{birth chance: } 10\\%')
        blob1_sim.add_info(birth_chance_info)
        blob1_sim.align_info(frame = cues['example']['start'] + 180)

        death_chance_info = tex_bobject.TexBobject('\\text{Death chance: } 5\\%')
        blob1_sim.add_info(death_chance_info)
        blob1_sim.align_info(frame = cues['example']['start'] + 750)
        rep_chance_info = tex_bobject.TexBobject(
            '\\text{Replication chance: } 0\\%',
            '\\text{Replication chance: } 1\\%',
            '\\text{Replication chance: } 2\\%',
            '\\text{Replication chance: } 3\\%',
            '\\text{Replication chance: } 4\\%',
            '\\text{Replication chance: } 5\\%',
            '\\text{Replication chance: } 6\\%',
        )
        blob1_sim.add_info(rep_chance_info)
        blob1_sim.align_info(frame = cues['example']['start'] + 960)
        rep_chance_info.morph_figure(1, start_frame = cues['example']['start'] + 1680)
        rep_chance_info.morph_figure(2, start_frame = cues['example']['start'] + 2040)
        rep_chance_info.morph_figure(3, start_frame = cues['example']['start'] + 2160)
        rep_chance_info.morph_figure(4, start_frame = cues['example']['start'] + 2280)
        rep_chance_info.morph_figure(5, start_frame = cues['example']['start'] + 2790)
        rep_chance_info.morph_figure(6, start_frame = cues['example']['start'] + 3330)


        equation.disappear(disappear_frame = scene_end)
        #blob1.disappear(disappear_frame = scene_end)
        blob1_sim.disappear(disappear_frame = scene_end)
'''
'''
class Finale(Scene):
    """docstring for [object Object]."""
    def __init__(self):
        super().__init__()
        #self.equation_duration = 340

        self.subscenes = collections.OrderedDict([
            ('deal_with_it', {'duration': 810}),
            ('evo', {'duration': 180})
        ])

        total_duration = 0
        for sub, attrs in self.subscenes.items():
            total_duration += attrs['duration']

        self.duration = total_duration

    def set_subscene_timing(self, frame):
        start = frame
        for sub, attrs in self.subscenes.items():
            attrs['start'] = start
            attrs['end'] = start + attrs['duration']
            start = attrs['end']


    def play_from_frame(self, frame):
        #Define flow
        self.set_subscene_timing(frame)
        cues = self.subscenes

        scene_end = frame + self.duration

        parent = bobject.Bobject()

        bun = import_object(
            'stanford_bunny',
            'creatures',
            location = (10, 5, 0),
            scale = 2
        )
        parent.add_subbobject(bun)
        sg = import_object(
            'sunglasses',
            location = (-3.188, 12, 1.889)
        )
        parent.add_subbobject(sg)

        parent.add_to_blender(
            appear_frame = cues['deal_with_it']['start'] - OBJECT_APPEARANCE_TIME
        )
        """bun.add_to_blender(
            appear_frame = cues['deal_with_it']['start'] - OBJECT_APPEARANCE_TIME
        )"""
        bun.move_to(
            new_angle = [5.5 * math.pi / 180, 0, 0],
            start_frame = cues['deal_with_it']['start'] - OBJECT_APPEARANCE_TIME,
            end_frame = cues['deal_with_it']['start']
        )
        bun.move_to(
            new_location = (0, 0, 0),
            new_scale = 4,
            start_frame = cues['deal_with_it']['start']
        )


        bun.move_to(
            new_angle = (0, 2 * math.pi, 0),
            start_frame = cues['deal_with_it']['start'] + 150,
            end_frame = cues['deal_with_it']['start'] + 270
        )

        """sg.add_to_blender(
            appear_frame = cues['deal_with_it']['start']
        )"""
        sg.move_to(
            start_frame = cues['deal_with_it']['start'] + 150,
            end_frame = cues['deal_with_it']['start'] + 270,
            new_location = (-3.196, 1.131, 1.889),
            new_angle = (-8.8 * math.pi / 180, -23.3 * math.pi / 180, 2 * math.pi / 180)
        )

        #Evolution
        evo = tex_bobject.TexBobject(
            '\\text{Evolution}',
            centered = True,
            scale = 3.5,
            location = (0, -4, 0)
        )
        evo.add_to_blender(
            appear_frame = cues['evo']['start'],
            animate = False,
            transition_time = 60
        )
        parent.move_to(
            new_location = (0, 2.5, 0),
            start_frame = cues['evo']['start'],
            end_frame = cues['evo']['start'] + 60
        )

        parent.disappear(
            disappear_frame = scene_end
        )
        evo.disappear(
            disappear_frame = scene_end
        )
'''
'''
class EndCard(Scene):
    """docstring for [object Object]."""
    def __init__(self):
        super().__init__()
        #self.equation_duration = 340

        self.subscenes = collections.OrderedDict([
            ('card', {'duration': 840}),
        ])

        total_duration = 0
        for sub, attrs in self.subscenes.items():
            total_duration += attrs['duration']

        self.duration = total_duration

    def set_subscene_timing(self, frame):
        start = frame
        for sub, attrs in self.subscenes.items():
            attrs['start'] = start
            attrs['end'] = start + attrs['duration']
            start = attrs['end']


    def play_from_frame(self, frame):
        #Define flow
        self.set_subscene_timing(frame)
        cues = self.subscenes

        scene_end = frame + self.duration

        blob = import_object(
            'boerd_blob',
            'creatures',
            scale = 3.4,
            location = (-8.5, 1.15, 0)
        )
        sub = tex_bobject.TexBobject(
            '\\text{Subscribe}',
            centered = True,
            location = (-8.5, -3.5, 0)
        )

        reddit = svg_bobject.SVGBobject(
            'reddit_logo',
            scale = 2,
            location = (-3.1, 5.3, 0)
        )
        discuss = tex_bobject.TexBobject(
            '\\text{Discuss}',
            centered = True,
            location = (0, -3.5, 0)
        )

        patreon = svg_bobject.SVGBobject(
            'Patreon_logomark',
            scale = 0.581,
            location = (5.393, 4.631, 0)
        )
        support = tex_bobject.TexBobject(
            '\\text{Support}',
            centered = True,
            location = (8.5, -3.5, 0)
        )



        blob.add_to_blender(
            appear_frame = 0
        )
        sub.add_to_blender(
            appear_frame = 0
        )

        reddit.add_to_blender(
            appear_frame = 120
        )
        discuss.add_to_blender(
            appear_frame = 120
        )

        patreon.add_to_blender(
            appear_frame = 240
        )
        support.add_to_blender(
            appear_frame = 240
        )


        remaining = [blob, sub, reddit, discuss, patreon, support]
        for bobj in remaining:
            bobj.disappear(disappear_frame = scene_end)
'''

'''
class NoReplicationWorld(Scene):
    def __init__(self):
        super().__init__()
        self.duration = 320

    def play_from_frame(self, frame):
        super().play_from_frame(frame)

        world = drawn_world.DrawnWorld(
            location = [-2, 0, 0],
            scale = 0.9,
            appear_frame = frame,
            start_delay = 20,
            duration = self.duration,
            #save = True,
            gene_updates = [
                ['color', 'creature_color_1', 'replication_modifier', 50, 100],
                ['color', 'creature_color_1', 'mutation_chance', 1, 100],
                ['color', 'creature_color_1', 'replication_modifier', 1, 101],
                ['color', 'creature_color_1', 'mutation_chance', DEFAULT_MUTATION_CHANCE, 101],
                ['color', 'creature_color_2', 'replication_modifier', 5, 101]
            ]
        )
        world.add_creatures_to_blender()
        world.set_world_keyframes()
        world.add_counter(
                    #shape = 'shape1',
                    color = 'creature_color_1',
                    #pre_string = "\\text{Balls: }",
                    pre_string = "\\text{Blue: }",
                    #location = [-7.5, -10, 0]
                    location = [8.5, 7, 0]
        ),
        world.add_counter(
                    color = 'creature_color_2',
                    pre_string = "\\text{Orange: }",
                    location = [8.5, 5.5, 0]
                    #location = [-7.5, -11.5, 0] \
        )

        tex = tex_bobject.TexBobject(
            "\\text{Whoa}",
            "\\text{Whaaaaat???}",
            location = (-11, -5, 0),
            size = 2
        )
        tex.add_to_blender(
            appear_frame = 60 + frame,
            animate = True
        )
        tex.morph_figure(1, frame + 200, 24)
'''

def main():
    pass


if __name__ == "__main__":
    main()
