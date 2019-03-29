import bpy
import imp
from random import random, randrange, choice, gauss, uniform
#from copy import copy
import pickle

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

DEFAULT_BAR_WIDTH = 0.3
DEFAULT_MAX_BAR_HEIGHT = 1.6
MAX_PRICE = market_sim.MAX_PRICE
BAR_THICKNESS = 0.08
BAR_BASE_LIP = 0.01
BAR_BASE_LENGTH_FACTOR = 1.3
O_SLASH_SCALE = 0.5
CAP_OBJECT_HEIGHT = 0.5


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
        name = 'agent',
        bar_width = DEFAULT_BAR_WIDTH,
        max_bar_height = DEFAULT_MAX_BAR_HEIGHT,
        **kwargs
    ):

        if agent == None: #No reason to make default agents
            raise Warning('DrawnAgent needs agent')
        self.agent = agent
        self.bar_width = bar_width
        self.max_bar_height = max_bar_height

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
        #probably a cleaner way to do this, but delete the blob if in graph mode
        #bpy.ops.object.select_all(action='DESELECT')
        if self.display_mode == 'graph':
            bleb = self.ref_obj.children[0]
            link_descendants(bleb, unlink = True)

    def make_display(self, thickness_factor = 1, appear_time = None):
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
        elif self.display_mode == 'graph':
            self.bar_loc = [0, 0, 0]

        else:
            raise Warning('Unrecognized display_mode')

        self.value_bar = import_object(
            'xy_plane_unrounded', 'primitives',
            location = self.bar_loc,
            name = 'value_display_bar',
            scale = [self.bar_width * thickness_factor, 0, 1]
        )

        #height of default cap object is 0.5, then it's scaled by self.bar_width when shown
        cap_height = CAP_OBJECT_HEIGHT * self.bar_width * thickness_factor
        cap_scale_y = self.bar_width * thickness_factor
        height_after_cap = self.max_bar_height * self.agent.price_limit / MAX_PRICE
        height = height_after_cap - cap_height
        if height < 0:
            height = 0
            cap_scale_y = self.bar_width * height_after_cap / cap_height

        self.bar_cap = import_object(
            'bar_cap', 'primitives',
            location = self.bar_loc,
            scale = [self.bar_width * thickness_factor, 0, 1],
            name = 'cap'
        )

        self.surplus_bar = import_object(
            'xy_plane_unrounded', 'primitives',
            location = add_lists_by_element(self.bar_loc, [0, height_after_cap, 0]),
            name = 'surplus_display_bar',
            scale = [self.bar_width * thickness_factor, 0, 0]
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
            scale = [
                (BAR_THICKNESS + 2 * BAR_BASE_LIP),
                base_bar_height,
                self.bar_width * BAR_BASE_LENGTH_FACTOR * thickness_factor
            ]
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
                self.bar_width * thickness_factor,
                height,
                1
            ]
        )
        '''self.surplus_bar.move_to(
            start_time = appear_time + OBJECT_APPEARANCE_TIME / FRAME_RATE,
            new_location = add_lists_by_element(self.bar_loc, [0, height, 0]),
            new_scale = [self.bar_width * thickness_factor, 0, 1]
        )'''
        self.bar_cap.move_to(
            start_time = appear_time + OBJECT_APPEARANCE_TIME / FRAME_RATE,
            new_location = add_lists_by_element(self.bar_loc, [0, height, 0]),
            new_scale = [self.bar_width * thickness_factor, cap_scale_y, 1]
        )

    def change_thickness(self, new_thickness = None, start_time = None):

        #Change x and y for cap
        #Change cap position to keep top in same spot
        prev_cap_scale = self.bar_cap.ref_obj.scale[0]
        new_scale = self.bar_width * new_thickness

        self.bar_cap.move_to(
            new_scale = [
                new_scale,
                new_scale,
                1
            ],
            displacement = [0, CAP_OBJECT_HEIGHT * (prev_cap_scale - new_scale), 0],
            start_time = start_time
        )

        prev_bar_scale_y = self.value_bar.ref_obj.scale[1]

        height_boost = CAP_OBJECT_HEIGHT * (prev_cap_scale - new_scale)

        self.value_bar.move_to(
            new_scale = [
                new_scale,
                prev_bar_scale_y + height_boost,
                1
            ],
            start_time = start_time
        )

        #Change thickness of surplus indicators
        self.surplus_bar.move_to(
            new_scale = [
                new_scale,
                self.surplus_bar.ref_obj.scale[1],
                self.surplus_bar.ref_obj.scale[2]
            ],
            displacement = [0, height_boost, 0],
            start_time = start_time
        )
        if self.extra_top_cap != None:
            self.extra_top_cap.move_to(
                new_scale = [
                    new_scale,
                    self.extra_top_cap.ref_obj.scale[1],
                    self.extra_top_cap.ref_obj.scale[2]
                ],
                start_time = start_time
            )
        if self.extra_bot_cap != None:
            self.extra_bot_cap.move_to(
                new_scale = [
                    new_scale,
                    self.extra_bot_cap.ref_obj.scale[1],
                    self.extra_bot_cap.ref_obj.scale[2]
                ],
                start_time = start_time
            )

        #Change thickness of expected price indicators
        self.expected_price_indicator.move_to(
            new_scale = new_thickness,
            start_time = start_time
        )

        #Aaaand the base
        self.bar_base.move_to(
            new_scale = [
                self.bar_base.ref_obj.scale[0],
                self.bar_base.ref_obj.scale[1],
                self.bar_width * BAR_BASE_LENGTH_FACTOR * new_thickness,
            ],
            start_time = start_time
        )


    def add_price_line(self, price = 0, appear_time = None, emote = False):
        if appear_time == None:
            raise Warning('add_price_line() needs appear_time')

        #Price line
        price_line_width = 0.01
        height = self.max_bar_height * price / MAX_PRICE
        self.price_line = import_object(
            'cylinder', 'primitives',
            location = add_lists_by_element(self.bar_loc, [0, height, 0]),
            rotation_euler = [0, math.pi / 2, 0],
            name = 'price_line',
            scale = [price_line_width, price_line_width, self.bar_width * 1.1]
        )
        apply_material(self.price_line.ref_obj.children[0], 'color6')

        self.display_container.add_subbobject(self.price_line)
        self.price_line.add_to_blender(appear_time = appear_time)

        if emote == True:
            self.price_reaction(price, start_time = appear_time + OBJECT_APPEARANCE_TIME / FRAME_RATE)

    def move_price_line(self, price = 0, start_time = None, emote = False):
        if start_time == None:
            raise Warning('move_price_line() needs start_time')

        height = self.max_bar_height * price / MAX_PRICE

        self.price_line.move_to(
            new_location = add_lists_by_element(self.bar_loc, [0, height, 0]),
            start_time = start_time
        )

        if emote == True:
            self.price_reaction(price = price, start_time = start_time + OBJECT_APPEARANCE_TIME / FRAME_RATE)

    def add_expected_price(self, price = None, session_index = None, thickness_factor = 1, appear_time = None):
        if appear_time == None:
            raise Warning('add_expected_price() needs appear_time')

        if price == None and session_index == None:
            raise Warning('Need price or session index to add expected price indicator')
        elif session_index != None:
            price = self.agent.goal_prices[session_index]

        #Price line
        try:
            height = self.max_bar_height * price / MAX_PRICE
        except:
            print(self.max_bar_height)
            print(price)
            print(MAX_PRICE)
            raise()
        l_tri = import_object(
            'rounded_isosceles', 'primitives',
            location = [- self.bar_width * 1.05, 0, 0],
            rotation_euler = [0, 0, -math.pi / 2],
            scale = 0.15 * self.bar_width
        )
        r_tri = import_object(
            'rounded_isosceles', 'primitives',
            location = [self.bar_width * 1.05, 0, 0],
            rotation_euler = [0, 0, math.pi / 2],
            scale = 0.15 * self.bar_width
        )
        for tri in [l_tri, r_tri]:
            apply_material(tri.ref_obj.children[0], 'color2')


        self.expected_price_indicator = bobject.Bobject(
            l_tri, r_tri,
            location = add_lists_by_element(self.bar_loc, [0, height, 0]),
            #rotation_euler = [0, math.pi / 2, 0],
            scale = thickness_factor,
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

        height = self.max_bar_height * price / MAX_PRICE

        self.expected_price_indicator.move_to(
            new_location = add_lists_by_element(self.bar_loc, [0, height, 0]),
            start_time = start_time
        )

    def highlight_surplus(self, price = None, start_time = None, end_time = None):
        cap_height = CAP_OBJECT_HEIGHT * self.bar_cap.ref_obj.scale[0]

        if self.agent.type == 'buyer':
            if price >= self.agent.price_limit:
                self.hide_surplus(start_time = start_time)
            else:
                price_height = self.max_bar_height * price / MAX_PRICE

                height_after_cap = self.max_bar_height * self.agent.price_limit / MAX_PRICE
                height = height_after_cap - cap_height

                if height >= price_height:
                    self.value_bar.move_to(
                        start_frame = start_time * FRAME_RATE - 1,
                        end_frame = start_time * FRAME_RATE,
                        new_scale = [
                            self.value_bar.ref_obj.scale[0],
                            price_height,
                            1
                        ]
                    )
                    self.surplus_bar.move_to(
                        start_frame = start_time * FRAME_RATE - 1,
                        end_frame = start_time * FRAME_RATE,
                        new_location = add_lists_by_element(self.bar_loc, [0, price_height, 0]),
                        new_scale = [
                            self.surplus_bar.ref_obj.scale[0],
                            height - price_height,
                            1
                        ]
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


                else:
                    #height = price_height
                    #cap_height = height_after_cap - height

                    self.value_bar.move_to(
                        start_frame = start_time * FRAME_RATE,
                        new_scale = [
                            self.value_bar.ref_obj.scale[0],
                            price_height,
                            1
                        ]
                    )
                    #cap_scale_y = self.bar_width *  / cap_height
                    self.bar_cap.move_to(
                        start_frame = start_time * FRAME_RATE,
                        new_scale = [
                            self.bar_cap.ref_obj.scale[0],
                            self.bar_cap.ref_obj.scale[0] * (height_after_cap - price_height) / cap_height ,
                            1
                        ],
                        new_location = add_lists_by_element(self.bar_loc, [0, price_height, 0])
                    )


                    #Copied code from other part of this if-else, but just
                    #coloring the bar cap
                    duration_time = None
                    if end_time != None:
                        duration_time = end_time - start_time
                    for bobj in [self.bar_cap]:
                        bobj.color_shift(
                            start_time = start_time,
                            duration_time = duration_time,
                            color = BUYER_SURPLUS_COLOR
                        )

        if self.agent.type == 'seller':
            if price <= self.agent.price_limit:
                self.hide_surplus(start_time = start_time)
            else:
                limit_height = self.max_bar_height * self.agent.price_limit / MAX_PRICE
                price_height = self.max_bar_height * price / MAX_PRICE

                surplus_bar_height = price_height - limit_height - 2 * cap_height
                if surplus_bar_height < 0:
                    surplus_bar_height = 0

                room_for_caps = price_height - limit_height
                if room_for_caps < 2 * cap_height:
                    cap_height = room_for_caps / 2

                if self.extra_top_cap == None:
                    pass
                    self.extra_top_cap = import_object(
                        'bar_cap', 'primitives',
                        location = add_lists_by_element(self.bar_loc, [0, limit_height, 0]),
                        scale = [self.value_bar.ref_obj.scale[0], 0, 1],
                        name = 'top_cap'
                    )
                    self.extra_bot_cap = import_object(
                        'bar_cap', 'primitives',
                        location = add_lists_by_element(self.bar_loc, [0, limit_height, 0]),
                        scale = [self.value_bar.ref_obj.scale[0], 0, 1],
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
                    new_scale = [
                        self.value_bar.ref_obj.scale[0],
                        cap_height / CAP_OBJECT_HEIGHT,
                        1
                    ],
                    new_location = add_lists_by_element(self.bar_loc, [0, price_height - cap_height, 0]),
                )
                self.extra_bot_cap.move_to(
                    start_time = start_time,
                    new_scale = [
                        self.value_bar.ref_obj.scale[0],
                        - cap_height / CAP_OBJECT_HEIGHT,
                        1
                    ],
                    new_location = add_lists_by_element(self.bar_loc, [0, limit_height + cap_height, 0]),
                )

                self.surplus_bar.move_to(
                    start_time = start_time,
                    new_location = add_lists_by_element(self.bar_loc, [0, limit_height + cap_height, 0]),
                    new_scale = [
                        self.value_bar.ref_obj.scale[0],
                        surplus_bar_height,
                        1
                    ],
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
                            new_scale = [
                                piece.ref_obj.scale[0],
                                0,
                                1
                            ],
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

        if self.agent.type == 'buyer':
            limit_height = self.max_bar_height * self.agent.price_limit / MAX_PRICE
            goal_cap_height = CAP_OBJECT_HEIGHT * self.bar_cap.ref_obj.scale[0]
            bar_height = limit_height - goal_cap_height

            self.bar_cap.move_to(
                new_location = add_lists_by_element(self.bar_loc, [0, bar_height, 0]),
                new_scale = [
                    self.bar_cap.ref_obj.scale[0], #Keep x scale the same
                    self.bar_cap.ref_obj.scale[0], #And make y copy x
                    1
                ],
                start_time = start_time
            )
            self.value_bar.move_to(
                new_scale = [
                    self.value_bar.ref_obj.scale[0],
                    bar_height,
                    1
                ],
                start_time = start_time
            )

        if self.agent.type == 'seller':
            limit_height = self.max_bar_height * self.agent.price_limit / MAX_PRICE

            #Put away
            for piece in [self.extra_top_cap, self.extra_bot_cap, self.surplus_bar]:
                if piece != None: #Sometimes this gets called on bars that don't show surplus
                    piece.move_to(
                        start_time = start_time,
                        new_location = add_lists_by_element(self.bar_loc, [0, limit_height, 0]),
                        new_scale = [piece.ref_obj.scale[0], 0, 0],
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
                    [0, self.max_bar_height + O_SLASH_SCALE, 0],
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
        loud = False,
        **kwargs
    ):
        super().__init__(scale = scale, name = name, **kwargs)

        if sim == None:
            raise Warning('DrawnMarket needs a market sim to draw')
        elif isinstance(sim, str):
            result = os.path.join(
                SIM_DIR,
                sim
            ) + ".pkl"
            if loud:
                print(result)
            with open(result, 'rb') as input:
                if loud:
                    print(input)
                self.sim = pickle.load(input)
            if loud:
                print("Loaded the world")
        else:
            self.sim = sim


        self.drawn_sellers = []
        self.drawn_buyers = []

        self.update_agent_scale(session_index = 0)

        self.elapsed_time = 0

        good_bobject_model = import_object('rocket', 'misc')
        self.good_object_model = good_bobject_model.ref_obj.children[0]
        good_bobject_model.tweak_colors_recursive()

        self.linked_graph = None

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

    def update_agent_scale(self, session_index = None):
        max_num_one_kind = 0
        list = self.sim.agents_lists[session_index]
        num_buyers = len([x for x in list if x.type == 'buyer'])
        num_sellers = len([x for x in list if x.type == 'seller'])
        max_num_one_kind = max(max_num_one_kind, num_buyers, num_sellers)

        #Complicated function that
        #modifier = (1.5 - 1 / (2 ** (max_num_one_kind - 5) + 1))
        modifier = (1 + math.atan(max_num_one_kind - 5) / math.pi )
        #Wanted to correct the 1/x scaling a bit
        self.agent_scale = AGENT_BASE_SCALE / max_num_one_kind * modifier

    def draw_sellers(self, start_time = None, agents = None, session_index = 0):
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
                    price = seller.agent.goal_prices[session_index],
                    appear_time = start_time + OBJECT_APPEARANCE_TIME / FRAME_RATE
                )
                seller.anchor = anchor


                self.drawn_sellers.append(seller)

            if seller in sellers_to_move:
                #raise Warning('Not implemented!')
                seller.anchor.move_to(
                    new_angle = [0, 0, math.pi / 2 - (i + 1) * angle],
                    start_time = start_time
                )
                seller.move_to(
                    new_scale = self.agent_scale,
                    start_time = start_time
                )
            if seller in sellers_to_remove:
                raise Warning('Not implemented!')

    def draw_buyers(self, start_time = None, agents = None, session_index = 0):
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
                for agent in self.drawn_buyers + buyers_to_add:
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

        for agent in self.drawn_buyers:
            agent.move_to(
                new_scale = self.agent_scale,
                start_time = start_time
            )

        for i, buyer in enumerate(buyers_to_add):
            if buyer in buyers_to_add:
                self.add_subbobject(buyer)
                buyer.add_to_blender(appear_time = start_time)
                buyer.make_display(appear_time = start_time + OBJECT_APPEARANCE_TIME / FRAME_RATE)
                buyer.add_expected_price(
                    price = buyer.agent.goal_prices[session_index],
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
                    if self.linked_graph != None:
                        g = self.linked_graph
                        displayed = g.displayed_buyer_bobjects + g.displayed_seller_bobjects
                        for drawn_agent in displayed:
                            #print(drawn_agent.agent)
                            ##print(drawn_seller_to_meet.agent)
                            #print(drawn_buyer.agent)
                            #print()
                            if drawn_agent.agent == drawn_seller_to_meet.agent or \
                                    drawn_agent.agent == drawn_buyer.agent:
                                #print()
                                #print("AGENTS MATCH")
                                #print()
                                meetings = [x for x in drawn_agent.agent.meetings if \
                                           x.transaction_price != None and x.session_index == session_index]
                                if len(meetings) == 1:
                                    drawn_agent.highlight_surplus(
                                        price = meetings[0].transaction_price,
                                        start_time = self.elapsed_time + ROUND_MOVE_DURATION,
                                    )
                                elif len(meetings) > 1:
                                    raise Warning('There is more than one successful meeting for this agent and session?')


                        '''for agent in self.linked_graph.agents

                        self.linked_graph.highlight_surpluses(
                            index = session_index,
                            start_time = self.elapsed_time + ROUND_MOVE_DURATION,
                        )'''

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

        if self.linked_graph != None:
            self.linked_graph.move_expected_prices(
                index = session_index + 1,
                start_time = self.elapsed_time
            )
            self.linked_graph.hide_surpluses(
                start_time = self.elapsed_time
            )

        #pause
        self.elapsed_time += PAUSE_LENGTH

    def animate_sessions(self, start_time = None):
        self.elapsed_time += start_time

        for i, session in enumerate(self.sim.sessions):
            self.update_agent_scale(session_index = i)
            self.draw_sellers(
                start_time = self.elapsed_time,
                agents = self.sim.agents_lists[i],
                session_index = i
            )
            self.draw_buyers(
                start_time = self.elapsed_time,
                agents = self.sim.agents_lists[i],
                session_index = i
            )
            if self.linked_graph != None:
                '''graphed_buyers = [x.agent for x in self.linked_graph.buyer_bobjects]
                graphed_sellers = [x.agent for x in self.linked_graph.seller_bobjects]
                for agent in self.sim.agents_lists[-1]:
                    if agent not in graphed_buyers + graphed_sellers:
                        self.linked_graph.add_agent(agent = agent)'''
                self.linked_graph.update_agent_display(
                    start_time = self.elapsed_time,
                    session_index = i
                )
            self.animate_session(session = session, session_index = i)

class MarketGraph(GraphBobject):
    """docstring for MarketGraph."""

    def __init__(self, sim = None, loud = False, display_arrangement = 'buyer_seller', *args, **kwargs):
        super().__init__(*args, **kwargs)

        if sim == None:
            raise Warning('MarketGraph needs a market sim to draw')
        elif isinstance(sim, str):
            result = os.path.join(
                SIM_DIR,
                sim
            ) + ".pkl"
            if loud:
                print(result)
            with open(result, 'rb') as input:
                if loud:
                    print(input)
                self.sim = pickle.load(input)
            if loud:
                print("Loaded the world")
        else:
            self.sim = sim

        self.display_arrangement = display_arrangement
        initial_agents = self.sim.agents_lists[0]
        if self.display_arrangement == 'buyer_seller':
            self.num_initial_displays = len(initial_agents)
        else:
            num_buyers = len([x for x in initial_agents if x.type == 'buyer'])
            num_sellers = len([x for x in initial_agents if x.type == 'seller'])
            self.num_initial_displays = max(num_buyers, num_sellers)

        self.display_width = self.x_range[1] / self.num_initial_displays

        self.bar_to_space_ratio = 0.8

        self.buyer_bobjects = []
        self.seller_bobjects = []
        for agent in initial_agents:
            self.add_agent(agent = agent)
        self.displayed_buyer_bobjects = []
        self.displayed_seller_bobjects = []

    def add_agent(self, agent = None):
        bar_width = self.bar_to_space_ratio * self.display_width / 2
        new_agent = DrawnAgent(
            agent = agent,
            display_mode = 'graph',
            bar_width = bar_width,
            max_bar_height = self.y_range[1]
        )
        self.add_subbobject(new_agent)

        if agent.type == 'buyer':
            self.buyer_bobjects.append(new_agent)
        elif agent.type == 'seller':
            self.seller_bobjects.append(new_agent)

        return new_agent

    def update_agent_display(self, start_time = None, mode = None, session_index = None):
        if mode == None:
            mode = self.display_arrangement
        else:
            self.display_arrangement = mode

        if session_index == None:
            raise Warning('Need session index to update agent display')

        #current_sellers = [x for x in self.sim.agents_lists[i] if x.type = 'seller']
        #current_buyers = [x for x in self.sim.agents_lists[i] if x.type = 'buyer']
        current_agents = self.sim.agents_lists[session_index]
        drawn_agents = [x.agent for x in self.seller_bobjects + self.buyer_bobjects]
        #print()
        #print(current_agents)
        #print(drawn_agents)
        for agent in current_agents:
            if agent not in drawn_agents:
                new_drawn_agent = self.add_agent(agent = agent)
                new_drawn_agent.add_to_blender(appear_time = start_time)

        #print([x.agent for x in self.displayed_seller_bobjects])
        #print()

        new_seller_displays = [x for x in self.seller_bobjects if x not in self.displayed_seller_bobjects]
        new_buyer_displays = [x for x in self.buyer_bobjects if x not in self.displayed_buyer_bobjects]
        displays_to_delete = [x for x in self.displayed_seller_bobjects if x not in self.seller_bobjects] + \
                                [x for x in self.displayed_buyer_bobjects if x not in self.buyer_bobjects]

        #Update self.bar_width
        if mode == 'buyer_seller':
            current_num = len(self.buyer_bobjects + self.seller_bobjects)
        elif mode == 'superimposed' or mode == 'stacked':
            current_num = max(len(self.buyer_bobjects), len(self.seller_bobjects))

        thickness_factor = self.num_initial_displays / current_num

        #Make new displays
        for display in new_seller_displays:
            #Delay make_display so the bobject will be in place before the bar
            #actually appears
            display.make_display(
                thickness_factor = thickness_factor,
                appear_time = start_time + OBJECT_APPEARANCE_TIME / FRAME_RATE
            )
            self.displayed_seller_bobjects.append(display)
            display.add_expected_price(
                appear_time = start_time + OBJECT_APPEARANCE_TIME / FRAME_RATE,
                session_index = session_index,
                thickness_factor = thickness_factor,
            )
        for display in new_buyer_displays:
            #Delay make_display so the bobject will be in place before the bar
            #actually appears
            display.make_display(
                thickness_factor = thickness_factor,
                appear_time = start_time + OBJECT_APPEARANCE_TIME / FRAME_RATE
            )
            self.displayed_buyer_bobjects.append(display)
            display.add_expected_price(
                appear_time = start_time + OBJECT_APPEARANCE_TIME / FRAME_RATE,
                session_index = session_index,
                thickness_factor = thickness_factor,
            )

        #print(len(self.agent_bobjects))

        ordered_seller_displays = sorted(
            self.displayed_seller_bobjects,
            key = lambda x: x.agent.price_limit
        )
        sort_direction = -1
        if mode == 'buyer_seller':
            sort_direction = 1
        ordered_buyer_displays = sorted(
            self.displayed_buyer_bobjects,
            key = lambda x: sort_direction * x.agent.price_limit
        )

        #space_width = (graph.x_range[1] - num_bars * bar_width) / (num_bars + 1)
        #x = (1 + i) * space_width + bar_width * (0.5 + i),
        #bar_to_space_ratio = 1
        #display_width = self.x_range[1] / len(ordered_displays)
        if mode == 'buyer_seller':
            current_num = len(ordered_buyer_displays + ordered_seller_displays)
            for i, bar in enumerate(ordered_buyer_displays + ordered_seller_displays):
                new_x = (i + 0.5) * self.display_width * self.num_initial_displays / current_num
                bar.move_to(
                    new_location = [new_x, 0, 0],
                    start_time = start_time
                )
                if bar not in new_buyer_displays + new_seller_displays:
                    bar.change_thickness(
                        new_thickness = self.num_initial_displays / current_num,
                        start_time = start_time
                    )
        if mode == 'superimposed':
            current_num = max(len(ordered_buyer_displays), len(ordered_seller_displays))
            for i, bar in enumerate(ordered_buyer_displays):
                new_x = (i + 0.5) * self.display_width * self.num_initial_displays / current_num
                bar.move_to(
                    new_location = [new_x, 0, -0.15],
                    start_time = start_time
                )
                if bar not in new_buyer_displays:
                    bar.change_thickness(
                        new_thickness = self.num_initial_displays / current_num,
                        start_time = start_time
                    )
            for i, bar in enumerate(ordered_seller_displays):
                new_x = (i + 0.5) * self.display_width * self.num_initial_displays / current_num
                bar.move_to(
                    new_location = [new_x, 0, 0],
                    start_time = start_time
                )
                if bar not in new_seller_displays:
                    bar.change_thickness(
                        new_thickness = self.num_initial_displays / current_num,
                        start_time = start_time
                    )
        if mode == 'stacked':
            current_num = max(len(ordered_buyer_displays), len(ordered_seller_displays))
            for i, bar in enumerate(ordered_buyer_displays):
                new_x = (i + 0.5) * self.display_width * self.num_initial_displays / current_num
                bar.move_to(
                    new_location = [new_x, self.y_range[1] * 1.1, 0],
                    start_time = start_time
                )
                if bar not in new_buyer_displays:
                    bar.change_thickness(
                        new_thickness = self.num_initial_displays / current_num,
                        start_time = start_time
                    )
            for i, bar in enumerate(ordered_seller_displays):
                new_x = (i + 0.5) * self.display_width * self.num_initial_displays / current_num
                bar.move_to(
                    new_location = [new_x, 0, 0],
                    start_time = start_time
                )
                if bar not in new_seller_displays:# and session_index > 0:
                    bar.change_thickness(
                        new_thickness = self.num_initial_displays / current_num,
                        start_time = start_time
                    )

    def add_expected_prices(self, index = None, start_time = None):
        displayed = self.displayed_buyer_bobjects + self.displayed_seller_bobjects
        for drawn_agent in displayed:
            price = drawn_agent.agent.goal_prices[index]
            drawn_agent.add_expected_price(price = price, appear_time = start_time)

    def move_expected_prices(self, index = None, start_time = None):
        displayed = self.displayed_buyer_bobjects + self.displayed_seller_bobjects
        for drawn_agent in displayed:
            price = drawn_agent.agent.goal_prices[index]
            drawn_agent.move_expected_price(price = price, start_time = start_time)

    def highlight_surpluses(self, index = None, start_time = None):
        displayed = self.displayed_buyer_bobjects + self.displayed_seller_bobjects
        for drawn_agent in displayed:
            #price = drawn_agent.agent.goal_prices[index]
            meetings = [x for x in drawn_agent.agent.meetings if \
                       x.transaction_price != None and x.session_index == index]
            if len(meetings) == 1:
                drawn_agent.highlight_surplus(
                    price = meetings[0].transaction_price,
                    start_time = start_time
                )
            elif len(meetings) > 1:
                raise Warning('There is more than one successful meeting for this agent and session?')

    def hide_surpluses(self, start_time = None):
        displayed = self.displayed_buyer_bobjects + self.displayed_seller_bobjects
        for drawn_agent in displayed:
            drawn_agent.hide_surplus(start_time = start_time)

        #Add drawn_agent (check)
        #hide/delete blob (check)
        #sort relative to other agents (check)
        #place bar and scale graph appropriately (check)
        #scale bar (esp cap) appropriately, likely making BAR_WIDTH an argument
        #rather than a constant (check)


        #Separate buyer/seller graphs, figure out how to combine
        #Test addition of agents (also for actual market), possily make scaling dynamic?
        #Show expectation and surplus
