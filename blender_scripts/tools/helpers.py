import os
import sys
import imp
import bpy
import bmesh
import math
from random import random, uniform
from copy import copy, deepcopy
import time
import datetime
import pickle

import constants
imp.reload(constants)
from constants import *

#sys.path.append('C:\\Users\\justi\\Documents\\CodeProjects\\Primer\\blender_scripts')
import bobject
import winsound

'''
Saving
'''
def save_sim_result(sim, filename, filename_seed, type = 'SIM'):
    if filename != None:
        name = filename
    elif filename_seed != None:
        k = 0
        directory = os.fsencode(SIM_DIR)
        while k <= len(os.listdir(directory)):
            #print('looking in dir')
            name_to_check = str(filename_seed) + '_' + str(k)
            already_exists = False
            for existing_file in os.listdir(directory):
                existing_file_name = os.fsdecode(existing_file)[:-4]
                #print(name_to_check)
                #print(existing_file_name)
                if existing_file_name == name_to_check:
                    already_exists = True
                    #print(already_exists)
            if already_exists:
                k += 1
            else:
                name = name_to_check
                break
    else:
        now = datetime.datetime.now()
        name = type + now.strftime('%Y%m%dT%H%M%S')
    #name = 'test'
    result = os.path.join(
        SIM_DIR,
        name
    ) + ".pkl"
    if not os.path.exists(result):
        print("Writing simulation to %s" % (result))
        with open(result, "wb") as outfile:
            pickle.dump(sim, outfile, pickle.HIGHEST_PROTOCOL)
    else:
        raise Warning(str(result) + " already exists")

'''
Blender object functions

Different from the Bobject class, which is actually just a python container for
true Blender objects. Bobject is the class that uses these most, though.
'''

def apply_material(obj, mat, recursive = False, type_req = None, intensity = None):
    if obj.type not in ['EMPTY', 'ARMATURE']:
        if type_req == None or obj.type == type_req:
            if isinstance(mat, str):
                obj.active_material = bpy.data.materials[mat]
            else: #Assumes mat is a material.
                obj.active_material = mat

    if recursive:
        for child in obj.children:
            apply_material(child, mat, recursive = recursive, type_req = type_req)

    if intensity != None and 'trans' in mat:
        nodes = obj.active_material.node_tree.nodes

        scat = nodes['Volume Scatter']
        absorb = nodes['Volume Absorption']
        emit = nodes['Emission']

        for node in [scat, absorb, emit]:
            node.inputs[1].default_value = intensity

def define_materials():
    clear = bpy.data.materials.new(name = "clear")
    clear.use_nodes = True
    nodes = clear.node_tree.nodes
    nodes.remove(nodes[1]) #This is the diffuse shader by default
    nodes.new(type = 'ShaderNodeBsdfRefraction')
    nodes[1].inputs[0].default_value = (0.8, 1, 1, 1)
    #Hook up the refraction shader to the output (nodes[0])
    clear.node_tree.links.new(nodes[1].outputs[0], nodes[0].inputs[0])

    for i, col in enumerate(COLORS):
        name = 'color' + str(i + 1)
        make_basic_material(rgb = deepcopy(col), name = name)
        name = 'creature_color' + str(i + 1)
        make_creature_material(rgb = deepcopy(col), name = name)
        name = 'trans_color' + str(i + 1)
        make_translucent_material(rgb = deepcopy(col), name = name)

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

def add_color_gradient_to_mat(mat, color_gradient):
    nodes = mat.node_tree.nodes
    num = len(nodes)
    color_node = nodes[-1]
    color_field = color_node.inputs[0]

    nodes.new(type = 'ShaderNodeMixRGB')
    mat.node_tree.links.new(nodes[num].outputs[0], color_field)
    nodes[-1].inputs[1].default_value = color_gradient['color_1']
    nodes[-1].inputs[2].default_value = color_gradient['color_2']

    nodes.new(type = 'ShaderNodeTexGradient')
    mat.node_tree.links.new(nodes[-1].outputs[0], nodes[-2].inputs[0])

    nodes.new(type = 'ShaderNodeMapping')
    mat.node_tree.links.new(nodes[-1].outputs[0], nodes[-2].inputs[0])
    nodes[-1].vector_type = 'TEXTURE'
    nodes[-1].translation = color_gradient['translation']
    nodes[-1].rotation = color_gradient['rotation']
    nodes[-1].scale = color_gradient['scale']

    nodes.new(type = 'ShaderNodeTexCoord')
    mat.node_tree.links.new(nodes[-1].outputs[0], nodes[-2].inputs[0])

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
    #strength = 0.1

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

