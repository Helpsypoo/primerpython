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
        #self.inner_ear_intro()
        #self.surgery_routes()
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
            '\\text{Superior Canal Dehiscence Syndrome}',
            location = [0, 2, 0],
            scale = 2,
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
        sc = tex_bobject.TexBobject(
            "\\text{Superior Canal}",
            location = [0, 1.5, 0],
            centered = True,
            typeface = 'arial',
            scale = 2.5
        )
        sc.add_to_blender(
            appear_time = 0,
            subbobject_timing = [30] * 8 + [75] * 5
        )
        sc.move_to(
            new_location = [0, 5, 0],
            start_time = 4
        )

        ds = tex_bobject.TexBobject(
            "\\text{Dehiscence Syndrome}",
            location = [0, -1.5, 0],
            centered = True,
            typeface = 'arial',
            scale = 2.5
        )
        ds.add_to_blender(
            appear_time = 2,
            subbobject_timing = [30] * 10 + [75] * 8
        )
        ds.move_to(
            new_location = [0, 2, 0],
            start_time = 4
        )

        acronym = tex_bobject.TexBobject(
            '\\bullet\\text{Inner ear overview}',
            color = 'color2',
            typeface = 'arial'
        )
        cause = tex_bobject.TexBobject(
            '\\bullet\\text{Symptoms}',
            color = 'color2',
            typeface = 'arial'
        )
        treat = tex_bobject.TexBobject(
            '\\bullet\\text{Diagnosis and treatment}',
            color = 'color2',
            typeface = 'arial'
        )
        contents = tex_complex.TexComplex(
            acronym, cause, treat,
            location = [-9, -1.5, 0],
            scale = 1.5,
            multiline = True
        )
        contents.add_to_blender(
            appear_time = 4,
            subbobject_timing = [35, 70, 105]
        )
        contents.disappear(disappear_time = 7)
        #vn.disappear(disappear_time = 7)

        sc.move_to(
            new_location = [-7.5, 6, 0],
            new_scale = 1.6,
            start_time = 6.5
        )
        ds.move_to(
            new_location = [5.2, 6, 0],
            new_scale = 1.6,
            start_time = 6.5
        )

        s = []
        for i in range(0, 13):
            s.append(sc.lookup_table[0][i])
        for char in s:
            char.color_shift(
                color = COLORS_SCALED[2],
                start_time = 8,
                duration_time = 2,
            )
        for char in s:
            char.color_shift(
                color = COLORS_SCALED[2],
                start_time = 13,
                duration_time = 2,
            )

        d = []
        for i in range(0, 10):
            d.append(ds.lookup_table[0][i])
        for char in d:
            char.color_shift(
                color = COLORS_SCALED[2],
                start_time = 10.5,
                duration_time = 2,
            )

        sc.disappear(disappear_time = 16)
        #sc.move_to(new_location = [0, 5.5, 0], start_time = 15.75)
        ds.disappear(disappear_time = 16)
        #ds.move_to(new_location = [0, 5.5, 0], start_time = 15.75)

    def inner_ear_intro(self):
        cam_bobj, cam_swivel = cam_and_swivel(
            cam_location = [0, 0, 5],
            cam_rotation_euler = [0, 0, 0],
            cam_name = "Camera Bobject",
            swivel_location = [0.2, 0, 0.25],
            swivel_rotation_euler = [math.pi / 2, 0,  55 * math.pi / 180],
            swivel_name = 'Cam swivel',
            #control_sun = True
        )
        cam_swivel.add_to_blender(appear_time = -1)
        cam_bobj.ref_obj.children[0].data.clip_end = 200

        start_time = 15
        coch_time = 18.5
        vest_time = 20.5
        sup_time = 29.5
        temp_time = 32.5
        dehiscence_time = 39.5
        head_time = 48

        r_inner_ear = bpy.data.objects['inner ear_from microCT']
        t_bone = bpy.data.objects['Temporal Bone 2 bone.outer']
        skin = bpy.data.objects['robertot']
        to_keep = [r_inner_ear, t_bone, skin]
        for obj in bpy.data.objects:
            if obj not in to_keep:
                obj.hide = True
                obj.hide_render = True

        slots = r_inner_ear.material_slots
        v_sys_mats = [
            slots[1].material,
            slots[2].material,
            slots[3].material,
            slots[4].material
        ]
        coch_mat = slots[0].material
        sup_mat = slots[2].material

        for mat in v_sys_mats + [coch_mat]:
            nodes = mat.node_tree.nodes
            mix = nodes['Mix Shader']
            mix.inputs[0].default_value = 0
            princ = nodes['Principled BSDF']
            color = princ.inputs[0]

            if mat == coch_mat:
                starting_color = list(color.default_value)
                color.keyframe_insert(
                    data_path = 'default_value',
                    frame = coch_time * FRAME_RATE
                )
                color.default_value = [0, 1, 0, 1]
                color.keyframe_insert(
                    data_path = 'default_value',
                    frame = coch_time * FRAME_RATE + OBJECT_APPEARANCE_TIME
                )

                color.keyframe_insert(
                    data_path = 'default_value',
                    frame = (vest_time - 0.5) * FRAME_RATE
                )
                color.default_value = starting_color
                color.keyframe_insert(
                    data_path = 'default_value',
                    frame = (vest_time - 0.5) * FRAME_RATE + OBJECT_APPEARANCE_TIME
                )

            if mat != coch_mat and mat != sup_mat:
                starting_color = list(color.default_value)
                color.keyframe_insert(
                    data_path = 'default_value',
                    frame = vest_time * FRAME_RATE
                )
                color.default_value = [0, 1, 0, 1]
                color.keyframe_insert(
                    data_path = 'default_value',
                    frame = vest_time * FRAME_RATE + OBJECT_APPEARANCE_TIME
                )

                color.keyframe_insert(
                    data_path = 'default_value',
                    frame = (sup_time - 0.5) * FRAME_RATE
                )
                color.default_value = starting_color
                color.keyframe_insert(
                    data_path = 'default_value',
                    frame = (sup_time - 0.5) * FRAME_RATE + OBJECT_APPEARANCE_TIME
                )

            if mat == sup_mat:
                starting_color = list(color.default_value)
                color.keyframe_insert(
                    data_path = 'default_value',
                    frame = vest_time * FRAME_RATE
                )
                color.default_value = [0, 1, 0, 1]
                color.keyframe_insert(
                    data_path = 'default_value',
                    frame = vest_time * FRAME_RATE + OBJECT_APPEARANCE_TIME
                )

                '''color.keyframe_insert(
                    data_path = 'default_value',
                    frame = (temp_time - 0.5) * FRAME_RATE
                )
                color.default_value = starting_color
                color.keyframe_insert(
                    data_path = 'default_value',
                    frame = (temp_time - 0.5) * FRAME_RATE + OBJECT_APPEARANCE_TIME
                )'''

        #Fade in temporal bone, then Dehiscence
        for slot in t_bone.material_slots:
            mat = slot.material
            nodes = mat.node_tree.nodes
            mix = nodes['Mix Shader']
            mix.inputs[0].default_value = 1
            #princ = nodes['Principled BSDF']
            #color = princ.inputs[0]

            mix.inputs[0].keyframe_insert(
                data_path = 'default_value',
                frame = (temp_time) * FRAME_RATE
            )
            mix.inputs[0].default_value = 0.8
            mix.inputs[0].keyframe_insert(
                data_path = 'default_value',
                frame = (temp_time) * FRAME_RATE + OBJECT_APPEARANCE_TIME
            )
            if mat == t_bone.material_slots[1].material: #Dehiscence
                mix.inputs[0].default_value = 0.4
                mix.inputs[0].keyframe_insert(
                    data_path = 'default_value',
                    frame = (dehiscence_time) * FRAME_RATE + OBJECT_APPEARANCE_TIME
                )

                mix2 = nodes['Mix Shader.001'].inputs[0]
                mix2.default_value = 0
                mix2.keyframe_insert(
                    data_path = 'default_value',
                    frame = dehiscence_time * FRAME_RATE
                )
                mix2.default_value = 1
                mix2.keyframe_insert(
                    data_path = 'default_value',
                    frame = dehiscence_time * FRAME_RATE + OBJECT_APPEARANCE_TIME
                )
                em = nodes['Emission']
                color = em.inputs[0]
                '''color.default_value = [1, 1, 1, 1]
                color.keyframe_insert(
                    data_path = 'default_value',
                    frame = turn_red_time * FRAME_RATE
                )'''
                color.default_value = [1, 0, 0, 1]
                '''color.keyframe_insert(
                    data_path = 'default_value',
                    frame = turn_red_time * FRAME_RATE + 2 * OBJECT_APPEARANCE_TIME
                )'''

        #Fade in head for context
        mat = skin.material_slots[0].material
        nodes = mat.node_tree.nodes
        mix = nodes['Mix Shader']
        mix.inputs[0].default_value = 1
        #princ = nodes['Principled BSDF']
        #color = princ.inputs[0]

        mix.inputs[0].keyframe_insert(
            data_path = 'default_value',
            frame = (head_time - 0.5) * FRAME_RATE
        )
        mix.inputs[0].default_value = 0.9
        mix.inputs[0].keyframe_insert(
            data_path = 'default_value',
            frame = (head_time - 0.5) * FRAME_RATE + OBJECT_APPEARANCE_TIME
        )

        #Zoom out for temporal bone
        cam_swivel.move_to(
            new_location = [0.2, 0, 1.25],
            start_time = temp_time - 0.5,
            end_time = temp_time + 2 * OBJECT_APPEARANCE_TIME / FRAME_RATE
        )
        cam_bobj.move_to(
            new_location = [0, 0, 24],
            start_time = temp_time - 0.5,
            end_time = temp_time + 2 * OBJECT_APPEARANCE_TIME / FRAME_RATE
        )

        #Zoom out for head context
        cam_swivel.move_to(
            new_location = [0, 5.1, -2],
            start_time = head_time - 0.5,
            end_time = head_time + 2 * OBJECT_APPEARANCE_TIME / FRAME_RATE
        )
        cam_bobj.move_to(
            new_location = [0, 0, 100],
            start_time = head_time - 0.5,
            end_time = head_time + 2 * OBJECT_APPEARANCE_TIME / FRAME_RATE
        )

        #swivel_rotation_euler = [75 * math.pi / 180, 0, 45 * math.pi / 180],


        #Spinnnnnnn camera
        cam_swivel.spin(
            spin_rate = 0.11,
            start_time = start_time,
            axis = 2
        )

    def surgery_routes(self):
        #Continuation of inner_ear_intro

        cam_bobj, cam_swivel = cam_and_swivel(
            cam_location = [0, 0, 5],
            cam_rotation_euler = [0, 0, 0],
            cam_name = "Camera Bobject",
            swivel_location = [0.2, 0, 0.25],
            swivel_rotation_euler = [math.pi / 2, 0,  55 * math.pi / 180],
            swivel_name = 'Cam swivel',
            #control_sun = True
        )
        cam_swivel.add_to_blender(appear_time = -1)
        cam_bobj.ref_obj.children[0].data.clip_end = 200

        start_time = 15
        coch_time = 18.5
        vest_time = 20.5
        sup_time = 29.5
        temp_time = 32.5
        dehiscence_time = 39.5
        head_time = 48

        behind_time = 55

        r_inner_ear = bpy.data.objects['inner ear_from microCT']
        t_bone = bpy.data.objects['Temporal Bone 2 bone.outer']
        skin = bpy.data.objects['robertot']
        to_keep = [r_inner_ear, t_bone, skin]
        for obj in bpy.data.objects:
            if obj not in to_keep:
                obj.hide = True
                obj.hide_render = True

        slots = r_inner_ear.material_slots
        v_sys_mats = [
            slots[1].material,
            slots[2].material,
            slots[3].material,
            slots[4].material
        ]
        coch_mat = slots[0].material
        sup_mat = slots[2].material

        for mat in v_sys_mats + [coch_mat]:
            nodes = mat.node_tree.nodes
            mix = nodes['Mix Shader']
            mix.inputs[0].default_value = 0
            princ = nodes['Principled BSDF']
            color = princ.inputs[0]

            if mat == coch_mat:
                starting_color = list(color.default_value)
                color.keyframe_insert(
                    data_path = 'default_value',
                    frame = coch_time * FRAME_RATE
                )
                color.default_value = [0, 1, 0, 1]
                color.keyframe_insert(
                    data_path = 'default_value',
                    frame = coch_time * FRAME_RATE + OBJECT_APPEARANCE_TIME
                )

                color.keyframe_insert(
                    data_path = 'default_value',
                    frame = (vest_time - 0.5) * FRAME_RATE
                )
                color.default_value = starting_color
                color.keyframe_insert(
                    data_path = 'default_value',
                    frame = (vest_time - 0.5) * FRAME_RATE + OBJECT_APPEARANCE_TIME
                )

            if mat != coch_mat and mat != sup_mat:
                starting_color = list(color.default_value)
                color.keyframe_insert(
                    data_path = 'default_value',
                    frame = vest_time * FRAME_RATE
                )
                color.default_value = [0, 1, 0, 1]
                color.keyframe_insert(
                    data_path = 'default_value',
                    frame = vest_time * FRAME_RATE + OBJECT_APPEARANCE_TIME
                )

                color.keyframe_insert(
                    data_path = 'default_value',
                    frame = (sup_time - 0.5) * FRAME_RATE
                )
                color.default_value = starting_color
                color.keyframe_insert(
                    data_path = 'default_value',
                    frame = (sup_time - 0.5) * FRAME_RATE + OBJECT_APPEARANCE_TIME
                )

            if mat == sup_mat:
                starting_color = list(color.default_value)
                color.keyframe_insert(
                    data_path = 'default_value',
                    frame = vest_time * FRAME_RATE
                )
                color.default_value = [0, 1, 0, 1]
                color.keyframe_insert(
                    data_path = 'default_value',
                    frame = vest_time * FRAME_RATE + OBJECT_APPEARANCE_TIME
                )

                '''color.keyframe_insert(
                    data_path = 'default_value',
                    frame = (temp_time - 0.5) * FRAME_RATE
                )
                color.default_value = starting_color
                color.keyframe_insert(
                    data_path = 'default_value',
                    frame = (temp_time - 0.5) * FRAME_RATE + OBJECT_APPEARANCE_TIME
                )'''

        #Fade in temporal bone, then Dehiscence
        for slot in t_bone.material_slots:
            mat = slot.material
            nodes = mat.node_tree.nodes
            mix = nodes['Mix Shader']
            mix.inputs[0].default_value = 1
            #princ = nodes['Principled BSDF']
            #color = princ.inputs[0]

            mix.inputs[0].keyframe_insert(
                data_path = 'default_value',
                frame = (temp_time) * FRAME_RATE
            )
            mix.inputs[0].default_value = 0.8
            mix.inputs[0].keyframe_insert(
                data_path = 'default_value',
                frame = (temp_time) * FRAME_RATE + OBJECT_APPEARANCE_TIME
            )
            if mat == t_bone.material_slots[1].material: #Dehiscence
                mix.inputs[0].default_value = 0.4
                mix.inputs[0].keyframe_insert(
                    data_path = 'default_value',
                    frame = (dehiscence_time) * FRAME_RATE + OBJECT_APPEARANCE_TIME
                )

                mix2 = nodes['Mix Shader.001'].inputs[0]
                mix2.default_value = 0
                mix2.keyframe_insert(
                    data_path = 'default_value',
                    frame = dehiscence_time * FRAME_RATE
                )
                mix2.default_value = 1
                mix2.keyframe_insert(
                    data_path = 'default_value',
                    frame = dehiscence_time * FRAME_RATE + OBJECT_APPEARANCE_TIME
                )
                em = nodes['Emission']
                color = em.inputs[0]
                '''color.default_value = [1, 1, 1, 1]
                color.keyframe_insert(
                    data_path = 'default_value',
                    frame = turn_red_time * FRAME_RATE
                )'''
                color.default_value = [1, 0, 0, 1]
                '''color.keyframe_insert(
                    data_path = 'default_value',
                    frame = turn_red_time * FRAME_RATE + 2 * OBJECT_APPEARANCE_TIME
                )'''

        #Fade in head for context
        mat = skin.material_slots[0].material
        nodes = mat.node_tree.nodes
        mix = nodes['Mix Shader']
        mix.inputs[0].default_value = 1
        #princ = nodes['Principled BSDF']
        #color = princ.inputs[0]

        mix.inputs[0].keyframe_insert(
            data_path = 'default_value',
            frame = (head_time - 0.5) * FRAME_RATE
        )
        mix.inputs[0].default_value = 0.9
        mix.inputs[0].keyframe_insert(
            data_path = 'default_value',
            frame = (head_time - 0.5) * FRAME_RATE + OBJECT_APPEARANCE_TIME
        )

        #Zoom out for temporal bone
        cam_swivel.move_to(
            new_location = [0.2, 0, 1.25],
            start_time = temp_time - 0.5,
            end_time = temp_time + 2 * OBJECT_APPEARANCE_TIME / FRAME_RATE
        )
        cam_bobj.move_to(
            new_location = [0, 0, 24],
            start_time = temp_time - 0.5,
            end_time = temp_time + 2 * OBJECT_APPEARANCE_TIME / FRAME_RATE
        )

        #Zoom out for head context
        cam_swivel.move_to(
            new_location = [0, 5.1, -2],
            start_time = head_time - 0.5,
            end_time = head_time + 2 * OBJECT_APPEARANCE_TIME / FRAME_RATE
        )
        cam_bobj.move_to(
            new_location = [0, 0, 100],
            start_time = head_time - 0.5,
            end_time = head_time + 2 * OBJECT_APPEARANCE_TIME / FRAME_RATE
        )

        #swivel_rotation_euler = [75 * math.pi / 180, 0, 45 * math.pi / 180],

        #Go behind head for surgery view
        cam_swivel.move_to(
            new_location = [0, -1.9, 0.6],
            new_angle = [math.pi / 2, 0, - math.pi / 2],
            start_time = behind_time - 0.5,
            end_time = behind_time + 2 * OBJECT_APPEARANCE_TIME / FRAME_RATE
        )
        cam_bobj.move_to(
            new_location = [0, 0, 20],
            start_time = behind_time - 0.5,
            end_time = behind_time + 2 * OBJECT_APPEARANCE_TIME / FRAME_RATE
        )

        #Spinnnnnnn camera
        '''cam_swivel.spin(
            spin_rate = 0.11,
            start_time = start_time,
            axis = 2
        )'''

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
        self.fade_contextual_objects()
        #self.highlight_sections()
        #self.otoconia_wiggle()
        self.dislodged_otoconia()
        #self.dix_hallpike(epley = True)
        #self.inner_ear_rot()

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

        cam_bobj = bobject.Bobject(
            location = [90, 0, 0],
            rotation_euler = [math.pi / 2, 0, 87 * math.pi / 180],
            name = "Camera Bobject"
        )
        cam_swivel = bobject.Bobject(
            cam_bobj,
            location = [0, 0, 0],
            rotation_euler = [0, 0, 0],
            name = 'Cam swivel'
        )
        cam_swivel.add_to_blender(appear_time = 0, animate = False)
        #cam_bobj.add_to_blender(appear_time = 0, animate = False)
        cam_obj = bpy.data.objects['Camera']
        cam_obj.data.clip_end = 1000
        cam_obj.location = [0, 0, 0]
        cam_obj.parent = cam_bobj.ref_obj

        #Look at brain and temporal bone
        cam_swivel.move_to(
            new_angle = [0, 0, -55 * math.pi / 180],
            start_time = self.brain_zoom_time,
            end_time = self.brain_zoom_time + 1.5
        )
        cam_bobj.move_to(
            new_location = [35.3, 0, 0],
            new_angle = [95.8 * math.pi / 180, 0, 85.6 * math.pi / 180],
            start_time = self.brain_zoom_time,
            end_time = self.brain_zoom_time + 1.5
        )

        #Look at inner ear
        cam_bobj.move_to(
            new_location = [5, 0, 0],
            new_angle = [92.5 * math.pi / 180, 0, 89 * math.pi / 180],
            start_time = self.inner_zoom_time,
            end_time = self.inner_zoom_time + 1.5
        )

        #Look at utricle
        cam_swivel.move_to(
            new_angle = [0, 15.5 * math.pi / 180, -190 * math.pi / 180],
            start_time = self.utricle_time,
            end_time = self.utricle_time + 1.5
        )
        cam_bobj.move_to(
            new_location = [0.3, 0, 0.15],
            new_angle = [80.9 * math.pi / 180, 0, 89 * math.pi / 180],
            start_time = self.utricle_time,
            end_time = self.utricle_time + 1.5
        )

        #Side view of canals
        cam_swivel.move_to(
            new_angle = [0, 0, -217 * math.pi / 180],
            start_time = self.dislodged_time,
            end_time = self.dislodged_time + 1.5
        )
        cam_bobj.move_to(
            new_location = [5, 0, 0],
            new_angle = [92.5 * math.pi / 180, 0, 91 * math.pi / 180],
            start_time = self.dislodged_time,
            end_time = self.dislodged_time + 1.5
        )


        #rotate and highlight
        rot_duration = 2#25
        deg_angle = -217 + 360 / 10 * rot_duration
        cam_swivel.move_to(
            new_angle = [0, 0, deg_angle * math.pi / 180],
            start_time = self.only_posterior_time,
            end_time = self.only_posterior_time + rot_duration
        )

        #Epley position (stationary camera after initial positioning)
        cam_swivel.move_to(
            new_angle = [0, 0, 60 * math.pi / 180],
            start_time = self.epley_camera_time,
        )

        """#Dix Hallpike lean back
        cam_bobj.move_to(
            new_location = [5.5, 0, -0.1],
            new_angle = [92.5 * math.pi / 180, 0, 91 * math.pi / 180],
            start_time = 175,
            end_time = 178
        )

        cam_bobj.move_to(
            new_location = [5, 0, 0],
            new_angle = [92.5 * math.pi / 180, 0, 91 * math.pi / 180],
            start_time = 205,
            end_time = 208
        )

        #Correction during Epley
        cam_bobj.move_to(
            new_location = [5, 0, -0.4],
            new_angle = [92.5 * math.pi / 180, 0, 91 * math.pi / 180],
            start_time = 215,
            end_time = 218
        )

        extra_time = 12 + 1.5
        cam_bobj.move_to(
            new_location = [5, 0, 0],
            new_angle = [92.5 * math.pi / 180, 0, 91 * math.pi / 180],
            start_time = 224 + extra_time,
            end_time = 224 + extra_time + 3
        )"""

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

    def otoconia_wiggle(self):
        mix_shader = bpy.data.materials['u_otoconia'].node_tree.nodes['Mix Shader']
        mix = mix_shader.inputs[0]
        mix.keyframe_insert(data_path = 'default_value', frame = self.otoconia_time * FRAME_RATE)
        old_value = mix.default_value
        mix.default_value = 1
        mix.keyframe_insert(data_path = 'default_value', frame = (self.otoconia_time + 1) * FRAME_RATE)
        mix.keyframe_insert(data_path = 'default_value', frame = (self.dislodged_time) * FRAME_RATE)
        mix.default_value = old_value
        mix.keyframe_insert(data_path = 'default_value', frame = (self.dislodged_time + 1) * FRAME_RATE)

        wiggle_start = self.oto_wiggle_time
        wiggle_end = self.oto_wiggle_time + 5
        wiggle_angle = 30 #degrees
        wiggle_disp = 0.01 #cm

        duration = wiggle_end - wiggle_start

        num_cycles = 2

        for obj in bpy.data.objects:
            if 'otoconia' in obj.name:
                obj.keyframe_insert(data_path = 'rotation_euler', frame = FRAME_RATE * wiggle_start)
                obj.keyframe_insert(data_path = 'location', frame = FRAME_RATE * wiggle_start)
                starting_angle = list(obj.rotation_euler)
                starting_loc = list(obj.location)
                for i in range(num_cycles):
                    #Wiggle forward
                    obj.rotation_euler[1] = starting_angle[1] + wiggle_angle * math.pi / 180
                    obj.location[0] = starting_loc[0] + wiggle_disp
                    obj.keyframe_insert(data_path = 'rotation_euler', frame = FRAME_RATE * (wiggle_start + duration / num_cycles * (i + 1/4)))
                    obj.keyframe_insert(data_path = 'location', frame = FRAME_RATE * (wiggle_start + duration / num_cycles * ( i + 1/4)))

                    #Wiggle back
                    obj.rotation_euler[1] = starting_angle[1] - wiggle_angle * math.pi / 180
                    obj.location[0] = starting_loc[0] - wiggle_disp
                    obj.keyframe_insert(data_path = 'rotation_euler', frame = FRAME_RATE * (wiggle_start + duration / num_cycles * (i + 3/4)))
                    obj.keyframe_insert(data_path = 'location', frame = FRAME_RATE * (wiggle_start + duration / num_cycles * ( i + 3/4)))

                obj.rotation_euler[1] = starting_angle[1]
                obj.location[0] = starting_loc[0]
                obj.keyframe_insert(data_path = 'rotation_euler', frame = FRAME_RATE * (wiggle_start + duration))
                obj.keyframe_insert(data_path = 'location', frame = FRAME_RATE * (wiggle_start + duration))

        #Highlight utricle
        utricle = bpy.data.objects['Utricle']
        highlight_object(
            object = utricle,
            start_time = wiggle_start,
            duration_time = 5
        )

    def dislodged_otoconia(self):
        #Make otoconia appear
        start_time = self.dislodged_time
        tilt_delay = 7.5
        tilt_start_time = start_time + tilt_delay
        tilt_duration = 16
        end_pause = 2
        end_time = start_time + tilt_delay + tilt_duration + end_pause

        angle = 60 #degrees
        #duration = end_time - start_time
        num_cycles = 1

        rbw = bpy.context.scene.rigidbody_world
        rbw.point_cache.frame_start = start_time * FRAME_RATE
        rbw.point_cache.frame_end = end_time * FRAME_RATE

        for obj in bpy.data.objects:
            if 'e_otoconia' in obj.name:
                obj.keyframe_insert(data_path = 'scale', frame = (start_time - 0.5) * FRAME_RATE)
                obj.scale = [2, 2, 2]
                obj.keyframe_insert(data_path = 'scale', frame = (start_time) * FRAME_RATE + OBJECT_APPEARANCE_TIME)

        #move skull
        skull = bpy.data.objects['Skull_Top']
        skull.keyframe_insert(data_path = 'rotation_euler', frame = tilt_start_time * FRAME_RATE)

        for i in range(num_cycles):
            #tilt backward
            skull.rotation_euler[1] -= angle * math.pi / 180
            skull.keyframe_insert(data_path = 'rotation_euler', frame = FRAME_RATE * (tilt_start_time + tilt_duration / num_cycles * (i + 1/4)))
            skull.keyframe_insert(data_path = 'rotation_euler', frame = FRAME_RATE * (tilt_start_time + tilt_duration / num_cycles * (i + 2/4)))

            #tilt forward
            skull.rotation_euler[1] += angle * math.pi / 180
            skull.keyframe_insert(data_path = 'rotation_euler', frame = FRAME_RATE * (tilt_start_time + tilt_duration / num_cycles * (i + 3/4)))
            skull.keyframe_insert(data_path = 'rotation_euler', frame = FRAME_RATE * (tilt_start_time + tilt_duration / num_cycles * (i + 4/4)))

            #Highlight cupula
            #Could do this more systematically, but it's pretty specific ¯\_(ツ)_/¯
            cupula = bpy.data.objects['Posterior canal cupula']
            highlight_object(
                object = cupula,
                start_time = tilt_start_time + tilt_duration / num_cycles * (i + 1/8),
                duration_time = tilt_duration / num_cycles / 4
            )
            highlight_object(
                object = cupula,
                start_time = tilt_start_time + tilt_duration / num_cycles * (i + 4/8),
                duration_time = tilt_duration / num_cycles / 4
            )

        override = {'scene': bpy.context.scene,
                    'point_cache': bpy.context.scene.rigidbody_world.point_cache}
        bpy.ops.ptcache.bake(override, bake=True)

        for obj in bpy.data.objects:
            if 'e_otoconia' in obj.name:
                #print(obj.rigid_body)
                end_rigid_body(
                    obj = obj,
                    end_frame = end_time * FRAME_RATE
                )

    def dix_hallpike(self, epley = False):
        extra_time = 12
        start_time = 170
        end_time = 222 + extra_time

        rbw = bpy.context.scene.rigidbody_world
        rbw.point_cache.frame_start = (1 + start_time) * FRAME_RATE
        rbw.point_cache.frame_end = end_time * FRAME_RATE

        for obj in bpy.data.objects:
            if 'e_otoconia' in obj.name:
                obj.keyframe_insert(data_path = 'scale', frame = 170 * FRAME_RATE)
                obj.scale = [2, 2, 2]
                obj.keyframe_insert(data_path = 'scale', frame = 170 * FRAME_RATE + OBJECT_APPEARANCE_TIME)

        #move skull
        skull = bpy.data.objects['Skull_Top']

        skull.keyframe_insert(data_path = 'rotation_euler', frame = 172 * FRAME_RATE)
        skull.rotation_euler[2] = -45 * math.pi / 180
        skull.keyframe_insert(data_path = 'rotation_euler', frame = 174 * FRAME_RATE)

        skull.keyframe_insert(data_path = 'rotation_euler', frame = 175 * FRAME_RATE)
        skull.rotation_euler[1] = -120 * math.pi / 180
        skull.keyframe_insert(data_path = 'rotation_euler', frame = 178 * FRAME_RATE)

        if epley == True:
            skull.keyframe_insert(data_path = 'rotation_euler', frame = 205 * FRAME_RATE)
            skull.rotation_euler[2] = 45 * math.pi / 180
            skull.keyframe_insert(data_path = 'rotation_euler', frame = 208 * FRAME_RATE)

            skull.keyframe_insert(data_path = 'rotation_euler', frame = 215 * FRAME_RATE)
            skull.rotation_euler[2] = 135 * math.pi / 180
            skull.keyframe_insert(data_path = 'rotation_euler', frame = 218 * FRAME_RATE)



            skull.keyframe_insert(data_path = 'rotation_euler', frame = (224 + extra_time) * FRAME_RATE)
            skull.rotation_euler[1] = 0 * math.pi / 180
            skull.keyframe_insert(data_path = 'rotation_euler', frame = (227 + extra_time) * FRAME_RATE)

            skull.keyframe_insert(data_path = 'rotation_euler', frame = (230 + extra_time) * FRAME_RATE)
            skull.rotation_euler[2] = 90 * math.pi / 180
            skull.keyframe_insert(data_path = 'rotation_euler', frame = (231.5 + extra_time) * FRAME_RATE)

        override = {'scene': bpy.context.scene,
                    'point_cache': bpy.context.scene.rigidbody_world.point_cache}
        bpy.ops.ptcache.bake(override, bake=True)

        for obj in bpy.data.objects:
            if 'e_otoconia' in obj.name:
                print(obj.rigid_body)
                end_rigid_body(
                    obj = obj,
                    end_frame = end_time * FRAME_RATE
                )
        bpy.context.scene.frame_set(end_time * FRAME_RATE + 1)
        u_oto = [x for x in bpy.data.objects if 'u_otoconia' in x.name]
        e_oto = [x for x in bpy.data.objects if 'e_otoconia' in x.name]
        for i in range(len(e_oto)):
            loc = list(u_oto[i].location) #Not sure it's necessary, but copying
                                          #this with list()
            e_oto[i].keyframe_insert(data_path = 'location', frame = end_time * FRAME_RATE + 1)
            e_oto[i].location = loc
            e_oto[i].keyframe_insert(data_path = 'location', frame = (end_time + 1) * FRAME_RATE)




    def inner_ear_rot(self):
        ie = import_object(
            'inner_ear_bobject', 'UCSF',
            scale = 5
        )
        ie.add_to_blender(
            appear_frame = 0,
            animate = False
        )
        ie.spin(
            start_frame = 0,
            end_time = 20,
            constant_rate = True,
            spin_rate = 1/20,
        )

'''
