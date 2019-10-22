'''
When using draw_scenes.py to play this, clear should be set to false, and
inner_ear.blend should be open.
'''

import bpy
import collections
import math
from copy import deepcopy
from random import shuffle
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
        self.utricle_time = 143.5
        #self.otoconia_time = 116
        #self.oto_wiggle_time = 118
        #self.dislodged_time = 125
        #self.only_posterior_time = 149

        #TODO: Determine timings
        self.epley_camera_time = 170

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
        #self.dix_hallpike(epley = True)

        #self.inner_ear_rot()
        #self.intro_and_cupula()
        #self.utricle_and_friends()
        #self.vanishing_hairs()
        #self.head_move_eyes_locked()
        #self.horizontal_canal_only()
        self.all_canals()

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
            end_time = 24,
            constant_rate = True,
            spin_rate = 1/20,
        )
        self.highlight_sections(
            start_time = 3,
            end_time = 40, #just big
            parts = ['vestibule', 'canals']
        )

    def intro_and_cupula(self):
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

        '''#Look at brain and temporal bone
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
        )'''

        #Look at inner ear
        cam_bobj.move_to(
            new_location = [5, 0, 0],
            new_angle = [92.5 * math.pi / 180, 0, 89 * math.pi / 180],
            start_time = 49,
            end_time = 52
        )

        self.fade_contextual_objects(
            start_time = 50.5,
            end_time = 52,
        )

        self.highlight_sections(
            start_time = 54.7,
            end_time = 58.5,
            parts = ['cochlea']
        )
        self.highlight_sections(
            start_time = 59.6,
            end_time = 65.5,
            parts = ['vestibule']
        )
        cam_swivel.move_to(
            new_angle = [0, 0, -65 * math.pi / 180],
            start_time = 60,
            end_time = 65
        )

        self.highlight_sections(
            start_time = 59.6,
            end_time = 68,
            parts = ['canals']
        )
        self.highlight_sections(
            start_time = 68,
            end_time = 71,
            parts = ['vestibule']
        )

        self.highlight_sections(
            start_time = 72.5,
            end_time = 81,
            parts = ['posterior']
        )
        self.highlight_sections(
            start_time = 73.5,
            end_time = 81,
            parts = ['superior']
        )
        self.highlight_sections(
            start_time = 74.5,
            end_time = 81,
            parts = ['horizontal']
        )

        cam_swivel.move_to(
            new_angle = [0, -11.7 * math.pi / 180, 370.5 * math.pi / 180],
            start_time = 81.5,
            end_time = 84.5,
        )
        cam_bobj.move_to(
            new_angle = [92.5 * math.pi / 180, 0, 89 * math.pi / 180],
            new_location = [0.7, -0.5, 0.2],
            start_time = 84,
            end_time = 85,
        )
        fade(
            object = bpy.data.objects['inner ear_from microCT'],
            start_time = 84,
            duration_time = 1,
            extent = 1
        )

        cam_swivel.move_to(
            new_angle = [0, -11.7 * math.pi / 180, 373.5 * math.pi / 180],
            start_time = 84.5,
            end_time = 100.5,
        )

        sturt = 93.5
        num_pulses = 7
        for i in range(num_pulses):
            self.highlight_sections(
                start_time = sturt + i,
                end_time = sturt + i + 1,
                attack = 0.5,
                decay = 0.5,
                parts = ['sensing_organs']
            )
        '''
        self.highlight_sections(
            start_time = 94.5,
            end_time = 95.5,
            attack = 0.5,
            decay = 0.5,
            parts = ['sensing_organs']
        )
        self.highlight_sections(
            start_time = 95.5,
            end_time = 96.5,
            attack = 0.5,
            decay = 0.5,
            parts = ['sensing_organs']
        )
        self.highlight_sections(
            start_time = 96.5,
            end_time = 97.5,
            attack = 0.5,
            decay = 0.5,
            parts = ['sensing_organs']
        )
        self.highlight_sections(
            start_time = 97.5,
            end_time = 98.5,
            attack = 0.5,
            decay = 0.5,
            parts = ['sensing_organs']
        )
        self.highlight_sections(
            start_time = 98.5,
            end_time = 99.5,
            attack = 0.5,
            decay = 0.5,
            parts = ['sensing_organs']
        )
        self.highlight_sections(
            start_time = 99.5,
            end_time = 100.5,
            attack = 0.5,
            decay = 0.5,
            parts = ['sensing_organs']
        )'''

        '''#Look at utricle
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
        )'''

    def utricle_and_friends(self):
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

        #Look at inner ear
        cam_bobj.move_to(
            new_location = [5, 0, 0],
            new_angle = [92.5 * math.pi / 180, 0, 89 * math.pi / 180],
            start_time = 49,
            end_time = 52
        )

        self.fade_contextual_objects(
            start_time = 50.5,
            end_time = 52,
        )


        #Highlight vestibule
        self.highlight_sections(
            start_time = 121.5,
            end_time = 132,
            parts = ['vestibule']
        )
        cam_swivel.move_to(
            new_angle = [0, 9.4 * math.pi / 180, 160 * math.pi / 180],
            start_time = 121,
            end_time = 132.5
        )

        #Look at utricle
        fade(
            object = bpy.data.objects['inner ear_from microCT'],
            start_time = 130,
            duration_time = 1,
            extent = 1
        )

        cam_bobj.move_to(
            new_location = [0.2, -0.03, 0.05],
            new_angle = [92.5 * math.pi / 180, 0, 89 * math.pi / 180],
            start_time = 127,
            end_time = 132.5
        )

        #Rotate while looking at utricle
        cam_swivel.move_to(
            new_angle = [0, 9.4 * math.pi / 180, 155 * math.pi / 180],
            start_time = 134,
            end_time = 154
        )

        cam_bobj.move_to(
            new_location = [0.2, -0.05, 0.05],
            new_angle = [92.5 * math.pi / 180, 0, 89 * math.pi / 180],
            start_time = 134,
            end_time = 156
        )

        self.highlight_sections(
            start_time = 144,
            end_time = 150,
            parts = ['utricle']
        )
        self.otoconia_wiggle(
            start_time = 144,
            end_time = 150,
            num_cycles = 3
        )

        #Move cam to show saccule too at 157
        cam_bobj.move_to(
            new_location = [0.45, -0.15, -0.03],
            new_angle = [92.5 * math.pi / 180, 0, 89 * math.pi / 180],
            start_time = 157,
            end_time = 159
        )
        #Highlight saccule at 161.5
        self.highlight_sections(
            start_time = 161.5,
            end_time = 200,
            parts = ['saccule']
        )

        '''
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
        )'''

    def vanishing_hairs(self):
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

        #Look at inner ear
        cam_bobj.move_to(
            new_location = [5, 0, 0],
            new_angle = [92.5 * math.pi / 180, 0, 89 * math.pi / 180],
            start_time = 68,
            end_time = 71
        )

        self.fade_contextual_objects(
            start_time = 69.5,
            end_time = 71,
        )

        #Highlight vestibule
        cam_swivel.move_to(
            new_angle = [0, 9.4 * math.pi / 180, 160 * math.pi / 180],
            start_time = 71,
            end_time = 76
        )

        #Look at utricle
        fade(
            object = bpy.data.objects['inner ear_from microCT'],
            start_time = 76,
            duration_time = 1,
            extent = 1
        )

        cam_bobj.move_to(
            new_location = [0.2, -0.03, 0.05],
            new_angle = [92.5 * math.pi / 180, 0, 89 * math.pi / 180],
            start_time = 75,
            end_time = 77
        )

        #Rotate while looking at utricle
        cam_swivel.move_to(
            new_angle = [0, 9.4 * math.pi / 180, 155 * math.pi / 180],
            start_time = 77,
            end_time = 86
        )

        cam_bobj.move_to(
            new_location = [0.2, -0.05, 0.05],
            new_angle = [92.5 * math.pi / 180, 0, 89 * math.pi / 180],
            start_time = 77,
            end_time = 86
        )

        otos = []
        for obj in bpy.data.objects:
            if 'u_otoconia' in obj.name:
                if '005' in obj.name or \
                   '009' in obj.name or \
                   '011' in obj.name or \
                   '001' in obj.name:

                    otos.append(obj)

        shuffle(otos) #I'm being indecisive about timings!
        for i, oto in enumerate(otos):
            fade(
                object = oto,
                start_time = 77 + 2 * i,
                duration_time = 1,
                extent = 1
            )


        '''
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
        )'''

    def head_move_eyes_locked(self):
        cam_bobj, cam_swivel = cam_and_swivel(
            cam_location = [0, 0, 90],
            cam_rotation_euler = [0, 0, 0],
            cam_name = "Camera Bobject",
            swivel_location = [0, 0, -2],
            swivel_rotation_euler = [math.pi / 2, 0, math.pi / 2],
            swivel_name = 'Cam swivel',
            #control_sun = True
        )
        cam_swivel.add_to_blender(appear_time = -1)


        skull = bpy.data.objects['Skull_Top']
        skull_bobj = bobject.Bobject(objects = [skull])
        skull_bobj.add_to_blender(appear_time = 0, animate = False)

        eye_l = bpy.data.objects['eye_l']
        eye_l_initial_angle = list(eye_l.rotation_euler)
        eye_r = bpy.data.objects['eye_r']
        eye_r_initial_angle = list(eye_r.rotation_euler)
        skin = bpy.data.objects['robertot']

        keeps = [
            eye_l, eye_r, skin,
            bpy.data.objects['Cam swivel'],
            bpy.data.objects['Camera Bobject'],
            bpy.data.objects['Sun'],
            bpy.data.objects['bobject'],
        ]
        for obj in bpy.data.objects:
            if obj not in keeps:
                fade(
                    object = obj,
                    start_time = 0,
                )

        sun = bpy.data.objects['Sun']
        sun.rotation_euler = [0, math.pi / 4, 0]

        bpy.ops.object.lamp_add(
            type = 'POINT',
            location = (1.75, 1.78, 9)
        )
        point_source = bpy.context.object
        point_source.data.node_tree.nodes[1].inputs[1].default_value = 1000

        angles = [
            [0, 0, 20 * math.pi / 180],
            [0, 0, 0 * math.pi / 180],
            [0, 0, 20 * math.pi / 180],
            [0, 0, 0 * math.pi / 180],
            [0, 0, 20 * math.pi / 180],
            #[0, 0, 15 * math.pi / 180],
            #[0, 0, -15 * math.pi / 180],
            #[0, 0, 15 * math.pi / 180],
            #[0, 0, -15 * math.pi / 180],
            #[0, 0, -15 * math.pi / 180],
            #[0, 10 * math.pi / 180, 0],
            #[0, -5 * math.pi / 180, 0],
            #[0, 0, 15 * math.pi / 180],
            #[0, 10 * math.pi / 180, 0],
            #[0, 0, 0]
        ]

        rot_start_time = 110.5 #to 119

        for i, angle in enumerate(angles):
            if i % 2 == 0:
                dur = 0.5
                delay = 1.5
            else:
                dur = 1
                delay = 1.5
            skull_bobj.move_to(
                new_angle = angle,
                start_time = rot_start_time,
                end_time = rot_start_time + dur
            )


            #Eyes aren't set up to work well as bobjects since I currently don't
            #plan to reuse them a bunch. Probably poor foresight. /shrug
            #They are also rotated in the z-direction with xyz euler angles, so
            #the corrections need to accound for this.
            eye_l.keyframe_insert(data_path = 'rotation_euler', frame = (rot_start_time) * FRAME_RATE)
            eye_l.rotation_euler = [
                eye_l_initial_angle[0] - angle[1],
                eye_l_initial_angle[1] + angle[0],
                eye_l_initial_angle[2] - angle[2]
            ]
            eye_l.keyframe_insert(data_path = 'rotation_euler', frame = (dur + rot_start_time) * FRAME_RATE)

            eye_r.keyframe_insert(data_path = 'rotation_euler', frame = (rot_start_time) * FRAME_RATE)
            eye_r.rotation_euler = [
                eye_r_initial_angle[0] - angle[1],
                eye_r_initial_angle[1] + angle[0],
                eye_r_initial_angle[2] - angle[2]
            ]
            eye_r.keyframe_insert(data_path = 'rotation_euler', frame = (dur + rot_start_time) * FRAME_RATE)

            rot_start_time += delay

    def horizontal_canal_only(self):
        cues = self.subscenes['zoom']

        cam_bobj = bobject.Bobject(
            location = [90, 0, 0],
            rotation_euler = [math.pi / 2, 0, 87 * math.pi / 180],
            name = "Camera Bobject"
        )
        cam_swivel = bobject.Bobject(
            cam_bobj,
            location = [0, 0, 0],
            rotation_euler = [0, 0, -34 * math.pi / 180],
            name = 'Cam swivel'
        )
        cam_swivel.add_to_blender(appear_time = 0, animate = False)
        #cam_bobj.add_to_blender(appear_time = 0, animate = False)
        cam_obj = bpy.data.objects['Camera']
        cam_obj.data.clip_end = 1000
        cam_obj.location = [0, 0, 0]
        cam_obj.parent = cam_bobj.ref_obj

        '''#Look at brain and temporal bone
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
        )'''

        #Look at inner ear
        cam_bobj.move_to(
            new_location = [5, 0, 0],
            new_angle = [92.5 * math.pi / 180, 0, 89 * math.pi / 180],
            start_time = 49,
            end_time = 52
        )

        self.fade_contextual_objects(
            start_time = 50.5,
            end_time = 52,
        )

        self.highlight_sections(
            start_time = 74.5,
            end_time = 76,
            attack = 0.5,
            decay = 0.5,
            parts = ['horizontal']
        )

    def all_canals(self):
        cam_bobj = bobject.Bobject(
            location = [78.8, 0, -1.3],
            rotation_euler = [math.pi / 2, 0, 87 * math.pi / 180],
            name = "Camera Bobject"
        )
        cam_swivel = bobject.Bobject(
            cam_bobj,
            location = [0, 0, 0],
            rotation_euler = [0, -10 * math.pi / 180, -20 * math.pi / 180],
            name = 'Cam swivel'
        )
        cam_swivel.add_to_blender(appear_time = 0, animate = False)
        #cam_bobj.add_to_blender(appear_time = 0, animate = False)
        cam_obj = bpy.data.objects['Camera']
        cam_obj.data.clip_end = 1000
        cam_obj.location = [0, 0, 0]
        cam_obj.parent = cam_bobj.ref_obj


        '''l_red_time = 115
        spin_time = 117.5
        spins = 6
        spin_duration = 6
        r_red_time = 122.5'''


        skin = bpy.data.objects['robertot']
        r_inner_ear = bpy.data.objects['inner ear_from microCT']
        l_inner_ear = bpy.data.objects['inner ear_from microCT.001']
        to_keep = [skin, r_inner_ear, l_inner_ear]
        for obj in bpy.data.objects:
            if obj not in to_keep:
                obj.hide = True
                obj.hide_render = True

        mix = skin.material_slots[0].material.node_tree.nodes['Mix Shader'].inputs[0]
        mix.default_value = 0.9

        cam_swivel.move_to(
            new_angle = [0, -10 * math.pi / 180, 20 * math.pi / 180],
            start_time = 10,
            end_time = 24
        )

        self.highlight_sections(
            start_time = 14,
            end_time = 68,
            parts = ['canals']
        )

        '''slots = r_inner_ear.material_slots
        v_sys_mats = [
            slots[0].material,
            slots[1].material,
            slots[2].material,
            slots[3].material,
            slots[4].material
        ]
        #Set initial state for inner ear materials
        for mat in v_sys_mats:
            nodes = mat.node_tree.nodes
            mix = nodes['Mix Shader']
            mix.inputs[0].default_value = 0
            princ = nodes['Principled BSDF']
            color = princ.inputs[0]
            color.default_value = [0, 1, 0, 1]

        #Make separate materials for left inner ear to animate separately
        for slot in l_inner_ear.material_slots:
            mat_copy = slot.material.copy()
            slot.material = mat_copy


        for mat in v_sys_mats:
            nodes = mat.node_tree.nodes
            princ = nodes['Principled BSDF']
            color = princ.inputs[0]

            color.keyframe_insert(
                data_path = 'default_value',
                frame = l_red_time * FRAME_RATE
            )
            color.default_value = [1, 0, 0, 1]
            color.keyframe_insert(
                data_path = 'default_value',
                frame = l_red_time * FRAME_RATE + 2 * OBJECT_APPEARANCE_TIME
            )'''

        '''skull = bpy.data.objects['Skull_Top']
        skull_bobj = bobject.Bobject(objects = [skull])
        skull_bobj.add_to_blender(appear_time = 0, unhide = False)
        skull_bobj.move_to(
            new_angle = [0, 0, spins * 2 * math.pi],
            start_time = spin_time,
            end_time = spin_time + spin_duration
        )'''

        '''for slot in l_inner_ear.material_slots:
            nodes = slot.material.node_tree.nodes
            color = nodes['Principled BSDF'].inputs[0]

            color.keyframe_insert(
                data_path = 'default_value',
                frame = r_red_time * FRAME_RATE
            )
            color.default_value = [1, 0, 0, 1]
            color.keyframe_insert(
                data_path = 'default_value',
                frame = r_red_time * FRAME_RATE + 2 * OBJECT_APPEARANCE_TIME
            )

        cam_swivel.move_to(
            new_angle = [75 * math.pi / 180, 0, 45 * math.pi / 180],
            start_time = 110,
            end_time = 127
        )'''

        '''rate = 0.025
        cam_swivel.spin(
            axis = 2,
            spin_rate = rate,
            start_time = zoom_out_time - 1 / rate * 0.125
        )'''

    def fade_contextual_objects(
        self,
        parts = [],
        start_time = None,
        end_time = None,
        start_time_2 = None,
        start_time_3 = None,
        transition_time = None
    ):
        if start_time_2 == None: #Will just assume the rest is unspecified
            start_time_2 = start_time + (end_time - start_time) / 3
            start_time_3 = start_time + 2 * (end_time - start_time) / 3
            transition_time = (end_time - start_time) / 2 #overlap a bit

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
                start_time = start_time,
                duration_time = transition_time,
                extent = 1
            )
        for i, obj in enumerate(second_fade):
            fade(
                object = obj,
                start_time = start_time_2,
                duration_time = transition_time,
                extent = 1
            )
        for i, obj in enumerate(third_fade):
            fade(
                object = obj,
                start_time = start_time_3,
                duration_time = transition_time,
                extent = 1 #0.95
            )

    def highlight_sections(
        self,
        parts = [],
        start_time = None,
        end_time = None,
        attack = 1,
        decay = 1
    ):
        if 'cochlea' in parts:
            #ear = bpy.data.objects['inner ear_from microCT']
            coch_shader = bpy.data.materials['clear material'].node_tree.nodes['Principled BSDF']
            coch_color = coch_shader.inputs[0]
            coch_color.keyframe_insert(data_path = 'default_value', frame = start_time * FRAME_RATE)
            old_value = list(coch_color.default_value)
            coch_color.default_value = [0, 1, 0, 1]
            coch_color.keyframe_insert(data_path = 'default_value', frame = (start_time + attack) * FRAME_RATE)
            coch_color.keyframe_insert(data_path = 'default_value', frame = (end_time - decay) * FRAME_RATE)
            coch_color.default_value = old_value
            coch_color.keyframe_insert(data_path = 'default_value', frame = end_time * FRAME_RATE)

        if 'vestibule' in parts:
            #ear = bpy.data.objects['inner ear_from microCT']
            vest_shader = bpy.data.materials['vestibule'].node_tree.nodes['Principled BSDF']
            vest_color = vest_shader.inputs[0]
            vest_color.keyframe_insert(data_path = 'default_value', frame = start_time * FRAME_RATE)
            old_value = list(vest_color.default_value)
            vest_color.default_value = [0, 1, 0, 1]
            vest_color.keyframe_insert(data_path = 'default_value', frame = (start_time + attack) * FRAME_RATE)
            vest_color.keyframe_insert(data_path = 'default_value', frame = (end_time - decay) * FRAME_RATE)
            vest_color.default_value = old_value
            vest_color.keyframe_insert(data_path = 'default_value', frame = end_time * FRAME_RATE)

        if 'canals' in parts:
            parts += ['posterior', 'horizontal', 'superior']

        if 'posterior' in parts:
            canal_shader = bpy.data.materials['posterior'].node_tree.nodes['Principled BSDF']
            canal_color = canal_shader.inputs[0]
            canal_color.keyframe_insert(data_path = 'default_value', frame = start_time * FRAME_RATE)
            old_value = list(canal_color.default_value)
            canal_color.default_value = [0, 1, 0, 1]
            canal_color.keyframe_insert(data_path = 'default_value', frame = (start_time + attack) * FRAME_RATE)
            canal_color.keyframe_insert(data_path = 'default_value', frame = (end_time - decay) * FRAME_RATE)
            canal_color.default_value = old_value
            canal_color.keyframe_insert(data_path = 'default_value', frame = end_time * FRAME_RATE)

        if 'horizontal' in parts:
            canal_shader = bpy.data.materials['horizontal'].node_tree.nodes['Principled BSDF']
            canal_color = canal_shader.inputs[0]
            canal_color.keyframe_insert(data_path = 'default_value', frame = start_time * FRAME_RATE)
            old_value = list(canal_color.default_value)
            canal_color.default_value = [0, 1, 0, 1]
            canal_color.keyframe_insert(data_path = 'default_value', frame = (start_time + attack) * FRAME_RATE)
            canal_color.keyframe_insert(data_path = 'default_value', frame = (end_time - decay) * FRAME_RATE)
            canal_color.default_value = old_value
            canal_color.keyframe_insert(data_path = 'default_value', frame = end_time * FRAME_RATE)

        if 'superior' in parts:
            canal_shader = bpy.data.materials['superior'].node_tree.nodes['Principled BSDF']
            canal_color = canal_shader.inputs[0]
            canal_color.keyframe_insert(data_path = 'default_value', frame = start_time * FRAME_RATE)
            old_value = list(canal_color.default_value)
            canal_color.default_value = [0, 1, 0, 1]
            canal_color.keyframe_insert(data_path = 'default_value', frame = (start_time + attack) * FRAME_RATE)
            canal_color.keyframe_insert(data_path = 'default_value', frame = (end_time - decay) * FRAME_RATE)
            canal_color.default_value = old_value
            canal_color.keyframe_insert(data_path = 'default_value', frame = end_time * FRAME_RATE)

        if 'horizontal cupula' in parts:
            emission = bpy.data.materials['nerve material'].node_tree.nodes['Emission']
            emission.inputs[0].default_value = [1, 0, 0, 1]

            mix = bpy.data.materials['nerve material'].node_tree.nodes['Mix Shader.001']
            frac = mix.inputs[0]
            frac.keyframe_insert(data_path = 'default_value', frame = start_time * FRAME_RATE)
            old_value = frac.default_value
            #frac.default_value = [0, 1, 0, 1]
            frac.default_value = 0.5
            frac.keyframe_insert(data_path = 'default_value', frame = (start_time + attack) * FRAME_RATE)
            frac.keyframe_insert(data_path = 'default_value', frame = (end_time - decay) * FRAME_RATE)
            frac.default_value = old_value
            frac.keyframe_insert(data_path = 'default_value', frame = end_time * FRAME_RATE)

        if 'utricle' in parts:
            emission = bpy.data.materials['utricle'].node_tree.nodes['Emission']
            emission.inputs[0].default_value = [1, 0, 0, 1]

            mix = bpy.data.materials['utricle'].node_tree.nodes['Mix Shader.001']
            frac = mix.inputs[0]
            frac.keyframe_insert(data_path = 'default_value', frame = start_time * FRAME_RATE)
            old_value = frac.default_value
            #frac.default_value = [0, 1, 0, 1]
            frac.default_value = 0.5
            frac.keyframe_insert(data_path = 'default_value', frame = (start_time + attack) * FRAME_RATE)
            frac.keyframe_insert(data_path = 'default_value', frame = (end_time - decay) * FRAME_RATE)
            frac.default_value = old_value
            frac.keyframe_insert(data_path = 'default_value', frame = end_time * FRAME_RATE)

        if 'saccule' in parts:
            emission = bpy.data.materials['saccule'].node_tree.nodes['Emission']
            emission.inputs[0].default_value = [1, 0, 0, 1]

            mix = bpy.data.materials['saccule'].node_tree.nodes['Mix Shader.001']
            frac = mix.inputs[0]
            frac.keyframe_insert(data_path = 'default_value', frame = start_time * FRAME_RATE)
            old_value = frac.default_value
            #frac.default_value = [0, 1, 0, 1]
            frac.default_value = 0.5
            frac.keyframe_insert(data_path = 'default_value', frame = (start_time + attack) * FRAME_RATE)
            frac.keyframe_insert(data_path = 'default_value', frame = (end_time - decay) * FRAME_RATE)
            frac.default_value = old_value
            frac.keyframe_insert(data_path = 'default_value', frame = end_time * FRAME_RATE)

    def otoconia_wiggle(
        self,
        start_time = None,
        end_time = None,
        num_cycles = 2
    ):
        '''mix_shader = bpy.data.materials['u_otoconia'].node_tree.nodes['Mix Shader']
        mix = mix_shader.inputs[0]
        mix.keyframe_insert(data_path = 'default_value', frame = self.otoconia_time * FRAME_RATE)
        old_value = mix.default_value
        mix.default_value = 1
        mix.keyframe_insert(data_path = 'default_value', frame = (self.otoconia_time + 1) * FRAME_RATE)
        mix.keyframe_insert(data_path = 'default_value', frame = (self.dislodged_time) * FRAME_RATE)
        mix.default_value = old_value
        mix.keyframe_insert(data_path = 'default_value', frame = (self.dislodged_time + 1) * FRAME_RATE)
        '''
        wiggle_start = start_time
        wiggle_end = end_time
        wiggle_angle = 30 #degrees
        wiggle_disp = 0.01 #cm
        duration = wiggle_end - wiggle_start

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

        '''#Highlight utricle
        utricle = bpy.data.objects['Utricle']
        highlight_object(
            object = utricle,
            start_time = wiggle_start,
            duration_time = 5
        )'''
"""
class AnatomyScene(Scene):
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

        '''#Dix Hallpike lean back
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
        )'''



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


"""
