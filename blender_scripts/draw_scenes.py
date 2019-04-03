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

import recurring_assets
imp.reload(recurring_assets)
from recurring_assets import *

import population
imp.reload(population)
from population import *

import gesture
imp.reload(gesture)
from gesture import *

import tex_complex
imp.reload(tex_complex)
from tex_complex import TexComplex

import blobject
imp.reload(blobject)
from blobject import Blobject

import supply_and_demand
imp.reload(supply_and_demand)

import market_sim
imp.reload(market_sim)

import drawn_market
imp.reload(drawn_market)

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
    #BUT WAIT. I can put stacks of pngs straight into premiere.
    scn.render.image_settings.color_depth = '16'
    scn.render.image_settings.color_mode = 'RGBA'
    scn.cycles.film_transparent = True

    #Set to 60 fps
    bpy.ops.script.execute_preset(
        filepath="C:\\Program Files\\Blender Foundation\\Blender\\2.79\\scripts\\presets\\framerate\\60.py",
        menu_idname="RENDER_MT_framerate_presets"
    )

    #Idfk how to do manipulate the context
    '''for area in bpy.context.screen.areas:
        if area.type == 'TIMELINE':
            bpy.context.area = area
            bpy.context.space_data.show_seconds = True'''

    #The line below makes it so Blender doesn't apply gamma correction. For some
    #reason, Blender handles colors differently from how every other program
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

def is_scene(obj):
    #print('checking scene')
    #if "TextScene" in str(obj):
    if not inspect.isclass(obj):
        #print('  not class')
        return False
    if not issubclass(obj, Scene):
        print(obj)
        #print('  not subclass of scene')
        return False
    if obj == Scene:
        #print(obj)
        #print('  is scene class itself')
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

def tex_test():
    initialize_blender(total_duration = 100)

    '''message = tex_bobject.TexBobject(
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

    message.disappear(disappear_time = 3.5)'''

    t = tex_bobject.TexBobject(
        '\\curvearrowleft'
    )
    t.add_to_blender(appear_time = 0)

    print_time_report()

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