def material_clean_up():
    #Function for removing some duplicate materials from repeated imports
    for mat in bpy.data.materials:
        if 'color' not in mat.name:
            bpy.data.materials.remove(mat)

def make_image_background(file_name):
    #Background
    world = bpy.context.scene.world
    nodes = world.node_tree.nodes
    nodes.new(type = 'ShaderNodeMixRGB')
    nodes.new(type = 'ShaderNodeTexImage')
    nodes.new(type = 'ShaderNodeTexCoord')

    path_mix_input = nodes[2].inputs[2]

    for l in world.node_tree.links:
        if l.to_socket == path_mix_input:
           world.node_tree.links.remove(l)

    world.node_tree.links.new(nodes[5].outputs[0], nodes[2].inputs[2])
    world.node_tree.links.new(nodes[4].outputs[0], nodes[5].inputs[1])
    world.node_tree.links.new(nodes[6].outputs[0], nodes[5].inputs[2])
    world.node_tree.links.new(nodes[7].outputs[5], nodes[6].inputs[0])

    stars_path = os.path.join(IMG_DIR, file_name)
    try:
        img = bpy.data.images.load(stars_path)
    except:
        raise NameError("Cannot load image %s" % path)
    nodes[6].image = img

    nodes[5].inputs[0].default_value = 1


    #Keyframes for background transition
    """
    planets_start = 0
    planets_end = 1000
    nodes[5].inputs[0].default_value = 0

    nodes[4].outputs[0].keyframe_insert(data_path = 'default_value', frame = planets_start)
    nodes[4].outputs[0].default_value = (0, 0, 0, 1)
    nodes[4].outputs[0].keyframe_insert(data_path = 'default_value', frame = planets_start + 60)

    nodes[5].inputs[0].keyframe_insert(data_path = 'default_value', frame = planets_start + 60)
    nodes[5].inputs[0].default_value = 1
    nodes[5].inputs[0].keyframe_insert(data_path = 'default_value', frame = planets_start + 120)
    nodes[5].inputs[0].keyframe_insert(data_path = 'default_value', frame = planets_end - 90)
    nodes[5].inputs[0].default_value = 0
    nodes[5].inputs[0].keyframe_insert(data_path = 'default_value', frame = planets_end - 30)

    nodes[4].outputs[0].keyframe_insert(data_path = 'default_value', frame = planets_end - 30)
    nodes[4].outputs[0].default_value = COLORS_SCALED[0]
    nodes[4].outputs[0].keyframe_insert(data_path = 'default_value', frame = planets_end + 30)"""

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

def link_descendants(obj, unlink = False, top_level = True):
    #If children exist, link those too
    #Will break if imported children were linked in add_to_blender
    #(if their object name in blender is the same as the filename)

    if unlink == True and top_level == True:
        bpy.ops.object.select_all(action='DESELECT')
        obj.select = True

    obj_names = [x.name for x in bpy.data.objects]
    for child in obj.children:
        if unlink == False:
            if child.name not in bpy.context.scene.objects:
                bpy.context.scene.objects.link(child)
        else:
            child.select = True
        link_descendants(child, unlink = unlink, top_level = False)
    if unlink == True:
        bpy.ops.object.delete()

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

def mult_lists_by_element(vec1, vec2, divide = False):
    vec3 = []
    if divide == False:
        for x1, x2, in zip(vec1, vec2):
            vec3.append(x1 * x2)
    else:
        for x1, x2, in zip(vec1, vec2):
            vec3.append(x1 / x2)

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

