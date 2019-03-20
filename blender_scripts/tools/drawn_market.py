import bpy
import imp
from random import random, randrange, choice, gauss, uniform
#from copy import copy
#import pickle

import bobject
imp.reload(bobject)
from bobject import Bobject

from graph_bobject import GraphBobject

from blobject import Blobject

import helpers
imp.reload(helpers)
from helpers import *

import market_sim

BUYER_MAT = 'creature_color4'
SELLER_MAT = 'creature_color3'
BUYER_BAR_COLOR = COLORS_SCALED[3]
SELLER_BAR_COLOR = COLORS_SCALED[2]
BUYER_SURPLUS_COLOR = COLORS_SCALED[1]
SELLER_SURPLUS_COLOR = 'color2' #Yeah, these are in different formats. Eh.

BAR_WIDTH = 0.3
MAX_BAR_HEIGHT = 1.6
MAX_PRICE = market_sim.MAX_PRICE
BAR_THICKNESS = 0.08
BAR_BASE_LIP = 0.01
O_SLASH_SCALE = 0.5

BUYER_X_MAX = 0.7
BUYER_X_MIN = -0.7
BUYER_Y_MAX = -0.2
BUYER_Y_MIN = -0.7
AGENT_BASE_SCALE = 0.6
AGENT_HEIGHT_FACTOR = 0.8

PAUSE_LENGTH = 1
ROUND_MOVE_DURATION = 0.5

