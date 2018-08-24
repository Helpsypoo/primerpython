import imp
import bpy
import mathutils
import math
import pickle
import inspect
from copy import deepcopy
from random import random, uniform

import sys
sys.path.append('C:\\Users\\justi\\Documents\\CodeProjects\\Primer\\blender_scripts')
sys.path.append('C:\\Users\\justi\\Documents\\CodeProjects\\Primer\\blender_scripts\\tools')

import bobject
import drawn_world
import tex_bobject
import constants


import clear
#import alone doesn't check for changes in cached files
imp.reload(drawn_world)
imp.reload(tex_bobject)

imp.reload(constants)
from constants import *

import svg_bobject
imp.reload(svg_bobject)
from svg_bobject import *

import graph_bobject
imp.reload(graph_bobject)
from graph_bobject import *

import helpers
imp.reload(helpers)
from helpers import *

sys.path.append('C:\\Users\\justi\\Documents\\CodeProjects\\Primer\\blender_scripts\\video_scenes')
import why_things_exist
imp.reload(why_things_exist)
from why_things_exist import *

import replication_only
imp.reload(replication_only)
from replication_only import *

import mutations
imp.reload(mutations)
from mutations import *

import logistic_growth
imp.reload(logistic_growth)
from logistic_growth import *

"""import fecal_transplant
imp.reload(fecal_transplant)
from fecal_transplant import *"""

import population
imp.reload(population)
from population import *

import gesture
imp.reload(gesture)
from gesture import *

import tex_complex
imp.reload(tex_complex)
from tex_complex import TexComplex

'''
Workflow improvements
- Make a decision about specifying start/end or start/duration and make
    keyframing functions follow that convention.
- Automate rendering
- Write function to run sims until it finds one with the right results
- Make sims take more arguments (e.g., pop cap, closeness)

New functionality
- Family tree

Open source
- Code organization centered on creation workflow
e.g., Add kwargs to class init functions to customize on instantiation
- Clean up imports
- Delete old print statements and commented-out blocks

Performance
- Final render speed
-- Possibly convert metaballs to mesh, or something
-- Hide bobjects that haven't appeared yet so they don't need to be syncronized
--  for render.
'''

