import collections
import math
from random import random, uniform, randrange
import bpy

import imp
import scene
imp.reload(scene)
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

import helpers
imp.reload(helpers)
from helpers import *

BLOB_VOLUME_DENSITY = 0.04

class SelfishGene(Scene):
    def __init__(self):
        self.subscenes = collections.OrderedDict([
            ('card', {'duration': 10})
        ])
        super().__init__()

    def play(self):
        super().play()

        #self.end_card()
        self.banner()
        #self.banner_angled()

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

    def banner(self):
        cam_bobj, cam_swivel = cam_and_swivel(
            cam_location = [0, 0, 32.8],
            cam_rotation_euler = [0, 0, 0],
            cam_name = "Camera Bobject",
            swivel_location = [0, 0, 0],
            swivel_rotation_euler = [0, 0, 0],
            swivel_name = 'Cam swivel',
            #control_sun = True
        )
        cam_swivel.add_to_blender(appear_time = -1)

        logo = svg_bobject.SVGBobject(
            "Layer",
            #file_name = "PrimerLogoWhite",
            location = [0, 0, 0],
            rotation_euler = [0, 0, 0],
            scale = 2,
            centered = True
        )
        for bobj in logo.rendered_curve_bobjects:
            apply_material(bobj.ref_obj.children[0], 'color2')
        stroke = logo.rendered_curve_bobjects[0]
        apply_material(stroke.ref_obj.children[0], 'color3')
        logo.morph_chains[0][0].ref_obj.location[2] = -1
        logo.add_to_blender(
            appear_time = -1,
            #subbobject_timing = [90, 30, 40, 50, 60, 70, 80],
            #subbobject_timing = [42, 30, 33, 36, 39, 42, 45],
            animate = False
        )

        b_blob = import_object(
            'boerd_blob', 'creatures',
            scale = 2,
            location = [-9, 0, 0],
            rotation_euler = [0, 20 * math.pi / 180, 0]
        )
        b_blob.add_to_blender(appear_time = 0, animate = False)
        apply_material(b_blob.ref_obj.children[0].children[0], 'creature_color3')
        b_blob.hello(
            start_time = 2,
            end_time = 8
        )

        r_blob = import_object(
            'boerd_blob', 'creatures',
            scale = 2,
            location = [12.5, 0, 0],
            rotation_euler = [0, 0, 0],
            #wiggle = True
        )
        r_blob.add_to_blender(appear_time = 0, animate = False)
        apply_material(r_blob.ref_obj.children[0].children[0], 'creature_color6')
        r_blob.evil_pose(
            start_time = 6,
            end_time = 10
        )

        g_blob = import_object(
            'boerd_blob', 'creatures',
            scale = 2,
            location = [9, 0, 0],
            rotation_euler = [0, - 10 * math.pi / 180, 0],
            wiggle = True,
            cycle_length = 600
        )
        g_blob.add_to_blender(appear_time = 0, animate = False)
        apply_material(g_blob.ref_obj.children[0].children[0], 'creature_color7')

        o_blob = import_object(
            'boerd_blob', 'creatures',
            scale = 2,
            location = [-12.5, 0, 0],
            rotation_euler = [0, 0, 0],
            #wiggle = True
        )
        o_blob.add_to_blender(appear_time = 0, animate = False)
        apply_material(o_blob.ref_obj.children[0].children[0], 'creature_color4')


    def banner_angled(self):
        cam_bobj, cam_swivel = cam_and_swivel(
            cam_location = [0, 0, 32.8],
            cam_rotation_euler = [0, 0, 0],
            cam_name = "Camera Bobject",
            swivel_location = [0, 0, 0],
            swivel_rotation_euler = [70 * math.pi / 180, 0, 0],
            swivel_name = 'Cam swivel',
            control_sun = True
        )
        cam_swivel.add_to_blender(appear_time = -1)

        logo = svg_bobject.SVGBobject(
            "Layer",
            #file_name = "PrimerLogoWhite",
            location = [0, 0, 0],
            rotation_euler = [math.pi / 2, 0, 0],
            scale = 4,
            centered = True
        )
        for bobj in logo.rendered_curve_bobjects:
            apply_material(bobj.ref_obj.children[0], 'color2')
        stroke = logo.rendered_curve_bobjects[0]
        apply_material(stroke.ref_obj.children[0], 'color3')
        logo.morph_chains[0][0].ref_obj.location[2] = -1
        logo.add_to_blender(
            appear_time = -1,
            #subbobject_timing = [90, 30, 40, 50, 60, 70, 80],
            #subbobject_timing = [42, 30, 33, 36, 39, 42, 45],
            animate = False
        )

        b_blob = import_object(
            'boerd_blob', 'creatures',
            scale = 2,
            location = [2, -10, 0],
            rotation_euler = [math.pi / 2, 0, 0],
            wiggle = True
        )
        b_blob.add_to_blender(appear_time = 0)
        apply_material(b_blob.ref_obj.children[0].children[0], 'creature_color3')


        r_blob = import_object(
            'boerd_blob', 'creatures',
            scale = 2,
            location = [-7, -7, 0],
            rotation_euler = [math.pi / 2, 0, 100 * math.pi / 180],
            wiggle = True
        )
        r_blob.add_to_blender(appear_time = 0)
        apply_material(r_blob.ref_obj.children[0].children[0], 'creature_color6')

        g_blob = import_object(
            'boerd_blob', 'creatures',
            scale = 2,
            location = [-5, -5, 0],
            rotation_euler = [math.pi / 2, 0, -10 * math.pi / 180],
            wiggle = True
        )
        g_blob.add_to_blender(appear_time = 0)
        apply_material(g_blob.ref_obj.children[0].children[0], 'creature_color7')

        o_blob = import_object(
            'boerd_blob', 'creatures',
            scale = 2,
            location = [10, -6, 0],
            rotation_euler = [math.pi / 2, 0, math.pi / 2],
            wiggle = True
        )
        o_blob.add_to_blender(appear_time = 0)
        apply_material(o_blob.ref_obj.children[0].children[0], 'creature_color4')
