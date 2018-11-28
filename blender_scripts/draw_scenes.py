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

import natural_sim
imp.reload(natural_sim)
from natural_sim import *

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

import fecal_transplant
imp.reload(fecal_transplant)
from fecal_transplant import *

import natural_selection
imp.reload(natural_selection)
from natural_selection import *

import scds
imp.reload(scds)
from scds import *

import population
imp.reload(population)
from population import *

import gesture
imp.reload(gesture)
from gesture import *

import tex_complex
imp.reload(tex_complex)
from tex_complex import TexComplex

from helpers import *

def initialize_blender(total_duration = DEFAULT_SCENE_DURATION, clear_blender = True):
    #clear objects and materials
    #Reading the homefile would likely by faster, but it
    #sets the context to None, which breaks a bunch of
    #other stuff down the line. I don't know how to make the context not None.
    #bpy.ops.wm.read_homefile()
    if clear_blender == True:
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


    scn.gravity = (0, 0, -9.81)

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

    """swatch1 = import_object('xyplane', 'primitives', name = 'swatch1', location = (-6, 0, 0), scale = 1.5)
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
    swatch5.add_to_blender()"""

    b = import_object(
        'boerd_blob', 'creatures',
    )
    apply_material(b.ref_obj.children[0].children[0], 'creature_color3')

    b.add_to_blender(appear_time = 0)
    b.color_shift(
        color = COLORS_SCALED[6],
        start_time = 4,
        duration_time = None,
        shift_time = 240,
        obj = b.ref_obj.children[0].children[0]
    )
    b.color_shift(
        color = COLORS_SCALED[4],
        start_time = 8,
        duration_time = None,
        shift_time = 240,
        obj = b.ref_obj.children[0].children[0]
    )
    b.color_shift(
        color = COLORS_SCALED[3],
        start_time = 12,
        duration_time = None,
        shift_time = 240,
        obj = b.ref_obj.children[0].children[0]
    )
    b.color_shift(
        color = COLORS_SCALED[5],
        start_time = 16,
        duration_time = None,
        shift_time = 240,
        obj = b.ref_obj.children[0].children[0]
    )

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

    message = tex_bobject.TexBobject(
        '\\text{You\'re}',
        '\\text{the}',
        '\\text{best!}',
        centered = True,
        scale = 8,
        typeface = 'arial'
    )
    message.add_to_blender(appear_time = 0)

    message.morph_figure('next', start_time = 1)

    message.morph_figure('next', start_time = 2)

    message.disappear(disappear_time = 3.5)

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

def draw_scenes_from_file(script_file, clear = True):
    #This function is meant to process many scenes at once.
    #Most scenes end up being large enough where it doesn't make sense to have
    #more than one in blender at once, so this is obsolete and will
    #break if you try to process more than one scene at a time.
    scenes = get_scene_object_list(script_file)
    print(scenes)
    duration = get_total_duration(scenes)
    initialize_blender(total_duration = duration, clear_blender = clear)

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

    g = graph_bobject.GraphBobject(
        #location = [-5, 0, 0],
        centered = True,
        x_range = 2,
        tick_step = 1/2,
        include_y = False
    )

    g.add_to_blender(appear_time = 0)

    g.add_point_at_coord(
        appear_time = 1,
        coord = [5, 5, 5]
    )

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