def initialize_blender(total_duration = DEFAULT_SCENE_DURATION):
    #clear objects and materials
    #Reading the homefile would likely by faster, but it
    #sets the context to None, which breaks a bunch of
    #other stuff down the line. I don't know how to make the context not None.
    #bpy.ops.wm.read_homefile()

    clear.clear_blender()

    scn = bpy.context.scene
    scn.render.engine = 'CYCLES'
    scn.cycles.device = 'GPU'
    scn.cycles.samples = SAMPLE_COUNT
    scn.cycles.preview_samples = SAMPLE_COUNT
    scn.cycles.light_sampling_threshold = LIGHT_SAMPLING_THRESHOLD
    scn.cycles.transparent_max_bounces = 40
    scn.render.resolution_percentage = RESOLUTION_PERCENTAGE
    scn.render.use_compositing = False
    scn.render.use_sequencer = False
    scn.render.image_settings.file_format = 'PNG'
    scn.render.tile_x = RENDER_TILE_SIZE
    scn.render.tile_y = RENDER_TILE_SIZE
    #Apparentlly 16-bit color depth pngs don't convert well to mp4 in Blender.
    #It gets all dark. 8-bit it is.
    #scn.render.image_settings.color_depth = '16'


    #Set to 60 fps
    bpy.ops.script.execute_preset(
        filepath="C:\\Program Files\\Blender Foundation\\Blender\\2.79\\scripts\\presets\\framerate\\60.py",
        menu_idname="RENDER_MT_framerate_presets"
    )
    #The line below makes it so Blender doesn't apply gamma correction. For some
    #reason, Blender handles colors differently from how every other programe
    #does, and it's terrible. Why.
    #But this fixes it. Also, the RGB values you see in Blender
    #will be wrong, because the gamma correction is still applied when the color
    #is defined, but setting view_transform to 'Raw' undoes the correction in
    #render.
    scn.view_settings.view_transform = 'Raw'


    scn.gravity = (0, -9.81, 0)

    bpy.ops.world.new()
    world = bpy.data.worlds[-1]
    scn.world = world
    nodes = world.node_tree.nodes
    nodes.new(type = 'ShaderNodeMixRGB')
    nodes.new(type = 'ShaderNodeLightPath')
    nodes.new(type = 'ShaderNodeRGB')
    world.node_tree.links.new(nodes[2].outputs[0], nodes[1].inputs[0])
    world.node_tree.links.new(nodes[3].outputs[0], nodes[2].inputs[0])
    world.node_tree.links.new(nodes[4].outputs[0], nodes[2].inputs[2])
    nodes[4].outputs[0].default_value = COLORS_SCALED[0]

    define_materials()

    #set up timeline
    bpy.data.scenes["Scene"].frame_start = 0
    bpy.data.scenes["Scene"].frame_end = total_duration * FRAME_RATE - 1
    bpy.context.scene.frame_set(0)

    #create camera and light
    bpy.ops.object.camera_add(location = CAMERA_LOCATION, rotation = CAMERA_ANGLE)
    cam = bpy.data.cameras[0]
    #cam.type = 'ORTHO'
    cam.type = 'PERSP'
    cam.ortho_scale = 30

    bpy.ops.object.empty_add(type = 'PLAIN_AXES', location = (0, 0, 100))
    lamp_parent = bpy.context.object
    lamp_parent.name = 'Lamps'

    lamp_height = 35
    bpy.ops.object.lamp_add(type = LAMP_TYPE, location = (0, 0, lamp_height))
    lamp = bpy.context.object
    lamp.parent = lamp_parent
    lamp.matrix_parent_inverse = lamp.parent.matrix_world.inverted()
    lamp.data.node_tree.nodes[1].inputs[1].default_value = 1.57

    #Sets view to look through camera.
    for area in bpy.context.screen.areas:
        if area.type == 'VIEW_3D':
            override = bpy.context.copy()
            override['area'] = area
            bpy.ops.view3d.viewnumpad(override, type = 'CAMERA')
            break

def color_test():
    initialize_blender()

    swatch1 = import_object('xyplane', 'primitives', name = 'swatch1', location = (-6, 0, 0), scale = 1.5)
    apply_material(swatch1.ref_obj.children[0], 'color1')
    swatch1.add_to_blender()

    swatch2 = import_object('xyplane', 'primitives', name = 'swatch2', location = (-3, 0, 0), scale = 1.5)
    apply_material(swatch2.ref_obj.children[0], 'color2')
    swatch2.add_to_blender()

    swatch3 = import_object('xyplane', 'primitives', name = 'swatch3', location = (0, 0, 0), scale = 1.5)
    apply_material(swatch3.ref_obj.children[0], 'color3')
    swatch3.add_to_blender()

    swatch4 = import_object('xyplane', 'primitives', name = 'swatch4', location = (3, 0, 0), scale = 1.5)
    apply_material(swatch4.ref_obj.children[0], 'color4')
    swatch4.add_to_blender()

    swatch5 = import_object('xyplane', 'primitives', name = 'swatch5', location = (6, 0, 0), scale = 1.5)
    apply_material(swatch5.ref_obj.children[0], 'color5')
    swatch5.add_to_blender()

def is_scene(obj):
   if not inspect.isclass(obj):
      return False
   if not issubclass(obj, Scene):
      return False
   if obj == Scene:
      return False
   return True

def get_total_duration(scenes):
    #scenes is a list of (name, object) pairs
    duration = 0
    for scene in scenes:
        duration += scene[1].duration + DEFAULT_SCENE_BUFFER
    return duration

def get_scene_object_list(script_file):
    pairs = inspect.getmembers(script_file, is_scene)
    #The output of inspect.getmembers is a list of (name, class) pairs.
    #This turns that list into a list of (name, object) pairs
    objects = []
    for pair in pairs:
        objects.append([pair[0], pair[1]()])
    return objects

