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

#bpy.ops.wm.open_mainfile(filepath="C:\\Users\\justi\\Documents\\CodeProjects\\Primer\\files\\blend\\UCSF\\inner_ear_rigid_body")

def fade(
    object = None,
    start_time = 0,
    duration_time = 1,
    fade_out = True,
    extent = 1
):
    start_frame = start_time * FRAME_RATE
    end_frame = start_frame + duration_time * FRAME_RATE
    if object == None:
        raise Warning('Need object to fade')

    print(object.name)

    for slot in object.material_slots:
        mat = slot.material
        mat_copy = mat.copy()
        slot.material = mat = mat_copy
        #print(mat)
        tree = mat.node_tree

        try: #Grab mix shader. This assumes it's
            mix = tree.nodes['Mix Shader'] #Assumes there is only one
        except:
            mat_out = tree.nodes['Material Output'].inputs[0]
            for link in tree.links:
                if link.to_socket == mat_out:
                    old_link = link
                    old_out = link.from_socket
                    break
            tree.links.remove(old_link)

            mix = tree.nodes.new(type = 'ShaderNodeMixShader')
            trans = tree.nodes.new(type = 'ShaderNodeBsdfTransparent')
            tree.links.new(old_out, mix.inputs[1])
            tree.links.new(trans.outputs[0], mix.inputs[2])
            tree.links.new(mix.outputs[0], mat_out)

        #Kind of non-intuitive to people used to 'alpha', but transparency 1 is
        #completely clear, while transparency 0 is opaque. I did it this way
        #because some materials I got from UCSF were set up this way.
        transparency = mix.inputs[0]
        if fade_out == True:
            transparency.keyframe_insert(data_path = 'default_value', frame = start_frame)
            transparency.default_value = 1
            if RENDER_QUALITY == 'high':
                transparency.default_value = extent
            transparency.keyframe_insert(data_path = 'default_value', frame = end_frame)
            if transparency.default_value == 1:
                object.keyframe_insert(data_path = 'hide', frame = end_frame - 1)
                object.keyframe_insert(data_path = 'hide_render', frame = end_frame - 1)
                object.hide = True
                object.hide_render = True
                object.keyframe_insert(data_path = 'hide', frame = end_frame)
                object.keyframe_insert(data_path = 'hide_render', frame = end_frame)
        else:
            transparency.default_value = 1
            transparency.keyframe_insert(data_path = 'default_value', frame = start_frame)
            transparency.default_value = 0
            transparency.keyframe_insert(data_path = 'default_value', frame = end_frame)

def highlight_object(
    object = None,
    start_time = 0,
    duration_time = 1
):
    start_frame = start_time * FRAME_RATE
    #end_frame = start_frame + duration_time * FRAME_RATE
    if object == None:
        raise Warning('Need object to fade')

    for slot in object.material_slots:
        mat = slot.material
        mat_copy = mat.copy()
        slot.material = mat = mat_copy
        #print(mat)
        shader = mat.node_tree.nodes['Principled BSDF'] #Assumes there is only one

        color = shader.inputs[0]
        color.keyframe_insert(data_path = 'default_value', frame = start_frame)
        original_color = list(color.default_value)
        color.default_value = [1, 0, 0, 1]
        color.keyframe_insert(data_path = 'default_value', frame = start_frame + duration_time / 4 * FRAME_RATE)
        color.keyframe_insert(data_path = 'default_value', frame = start_frame + 3 * duration_time / 4 * FRAME_RATE)
        color.default_value = original_color
        color.keyframe_insert(data_path = 'default_value', frame = start_frame + duration_time * FRAME_RATE)

def end_rigid_body(
    obj = None,
    end_frame = None
):
    print(obj.name)
    print(obj.rigid_body)
    #This might not be necessary, but it seems to help avoid context errors for
    #the bpy.ops operators
    bpy.context.scene.objects.active = None
    for object in bpy.data.objects:
        object.select = False

    bpy.context.scene.frame_set(end_frame - 1)

    bpy.context.scene.objects.active = obj
    obj.select = True
    print()
    print(obj.name)
    print(obj.rigid_body)

    #Keframe position based on sim result
    obj.keyframe_insert(data_path = 'location', frame = end_frame - 1)
    bpy.ops.object.visual_transform_apply()
    obj.keyframe_insert(data_path = 'location', frame = end_frame)

    #Keyframe 'animated' property in physics settings
    obj.rigid_body.kinematic = False
    obj.rigid_body.keyframe_insert(data_path = 'kinematic', frame = end_frame - 1)
    obj.rigid_body.kinematic = True
    obj.rigid_body.keyframe_insert(data_path = 'kinematic', frame = end_frame)

    bpy.context.scene.objects.active = None
    obj.select = False

