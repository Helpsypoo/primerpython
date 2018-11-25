'''
When using draw_scenes.py to play this, clear should be set to false, and
inner_ear.blend should be open.
'''

import bpy
import collections
import math
from copy import deepcopy
#import imp

from constants import *
from helpers import *
#import scene
#imp.reload(scene)
from scene import Scene
import bobject
import svg_bobject
import tex_bobject
import tex_complex
import gesture

class TextScene(Scene):
    def __init__(self):
        self.subscenes = collections.OrderedDict([
            ('zoom', {'duration': 1000}),
            #('post_transplant', {'duration': 10}),\
        ])
        super().__init__()

    def play(self):
        super().play()
        #self.subscenes
        #self.duration
        #bpy.ops.wm.revert_mainfile()

        #These don't really need to be object methods ¯\_(ツ)_/¯
        #self.intro_card()
        self.outline()
        #self.transition_card()
        #self.end_card()

    def intro_card(self):
        logo = svg_bobject.SVGBobject(
            "UCSF_logo_signature",
            #location = (-5, 3.75, 0), #Centered position
            #scale = 0.26, #Centered scale
            location = [-10.675, -6.3, 0],
            scale = 0.128,
            color = 'color2',
            centered = True
        )
        baf = svg_bobject.SVGBobject(
            'BaFC_Arial',
            location = [4.325, -5.2, 0],
            scale = 1.85,
            color = 'color2',
            centered = True
        )
        vest = tex_bobject.TexBobject(
            '\\text{Vestibular Videos:}',
            location = [0, 4.5, 0],
            scale = 2,
            color = 'color2',
            centered = True,
            typeface = 'garamond'
        )
        title = tex_bobject.TexBobject(
            '\\text{Vestibular Neuritis}',
            location = [0, 1.5, 0],
            scale = 3.14,
            color = 'color2',
            centered = True,
            typeface = 'garamond'
        )
        vert = tex_bobject.TexBobject(
            '|',
            location = [-6.35, -4.74, 0],
            scale = [2, 5.32, 4],
            centered = True,
            color = 'color2',
        )

        logo.add_to_blender(appear_time = -1, animate = False)
        baf.add_to_blender(appear_time = -1, animate = False)
        vest.add_to_blender(appear_time = -1, animate = False)
        title.add_to_blender(appear_time = -1, animate = False)
        vert.add_to_blender(appear_time = -1, animate = False)

        for bobj in [logo, baf, vest, vert]:
            for handle in bobj.ref_obj.children:
                print(handle.name)
                print(handle.children[0].name)
                #For some reason, some handles have extra children
                try:
                    fade(
                        object = handle.children[0],
                        start_time = 0,
                        duration_time = 1,
                        fade_out = False
                    )
                except:
                    pass
        for bobj in [title]:
            for handle in bobj.ref_obj.children:
                print(handle.name)
                print(handle.children[0].name)
                #For some reason, some handles have extra children
                try:
                    fade(
                        object = handle.children[0],
                        start_time = 2,
                        duration_time = 1,
                        fade_out = False
                    )
                except:
                    pass

    def outline(self):
        vn = tex_bobject.TexBobject(
            "\\text{Vestibular Neuritis}",
            location = [0, 0, 0],
            centered = True,
            typeface = 'arial',
            scale = 3
        )
        vn.add_to_blender(
            appear_time = 0,
            subbobject_timing = [30] * 10 + [75] * 8
        )
        vn.move_to(
            new_location = [0, 3.5, 0],
            start_time = 2.5
        )

        acronym = tex_bobject.TexBobject(
            '\\bullet\\text{Vestibular system overview}',
            color = 'color2',
            typeface = 'arial'
        )
        cause = tex_bobject.TexBobject(
            '\\bullet\\text{Symptoms}',
            color = 'color2',
            typeface = 'arial'
        )
        treat = tex_bobject.TexBobject(
            '\\bullet\\text{Treatments}',
            color = 'color2',
            typeface = 'arial'
        )
        contents = tex_complex.TexComplex(
            acronym, cause, treat,
            location = [-9, 0.5, 0],
            scale = 1.5,
            multiline = True
        )
        contents.add_to_blender(
            appear_time = 4,
            subbobject_timing = [0, 35, 70]
        )
        contents.disappear(disappear_time = 7)
        #vn.disappear(disappear_time = 7)

        vn.move_to(
            new_location = [0, 5.5, 0],
            start_time = 6.5
        )

        itis = []
        for i in range(14, 18):
            itis.append(vn.lookup_table[0][i])
        for char in itis:
            char.color_shift(
                color = COLORS_SCALED[2],
                start_time = 8,
                duration_time = 2,
            )

        neur = []
        for i in range(10, 14):
            neur.append(vn.lookup_table[0][i])
        for char in neur:
            char.color_shift(
                color = COLORS_SCALED[2],
                start_time = 10.5,
                duration_time = 2,
            )

        vest = []
        for i in range(0, 10):
            vest.append(vn.lookup_table[0][i])
        for char in vest:
            char.color_shift(
                color = COLORS_SCALED[2],
                start_time = 13,
                duration_time = 2,
            )

        vn.disappear(disappear_time = 16)

    def transition_card(self):
        text = tex_bobject.TexBobject(
            #'\\text{The Cause of BPPV}',
            '\\text{Diagnosis and Treatment}',
            location = [0, 0, 0],
            scale = 2.5,
            color = 'color2',
            centered = True,
            typeface = 'arial'
        )
        text.add_to_blender(appear_time = -1, animate = False)

        for bobj in [text]:
            for handle in bobj.ref_obj.children:
                print(handle.name)
                print(handle.children[0].name)
                #For some reason, some handles have extra children
                try:
                    fade(
                        object = handle.children[0],
                        start_time = 0,
                        duration_time = 1,
                        fade_out = False
                    )
                except:
                    pass

    def end_card(self):
        logo = svg_bobject.SVGBobject(
            "UCSF_logo",
            #location = (-5, 3.75, 0), #Centered position
            #scale = 0.26, #Centered scale
            location = [0, 0, 0],
            scale = 0.121,
            color = 'color2',
            #centered = True,
        )
        baf = svg_bobject.SVGBobject(
            'BaFC_Arial',
            location = [5.2257280349731445, -0.26257357001304626, 0.0],
            scale = 2.23,
            color = 'color2',
            #centered = True,
        )
        logobaf = bobject.Bobject(
            logo, baf,
            location = [-11.57, 2.5, 0],
            #location = [0, 1.5, Z0],
            scale = 0.852,
            #centered = True
        )
        logobaf.add_to_blender(
            appear_time = 0,
            animate = False,
        )
        url = tex_bobject.TexBobject(
            '\\text{ohns.ucsf.edu/otology-neurotology/balance-and-falls}',
            location = [0, 0.8, 0],
            color = 'color2',
            name = 'url',
            typeface = 'arial',
            scale = 0.8,
            centered = True
        )
        url.add_to_blender(appear_time = 0)

        mpb_loc = [1, -4.25, 0]
        mpb = tex_bobject.TexBobject(
            '\\text{Made possible by:}',
            location = mpb_loc,
            color = 'color2',
            name = 'mpb',
            typeface = 'arial'
        )
        mzhf = tex_bobject.TexBobject(
            '\\text{Mount Zion Health Fund}',
            color = 'color2',
            scale = 1.2,
            location = [
                mpb_loc[0] + 0.5,
                mpb_loc[1] - 1.4,
                mpb_loc[2]
            ],
            name = 'mzhf',
            typeface = 'arial'
        )
        vpb_loc = [-13, -4.25, 0]
        vpb = tex_bobject.TexBobject(
            '\\text{Video produced by:}',
            color = 'color2',
            location = vpb_loc,
            name = 'vpb',
            typeface = 'arial'
        )
        jh = tex_bobject.TexBobject(
            '\\text{Justin Helps}',
            location = [
                vpb_loc[0] + 0.5,
                vpb_loc[1] - 1.4,
                vpb_loc[2]
            ],
            scale = 1.2,
            color = 'color2',
            name = 'jh',
            typeface = 'arial'
        )
        jds = tex_bobject.TexBobject(
            '\\text{Jeffrey D. Sharon, MD}',
            location = [
                vpb_loc[0] + 0.5,
                vpb_loc[1] - 2.8,
                vpb_loc[2]
            ],
            scale = 1.2,
            color = 'color2',
            name = 'jds',
            typeface = 'arial'
        )

        for bobj in [mpb, mzhf, vpb, jh, jds]:
            bobj.add_to_blender(
                appear_time = 0,
                animate = False
            )



