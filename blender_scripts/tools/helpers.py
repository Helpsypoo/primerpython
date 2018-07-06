import os
import sys
import imp
import bpy
import math
from random import random, uniform
from copy import deepcopy
import time
import datetime

import constants
imp.reload(constants)
from constants import *

#sys.path.append('C:\\Users\\justi\\Documents\\CodeProjects\\Primer\\blender_scripts')
import bobject
import winsound

'''
Blender object functions

Different from the Bobject class, which is actually just a python container for
true Blender objects. Bobject is the class that uses these most, though.
'''

def apply_material(obj, mat, recursive = False, type_req = None):
    if obj.type not in ['EMPTY', 'ARMATURE']:
        if type_req == None or obj.type == type_req:
            obj.active_material = bpy.data.materials[mat]

    if recursive:
        for child in obj.children:
            apply_material(child, mat, recursive = recursive, type_req = type_req)

def define_materials():
    clear = bpy.data.materials.new(name = "clear")
    clear.use_nodes = True
    nodes = clear.node_tree.nodes
    nodes.remove(nodes[1]) #This is the diffuse shader by default
    nodes.new(type = 'ShaderNodeBsdfRefraction')
    nodes[1].inputs[0].default_value = (0.8, 1, 1, 1)
    #Hook up the refraction shader to the output (nodes[0])
    clear.node_tree.links.new(nodes[1].outputs[0], nodes[0].inputs[0])

    make_basic_material(rgb = deepcopy(COLORS[0]), name = 'color1')
    make_basic_material(rgb = deepcopy(COLORS[1]), name = 'color2')
    make_basic_material(rgb = deepcopy(COLORS[2]), name = 'color3')
    make_basic_material(rgb = deepcopy(COLORS[3]), name = 'color4')
    make_basic_material(rgb = deepcopy(COLORS[4]), name = 'color5')
    make_basic_material(rgb = deepcopy(COLORS[5]), name = 'color6')
    make_basic_material(rgb = deepcopy(COLORS[6]), name = 'color7')

    make_creature_material(rgb = deepcopy(COLORS[0]), name = 'creature_color1')
    make_creature_material(rgb = deepcopy(COLORS[1]), name = 'creature_color2')
    make_creature_material(rgb = deepcopy(COLORS[2]), name = 'creature_color3')
    make_creature_material(rgb = deepcopy(COLORS[3]), name = 'creature_color4')
    make_creature_material(rgb = deepcopy(COLORS[4]), name = 'creature_color5')
    make_creature_material(rgb = deepcopy(COLORS[5]), name = 'creature_color6')
    make_creature_material(rgb = deepcopy(COLORS[6]), name = 'creature_color7')

    make_translucent_material(rgb = deepcopy(COLORS[0]), name = 'trans_color1')
    make_translucent_material(rgb = deepcopy(COLORS[1]), name = 'trans_color2')
    make_translucent_material(rgb = deepcopy(COLORS[2]), name = 'trans_color3')
    make_translucent_material(rgb = deepcopy(COLORS[3]), name = 'trans_color4')
    make_translucent_material(rgb = deepcopy(COLORS[4]), name = 'trans_color5')
    make_translucent_material(rgb = deepcopy(COLORS[5]), name = 'trans_color6')
    make_translucent_material(rgb = deepcopy(COLORS[6]), name = 'trans_color7')

def make_basic_material(rgb = None, name = None):
    if rgb == None or name == None:
        raise Warning('Need rgb and name to make basic material')
    for i in range(3):
        #Range exactly 3 so a fourth component (alpha) isn't affected
        rgb[i] /= 255

    color = bpy.data.materials.new(name = name)
    color.use_nodes = True
    nodes = color.node_tree.nodes
    #nodes[1].inputs[1].default_value = 1 #Roughness. 1 means not shiny.
    nodes[1].inputs[0].default_value = rgb

    rgb = rgb[:3] #Cuts to 3 components so it works for diffuse_color
                  #which doesn't take alpha
    color.diffuse_color = rgb