def test():
    initialize_blender()

    """
    sim = market_sim.Market(
        num_buyers = 1,
        num_sellers = 2,
        #interaction_mode = 'negotiate',
        #interaction_mode = 'walk',
        interaction_mode = 'seller_asks_buyer_decides',
        initial_price = 50,
        session_mode = 'rounds_w_concessions',
        #session_mode = 'rounds',
        #session_mode = 'one_shot',
        fluid_sellers = True
    )
    num_sessions = 200
    for i in range(num_sessions):
        print("Running session " + str(i))
        sim.new_session()
        #print(sim.sessions[-1])

    for i, session in enumerate(sim.sessions):
        print('Session ' + str(i))
        print(' Completed transactions: ' + str(session.num_transactions) + ' Sellers: ' + str(session.num_sellers) + ' Price: ' + str(session.avg_price))

        ordered_bids = sorted([x.goal_prices[i] for x in session.buyers])
        #ordered_bids.reverse()
        print(ordered_bids)
        ordered_asks = sorted([x.goal_prices[i] for x in session.sellers])
        print(ordered_asks)

        goal_prices = []
        for transaction in session.meetings:
            print(transaction.transaction_price)
            try:
                goal_prices.append([transaction.buyer.goal_prices[i], transaction.seller.goal_prices[i]])
            except:
                print(i)
                print(len(transaction.buyer.goal_prices))
                print(len(transaction.seller.goal_prices))
                raise()
        print(' ' + str(goal_prices))

        '''for agent in sim.agents:
            print(len(agent.goal_prices))'''

    ordered_bids = sorted([x.price_limit for x in sim.agents if x.type == 'buyer'])
    ordered_bids.reverse()
    print(ordered_bids)
    ordered_asks = sorted([x.price_limit for x in sim.agents if x.type == 'seller'])
    print(ordered_asks)



    '''for i, [bid, ask] in enumerate(zip(ordered_bids, ordered_asks)):
        if bid >= ask:
            continue
        else:
            print(i-1, ordered_bids[i-1], ordered_asks[i-1])
            print(i, bid, ask)
            print(i+1, ordered_bids[i+1], ordered_asks[i+1])
            break'''

    """

    '''agent = market_sim.Agent(
        type = 'seller',
        price_limit = 10,
        interaction_mode = 'seller_asks_buyer_decides'
    )
    d_agent = drawn_market.DrawnAgent(agent = agent)
    d_agent.add_to_blender(appear_time = 1)

    d_agent.make_display(appear_time = 3)
    d_agent.add_price_line(price = 45, appear_time = 5, emote = True)
    d_agent.move_price_line(price = 25, start_time = 7, emote = True)

    d_agent.add_expected_price(price = 25, appear_time = 9)
    d_agent.move_expected_price(price = 15, start_time = 11)

    d_agent.highlight_surplus(price = 25, start_time = 13, end_time = 15)'''

    new_sim = False
    if new_sim:
        sim = market_sim.Market(
            #num_initial_buyers = 1,
            #num_initial_sellers = 1,
            #interaction_mode = 'negotiate',
            #interaction_mode = 'walk',
            buyer_limits = [40],
            seller_limits = [20],
            interaction_mode = 'seller_asks_buyer_decides',
            initial_price = 30,
            session_mode = 'rounds_w_concessions',
            #session_mode = 'rounds',
            #session_mode = 'one_shot',
            fluid_sellers = True
        )
        num_sessions = 5
        for i in range(num_sessions):
            new_agents = []
            '''if i == 2:
                new_seller = market_sim.Agent(
                    type = 'seller',
                    interaction_mode = sim.interaction_mode,
                    initial_price = sim.sessions[-1].rounds[-1][-1].transaction_price,
                    price_limit = 29
                )
                new_agents.append(new_seller)
            if i == 3:
                new_buyer = market_sim.Agent(
                    type = 'buyer',
                    interaction_mode = sim.interaction_mode,
                    initial_price = sim.sessions[-1].rounds[-1][-1].transaction_price,
                    price_limit = 29
                )
                new_agents.append(new_buyer)'''
            '''if i > 0:
                new_seller = market_sim.Agent(
                    type = 'seller',
                    interaction_mode = sim.interaction_mode,
                    initial_price = sim.sessions[-1].rounds[-1][-1].transaction_price,
                    price_limit = 4 + 2 * i
                )
                new_agents.append(new_seller)
                new_buyer = market_sim.Agent(
                    type = 'buyer',
                    interaction_mode = sim.interaction_mode,
                    initial_price = sim.sessions[-1].rounds[-1][-1].transaction_price,
                    price_limit = 50 - 2 * i
                )
                new_agents.append(new_buyer)'''
            print("Running session " + str(i))
            save = False
            if i == num_sessions - 1:
                save = True
            sim.new_session(save = save, new_agents = new_agents)
            #print(sim.sessions[-1])
    else:
        #Three total
        #sim = 'MARKET20190327T161915'
        #12 total
        #sim = 'MARKET20190327T222513'
        #1 on 1
        #sim = 'MARKET20190328T165425'
        #2 on 1
        #sim = 'MARKET20190329T150237'
        #2 on 3
        sim = 'MARKET20190329T154933'

    '''
    #print('baanasdf')
    for i, [bid, ask] in enumerate(zip(ordered_bids, ordered_asks)):
        if bid >= ask:
            continue
        else:
            print(i-1, ordered_bids[i-1], ordered_asks[i-1])
            print(i, bid, ask)
            print(i+1, ordered_bids[i+1], ordered_asks[i+1])
            break
    '''

    show_graph = True
    if show_graph:
        graph = drawn_market.MarketGraph(
            arrows = False,
            padding = 0,
            centered = True,
            sim = sim,
            location = [6, 0, 0],
            scale = 0.5,
            display_arrangement = 'buyer_seller',
            show_axes = False
        )


        num_sessions = 30
        for i in range(num_sessions):
            new_agents = []
            if i == 0:
                new_agents.append(
                    market_sim.Agent(
                        type = 'buyer',
                        interaction_mode = graph.sim.interaction_mode,
                        initial_price = graph.sim.sessions[-1].rounds[-1][-1].transaction_price,
                        price_limit = 20
                    )
                )
            print("Running session " + str(i))
            save = False
            if i == num_sessions - 1:
                save = True
            graph.sim.new_session(save = save, new_agents = new_agents)

        graph.add_to_blender(appear_time = 0)
        #graph.add_agent(agent = sim.agents_lists[0][0], start_time = 0)
        #graph.update_agent_display(start_time = 5, session_index = 0)
        #graph.display_arrangement = 'superimposed'
        #graph.update_agent_display(start_time = 3)

        #graph.add_expected_prices(index = 0, start_time = 6)

        #for i in range(num_sessions):
        #    graph.highlight_surpluses(index = i + 1, start_time = 7 + i)
        #    graph.move_expected_prices(index = i + 1, start_time = 7 + i + 0.5)
        #    graph.hide_surpluses(start_time = 5 + i + 0.5)

    animate = True
    if animate:
        if show_graph:
            sim = graph.sim
        market = drawn_market.DrawnMarket(
            sim = sim,
            location = [-6, 0, 0]
        )
        if show_graph:
            market.linked_graph = graph
        market.add_to_blender(appear_time = 0)
        market.animate_sessions(start_time = 7)

    #print()
    #print()
    #for list in market.sim.agents_lists:
    #    print(' ' + str(list))
    #print()
    #print()
    #print([x.agent for x in graph.buyer_bobjects + graph.seller_bobjects])
    #print()
    #print([x.agent for x in market.drawn_buyers + market.drawn_sellers])

    summary = False
    if summary and new_sim:
        try:
            iterable = enumerate(sim.sessions)
        except:
            iterable = enumerate(market.sim.sessions)

        for i, session in iterable:
            print('Session ' + str(i))
            print(' Completed transactions: ' + str(session.num_transactions) + ' Sellers: ' + str(session.num_sellers) + ' Price: ' + str(session.avg_price))

            ordered_bids = sorted([x.goal_prices[i] for x in session.buyers])
            ordered_bids.reverse()
            print(' New banana ' + str(ordered_bids))
            ordered_asks = sorted([x.goal_prices[i] for x in session.sellers])
            print(' New banana ' + str(ordered_asks))

            goal_prices = []
            for round in session.rounds:
                goal_prices = []
                for transaction in round:
                    #print(transaction.transaction_price)
                    try:
                        goal_prices.append([transaction.buyer.goal_prices[i], transaction.seller.goal_prices[i]])
                    except:
                        print(i)
                        print(len(transaction.buyer.goal_prices))
                        print(len(transaction.seller.goal_prices))
                        raise()
                print(' ' + str(goal_prices))

            '''for agent in sim.agents:
                print(len(agent.goal_prices))'''

        ordered_bids = sorted([x.price_limit for x in sim.agents_lists[-1] if x.type == 'buyer'])
        ordered_bids.reverse()
        print(ordered_bids)
        ordered_asks = sorted([x.price_limit for x in sim.agents_lists[-1] if x.type == 'seller'])
        print(ordered_asks)

def main():
    """Use this as a test scene"""
    #tex_test()
    """"""

    #test()
    #draw_scenes_from_file(scds, clear = False)
    draw_scenes_from_file(supply_and_demand)

    print_time_report()
    finish_noise()

if __name__ == "__main__":
    try:
        main()
    except:
        print_time_report()
        finish_noise(error = True)
        raise()