'''
class AnatomyScene(Scene):
    def __init__(self):
        bpy.context.scene.cycles.caustics_reflective = False
        bpy.context.scene.cycles.caustics_refractive = False
        bpy.context.scene.cycles.use_transparent_shadows = False
        bpy.context.scene.cycles.transparent_max_bounces = 1000

        self.subscenes = collections.OrderedDict([
            ('zoom', {'duration': 1000}),
        ])
        super().__init__()

        self.brain_zoom_time = 86.5
        self.inner_zoom_time = 88.5
        self.vestibule_time = 94
        self.canals_time = 104
        self.utricle_time = 113.5
        self.otoconia_time = 116
        self.oto_wiggle_time = 118
        self.dislodged_time = 125
        self.only_posterior_time = 149

        #TODO: Determine timings
        self.epley_camera_time = 170

    def play(self):
        super().play()
        #self.subscenes
        #self.duration
        #bpy.ops.wm.revert_mainfile()

        #These don't really need to be object methods ¯\_(ツ)_/¯
        self.zoom()
        self.head_move_eyes_locked()
        self.nystagmus()
        #self.fade_contextual_objects()
        #self.highlight_sections()

    def fade_contextual_objects(self):
        print('Playing')
        skull = bpy.data.objects['Skull_Top']
        first_fade = [
            bpy.data.objects['robertot'],
            skull,
        ]
        second_fade = [
            bpy.data.objects['Temporal Bone 2 bone.outer'],
            bpy.data.objects['Brain'],
        ]
        third_fade = [
            bpy.data.objects['Incus VE'],
            bpy.data.objects['Malleus VE'],
            bpy.data.objects['Stapes VE'],
            bpy.data.objects['Eighth Nerve VE'],
            bpy.data.objects['Vestibular nerve origin'],
            bpy.data.objects['Cochlear_nerve_origin_2'],
        ]

        for i, obj in enumerate(first_fade):
            fade(
                object = obj,
                start_time = self.brain_zoom_time,
                duration_time = 1.5,
                extent = 1
            )
        for i, obj in enumerate(second_fade):
            fade(
                object = obj,
                start_time = self.inner_zoom_time,
                duration_time = 1.5,
                extent = 1
            )
        for i, obj in enumerate(third_fade):
            fade(
                object = obj,
                start_time = self.inner_zoom_time + 2,
                duration_time = 1.5,
                extent = 1 #0.95
            )

    def zoom(self):
        cues = self.subscenes['zoom']

        cam_bobj, cam_swivel = cam_and_swivel(
            cam_location = [0, 0, 90],
            cam_rotation_euler = [0, 0, 0],
            cam_name = "Camera Bobject",
            swivel_location = [0, 0, 0],
            swivel_rotation_euler = [math.pi / 2, 0, 70 * math.pi / 180],
            swivel_name = 'Cam swivel',
            #control_sun = True
        )
        cam_swivel.add_to_blender(appear_time = -1)

        sun = bpy.data.objects['Sun']
        sun_bobj = bobject.Bobject(objects = [sun])
        sun_bobj.move_to(
            new_angle = [-17 * math.pi / 180, 54 * math.pi / 180, 0],
            start_time = -1
        )

    def head_move_eyes_locked(self):
        skull = bpy.data.objects['Skull_Top']
        skull_bobj = bobject.Bobject(objects = [skull])
        skull_bobj.add_to_blender(appear_time = 0)

        eye_l = bpy.data.objects['eye_l']
        eye_l_initial_angle = list(eye_l.rotation_euler)
        eye_r = bpy.data.objects['eye_r']
        eye_r_initial_angle = list(eye_r.rotation_euler)

        angles = [
            [0, 0, 15 * math.pi / 180],
            [0, 0, -15 * math.pi / 180],
            [0, -10 * math.pi / 180, 0],
            [0, 0, 0]
        ]

        for i, angle in enumerate(angles):
            time = i / 2
            skull_bobj.move_to(
                new_angle = angle,
                start_time = time + 1
            )

            #Eyes aren't set up to work well as bobjects since I currently don't
            #plan to reuse them a bunch. Probably poor foresight. /shrug
            #They are also rotated in the z-direction with xyz euler angles, so
            #the corrections need to accound for this.
            eye_l.keyframe_insert(data_path = 'rotation_euler', frame = (time + 1) * FRAME_RATE)
            eye_l.rotation_euler = [
                eye_l_initial_angle[0] - angle[1],
                eye_l_initial_angle[1] + angle[0],
                eye_l_initial_angle[2] - angle[2]
            ]
            eye_l.keyframe_insert(data_path = 'rotation_euler', frame = (time + 1 + 0.5) * FRAME_RATE)

            eye_r.keyframe_insert(data_path = 'rotation_euler', frame = (time + 1) * FRAME_RATE)
            eye_r.rotation_euler = [
                eye_r_initial_angle[0] - angle[1],
                eye_r_initial_angle[1] + angle[0],
                eye_r_initial_angle[2] - angle[2]
            ]
            eye_r.keyframe_insert(data_path = 'rotation_euler', frame = (time + 1 + 0.5) * FRAME_RATE)

    def nystagmus(self):
        eye_l = bpy.data.objects['eye_l']
        eye_l_initial_angle = list(eye_l.rotation_euler)
        eye_r = bpy.data.objects['eye_r']
        eye_r_initial_angle = list(eye_r.rotation_euler)

        angle = [0, 0, 15 * math.pi / 180]
        start_time = 3.5

        for i in range(5):
            time = start_time + i * 0.325
            #Eyes aren't set up to work well as bobjects since I currently don't
            #plan to reuse them a bunch. Probably poor foresight. /shrug
            #They are also rotated in the z-direction with xyz euler angles, so
            #the corrections need to accound for this.
            eye_l.keyframe_insert(data_path = 'rotation_euler', frame = time * FRAME_RATE)
            eye_l.rotation_euler = [
                eye_l_initial_angle[0] + angle[1],
                eye_l_initial_angle[1] - angle[0],
                eye_l_initial_angle[2] + angle[2]
            ]
            eye_l.keyframe_insert(data_path = 'rotation_euler', frame = (time + 0.25) * FRAME_RATE)
            eye_l.rotation_euler = [
                eye_l_initial_angle[0],
                eye_l_initial_angle[1],
                eye_l_initial_angle[2]
            ]
            eye_l.keyframe_insert(data_path = 'rotation_euler', frame = (time + 0.325) * FRAME_RATE)

            eye_r.keyframe_insert(data_path = 'rotation_euler', frame = time * FRAME_RATE)
            eye_r.rotation_euler = [
                eye_r_initial_angle[0] + angle[1],
                eye_r_initial_angle[1] - angle[0],
                eye_r_initial_angle[2] + angle[2]
            ]
            eye_r.keyframe_insert(data_path = 'rotation_euler', frame = (time + 0.25) * FRAME_RATE)
            eye_r.rotation_euler = [
                eye_r_initial_angle[0],
                eye_r_initial_angle[1],
                eye_r_initial_angle[2]
            ]
            eye_r.keyframe_insert(data_path = 'rotation_euler', frame = (time + 0.325) * FRAME_RATE)

    def highlight_sections(self):
        #ear = bpy.data.objects['inner ear_from microCT']
        vest_shader = bpy.data.materials['vestibule'].node_tree.nodes['Principled BSDF']
        vest_color = vest_shader.inputs[0]
        vest_color.keyframe_insert(data_path = 'default_value', frame = self.vestibule_time * FRAME_RATE)
        old_value = list(vest_color.default_value)
        vest_color.default_value = [0, 1, 0, 1]
        vest_color.keyframe_insert(data_path = 'default_value', frame = (self.vestibule_time + 1) * FRAME_RATE)
        vest_color.keyframe_insert(data_path = 'default_value', frame = (self.vestibule_time + 11) * FRAME_RATE)
        vest_color.default_value = old_value
        vest_color.keyframe_insert(data_path = 'default_value', frame = (self.vestibule_time + 12) * FRAME_RATE)


        canal_shader = bpy.data.materials['canals'].node_tree.nodes['Principled BSDF']
        canal_color = canal_shader.inputs[0]
        canal_color.keyframe_insert(data_path = 'default_value', frame = self.canals_time * FRAME_RATE)
        old_value = list(canal_color.default_value)
        canal_color.default_value = [0, 1, 0, 1]
        canal_color.keyframe_insert(data_path = 'default_value', frame = (self.canals_time + 1) * FRAME_RATE)
        canal_color.keyframe_insert(data_path = 'default_value', frame = (self.canals_time + 6.5) * FRAME_RATE)
        canal_color.default_value = old_value
        canal_color.keyframe_insert(data_path = 'default_value', frame = (self.canals_time + 7.5) * FRAME_RATE)
        #Also the posterior canal, which is separate, for later
        canal_shader = bpy.data.materials['posterior'].node_tree.nodes['Principled BSDF']
        canal_color = canal_shader.inputs[0]
        canal_color.keyframe_insert(data_path = 'default_value', frame = self.canals_time * FRAME_RATE)
        old_value = list(canal_color.default_value)
        canal_color.default_value = [0, 1, 0, 1]
        canal_color.keyframe_insert(data_path = 'default_value', frame = (self.canals_time + 1) * FRAME_RATE)
        canal_color.keyframe_insert(data_path = 'default_value', frame = (self.canals_time + 6.5) * FRAME_RATE)
        canal_color.default_value = old_value
        canal_color.keyframe_insert(data_path = 'default_value', frame = (self.canals_time + 7.5) * FRAME_RATE)

        #Now just the posterior
        canal_shader = bpy.data.materials['posterior'].node_tree.nodes['Principled BSDF']
        canal_color = canal_shader.inputs[0]
        canal_color.keyframe_insert(data_path = 'default_value', frame = self.only_posterior_time * FRAME_RATE)
        old_value = list(canal_color.default_value)
        canal_color.default_value = [0, 1, 0, 1]
        canal_color.keyframe_insert(data_path = 'default_value', frame = (self.only_posterior_time + 1) * FRAME_RATE)
        canal_color.keyframe_insert(data_path = 'default_value', frame = (self.only_posterior_time + 19) * FRAME_RATE)
        canal_color.default_value = old_value
        canal_color.keyframe_insert(data_path = 'default_value', frame = (self.only_posterior_time + 20) * FRAME_RATE)
'''