def make_creature_material(rgb = None, name = None):
    if rgb == None or name == None:
        raise Warning('Need rgb and name to make creature material')
    for i in range(3):
        #Range exactly 3 so a fourth component (alpha) isn't affected
        rgb[i] /= 255

    color = bpy.data.materials.new(name = name)
    color.use_nodes = True
    nodes = color.node_tree.nodes
    #nodes[1].inputs[1].default_value = 1 #Roughness. 1 means not shiny.
    nodes.new(type = 'ShaderNodeBsdfPrincipled')
    nodes[2].inputs[0].default_value = rgb
    color.node_tree.links.new(nodes[2].outputs[0], nodes[0].inputs[0])

    rgb = rgb[:3] #Cuts to 3 components so it works for diffuse_color
                  #which doesn't take alpha
    color.diffuse_color = rgb

def make_translucent_material(rgb = None, name = None):
    if rgb == None or name == None:
        raise Warning('Need rgb and name to make translucent material')
    for i in range(3):
        #Range exactly 3 so a fourth component (alpha) isn't affected
        rgb[i] /= 255

    strength = 4 #Arbitrary, could make this a constant

    color = bpy.data.materials.new(name = name)
    color.use_nodes = True
    nodes = color.node_tree.nodes
    color.node_tree.links.remove(nodes[0].inputs[0].links[0])
    nodes.new(type = 'ShaderNodeAddShader') #index 2
    color.node_tree.links.new(nodes[2].outputs[0], nodes[0].inputs[1])
    nodes.new(type = 'ShaderNodeAddShader') #index 3
    color.node_tree.links.new(nodes[3].outputs[0], nodes[2].inputs[1])
    nodes.new(type = 'ShaderNodeEmission') #index 4
    nodes[4].inputs[0].default_value = rgb
    nodes[4].inputs[1].default_value = strength
    color.node_tree.links.new(nodes[4].outputs[0], nodes[2].inputs[0])
    nodes.new(type = 'ShaderNodeVolumeScatter') #index 5
    nodes[5].inputs[0].default_value = rgb
    nodes[5].inputs[1].default_value = strength
    color.node_tree.links.new(nodes[5].outputs[0], nodes[3].inputs[0])
    nodes.new(type = 'ShaderNodeVolumeAbsorption') #index 6
    nodes[6].inputs[0].default_value = rgb
    nodes[6].inputs[1].default_value = strength
    color.node_tree.links.new(nodes[6].outputs[0], nodes[3].inputs[1])

    rgb = rgb[:3] #Cuts to 3 components so it works for diffuse_color
                  #which doesn't take alpha
    color.diffuse_color = rgb

def join_by_material(obj_list):
    #Usful when morphing meshes.
    #It reduces the number of particle systems needed.
    for mat in bpy.data.materials:
        for shape in obj_list:
            shape.select = False
            #print(mat)
            if mat in list(shape.data.materials):
                shape.select = True
                bpy.context.scene.objects.active = shape
        bpy.ops.object.join()

def link_descendants(obj):
    #If children exist, link those too
    #Will break if imported children were linked in add_to_blender
    #(if their object name in blender is the same as the filename)
    obj_names = [x.name for x in bpy.data.objects]
    for child in obj.children:
        if child.name not in bpy.context.scene.objects:
            bpy.context.scene.objects.link(child)
        link_descendants(child)

def append_descendants(obj, lst, type_req = None):
    for child in obj.children:
        if type_req == None:
            lst.append(child)
        else:
            if child.type == type_req:
                lst.append(child)
        append_descendants(child, lst)

def hide_self_and_descendants(obj, hide = True, keyframes = False, frame = None):
    #If hide == True, this hides everything.
    #If hide == False, this un-hides everything.

    if keyframes == True:
        if frame == None:
            raise Exception('in hide_self_and_descendants(), frame must be '
                            'specified if keyframes == True')
        #if obj.hide == True and hide == True:
        #    print("Calling hide_self_and_descendants on object that's "
        #                  "already hidden")

        #obj.hide = not hide
        #obj.hide_render = not hide
        #obj.keyframe_insert(data_path = 'hide', frame = frame - 1)
        #obj.keyframe_insert(data_path = 'hide_render', frame = frame - 1)
        obj.hide = hide
        obj.hide_render = hide
        obj.keyframe_insert(data_path = 'hide', frame = frame)
        obj.keyframe_insert(data_path = 'hide_render', frame = frame)
    else:
        obj.hide = hide
        obj.hide_render = hide
    for child in obj.children:
        hide_self_and_descendants(child, hide = hide, keyframes = keyframes, frame = frame)

