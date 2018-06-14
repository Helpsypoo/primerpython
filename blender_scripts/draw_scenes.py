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
- Preview of graphs and family trees (?)

New functionality
- Stop and alter play speed of sims
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
    scn.render.resolution_percentage = RESOLUTION_PERCENTAGE
    scn.render.use_compositing = False
    scn.render.use_sequencer = False
    scn.render.image_settings.file_format = 'PNG'
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
    bpy.data.scenes["Scene"].frame_end = total_duration * FRAME_RATE
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

    blob2_intro_start = 0
    blob2_intro_end = blob2_intro_start + 40

    blob2_sim_start = blob2_intro_end
    blob2_sim_end = blob2_sim_start

    scene_end = blob2_sim_end

    initialize_blender(total_duration = scene_end)

    blob2 = import_object(
        'boerd_blob_squat',
        'creatures',
        location = (7, 2, 0),
        scale = 4
    )
    for child in blob2.ref_obj.children[0].children:
        if child.type == 'META':
            if len(child.material_slots) > 0:
                child.data.resolution = 0.1
                apply_material(child, 'creature_color4')

    '''birth_chance_tex2 = tex_bobject.TexBobject('\\text{Birth chance each frame} = 10\\%')
    birth_tex_container2 = tex_complex.TexComplex(
        birth_chance_tex2,
        centered= True,
        location = (7, -4, 0),
        scale = 0.67
    )
    birth_tex_container2.add_to_blender(
        appear_frame = blob2_intro_start + 24,
        animate = True
    )
    death_chance_tex2 = tex_bobject.TexBobject('\\text{Survival chance each frame} = 99\\%')
    death_tex_container2 = tex_complex.TexComplex(
        death_chance_tex2,
        centered= True,
        location = (7, -5, 0),
        scale = 0.67
    )
    death_tex_container2.add_to_blender(
        appear_frame = blob2_intro_start + 48,
        animate = True
    )
    birth_tex_container2.disappear(disappear_frame = blob2_intro_end)
    death_tex_container2.disappear(disappear_frame = blob2_intro_end)'''

    '''initial_creature_count = 10
    initial_creatures = []
    for i in range(initial_creature_count):
        new_creature = creature.Creature(color = 'creature_color_2', shape = 'shape2')
        initial_creatures.append(new_creature)
    blob2_sim = drawn_world.DrawnWorld(
        name = 'blob2_sim',
        location = [7.5, -2.5, 0],
        scale = 0.6,
        appear_frame = blob2_sim_start,
        start_delay = 0,
        duration = scene_end - blob2_sim_start,
        initial_creatures = initial_creatures,
        #save = True,
        #load = 'prep_chars_test',
        gene_updates = [
            ['color', 'creature_color_2', 'birth_modifier', 100, 0],
            ['shape', 'shape2', 'birth_modifier', 1, 0],
            ['size', '1', 'birth_modifier', 1, 0],
            ['color', 'creature_color_2', 'replication_modifier', 0, 0],
            ['color', 'creature_color_2', 'death_modifier', 10, 0],
        ],
        counter_alignment = 'top_left'
    )'''

    ##Create blender-side objects and manipulate
    blob2.add_to_blender(
        appear_frame = blob2_intro_start,
        animate = True
    )
    '''blob2.move_to(
        start_frame = blob2_intro_end - OBJECT_APPEARANCE_TIME,
        end_frame = blob2_intro_end,
        new_location = (11, 4.5, 0),
        new_scale = [2] * 3,
    )'''
    '''blob2_sim.add_counter(
        color = 'creature_color_2',
        label = '\\text{Total: }'
    )
    blob2_sim.add_counter(
        color = 'creature_color_2',
        label = '\\text{Average: }',
        average = True
    )'''

    '''birth_chance_info2 = tex_bobject.TexBobject('\\text{Birth chance: } 10\\%')
    blob2_sim.add_info(birth_chance_info2)

    death_chance_info2 = tex_bobject.TexBobject('\\text{Survival chance: } 99\\%')
    blob2_sim.add_info(death_chance_info2)

    blob2_sim.add_to_blender(
        appear_frame = blob2_sim_start,
        animate = True
    )'''

    '''bun = import_object('stanford_bunny', 'creatures', scale = 8)
    torus = import_object('torus', 'primitives', scale = 60, location = (0, 0, 40))
    form_bun = bobject.MeshMorphBobject(name = 'form_bun')
    form_bun.add_subbobject_to_series(torus)
    form_bun.add_subbobject_to_series(bun)

    form_bun.add_to_blender(appear_frame = 0, animate = False)

    form_bun.morph_bobject(0, 1, 20, 60, dissolve_time = 30)

    #Spiiiiiiiin
    form_bun.ref_obj.rotation_euler = (0, -math.pi / 2, 0)
    form_bun.ref_obj.keyframe_insert(data_path="rotation_euler", frame = 0)
    form_bun.ref_obj.rotation_euler = (0, math.pi / 2, 0)
    form_bun.ref_obj.keyframe_insert(data_path="rotation_euler", frame = 100)'''

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
    initialize_blender(total_duration = 350)

    rhs = tex_bobject.TexBobject(
        "B + (R-D) \\times N",
        "1 + (R-D) \\times N",
        "1 + (R-0.1) \\times N",
        "1 + (0-0.1) \\times N",
        centered = True
    )
    equals = tex_bobject.TexBobject(
        "\!=",
        centered = True
    )
    lhs = tex_bobject.TexBobject(
        "\\Delta",
        centered = True
    )
    equation = tex_complex.TexComplex(
        lhs, equals,
        rhs,
        location = (0, 0, 0),
        scale = 1,
        centered = True
    )
    equation.add_annotation(
        targets = [
            2, #tex_bobject
            [
                [0, 3, 3],  #form, first char, last char
                [1, 2, 6],
                [2, 2, 8],
            ],
        ],
        labels = [
            ['\\text{Reproduction}', '\\text{chance per}', '\\text{creature}'],
            ['\\text{Net change}', '\\text{per creature}', 'banana'],
            ['\\text{Net change}', '\\text{per creature}']
        ],
        alignment = 'top',
        angle = math.pi / 6
    )
    equation.add_to_blender(
        appear_frame = 0,
        animate = False
    )

    rhs.morph_figure(1, start_frame = 60)
    rhs.morph_figure(2, start_frame = 120)

    equation.move_to(
        new_location = (1, 1, 1),
        start_frame = 180
    )

    '''rhs.imported_svg_data[rhs.paths[0]]['curves'][2].add_to_blender(
        appear_frame = 0
    )'''
    #obj = rhs.imported_svg_data[rhs.paths[0]]['curves'][2].objects[0]
    #bpy.context.scene.objects.link(obj)

    '''net_bracket = gesture.Gesture(
        gesture_series = [
            {
                'type': 'bracket',
                'points': {
                    'annotation_point': (8.5, 5/3, 0),
                    'left_point': (6.8, 2/3, 0),
                    'right_point': (10.4, 2/3, 0)
                }
            },
            {
                'type': 'bracket',
                'points': {
                    'annotation_point': (8.5, 5/3, 0),
                    'left_point': (6.55, 2/3, 0),
                    'right_point': (10.4, 2/3, 0)
                }
            },
        ],
        color = 'color2'
    )
    net_bracket.add_to_blender(appear_frame = 120)'''


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
    duration = get_total_duration(scenes)
    initialize_blender(total_duration =  duration)

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
    initialize_blender()

    parent = bobject.Bobject()
    parent.add_subbobject_to_series(import_object('H2O'))
    parent.add_subbobject_to_series(import_object('sucrose'))
    parent.add_to_blender()

    #parent.morph_bobject(1, 50, 70)

