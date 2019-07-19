import bpy
import mathutils

import inspect
import imp
from random import random, uniform
import math
import time
from copy import deepcopy

import constants
imp.reload(constants)
from constants import *

import helpers
imp.reload(helpers)
from helpers import *

#Blender Object
class Bobject(object):
    """docstring for ."""
    #Create object data
    def __init__(self, *subbobjects, **kwargs):
        super().__init__()
        self.kwargs = kwargs #This is used in the get_from_kwargs() method

        self.name = self.get_from_kwargs('name', 'bobject')

        #Would be cleaner elsewhere to override the setter to update
        #self.ref_obj.scale when self.intrinsic_scale is updated
        #(similarly for any attribute that's actually on the ref_obj)
        #self.appear_frame = self.get_from_kwargs('appear_frame', 0)

        ref_obj = bpy.data.objects.new(name = self.name, object_data = None)
        ref_obj.location = self.get_from_kwargs('location', (0, 0, 0) )
        ref_obj.rotation_euler = self.get_from_kwargs('rotation_euler', (0, 0, 0) )
        #TODO: Change self.intrinsic_scale to self.intrinsic_scale to differentiate it from
        #the actual current scale of the object after manipulations.
        self.intrinsic_scale = self.get_from_kwargs('scale', 1)
        if isinstance(self.intrinsic_scale, int) or isinstance(self.intrinsic_scale, float):
            self.intrinsic_scale = [self.intrinsic_scale] * 3
        ref_obj.scale = self.intrinsic_scale
        ref_obj.name = self.name
        self.ref_obj = ref_obj

        #Blender objects with this bobject as the container
        self.objects = self.get_from_kwargs('objects', [])
        for obj in self.objects:
            obj.parent = ref_obj

        #Other bobject containers which handle themselves
        self.subbobjects = self.get_from_kwargs('subbobjects', [])
        for bobj in subbobjects:
            self.add_subbobject(bobj)

        self.superbobject = None #Changed when initializing a super
        self.appear_with_super = self.get_from_kwargs('appear_with_super', True)

        material_set = self.get_from_kwargs('mat', None)
        if material_set != None:
            apply_material(self.ref_obj.children[0], material_set)

        self.added_to_blender = False

    def get_from_kwargs(self, kwarg_str, default):
        if kwarg_str in self.kwargs:
            return self.kwargs[kwarg_str]
        else:
            return default

    def add_subbobject(self, bobj):
        self.subbobjects.append(bobj)
        bobj.ref_obj.parent = self.ref_obj
        bobj.superbobject = self

    def add_to_blender(
        self,
        appear_frame = None,
        appear_time = None,
        animate = True,
        subbobject_timing = 'start',
        transition_time = OBJECT_APPEARANCE_TIME,
        is_creature = False,
        unhide = True
    ):
        if appear_time != None:
            if appear_frame != None:
                raise Warning("You defined both appear frame and appear time. " +\
                              "Just do one, ya dick.")
            appear_frame = appear_time * FRAME_RATE
        elif appear_frame == None:
            appear_frame = 0

        if self.added_to_blender == False:

            main_obj = self.ref_obj
            if main_obj.name not in bpy.context.scene.objects:
                bpy.context.scene.objects.link(main_obj)
            else:
                pass
                #print("Re-adding " + self.name)

            self.appear_frame = appear_frame

            if unhide == True:
                main_obj.hide = True
                main_obj.hide_render = True
                main_obj.keyframe_insert(data_path="hide", frame = appear_frame - 1)
                main_obj.keyframe_insert(data_path="hide_render", frame = appear_frame - 1)
                main_obj.hide = False
                main_obj.keyframe_insert(data_path="hide", frame = appear_frame)


                for obj in self.objects:
                    if obj.name not in bpy.context.scene.objects:
                        bpy.context.scene.objects.link(obj)
                    link_descendants(obj) #Useful for multi-part imports from .blend files
                    hide_self_and_descendants(
                        obj,
                        keyframes = True,
                        frame = appear_frame - 1
                    )
                    hide_self_and_descendants(
                        obj,
                        hide = False, #Unhide objects
                        keyframes = True,
                        frame = appear_frame
                    )

            if animate == False:
                if self.superbobject == None:
                    scale_up_frame = appear_frame - transition_time
                #Might be able to get rid of this once morphing is fixed
                else:
                    #print(self.superbobject.appear_frame)
                    scale_up_frame = self.superbobject.appear_frame - transition_time
                #Makes the scale-up happen before the unhiding if we don't want
                #the bobject to animate in
            else:
                scale_up_frame = appear_frame
            if is_creature == True:
                duration = MATURATION_TIME
            else:
                duration = transition_time

            main_obj.scale = [0, 0, 0]
            main_obj.keyframe_insert(data_path="scale", frame = scale_up_frame)
            main_obj.scale = self.intrinsic_scale
            main_obj.keyframe_insert(data_path="scale", frame = scale_up_frame + duration)
            #don't need to do this for contained objects because it happens through
            #parenting

            self.added_to_blender = True

        self.add_subbobjects(
            appear_frame = appear_frame,
            subbobject_timing = subbobject_timing
        )

    def add_subbobjects(
        self,
        appear_frame = None,
        appear_time = None,
        animate = True,
        transition_time = OBJECT_APPEARANCE_TIME,
        subbobject_timing = 'start'
    ):
        if appear_time != None:
            if appear_frame != None:
                raise Warning("You defined both appear frame and appear time. " +\
                              "Just do one, ya dick.")
            appear_frame = appear_time * FRAME_RATE
        elif appear_frame == None:
            appear_frame = 0

        followers = [x for x in self.subbobjects if x.appear_with_super == True and \
                            x.added_to_blender == False]

        if subbobject_timing == 'start':
            for bobj in followers:
                bobj.add_to_blender(
                    appear_frame = appear_frame,
                    animate = animate,
                    transition_time = transition_time
                )
        elif subbobject_timing == 'flurry':
            timing = transition_time / len(self.subbobjects)
            for i, bobj in enumerate(followers):
                bobj.add_to_blender(appear_frame = appear_frame + i * timing)
        elif isinstance(subbobject_timing, int):
            for i, bobj in enumerate(followers):
                bobj.add_to_blender(appear_frame = appear_frame + subbobject_timing)
        elif isinstance(subbobject_timing, list):
            if len(subbobject_timing) != len(followers):
                raise Warning("Subbobject list and timing list are mismatched.")
            for frame, bobj in zip(subbobject_timing, followers):
                #frame += subbobject_delay
                bobj.add_to_blender(appear_frame = appear_frame + frame, animate = True)
        else:
            raise Warning("So many types are accepted for subbobject_timing, "
                          "but you still managed to give an invalid value.")

    #Keyframe additions
    def disappear(
        self,
        disappear_frame = None,
        disappear_time = None,
        animate = True,
        no_shrink = False,
        is_creature = False,
        duration_frames = OBJECT_APPEARANCE_TIME
    ):
        if disappear_time != None:
            if disappear_frame != None:
                raise Warning("You defined both disappear frame and disappear time. " +\
                              "Just do one, ya dick.")
            disappear_frame = disappear_time * FRAME_RATE
        if disappear_frame == None:
            raise Warning('Must specify frame or time for bobject disappearance')

        main_obj = self.ref_obj

        main_obj.hide = True
        main_obj.hide_render = True
        main_obj.keyframe_insert(data_path="hide", frame = disappear_frame)
        main_obj.keyframe_insert(data_path="hide_render", frame = disappear_frame)

        for obj in self.objects:
            hide_self_and_descendants(
                obj,
                keyframes = True,
                frame = disappear_frame
            )

        if is_creature == True:
            duration_frames = MATURATION_TIME

        if animate == True:
            #scale_down_frame = disappear_frame + OBJECT_APPEARANCE_TIME
            #Makes the scale-down happen after the hiding if we don't want
            #the bobject to animate out
            scale_down_frame = disappear_frame

            #Uses current scale. This assumes keyframes have been added
            #chronologically, so the previous keyframe agrees with the current
            #object scale.
            main_obj.keyframe_insert(data_path="scale", frame = scale_down_frame - duration_frames)
            main_obj.scale = [0, 0, 0]
            main_obj.keyframe_insert(data_path="scale", frame = scale_down_frame)

        else:
            scale_down_frame = disappear_frame



        for subbobj in self.subbobjects:
            subbobj.disappear(disappear_frame = disappear_frame, animate = False)

    def move_to(
        self,
        start_time = None,
        end_time = None,
        start_frame = None,
        end_frame = None,
        displacement = None,
        new_location = None,
        new_scale = None,
        new_angle = None
    ):
        #Convert time args to frames
        if start_time != None:
            if start_frame != None:
                raise Warning("You defined both start frame and start time. " +\
                              "Just do one, ya dick.")
            start_frame = int(start_time * FRAME_RATE)
        if end_time != None:
            if end_frame != None:
                raise Warning("You defined both end frame and end time. " +\
                              "Just do one, ya dick.")
            end_frame = int(end_time * FRAME_RATE)

        #Ensure start and end frame defined.
        if start_frame == None:
            if end_frame == None:
                raise Warning('Need start frame and/or end frame for move_to')
            else:
                start_frame = end_frame - OBJECT_APPEARANCE_TIME

        if end_frame == None:
            end_frame = start_frame + OBJECT_APPEARANCE_TIME

        obj = self.ref_obj
        if displacement != None:
            obj.keyframe_insert(data_path="location", frame = start_frame)
            for i in range(len(self.ref_obj.location)):
                self.ref_obj.location[i] += displacement[i]
            obj.keyframe_insert(data_path="location", frame = end_frame)
        if new_location != None:
            obj.keyframe_insert(data_path="location", frame = start_frame)
            obj.location = new_location
            obj.keyframe_insert(data_path="location", frame = end_frame)
        if new_scale != None:
            #if end_frame >= scale_until:
            #    raise Warning('In move_to(), end frame is after scale_until')
            obj.keyframe_insert(data_path="scale", frame = start_frame)
            if isinstance(new_scale, int) or isinstance(new_scale, float):
                new_scale = [new_scale] * 3
            obj.scale = new_scale
            self.intrinsic_scale = new_scale
            obj.keyframe_insert(data_path="scale", frame = end_frame)
        if new_angle != None:
            obj.keyframe_insert(data_path="rotation_euler", frame = start_frame)
            obj.rotation_euler = new_angle
            obj.keyframe_insert(
                data_path="rotation_euler",
                frame = end_frame
            )
        #bpy.context.scene.update()

    #Deprecated, because why just pick one axis?
    def spiny(
        self,
        **kwargs
        #spin_rate = 1, #Revolutions per second
        #start_time = None,
        #end_time = None,
        #start_frame = None,
        #end_frame = None
    ):
        self.spin(**kwargs) #Default axis is y

    def spin(
        self,
        axis = 1,
        spin_rate = 1, #Revolutions per second
        start_time = None,
        end_time = None,
        start_frame = None,
        end_frame = None,
        constant_rate = True
    ):
        if start_time != None:
            if start_frame != None:
                raise Warning("You defined both start frame and start time. " +\
                              "Just do one, ya dick.")
            start_frame = int(start_time * FRAME_RATE)
        if end_time != None:
            if end_frame != None:
                raise Warning("You defined both end frame and end time. " +\
                              "Just do one, ya dick.")
            end_frame = int(end_time * FRAME_RATE)

        if start_frame == None:
            raise Warning('Need start frame for spin function')
        if end_frame == None:
            end_frame = bpy.context.scene.frame_end

        obj = self.ref_obj
        obj.keyframe_insert(data_path="rotation_euler", frame = start_frame)

        new_y = spin_rate * 2 * math.pi * (end_frame - start_frame) / FRAME_RATE

        obj.rotation_euler[axis] = new_y
        obj.keyframe_insert(
            data_path="rotation_euler",
            frame = end_frame
        )

        if constant_rate == True:
            for fc in self.ref_obj.animation_data.action.fcurves:
                if fc.data_path == 'rotation_euler':
                    #fc.extrapolation = 'LINEAR' # Set extrapolation type
                    # Iterate over this fcurve's keyframes and set handles to vector
                    for kp in fc.keyframe_points:
                        #kp.handle_left_type  = 'VECTOR'
                        #kp.handle_right_type = 'VECTOR'
                        kp.interpolation = 'LINEAR'

    def pulse(
        self,
        start_time = None,
        start_frame = None,
        factor = 1.2,
        attack = None,
        decay = None,
        duration_time = None,
        duration = None,
    ):
        if start_time != None:
            if start_frame != None:
                raise Warning("You defined both start_frame and start_time. " +\
                              "Just do one, ya dick.")
            start_frame = start_time * FRAME_RATE
        if duration_time != None:
            if duration != None:
                raise Warning("You defined duration by both frames and time. " +\
                              "Just do one, ya dick.")
            duration = duration_time * FRAME_RATE
        else:
            if duration == None:
                duration = OBJECT_APPEARANCE_TIME * 4

        end_time = start_time + duration_time

        if attack == None:
            if end_time == None:
                attack = OBJECT_APPEARANCE_TIME / FRAME_RATE
            elif end_time - start_time > 2:
                attack = OBJECT_APPEARANCE_TIME / FRAME_RATE
            else:
                attack = (end_time - start_time) / 2
        attack_frames = attack * FRAME_RATE

        if decay == None:
            if end_time == None:
                decay = OBJECT_APPEARANCE_TIME / FRAME_RATE
            elif end_time - start_time > 2:
                decay = OBJECT_APPEARANCE_TIME / FRAME_RATE
            else:
                decay = (end_time - start_time) / 2
        decay_frames = decay * FRAME_RATE

        obj = self.ref_obj
        obj.keyframe_insert(data_path="scale", frame = start_frame)
        obj.scale *= factor
        obj.keyframe_insert(data_path="scale", frame = start_frame + attack_frames)
        obj.keyframe_insert(data_path="scale", frame = start_frame + duration - decay_frames)
        obj.scale /= factor
        obj.keyframe_insert(data_path="scale", frame = start_frame + duration)

    def color_shift(
        self,
        color = COLORS_SCALED[3],
        start_time = None,
        start_frame = None,
        duration_time = 2,
        duration = None,
        shift_time = OBJECT_APPEARANCE_TIME,
        obj = None,
        color_gradient = None
    ):
        if start_time != None:
            if start_frame != None:
                raise Warning("You defined both frame and time. " +\
                              "Just do one, ya dick.")
            start_frame = int(start_time * FRAME_RATE)

        if duration_time != None:
            duration = duration_time * FRAME_RATE
            if duration < shift_time * 2:
                shift_time = duration / 2
                print('Adjusted shift time')

        #automatically finds object for simple bobjects
        if obj == None:
            obj = self.ref_obj.children[0]
        try:
            mat_copy = obj.material_slots[0].material.copy()
        except:
            print(obj)
            raise()
        obj.active_material = mat_copy
        color_node = mat_copy.node_tree.nodes[-1]
        color_field = color_node.inputs[0]

        if color_gradient == None:
            if duration != None:
                #If duration is finite, store original color
                original_color = list(color_field.default_value)


            color_field.keyframe_insert(data_path = 'default_value', frame = start_frame)
            color_field.default_value = color
            color_field.keyframe_insert(data_path = 'default_value', frame = start_frame + shift_time)

            #Viewport color
            mat_copy.keyframe_insert(data_path = 'diffuse_color', frame = start_frame)
            mat_copy.diffuse_color = color[:3]
            mat_copy.keyframe_insert(data_path = 'diffuse_color', frame = start_frame + shift_time)

            if duration != None:
                #If duration is finite, return to original color
                color_field.keyframe_insert(data_path = 'default_value', frame = start_frame + duration - shift_time)
                color_field.default_value = original_color
                color_field.keyframe_insert(data_path = 'default_value', frame = start_frame + duration)

                mat_copy.keyframe_insert(data_path = 'diffuse_color', frame = start_frame + duration - shift_time)
                mat_copy.diffuse_color = original_color[:3]
                mat_copy.keyframe_insert(data_path = 'diffuse_color', frame = start_frame + duration)

        #No actual need for keyframes right now.
        else: #Gradient
            #These default value work for arrows
            if 'color_1' not in color_gradient:
                color_gradient['color_1'] = color_field.default_value
            if 'color_2' not in color_gradient:
                color_gradient['color_2'] = color
            if 'rotation' not in color_gradient:
                color_gradient['rotation'] = [0, 0, - math.pi / 2]
            if 'translation' not in color_gradient:
                color_gradient['translation'] = [0, 0, 0]
            if 'scale' not in color_gradient:
                color_gradient['scale'] = [0.2, 0.2, 0]

            add_color_gradient_to_mat(mat_copy, color_gradient)

    def wobble(
        self,
        axis = 2,
        max_angle = 2, #degrees
        frequency = 4, #Hertz
        start_time = None,
        end_time = None
    ):
        if start_time == None:
            raise Warning('Need start_time for wobble')
        if end_time == None:
            raise Warning('Need end_time for wobble')

        inc = 1 / frequency / 2
        max_angle_rad = max_angle * math.pi / 180

        time = start_time
        self.ref_obj.keyframe_insert(
            data_path = 'rotation_euler',
            frame = start_time * FRAME_RATE
        )
        time += inc
        self.ref_obj.rotation_euler[axis] += max_angle_rad
        self.ref_obj.keyframe_insert(
            data_path = 'rotation_euler',
            frame = time * FRAME_RATE
        )
        while time < end_time - inc:
            time += inc
            self.ref_obj.rotation_euler[axis] -= 2 * max_angle_rad
            self.ref_obj.keyframe_insert(
                data_path = 'rotation_euler',
                frame = time * FRAME_RATE
            )
            time += inc
            self.ref_obj.rotation_euler[axis] += 2 * max_angle_rad
            self.ref_obj.keyframe_insert(
                data_path = 'rotation_euler',
                frame = time * FRAME_RATE
            )
        time += inc
        self.ref_obj.rotation_euler[axis] -= max_angle_rad
        self.ref_obj.keyframe_insert(
            data_path = 'rotation_euler',
            frame = time * FRAME_RATE
        )


    def tweak_colors_recursive(self, obj = None):
        if obj == None:
            obj = self.ref_obj
        color_to_primer_palette(obj = obj)
        for child in obj.children:
            self.tweak_colors_recursive(obj = child)

    """def blob_wave(
        self,
        start_time = 0,
        duration = 0,
        end_pause_duration = 0
    ):
        #This function only works for blob creatures. Maybe they deserve their
        #own subclass of bobject.
        start_frame = start_time * FRAME_RATE
        end_pause_frames = end_pause_duration * FRAME_RATE
        duration_frames = duration * FRAME_RATE

        wave_cycle_length = 8
        cycle_error = 4
        num_wave_cycles = math.floor(duration_frames / wave_cycle_length)
        duration_frames = num_wave_cycles * wave_cycle_length

        l_arm_up_z = 1
        l_arm_down_z = -1
        l_arm_out_y = 3
        l_arm_out_x = 0.5
        r_arm_up_z = -1
        r_arm_down_z = 1
        r_arm_out_y = -5

        #These labels are from the point of view of the blob, which is opposite
        #from how they're labeled in the template .blend file. Huzzah.
        l_arm = None
        r_arm = None
        for child in self.ref_obj.children:
            if 'boerd_blob' in child.name:
                l_arm = child.pose.bones[1]
                r_arm = child.pose.bones[2]

        l_arm.keyframe_insert(
            data_path = "rotation_quaternion",
            frame = start_frame
        )
        initial_angle = deepcopy(l_arm.rotation_quaternion)
        l_arm.rotation_quaternion[1] = l_arm_out_x
        l_arm.rotation_quaternion[2] = l_arm_out_y
        l_arm.rotation_quaternion[3] = l_arm_down_z
        l_arm.keyframe_insert(
            data_path = "rotation_quaternion",
            frame = start_frame + wave_cycle_length + uniform(-cycle_error, cycle_error)
        )

        #waves
        for i in range(1, num_wave_cycles - 1): #last one gets overridden
            if i % 2 == 1:
                l_arm.rotation_quaternion[3] = l_arm_up_z
            if i % 2 == 0:
                l_arm.rotation_quaternion[3] = l_arm_down_z
            l_arm.keyframe_insert(
                data_path = "rotation_quaternion",
                frame = start_frame + wave_cycle_length + uniform(-cycle_error, cycle_error) + i * wave_cycle_length
            )

        #And back
        l_arm.keyframe_insert(
            data_path = "rotation_quaternion",
            frame = start_frame + duration_frames - wave_cycle_length  + uniform(-cycle_error, cycle_error)
        )
        #if end_pause_frames != 0:
        l_arm.keyframe_insert(
            data_path = "rotation_quaternion",
            frame = start_frame + duration_frames - wave_cycle_length + end_pause_frames
        )
        l_arm.rotation_quaternion = initial_angle
        l_arm.keyframe_insert(
            data_path = "rotation_quaternion",
            frame = start_frame + duration_frames + end_pause_frames
        )

        #Right arm
        r_arm.keyframe_insert(
            data_path = "rotation_quaternion",
            frame = start_frame
        )
        initial_angle = deepcopy(r_arm.rotation_quaternion)
        r_arm.rotation_quaternion[2] = r_arm_out_y
        r_arm.rotation_quaternion[3] = r_arm_down_z
        r_arm.keyframe_insert(
            data_path = "rotation_quaternion",
            frame = start_frame + wave_cycle_length + uniform(-cycle_error, cycle_error)
        )

        #waves
        for i in range(1, num_wave_cycles - 1):
            if i % 2 == 1:
                r_arm.rotation_quaternion[3] = r_arm_up_z
            if i % 2 == 0:
                r_arm.rotation_quaternion[3] = r_arm_down_z
            r_arm.keyframe_insert(
                data_path = "rotation_quaternion",
                frame = start_frame + wave_cycle_length + uniform(-cycle_error, cycle_error) + i * wave_cycle_length
            )

        #And back
        r_arm.keyframe_insert(
            data_path = "rotation_quaternion",
            frame = start_frame + duration_frames - wave_cycle_length + uniform(-cycle_error, cycle_error)
        )
        r_arm.keyframe_insert(
            data_path = "rotation_quaternion",
            frame = start_frame + duration_frames - wave_cycle_length + end_pause_frames
        )
        r_arm.rotation_quaternion = initial_angle
        r_arm.keyframe_insert(
            data_path = "rotation_quaternion",
            frame = start_frame + duration_frames + end_pause_frames
        )

    def blob_scoop(
        self,
        start_time = 0,
        duration = 0,
        top_pause_time = 0
    ):
        #This function only works for blob creatures. Maybe they deserve their
        #own subclass of bobject.
        start_frame = start_time * FRAME_RATE
        duration_frames = (duration - top_pause_time) * FRAME_RATE

        l_arm_up_z = -2.7
        l_arm_down_z = 3
        l_arm_out_y = -7.6
        l_arm_forward_x = -3


        r_arm_up_z = -3.6
        r_arm_down_z = 1.8
        r_arm_out_y = -12.7
        r_arm_forward_x = -2.2

        #These labels are from the point of view of the blob, which is opposite
        #from how they're labeled in the template .blend file. Huzzah.
        l_arm = None
        r_arm = None
        for child in self.ref_obj.children:
            if 'boerd_blob' in child.name:
                l_arm = child.pose.bones[1]
                r_arm = child.pose.bones[2]

        #Left arm out
        l_arm.keyframe_insert(
            data_path = "rotation_quaternion",
            frame = start_frame
        )
        initial_angle = deepcopy(l_arm.rotation_quaternion)
        l_arm.rotation_quaternion[1] = l_arm_forward_x
        l_arm.rotation_quaternion[2] = l_arm_out_y
        l_arm.rotation_quaternion[3] = l_arm_down_z
        l_arm.keyframe_insert(
            data_path = "rotation_quaternion",
            frame = start_frame + duration_frames / 3
        )

        #scoop
        l_arm.rotation_quaternion[3] = l_arm_up_z
        l_arm.keyframe_insert(
            data_path = "rotation_quaternion",
            frame = start_frame + 2 * duration_frames / 3
        )
        l_arm.keyframe_insert(
            data_path = "rotation_quaternion",
            frame = start_frame + 2 * duration_frames / 3 + top_pause_time * FRAME_RATE
        )

        #And back
        l_arm.rotation_quaternion = initial_angle
        l_arm.keyframe_insert(
            data_path = "rotation_quaternion",
            frame = start_frame + duration_frames + top_pause_time * FRAME_RATE
        )

        #Right arm
        r_arm.keyframe_insert(
            data_path = "rotation_quaternion",
            frame = start_frame
        )
        initial_angle = deepcopy(r_arm.rotation_quaternion)
        r_arm.rotation_quaternion[1] = r_arm_forward_x
        r_arm.rotation_quaternion[2] = r_arm_out_y
        r_arm.rotation_quaternion[3] = r_arm_down_z
        r_arm.keyframe_insert(
            data_path = "rotation_quaternion",
            frame = start_frame + duration_frames / 3
        )

        #scoop
        r_arm.rotation_quaternion[3] = r_arm_up_z
        r_arm.keyframe_insert(
            data_path = "rotation_quaternion",
            frame = start_frame + 2 * duration_frames / 3
        )
        r_arm.keyframe_insert(
            data_path = "rotation_quaternion",
            frame = start_frame + 2 * duration_frames / 3
        )

        #And back
        r_arm.rotation_quaternion = initial_angle
        r_arm.keyframe_insert(
            data_path = "rotation_quaternion",
            frame = start_frame + duration_frames + top_pause_time * FRAME_RATE
        )

    def evil_pose(
        self,
        start_time = None,
        end_time = None,
        attack = None,
        decay = None
    ):
        if start_time == None:
            raise Warning('Need start time for evil pose')

        start_frame = start_time * FRAME_RATE
        end_frame = None
        if end_time != None:
            end_frame = end_time * FRAME_RATE

        if attack == None:
            if end_time == None:
                attack = OBJECT_APPEARANCE_TIME / FRAME_RATE
            elif end_time - start_time > 2:
                attack = OBJECT_APPEARANCE_TIME / FRAME_RATE
            else:
                attack = (end_time - start_time) / 4
        attack_frames = attack * FRAME_RATE

        if decay == None:
            if end_time == None:
                decay = OBJECT_APPEARANCE_TIME / FRAME_RATE
            elif end_time - start_time > 2:
                decay = OBJECT_APPEARANCE_TIME / FRAME_RATE
            else:
                decay = (end_time - start_time) / 4
        decay_frames = decay * FRAME_RATE


        #Blob's left arm up = [1, -2.5, -8.1, -1.5]
        #Blob's right arm up = [1, 0.4, -36.6, -9]

        #These labels are from the point of view of the blob, which is opposite
        #from how they're labeled in the template .blend file. Huzzah.
        l_arm = None
        r_arm = None
        for child in self.ref_obj.children:
            if 'boerd_blob' in child.name:
                l_arm = child.pose.bones[1]
                r_arm = child.pose.bones[2]

        #Left arm up
        l_arm.keyframe_insert(
            data_path = "rotation_quaternion",
            frame = start_frame
        )
        initial_angle = list(l_arm.rotation_quaternion)
        l_arm.rotation_quaternion = [1, -2.5, -8.1, -1.5]
        l_arm.keyframe_insert(
            data_path = "rotation_quaternion",
            frame = start_frame + attack_frames
        )

        #Shakes?

        #And back
        if end_frame != None:
            l_arm.keyframe_insert(
                data_path = "rotation_quaternion",
                frame = end_frame - decay_frames
            )
            l_arm.rotation_quaternion = initial_angle
            l_arm.keyframe_insert(
                data_path = "rotation_quaternion",
                frame = end_frame
            )

        #Right arm up
        r_arm.keyframe_insert(
            data_path = "rotation_quaternion",
            frame = start_frame
        )
        initial_angle = list(r_arm.rotation_quaternion)
        r_arm.rotation_quaternion = [1, -2.5, -8.1, -1.5]
        r_arm.keyframe_insert(
            data_path = "rotation_quaternion",
            frame = start_frame + attack_frames
        )

        #And back
        if end_frame != None:
            r_arm.keyframe_insert(
                data_path = "rotation_quaternion",
                frame = end_frame - decay_frames
            )
            r_arm.rotation_quaternion = initial_angle
            r_arm.keyframe_insert(
                data_path = "rotation_quaternion",
                frame = end_frame
            )


        #Head
        head = self.ref_obj.children[0].pose.bones[3]
        initial = list(head.rotation_quaternion)

        head_back = [1, -0.1, 0, 0.1]
        head_back_left = [1, -0.1, 0.1, 0.1]
        head_back_right = [1, -0.1, -0.1, 0.1]

        head.keyframe_insert(
            data_path = "rotation_quaternion",
            frame = start_frame
        )
        head.rotation_quaternion = head_back
        head.keyframe_insert(
            data_path = "rotation_quaternion",
            frame = start_frame + attack_frames
        )


        #Shakes
        still_time = end_frame - start_frame - attack_frames - decay_frames
        if still_time >= 5 * OBJECT_APPEARANCE_TIME:
            still_time = still_time - 2 * OBJECT_APPEARANCE_TIME

            head.keyframe_insert(
                data_path = "rotation_quaternion",
                frame = start_frame + attack_frames + still_time / 3
            )
            head.rotation_quaternion = head_back_left
            head.keyframe_insert(
                data_path = "rotation_quaternion",
                frame = start_frame + attack_frames + still_time / 3 + OBJECT_APPEARANCE_TIME
            )

            head.keyframe_insert(
                data_path = "rotation_quaternion",
                frame = start_frame + attack_frames + 2 * still_time / 3 + 1 * OBJECT_APPEARANCE_TIME
            )
            head.rotation_quaternion = head_back_right
            head.keyframe_insert(
                data_path = "rotation_quaternion",
                frame = start_frame + attack_frames + 2 * still_time / 3 + 2 * OBJECT_APPEARANCE_TIME
            )


        head.keyframe_insert(
            data_path = "rotation_quaternion",
            frame = end_frame - decay_frames
        )
        head.rotation_quaternion = initial
        head.keyframe_insert(
            data_path = "rotation_quaternion",
            frame = end_frame
        )

        #Eyes
        eyes = [
            self.ref_obj.children[0].children[-2],
            self.ref_obj.children[0].children[-3],
        ]
        for eye in eyes:
                key = eye.data.shape_keys.key_blocks['Key 1']
                key.keyframe_insert(data_path = 'value', frame = start_frame)
                key.value = 1
                key.keyframe_insert(data_path = 'value', frame = start_frame + attack_frames)
                if end_frame != None:
                    key.keyframe_insert(data_path = 'value', frame = end_frame - decay_frames)
                    key.value = 0
                    key.keyframe_insert(data_path = 'value', frame = end_frame)

        #Mouth
        self.eat_animation(
            start_frame = start_frame,
            end_frame = end_frame,
            attack_frames = attack_frames,
            decay_frames = decay_frames
        )

    def hello(
        self,
        start_time = None,
        end_time = None,
        attack = None,
        decay = None
    ):
        if start_time == None:
            raise Warning('Need start time for blob hello')

        start_frame = start_time * FRAME_RATE
        end_frame = None
        if end_time != None:
            end_frame = end_time * FRAME_RATE

        if attack == None:
            if end_time == None:
                attack = OBJECT_APPEARANCE_TIME / FRAME_RATE / 2
            elif end_time - start_time > 2:
                attack = OBJECT_APPEARANCE_TIME / FRAME_RATE / 2
            else:
                attack = (end_time - start_time) / 4
        attack_frames = attack * FRAME_RATE

        if decay == None:
            if end_time == None:
                decay = OBJECT_APPEARANCE_TIME / FRAME_RATE / 2
            elif end_time - start_time > 2:
                decay = OBJECT_APPEARANCE_TIME / FRAME_RATE / 2
            else:
                decay = (end_time - start_time) / 4
        decay_frames = decay * FRAME_RATE


        r_arm_up_z = -1.5
        r_arm_down_z = 1
        r_arm_out_y = -5

        #These labels are from the point of view of the blob, which is opposite
        #from how they're labeled in the template .blend file. Huzzah.
        r_arm = None
        for child in self.ref_obj.children:
            if 'boerd_blob' in child.name:
                r_arm = child.pose.bones[2]


        r_arm.keyframe_insert(
            data_path = "rotation_quaternion",
            frame = start_frame
        )

        #Right wave
        initial_angle = list(r_arm.rotation_quaternion)

        wave_cycle_length_min = 12
        waving_duration = end_frame - start_frame - attack_frames - decay_frames
        num_wave_cycles = math.floor(waving_duration / wave_cycle_length_min)
        wave_cycle_length = waving_duration / num_wave_cycles

        for i in range(num_wave_cycles):
            r_arm.rotation_quaternion = [
                initial_angle[0],
                initial_angle[1],
                r_arm_out_y,
                r_arm_down_z
            ]
            r_arm.keyframe_insert(
                data_path = "rotation_quaternion",
                frame = start_frame + attack_frames + wave_cycle_length * i
            )
            r_arm.rotation_quaternion = [
                initial_angle[0],
                initial_angle[1],
                r_arm_out_y,
                r_arm_up_z
            ]
            r_arm.keyframe_insert(
                data_path = "rotation_quaternion",
                frame = start_frame + attack_frames + wave_cycle_length * (i + 0.5)
            )

        #And back
        if end_frame != None:
            r_arm.rotation_quaternion = [
                initial_angle[0],
                initial_angle[1],
                r_arm_out_y,
                r_arm_down_z
            ]
            r_arm.keyframe_insert(
                data_path = "rotation_quaternion",
                frame = end_frame - decay_frames
            )
            r_arm.rotation_quaternion = initial_angle
            r_arm.keyframe_insert(
                data_path = "rotation_quaternion",
                frame = end_frame
            )


        #Head
        head = self.ref_obj.children[0].pose.bones[3]
        initial = list(head.rotation_quaternion)

        head_tilt = [1, -0.1, 0, -0.1]

        head.keyframe_insert(
            data_path = "rotation_quaternion",
            frame = start_frame
        )
        head.rotation_quaternion = head_tilt
        head.keyframe_insert(
            data_path = "rotation_quaternion",
            frame = start_frame + attack_frames
        )

        head.keyframe_insert(
            data_path = "rotation_quaternion",
            frame = end_frame - decay_frames
        )
        head.rotation_quaternion = initial
        head.keyframe_insert(
            data_path = "rotation_quaternion",
            frame = end_frame
        )

    def wince(
        self,
        start_time = None,
        end_time = None,
        attack = None,
        decay = None
    ):
        if start_time == None:
            raise Warning('Need start time for evil pose')

        start_frame = start_time * FRAME_RATE
        end_frame = None
        if end_time != None:
            end_frame = end_time * FRAME_RATE

        default_attack = OBJECT_APPEARANCE_TIME / 2

        if attack == None:
            if end_time == None:
                attack = default_attack / FRAME_RATE
            elif end_time - start_time > 2:
                attack = default_attack / FRAME_RATE
            else:
                attack = (end_time - start_time) / 4
        attack_frames = attack * FRAME_RATE

        if decay == None:
            if end_time == None:
                decay = default_attack / FRAME_RATE
            elif end_time - start_time > 2:
                decay = default_attack / FRAME_RATE
            else:
                decay = (end_time - start_time) / 4
        decay_frames = decay * FRAME_RATE

        #Head
        head = self.ref_obj.children[0].pose.bones[3]
        initial = list(head.rotation_quaternion)

        head_down = [1, 0.2, 0.1, -0.5]
        head_down_left = [1, 0, 0.4, -0.5]
        head_down_right = [1, 0, -0.1, -0.5]

        head.keyframe_insert(
            data_path = "rotation_quaternion",
            frame = start_frame
        )
        head.rotation_quaternion = head_down
        head.keyframe_insert(
            data_path = "rotation_quaternion",
            frame = start_frame + attack_frames
        )


        #Shakes
        still_time = end_frame - start_frame - attack_frames - decay_frames
        num_shakes = math.floor(2 * still_time / OBJECT_APPEARANCE_TIME)
        for i in range(num_shakes):
            '''head.keyframe_insert(
                data_path = "rotation_quaternion",
                frame = start_frame + attack_frames + still_time / 3
            )'''
            if i % 2 == 0:
                head.rotation_quaternion = head_down_left
            else:
                head.rotation_quaternion = head_down_right
            head.keyframe_insert(
                data_path = "rotation_quaternion",
                frame = start_frame + attack_frames + (1 + i) * OBJECT_APPEARANCE_TIME / 2
            )

            '''head.keyframe_insert(
                data_path = "rotation_quaternion",
                frame = start_frame + attack_frames + 2 * still_time / 3 + 1 * OBJECT_APPEARANCE_TIME
            )
            head.rotation_quaternion = head_back_right
            head.keyframe_insert(
                data_path = "rotation_quaternion",
                frame = start_frame + attack_frames + 2 * still_time / 3 + 2 * OBJECT_APPEARANCE_TIME
            )'''



        head.keyframe_insert(
            data_path = "rotation_quaternion",
            frame = end_frame - decay_frames
        )
        head.rotation_quaternion = initial
        head.keyframe_insert(
            data_path = "rotation_quaternion",
            frame = end_frame
        )

        #Eyes
        eyes = [
            self.ref_obj.children[0].children[-2],
            self.ref_obj.children[0].children[-3],
        ]
        for eye in eyes:
            init_eye_scale = list(eye.scale)
            init_eye_rot = list(eye.rotation_euler)

            eye.keyframe_insert(data_path = 'scale', frame = start_frame)
            eye.scale = [1, 0.3, 0.3]
            eye.keyframe_insert(data_path = 'scale', frame = start_frame + attack_frames)
            eye.keyframe_insert(data_path = 'scale', frame = end_frame - decay_frames)
            eye.scale = init_eye_scale
            eye.keyframe_insert(data_path = 'scale', frame = end_frame)

            eye.keyframe_insert(data_path = 'rotation_euler', frame = start_frame)
            if eye == eyes[1]:
                eye.rotation_euler = [0, -20 * math.pi / 180, 0]
            else:
                eye.rotation_euler = [0, 20 * math.pi / 180, 0]
            eye.keyframe_insert(data_path = 'rotation_euler', frame = start_frame + attack_frames)
            eye.keyframe_insert(data_path = 'rotation_euler', frame = end_frame - decay_frames)
            eye.rotation_euler = init_eye_rot
            eye.keyframe_insert(data_path = 'rotation_euler', frame = end_frame)

        '''leye = self.ref_obj.children[0].pose.bones[5]
        reye = self.ref_obj.children[0].pose.bones[6]

        for eye_bone in [leye, reye]:
            eye_bone.keyframe_insert(data_path = 'rotation_quaternion', frame = start_frame)
            if eye_bone == leye:
                eye.rotation_quaternion = [1, 0, 0.1, 0]
            else:
                eye.rotation_quaternion = [1, 0, -0.1, 0]
            eye_bone.keyframe_insert(data_path = 'rotation_quaternion', frame = start_frame + attack_frames)
            eye_bone.keyframe_insert(data_path = 'rotation_quaternion', frame = end_frame - decay_frames)
            eye_bone.rotation_quaternion = init_eye_rot
            eye_bone.keyframe_insert(data_path = 'rotation_quaternion', frame = end_frame)'''


    def hold_object(
        self,
        start_time = None,
        end_time = None,
        attack = None,
        decay = None
    ):
        if start_time == None:
            raise Warning('Need start time for evil pose')

        start_frame = start_time * FRAME_RATE
        end_frame = None
        if end_time != None:
            end_frame = end_time * FRAME_RATE

        if attack == None:
            if end_time == None:
                attack = OBJECT_APPEARANCE_TIME / FRAME_RATE
            elif end_time - start_time > 2:
                attack = OBJECT_APPEARANCE_TIME / FRAME_RATE
            else:
                attack = (end_time - start_time) / 4
        attack_frames = attack * FRAME_RATE

        if decay == None:
            if end_time == None:
                decay = OBJECT_APPEARANCE_TIME / FRAME_RATE
            elif end_time - start_time > 2:
                decay = OBJECT_APPEARANCE_TIME / FRAME_RATE
            else:
                decay = (end_time - start_time) / 4
        decay_frames = decay * FRAME_RATE


        #Blob's left arm up = [1, -2.5, -8.1, -1.5]
        #Blob's right arm up = [1, 0.4, -36.6, -9]

        #These labels are from the point of view of the blob, which is opposite
        #from how they're labeled in the template .blend file. Huzzah.
        l_arm = None
        r_arm = None
        for child in self.ref_obj.children:
            if 'boerd_blob' in child.name:
                l_arm = child.pose.bones[1]
                r_arm = child.pose.bones[2]

        #Left arm up
        l_arm.keyframe_insert(
            data_path = "rotation_quaternion",
            frame = start_frame
        )
        initial_angle = list(l_arm.rotation_quaternion)
        l_arm.rotation_quaternion = [1, 0.3, -0.2, -0.9]
        l_arm.keyframe_insert(
            data_path = "rotation_quaternion",
            frame = start_frame + attack_frames
        )

        #Shakes?

        #And back
        if end_frame != None:
            l_arm.keyframe_insert(
                data_path = "rotation_quaternion",
                frame = end_frame - decay_frames
            )
            l_arm.rotation_quaternion = initial_angle
            l_arm.keyframe_insert(
                data_path = "rotation_quaternion",
                frame = end_frame
            )

        #Right arm up
        r_arm.keyframe_insert(
            data_path = "rotation_quaternion",
            frame = start_frame
        )
        initial_angle = list(r_arm.rotation_quaternion)
        r_arm.rotation_quaternion = [0.837, 0.235, 0.215, 0.445]
        r_arm.keyframe_insert(
            data_path = "rotation_quaternion",
            frame = start_frame + attack_frames
        )

        #And back
        if end_frame != None:
            r_arm.keyframe_insert(
                data_path = "rotation_quaternion",
                frame = end_frame - decay_frames
            )
            r_arm.rotation_quaternion = initial_angle
            r_arm.keyframe_insert(
                data_path = "rotation_quaternion",
                frame = end_frame
            )


    def eat_animation(
        self,
        start_frame = None,
        end_frame = None,
        attack_frames = None,
        decay_frames = None
    ):
        if start_frame == None:
            raise Warning('Need start frame for eat animation')

        if attack_frames == None:
            if end_frame == None:
                attack_frames = OBJECT_APPEARANCE_TIME
            else:
                attack_frames = (end_frame - start_frame) / 2

        if decay_frames == None:
            if end_frame == None:
                decay_frames = OBJECT_APPEARANCE_TIME
            else:
                decay_frames = (end_frame - start_frame) / 2


        #I parented the mouth in a pretty ridiculous way, but it works.
        for child in self.ref_obj.children[0].children:
            if 'Mouth' in child.name:
                mouth = child
                break

        o_loc = list(mouth.location)
        o_rot = list(mouth.rotation_euler)
        o_scale = list(mouth.scale)

        mouth.keyframe_insert(data_path = 'location', frame = start_frame)
        mouth.keyframe_insert(data_path = 'rotation_euler', frame = start_frame)
        mouth.keyframe_insert(data_path = 'scale', frame = start_frame)

        mouth.location = [-0.04, 0.36, 0.3760]
        mouth.rotation_euler = [
            -8.91 * math.pi / 180,
            -0.003 * math.pi / 180,
            -3.41 * math.pi / 180,
        ]
        mouth.scale = [
            0.853,
            2.34,
            0.889
        ]

        mouth.keyframe_insert(data_path = 'location', frame = start_frame + attack_frames)
        mouth.keyframe_insert(data_path = 'rotation_euler', frame = start_frame + attack_frames)
        mouth.keyframe_insert(data_path = 'scale', frame = start_frame + attack_frames)

        mouth.keyframe_insert(data_path = 'location', frame = end_frame - decay_frames)
        mouth.keyframe_insert(data_path = 'rotation_euler', frame = end_frame - decay_frames)
        mouth.keyframe_insert(data_path = 'scale', frame = end_frame - decay_frames)

        mouth.location = o_loc
        mouth.rotation_euler = o_rot
        mouth.scale = o_scale

        mouth.keyframe_insert(data_path = 'location', frame = end_frame)
        mouth.keyframe_insert(data_path = 'rotation_euler', frame = end_frame)
        mouth.keyframe_insert(data_path = 'scale', frame = end_frame)"""

    def de_explode(
        self,
        start_time = 0,
        duration = 1
    ):
        #Works on a group of objects with a series of parent-child relationships
        #Spreads the objects out, then pulls them together based on family tree
        #structure

        def find_longest_line(obj):
            l_so_far = 0
            for child in obj.children:
                length = 1 + find_longest_line(child)
                #Hax to make up for the delay at the Phosphorus atoms later on
                if child.scale[0] > 0.5:
                    length += 4
                if length > l_so_far:
                    l_so_far = length

            return l_so_far
        longest_line = find_longest_line(self.ref_obj)



        start_frame = start_time * FRAME_RATE
        duration_frames = duration * FRAME_RATE

        dur_per_child = duration_frames / longest_line

        seed = self.ref_obj
        de_explode_children(seed, start_frame, dur_per_child)