'''
Vector operations on lists/tuples
'''

def add_lists_by_element(list1, list2, subtract = False):
    if len(list1) != len(list2):
        raise Warning("The lists aren't the same length")
    list3 = list(deepcopy(list2))
    if subtract == True:
        for i in range(len(list3)):
            list3[i] *= -1
    return list(map(sum, zip(list1, list3)))

def mult_lists_by_element(vec1, vec2):
    vec3 = []
    for x1, x2, in zip(vec1, vec2):
        vec3.append(x1 * x2)

    return vec3

def scalar_mult_vec(vec, scalar):
    v = deepcopy(vec)
    for i in range(len(v)):
        v[i] *= scalar
    return v

def dot_product(vec1, vec2):
    product = 0
    for x1, x2, in zip(vec1, vec2):
        product += x1 * x2

    return product

def vec_len(vec):
    length = 0
    for x in vec:
        length += x * x
    length = math.sqrt(length)
    return length

def get_unit_vec(vec):
    v = []
    length = vec_len(vec)
    for i in range(len(vec)):
        v.append(vec[i] / length)
    return v

'''
Blender object imports
'''
def import_object(filename, *folders, **kwargs):
    #Needs filename and the name of the template object to be the same
    DIR = BLEND_DIR
    for folder in folders:
        DIR = os.path.join(DIR, folder)

    filepath = os.path.join(
        DIR,
        filename
    ) + '.blend'

    #Unsurprisingly, but for reasons not fully understood, this doesn't work
    #properly when the blender's open file is the one at the filepath.
    with bpy.data.libraries.load(filepath) as (data_from, data_to):
        data_to.objects = data_from.objects
        num = len([x for x in data_to.objects if filename in x])

    #Get most recent objects with the right kind of name
    #Matters when we want to import multiple objects from a .blend file
    #objs = [x for x in bpy.data.objects if filename == x.name]
    #obj_names = [x.name for x in objs]
    new_obj = None
    for object in bpy.data.objects:
        if object.name == filename:
            new_obj = object
    if new_obj == None:
        raise Warning('Did not find object with same name as file')

    #Make object and children names unique by adding a num in front
    #Blender already adds numbers to the end of names, but this allows more
    #than 1000 objects with the (otherwise) same name and groups metaballs
    #together.
    existing_names = [x.name for x in bpy.data.objects]
    count = 0
    prefix = str(count).zfill(4)
    name = prefix + new_obj.name
    while name in existing_names:
        count += 1
        prefix = str(count).zfill(4)
        name = prefix + new_obj.name
    new_obj.name = name
    #Give children a unique prefix to separate metaball groups
    #Would need to expand this if importing more complex files where children
    #have children
    for child in new_obj.children:
        child.name = new_obj.name + child.name

    if 'name' not in kwargs.keys():
        name = new_obj.name
        kwargs['name'] = name

    #If this is an svg from blend, make subbobjects out of children before
    #making the final bobject.
    '''if 'svg' in kwargs and kwargs['svg'] == True:
        #print('bananananan')
        subbobjs = []
        for child in new_obj.children:
            child_bobj = bobject.Bobject(objects = [child])
            subbobjs.append(child_bobj)
        new_bobject = bobject.Bobject(*subbobjs, **kwargs)
    else:'''
    new_bobject = bobject.Bobject(objects = [new_obj], **kwargs)



    #Blinks
    ref_obj = new_bobject.ref_obj
    if filename == 'boerd_blob' or filename == 'boerd_blob_squat':
        leye = ref_obj.children[0].pose.bones[5]
        reye = ref_obj.children[0].pose.bones[6]
        t = 0
        if 'cycle_length' not in kwargs:
            cycle_length = BLINK_CYCLE_LENGTH
        else:
            cycle_length = kwargs['cycle_length']
        while t < cycle_length:
            blink_roll = random()
            if blink_roll < BLINK_CHANCE:
                leye.keyframe_insert(data_path = 'scale', frame = t)
                leye.scale[1] = 0.2
                frm = math.floor(BLINK_LENGTH / 2) - 1
                leye.keyframe_insert(data_path = 'scale', frame = t + frm)
                frm = math.ceil(BLINK_LENGTH / 2) + 1
                leye.keyframe_insert(data_path = 'scale', frame = t + frm)
                leye.scale[1] = 1
                leye.keyframe_insert(data_path = 'scale', frame = t + BLINK_LENGTH)

                reye.keyframe_insert(data_path = 'scale', frame = t)
                reye.scale[1] = 0.2
                frm = math.floor(BLINK_LENGTH / 2) - 1
                reye.keyframe_insert(data_path = 'scale', frame = t + frm)
                frm = math.ceil(BLINK_LENGTH / 2) + 1
                reye.keyframe_insert(data_path = 'scale', frame = t + frm)
                reye.scale[1] = 1
                reye.keyframe_insert(data_path = 'scale', frame = t + BLINK_LENGTH)

                t += BLINK_LENGTH
            else:
                t += 1
        #Make blinks cyclical
        try:
            leye_fcurve = ref_obj.children[0].animation_data.action.fcurves.find(
                'pose.bones["brd_bone_eye.l"].scale',
                index = 1
            )
            l_cycle = leye_fcurve.modifiers.new(type = 'CYCLES')
            l_cycle.frame_start = 0
            l_cycle.frame_end = BLINK_CYCLE_LENGTH

            reye_fcurve = ref_obj.children[0].animation_data.action.fcurves.find(
                'pose.bones["brd_bone_eye.r"].scale',
                index = 1
            )
            r_cycle = reye_fcurve.modifiers.new(type = 'CYCLES')
            r_cycle.frame_start = 0
            r_cycle.frame_end = BLINK_CYCLE_LENGTH
        except:
            #Sometimes a creature goes the whole cycle length without blinking,
            #in which case, there's no fcurve, so the above block throws an
            #error. In the end, it's fine if the creature never blinks. It's rare.
            pass

    #Wiggles
    if 'wiggle' in kwargs:
        wiggle = kwargs['wiggle']
    else:
        wiggle = False
    if (filename == 'boerd_blob' or filename == 'boerd_blob_squat') \
        and wiggle == True:
        if 'cycle_length' not in kwargs:
            wiggle_cycle_length = BLINK_CYCLE_LENGTH
        else:
            wiggle_cycle_length = kwargs['cycle_length']
        wiggle_slow_factor = 1
        wind_down_time = FRAME_RATE / wiggle_slow_factor

        new_bobject.head_angle = [None] * wiggle_cycle_length
        new_bobject.head_angle_vel = [None] * wiggle_cycle_length
        for t in range(wiggle_cycle_length):
            if t == 0:
                #Start in neutral position
                new_bobject.head_angle[t] = [
                    1,
                    uniform(0, 0),
                    uniform(0, 0),
                    uniform(0, 0),
                ]
                new_bobject.head_angle_vel[t] = [
                    0,
                    uniform(-0.0025, 0.0025),
                    uniform(-0.0025, 0.0025),
                    uniform(-0.0025, 0.0025)
                ]
                bone = ref_obj.children[0].pose.bones[3]
                bone.rotation_quaternion = new_bobject.head_angle[t]
                bone.keyframe_insert(
                    data_path = "rotation_quaternion",
                    frame = t * wiggle_slow_factor
                )
            elif t < wiggle_cycle_length - wind_down_time:
                #Random movement up to a half second before end of cycle.
                #update position
                a = new_bobject.head_angle[t-1]
                b = new_bobject.head_angle_vel[t-1]
                new_bobject.head_angle[t] = list(map(sum, zip(a, b)))

                #Hard max on head angles
                extrema = [
                    [1, 1],
                    [-0.05, 0.05],
                    [-0.05, 0.05],
                    [-0.05, 0]
                ]
                a = new_bobject.head_angle[t]
                for i in range(1, len(new_bobject.head_angle[t])):
                    if a[i] < extrema[i][0]:
                        a[i] = extrema[i][0]
                    if a[i] > extrema[i][1]:
                        a[i] = extrema[i][1]

                #update velocity to be used when updating position
                #in next frame
                a = new_bobject.head_angle_vel[t-1]
                b = [
                    0,
                    uniform(-0.0005, 0.0005),
                    uniform(-0.0005, 0.0005),
                    uniform(-0.0005, 0.0005)
                ]
                #Shift the acceleration distribution toward neutral
                for i in range(1, len(b)):
                    go_back = -new_bobject.head_angle[t][i] / 5000
                    b[i] += go_back
                new_bobject.head_angle_vel[t] = list(map(sum, zip(a, b)))

                bone = ref_obj.children[0].pose.bones[3]
                bone.rotation_quaternion = new_bobject.head_angle[t]
                bone.keyframe_insert(
                    data_path = "rotation_quaternion",
                    frame = t * wiggle_slow_factor
                )
            else:
                #Approach neutral toward end of cycle, for continuity across
                #scenes
                #update position
                a = new_bobject.head_angle[t-1]
                b = new_bobject.head_angle_vel[t-1]
                new_bobject.head_angle[t] = list(map(sum, zip(a, b)))

                #Hard max on head angles
                extrema = [
                    [1, 1],
                    [-0.1, 0.1],
                    [-0.1, 0.1],
                    [-0.1, 0]
                ]
                a = new_bobject.head_angle[t]
                for i in range(1, len(new_bobject.head_angle[t])):
                    if a[i] < extrema[i][0]:
                        a[i] = extrema[i][0]
                        if b[i] < 0: b[i] = 0
                    if a[i] > extrema[i][1]:
                        a[i] = extrema[i][1]
                        if b[i] > 0: b[i] = 0

                #update velocity to be used when updating position
                #in next frame
                #Calculate acceleration needed to get back to neutral


                time_left = wiggle_cycle_length - t
                timing_factor = (wind_down_time - time_left) * time_left \
                                        / wind_down_time ** 2
                target_v = [ #Approaches zero as distance goes to zero
                    - a[1] * timing_factor,
                    - a[2] * timing_factor,
                    - a[3] * timing_factor,
                ]
                #print(target_v)

                acc_x = (target_v[0] - b[1]) / 2
                acc_y = (target_v[1] - b[2]) / 2
                acc_z = (target_v[2] - b[3]) / 2

                a = new_bobject.head_angle_vel[t-1]
                b = [
                    0,
                    acc_x,
                    acc_y,
                    acc_z,
                ]
                #print(" " + str(b))

                new_bobject.head_angle_vel[t] = list(map(sum, zip(a, b)))

                bone = ref_obj.children[0].pose.bones[3]
                bone.rotation_quaternion = new_bobject.head_angle[t]
                bone.keyframe_insert(
                    data_path = "rotation_quaternion",
                    frame = t * wiggle_slow_factor
                )

        #Make wiggle cyclical
        bone_x_fcurve = ref_obj.children[0].animation_data.action.fcurves.find(
            'pose.bones["brd_bone_neck"].rotation_quaternion',
            index = 0
        )
        neck_x_cycle = bone_x_fcurve.modifiers.new(type = 'CYCLES')
        neck_x_cycle.frame_start = 0
        neck_x_cycle.frame_end = wiggle_cycle_length * wiggle_slow_factor

        bone_y_fcurve = ref_obj.children[0].animation_data.action.fcurves.find(
            'pose.bones["brd_bone_neck"].rotation_quaternion',
            index = 1
        )
        neck_y_cycle = bone_y_fcurve.modifiers.new(type = 'CYCLES')
        neck_y_cycle.frame_start = 0
        neck_y_cycle.frame_end = wiggle_cycle_length * wiggle_slow_factor

        bone_z_fcurve = ref_obj.children[0].animation_data.action.fcurves.find(
            'pose.bones["brd_bone_neck"].rotation_quaternion',
            index = 2
        )
        neck_z_cycle = bone_z_fcurve.modifiers.new(type = 'CYCLES')
        neck_z_cycle.frame_start = 0
        neck_z_cycle.frame_end = wiggle_cycle_length * wiggle_slow_factor


    if filename == 'stanford_bunny':
        eye = ref_obj.children[0].children[0]
        t = 0
        while t < BLINK_CYCLE_LENGTH:
            blink_roll = random()
            if blink_roll < BLINK_CHANCE:
                eye.keyframe_insert(data_path = 'scale', frame = t)
                eye.scale[1] = 0.2
                frm = math.floor(BLINK_LENGTH / 2) - 1
                eye.keyframe_insert(data_path = 'scale', frame = t + frm)
                frm = math.ceil(BLINK_LENGTH / 2) + 1
                eye.keyframe_insert(data_path = 'scale', frame = t + frm)
                eye.scale[1] = 1
                eye.keyframe_insert(data_path = 'scale', frame = t + BLINK_LENGTH)

                t += BLINK_LENGTH
            else:
                t += 1
        #Make blinks cyclical
        try:
            eye_fcurve = ref_obj.children[0].children[0].animation_data.action.fcurves.find(
                'scale',
                index = 1
            )
            cycle = eye_fcurve.modifiers.new(type = 'CYCLES')
            cycle.frame_start = 0
            cycle.frame_end = BLINK_CYCLE_LENGTH
        except:
            #Sometimes a creature goes the whole cycle length without blinking,
            #in which case, there's no fcurve, so the above block throws an
            #error. In the end, it's fine if the creature never blinks. It's rare.
            pass


    return new_bobject