class DrawnAgent(Blobject):
    """docstring for DrawnAgent."""

    def __init__(
        self,
        agent = None,
        display_mode = 'camera_left',
        **kwargs
    ):

        if agent == None: #No reason to make default agents
            raise Warning('DrawnAgent needs agent')
        self.agent = agent

        if self.agent.type == 'seller':
            self.mat_string = SELLER_MAT
        if self.agent.type == 'buyer':
            self.mat_string = BUYER_MAT

        super().__init__(
            mat = self.mat_string,
            wiggle = True,
            **kwargs
        )

        self.display_mode = display_mode

        self.extra_top_cap = None
        self.extra_bot_cap = None

        #Toggle to control whether to move to lobby on a given animation
        self.was_just_meeting_seller = False

        self.good = None
        self.slash = None

    def add_to_blender(self, **kwargs):
        super().add_to_blender(**kwargs)

    def make_display(self, appear_time = None):
        if appear_time == None:
            raise Warning('make_display() needs appear_time')

        display_bobjects = []

        if self.display_mode == 'camera_left':
            self.bar_loc = [-1.5, -0.8, 0]
        elif self.display_mode == 'above':
            self.bar_loc = [0, 1, 0]
        elif self.display_mode == 'table':
            self.bar_loc = [0, 1, 0]

            table = import_object(
                'table', 'misc',
                rotation_euler = [0, math.pi / 2, math.pi / 2],
                location = [0.000584, -0.206953, 1.01555]
            )
            display_bobjects.append(table)

        else:
            raise Warning('Unrecognized display_mode')

        self.value_bar = import_object(
            'xy_plane_unrounded', 'primitives',
            location = self.bar_loc,
            name = 'value_display_bar',
            scale = [BAR_WIDTH, 0, 1]
        )

        #height of cap object is 0.5, then it's scaled by BAR_WIDTH when shown
        cap_height = 0.5 * BAR_WIDTH
        cap_scale_y = BAR_WIDTH
        height_after_cap = MAX_BAR_HEIGHT * self.agent.price_limit / MAX_PRICE
        height = height_after_cap - cap_height
        if height < 0:
            height = 0
            cap_scale_y = BAR_WIDTH * height_after_cap / cap_height

        self.bar_cap = import_object(
            'bar_cap', 'primitives',
            location = self.bar_loc,
            scale = [BAR_WIDTH, 0, 1],
            name = 'cap'
        )

        self.surplus_bar = import_object(
            'xy_plane_unrounded', 'primitives',
            location = self.bar_loc,
            name = 'surplus_display_bar',
            scale = [BAR_WIDTH, 0, 1]
        )

        for piece in [self.value_bar, self.surplus_bar, self.bar_cap]:
            apply_material(piece.ref_obj.children[0], 'color' + self.mat_string[-1])

        #Bar base
        base_bar_height = 0.02
        self.bar_base = import_object(
            'cylinder', 'primitives',
            #location = self.bar_loc,
            location = add_lists_by_element(self.bar_loc, [0, 0, -BAR_THICKNESS]),
            rotation_euler = [0, math.pi / 2, 0],
            name = 'bar_base',
            scale = [BAR_THICKNESS + 2 * BAR_BASE_LIP, base_bar_height, BAR_WIDTH * 1.2]
        )
        apply_material(self.bar_base.ref_obj.children[0], 'color2')

        display_bobjects += [
            self.value_bar,
            self.surplus_bar,
            self.bar_cap,
            self.bar_base
        ]

        self.display_container = bobject.Bobject(
            *display_bobjects,
            name = 'value_display'
        )
        self.display_container.add_to_blender(
            appear_time = appear_time - OBJECT_APPEARANCE_TIME / FRAME_RATE,
            subbobject_timing = OBJECT_APPEARANCE_TIME
        )

        constraint = self.display_container.ref_obj.constraints.new('CHILD_OF')
        #constraint.use_rotation_x = False
        #constraint.use_rotation_y = False
        #constraint.use_rotation_z = False
        #constraint.influence = 1
        constraint.target = self.ref_obj

        #expand bar_pieces
        self.value_bar.move_to(
            start_time = appear_time + OBJECT_APPEARANCE_TIME / FRAME_RATE,
            new_scale = [
                BAR_WIDTH,
                height,
                1
            ]
        )
        self.surplus_bar.move_to(
            start_time = appear_time + OBJECT_APPEARANCE_TIME / FRAME_RATE,
            new_location = add_lists_by_element(self.bar_loc, [0, height, 0]),
            new_scale = [BAR_WIDTH, 0, 1]
        )
        self.bar_cap.move_to(
            start_time = appear_time + OBJECT_APPEARANCE_TIME / FRAME_RATE,
            new_location = add_lists_by_element(self.bar_loc, [0, height, 0]),
            new_scale = [BAR_WIDTH, cap_scale_y, 1]
        )

    def add_price_line(self, price = 0, appear_time = None, emote = False):
        if appear_time == None:
            raise Warning('add_price_line() needs appear_time')

        #Price line
        price_line_width = 0.01
        height = MAX_BAR_HEIGHT * price / MAX_PRICE
        self.price_line = import_object(
            'cylinder', 'primitives',
            location = add_lists_by_element(self.bar_loc, [0, height, 0]),
            rotation_euler = [0, math.pi / 2, 0],
            name = 'price_line',
            scale = [price_line_width, price_line_width, BAR_WIDTH * 1.1]
        )
        apply_material(self.price_line.ref_obj.children[0], 'color6')

        self.display_container.add_subbobject(self.price_line)
        self.price_line.add_to_blender(appear_time = appear_time)

        if emote == True:
            self.price_reaction(price, start_time = appear_time + OBJECT_APPEARANCE_TIME / FRAME_RATE)

    def move_price_line(self, price = 0, start_time = None, emote = False):
        if start_time == None:
            raise Warning('move_price_line() needs start_time')

        height = MAX_BAR_HEIGHT * price / MAX_PRICE

        self.price_line.move_to(
            new_location = add_lists_by_element(self.bar_loc, [0, height, 0]),
            start_time = start_time
        )

        if emote == True:
            self.price_reaction(price = price, start_time = start_time + OBJECT_APPEARANCE_TIME / FRAME_RATE)

    def add_expected_price(self, price = 0, appear_time = None):
        if appear_time == None:
            raise Warning('add_expected_price() needs appear_time')

        #Price line
        height = MAX_BAR_HEIGHT * price / MAX_PRICE
        l_tri = import_object(
            'rounded_isosceles', 'primitives',
            location = [- BAR_WIDTH * 1.2, 0, 0],
            rotation_euler = [0, 0, -math.pi / 2],
            scale = 0.1
        )
        r_tri = import_object(
            'rounded_isosceles', 'primitives',
            location = [BAR_WIDTH * 1.2, 0, 0],
            rotation_euler = [0, 0, math.pi / 2],
            scale = 0.1
        )
        for tri in [l_tri, r_tri]:
            apply_material(tri.ref_obj.children[0], 'color2')


        self.expected_price_indicator = bobject.Bobject(
            l_tri, r_tri,
            location = add_lists_by_element(self.bar_loc, [0, height, 0]),
            #rotation_euler = [0, math.pi / 2, 0],
            name = 'expected_price',
        )
        #apply_material(self.expected_price_indicator.ref_obj.children[0], 'color6')

        self.display_container.add_subbobject(self.expected_price_indicator)
        self.expected_price_indicator.add_to_blender(
            appear_time = appear_time - OBJECT_APPEARANCE_TIME / FRAME_RATE,
            subbobject_timing = OBJECT_APPEARANCE_TIME
        )

    def move_expected_price(self, price = 0, start_time = None):
        if start_time == None:
            raise Warning('move_expected_price() needs start_time')

        height = MAX_BAR_HEIGHT * price / MAX_PRICE

        self.expected_price_indicator.move_to(
            new_location = add_lists_by_element(self.bar_loc, [0, height, 0]),
            start_time = start_time
        )

    def highlight_surplus(self, price = None, start_time = None, end_time = None):
        cap_height = 0.5 * BAR_WIDTH

        if self.agent.type == 'buyer':
            if price >= self.agent.price_limit:
                print('No surplus')
            else:
                price_height = MAX_BAR_HEIGHT * price / MAX_PRICE

                height_after_cap = MAX_BAR_HEIGHT * self.agent.price_limit / MAX_PRICE
                height = height_after_cap - cap_height


                if height - price_height >= 0:
                    self.value_bar.move_to(
                        start_frame = start_time * FRAME_RATE - 1,
                        end_frame = start_time * FRAME_RATE,
                        new_scale = [BAR_WIDTH, price_height, 1]
                    )
                    self.surplus_bar.move_to(
                        start_frame = start_time * FRAME_RATE - 1,
                        end_frame = start_time * FRAME_RATE,
                        new_location = add_lists_by_element(self.bar_loc, [0, price_height, 0]),
                        new_scale = [BAR_WIDTH, height - price_height, 1]
                    )
                else:
                    self.value_bar.move_to(
                        start_frame = start_time * FRAME_RATE,
                        new_scale = [BAR_WIDTH, price_height, 1]
                    )
                    cap_scale_y = BAR_WIDTH * (height_after_cap - price_height) / cap_height
                    self.bar_cap.move_to(
                        start_frame = start_time * FRAME_RATE,
                        new_scale = [BAR_WIDTH, cap_scale_y, 1],
                        new_location = add_lists_by_element(self.bar_loc, [0, price_height, 0])
                    )



                duration_time = None
                if end_time != None:
                    duration_time = end_time - start_time
                for bobj in [self.surplus_bar, self.bar_cap]:
                    bobj.color_shift(
                        start_time = start_time,
                        duration_time = duration_time,
                        color = BUYER_SURPLUS_COLOR
                    )


        if self.agent.type == 'seller':
            if price <= self.agent.price_limit:
                print('No surplus')
            else:
                limit_height = MAX_BAR_HEIGHT * self.agent.price_limit / MAX_PRICE
                price_height = MAX_BAR_HEIGHT * price / MAX_PRICE

                if self.extra_top_cap == None:
                    pass
                    self.extra_top_cap = import_object(
                        'bar_cap', 'primitives',
                        location = self.bar_loc,
                        scale = [BAR_WIDTH, 0, 1],
                        name = 'top_cap'
                    )
                    self.extra_bot_cap = import_object(
                        'bar_cap', 'primitives',
                        location = self.bar_loc,
                        scale = [BAR_WIDTH, 0, 1],
                        name = 'bot_cap'
                    )
                    for extra_cap in [self.extra_top_cap, self.extra_bot_cap]:
                        self.display_container.add_subbobject(extra_cap)
                        extra_cap.add_to_blender(
                            appear_frame = start_time * FRAME_RATE - 1,
                            transition_time = 1
                        )

                self.extra_top_cap.move_to(
                    start_time = start_time,
                    new_scale = [BAR_WIDTH, BAR_WIDTH, 1],
                    new_location = add_lists_by_element(self.bar_loc, [0, price_height - cap_height, 0]),
                )
                self.extra_bot_cap.move_to(
                    start_time = start_time,
                    new_scale = [BAR_WIDTH, -BAR_WIDTH, 1],
                    new_location = add_lists_by_element(self.bar_loc, [0, limit_height + cap_height, 0]),
                )
                self.surplus_bar.move_to(
                    start_time = start_time,
                    new_location = add_lists_by_element(self.bar_loc, [0, limit_height + cap_height, 0]),
                    new_scale = [BAR_WIDTH, price_height - limit_height - 2 * cap_height, 1],
                )

                for bobj in [self.surplus_bar, self.extra_top_cap, self.extra_bot_cap]:
                    apply_material(bobj.ref_obj.children[0], SELLER_SURPLUS_COLOR)

                '''#Change color. In this case, make color changes before and after
                #appearance
                duration_time = None
                if end_time != None:
                    duration_time = end_time - start_time + OBJECT_APPEARANCE_TIME / FRAME_RATE * 2
                for bobj in [self.surplus_bar, self.extra_top_cap, self.extra_bot_cap]:
                    bobj.color_shift(
                        start_time = start_time - OBJECT_APPEARANCE_TIME / FRAME_RATE,
                        duration_time = duration_time,
                        color = SELLER_SURPLUS_COLOR
                    )'''

                #Put away
                if end_time != None:
                    for piece in [self.extra_top_cap, self.extra_bot_cap, self.surplus_bar]:
                        piece.move_to(
                            start_time = end_time - OBJECT_APPEARANCE_TIME / FRAME_RATE,
                            new_location = add_lists_by_element(self.bar_loc, [0, limit_height, 0]),
                            new_scale = [BAR_WIDTH, 0, 1],
                        )

    def hide_surplus(self, start_time = None):
        if self.agent.type == 'buyer':
            duration_time = None
            '''if end_time != None:
                duration_time = end_time - start_time'''
            for bobj in [self.surplus_bar, self.bar_cap]:
                bobj.color_shift(
                    start_time = start_time,
                    duration_time = duration_time,
                    color = BUYER_BAR_COLOR
                )

        if self.agent.type == 'seller':
            limit_height = MAX_BAR_HEIGHT * self.agent.price_limit / MAX_PRICE

            #Put away
            for piece in [self.extra_top_cap, self.extra_bot_cap, self.surplus_bar]:
                if piece != None: #Sometimes this gets called on bars that don't show surplus
                    piece.move_to(
                        start_time = start_time,
                        new_location = add_lists_by_element(self.bar_loc, [0, limit_height, 0]),
                        new_scale = [BAR_WIDTH, 0, 1],
                    )

    def price_reaction(self, price = None, start_time = None):
        if self.agent.type == 'buyer':
            if price < self.agent.price_limit:
                self.normal_eyes(start_time = start_time)
                self.show_mouth(start_time = start_time)
            elif price > self.agent.price_limit:
                self.angry_eyes(start_time = start_time)
                self.hide_mouth(start_time = start_time)
        elif self.agent.type == 'seller':
            if price > self.agent.price_limit:
                self.normal_eyes(start_time = start_time)
                self.show_mouth(start_time = start_time)
            elif price < self.agent.price_limit:
                self.angry_eyes(start_time = start_time)
                self.hide_mouth(start_time = start_time)

    def set_out_good(self, start_time = None, model = None):
        good = DrawnGood(
            object_model = model,
            name = 'good',
            location = [0, 0.28, 1],
            scale = 0.5
        )
        constraint = good.ref_obj.constraints.new('CHILD_OF')
        constraint.target = self.ref_obj
        self.good = good

        good.add_to_blender(appear_time = start_time)

    def show_o_slash(self, appear_time = None):
        if self.slash == None:
            self.slash = import_object(
                'o_slash', 'primitives',
                location = add_lists_by_element(
                    self.bar_loc,
                    [0, MAX_BAR_HEIGHT + O_SLASH_SCALE, 0],
                ),
                scale = O_SLASH_SCALE
            )
            self.add_subbobject(self.slash)
            apply_material(self.slash.ref_obj.children[0], 'color6')
            self.slash.add_to_blender(appear_time = appear_time)
        else:
            self.slash.move_to(
                new_scale = O_SLASH_SCALE,
                start_time = appear_time
            )

    def hide_o_slash(self, start_time = None, end_time = None):
        if end_time == None:
            end_time = start_time + OBJECT_APPEARANCE_TIME / FRAME_RATE
        else:
            self.slash.disappear(disappear_time = end_time)

