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
#import scene
#imp.reload(scene)
from scene import Scene
import bobject
import svg_bobject
import tex_bobject

#bpy.ops.wm.open_mainfile(filepath="C:\\Users\\justi\\Documents\\CodeProjects\\Primer\\files\\blend\\UCSF\\inner_ear_rigid_body")

def fade(
    object = None,
    start_time = 0,
    duration_time = 1,
    fade_out = True
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
                transparency.default_value = 0.99 #Actually show ghosts of objects
            transparency.keyframe_insert(data_path = 'default_value', frame = end_frame)
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
        #self.fade_contextual_objects()
        #self.highlight_sections()
        #self.otoconia_wiggle()
        #self.dislodged_otoconia()
        pass

    def intro_card(self):
        logo = svg_bobject.SVGBobject(
            "UCSF_logo_signature",
            #location = (-5, 3.75, 0), #Centered position
            #scale = 0.26, #Centered scale
            location = [-13.4, -3.47, 0],
            scale = 0.128,
            color = 'color2'
        )
        baf = svg_bobject.SVGBobject(
            'BaFC_Arial',
            location = [-4.83, -4.61, 0],
            scale = 1.85,
            color = 'color2'
        )
        intro = svg_bobject.SVGBobject(
            'IntroToBPPV_Garamond',
            location = [-12, 3.37, 0],
            scale = 3.14,
            color = 'color2'
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
        intro.add_to_blender(appear_time = -1, animate = False)
        vert.add_to_blender(appear_time = -1, animate = False)

        for bobj in [logo, baf, intro, vert]:
            print(bobj)
            print(bobj.ref_obj.name)
            print(len(bobj.ref_obj.children))
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





"""
class AnatomyScene(Scene):
    def __init__(self):
        bpy.context.scene.cycles.caustics_reflective = False
        bpy.context.scene.cycles.caustics_refractive = False
        bpy.context.scene.cycles.use_transparent_shadows = False
        bpy.context.scene.cycles.transparent_max_bounces = 1000

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
        #self.zoom()
        #self.fade_contextual_objects()
        #self.highlight_sections()
        #self.otoconia_wiggle()
        #self.dislodged_otoconia()
        self.dix_hallpike(epley = True)

    def fade_contextual_objects(self):
        print('Playing')
        skull = bpy.data.objects['Skull_Top']
        background = [
            bpy.data.objects['robertot'],
            skull,
            bpy.data.objects['Temporal Bone 2 bone.outer'],
            bpy.data.objects['Brain'],
            bpy.data.objects['Incus VE'],
            bpy.data.objects['Malleus VE'],
            bpy.data.objects['Stapes VE'],
            bpy.data.objects['Eighth Nerve VE'],
            bpy.data.objects['Vestibular nerve origin'],
            bpy.data.objects['Cochlear_nerve_origin_2'],
        ]

        for i, obj in enumerate(background):
            fade(
                object = obj,
                start_time = 1 + 0.1 * i,
                duration_time = 1
            )

    def zoom(self):
        cues = self.subscenes['zoom']

        cam_bobj = bobject.Bobject(
            location = [100, 0, 0],
            rotation_euler = [math.pi / 2, 0, math.pi / 2],
            name = "Camera Bobject"
        )
        cam_bobj.add_to_blender(appear_time = 0, animate = False)
        cam_obj = bpy.data.objects['Camera']
        cam_obj.data.clip_end = 1000
        cam_obj.location = [0, 0, 0]
        cam_obj.parent = cam_bobj.ref_obj

        skull = bpy.data.objects['Skull_Top']
        skull.keyframe_insert(data_path = 'rotation_euler', frame = 60)
        skull.rotation_euler = [0, 0, 600 * math.pi / 180]
        skull.keyframe_insert(data_path = 'rotation_euler', frame = 720)


        cam_bobj.move_to(
            new_location = [4, 0, 0.15],
            start_time = 1,
            end_time = 2.25
        )

    def highlight_sections(self):
        #ear = bpy.data.objects['inner ear_from microCT']
        vest_shader = bpy.data.materials['vestibule'].node_tree.nodes['Principled BSDF']
        vest_color = vest_shader.inputs[0]
        vest_color.keyframe_insert(data_path = 'default_value', frame = 3 * FRAME_RATE)
        old_value = list(vest_color.default_value)
        vest_color.default_value = [0, 1, 0, 1]
        vest_color.keyframe_insert(data_path = 'default_value', frame = 4 * FRAME_RATE)
        vest_color.default_value = old_value
        vest_color.keyframe_insert(data_path = 'default_value', frame = 5 * FRAME_RATE)

        canal_shader = bpy.data.materials['canals'].node_tree.nodes['Principled BSDF']
        canal_color = canal_shader.inputs[0]
        canal_color.keyframe_insert(data_path = 'default_value', frame = 6 * FRAME_RATE)
        old_value = list(canal_color.default_value)
        canal_color.default_value = [0, 1, 0, 1]
        canal_color.keyframe_insert(data_path = 'default_value', frame = 7 * FRAME_RATE)
        canal_color.default_value = old_value
        canal_color.keyframe_insert(data_path = 'default_value', frame = 8 * FRAME_RATE)

    def otoconia_wiggle(self):
        wiggle_start = 2
        wiggle_end = 4
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

        #Highlight utricle and saccule

    def dislodged_otoconia(self):
        #Make otoconia appear
        start_time = 1
        tilt_delay = 1
        tilt_start_time = start_time + tilt_delay
        tilt_duration = 8
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
                obj.keyframe_insert(data_path = 'scale', frame = start_time * FRAME_RATE)
                obj.scale = [2, 2, 2]
                obj.keyframe_insert(data_path = 'scale', frame = start_time * FRAME_RATE + OBJECT_APPEARANCE_TIME)

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
                start_time = tilt_start_time + tilt_duration / num_cycles * i,
                duration_time = tilt_duration / num_cycles / 2
            )
            highlight_object(
                object = cupula,
                start_time = tilt_start_time + tilt_duration / num_cycles * (i + 1/2),
                duration_time = tilt_duration / num_cycles / 2
            )

    def dix_hallpike(self, epley = False):
        end_time = 48

        rbw = bpy.context.scene.rigidbody_world
        rbw.point_cache.frame_start = 1 * FRAME_RATE
        rbw.point_cache.frame_end = end_time * FRAME_RATE

        for obj in bpy.data.objects:
            if 'e_otoconia' in obj.name:
                obj.keyframe_insert(data_path = 'scale', frame = 1 * FRAME_RATE)
                obj.scale = [2, 2, 2]
                obj.keyframe_insert(data_path = 'scale', frame = 1 * FRAME_RATE + OBJECT_APPEARANCE_TIME)

        #move skull
        skull = bpy.data.objects['Skull_Top']

        skull.keyframe_insert(data_path = 'rotation_euler', frame = 2 * FRAME_RATE)
        skull.rotation_euler[2] = -45 * math.pi / 180
        skull.keyframe_insert(data_path = 'rotation_euler', frame = 4 * FRAME_RATE)

        skull.keyframe_insert(data_path = 'rotation_euler', frame = 6 * FRAME_RATE)
        skull.rotation_euler[1] = -120 * math.pi / 180
        skull.keyframe_insert(data_path = 'rotation_euler', frame = 11 * FRAME_RATE)

        if epley == True:
            skull.keyframe_insert(data_path = 'rotation_euler', frame = 16 * FRAME_RATE)
            skull.rotation_euler[2] = 45 * math.pi / 180
            skull.keyframe_insert(data_path = 'rotation_euler', frame = 21 * FRAME_RATE)

            skull.keyframe_insert(data_path = 'rotation_euler', frame = 26 * FRAME_RATE)
            skull.rotation_euler[2] = 135 * math.pi / 180
            skull.keyframe_insert(data_path = 'rotation_euler', frame = 31 * FRAME_RATE)

            skull.keyframe_insert(data_path = 'rotation_euler', frame = 46 * FRAME_RATE)
            skull.rotation_euler[1] = 0 * math.pi / 180
            skull.keyframe_insert(data_path = 'rotation_euler', frame = 51 * FRAME_RATE)

            skull.keyframe_insert(data_path = 'rotation_euler', frame = 56 * FRAME_RATE)
            skull.rotation_euler[2] = 90 * math.pi / 180
            skull.keyframe_insert(data_path = 'rotation_euler', frame = 61 * FRAME_RATE)

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
"""