'''
Animation helpers
'''
def make_animations_linear(thing_with_animation_data):
    for fc in thing_with_animation_data.animation_data.action.fcurves:
        fc.extrapolation = 'LINEAR' # Set extrapolation type
        # Iterate over this fcurve's keyframes and set handles to vector
        for kp in fc.keyframe_points:
            kp.handle_left_type  = 'VECTOR'
            kp.handle_right_type = 'VECTOR'

'''
Time testing
'''
TIME_LIST = []
now = datetime.datetime.now()
TIME_LIST.append(now)
TIME_REPORT = []

def execute_and_time(message, *funcs):
    #Not sure how this will work for more than one function that returns
    outputs = []
    for func in funcs:
        output = func
        if output != None:
            outputs.append(output)

    now = datetime.datetime.now()
    TIME_LIST.append(now)
    diff = TIME_LIST[-1] - TIME_LIST[-2]
    TIME_REPORT.append([diff.total_seconds(), message])
    if not outputs:
        return
    if len(outputs) == 1:
        outputs = outputs[0]
    return outputs

def print_time_report():
    print()
    for line in TIME_REPORT:
        print(line[0], line[1])
    now = datetime.datetime.now()
    total = now - TIME_LIST[0]
    print(total.total_seconds(), "Total")

def finish_noise(error = False):
    '''tempo = 138 #beats per minute
    mspb = 60000 // tempo #milliseconds per beat

    duration = mspb // 4 #Triplet. Shorter because there's actually a delay
                         #between notes. It's like winsound wasn't planning on
                         #music or something. Wth.  ¯\_(ツ)_/¯
    freq = 523  # C
    winsound.Beep(freq, duration)
    duration = mspb // 4
    freq = 523  # C
    winsound.Beep(freq, duration)
    duration = mspb // 4
    freq = 523  # C
    winsound.Beep(freq, duration)
    duration = mspb #Quarter note
    freq = 523  # C
    winsound.Beep(freq, duration)

    duration = mspb #Quarter note
    freq = 415  # Ab
    winsound.Beep(freq, duration)
    duration = mspb #Quarter note
    freq = 466  # Bb
    winsound.Beep(freq, duration)
    duration = mspb // 4
    freq = 523  # C
    winsound.Beep(freq, duration)
    time.sleep((mspb // 2) / 1000) #Also different than you'd think.
    duration = mspb // 4
    freq = 466  # Bb
    winsound.Beep(freq, duration)
    duration = mspb #Quarter note
    freq = 523  # C
    winsound.Beep(freq, duration)'''
    if error == True:
        winsound.PlaySound("SystemHand", winsound.SND_ALIAS)
    else:
        winsound.MessageBeep()
    #If you're using this and aren't using windows, here's a resource:
    #https://stackoverflow.com/questions/16573051/python-sound-alarm-when-code-finishes
    #print('\007')

def main():
    import_object('boerd_blob')

if __name__ == "__main__":
    main()