class DrawnGood(Bobject):
    """docstring for DrawnGood."""

    def __init__(self, object_model, **kwargs):
        super().__init__(
            objects = [object_model.copy()],
            **kwargs
        )

class DrawnMarket(Bobject):
    """docstring for DrawnMarket."""
    def __init__(
        self,
        sim = None,
        scale = 5,
        name = 'market',
        **kwargs
    ):
        super().__init__(scale = scale, name = name, **kwargs)

        if sim == None:
            raise Warning('DrawnMarket needs a market sim to draw')
        self.sim = sim

        self.drawn_sellers = []
        self.drawn_buyers = []

        max_num_one_kind = 0
        for list in sim.agents_lists:
            num_buyers = len([x for x in list if x.type == 'buyer'])
            num_sellers = len([x for x in list if x.type == 'seller'])
            max_num_one_kind = max(max_num_one_kind, num_buyers, num_sellers)

        #Complicated function that
        #modifier = (1.5 - 1 / (2 ** (max_num_one_kind - 5) + 1))
        modifier = (1 + math.atan(max_num_one_kind - 5) / math.pi )
        #Wanted to correct the 1/x scaling a bit
        self.agent_scale = AGENT_BASE_SCALE / max_num_one_kind * modifier

        self.elapsed_time = 0

        good_bobject_model = import_object('rocket', 'misc')
        self.good_object_model = good_bobject_model.ref_obj.children[0]
        good_bobject_model.tweak_colors_recursive()

    def add_to_blender(self, appear_time = None, **kwargs):
        if appear_time == None:
            raise Warning('Need appear_time for DrawnMarket.add_to_blender()')

        self.appear_time = appear_time

        floor = import_object(
            'disc', 'primitives',
            location = [0, 0, 0],
            name = 'market_floor'
        )
        apply_material(floor.ref_obj.children[0], 'color2')
        self.add_subbobject(floor)
        super().add_to_blender(appear_time = self.appear_time, **kwargs)

        self.draw_sellers(
            start_time = self.appear_time + OBJECT_APPEARANCE_TIME / FRAME_RATE,
            agents = self.sim.agents_lists[0]
        )
        self.draw_buyers(
            start_time = self.appear_time + OBJECT_APPEARANCE_TIME / FRAME_RATE,
            agents = self.sim.agents_lists[0]
        )

    def draw_sellers(self, start_time = None, agents = None):
        sellers = []
        for agent in agents:
            if agent.type == 'seller':
                sellers.append(agent)

        #Kind of confusing, but referring to members of DrawnAgent class as
        #'sellers' and members of Agent class as 'agents', even though both are
        #sellers.
        sellers_to_remove = [x for x in self.drawn_sellers if x.agent not in sellers]
        sellers_to_move = [x for x in self.drawn_sellers if x.agent in sellers]
        agents_already_drawn = [x.agent for x in self.drawn_sellers]
        agents_to_draw = [x for x in sellers if x not in agents_already_drawn]
        sellers_to_add = []
        for seller in agents_to_draw:
            sellers_to_add.append(
                DrawnAgent(
                    agent = seller,
                    display_mode = 'table',
                    location = [0, 1 - self.agent_scale, self.agent_scale * AGENT_HEIGHT_FACTOR],
                    rotation_euler = [math.pi / 2, 0, 0],
                    scale = self.agent_scale
                )
            )

        sorted_sellers = sorted(
            sellers_to_move + sellers_to_add,
            key = lambda x: x.agent.price_limit
        )

        angle = math.pi / (len(sorted_sellers) + 1)
        for i, seller in enumerate(sorted_sellers):
            if seller in sellers_to_add:
                anchor = Bobject(
                    rotation_euler = [0, 0, math.pi / 2 - (i + 1) * angle],
                    name = 'seller_anchor'
                )
                self.add_subbobject(anchor)
                anchor.add_subbobject(seller)
                anchor.add_to_blender(
                    appear_time = start_time - OBJECT_APPEARANCE_TIME / FRAME_RATE,
                    subbobject_timing = OBJECT_APPEARANCE_TIME
                )
                seller.make_display(appear_time = start_time + OBJECT_APPEARANCE_TIME / FRAME_RATE)
                seller.add_expected_price(
                    price = seller.agent.goal_prices[0],
                    appear_time = start_time + OBJECT_APPEARANCE_TIME / FRAME_RATE
                )
                seller.anchor = anchor


            self.drawn_sellers.append(seller)

            if seller in sellers_to_move:
                raise Warning('Not implemented!')
            if seller in sellers_to_remove:
                raise Warning('Not implemented!')

    def draw_buyers(self, start_time = None, agents = None):
        buyers = []
        for agent in agents:
            if agent.type == 'buyer':
                buyers.append(agent)

        #Kind of confusing, but referring to members of DrawnAgent class as
        #'buyers' and members of Agent class as 'agents', even though both are
        #buyers.
        buyers_to_remove = [x for x in self.drawn_buyers if x.agent not in buyers]
        #buyers_to_move = [x for x in self.drawn_buyers if x.agent in buyers]
        agents_already_drawn = [x.agent for x in self.drawn_buyers]
        agents_to_draw = [x for x in buyers if x not in agents_already_drawn]
        buyers_to_add = []
        for buyer in agents_to_draw:
            too_close = True
            while too_close == True:
                too_close = False
                location = [
                    uniform(BUYER_X_MIN, BUYER_X_MAX),
                    uniform(BUYER_Y_MIN, BUYER_Y_MAX),
                    self.agent_scale * AGENT_HEIGHT_FACTOR
                ]
                min_dist = math.inf
                for agent in agents_already_drawn + buyers_to_add:
                    dist = vec_len(add_lists_by_element(
                        location,
                        agent.ref_obj.location,
                        subtract = True
                    ))
                    if dist < min_dist:
                        min_dist = dist
                if min_dist < self.agent_scale:
                    too_close = True
                    #print(dist)
                    print("Trying again")

            buyers_to_add.append(
                DrawnAgent(
                    agent = buyer,
                    display_mode = 'above',
                    location = location,
                    rotation_euler = [math.pi / 2, 0, uniform(0, 2 * math.pi)],
                    scale = self.agent_scale
                )
            )

        for i, buyer in enumerate(buyers_to_add):
            if buyer in buyers_to_add:
                self.add_subbobject(buyer)
                buyer.add_to_blender(appear_time = start_time)
                buyer.make_display(appear_time = start_time + OBJECT_APPEARANCE_TIME / FRAME_RATE)
                buyer.add_expected_price(
                    price = buyer.agent.goal_prices[0],
                    appear_time = start_time + OBJECT_APPEARANCE_TIME / FRAME_RATE
                )
                self.drawn_buyers.append(buyer)

            if buyer in buyers_to_remove:
                raise Warning('Not implemented!')

    def animate_session(self, session = None, session_index = None):
        #Set up sellers
        for seller in self.drawn_sellers:
            #If sitting session out, add o_slash
            if seller.agent not in session.sellers:
                seller.show_o_slash(appear_time = self.elapsed_time)
            else:
                seller.hide_o_slash(start_time = self.elapsed_time)
                #set out goods
                if seller.good == None:
                    seller.set_out_good(
                        start_time = self.elapsed_time,
                        model = self.good_object_model
                    )

        #pause
        self.elapsed_time += PAUSE_LENGTH
        #print(len(session.rounds))
        #Animate rounds
        for round in session.rounds:
            ##Move Buyers
            for drawn_buyer in self.drawn_buyers:
                seller_to_meet = None
                transaction_price = None
                for meeting in round:
                    if meeting.buyer == drawn_buyer.agent:
                        #print("Hey, this meeting has the right buyer")
                        seller_to_meet = meeting.seller
                        transaction_price = meeting.transaction_price

                if seller_to_meet != None: #Go to seller
                    drawn_seller_to_meet = None
                    for d_seller in self.drawn_sellers:
                        if d_seller.agent == seller_to_meet:
                            drawn_seller_to_meet = d_seller

                    loc = drawn_seller_to_meet.ref_obj.location
                    ang = drawn_seller_to_meet.anchor.ref_obj.rotation_euler[2]




                    TABLE_SPACING = 2 * self.agent_scale
                    location = [ #loc[0] = 0, rotating y coord
                        -(loc[1] - TABLE_SPACING) * math.sin(ang),
                        (loc[1] - TABLE_SPACING) * math.cos(ang),
                        loc[2],
                    ]

                    #Prep to use ang for actual drawn_agent orientation
                    ang += math.pi
                    ang = make_angles_within_pi(
                        angle_to_change = ang,
                        target_angle = drawn_buyer.ref_obj.rotation_euler[2]
                    )

                    angle = [
                        drawn_buyer.ref_obj.rotation_euler[0],
                        drawn_buyer.ref_obj.rotation_euler[1],
                        ang
                    ]

                    drawn_buyer.was_just_meeting_seller = True

                    drawn_buyer.move_to(
                        start_time = self.elapsed_time,
                        end_time = self.elapsed_time + ROUND_MOVE_DURATION / 4,
                        new_angle = angle
                    )
                    drawn_buyer.move_to(
                        start_time = self.elapsed_time,
                        end_time = self.elapsed_time + ROUND_MOVE_DURATION,
                        new_location = location
                    )

                elif drawn_buyer.was_just_meeting_seller == True: #Go to lobby
                    old_loc = drawn_buyer.ref_obj.location
                    location = [
                        uniform(BUYER_X_MIN, BUYER_X_MAX),
                        uniform(BUYER_Y_MIN, BUYER_Y_MAX),
                        old_loc[2]
                    ]
                    ang = math.atan2(
                        location[1] - old_loc[1],
                        location[0] - old_loc[0]
                    ) + math.pi / 2 #because the angle is actually from the y-axis
                                    #because I like things to be hard for no reason
                    ang = make_angles_within_pi(
                        angle_to_change = ang,
                        target_angle = drawn_buyer.ref_obj.rotation_euler[2]
                    )
                    angle = [
                        drawn_buyer.ref_obj.rotation_euler[0],
                        drawn_buyer.ref_obj.rotation_euler[1],
                        ang
                    ]
                    drawn_buyer.was_just_meeting_seller = False

                    '''#Add keyframes, making rotation happen faster
                    obj = drawn_buyer.ref_obj
                    obj.keyframe_insert(
                        data_path = 'rotation_euler',
                        frame = self.elapsed_time * FRAME_RATE
                    )
                    obj.keyframe_insert(
                        data_path = 'location',
                        frame = self.elapsed_time * FRAME_RATE
                    )


                    drawn_buyer.move_to(
                        start_time = self.elapsed_time,
                        end_time = self.elapsed_time + ROUND_MOVE_DURATION,
                        new_location = location,
                        new_angle = angle
                    )'''

                    drawn_buyer.move_to(
                        start_time = self.elapsed_time,
                        end_time = self.elapsed_time + ROUND_MOVE_DURATION / 4,
                        new_angle = angle
                    )
                    drawn_buyer.move_to(
                        start_time = self.elapsed_time,
                        end_time = self.elapsed_time + ROUND_MOVE_DURATION,
                        new_location = location
                    )


                else:
                    location = drawn_buyer.ref_obj.location
                    angle = None

                    drawn_buyer.move_to(
                        start_time = self.elapsed_time,
                        end_time = self.elapsed_time + ROUND_MOVE_DURATION,
                        new_location = location,
                        new_angle = angle
                    )

                if transaction_price != None:
                    drawn_buyer.highlight_surplus(
                        price = transaction_price,
                        start_time = self.elapsed_time + ROUND_MOVE_DURATION,
                        #end_time = self.elapsed_time + ROUND_MOVE_DURATION + PAUSE_LENGTH * 2
                    )
                    drawn_seller_to_meet.highlight_surplus(
                        price = transaction_price,
                        start_time = self.elapsed_time + ROUND_MOVE_DURATION,
                        #end_time = self.elapsed_time + ROUND_MOVE_DURATION + PAUSE_LENGTH * 2
                    )

                    #Hand off good
                    good_sold = drawn_seller_to_meet.good
                    old_cons = good_sold.ref_obj.constraints[0]
                    old_cons.keyframe_insert(
                        data_path = 'influence',
                        frame = (self.elapsed_time + ROUND_MOVE_DURATION + PAUSE_LENGTH / 2) * FRAME_RATE
                    )
                    old_cons.influence = 0
                    old_cons.keyframe_insert(
                        data_path = 'influence',
                        frame = (self.elapsed_time + ROUND_MOVE_DURATION + PAUSE_LENGTH / 2) * FRAME_RATE + 1
                    )

                    new_cons = good_sold.ref_obj.constraints.new('CHILD_OF')
                    new_cons.target = drawn_buyer.ref_obj
                    drawn_buyer.good = good_sold
                    new_cons.influence = 0
                    new_cons.keyframe_insert(
                        data_path = 'influence',
                        frame = (self.elapsed_time + ROUND_MOVE_DURATION + PAUSE_LENGTH / 2) * FRAME_RATE
                    )
                    new_cons.influence = 1
                    new_cons.keyframe_insert(
                        data_path = 'influence',
                        frame = (self.elapsed_time + ROUND_MOVE_DURATION + PAUSE_LENGTH / 2) * FRAME_RATE + 1
                    )

                    #Turn good_around
                    good_sold.ref_obj.keyframe_insert(
                        data_path = 'rotation_euler',
                        frame = (self.elapsed_time + ROUND_MOVE_DURATION + PAUSE_LENGTH / 2) * FRAME_RATE
                    )
                    good_sold.ref_obj.rotation_euler = [
                        good_sold.ref_obj.rotation_euler[0],
                        good_sold.ref_obj.rotation_euler[1] + math.pi,
                        good_sold.ref_obj.rotation_euler[2],
                    ]
                    good_sold.ref_obj.keyframe_insert(
                        data_path = 'rotation_euler',
                        frame = (self.elapsed_time + ROUND_MOVE_DURATION + PAUSE_LENGTH / 2) * FRAME_RATE + 1
                    )

                    drawn_seller_to_meet.good = None

            self.elapsed_time += ROUND_MOVE_DURATION


            ##Animate sales
            pass

            ##pause
            self.elapsed_time += PAUSE_LENGTH

        #Buyers to lobby
        for drawn_buyer in self.drawn_buyers:
            if drawn_buyer.was_just_meeting_seller == True:
                old_loc = drawn_buyer.ref_obj.location
                new_loc = [
                    uniform(BUYER_X_MIN, BUYER_X_MAX),
                    uniform(BUYER_Y_MIN, BUYER_Y_MAX),
                    old_loc[2]
                ]
                disp_ang = math.atan2(
                    new_loc[1] - old_loc[1],
                    new_loc[0] - old_loc[0]
                ) + math.pi / 2 #because the angle is actually from the y-axis
                                #because I like things to be hard for no reason
                disp_ang = make_angles_within_pi(
                    angle_to_change = disp_ang,
                    target_angle = drawn_buyer.ref_obj.rotation_euler[2]
                )
                drawn_buyer.move_to(
                    start_time = self.elapsed_time,
                    end_time = self.elapsed_time + ROUND_MOVE_DURATION / 4,
                    new_angle = [
                        drawn_buyer.ref_obj.rotation_euler[0],
                        drawn_buyer.ref_obj.rotation_euler[1],
                        disp_ang
                    ]
                )
                drawn_buyer.move_to(
                    start_time = self.elapsed_time,
                    end_time = self.elapsed_time + ROUND_MOVE_DURATION,
                    new_location = new_loc,
                )
            drawn_buyer.was_just_meeting_seller = False

        #Consume/celebration animation?
        pass

        #Adjust prices
        self.elapsed_time += PAUSE_LENGTH
        for drawn_agent in self.drawn_buyers + self.drawn_sellers:
            drawn_agent.move_expected_price(
                price = drawn_agent.agent.goal_prices[session_index + 1],
                start_time = self.elapsed_time
            )
            drawn_agent.hide_surplus(
                start_time = self.elapsed_time
            )
        #Put away bought goods
        for drawn_buyer in self.drawn_buyers:
            if drawn_buyer.good != None:
                drawn_buyer.good.disappear(disappear_time = self.elapsed_time)
                #drawn_buyer.good = None


        #pause
        self.elapsed_time += PAUSE_LENGTH

    def animate_sessions(self, start_time = None):
        self.elapsed_time += start_time

        for i, session in enumerate(self.sim.sessions):
            self.animate_session(session = session, session_index = i)

class MarketGraph(GraphBobject):
    """docstring for MarketGraph."""

    def __init__(self, **kwargs):
        super().__init__(self, **kwargs)

    def add_agent(agent = None, start_time = None):
        pass

        #Add drawn_agent
        #hide/delete blob
        #sort relative to other agents
        #place and scale graph appropriately
        #scale bar (esp cap) appropriately, likely making BAR_WIDTH an argument
        #rather than a constant
        #May have to edit change_window()