def test_object():
    scene_length = 4

    initialize_blender(total_duration = scene_length)

    ear = import_object(
        'inner_ear_2',
        location = (5, -11, 0),
        scale = 5,
    )
    apply_material(ear.ref_obj.children[0], 'creature_color4')
    apply_material(ear.ref_obj.children[0].children[0], 'trans_color2')
    ##Create blender-side objects and manipulate
    ear.add_to_blender(
        appear_time = 0
    )

def test_sim():
    total_duration = 200

    initialize_blender(total_duration = total_duration)

    blob1_sim_start = 0
    #Blob sim 1
    ##Create python-side objects

    initial_creature_count = 10
    initial_creatures = []
    for i in range(initial_creature_count):
        new_creature = creature.Creature(color = 'creature_color_1', shape = 'shape2')
        initial_creatures.append(new_creature)
    blob1_sim = drawn_world.DrawnWorld(
        name = 'blob2_sim',
        location = [0, 0, 0],
        scale = 1,
        appear_frame = blob1_sim_start,
        start_delay = 50,
        #load = 'speed_test',
        duration = total_duration,
        #initial_creatures = initial_creatures,
        gene_updates = [
            ['color', 'creature_color_1', 'birth_modifier', 100, 0],
            ['shape', 'shape1', 'birth_modifier', 1, 0],
            ['size', '1', 'birth_modifier', 1, 0],
            ['color', 'creature_color_1', 'replication_modifier', 0, 0],
            ['color', 'creature_color_1', 'death_modifier', 10, 0],
        ],
        counter_alignment = 'top_left'
    )

    blob1_sim.add_counter(
                label = "\\text{Total: }",
    ),
    blob1_sim.add_counter(
                label = "\\text{Average: }",
                average = True
    )
    blob1_sim.add_to_blender(
        appear_frame = blob1_sim_start,
        animate = True
    )

    blob1_sim.disappear(
        disappear_frame = total_duration
    )
    '''for chain in blob1_sim.info[0].subbobjects[1].char_morph_chains:
        for link in chain:
            print(link.ref_obj.name)
        print()'''




    print_time_report()

def tex_test():
    initialize_blender(total_duration = 100)

    plug_Ns = []
    delta_outs = []
    num_states = 51
    for i in range(0, max):
        Nstring = "\\big(0.1-0.05 - 0.001\\times" + str(i) + "\\big) \\times" + str(i)
        plug_Ns.append(Nstring)
        delta = (0.05 - 0.001 * i) * i
        delta_string = str('{0:.2f}'.format(delta))
        delta_outs.append(delta_string)

    rhs2 = tex_bobject.TexBobject(
        *plug_Ns,
        transition_type = 'instant',
        centered = True
    )
    equals2 = tex_bobject.TexBobject(
        "\!=",
        transition_type = 'instant',
        centered = True
    )
    lhs2 = tex_bobject.TexBobject(
        *delta_outs,
        transition_type = 'instant',
        centered = True
    )
    equation2 = tex_complex.TexComplex(
        lhs2, equals2, rhs2,
        location = (0, 0, 0),
        scale = 2,
        centered = True
    )
    equation2.add_to_blender(appear_time = 0.5, animate = False)

    for i in range(1, num_states):
        if i == 10:
            arrange_super = True
        else: arrange_super = False
        rhs2.morph_figure(i, start_time = 1 + i * 0.05, arrange_super = arrange_super)
        lhs2.morph_figure(i, start_time = 1 + i * 0.05, arrange_super = False)


    """ming = tex_bobject.TexBobject(
        '\\text{You\'re}',
        '\\text{the}',
        '\\text{best!}',
        centered = True,
        scale = 8
    )
    ming.add_to_blender(appear_time = 0)

    ming.morph_figure('next', start_time = 1)

    ming.morph_figure('next', start_time = 2)

    ming.disappear(disappear_time = 3.5)"""

    '''reddit = import_object(
        'reddit', 'svgblend',
        scale = 4,
        location = (-5, 0, 0)
    )
    reddit.add_to_blender(appear_frame = 0)
    patreon = import_object(
        'patreon', 'svgblend',
        scale = 4,
        location = (5, 0, 0)
    )
    patreon.add_to_blender(appear_frame = 0)'''

    """patreon = import_object(
        'patreon', 'svgblend',
        scale = 6,
        location = (-8, 0, 0)
    )
    patreon.add_to_blender(appear_time = 0)
    thanks = tex_bobject.TexBobject(
        '\\text{Special thanks:}',
        location = [-1.5, 3.8, 0],
        color = 'color2',
        scale = 2
    )
    thanks.add_to_blender(appear_time = 0)
    js = tex_bobject.TexBobject(
        '\\text{You}',
        location = [-2.5, -2, 0],
        color = 'color2',
        scale = 8
    )
    js.add_to_blender(
        appear_time = 1,
        animate = False
    )

    remaining = [patreon, thanks, js]
    for thing in remaining:
        thing.disappear(disappear_time = 3)"""

    print_time_report()