def de_explode_children(obj, start_frame, duration_frames):
    for child in obj.children:
        #location
        final_loc = deepcopy(child.location)
        #if delay == 0: #First parent
        spread_factor = 3
        child.location = [
            spread_factor * uniform(-1, 1),
            spread_factor * uniform(-1, 1),
            spread_factor * uniform(-1, 1)
        ]
        child.keyframe_insert(
            data_path = 'location',
            frame = start_frame
        )
        child.location = final_loc
        child.keyframe_insert(
            data_path = 'location',
            frame = start_frame + duration_frames * 6
        )

        final_scale = deepcopy(child.scale)
        child.scale = [0, 0, 0]
        child.keyframe_insert(
            data_path = 'scale',
            frame = start_frame
        )
        if 'Cylinder' in child.name:
            #Cylinders appear once surrounding atoms are in place.
            child.keyframe_insert(
                data_path = 'scale',
                #Start to appear once in place
                frame = start_frame + duration_frames * 12
            )
            child.scale = final_scale
            child.keyframe_insert(
                data_path = 'scale',
                frame = start_frame + duration_frames * 16
            )

        else:
            child.keyframe_insert(
                data_path = 'scale',
                #2 sec before arriving, the atom begins to appear
                frame = start_frame
            )
            child.scale = final_scale
            child.keyframe_insert(
                data_path = 'scale',
                #1 sec before arriving, the atom is full size
                frame = start_frame + duration_frames
            )

        #Extra delay on recursion at Phosphorus
        if child.scale[0] > 0.5:
            de_explode_children(
                child,
                start_frame + duration_frames * 5,
                duration_frames
            )
        else:
            de_explode_children(
                child,
                start_frame + duration_frames,
                duration_frames
            )

