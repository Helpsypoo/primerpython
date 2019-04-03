import collections
import math
from random import random, uniform, randrange
import bpy

import imp
#import scene
#imp.reload(scene)
from scene import Scene

import bobject
imp.reload(bobject)
#import svg_bobject
#imp.reload(svg_bobject)
import tex_bobject
imp.reload(tex_bobject)
#import tex_complex
#imp.reload(tex_complex)
#import gesture
#imp.reload(gesture)
#import graph_bobject
#imp.reload(graph_bobject)



import blobject
imp.reload(blobject)
#from blobject import Blobject

import market_sim
imp.reload(market_sim)
import drawn_market
imp.reload(drawn_market)


import helpers
imp.reload(helpers)
from helpers import *

import constants
imp.reload(constants)
#from constants import SIM_DIR


class InclusiveFitness(Scene):
    def __init__(self):
        self.subscenes = collections.OrderedDict([
            ('card', {'duration': 10000})
        ])
        super().__init__()

    def play(self):
        super().play()

        #self.intro()
        #self.price_limits()
        self.sim_rules_1()

    def intro(self):
        pass

    def price_limits(self):
        cam_bobj, cam_swivel = cam_and_swivel(
            cam_location = [0, 0, 32.8],
            cam_rotation_euler = [0, 0, 0],
            cam_name = "Camera Bobject",
            swivel_location = [0, 0, 0],
            swivel_rotation_euler = [0, 0, 0],
            swivel_name = 'Cam swivel',
            #control_sun = True
        )
        cam_swivel.add_to_blender(appear_time = -1, animate = False)

        #Show seller
        seller = market_sim.Agent(
            type = 'seller',
            price_limit = 20,
            interaction_mode = 'seller_asks_buyer_decides'
        )
        b = drawn_market.DrawnAgent(
            scale = 4,
            agent = seller,
            display_mode = 'camera_right',
            wiggle = False,
            location = [0, -1, 0]
        )
        seller_tex = tex_bobject.TexBobject(
            '\\text{Seller}',
            location = [0, 1.25, 0],
            centered = True,
            scale = 0.5
        )
        b.add_subbobject(seller_tex)
        b.add_to_blender(appear_time = 0, subbobject_timing = OBJECT_APPEARANCE_TIME)
        r = import_object(
            'rocket', 'misc',
            location = [-1, -0.4, 0],
            scale = 0.5
        )
        r.ref_obj.parent = b.ref_obj
        r.tweak_colors_recursive()
        r.add_to_blender(appear_time = 1)
        #b.hold_object(start_time = 1)

        #Show buyer
        buyer = market_sim.Agent(
            type = 'buyer',
            price_limit = 40,
            interaction_mode = 'seller_asks_buyer_decides'
        )
        o = drawn_market.DrawnAgent(
            scale = 4,
            location = [4.5, -1, 0],
            wiggle = False,
            agent = buyer,
            display_mode = 'camera_left'
            #mat = 'creature_color4',
        )
        b.move_to(start_time = 4, new_location = [-4.5, -1, 0])

        buyer_tex = tex_bobject.TexBobject(
            '\\text{Buyer}',
            '\\text{Buyer 1}',
            location = [0, 1.25, 0],
            centered = True,
            scale = 0.5
        )
        o.add_subbobject(buyer_tex)
        o.add_to_blender(appear_time = 4, subbobject_timing = OBJECT_APPEARANCE_TIME)
        o.move_head(
            start_time = 5,
            end_time = 7,
            rotation_quaternion = [1, 0.1, -0.3, -0.1]
        )

        #Make seller display
        b.make_display(
            appear_time = 8,
            no_rot = True
        )
        b.move_to(
            start_time = 8,
            new_location = [-6, -1, 0],
            new_angle = [0, 10 * math.pi / 180, 0]
        )
        o.move_to(start_time = 8, new_location = [6, -1, 0])

        b.add_expected_price(appear_time = 9, price = 20)

        b.move_expected_price(start_time = 10, price = 30)
        b.nod_yes(start_time = 10, end_time = 11)

        b.move_expected_price(start_time = 12, price = 10)
        b.shake_no(start_time = 13, end_time = 14)
        b.move_expected_price(start_time = 14, price = 30)

        #Make buyer display
        o.make_display(
            appear_time = 15,
            no_rot = True
        )
        b.move_to(
            start_time = 15,
            new_location = [-7, -1, 0],
        )
        o.move_to(start_time = 15, new_location = [7, -1, 0])

        o.add_expected_price(appear_time = 16, price = 40)

        o.move_expected_price(start_time = 17, price = 30)
        o.nod_yes(start_time = 17, end_time = 18)

        o.move_expected_price(start_time = 19, price = 50)
        o.shake_no(start_time = 20, end_time = 21)

        o.move_expected_price(start_time = 21, price = 30)


        b.move_expected_price(start_time = 22, price = 40)
        o.move_expected_price(start_time = 22, price = 40)
        b.move_expected_price(start_time = 22.5, end_time = 23.2, price = 20)
        o.move_expected_price(start_time = 22.5, end_time = 23.2, price = 20)
        b.move_expected_price(start_time = 23.2, end_time = 23.9, price = 40)
        o.move_expected_price(start_time = 23.2, end_time = 23.9, price = 40)
        b.move_expected_price(start_time = 23.9, price = 30)
        o.move_expected_price(start_time = 23.9, price = 30)

        #Zoom in to talk about surplus
        cam_bobj.move_to(
            new_location = [0, -1.5, 12.5],
            start_time = 25
        )

        price_tex_scale = 0.5
        buyer_price_tex = tex_bobject.TexBobject(
            '\\$ 40',
            location = [0, 0.93, 0],
            centered = True,
            scale = price_tex_scale
        )
        buyer_price_tex.add_to_blender(appear_time = 26)
        seller_price_tex = tex_bobject.TexBobject(
            '\\$ 20',
            location = [0, -1.65, 0],
            centered = True,
            scale = price_tex_scale
        )
        seller_price_tex.add_to_blender(appear_time = 27)

        mid_price_tex = tex_bobject.TexBobject(
            '\\$ 30',
            location = [0, -0.35, 0],
            centered = True,
            scale = price_tex_scale
        )
        mid_price_tex.add_to_blender(appear_time = 28)
        r.move_to(
            new_location = [4.53, -0.4, 0.76],
            start_time = 28,
            end_time = 29
        )


        buyer_price_tex.pulse(start_time = 30, duration_time = 1)
        mid_price_tex.pulse(start_time = 31, duration_time = 1)
        o.highlight_surplus(
            start_time = 32,
            price = 30
        )

        seller_price_tex.pulse(start_time = 33, duration_time = 1)
        mid_price_tex.pulse(start_time = 34, duration_time = 1)
        b.highlight_surplus(
            start_time = 35,
            price = 30
        )

        surp = tex_bobject.TexBobject(
            '\\text{\"Surplus\"}',
            centered = True,
            location = [-2.86, 0.7, 0]
        )
        surp.add_to_blender(appear_time = 37)

        #Zoom back out
        to_disappear = [surp, buyer_price_tex, seller_price_tex, mid_price_tex,
                        o.expected_price_indicator, b.expected_price_indicator]
        for thing in to_disappear:
            thing.disappear(disappear_time = 40)
        cam_bobj.move_to(
            new_location = [0, 0, 32.8],
            start_time = 40
        )

        r.move_to(
            new_location = [-1, -0.4, 0],
            start_time = 41
        )
        b.hide_surplus(start_time = 41)
        o.hide_surplus(start_time = 41)

        #Show second buyer
        cam_bobj.move_to(
            new_location = [3.86, 0, 40.85],
            start_time = 43
        )
        buyer2 = market_sim.Agent(
            type = 'buyer',
            price_limit = 35,
            interaction_mode = 'seller_asks_buyer_decides'
        )
        o2 = drawn_market.DrawnAgent(
            scale = 4,
            location = [17.5, -1, 0],
            wiggle = True,
            agent = buyer2,
            display_mode = 'camera_left'
            #mat = 'creature_color4',
        )

        buyer_tex2 = tex_bobject.TexBobject(
            '\\text{Buyer 2}',
            location = [0, 1.25, 0],
            centered = True,
            scale = 0.5
        )
        o2.add_subbobject(buyer_tex2)
        o2.add_to_blender(appear_time = 45, subbobject_timing = OBJECT_APPEARANCE_TIME)
        buyer_tex.morph_figure(1, start_time = 45)

        o2.make_display(
            appear_time = 46,
            no_rot = True
        )

        to_disappear = [b, o, o2]
        for i, thing in enumerate(to_disappear):
            thing.disappear(disappear_time = 50 - (len(to_disappear) - 1 - i) * 0.05)

    def sim_rules_1(self):
        cam_bobj, cam_swivel = cam_and_swivel(
            cam_location = [0, 0, 34],
            cam_rotation_euler = [0, 0, 0],
            cam_name = "Camera Bobject",
            swivel_location = [0, 0, 0],
            swivel_rotation_euler = [74 * math.pi / 180, 0, 0],
            swivel_name = 'Cam swivel',
            #control_sun = True
        )
        cam_swivel.add_to_blender(appear_time = -1, animate = False)

        new_sim = True
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
            num_sessions = 3
            for i in range(num_sessions):
                new_agents = []
                print("Running session " + str(i))
                save = False
                if i == num_sessions - 1:
                    save = True
                sim.new_session(save = save, new_agents = new_agents)
                #print(sim.sessions[-1])
        else:
            sim = 'MARKET20190329T154933'

        animate = True
        if animate:
            market = drawn_market.DrawnMarket(
                sim = sim,
                location = [0, 0, 0]
            )
            market.add_to_blender(appear_time = 0)
            market.animate_sessions(start_time = 7)