def nat_sim_test():
    initialize_blender()

    initial_creatures = []
    for i in range(40):
        altruist = False
        if i % 5 == 0:
            altruist = True
        cre = natural_sim.Creature(altruist = altruist)
        initial_creatures.append(cre)

    sim = natural_sim.DrawnNaturalSim(
        scale = 1,
        food_count = 50,
        #initial_creatures = initial_creatures,
        #sim = 'NAT20181126T094348',
        location = [-6.5, 0, 0],
        day_length_style = 'fixed_speed',
        #day_length_style = 'fixed_length'
        #mutation_switches = [False, False, False, False]
    )

    '''
    Notes
    - 30 food
     - 0.1 mutation chance
        - good, but takes 300+ gens
        - a bit hit-and-miss when starting at 0 kin distance
        - Distributed starting point
     - 0.3 mutation chance
        - Chaotic (two runs)
     - 0.5 mutation chance
        - Spiked past 1.2 and returned to 0.6-7
        - A bit chaotic, not clearly adaptive
     - 1.0 mutation chance - Went extinct twice
    - 50 food
     - 0.1 mutation chance - seems actually to not be adaptive over 300 gens
    '''

    #sim.sim.mutation_switches = [True, True, True]
    #sim.sim.food_count = 10

    sim_length = 500
    for i in range(sim_length):
        save = False
        filename = None
        #filename = 'f' + str(sim.sim.food_count) + '_' + \
        #            str(sim.sim.mutation_switches) + '_' + \
        #            str(len(sim.sim.date_records))
        if i == sim_length - 1:
            save = True
            #if (i+1) % 50 == 0:
            #save = True
            #filename = 'f' + str(sim.sim.food_count) + '_' + \
            #            str(sim.sim.mutation_switches) + '_' + \
            #            str(len(sim.sim.date_records))
        if i == 10:
            #sim.sim.mutation_switches = [True, False, False]
            print()
        if i == 30:
            #sim.sim.mutation_switches = [True, True, True]
            print()
        #if i < 180 and i % 2 == 0:
        #    sim.sim.food_count -= 1
        #    print(' Food count now ' + str(sim.sim.food_count))
        if i == 50:
            print()

        sim.sim.sim_next_day(save = save, filename = filename)

    g = graph_bobject.GraphBobject3D(
        x_range = [0, 2],
        y_range = [0, 2],
        z_range = [0, 2],
        x_label = '\\text{Size}',
        y_label = '\\text{Speed}',
        z_label = '\\text{Sense}',
        width = 10,
        height = 10,
        depth = 10,
        location = [8, 8, 4],
        rotation_euler = [math.pi / 2, 0, 0],
        centered = True,
        tick_step = 0.5
    )
    #g.add_to_blender(appear_time = 1)
    #Graphs have many tex_bobjects, whose speed is sensitive to the number of object in
    #Blender at the moment, so it's good to add the graph to blender before the sim.

    '''sim.add_to_blender(
        appear_time = 1,
        start_day = 199,
        end_day = 199
    )'''

    cres_with_points = []
    cre_counts = []
    records = sim.sim.date_records
    time = 2 #start time
    print(len(records))
    print()
    avgs_size = []
    avgs_kin = []
    tots_alt = []
    prop_alt = []
    for date in range(len(records)):
        #Add count at date to list, for the counter tex_bobject
        if date == 10:
            pass
            #print()

        cre_counts.append(str(len(records[date]['creatures'])))
        print('Creatures on day ' + str(date) + ': ' + str(cre_counts[-1]))
        tot_size = 0
        tot_spd = 0
        tot_sense = 0
        tot_kin = 0
        tot_alt = 0
        tot = 0
        max_sense = -math.inf
        min_sense = math.inf
        for cre in records[date]['creatures']:
            tot_size += cre.size
            tot_spd += cre.speed
            tot_sense += cre.sense
            tot_kin += cre.kin_radius
            tot_alt += cre.altruist
            tot += 1
            if cre.sense > max_sense:
                max_sense = cre.sense
            if cre.sense < min_sense:
                min_sense = cre.sense
        if tot > 0: #Avoid error on extinction
            avg_size = tot_size / len(records[date]['creatures'])
            avg_spd = tot_spd / len(records[date]['creatures'])
            avg_sense = tot_sense / len(records[date]['creatures'])
            avg_kin = tot_kin / len(records[date]['creatures'])
            print(" Avgs for today are (size, speed, sense) " + \
                        str(round(avg_size, 2)) + ' ' + \
                        str(round(avg_spd, 2)) + ' ' + \
                        str(round(avg_sense, 2))
                 )
            print(" Avg kin radius: " + str(avg_kin))
            avgs_size.append(avg_size)
            avgs_kin.append(avg_kin)
            tots_alt.append(tot_alt)
            prop_alt.append(tot_alt / tot)
        if date == 19:
            print( 'Max sense: ' + str(max_sense))
            print( 'Min sense: ' + str(min_sense))

    kin_graph = graph_bobject.GraphBobject(
        #prop_alt,
        avgs_kin,
        location = [0, 0, 0],
        centered = True,
        x_range = len(tots_alt),
        y_range = 1,
        width = 20,
        height = 15,
        tick_step = [20, 0.2],
        #overlay_functions = True
    )
    kin_graph.add_to_blender(appear_time = 0)
    #kin_graph.add_new_function_and_curve(
    #    avgs_size,
    #    color = 4
    #)

    graph_point_leftovers = []
    '''
    for date in range(len(records)):
        if date == len(records) - 1:
            #print()
            #print("The date is " + str(date))
            #print(" There are " + str(len(records[date]['creatures'])) + " creatures today")
            #print(" " + str(len(cres_with_points)) + " creatures have points now")
            print("Updating graph for day " + str(date))


            #Add count at date to list, for the counter tex_bobject
            #cre_counts.append(str(len(records[date]['creatures'])))

            #Delete points for creatures the died
            to_delete = []
            for cre in cres_with_points:
                #print(' A creature has a point')
                if cre not in records[date]['creatures']:
                    #print(' taking point from creature')
                    cre.point.disappear(
                        disappear_time = time,
                        #Will need duration in actual scene
                    )
                    to_delete.append(cre)
            for cre in to_delete:
                cres_with_points.remove(cre)
            #print(' Now ' + str(len(cres_with_points)) + " cres have points")

            #Add points for new creatures
            for cre in records[date]['creatures']:
                #print(" There's a cre")
                if cre not in cres_with_points:
                    #print(' Giving a point')
                    point = g.add_point_at_coord(
                        coord = [
                            cre.size + uniform(-0.03, 0.03),
                            cre.speed + uniform(-0.03, 0.03),
                            cre.sense + uniform(-0.03, 0.03)
                        ],
                        appear_time = time,
                        #Will need duration in actual scene
                    )
                    apply_material(
                        point.ref_obj.children[0],
                        cre.bobject.ref_obj.children[0].children[0].active_material
                    )
                    cre.point = point
                    cres_with_points.append(cre)
                    #print(' Now ' + str(len(cres_with_points)) + " cres have points")

            #Add time after day
            time += records[date]['anim_durations']['dawn'] + \
                    records[date]['anim_durations']['morning'] + \
                    records[date]['anim_durations']['day'] + \
                    records[date]['anim_durations']['evening'] + \
                    records[date]['anim_durations']['night']
    '''

    #print(cre_counts)
    """
    print('Here comes count_tex')
    count_tex = tex_bobject.TexBobject(*cre_counts, transition_type = 'instant')
    print('Okay, done with count_tex')
    count_lab = tex_bobject.TexBobject('\\text{Number: }')
    counter = tex_complex.TexComplex(
        count_lab, count_tex,
        location = [-5, 0, 10],
        rotation_euler = [math.pi / 2, 0, 0]
    )
    counter.add_to_blender(appear_time = 1)

    #Perhaps not the most efficient, but another loop through the dates to
    #animate the creature counter
    time = 2
    print()
    print(len(cre_counts))
    for date in range(len(records)):
        print(date)
        if date > 0:
            count_tex.morph_figure('next', start_time = time)

        #Add time after day
        time += records[date]['anim_durations']['dawn'] + \
                records[date]['anim_durations']['morning'] + \
                records[date]['anim_durations']['day'] + \
                records[date]['anim_durations']['evening'] + \
                records[date]['anim_durations']['night']
    """


def main():
    """Use this as a test scene"""
    #tex_test()
    """"""

    nat_sim_test()
    #graph_test()
    #draw_scenes_from_file(vn, clear = False)
    #draw_scenes_from_file(scds)

    print_time_report()
    finish_noise()

if __name__ == "__main__":
    try:
        main()
    except:
        print_time_report()
        finish_noise(error = True)
        raise()