'''
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
        #self.acronym_breakdown()
        #self.transition_card()
        self.end_card()

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
        vest = svg_bobject.SVGBobject(
            'vestibular_videos_garamond',
            location = [0, 4.5, 0],
            scale = 2,
            color = 'color2',
            centered = True
        )
        intro = svg_bobject.SVGBobject(
            'IntroToBPPV_Garamond',
            location = [0, 1.5, 0],
            scale = 3.14,
            color = 'color2',
            centered = True
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
        intro.add_to_blender(appear_time = -1, animate = False)
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
        for bobj in [intro]:
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

    def acronym_breakdown(self):
        b = tex_bobject.TexBobject(
            '\\text{B}',
            '\\text{Benign}',
            color = 'color2'
        )
        pa = tex_bobject.TexBobject(
            '\\text{P}',
            '\\text{Paroxysmal}',
            color = 'color2'
        )
        po = tex_bobject.TexBobject(
            '\\text{P}',
            '\\text{Positional}',
            color = 'color2'
        )
        v = tex_bobject.TexBobject(
            '\\text{V}',
            '\\text{Vertigo}',
            color = 'color2'
        )
        """baf = svg_bobject.SVGBobject(
            'B_Arial',
            'BaFC_Arial',
            location = [0, 0, 0],
            #scale = 1.85,
            color = 'color2'
        )"""
        """gaf = svg_bobject.SVGBobject(
            'BaFC_Arial',
            location = [0, 0, 0],
            #scale = 1.85,
            color = 'color2'
        )"""
        bppv = tex_complex.TexComplex(
            b, pa, po, v,
            scale = 6,
            location = [-6.8, 0, 0]
        )

        bppv.add_to_blender(
            appear_frame = 0,
            animate = False,
            subbobject_timing = [0, 24, 48, 72]
        )

        bppv.move_to(
            new_location = [-12.5, 4, 0],
            new_scale = 4,
            start_time = 2.5
        )
        acronym = tex_bobject.TexBobject(
            '\\bullet\\text{Break down the acronym}',
            color = 'color2'
        )
        cause = tex_bobject.TexBobject(
            '\\bullet\\text{Understand the cause}',
            color = 'color2'
        )
        treat = tex_bobject.TexBobject(
            '\\bullet\\text{Look at diagnosis and treatment}',
            color = 'color2'
        )
        contents = tex_complex.TexComplex(
            acronym, cause, treat,
            location = [-11, 0, 0],
            scale = 1.75,
            multiline = True
        )
        contents.add_to_blender(
            appear_time = 4,
            subbobject_timing = [0, 30, 60]
        )
        contents.disappear(disappear_time = 6)




        bppv.multiline = True
        bppv.arrange_tex_bobjects(
            start_time = 7,
            end_time = 7.5
        )
        bppv.move_to(
            start_time = 7,
            new_scale = 3,
            new_location = [-12.5, 5.5, 0]
        )

        b.morph_figure(1, start_time = 8)
        pa.morph_figure(1, start_time = 9)
        po.morph_figure(1, start_time = 10)
        v.morph_figure(1, start_time = 11)

        for char in b.subbobjects:
            char.color_shift(
                color = COLORS_SCALED[2],
                start_time = 12,
                duration_time = 2,
            )
        for char in pa.subbobjects:
            char.color_shift(
                color = COLORS_SCALED[2],
                start_time = 15,
                duration_time = 2,
            )
        for char in po.subbobjects:
            char.color_shift(
                color = COLORS_SCALED[2],
                start_time = 18,
                duration_time = 2,
            )
        for char in v.subbobjects:
            char.color_shift(
                color = COLORS_SCALED[2],
                start_time = 21,
                duration_time = 2,
            )

        #"You get BPPV"
        for i, word in enumerate(bppv.subbobjects):
            char = word.lookup_table[1][0] #second figure, first char
            char.pulse(
                start_time = 24 + 0.25 * i,
                duration_time = 0.5,
                attack = 0.2 * FRAME_RATE,
                decay = 0.2 * FRAME_RATE
            )

        for thing in bppv.subbobjects:
            thing.disappear(disappear_time = 27)


        """b_note_loc = [2.5, 5.4, 0]
        gest_scale = 1.6
        b_gest = gesture.Gesture(
            gesture_series = [
                {
                    'type': 'arrow',
                    'points': {
                        'tail': ((b_note_loc[0] - 1)/gest_scale, b_note_loc[1]/gest_scale, 0),
                        'head': (-3.4/gest_scale, 5.3/gest_scale, 0)
                    }
                }
            ],
            scale = gest_scale,
            color = 'color2'
        )
        b_note = tex_bobject.TexBobject(
            '\\text{Not life-threatening}',
            location = b_note_loc,
            scale = 1.5,
            color = 'color2'
        )
        b_gest.add_to_blender(appear_time = 13)
        b_note.add_to_blender(appear_time = 13)"""

    def transition_card(self):
        text = tex_bobject.TexBobject(
            #'\\text{The Cause of BPPV}',
            '\\text{Diagnosis and Treatment}',
            location = [0, 0, 0],
            scale = 2.5,
            color = 'color2',
            centered = True
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
            location = [-11.57, 1.5, 0],
            scale = 0.852
        )
        logobaf.add_to_blender(
            appear_time = 0,
            animate = False,
        )
        mpb_loc = [-13.5, -5, 0]
        mpb = tex_bobject.TexBobject(
            '\\text{Made possible by:}',
            location = mpb_loc,
            color = 'color2',
            name = 'mpb'
        )
        mzhf = tex_bobject.TexBobject(
            '\\text{Mount Zion Health Fund}',
            color = 'color2',
            scale = 1.5,
            location = [
                mpb_loc[0],
                mpb_loc[1] - 1.5,
                mpb_loc[2]
            ],
            name = 'mzhf'
        )
        vpb_loc = [5.5, -5, 0]
        vpb = tex_bobject.TexBobject(
            '\\text{Video produced by:}',
            color = 'color2',
            location = vpb_loc,
            name = 'vpb'
        )
        jh = tex_bobject.TexBobject(
            '\\text{Justin Helps}',
            location = [
                vpb_loc[0],
                vpb_loc[1] - 1.5,
                vpb_loc[2]
            ],
            scale = 1.5,
            color = 'color2',
            name = 'jh'
        )

        for bobj in [mpb, mzhf, vpb, jh]:
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
        #self.fade_contextual_objects()
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

        """#Look at brain and temporal bone
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
        )"""

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
