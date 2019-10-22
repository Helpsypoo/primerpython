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
        self.intro_card()
        #self.outline()
        #self.vemp_text()
        #self.pt_list()
        #self.migraine_outline()
        #self.dizziness_outline()
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
            color = 'color1',
            centered = True
        )
        baf = svg_bobject.SVGBobject(
            'BaFC_Arial',
            location = [4.325, -5.2, 0],
            scale = 1.85,
            color = 'color1',
            centered = True
        )
        vest = tex_bobject.TexBobject(
            '\\text{Vestibular Videos:}',
            location = [0, 4.5, 0],
            scale = 2,
            color = 'color1',
            centered = True,
            typeface = 'garamond'
        )
        title = tex_bobject.TexBobject(
            #'\\text{How The Vestibular System Works}',
            #'\\text{Dizziness as we age}',
            #'\\text{The Video Head Impulse Test}',
            #'\\text{The Rotary Chair Test}',
            #'\\text{The VEMP Test}',
            #'\\text{Videonystagmography}',
            #'\\text{Vestibular Physical Therapy}',
            '\\text{Vestibular Evoked}',
            location = [0, 0.75, 0],
            scale = 3,
            color = 'color1',
            centered = True,
            typeface = 'garamond'
        )
        title2 = tex_bobject.TexBobject(
            #'\\text{How The Vestibular System Works}',
            #'\\text{Dizziness as we age}',
            #'\\text{The Video Head Impulse Test}',
            #'\\text{The Rotary Chair Test}',
            #'\\text{The VEMP Test}',
            #'\\text{Videonystagmography}',
            #'\\text{Vestibular Physical Therapy}',
            '\\text{Myogenic Potential Test}',
            location = [0, 0.75, 0],
            scale = 3,
            color = 'color1',
            centered = True,
            typeface = 'garamond'
        )
        title3 = tex_bobject.TexBobject(
            #'\\text{How The Vestibular System Works}',
            #'\\text{Dizziness as we age}',
            #'\\text{The Video Head Impulse Test}',
            #'\\text{The Rotary Chair Test}',
            #'\\text{The VEMP Test}',
            #'\\text{Videonystagmography}',
            #'\\text{Vestibular Physical Therapy}',
            '\\text{(VEMP Test)}',
            location = [0, 0.75, 0],
            scale = 2,
            color = 'color1',
            centered = True,
            typeface = 'garamond'
        )
        vert = tex_bobject.TexBobject(
            '|',
            location = [-6.35, -4.74, 0],
            scale = [2, 5.32, 4],
            centered = True,
            color = 'color1',
        )

        logo.add_to_blender(appear_time = -1, animate = False)
        baf.add_to_blender(appear_time = -1, animate = False)
        vest.add_to_blender(appear_time = -1, animate = False)
        title.add_to_blender(appear_time = -1, animate = False)
        title2.add_to_blender(appear_time = -1, animate = False)
        title3.add_to_blender(appear_time = -1, animate = False)
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
            #subbobject_timing = [30] * 8 + [75] * 5
        )
        sc.move_to(
            new_location = [0, 3.5, 0],
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

    def vemp_text(self):
        vemp = tex_bobject.TexBobject(
            "\\text{VEMP}",
            "\\begin{array}{@{}c@{}}\\text{Vestibular} \\\\ \\text{Evoked} \\\\ \\text{Myogenic} \\\\ \\text{Potential} \\end{array}",
            location = [0, 5, 0],
            centered = True,
            typeface = 'arial',
            scale = 3
        )
        vemp.add_to_blender(appear_time = 0)

        svm = tex_bobject.TexBobject(
            "\\text{Sound}",
            "\\text{Sound} \\rightarrow \\begin{array}{@{}c@{}}\\text{Muscle} \\\\ \\text{activation} \\end{array}",
            "\\text{Sound} \\rightarrow \\begin{array}{@{}c@{}}\\text{Vestibular} \\\\ \\text{activation} \\end{array} \\rightarrow \\begin{array}{@{}c@{}}\\text{Muscle} \\\\ \\text{activation} \\end{array}",
            location = [0, -2, 0],
            centered = True,
            typeface = 'arial',
            scale = 2
        )
        svm.add_to_blender(appear_time = 1)
        svm.morph_figure(1, start_time = 2)
        svm.morph_figure(2, start_time = 3)

        svm.disappear(disappear_time = 4.5)

        vemp.morph_figure(1, start_time = 6)
        vemp.move_to(
            new_location = [0, 0, 0],
            start_time = 5
        )

        for i in range(16, 24):
            vemp.lookup_table[1][i].color_shift(
                color = COLORS_SCALED[2],
                start_time = 7,
                duration_time = 1.5
            )

        for i in range(24, 33):
            vemp.lookup_table[1][i].color_shift(
                color = COLORS_SCALED[2],
                start_time = 9,
                duration_time = 1.5
            )

    def migraine_outline(self):
        vn = tex_bobject.TexBobject(
            #"\\text{Vestibular migraine}",
            "\\text{Some migraine symptoms}",
            location = [0, 0, 0],
            centered = True,
            typeface = 'arial',
            scale = 3
        )
        vn.add_to_blender(appear_time = 0)
        vn.move_to(
            new_location = [0, 5, 0],
            start_time = 2.5
        )

        acronym = tex_bobject.TexBobject(
            '\\bullet\\text{Headache}',
            color = 'color2',
            typeface = 'arial'
        )
        cause = tex_bobject.TexBobject(
            '\\bullet\\text{Seeing lights and colors}',
            color = 'color2',
            typeface = 'arial'
        )
        treat = tex_bobject.TexBobject(
            '\\bullet\\text{Light and sound sensitivity}',
            color = 'color2',
            typeface = 'arial'
        )
        nausea = tex_bobject.TexBobject(
            '\\bullet\\text{Nausea}',
            color = 'color2',
            typeface = 'arial'
        )
        others = tex_bobject.TexBobject(
            '\\bullet\\text{Others}',
            '\\bullet\\text{Dizziness}',
            color = 'color2',
            typeface = 'arial'
        )
        contents = tex_complex.TexComplex(
            acronym, cause, treat, nausea, others,
            location = [-9, 1.75, 0],
            scale = 1.5,
            multiline = True
        )
        contents.add_to_blender(
            appear_time = 4,
            subbobject_timing = [0, 35, 70, 105, 140]
        )
        others.morph_figure(1, start_time = 7)
        #contents.disappear(disappear_time = 7)
        #vn.disappear(disappear_time = 7)

        '''vn.move_to(
            new_location = [0, 5.5, 0],
            start_time = 6.5
        )'''

        #vn.disappear(disappear_time = 16)

    def dizziness_outline(self):
        vn = tex_bobject.TexBobject(
            "\\text{Fall prevention}",
            location = [0, 0, 0],
            centered = True,
            typeface = 'arial',
            scale = 3
        )
        vn.add_to_blender(appear_time = 0)
        vn.move_to(
            new_location = [0, 3.5, 0],
            start_time = 2.5
        )

        acronym = tex_bobject.TexBobject(
            '\\bullet\\text{Visual}',
            color = 'color2',
            typeface = 'arial'
        )
        cause = tex_bobject.TexBobject(
            '\\bullet\\text{Somatosensory}',
            color = 'color2',
            typeface = 'arial'
        )
        treat = tex_bobject.TexBobject(
            '\\bullet\\text{Vestibular}',
            color = 'color2',
            typeface = 'arial'
        )
        disease = tex_bobject.TexBobject(
            '\\bullet\\text{Diseases and medications}',
            color = 'color2',
            typeface = 'arial'
        )
        contents = tex_complex.TexComplex(
            acronym, cause, treat, disease,
            location = [-9, 0.5, 0],
            scale = 1.5,
            multiline = True
        )
        contents.add_to_blender(
            appear_time = 4,
            subbobject_timing = [0, 35, 70, 105]
        )
        #contents.disappear(disappear_time = 7)
        #vn.disappear(disappear_time = 7)

        '''vn.move_to(
            new_location = [0, 5.5, 0],
            start_time = 6.5
        )'''

        vn.disappear(disappear_time = 16)

    def dizziness_factors(self):
        vn = tex_bobject.TexBobject(
            "\\text{Contributing factors}",
            location = [0, 0, 0],
            centered = True,
            typeface = 'arial',
            scale = 2.5
        )
        vn.add_to_blender(appear_time = 0)
        vn.move_to(
            new_location = [0, 4.5, 0],
            start_time = 2.5
        )

        acronym = tex_bobject.TexBobject(
            '\\bullet\\text{Visual}',
            color = 'color2',
            typeface = 'arial'
        )
        cause = tex_bobject.TexBobject(
            '\\bullet\\text{Somatosensory}',
            color = 'color2',
            typeface = 'arial'
        )
        treat = tex_bobject.TexBobject(
            '\\bullet\\text{Vestibular}',
            color = 'color2',
            typeface = 'arial'
        )
        disease = tex_bobject.TexBobject(
            '\\bullet\\text{Diseases and medications}',
            color = 'color2',
            typeface = 'arial'
        )
        contents = tex_complex.TexComplex(
            acronym, cause, treat, disease,
            location = [-9, 1.5, 0],
            scale = 1.5,
            multiline = True
        )
        contents.add_to_blender(
            appear_time = 4,
            subbobject_timing = [0, 35, 70, 105]
        )
        #contents.disappear(disappear_time = 7)
        #vn.disappear(disappear_time = 7)

        '''vn.move_to(
            new_location = [0, 5.5, 0],
            start_time = 6.5
        )'''

        vn.disappear(disappear_time = 16)

    def pt_list(self):
        vn = tex_bobject.TexBobject(
            "\\text{Contributors to balance}",
            location = [0, 0, 0],
            centered = True,
            typeface = 'arial',
            scale = 2.5
        )
        vn.add_to_blender(appear_time = 0)
        vn.move_to(
            new_location = [0, 5, 0],
            start_time = 2.5
        )

        acronym = tex_bobject.TexBobject(
            '\\bullet\\text{Sensory}',
            color = 'color2',
            typeface = 'arial'
        )
        cause = tex_bobject.TexBobject(
            '\\bullet\\text{Biomechanical}',
            color = 'color2',
            typeface = 'arial'
        )
        treat = tex_bobject.TexBobject(
            '\\bullet\\text{Neurologic}',
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
            subbobject_timing = [0, 60, 120]
        )
        #contents.disappear(disappear_time = 7)
        #vn.disappear(disappear_time = 7)

        '''vn.move_to(
            new_location = [0, 5.5, 0],
            start_time = 6.5
        )'''

        vn.disappear(disappear_time = 16)

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
            #'\\text{The Vestibular System}',
            #'\\text{Contributing factors}',
            '\\text{Body systems}',
            #'\\text{Medications}',
            #'\\text{Management}',
            #'\\text{Sensory systems}',
            #'\\text{Biomechanics}',
            #'\\text{Neurologic demands}',
            #'\\text{Rehabilitation Programs}',
            #'\\text{Overview and Symptoms}',
            #'\\text{Cause and Diagnosis}',
            #'\\text{Treatment}',
            location = [0, 0, 0],
            scale = 2.5,
            color = 'color1',
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
            color = 'color1',
            #centered = True,
        )
        baf = svg_bobject.SVGBobject(
            'BaFC_Arial',
            location = [5.2257280349731445, -0.26257357001304626, 0.0],
            scale = 2.23,
            color = 'color1',
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
            color = 'color1',
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
            color = 'color1',
            name = 'mpb',
            typeface = 'arial'
        )
        mzhf = tex_bobject.TexBobject(
            '\\text{Mount Zion Health Fund}',
            color = 'color1',
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
            color = 'color1',
            location = vpb_loc,
            name = 'vpb',
            typeface = 'arial'
        )
        jh = tex_bobject.TexBobject(
            '\\text{Justin Helps}',
            location = [
                vpb_loc[0] + 0.5,
                vpb_loc[1] - 1.2,
                vpb_loc[2]
            ],
            scale = 0.8,
            color = 'color1',
            name = 'jh',
            typeface = 'arial'
        )
        ep = tex_bobject.TexBobject(
            #'\\text{Lauren Pasquesi, AuD}',
            #'\\text{Erica Pitsch, PT}',
            '\\text{Roseanne Krauter, FNP-BC}',
            location = [
                vpb_loc[0] + 0.5,
                vpb_loc[1] - 2.2,
                vpb_loc[2]
            ],
            scale = 0.8,
            color = 'color1',
            name = 'jds',
            typeface = 'arial'
        )
        jds = tex_bobject.TexBobject(
            '\\text{Jeffrey D. Sharon, MD}',
            location = [
                vpb_loc[0] + 0.5,
                vpb_loc[1] - 3.2,
                vpb_loc[2]
            ],
            scale = 0.8,
            color = 'color1',
            name = 'jds',
            typeface = 'arial'
        )


        for bobj in [mpb, mzhf, vpb, jh, ep, jds]:
            bobj.add_to_blender(
                appear_time = 0,
                animate = False
            )
