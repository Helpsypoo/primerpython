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
import tex_complex
imp.reload(tex_complex)
import gesture
imp.reload(gesture)
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


class SupplyAndDemand(Scene):
    def __init__(self):
        self.subscenes = collections.OrderedDict([
            ('card', {'duration': 10000})
        ])
        super().__init__()

    def play(self):
        super().play()

        #self.intro()
        #self.price_limits()
        #self.sim_rules_1()
        #self.price_inertia()
        #self.sim_rules_2()
        #self.actual_sim()
        self.arguing()

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
        b.add_to_blender(appear_time = 26, subbobject_timing = OBJECT_APPEARANCE_TIME)
        r = import_object(
            'rocket', 'misc',
            location = [-1, -0.4, 0],
            scale = 0.5
        )
        r.ref_obj.parent = b.ref_obj
        r.tweak_colors_recursive()
        r.add_to_blender(appear_time = 29.7)
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
        o.add_to_blender(appear_time = 31.5, subbobject_timing = OBJECT_APPEARANCE_TIME)
        o.move_head(
            start_time = 33.5,
            end_time = 35.2,
            rotation_quaternion = [1, 0.1, -0.3, -0.1]
        )

        b_display_appear_time = 38.5
        #Make seller display
        b.make_display(
            appear_time = b_display_appear_time,
            no_rot = True
        )
        b.move_to(
            start_time = b_display_appear_time,
            new_location = [-6, -1, 0],
            new_angle = [0, 10 * math.pi / 180, 0]
        )
        o.move_to(start_time = b_display_appear_time, new_location = [6, -1, 0])

        b.add_expected_price(appear_time = 55, price = 20)

        b.move_expected_price(start_time = 55.1, price = 30)
        b.nod_yes(start_time = 51.5, end_time = 53)

        b.move_expected_price(start_time = 53.5, price = 10)
        b.shake_no(start_time = 54.2, end_time = 56)
        b.move_expected_price(start_time = 59, price = 20)

        #Make buyer display
        b_display_appear_time = 62.5
        o.make_display(
            appear_time = b_display_appear_time,
            no_rot = True
        )
        b.move_to(
            start_time = b_display_appear_time,
            new_location = [-7, -1, 0],
        )
        o.move_to(start_time = b_display_appear_time, new_location = [7, -1, 0])

        o.add_expected_price(appear_time = 64.5, price = 40)

        o.move_expected_price(start_time = 65.7, price = 30)
        o.nod_yes(start_time = 66.2, end_time = 18)

        o.move_expected_price(start_time = 68, price = 50)
        o.shake_no(start_time = 68.4, end_time = 21)

        o.move_expected_price(start_time = 70, price = 40)


        b.move_expected_price(start_time = 73.5, price = 40)
        o.move_expected_price(start_time = 73.5, price = 40)
        b.move_expected_price(start_time = 74, end_time = 74.7, price = 20)
        o.move_expected_price(start_time = 74, end_time = 74.7, price = 20)
        b.move_expected_price(start_time = 74.7, end_time = 75.4, price = 40)
        o.move_expected_price(start_time = 74.7, end_time = 75.4, price = 40)
        b.move_expected_price(start_time = 75.4, price = 30)
        o.move_expected_price(start_time = 75.4, price = 30)

        #Zoom in to talk about surplus
        cam_bobj.move_to(
            new_location = [0, -1.5, 12.5],
            start_time = 79.5,
            end_time = 80.5
        )

        price_tex_scale = 0.5
        buyer_price_tex = tex_bobject.TexBobject(
            '\\$ 40',
            location = [0, 0.93, 0],
            centered = True,
            scale = price_tex_scale
        )
        buyer_price_tex.add_to_blender(appear_time = 82)
        seller_price_tex = tex_bobject.TexBobject(
            '\\$ 20',
            location = [0, -1.65, 0],
            centered = True,
            scale = price_tex_scale
        )
        seller_price_tex.add_to_blender(appear_time = 84.1)

        mid_price_tex = tex_bobject.TexBobject(
            '\\$ 30',
            location = [0, -0.35, 0],
            centered = True,
            scale = price_tex_scale
        )
        mid_price_tex.add_to_blender(appear_time = 87.7)
        r.move_to(
            new_location = [4.53, -0.4, 0.76],
            start_time = 87.7,
            end_time = 88.7
        )


        buyer_price_tex.pulse(start_time = 90, duration_time = 2.5)
        mid_price_tex.pulse(start_time = 92.5, duration_time = 2.5)
        o.dur4(
            start_time = 96,
            price = 30
        )

        seller_price_tex.pulse(start_time = 99, duration_time = 1)
        mid_price_tex.pulse(start_time = 100, duration_time = 1)
        b.highlight_surplus(
            start_time = 101.1,
            price = 30
        )

        surp = tex_bobject.TexBobject(
            '\\text{\"Surplus\"}',
            centered = True,
            location = [-2.86, 0.7, 0]
        )
        surp.add_to_blender(appear_time = 113)

        b.hide_surplus(start_time = 130.5)
        o.hide_surplus(start_time = 130.5)
        o.highlight_surplus(
            start_time = 131,
            price = 30
        )
        b.highlight_surplus(
            start_time = 131,
            price = 30
        )

        #Zoom back out
        to_disappear = [surp, buyer_price_tex, seller_price_tex, mid_price_tex,
                        o.expected_price_indicator, b.expected_price_indicator]
        for thing in to_disappear:
            thing.disappear(disappear_time = 140)
        cam_bobj.move_to(
            new_location = [0, 0, 32.8],
            start_time = 139.5,
            end_time = 140.5
        )

        r.move_to(
            new_location = [-1, -0.4, 0],
            start_time = 140.5
        )
        b.hide_surplus(start_time = 140.5)
        o.hide_surplus(start_time = 140.5)

        #Show second buyer
        cam_bobj.move_to(
            new_location = [3.86, 0, 40.85],
            start_time = 143,
            end_time = 144
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
        o2.add_to_blender(appear_time = 144.5, subbobject_timing = OBJECT_APPEARANCE_TIME)
        buyer_tex.morph_figure(1, start_time = 144.5)

        o2.make_display(
            appear_time = 149.5,
            no_rot = True
        )

        to_disappear = [b, o, o2]
        for i, thing in enumerate(to_disappear):
            thing.disappear(disappear_time = 170 - (len(to_disappear) - 1 - i) * 0.05)

    def sim_rules_1(self):
        cam_bobj, cam_swivel = cam_and_swivel(
            cam_location = [0, 4.75, 8],
            cam_rotation_euler = [0, 0, 0],
            cam_name = "Camera Bobject",
            swivel_location = [0, 0, 0],
            swivel_rotation_euler = [74 * math.pi / 180, 0, 0],
            swivel_name = 'Cam swivel',
            #control_sun = True
        )
        cam_swivel.add_to_blender(appear_time = -1, animate = False)

        new_sim = False
        if new_sim:
            sim = market_sim.Market(
                #num_initial_buyers = 1,
                #num_initial_sellers = 1,
                #interaction_mode = 'negotiate',
                #interaction_mode = 'walk',
                buyer_limits = [50, 45, 40, 35, 30],
                seller_limits = [15, 20, 25, 30, 35],
                interaction_mode = 'seller_asks_buyer_decides',
                initial_price = 32,
                session_mode = 'rounds_w_concessions',
                #session_mode = 'rounds',
                #session_mode = 'one_shot',
                fluid_sellers = False
            )
            num_sessions = 1
            for i in range(num_sessions):
                new_agents = []
                print("Running session " + str(i))
                save = False
                if i == num_sessions - 1:
                    save = True
                sim.new_session(save = save, new_agents = new_agents)
                #print(sim.sessions[-1])
        else:
            sim = 'sim_rules'

        animate = True
        if animate:
            market = drawn_market.DrawnMarket(
                sim = sim,
                location = [0, 0, 0],
                scale = 13,
                #phase_durations = {
                #    'seller_setup_anim_duration' : ROUND_MOVE_DURATION,
                #    'seller_setup_duration' : ROUND_MOVE_DURATION,
                #    'round_move_duration' : ROUND_MOVE_DURATION,
                #    'pause_before_exchange' : 0,
                #    'exchange_duration' : ROUND_MOVE_DURATION,
                #    'round_duration' : PAUSE_LENGTH,
                #    'buyer_return_anim_duration' : ROUND_MOVE_DURATION,
                #    'buyer_return_duration': ROUND_MOVE_DURATION,
                #    'price_adjust_anim_duration' : ROUND_MOVE_DURATION,
                #    'price_adjust_duration' : ROUND_MOVE_DURATION
                #},
            )
            market.phase_durations['seller_setup_duration'] = 5
            market.phase_durations['round_move_duration'] = 1
            market.phase_durations['pause_before_exchange'] = 15
            market.phase_durations['round_duration'] = 17
            #market.phase_durations['exchange_duration'] = 5
            #market.phase_durations['round_duration'] = 10
            market.add_to_blender(appear_time = 172)
            market.animate_sessions(start_time = 175)

            cam_bobj.move_to(
                new_location = [-1.64, 1.59, 29.72],
                start_time = 177,
                end_time = 179
            )
            cam_swivel.move_to(
                new_angle = [74 * math.pi / 180, 0, -39.4 * math.pi / 180],
                start_time = 177,
                end_time = 179
            )

            cam_bobj.move_to(
                new_location = [-4.56, 4.13, 9.09],
                start_time = 184,
                end_time = 185
            )
            cam_swivel.move_to(
                new_angle = [74 * math.pi / 180, 0, 6 * math.pi / 180],
                start_time = 184,
                end_time = 185
            )

            for agent in market.drawn_sellers + market.drawn_buyers:
                agent.expected_price_indicator.pulse(
                    start_time = 188,
                    duration_time = 1
                )
                agent.expected_price_indicator.pulse(
                    start_time = 189,
                    duration_time = 1
                )

    def price_inertia(self):
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

        blob_time = 193.75
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
            location = [-7, -1, 0]
        )
        seller_tex = tex_bobject.TexBobject(
            '\\text{Seller}',
            location = [0, 1.25, 0],
            centered = True,
            scale = 0.5
        )
        b.add_subbobject(seller_tex)
        b.add_to_blender(appear_time = blob_time, subbobject_timing = OBJECT_APPEARANCE_TIME)
        r = import_object(
            'rocket', 'misc',
            location = [-1, -0.4, 0],
            scale = 0.5
        )
        r.ref_obj.parent = b.ref_obj
        r.tweak_colors_recursive()
        r.add_to_blender(appear_time = 194)
        #b.hold_object(start_time = 1)

        #Show buyer
        buyer = market_sim.Agent(
            type = 'buyer',
            price_limit = 40,
            interaction_mode = 'seller_asks_buyer_decides'
        )
        o = drawn_market.DrawnAgent(
            scale = 4,
            location = [7, -1, 0],
            wiggle = False,
            agent = buyer,
            display_mode = 'camera_left'
            #mat = 'creature_color4',
        )

        buyer_tex = tex_bobject.TexBobject(
            '\\text{Buyer}',
            '\\text{Buyer 1}',
            location = [0, 1.25, 0],
            centered = True,
            scale = 0.5
        )
        o.add_subbobject(buyer_tex)
        o.add_to_blender(appear_time = blob_time, subbobject_timing = OBJECT_APPEARANCE_TIME)
        '''o.move_head(
            start_time = 5,
            end_time = 7,
            rotation_quaternion = [1, 0.1, -0.3, -0.1]
        )'''

        #Make seller display
        b.make_display(
            appear_time = 194,
            no_rot = True
        )
        b.add_expected_price(appear_time = 195, price = 30)

        #Make buyer display
        o.make_display(
            appear_time = 194,
            no_rot = True
        )

        o.add_expected_price(appear_time = 195, price = 30)

        #Zoom in to talk about surplus
        '''cam_bobj.move_to(
            new_location = [0, -1.5, 12.5],
            start_time = 25
        )'''

        price_tex_scale = 0.5
        buyer_price_tex = tex_bobject.TexBobject(
            '\\$ 40',
            location = [0, 0.93, 0],
            centered = True,
            scale = price_tex_scale
        )
        buyer_price_tex.add_to_blender(appear_time = 195)
        seller_price_tex = tex_bobject.TexBobject(
            '\\$ 20',
            location = [0, -1.65, 0],
            centered = True,
            scale = price_tex_scale
        )
        seller_price_tex.add_to_blender(appear_time = 195)

        mid_price_tex = tex_bobject.TexBobject(
            '\\$ 30',
            location = [0, -0.35, 0],
            centered = True,
            scale = price_tex_scale
        )
        mid_price_tex.add_to_blender(appear_time = 195)


        buyer_price_tex.pulse(start_time = 197.3, duration_time = 1)
        mid_price_tex.pulse(start_time = 199.6, duration_time = 1)

        b.move_expected_price(start_time = 202, price = 35)
        b.move_head(
            rotation_quaternion = [1, 0, 0.5, 0],
            start_time = 201,
            end_time = 205
        )
        b.show_mouth(start_time = 201)
        b.hide_mouth(start_time = 204)

        o.move_head(
            rotation_quaternion = [1, 0.1, -0.5, -0.1],
            start_time = 203,
            end_time = 206
        )
        o.angry_eyes(
            start_time = 203.75,
            end_time = None
        )

        to_disappear = [b, buyer_price_tex, seller_price_tex, mid_price_tex, o]
        for i, thing in enumerate(to_disappear):
            thing.disappear(disappear_time = 206.5 - (len(to_disappear) - 1 - i) * 0.05)

    def sim_rules_2(self):
        cam_bobj, cam_swivel = cam_and_swivel(
            cam_location = [0, 4.75, 8],
            cam_rotation_euler = [0, 0, 0],
            cam_name = "Camera Bobject",
            swivel_location = [0, 0, 0],
            swivel_rotation_euler = [74 * math.pi / 180, 0, 0],
            swivel_name = 'Cam swivel',
            #control_sun = True
        )
        cam_swivel.add_to_blender(appear_time = -1, animate = False)

        new_sim = False
        if new_sim:
            sim = market_sim.Market(
                #num_initial_buyers = 1,
                #num_initial_sellers = 1,
                #interaction_mode = 'negotiate',
                #interaction_mode = 'walk',
                buyer_limits = [50, 45, 40, 35, 30],
                seller_limits = [15, 20, 25, 30, 35],
                interaction_mode = 'seller_asks_buyer_decides',
                initial_price = 32,
                session_mode = 'rounds_w_concessions',
                #session_mode = 'rounds',
                #session_mode = 'one_shot',
                fluid_sellers = False
            )
            num_sessions = 1
            for i in range(num_sessions):
                new_agents = []
                print("Running session " + str(i))
                save = False
                if i == num_sessions - 1:
                    save = True
                sim.new_session(save = save, new_agents = new_agents)
                #print(sim.sessions[-1])
        else:
            sim = 'sim_rules'

        '''
            The day continues...: 3:26.5
                Return to view, no surplus yet
        ... Every rocket has been SOLD: 3:29
                Highlight surplus
        ... remaining buyers: 3:31
                Second round movement
        ... refused to BUY: 3:32
        ... all remaining sellers: 3:33.5
                second round sellers go home

        '''

        animate = True
        if animate:
            market = drawn_market.DrawnMarket(
                sim = sim,
                location = [0, 0, 0],
                scale = 13,
                #phase_durations = {
                #    'seller_setup_anim_duration' : ROUND_MOVE_DURATION,
                #    'seller_setup_duration' : ROUND_MOVE_DURATION,
                #    'round_move_duration' : ROUND_MOVE_DURATION,
                #    'pause_before_exchange' : 0,
                #    'exchange_duration' : ROUND_MOVE_DURATION,
                #    'round_duration' : PAUSE_LENGTH,
                #    'buyer_return_anim_duration' : ROUND_MOVE_DURATION,
                #    'buyer_return_duration': ROUND_MOVE_DURATION,
                #    'price_adjust_anim_duration' : ROUND_MOVE_DURATION,
                #    'price_adjust_duration' : ROUND_MOVE_DURATION
                #},
            )
            #market.phase_durations['seller_setup_duration'] = 5
            #market.phase_durations['round_move_duration'] = 1
            #market.phase_durations['pause_before_exchange'] = 15
            #market.phase_durations['round_duration'] = 17

            market.phase_durations['round_move_duration'] = 1
            market.phase_durations['pause_before_exchange'] = 2
            market.phase_durations['round_duration'] = 4
            market.phase_durations['buyer_return_anim_duration'] = 1
            market.phase_durations['buyer_return_duration'] = 8
            market.phase_durations['price_adjust_duration'] = 8

            market.add_to_blender(appear_time = 172)
            phase_duration_updates = [
                [
                    1,
                    {
                        'seller_setup_anim_duration' : 0.3,
                        'seller_setup_duration' : 0.3,
                        'round_move_duration' : 0.3,
                        'pause_before_exchange' : 0,
                        'exchange_duration' : 0.3,
                        'round_duration' : 0.6,
                        'buyer_return_anim_duration' : 0.3,
                        'buyer_return_duration': 0.6,
                        'price_adjust_anim_duration' : 0.3,
                        'price_adjust_duration' : 0.3
                    }
                ]
            ]
            market.animate_sessions(
                start_time = 204.5,
                phase_duration_updates = phase_duration_updates
            )

            cam_bobj.move_to(
                new_location = [-4.56, 4.13, 9.09],
                start_time = 184,
                end_time = 185
            )
            cam_swivel.move_to(
                new_angle = [74 * math.pi / 180, 0, 6 * math.pi / 180],
                start_time = 184,
                end_time = 185
            )

            cam_bobj.move_to(
                new_location = [0, 4.13, 22.83],
                start_time = 207.5,
                end_time = 208.5
            )
            cam_swivel.move_to(
                new_angle = [74 * math.pi / 180, 0, 0],
                start_time = 207.5,
                end_time = 208.5
            )

            cam_bobj.move_to(
                new_location = [0, 4.75, 8],
                start_time = 222,
                end_time = 223
            )
            cam_swivel.move_to(
                new_angle = [74 * math.pi / 180, 0, 0],
                start_time = 222,
                end_time = 223
            )

            cam_bobj.move_to(
                new_location = [0, -0.75, 34],
                start_time = 232,
                end_time = 233
            )
            cam_swivel.move_to(
                new_angle = [65 * math.pi / 180, 0, 0],
                start_time = 232,
                end_time = 233
            )

            for agent in market.drawn_sellers + market.drawn_buyers:
                agent.expected_price_indicator.pulse(
                    start_time = 188,
                    duration_time = 1
                )
                agent.expected_price_indicator.pulse(
                    start_time = 189,
                    duration_time = 1
                )


            market.disappear(
                disappear_time = 241.5
            )

    def actual_sim(self):
        cam_bobj, cam_swivel = cam_and_swivel(
            cam_location = [0, 2.5, 34],
            cam_rotation_euler = [0, 0, 0],
            cam_name = "Camera Bobject",
            swivel_location = [0, 0, 0],
            swivel_rotation_euler = [74 * math.pi / 180, 0, 0],
            swivel_name = 'Cam swivel',
            #control_sun = True
        )
        cam_swivel.add_to_blender(appear_time = -1, animate = False)

        '''
        4:01.5 - Sim rules 2 finishes disappearing.
        4:02 - Actual sim appears
        4:08 - Move sim over
        4:09 - Draw linked graph
        4:10.5 - Start sim
        4:26.5 - Add second buyer
        5:15.5 - Add second and third seller
        '''


        def demand_curve(x):
            #Quadratics that contain starting values,
            #and stays within the needed bounds,
            #and results in the possibility of all agents transacting if
            #forced
            return (x - 17) * (x - 1) / 2.9 + 40

        def supply_curve(x):
            if x > 9:
                x = 9 #Just be flat after 9
            return (x - 4) * (x + 4) / 3.4 + 20


        buyer_limits = [demand_curve(x) for x in range(10)]
        seller_limits = [supply_curve(x) for x in range(10)]

        new_sim = False
        add_to_sim = None #'two_on_one'
        two_one_index = 10
        two_three_index = two_one_index + 20
        three_each_index = two_three_index + 40
        three_each_high_index = three_each_index + 12
        three_each_low_index = three_each_high_index + 40
        ten_each_index = three_each_low_index + 35

        num_at_ten_each = 30
        num_sessions = ten_each_index + num_at_ten_each

        if new_sim:
            sim = market_sim.Market(
                #num_initial_buyers = 1,
                #num_initial_sellers = 1,
                #interaction_mode = 'negotiate',
                #interaction_mode = 'walk',
                buyer_limits = [buyer_limits.pop(1)],
                seller_limits = [seller_limits.pop(4)],
                interaction_mode = 'seller_asks_buyer_decides',
                initial_price = 30,
                session_mode = 'rounds_w_concessions',
                #session_mode = 'rounds',
                #session_mode = 'one_shot',
                fluid_sellers = True
            )
            #for i in range(num_sessions):
            for i in range(num_sessions):
                new_agents = []
                print("Running session " + str(i))
                if i == two_one_index:
                    new_buyer = market_sim.Agent(
                        type = 'buyer',
                        interaction_mode = sim.interaction_mode,
                        initial_price = sim.sessions[-1].rounds[-1][-1].transaction_price,
                        price_limit = buyer_limits.pop(1),
                    )
                    new_agents.append(new_buyer)
                if i == two_three_index:
                    new_seller = market_sim.Agent(
                        type = 'seller',
                        interaction_mode = sim.interaction_mode,
                        initial_price = sim.sessions[-1].rounds[-1][-1].transaction_price,
                        price_limit = seller_limits.pop(3),
                    )
                    new_agents.append(new_seller)
                    new_seller = market_sim.Agent(
                        type = 'seller',
                        interaction_mode = sim.interaction_mode,
                        initial_price = sim.sessions[-1].rounds[-1][-1].transaction_price,
                        price_limit = seller_limits.pop(4),
                        #price_limit = seller_limits.pop(3),
                    )
                    new_agents.append(new_seller)
                if i == three_each_index:
                    new_buyer = market_sim.Agent(
                        type = 'buyer',
                        interaction_mode = sim.interaction_mode,
                        initial_price = sim.sessions[-1].rounds[-1][-1].transaction_price,
                        price_limit = buyer_limits.pop(3),
                        #price_limit = buyer_limits.pop(6),
                    )
                    new_agents.append(new_buyer)
                if i == three_each_high_index:
                    for agent in sim.agents_lists[-1]:
                        agent.adjust_price(set_price = 32, edit_last = True)
                    sim.sessions[-1].next_expected_price = 32
                if i == three_each_low_index:
                    for agent in sim.agents_lists[-1]:
                        agent.adjust_price(set_price = 20, edit_last = True)
                    sim.sessions[-1].next_expected_price = 20
                if i == ten_each_index:
                    for j in range(7):
                        new_buyer = market_sim.Agent(
                            type = 'buyer',
                            interaction_mode = sim.interaction_mode,
                            initial_price = sim.sessions[-1].rounds[-1][-1].transaction_price,
                            price_limit = buyer_limits.pop(0),
                        )
                        new_agents.append(new_buyer)
                        new_seller = market_sim.Agent(
                            type = 'seller',
                            interaction_mode = sim.interaction_mode,
                            initial_price = sim.sessions[-1].rounds[-1][-1].transaction_price,
                            price_limit = seller_limits.pop(0),
                        )
                        new_agents.append(new_seller)
                save = False
                if i == num_sessions - 1:
                    save = True
                sim.new_session(save = save, new_agents = new_agents)
                #print(sim.sessions[-1])
        elif add_to_sim != None:
            sim = add_to_sim
            #initialize a drawnmarket just to load the previous market
            market = drawn_market.DrawnMarket(
                sim = sim,
                location = [-6, 0, 0],
                scale = 6.5
            )
            sim = market.sim

            #Pop the initial agents, which are already in the loaded sim
            buyer_limits.pop(1)
            seller_limits.pop(4)
            buyer_limits.pop(1)
            seller_limits.pop(3)
            seller_limits.pop(4)
            buyer_limits.pop(3)

            for i in range(ten_each_index, ten_each_index + num_at_ten_each):
                new_agents = []
                print("Running session " + str(i))
                if i == ten_each_index:
                    for j in range(7):
                        new_buyer = market_sim.Agent(
                            type = 'buyer',
                            interaction_mode = sim.interaction_mode,
                            initial_price = sim.sessions[-1].rounds[-1][-1].transaction_price,
                            price_limit = buyer_limits.pop(0),
                        )
                        new_agents.append(new_buyer)
                        new_seller = market_sim.Agent(
                            type = 'seller',
                            interaction_mode = sim.interaction_mode,
                            initial_price = sim.sessions[-1].rounds[-1][-1].transaction_price,
                            price_limit = seller_limits.pop(0),
                        )
                        new_agents.append(new_seller)
                save = False
                if i == ten_each_index + num_at_ten_each - 1:
                    save = True
                sim.new_session(save = save, new_agents = new_agents)
        else:
            sim = 'ten_each'

        show_graph = True
        if show_graph:
            graph = drawn_market.MarketGraph(
                #demand_curve, supply_curve,
                arrows = False,
                x_range = 10,
                y_range = 50,
                tick_step = [20, 10],
                x_label = "\\text{Quantity}",
                y_label = "\\text{Price}",
                y_label_pos = 'end',
                padding = 0,
                centered = True,
                sim = sim,
                location = [6.5, 0, 0],
                rotation_euler = [74 * math.pi / 180, 0, 0],
                scale = 0.9,
                display_arrangement = 'buyer_seller',
                show_axes = False,
                #overlay_functions = True,
            )


            '''num_sessions = 30
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
                graph.sim.new_session(save = save, new_agents = new_agents)'''

            graph.add_to_blender(appear_time = 249)

        animate = True
        if animate:
            if show_graph:
                sim = graph.sim
            market = drawn_market.DrawnMarket(
                sim = sim,
                location = [0, 0, 0],
                rotation_euler = [0, 0, 60 * math.pi / 180],
                scale = 9.5
            )
            if show_graph:
                market.linked_graph = graph
            #market.add_to_blender(appear_time = 0)
            unit = 0.3
            market.phase_durations = {
                'seller_setup_anim_duration' : unit,
                'seller_setup_duration' : 0,
                'round_move_duration' : unit,
                'pause_before_exchange' : 0,
                'exchange_duration' : unit,
                'round_duration' : 2 * unit,
                'buyer_return_anim_duration' : unit,
                'buyer_return_duration': unit,
                'price_adjust_anim_duration' : unit,
                'price_adjust_duration' : unit
            }

            market.add_to_blender(appear_time = 242)
            market.move_to(
                start_time = 248,
                new_location = [-6, 0, 0],
                new_scale = 6.5
            )
            cam_swivel.move_to(
                new_angle = [74 * math.pi / 180, 0, 0],
                start_time = 248
            )

            updates_2_on_1 = [
                [
                    two_one_index,
                    {
                        'seller_setup_anim_duration' : 0.5,
                        'seller_setup_duration' : 4.5,
                    }
                ],
                [
                    two_one_index + 1,
                    {
                        'seller_setup_anim_duration' : unit,
                        'seller_setup_duration' : 0,
                    }
                ],
                [
                    two_three_index - 1,
                    {
                        'buyer_return_duration': 16,
                    }
                ]
            ]
            unit = 0.1
            updates_2_on_3 = [
                [
                    two_three_index,
                    {
                        'seller_setup_anim_duration' : 0.5,
                        'seller_setup_duration' : 24,
                        'round_move_duration' : unit,
                        'pause_before_exchange' : 0,
                        'exchange_duration' : unit,
                        'round_duration' : 2 * unit,
                        'buyer_return_anim_duration' : unit,
                        'buyer_return_duration': unit,
                        'price_adjust_anim_duration' : unit,
                        'price_adjust_duration' : unit
                    }
                ],
                [
                    two_three_index + 1,
                    {
                        'seller_setup_anim_duration' : unit,
                        'seller_setup_duration' : 0,
                    }
                ],
                [
                    three_each_index - 1,
                    {
                        'buyer_return_duration': 12,
                    }
                ]
            ]
            unit = 0.2
            updates_3_on_3 = [
                [
                    three_each_index,
                    {
                        'seller_setup_anim_duration' : 0.5,
                        'seller_setup_duration' : 14,
                        'round_move_duration' : unit,
                        'pause_before_exchange' : 0,
                        'exchange_duration' : unit,
                        'round_duration' : 2 * unit,
                        'buyer_return_anim_duration' : unit,
                        'buyer_return_duration': unit,
                        'price_adjust_anim_duration' : unit,
                        'price_adjust_duration' : unit
                    }
                ],
                [
                    three_each_index + 1,
                    {
                        'seller_setup_anim_duration' : unit,
                        'seller_setup_duration' : 0,
                    }
                ],
                [
                    three_each_high_index - 1,
                    {
                        #'seller_setup_anim_duration' : 0.3,
                        #'seller_setup_duration' : 0,
                        #'round_move_duration' : 0.3,
                        #'pause_before_exchange' : 0,
                        #'exchange_duration' : 0.3,
                        #'round_duration' : 0.6,
                        #'buyer_return_anim_duration' : 0.3,
                        'buyer_return_duration': 9,
                        #'price_adjust_anim_duration' : 0.3,
                        #'price_adjust_duration' : unit
                    }
                ]
            ]
            unit = 0.05
            updates_3_on_3_high = [
                [
                    three_each_high_index,
                    {
                        'seller_setup_anim_duration' : 0.5,
                        'seller_setup_duration' : 0.5,
                        'round_move_duration' : unit,
                        'pause_before_exchange' : 0,
                        'exchange_duration' : unit,
                        'round_duration' : 2 * unit,
                        'buyer_return_anim_duration' : unit,
                        'buyer_return_duration': unit,
                        'price_adjust_anim_duration' : unit,
                        'price_adjust_duration' : unit
                    }
                ],
                [
                    three_each_high_index + 1,
                    {
                        'seller_setup_anim_duration' : unit,
                        'seller_setup_duration' : 0,
                        #'round_move_duration' : unit,
                        #'pause_before_exchange' : 0,
                        #'exchange_duration' : unit,
                        #'round_duration' : 2 * unit,
                        #'buyer_return_anim_duration' : unit,
                        #'buyer_return_duration': unit,
                        #'price_adjust_anim_duration' : unit,
                        #'price_adjust_duration' : unit
                    }
                ],
                [
                    three_each_low_index - 1,
                    {
                        #'seller_setup_anim_duration' : unit,
                        #'seller_setup_duration' : 0,
                        #'round_move_duration' :  unit,
                        #'pause_before_exchange' : 0,
                        #'exchange_duration' : unit,
                        #'round_duration' : 2 * unit,
                        #'buyer_return_anim_duration' : unit,
                        'buyer_return_duration': 3,
                        #'price_adjust_anim_duration' : unit,
                        #'price_adjust_duration' : unit
                    }
                ]
            ]
            updates_3_on_3_low = [
                [
                    three_each_low_index,
                    {
                        'seller_setup_anim_duration' : 0.5,
                        'seller_setup_duration' : 0.5,
                        'round_move_duration' : unit,
                        'pause_before_exchange' : 0,
                        'exchange_duration' : unit,
                        'round_duration' : 2 * unit,
                        'buyer_return_anim_duration' : unit,
                        'buyer_return_duration': unit,
                        'price_adjust_anim_duration' : unit,
                        'price_adjust_duration' : unit
                    }
                ],
                [
                    three_each_low_index + 1,
                    {
                        'seller_setup_anim_duration' : unit,
                        'seller_setup_duration' : 0,
                        #'round_move_duration' : unit,
                        #'pause_before_exchange' : 0,
                        #'exchange_duration' : unit,
                        #'round_duration' : 2 * unit,
                        #'buyer_return_anim_duration' : unit,
                        #'buyer_return_duration': unit,
                        #'price_adjust_anim_duration' : unit,
                        #'price_adjust_duration' : unit
                    }
                ],
                [
                    ten_each_index - 1,
                    {
                        #'seller_setup_anim_duration' : unit,
                        #'seller_setup_duration' : 0,
                        #'round_move_duration' : unit,
                        #'pause_before_exchange' : 0,
                        #'exchange_duration' : unit,
                        #'round_duration' : 2 * unit,
                        #'buyer_return_anim_duration' : unit,

                        'buyer_return_duration': 10,

                        #'price_adjust_anim_duration' : unit,
                        #'price_adjust_duration' : unit
                    }
                ]
            ]
            updates_ten_each = [
                [
                    ten_each_index,
                    {
                        'seller_setup_anim_duration' : 0.5,
                        'seller_setup_duration' : 2,
                        'round_move_duration' : unit,
                        'pause_before_exchange' : 0,
                        'exchange_duration' : unit,
                        'round_duration' : 2 * unit,
                        'buyer_return_anim_duration' : unit,
                        'buyer_return_duration': unit,
                        'price_adjust_anim_duration' : unit,
                        'price_adjust_duration' : unit
                    }
                ],
                [
                    ten_each_index + 1,
                    {
                        'seller_setup_anim_duration' : unit,
                        'seller_setup_duration' : 0,
                        #'round_move_duration' : unit,
                        #'pause_before_exchange' : 0,
                        #'exchange_duration' : unit,
                        #'round_duration' : 2 * unit,
                        #'buyer_return_anim_duration' : unit,
                        #'buyer_return_duration': unit,
                        #'price_adjust_anim_duration' : unit,
                        #'price_adjust_duration' : unit
                    }
                ],
                [
                    ten_each_index + num_at_ten_each,
                    {
                        #'seller_setup_anim_duration' : unit,
                        #'seller_setup_duration' : 0,
                        #'round_move_duration' : unit,
                        #'pause_before_exchange' : 0,
                        #'exchange_duration' : unit,
                        #'round_duration' : 2 * unit,
                        #'buyer_return_anim_duration' : unit,

                        'buyer_return_duration': 10,

                        #'price_adjust_anim_duration' : unit,
                        #'price_adjust_duration' : unit
                    }
                ]
            ]


            market.animate_sessions(
                start_time = 250.5,
                first_animated_session = 0,
                last_animated_session = two_one_index
            )
            market.animate_sessions(
                start_time = 266.5,
                first_animated_session = two_one_index,
                last_animated_session = two_three_index,
                phase_duration_updates = updates_2_on_1
            )
            market.animate_sessions(
                start_time = 315.5,
                first_animated_session = two_three_index,
                last_animated_session = three_each_index,
                phase_duration_updates = updates_2_on_3
            )
            market.animate_sessions(
                start_time = 379,
                graph_mode_changes = {
                    str(three_each_index) : ['stacked', 11],
                },
                first_animated_session = three_each_index,
                last_animated_session = three_each_high_index,
                phase_duration_updates = updates_3_on_3
            )
            market.animate_sessions(
                start_time = 424.5,
                first_animated_session = three_each_high_index,
                last_animated_session = three_each_low_index,
                phase_duration_updates = updates_3_on_3_high
            )
            market.animate_sessions(
                start_time = 439.5,
                first_animated_session = three_each_low_index,
                last_animated_session = ten_each_index,
                phase_duration_updates = updates_3_on_3_low
            )
            market.animate_sessions(
                start_time = 461,
                graph_mode_changes = {
                    str(ten_each_index + 9) : ['superimposed', 0],
                },
                first_animated_session = ten_each_index,
                #last_animated_session = None,
                phase_duration_updates = updates_ten_each
            )

        #Point at surplus
        scale = 2
        tail1 = [8 + 1/3, 11.5]
        head1 = [8 + 1/3, 7.5]
        surp_arrow = gesture.Gesture(
            gesture_series = [
                {
                    'type': 'arrow',
                    'points': {
                        'tail': (tail1[0] / scale, tail1[1] / scale, 0),
                        'head': (head1[0] / scale, head1[1] / scale, 0)
                    }
                }
            ],
            scale = scale,
        )
        surp_arrow.ref_obj.parent = graph.ref_obj
        surp_arrow.add_to_blender(appear_time = 305)
        surp_arrow.disappear(disappear_time = 312.5)

        #point at new seller value bars
        scale = 2
        tail1 = [9, 9.6]
        head1 = [9, 5.6]
        tail2 = [5, 8]
        head2 = [5, 4]
        surp_arrow = gesture.Gesture(
            gesture_series = [
                {
                    'type': 'arrow',
                    'points': {
                        'tail': (tail1[0] / scale, tail1[1] / scale, 0),
                        'head': (head1[0] / scale, head1[1] / scale, 0)
                    }
                },
                {
                    'type': 'arrow',
                    'points': {
                        'tail': (tail2[0] / scale, tail2[1] / scale, 0),
                        'head': (head2[0] / scale, head2[1] / scale, 0)
                    }
                }
            ],
            scale = scale,
        )
        surp_arrow.ref_obj.parent = graph.ref_obj
        surp_arrow.add_to_blender(appear_time = 325)
        surp_arrow.morph_figure(1, start_time = 331.5)
        surp_arrow.disappear(disappear_time = 335)

        #point at buyer surpluses
        scale = 2
        tail1 = [3, 11.8]
        head1 = [3, 8.4]
        tail2 = [1, 10.7]
        head2 = [1, 7.3]
        surp_arrow1 = gesture.Gesture(
            gesture_series = [
                {
                    'type': 'arrow',
                    'points': {
                        'tail': (tail1[0] / scale, tail1[1] / scale, 0),
                        'head': (head1[0] / scale, head1[1] / scale, 0)
                    }
                }
            ],
            scale = scale,
        )
        surp_arrow2 = gesture.Gesture(
            gesture_series = [
                {
                    'type': 'arrow',
                    'points': {
                        'tail': (tail2[0] / scale, tail2[1] / scale, 0),
                        'head': (head2[0] / scale, head2[1] / scale, 0)
                    }
                }
            ],
            scale = scale,
        )
        surp_arrow1.ref_obj.parent = graph.ref_obj
        surp_arrow1.add_to_blender(appear_time = 370)
        surp_arrow1.disappear(disappear_time = 376)
        surp_arrow2.ref_obj.parent = graph.ref_obj
        surp_arrow2.add_to_blender(appear_time = 370)
        surp_arrow2.disappear(disappear_time = 376)


        #point at extreme buyers and sellers
        scale = 2
        tail1 = [11, 19.6]
        head1 = [9, 16.2]
        tail2 = [11, 9.1]
        head2 = [9, 5.7]
        surp_arrow1 = gesture.Gesture(
            gesture_series = [
                {
                    'type': 'arrow',
                    'points': {
                        'tail': (tail1[0] / scale, tail1[1] / scale, 0),
                        'head': (head1[0] / scale, head1[1] / scale, 0)
                    }
                }
            ],
            scale = scale,
        )
        surp_arrow2 = gesture.Gesture(
            gesture_series = [
                {
                    'type': 'arrow',
                    'points': {
                        'tail': (tail2[0] / scale, tail2[1] / scale, 0),
                        'head': (head2[0] / scale, head2[1] / scale, 0)
                    }
                }
            ],
            scale = scale,
        )
        surp_arrow1.ref_obj.parent = graph.ref_obj
        surp_arrow1.add_to_blender(appear_time = 415.5)
        surp_arrow1.disappear(disappear_time = 422)
        surp_arrow2.ref_obj.parent = graph.ref_obj
        surp_arrow2.add_to_blender(appear_time = 417.5)
        surp_arrow2.disappear(disappear_time = 422)

        #Point again at seller bar
        surp_arrow2.add_to_blender(appear_time = 432)
        surp_arrow2.disappear(disappear_time = 436)

        #Point again at buyer bar
        surp_arrow1.add_to_blender(appear_time = 442)
        surp_arrow1.disappear(disappear_time = 428)

        equil = tex_bobject.TexBobject(
            '\\text{"Equilibrium"}',
            centered = True,
            location = [-6, 0, 8.5],
            rotation_euler = [74 * math.pi / 180, 0, 0],
            scale = 2
        )
        equil.add_to_blender(appear_time = 446.75)

        qs = tex_bobject.TexBobject('\\text{Quantity supplied}')
        eq = tex_bobject.TexBobject('\!=')
        qd = tex_bobject.TexBobject('\\text{Quantity demanded}')
        qseqd = tex_complex.TexComplex(
            qs, eq, qd,
            location = [-6, 0, 6.5],
            rotation_euler = [74 * math.pi / 180, 0, 0],
            scale = 0.9,
            centered = True
        )
        qseqd.add_to_blender(
            appear_time = 455.5,
            subbobject_timing = [0, 60, 120]
        )

        qseqd.arrange_tex_bobjects(start_time = 460)

        #Wiggle those willing to transact
        to_wiggle = [
            graph.seller_bobjects[0],
            graph.seller_bobjects[1],
            graph.buyer_bobjects[0],
            graph.buyer_bobjects[1],
        ]
        for thing in to_wiggle:
            thing.wobble(
                start_time = 450.5,
                end_time = 451.5,
            )

        #Wiggle suppliers
        to_wiggle = [
            graph.seller_bobjects[0],
            graph.seller_bobjects[1],
        ]
        for thing in to_wiggle:
            thing.wobble(
                start_time = 455.5,
                end_time = 456.5,
            )

        #Wiggle demanders
        to_wiggle = [
            graph.buyer_bobjects[0],
            graph.buyer_bobjects[1],
        ]
        for thing in to_wiggle:
            thing.wobble(
                start_time = 457.25,
                end_time = 458.25,
            )

        #graph.display_arrangement = 'stacked'
        graph.move_to(
            start_time = 390,
            new_location = [7.5, 0, -3],
            new_scale = 0.65
        )

        graph.move_to(
            start_time = 470.25,
            end_time = 471.5,
            new_location = [8, 0, -0.6],
            new_scale = 0.9
        )

        graph.add_axes()
        graph.add_subbobjects(appear_time = 480)

        graph.add_new_function_and_curve(
            demand_curve,
            color = 4
        )
        graph.add_new_function_and_curve(
            supply_curve,
            color = 3
        )

        graph.animate_function_curve(
            start_time = 481,
            end_time = 483,
            index = 0
        )
        graph.animate_function_curve(
            start_time = 484.5,
            end_time = 486.5,
            index = 1
        )

        cam_swivel.move_to(
            new_angle = [74 * math.pi / 180, 0, -5 * math.pi / 180],
            start_time = 493,
            end_time = 499
        )
        cam_swivel.move_to(
            new_angle = [74 * math.pi / 180, 0, 0 * math.pi / 180],
            start_time = 499,
            end_time = 505
        )

        to_disappear = [graph, market, equil, qseqd]
        for thing in to_disappear:
            thing.disappear(disappear_time = 505)

    def arguing(self):
        g = blobject.Blobject(
            mat = 'creature_color7',
            location = [6, 0, 0],
            scale = 5,
            wiggle = False
        )
        g.add_to_blender(appear_time = 505.5)
        g.move_to(
            new_angle = [0, -math.pi / 3, 0],
            start_time = 506.25
        )
        g.angry_eyes(start_time = 506.25)
        g.blob_wave(start_time = 506.25, duration = 4.75)

        r = blobject.Blobject(
            mat = 'creature_color6',
            location = [-6, 0, 0],
            scale = 5,
            wiggle = False
        )
        r.add_to_blender(appear_time = 505.5)
        r.move_to(
            new_angle = [0, math.pi / 3, 0],
            start_time = 506.25
        )
        r.angry_eyes(start_time = 506.25)
        r.blob_wave(start_time = 506.25, duration = 4.75)

        g.move_to(
            new_angle = [0, 0, 0],
            start_time = 511
        )
        r.move_to(
            new_angle = [0, 0, 0],
            start_time = 511
        )

        g.normal_eyes(start_time = 520.5)
        r.normal_eyes(start_time = 520.5)

        g.move_to(
            new_angle = [0, -math.pi / 3, 0],
            start_time = 523
        )
        r.move_to(
            new_angle = [0, math.pi / 3, 0],
            start_time = 522
        )

        r.hold_object(start_time = 525)
        g.move_head(
            start_time = 526.5,
            rotation_quaternion = [1, -0.1, 0, -0.1]
        )

        r.disappear(disappear_time = 529)
        g.disappear(disappear_time = 529)