class MeshMorphBobject(Bobject):
    def __init__(self, *subbobjects, **kwargs):
        super().__init__(*subbobjects, **kwargs)
        self.series = self.get_from_kwargs('series', [])
        self.particle_controller = None

    def add_to_blender(self, **kwargs):
        super().add_to_blender(**kwargs)
        if 'appear_time' in kwargs:
            kwargs['appear_frame'] = kwargs['appear_time'] * FRAME_RATE
        self.series[0].add_to_blender(
            animate = False,
            appear_frame = kwargs['appear_frame']
        )

    def add_subbobject_to_series(self, subbobject):
        for child in self.ref_obj.children:
            is_from_bobject = False
            for thing in self.series:
                if thing.ref_obj == child:
                    is_from_bobject = True
            if is_from_bobject == False:
                raise Warning('This bobject already has children not in the series.')
        if not isinstance(subbobject, Bobject):
            raise Warning('Subbobjects in series should be bobjects, else Justin gets confused.')

        self.series.append(subbobject)
        subbobject.ref_obj.parent = self.ref_obj
        subbobject.superbobject = self

    def morph_bobject(
        self,
        initial_index,
        final_index,
        start_time = None,
        end_time = None,
        start_frame = None,
        end_frame = None,
        dissolve_time = 0
    ):
        if start_time != None:
            if start_frame != None:
                raise Warning("You defined both start frame and start time. " +\
                              "Just do one, ya dick.")
            start_frame = int(start_time * FRAME_RATE)
        if end_time != None:
            if end_frame != None:
                raise Warning("You defined both end frame and end time. " +\
                              "Just do one, ya dick.")
            end_frame = int(end_time * FRAME_RATE)

        if start_frame == None or end_frame == None:
            raise Warning("Need to define start/end frame/time to morph bobject")

        self.series[initial_index].disappear(
            disappear_frame = start_frame + 1,
            animate = False
        )
        self.series[final_index].add_to_blender(
            appear_frame = end_frame,
            animate = False
        )

        initial_meshes = []
        for child in self.series[initial_index].ref_obj.children:
            if child.type == 'MESH':
                initial_meshes.append(child)
            append_descendants(child, initial_meshes, type_req = 'MESH')
        final_meshes = []
        for child in self.series[final_index].ref_obj.children:
            if child.type == 'MESH':
                final_meshes.append(child)
            append_descendants(child, final_meshes, type_req = 'MESH')


        if RENDER_QUALITY == 'medium' or RENDER_QUALITY == "high":
            if self.particle_controller == None:
                controller_bobj = import_object('icosphere', 'primitives')
                controller_ref = controller_bobj.ref_obj
                controller_ref.name = 'morph_helpers'
                controller_ref.location = (0, 1000, 0) #This should never be seen
                controller_ref.parent = self.ref_obj
                bpy.context.scene.objects.link(controller_ref)
                link_descendants(controller_ref)
                controller = controller_ref.children[0]
                controller.name = "particle_controller"
                self.particle_controller = controller

            #TODO: Change when looping through objects to morph
            for first in initial_meshes:
                for last in final_meshes:
                    self.morph_mesh_to_mesh(first, last, start_frame, end_frame, dissolve_time = dissolve_time)

        if RENDER_QUALITY == 'high':
            print('Bobject morphed')

    def morph_mesh_to_mesh(self, first, last, start_frame, end_frame, dissolve_time = 0):
        self.add_morph_particles(first, start_frame, end_frame)
        self.add_morph_particles(last, end_frame - 1, end_frame)
        #Above is a way of making the particles live only at the end frame
        #which allows particles to aim for where the target mesh will be.
        self.key_particles(first, last, start_frame, end_frame, dissolve_time = dissolve_time)

    def add_morph_particles(self, obj, start_frame, end_frame, dissolve_time = 0):
        bpy.context.scene.frame_set(start_frame)
        bpy.context.scene.update()
        has_particles = False
        #Could really just search for particle systems directly. No need to
        #look in modifiers.
        for mod in obj.modifiers:
            if mod.type == 'PARTICLE_SYSTEM':
                has_particles = True
                break

        #Just one particle system per mesh, except for on the controller
        if has_particles == False or obj == self.particle_controller:
            mod = obj.modifiers.new("ParticleSystem", type = 'PARTICLE_SYSTEM')
            psys = mod.particle_system
            psys.seed = random() * 10000
            stngs = psys.settings

            stngs.count = PARTICLES_PER_MESH
            stngs.frame_end = start_frame + dissolve_time #+ self.appear_frame
            stngs.frame_start = start_frame #+ self.appear_frame
            stngs.lifetime = end_frame - start_frame
            stngs.emit_from = 'FACE'
            stngs.distribution = 'RAND'

            stngs.physics_type = "NO"
            stngs.render_type = 'NONE'


            stngs.normal_factor = 0
            stngs.tangent_factor = 0
            stngs.effector_weights.gravity = 0

    '''def add_turbulent_particles(self, obj, start_frame, end_frame):
        mod = obj.modifiers.new("ParticleSystem", type = 'PARTICLE_SYSTEM')
        psys = mod.particle_system
        psys.seed = random() * 10000
        stngs = psys.settings

        stngs.count = PARTICLES_PER_MESH
        stngs.frame_start = start_frame #+ self.appear_frame
        stngs.frame_end = start_frame #+ self.appear_frame
        stngs.lifetime = end_frame - start_frame
        stngs.emit_from = 'FACE'
        stngs.distribution = 'RAND'

        stngs.physics_type = 'NEWTON'
        stngs.render_type = 'NONE'

        stngs.normal_factor = 0
        stngs.tangent_factor = 0
        stngs.effector_weights.gravity = 0

        bpy.ops.object.effector_add(type = 'TURBULENCE', location = obj.location)
        turb = bpy.context.object
        turb.parent = self.particle_controller.parent
        turb.field.strength = 1'''

    def key_particles(self, start, end, start_frame, end_frame, backward = False, dissolve_time = 0):
        #Once to shoot particles out of the original object
        self.add_morph_particles(self.particle_controller, start_frame, end_frame, dissolve_time = dissolve_time)
        psys = self.particle_controller.modifiers[-1].particle_system
        stngs = psys.settings

        #Set up particle keys
        stngs.physics_type = "KEYED"
        psys.use_keyed_timing = True

        #Set up object for particles to duplicate (for color)
        stngs.render_type = 'OBJECT'
        bpy.ops.mesh.primitive_ico_sphere_add(location = (1000, 0, 0))
        dup = bpy.context.object
        #dup.parent = start
        dup.parent = self.particle_controller.parent
        dup.data.materials.append(start.active_material)
        stngs.dupli_object = dup

        #stngs.size_random = 1
        stngs.particle_size = 0
        stngs.keyframe_insert(data_path = 'particle_size', frame = start_frame)
        stngs.particle_size = MORPH_PARTICLE_SIZE
        stngs.keyframe_insert(data_path = 'particle_size', frame = start_frame + PARTICLE_APPEARANCE_TIME)
        stngs.particle_size = 0
        stngs.keyframe_insert(data_path = 'particle_size', frame = end_frame)

        bpy.ops.particle.new_target({'particle_system': psys})
        targ = psys.targets[-1]
        targ.object = start
        targ.duration = PARTICLE_APPEARANCE_TIME


        '''self.add_turbulent_particles(start, start_frame, end_frame)
        bpy.ops.particle.new_target({'particle_system': psys})
        targ = psys.targets[-1]
        targ.object = start
        targ.system = 2
        targ.time = (end_frame - start_frame) / 4'''

        bpy.ops.particle.new_target({'particle_system': psys})
        targ = psys.targets[-1]
        targ.object = end
        targ.time = end_frame - start_frame - dissolve_time


        #And again to suck particles into new object
        #Might make sense to reorg this
        self.add_morph_particles(self.particle_controller, start_frame, end_frame, dissolve_time = dissolve_time)
        psys = self.particle_controller.modifiers[-1].particle_system
        stngs = psys.settings

        #Set up particle keys
        stngs.physics_type = "KEYED"
        psys.use_keyed_timing = True

        #Set up object for particles to duplicate (for color)
        stngs.render_type = 'OBJECT'
        bpy.ops.mesh.primitive_ico_sphere_add(location = (0, 1000, 0))
        dup = bpy.context.object
        dup.parent = self.particle_controller.parent
        dup.data.materials.append(end.active_material)
        stngs.dupli_object = dup

        bpy.ops.particle.new_target({'particle_system': psys})
        targ = psys.targets[-1]
        targ.object = start
        targ.duration = PARTICLE_APPEARANCE_TIME

        '''self.add_turbulent_particles(start, start_frame, end_frame)
        bpy.ops.particle.new_target({'particle_system': psys})
        targ = psys.targets[-1]
        targ.object = start
        targ.system = 2
        targ.time = (end_frame - start_frame) / 4'''

        bpy.ops.particle.new_target({'particle_system': psys})
        targ = psys.targets[-1]
        targ.object = end
        targ.time = end_frame - start_frame  - dissolve_time - PARTICLE_APPEARANCE_TIME
        targ.duration = PARTICLE_APPEARANCE_TIME

        #stngs.size_random = 1
        stngs.particle_size = 0
        stngs.keyframe_insert(data_path = 'particle_size', frame = start_frame)
        stngs.particle_size = MORPH_PARTICLE_SIZE
        stngs.keyframe_insert(data_path = 'particle_size', frame = end_frame - PARTICLE_APPEARANCE_TIME)
        stngs.particle_size = 0
        stngs.keyframe_insert(data_path = 'particle_size', frame = end_frame)