def morph_test():
    initialize_blender()

    bobj = bobject.MeshMorphBobject(scale = 1)

    #bobj.add_subbobject_to_series(import_object('sphere_cube'))
    #bobj.add_subbobject_to_series(import_object('octo'))
    #bobj.add_subbobject_to_series(import_object('goodicosphere', scale = 3))
    bobj.add_subbobject_to_series(import_object('H2O', 'biochem', scale = 6))
    #bobj.series[0].ref_obj.location = (0, 0, 0)
    apply_material(bobj.series[0].ref_obj.children[0], 'color3')


    bobj.add_subbobject_to_series(import_object('sucrose', 'biochem', scale = 1.2))
    bobj.series[1].ref_obj.location = (0, 0.5, 0)
    apply_material(bobj.series[1].ref_obj.children[0], 'color4')

    bobj.add_subbobject_to_series(import_object('bacteria', 'biochem', scale = 4))

    bobj.add_to_blender()
    bobj.morph_bobject(0, 1, 20, 35)
    bobj.morph_bobject(1, 2, 55, 70)

    '''bobj.series[1].ref_obj.keyframe_insert(data_path="location", frame = 0)
    bobj.series[1].ref_obj.location = (0, 2, 0)
    bobj.series[1].ref_obj.keyframe_insert(data_path="location", frame = 100)'''


    #bobj.series[1].ref_obj.children[0].hide = False

    #Spiiiiiiiin
    bobj.ref_obj.rotation_euler = (0, 0, 0)
    bobj.ref_obj.keyframe_insert(data_path="rotation_euler", frame = 0)
    bobj.ref_obj.rotation_euler = (0, 0, 2*math.pi)
    bobj.ref_obj.keyframe_insert(data_path="rotation_euler", frame = 100)

    print_time_report()

def gesture_test():
    initialize_blender()

    bracket = gesture.Gesture(
        gesture_series = [
            {
                'type': 'arrow',
                'points': {
                    'tail': (0, -2, 0),
                    'head': (2, 0, 0)
                }
            },
            {
                'type': 'arrow',
                'points': {
                    'tail': (0, 0, 0),
                    'head': (0, -1, 0)
                }
            },
            {
                'type': 'bracket',
                'points': {
                    'annotation_point': (0, 1, 0),
                    'left_point': (-3, 0, 0),
                    'right_point': (5, 0, 0)
                }
            }
        ]
    )
    bracket.add_to_blender(appear_frame = 0)
    bracket.morph_figure(1, start_frame = 50)
    bracket.morph_figure(2, start_frame = 100)