def cross_product(a, b):
    result = []
    for i in range(3):
        result.append(a[(i+1)%3]*b[(i+2)%3] - a[(i+2)%3]*b[(i+1)%3])

    return result

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
Color functions
'''
def mix_colors(color1, color2, mix):
    if len(color1) != len(color2):
        raise Warning('Colors are different lengths')
    mixed_color = []
    #hsvcolor1 = rgb_to_hsv(*color1[:3])
    #hsvcolor2 = rgb_to_hsv(*color2[:3])
    for i in range(len(color1)):
        comp = color1[i] * (1 - mix) + color2[i] * mix
        #comp = hsvcolor1[i] * (1 - mix) + hsvcolor2[i] * (1 - mix)
        mixed_color.append(comp)

    #return hsv_to_rgb(*mixed_color)
    return mixed_color

def hsv_to_rgb(h, s, v):
    h = float(h)
    s = float(s)
    v = float(v)
    h60 = h / 60.0
    h60f = math.floor(h60)
    hi = int(h60f) % 6
    f = h60 - h60f
    p = v * (1 - s)
    q = v * (1 - f * s)
    t = v * (1 - (1 - f) * s)
    r, g, b = 0, 0, 0
    if hi == 0: r, g, b = v, t, p
    elif hi == 1: r, g, b = q, v, p
    elif hi == 2: r, g, b = p, v, t
    elif hi == 3: r, g, b = p, q, v
    elif hi == 4: r, g, b = t, p, v
    elif hi == 5: r, g, b = v, p, q
    #Returns rgb values scaled to a max value of 1 instead of 255
    #r, g, b = int(r * 255), int(g * 255), int(b * 255)
    return [r, g, b]

def rgb_to_hsv(r, g, b):
    #Takes rgb values scaled to a max value of 1 instead of 255
    #r, g, b = r/255.0, g/255.0, b/255.0
    mx = max(r, g, b)
    mn = min(r, g, b)
    df = mx-mn
    if mx == mn:
        h = 0
    elif mx == r:
        h = (60 * ((g-b)/df) + 360) % 360
    elif mx == g:
        h = (60 * ((b-r)/df) + 120) % 360
    elif mx == b:
        h = (60 * ((r-g)/df) + 240) % 360
    if mx == 0:
        s = 0
    else:
        s = df/mx
    v = mx
    return [h, s, v]

def color_to_primer_palette(obj):
    #Only works for non-node materials
    if len(obj.material_slots) == 0:
        return

    col = list(obj.material_slots[0].material.diffuse_color)

    min_dist = math.inf
    match_index = None
    for j, color in enumerate(COLORS_SCALED):
        dist = 0
        for i in range(3):
            dist += (abs(col[i] - color[i])) ** 2
        if dist < min_dist:
            min_dist = dist
            match_index = j

    mat_string = 'color' + str(match_index + 1)

    apply_material(obj, mat_string)






'''
Geometry
'''

def triangle_orientation(point1, point2, point3):
    a = add_lists_by_element(point2, point1, subtract = True)
    b = add_lists_by_element(point3, point1, subtract = True)
    c = cross_product(a, b)

    if c[2] == 0:
        return 0 #colinear assuming points are in xy-plane
    elif c[2] > 0:
        return 1 #counter-clockwise
    elif c[2] < 0:
        return -1 #clockwise

def do_segments_intersect(seg1, seg2):
    #(Point p1, Point q1, Point p2, Point q2)

    o1 = triangle_orientation(seg1[0], seg1[1], seg2[0]);
    o2 = triangle_orientation(seg1[0], seg1[1], seg2[1]);
    o3 = triangle_orientation(seg2[0], seg2[1], seg1[0]);
    o4 = triangle_orientation(seg2[0], seg2[1], seg1[1]);

    if o1 != o2 and o3 != o4:
        return True;

    #Doesn't handle the collinear case

def make_angles_within_pi(angle_to_change = None, reference_angle = None):
    while angle_to_change - reference_angle > math.pi:
        angle_to_change -= 2 * math.pi
    while angle_to_change - reference_angle < -math.pi:
        angle_to_change += 2 * math.pi
    return angle_to_change


def circle_grid(
    num_rings = 10,
    dot_count_multiple = 6,
    rot_add = 6,
):
    locations = []
    for i in range(num_rings):
        if i == 0:
            num_dots = 1
        else:
            num_dots = i * dot_count_multiple

        if num_rings > 1:
            radius = i / (num_rings - 1)
        else:
            radius = 0
        for j in range(num_dots):
            angle = j / num_dots * 2 * math.pi + (i * rot_add * math.pi / 180)
            loc = [
                radius * math.cos(angle),
                radius * math.sin(angle),
                0
            ]

            locations.append(loc)

    return locations

'''
Mesh intersections
'''
def bmesh_copy_from_object(obj, transform=True, triangulate=True, apply_modifiers=False):
    """
    Returns a transformed, triangulated copy of the mesh
    """

    assert(obj.type == 'MESH')

    if apply_modifiers and obj.modifiers:
        me = obj.to_mesh(bpy.context.scene, True, 'PREVIEW', calc_tessface=False)
        bm = bmesh.new()
        bm.from_mesh(me)
        bpy.data.meshes.remove(me)
    else:
        me = obj.data
        if obj.mode == 'EDIT':
            bm_orig = bmesh.from_edit_mesh(me)
            bm = bm_orig.copy()
        else:
            bm = bmesh.new()
            bm.from_mesh(me)

    # Remove custom data layers to save memory
    for elem in (bm.faces, bm.edges, bm.verts, bm.loops):
        for layers_name in dir(elem.layers):
            if not layers_name.startswith("_"):
                layers = getattr(elem.layers, layers_name)
                for layer_name, layer in layers.items():
                    layers.remove(layer)

    if transform:
        bm.transform(obj.matrix_world)

    if triangulate:
        bmesh.ops.triangulate(bm, faces=bm.faces)

    return bm

def bmesh_check_intersect_objects(obj, obj2, location_as_proxy = True):
    """
    Check if any faces intersect with the other object
    returns a boolean
    """

    if location_as_proxy == True:
        diff = obj2.location - obj.location
        dist = diff.length
        if dist > 1:
            return False

    assert(obj != obj2)

    # Triangulate
    bm = bmesh_copy_from_object(obj, transform=True, triangulate=True)
    bm2 = bmesh_copy_from_object(obj2, transform=True, triangulate=True)

    # If bm has more edges, use bm2 instead for looping over its edges
    # (so we cast less rays from the simpler object to the more complex object)
    if len(bm.edges) > len(bm2.edges):
        bm2, bm = bm, bm2

    # Create a real mesh (lame!)
    scene = bpy.context.scene
    me_tmp = bpy.data.meshes.new(name="~temp~")
    bm2.to_mesh(me_tmp)
    bm2.free()
    obj_tmp = bpy.data.objects.new(name=me_tmp.name, object_data=me_tmp)
    scene.objects.link(obj_tmp)
    scene.update()
    ray_cast = obj_tmp.ray_cast

    intersect = False

    EPS_NORMAL = 0.000001
    EPS_CENTER = 0.01  # should always be bigger

    #for ed in me_tmp.edges:
    for ed in bm.edges:
        v1, v2 = ed.verts

        # setup the edge with an offset
        co_1 = v1.co.copy()
        co_2 = v2.co.copy()
        co_mid = (co_1 + co_2) * 0.5
        no_mid = (v1.normal + v2.normal).normalized() * EPS_NORMAL
        co_1 = co_1.lerp(co_mid, EPS_CENTER) + no_mid
        co_2 = co_2.lerp(co_mid, EPS_CENTER) + no_mid

        res, co, no, index = ray_cast(co_1, co_2)
        if index != -1:
            intersect = True
            break

    scene.objects.unlink(obj_tmp)
    bpy.data.objects.remove(obj_tmp)
    bpy.data.meshes.remove(me_tmp)

    scene.update()

    return intersect

def find_intersections(meshes):
    intersections = []
    for i in range(len(meshes)):
        print(str(i + 1) + ' of ' + str(len(meshes)))
        #print('Checking for intersections with ' + meshes[i].name)
        for j in range(0, i):
            intersection = bmesh_check_intersect_objects(meshes[i], meshes[j])
            #print(intersection)
            #Sometimes cylinders and spheres touch even though they shouldn't
            #be counted
            same_type = False
            if 'Sphere' in meshes[i].name and 'Sphere' in meshes[j].name:
                same_type = True
            if 'Cylinder' in meshes[i].name and 'Cylinder' in meshes[j].name:
                same_type = True
            if intersection == True and same_type == False:
                intersections.append([meshes[i], meshes[j]])

    return intersections

def get_centrality(mesh, intersection_checklist, depth):
    #Kind of a weird name for this function

    score = 0
    if 'Sphere' in mesh.name:
        score = depth * depth
    for line in intersection_checklist:
        if mesh in line[0] and line[1] == False:
            #print(' ' + mesh.name + ' ' + str(line[0]))
            line[1] = True

            for thing in line[0]:
                if thing != mesh:
                    next_mesh = thing

            if 'Sphere' in next_mesh.name:
                next_depth = depth + 1
            else:
                next_depth = depth

            score += get_centrality(next_mesh, intersection_checklist, next_depth)

    return score

def establish_ancestors(mesh, intersections):
    #Kind of a weird name for this function

    #print(mesh)
    #print(mesh.name)

    for inter in intersections:
        if mesh in inter:
            for thing in inter:
                if thing != mesh:
                    next_mesh = thing

            #Second requirement prevents error with root parent
            if next_mesh.parent == None and len(next_mesh.children) == 0:
                #Don't make cylinders parents, since they need different visual
                #treatment
                while "Cylinder" in mesh.name:
                    mesh = mesh.parent
                next_mesh.parent = mesh
                next_mesh.matrix_parent_inverse = mesh.matrix_world.inverted()
                establish_ancestors(next_mesh, intersections)

def make_parent_tree():
    #Only works when all meshes are part of one intersecting whole.

    meshes = []
    for obj in bpy.data.objects:
        if obj.type == 'MESH':
            meshes.append(obj)

    intersections = find_intersections(meshes)
    print(intersections)
    print()

    #Getting centrality identifies an atom near some definition of the middle of
    #the molecule. Not actually necessary and takes a while for big molecules.
    #Originally did this because I was going to manually uwnind RNA.
    #Even then, not necessary.
    print('Getting centrality')

    while len(intersections) > 0:
        #min_score = math.inf
        max_score = -math.inf
        central_mesh = None
        for mesh in meshes:
            intersection_checklist = []
            for inter in intersections:
                intersection_checklist.append([inter, False])
            score = get_centrality(mesh, intersection_checklist, 0)
            #print(mesh.name, score)
            if len(mesh.children) == 0 and \
               mesh.parent == None and \
               'Cylinder' not in mesh.name and \
               score > max_score:
               #score < min_score:
                #min_score = score
                max_score = score
                central_mesh = mesh
        #print()
        #print(central_mesh.name, min_score)
        #print()

        establish_ancestors(central_mesh, intersections)

        remaining_intersections = []
        for inter in intersections:
            if inter[0] == central_mesh or inter[1] == central_mesh:
                continue
            if is_ancestor(inter[0], central_mesh):
                continue
            if is_ancestor(inter[1], central_mesh):
                continue
            remaining_intersections.append(inter)

        intersections = remaining_intersections
        print(intersections)

def is_ancestor(mesh, candidate_ancestor):
    if mesh.parent == candidate_ancestor:
        #print(str(candidate_ancestor) + ' is ancestor of ' + str(mesh))
        return True
    if mesh.parent == None:
        #print(str(candidate_ancestor) + ' is NOT ancestor of ' + str(mesh))
        return False

    return is_ancestor(mesh.parent, candidate_ancestor)

'''
Bobject helpers
'''
#Import object from another blend file and return bobject
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

        leye.keyframe_insert(data_path = 'scale', frame = 0)
        leye.keyframe_insert(data_path = 'scale', frame = BLINK_CYCLE_LENGTH)
        reye.keyframe_insert(data_path = 'scale', frame = 0)
        reye.keyframe_insert(data_path = 'scale', frame = BLINK_CYCLE_LENGTH)


        while t < cycle_length - BLINK_LENGTH:
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
            #l_cycle.blend_out = BLINK_CYCLE_LENGTH

            reye_fcurve = ref_obj.children[0].animation_data.action.fcurves.find(
                'pose.bones["brd_bone_eye.r"].scale',
                index = 1
            )
            r_cycle = reye_fcurve.modifiers.new(type = 'CYCLES')
            #r_cycle.blend_out = BLINK_CYCLE_LENGTH
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
            wiggle_cycle_length = int(kwargs['cycle_length'])
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

def cam_and_swivel(
    cam_location = [25, 0, 0],
    cam_rotation_euler = [0, 0, 0],
    cam_name = "Camera Bobject",
    swivel_location = [0, 0, 0],
    swivel_rotation_euler = [0, 0, 0],
    swivel_name = 'Cam swivel',
    control_sun = False
):
    cam_bobj = bobject.Bobject(
        location = cam_location,
        rotation_euler = cam_rotation_euler,
        name = cam_name
    )
    cam_swivel = bobject.Bobject(
        cam_bobj,
        location = swivel_location,
        rotation_euler = swivel_rotation_euler,
        name = swivel_name,
    )

    cam_obj = bpy.data.objects['Camera']
    cam_obj.data.clip_end = 100
    cam_obj.location = [0, 0, 0]
    cam_obj.parent = cam_bobj.ref_obj

    if control_sun == True:
        sun_obj = bpy.data.objects['Sun']
        sun_obj.location = [0, 0, 0]
        sun_obj.parent = cam_bobj.ref_obj

    return cam_bobj, cam_swivel


'''
Animation helpers
'''
def make_animations_linear(thing_with_animation_data, data_paths = None, extrapolate = False):
    if data_paths == None:
        f_curves = thing_with_animation_data.animation_data.action.fcurves
    else:
        f_curves = []
        for fc in thing_with_animation_data.animation_data.action.fcurves:
            if fc.data_path in data_paths:
                f_curves.append(fc)
    for fc in f_curves:
        if extrapolate == True:
            fc.extrapolation = 'LINEAR' # Set extrapolation type
        # Iterate over this fcurve's keyframes and set handles to vector
        for kp in fc.keyframe_points:
            kp.handle_left_type  = 'VECTOR'
            kp.handle_right_type = 'VECTOR'
            kp.interpolation = 'LINEAR'


'''
Anatomy video helpers
'''
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
Time measurement
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
    TIME_LIST.append(now) #Actually just records end time, not start and end
                          #So reported value includes previous, seemingly untimed code
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
