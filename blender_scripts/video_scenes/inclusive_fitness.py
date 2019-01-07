import collections
import math
from random import random, uniform, randrange
import bpy

import imp
#import scene
#imp.reload(scene)
from scene import Scene

import svg_bobject
imp.reload(svg_bobject)
import tex_bobject
imp.reload(tex_bobject)
import tex_complex
imp.reload(tex_complex)
import gesture
imp.reload(gesture)
import graph_bobject
imp.reload(graph_bobject)
import natural_sim
imp.reload(natural_sim)
import table_bobject
imp.reload(table_bobject)

import blobject
imp.reload(blobject)
from blobject import Blobject

import helpers
imp.reload(helpers)
from helpers import *


class InclusiveFitness(Scene):
    def __init__(self):
        self.subscenes = collections.OrderedDict([
            ('card', {'duration': 10})
        ])
        super().__init__()

    def play(self):
        super().play()

        #self.intro()
        self.sim_rules()
        #self.green_beard()
        #self.end_card()
        #self.thumbnail()

    def intro(self):
        return

        for i, thing in enumerate(to_disappear):
            thing.disappear(disappear_time = 6.5 - (len(to_disappear) - 1 - i) * 0.05)

    def sim_rules(self):
        cam_bobj, cam_swivel = cam_and_swivel(
            cam_location = [0, 0, 34],
            cam_rotation_euler = [0, 0, 0],
            cam_name = "Camera Bobject",
            swivel_location = [0, 0, 0],
            swivel_rotation_euler = [74 * math.pi / 180, 0, 0],
            swivel_name = 'Cam swivel',
            #control_sun = True
        )
        cam_swivel.add_to_blender(appear_time = -1, animate = False)

        world = natural_sim.DrawnNaturalSim(
            scale = 2.8,
            food_count = 50,
            #initial_energy = 1500,
            #dimensions = [75, 75],
            #sim = 'ns_env_intro_4',
            #initial_creatures = 3,
            location = [0, 0, 0],
            day_length_style = 'fixed_speed',
            #day_length_style = 'fixed_length'
            #mutation_switches = [False, False, False]
        )
        num_days = 1
        for i in range(num_days):
            save = False
            if i == num_days - 1:
                save = True
            world.sim.sim_next_day(save = save)

        world.sim.date_records[0]['anim_durations'] = {
            'dawn' : 1, #Put out food and creatures
            'morning' : 0.5, #pause after setup
            'day' : 2, #creatures go at it
            'evening' : 0.5, #pause before reset
            'night' : 0.5 #reset
        }
        world.add_to_blender(appear_time = 0, start_delay = 0)




    def green_beard(self):

        blob = Blobject(wiggle = True, mouth = True)
        blob.add_to_blender(appear_time = 0)
        blob.add_beard(mat = 'color7')
        blob.hello(start_time = 0, end_time = 4)

        '''beard = import_object(
            'beard', 'misc',
            location = [0.86383, -1.79778, 0.29876],
            rotation_euler = [-40.8 * math.pi / 180, 68.3 * math.pi / 180, -5.77 * math.pi / 180],
            scale = [1.377, 1.377, 0.685]
        )
        beard.ref_obj.parent = blob.ref_obj.children[0]
        beard.ref_obj.parent_bone = blob.ref_obj.children[0].pose.bones["brd_bone_neck"].name
        beard.ref_obj.parent_type = 'BONE'
        beard.add_to_blender(appear_time = 0)'''

    def end_card(self):
        cues = self.subscenes
        scene_end = self.duration

        bpy.ops.mesh.primitive_plane_add()
        play_bar = bpy.context.object
        play_bar.scale[0] = 15
        play_bar.scale[1] = 90 / 720 * 8.4
        play_bar.location = [0, -8.4 + play_bar.scale[1], -0.01]

        bpy.ops.mesh.primitive_plane_add()
        vid_rec = bpy.context.object
        vid_rec.scale[0] = 410 / 1280 * 15
        vid_rec.scale[1] = 230 / 720 * 8.4
        vid_rec.location = [9, -3, -0.01]
        apply_material(vid_rec, 'color6')

        bpy.ops.mesh.primitive_cylinder_add()
        sub_cir = bpy.context.object
        sub_cir.scale = [98 / 1280 * 30, 98 / 1280 * 30, 0]
        sub_cir.location = [-11, 3.2, -0.01]

        #Whole end area
        bpy.ops.mesh.primitive_plane_add()
        end_area = bpy.context.object
        end_area.scale[0] = 1225 / 1280 * 15
        end_area.scale[1] = 518 / 720 * 8.4
        end_area.location = [0, 0.2, -0.15]

        logo = svg_bobject.SVGBobject(
            "Layer",
            #file_name = "PrimerLogoWhite",
            location = (-8.7, 3, 0),
            scale = 1.4
        )
        for bobj in logo.rendered_curve_bobjects:
            apply_material(bobj.ref_obj.children[0], 'color2')
        stroke = logo.rendered_curve_bobjects[0]
        apply_material(stroke.ref_obj.children[0], 'color3')
        logo.morph_chains[0][0].ref_obj.location[2] = -1
        logo.add_to_blender(
            appear_time = cues['card']['start'],
            #subbobject_timing = [90, 30, 40, 50, 60, 70, 80],
            subbobject_timing = [42, 30, 33, 36, 39, 42, 45],
            animate = True
        )

        patreon = import_object(
            'patreon', 'svgblend',
            scale = 2.297,
            location = (-11, -3, 0),
            name = 'Patreon'
        )
        patreon.add_to_blender(appear_time = 0)
        thanks = tex_bobject.TexBobject(
            '\\text{Special thanks:}',
            location = [-8.35, -1.4, 0],
            color = 'color2'
        )
        thanks.add_to_blender(appear_time = 0)
        js = tex_bobject.TexBobject(
            '\\text{Jordan Scales}',
            location = [-7.8, -2.75, 0],
            color = 'color2',
            scale = 1
        )
        js.add_to_blender(appear_time = 0.5)

        ap = tex_bobject.TexBobject(
            '\\text{Anonymous Patrons}',
            location = [-7.8, -4, 0],
            color = 'color2',
            scale = 1
        )
        ap.add_to_blender(appear_time = 0.75)


        remaining = [logo, patreon, thanks, js, ap]
        for thing in remaining:
            thing.disappear(disappear_time = 2.5)

    def thumbnail(self):
        sg = svg_bobject.SVGBobject(
            "the_selfish_gene_century_italic",
            #location = (-5, 3.75, 0), #Centered position
            #scale = 0.26, #Centered scale
            location = [-6.7, 4.9, 0],
            scale = 4.6,
            color = 'color2',
            centered = True
        )
        sg.add_to_blender(appear_time = 0)

        for i in range(3, 10):
            sg.lookup_table[0][i].color_shift(
                color = COLORS_SCALED[5],
                start_time = -1,
                duration_time = None
            )


        d = import_object(
            'dna_two_strand', 'biochem',
            location = [7, 0, 0],#[7, 0, 0],
            rotation_euler = [0, 0, 0 * math.pi / 180],
            scale = 7
        )
        d.add_to_blender(appear_time = 0)

        d.spin(start_time = 0, spin_rate = 0.1)
        #d.tweak_colors_recursive()

        '''gd = import_object(
            'dna_two_strand', 'biochem',
            location = [7, 3.5, 0],#[7, 0, 0],
            rotation_euler = [0, 0, -90 * math.pi / 180],
            scale = 4.5#7
        )
        gd.add_to_blender(appear_time = 0)

        gd.spin(start_time = 0, spin_rate = 0.1)'''

        def make_clear_recursive(obj):
            apply_material(obj, 'trans_color2', intensity = 0.7)
            for child in obj.children:
                make_clear_recursive(child)

        make_clear_recursive(d.ref_obj.children[0])