def draw_scenes_from_file(script_file):
    #This function is meant to process many scenes at once.
    #Most scenes end up being large enough where it doesn't make sense to have
    #more than one in blender at once, so this is obsolete and will
    #break if you try to process more than one scene at a time.
    scenes = get_scene_object_list(script_file)
    #print(scenes)
    duration = get_total_duration(scenes)
    initialize_blender(total_duration = duration)

    frame = 0
    for scene in scenes:
        execute_and_time(
            scene[0], #This is just a string
            scene[1].play()
        )
        #frame += scene[1].duration + DEFAULT_SCENE_BUFFER

    #Hide empty objects from render, for speed
    for obj in bpy.data.objects:
        if obj.type == 'EMPTY':
            obj.hide_render = True
    #Doesn't change much, since most empty objects are keyframed handles for
    #other objects.

    print_time_report()

def test_molecule():
    #initialize_blender()

    make_parent_tree()

    """rna = import_object(
        'rna', 'biochem',
    )
    rna.add_to_blender(
        appear_time = 0,
        animate = False
    )"""

def graph_test():
    initialize_blender(total_duration = 120)

    '''def func(x):
        return 10 * math.sin(3*x) * math.cos(x / 6) #+ math.sin(5*x)
        #return 3 + 5 * x - 1.5 * x * x + (x ** 3) / 9.2
        #return 10 - (9 * (10 ** (10 - x)) / (10 ** 10))
    '''

    def func(x):
        return 2 * math.sin(x) + 3
        #return 3 + 5 * x - 1.5 * x * x + (x ** 3) / 9.2
        #return 10 - (9 * (10 ** (10 - x)) / (10 ** 10))
        #return - x * x / 10 + 10

    graph = graph_bobject.GraphBobject(
        func,
        x_range = [0, 10],
        y_range = [0, 10],
        tick_step = [5, 5],
        width = 15,
        height = 15,
        x_label = '\\text{Time}',
        x_label_pos = 'along',
        y_label = 'N',
        y_label_pos = 'along',
        location = (0, 0, 0),
        centered = True,
        arrows = True
    )
    graph.add_to_blender(curve_colors = 'fade_secondary')

    graph.change_window(
        start_time = 5,
        new_x_range = [0, 6],
        new_y_range = [0, 6],
        new_tick_step = [2, 2]
    )

    '''graph.animate_function_curve(
        start_frame = 60,
        end_frame = 180,
        uniform_along_x = True,
        index = 0
    )'''

def marketing():
    scene_end = 12
    initialize_blender(total_duration = scene_end)

    x = 7.64349
    y = -8.71545

    b_blob = import_object(
        'boerd_blob_stern', 'creatures',
        location = [-x, y, 0],
        rotation_euler = [0, 57.4 * math.pi / 180, 0],
        scale = 12,
    )
    b_blob.ref_obj.children[0].children[0].data.resolution = 0.2
    apply_material(b_blob.ref_obj.children[0].children[0], 'creature_color3')
    b_blob.add_to_blender(appear_time = 0)

    y_blob = import_object(
        'boerd_blob_stern', 'creatures',
        rotation_euler = [0, -57.4 * math.pi / 180, 0],
        location = [x, y, 0],
        scale = 12,
    )
    y_blob.ref_obj.children[0].children[0].data.resolution = 0.2
    apply_material(y_blob.ref_obj.children[0].children[0], 'creature_color4')
    y_blob.add_to_blender(appear_time = 0)

    y_blob.blob_wave(
        start_time = 0,
        duration = 12
    )

    comp = tex_bobject.TexBobject(
        '\\text{COMPETITION} \\phantom{blargh}',
        centered = True,
        scale = 4.5,
        location = [0, 5.5, 0],
        color = 'color2'
    )
    comp.add_to_blender(appear_time = 0)

def main():
    #test_molecule()
    #tex_test()
    #test_object()
    marketing()

    #graph_test()
    #draw_scenes_from_file(logistic_growth)

    #initialize_blender(total_duration = 15)
    #mutations.play_scenes()

    #print_time_report()
    finish_noise()


if __name__ == "__main__":
    try:
        main()
    except:
        finish_noise(error = True)
        raise()