class RainBobject(Bobject):
    """docstring for RainBobject.
    This is really just made for one instance. If I do more rain, I'll need to
    make it more customizable.
    """
    def __init__(self, start_raining = 0, stop_raining = 0, **kwargs):
        super().__init__(**kwargs)

        self.start_raining = start_raining + OBJECT_APPEARANCE_TIME
        #The above addition of OBJECT_APPEARANCE_TIME is purposely there in
        #addition to any buffer passed into start_raining to make sure the
        #emitter is in place before it actually starts raining. Probably a more
        #robust way of doing it, but this stopped rogue raindrops for now.
        self.stop_raining = stop_raining

        self.make_it_rain()

    def add_to_blender(self, **kwargs):
        super().add_to_blender(**kwargs)

        #For collision objects, replace the unhide keyframe with another hide
        #keyframe so they are never actually shown. They're just for physics.
        #Doing it this way so the extra thickness on characters doesn't appear.
        #More keyframes than necessary.
        appear_frame = kwargs['appear_frame']
        for obj in self.collision_objects:
            obj.hide = True
            obj.hide_render = True
            obj.keyframe_insert(data_path="hide", frame = appear_frame)
            obj.keyframe_insert(data_path="hide_render", frame = appear_frame)

    def disappear(self, disappear_frame = None, animate = False):
        #This override allows drops to fall away after the collision objects
        #go away, rather than just disappearing.
        if animate == True:
            raise Warning("RainBobjects are currently designed to not be animated")

        #Make emitter and raindrop last longer
        if disappear_frame != None:
            objs = [x for x in self.subbobjects if x.name == 'emitter']
            for obj in objs:#[self.emitter, self.raindrop]:
                obj.disappear(disappear_frame = disappear_frame + 100, animate = False)
                obj.ref_obj.parent = None
                obj.superbobject = None
                self.subbobjects.remove(obj)

            #Make drops fall through hidden collision_objects, which seem to
            #still take part in physics.
            for obj in self.collision_objects:
                col = obj.collision
                col.keyframe_insert(data_path = 'permeability', frame = disappear_frame - 1)
                col.permeability = 1
                col.keyframe_insert(data_path = 'permeability', frame = disappear_frame)

        super().disappear(disappear_frame = disappear_frame, animate = animate)

    def make_it_rain(self):
        emitter_container = import_object('xzplane', 'primitives', name = 'emitter')
        #emitter_container.ref_obj.parent = self.ref_obj
        self.add_subbobject(emitter_container)
        emitter_container.ref_obj.children[0].location = (0, 12, 0)
        emitter_container.ref_obj.children[0].scale = (16, 16, 16)

        emitter = emitter_container.ref_obj.children[0]
        #A bit hacky, but this method links the emitter object to the scene,
        #changes settings, and then unlinks the emitter object. The normal flow
        #with bobjects is to set everything up, then link the object(s) to the
        #scene, but this particular emitter uses fluid physics for the particle
        #system, which needs to be linked to the scene to update settings.
        bpy.context.scene.objects.link(emitter)
        emitter.scale[2] = 1/160
        #self.emitter = emitter #Used to override add_to_blender()

        mod = emitter.modifiers.new("ParticleSystem", type = 'PARTICLE_SYSTEM')
        psys = mod.particle_system
        psys.seed = random() * 10000
        stngs = psys.settings

        #Could improve this by making rain density a constant and setting count
        #based on that density and that duration
        if RENDER_QUALITY == 'high':
            stngs.count = 30000
        else:
            stngs.count = 1000
        stngs.lifetime = self.stop_raining - self.start_raining
        #Stop emitting drops in time to have them all run out by the end frome
        fall_time = 55 #probably make this an arg when generalizing
        stngs.frame_end = self.stop_raining - fall_time #+ self.appear_frame
        stngs.frame_start = self.start_raining
        stngs.emit_from = 'FACE'
        stngs.distribution = 'RAND'
        stngs.normal_factor = 0
        stngs.tangent_factor = 0
        stngs.factor_random = 0.5
        stngs.brownian_factor = 0.1

        stngs.physics_type = 'FLUID'
        bpy.data.scenes[0].update()
        stngs.fluid.solver = 'CLASSICAL'
        stngs.fluid.fluid_radius = 0.2
        stngs.render_type = 'OBJECT'
        stngs.particle_size = 0.05
        stngs.size_random = 0.5
        dup_bobj = import_object('goodicosphere', 'primitives', location = (1000, 0 , 0), name = 'raindrop model')
        dup_bobj.ref_obj.parent = self.ref_obj
        dup = dup_bobj.ref_obj.children[0]
        apply_material(dup, 'clear')
        stngs.dupli_object = dup
        self.raindrop = dup

        #See comment above about why linking and unlinking happens here.
        bpy.context.scene.objects.unlink(emitter)

        obj = bpy.context.object

    def add_collision_objects(self, collision_bobjects, text = False, frame = 0):
        objects = []
        new_objects = []
        if text == True:
            for bobj in collision_bobjects:
                #intentionally don't append the object itself, (only descendants)
                #since for text, it's a hidden reference object
                #append_descendants(obj, objects)
                objects.append(bobj.ref_obj.children[0])

            #objects = [x for x in objects if x.type == 'CURVE']
            #The above line is a bit of a hack to make this work now that chars
            #are bobjects. Seems okay.

            scn = bpy.context.scene
            scn.frame_set(frame)

            for obj in objects: #Skip the reference character if text
                obj.data.extrude = 0.1
                new_mesh = obj.to_mesh(scn, True, 'PREVIEW')
                new_obj = bpy.data.objects.new('collision', new_mesh)
                obj.data.extrude = 0
                #new_obj.parent = self.ref_obj
                new_bobj = Bobject(objects = [new_obj])
                self.subbobjects.append(new_bobj)
                #This intentionally avoids the method add_subbobject() because
                #the new bobject's parent should be the same as the original
                #bobject, allowing animations to affect the collision objects.
                new_bobj.ref_obj.parent = obj.parent.parent
                new_bobj.ref_obj.matrix_local = obj.parent.matrix_local

                new_obj.modifiers.new("CollisionSettings", type = 'COLLISION')
                new_obj.collision.damping_factor = 0.8
                new_obj.collision.damping_random = 0.5
                new_objects.append(new_obj)

        else:
            raise Warning("Collision objects not implemented for non-text")
        self.collision_objects = new_objects
        bpy.data.scenes[0].update()