def graph_test():
    initialize_blender(total_duration = 1200)

    '''def func(x):
        return 10 * math.sin(3*x) * math.cos(x / 6) #+ math.sin(5*x)
        #return 3 + 5 * x - 1.5 * x * x + (x ** 3) / 9.2
        #return 10 - (9 * (10 ** (10 - x)) / (10 ** 10))
    '''

    def func(x):
        return x / 5 #+ math.sin(5*x)
        #return 3 + 5 * x - 1.5 * x * x + (x ** 3) / 9.2
        #return 10 - (9 * (10 ** (10 - x)) / (10 ** 10))
        #return - x * x / 10 + 10

    initial_creature_count = 10
    initial_creatures = []
    for i in range(initial_creature_count):
        new_creature = creature.Creature(color = 'creature_color_1', shape = 'shape1')
        initial_creatures.append(new_creature)
    pop = population.Population(
        duration = DEFAULT_WORLD_DURATION,
        initial_creatures = initial_creatures,
        gene_updates = [
            ['color', 'creature_color_1', 'birth_modifier', 50, 0],
            ['shape', 'shape1', 'birth_modifier', 1, 0],
            ['size', '1', 'birth_modifier', 1, 0],
            ['color', 'creature_color_1', 'replication_modifier', 0, 0],
            ['color', 'creature_color_1', 'death_modifier', 5, 0],
        ]
    )
    num_sims = 5
    funcs = []
    for i in range(num_sims):
        pop.simulate()
        funcs.append(pop.get_creature_count_by_t())
        #funcs.append(pop.get_creature_count_by_t())

    graph = graph_bobject.GraphBobject(
        *funcs,
        x_range = [0, 100],
        y_range = [0, 20],
        tick_step = [20, 5],
        width = 10,
        height = 10,
        x_label = '\\text{Time}',
        x_label_pos = 'along',
        y_label = 'N',
        y_label_pos = 'along',
        location = (-6.5, 0, 0),
        centered = True,
        arrows = True
    )
    graph.add_to_blender(curve_colors = 'fade_secondary')
    graph.animate_function_curve(
        start_frame = 60,
        end_frame = 180,
        uniform_along_x = True,
        index = 0
    )
    graph.animate_all_function_curves(
        start_frame = 180,
        end_frame = 1060,
        uniform_along_x = True,
        skip = 1,
        start_window = 0.5
    )
    try:
        appear_coord = [0, funcs[0][0], 0]
    except:
        appear_coord = [0, funcs[0](0), 0]
    point = graph.add_point_at_coord(
        coord = appear_coord,
        appear_frame = 30,
        axis_projections = True,
        track_curve = 0
    )
    graph.animate_point(
        end_coord = [100, 0, 0],
        start_frame = 60,
        end_frame = 180,
        point = point
    )
    #graph.morph_curve(1, start_frame = 360)
    '''graph.multi_animate_point(
        point = point,
        start_frame = 480,
        x_of_t = x_of_t
    )'''

    """def func2(x): return 5 - x / 2
    graph2 = graph_bobject.GraphBobject(
        func2,
        x_range = [0, 20],
        y_range = [-10, 10],
        tick_step = [5, 5],
        width = 10,
        height = 10,
        x_label = 'N',
        x_label_pos = 'end',
        y_label = '\\Delta_{expected}',
        y_label_pos = 'end',
        location = (6.5, 0, 0),
        centered = True,
        arrows = True
    )
    graph2.add_to_blender()
    appear_coord = [func[0], func2(func[0]), 0]
    point2 = graph2.add_point_at_coord(
        coord = appear_coord,
        appear_frame = 30,
        axis_projections = True,
        track_curve = True
    )
    graph2.multi_animate_point(
        start_frame = 60,
        point = point2,
        x_of_t = func
    )"""

def bcard():
    initialize_blender()
    primer = import_object('logo')

    primer.add_to_blender(appear_frame = 0)

def main():
    #test_object()
    #execute_and_time(test_sim())
    #execute_and_time(tex_test())
    #test_molecule()
    #morph_test()
    #graph_test()
    #color_test()
    #bcard()
    #gesture_test()

    draw_scenes_from_file(replication_only)

    #print_time_report()
    finish_noise()


if __name__ == "__main__":
    main()
