import imp
from random import random, randrange, choice, gauss, uniform
#from copy import copy
#import pickle

import bobject
imp.reload(bobject)
from bobject import *

import blobject

import helpers
imp.reload(helpers)
from helpers import *

PRICE_ADJUST_MODE = 'chance'
PRICE_ADJUST_CHANCE = 0.5
PRICE_ADJUST_MEAN = 1
PRICE_ADJUST_DEV = 0.1
PRICE_CONCESSION = 0.25

class Agent(object):
    """docstring for Agent."""
    def __init__(
        self,
        type = 'buyer',
        interaction_mode = None,
        price_limit = None,
        initial_price = None, #For setting market expectations
    ):
        super().__init__()
        self.type = type
        if interaction_mode == None:
            raise Warning('Agent needs interaction_mode')
        self.interaction_mode = interaction_mode

        if price_limit == None:
            raise Warning('Everyone has a price!')
        self.price_limit = price_limit

        #determine initial goal price
        if initial_price == None:
            initial_price = self.price_limit
        else:
            if self.type == 'buyer':
                initial_price = min(initial_price, self.price_limit)
            elif self.type == 'seller':
                initial_price = max(initial_price, self.price_limit)

        self.goal_prices = [initial_price] #initial value

    def adjust_price(self, success = None, set_price = None):
        if set_price != None:
            self.goal_prices.append(set_price)
        else:
            if success == None:
                raise Warning('Need to know outcome to adjust price')
            #1, with just a touch of variability to avoid weird states
            if PRICE_ADJUST_MODE == 'gauss':
                adjust_amount = gauss(PRICE_ADJUST_MEAN, PRICE_ADJUST_DEV)
            if PRICE_ADJUST_MODE == 'chance':
                if random() < PRICE_ADJUST_CHANCE:
                    adjust_amount = PRICE_ADJUST_MEAN
                else:
                    adjust_amount = 0
            if success == True:
                if self.type == 'buyer': #and self.interaction_mode != 'seller_asks_buyer_decides':
                    self.goal_prices.append(self.goal_prices[-1] - adjust_amount)
                if self.type == 'seller':
                    self.goal_prices.append(self.goal_prices[-1] + adjust_amount)
            if success == False:
                if self.type == 'buyer': #and self.interaction_mode != 'seller_asks_buyer_decides':
                    self.goal_prices.append(min(self.goal_prices[-1] + adjust_amount, self.price_limit))
                if self.type == 'seller':
                    self.goal_prices.append(max(self.goal_prices[-1] - adjust_amount, self.price_limit))

class Meeting(object):
    """docstring for Meeting."""
    def __init__(self,
        buyer = None,
        seller = None,
        interaction_mode = None
    ):
        super().__init__()
        self.buyer = buyer
        self.seller = seller

        if self.seller == None or self.buyer == None:
            raise Warning('Meeting is missing a buyer or a seller')

        bid = self.buyer.goal_prices[-1]
        ask = self.seller.goal_prices[-1]

        if interaction_mode == None:
            raise Warning('Buyers and sellers have undefined interaction mode')

        self.transaction_price = None

        if interaction_mode == 'seller_asks_buyer_decides':
            if ask <= bid:
                self.transaction_price = ask
        elif interaction_mode == 'buyer_gets_it': #End of day desperate to sell
            self.transaction_price = bid
        else:
            if ask <= bid:
                self.transaction_price = uniform(ask, bid + 1)

            else:
                if interaction_mode == 'negotiate':
                    minimum = max(bid, seller.price_limit)
                    maximum = min(ask, buyer.price_limit)
                    if minimum <= maximum:
                        self.transaction_price = uniform(minimum, maximum + 1)
                elif interaction_mode == 'walk': #Not necessary, but here for clarity
                    self.transaction_price = None
                elif interaction_mode == 'mix_negotiate_and_walk':
                    if random() < 0.5: #Just 50-50 willingness for now, regardless of spread
                        minimum = max(bid, seller.price_limit)
                        maximum = min(ask, buyer.price_limit)
                        if minimum <= maximum:
                            self.transaction_price = uniform(minimum, maximum + 1)
                else:
                    raise Warning('Interaction mode not implemented')

class Session(object):
    """docstring for Session."""
    def __init__(
        self,
        buyers = None,
        sellers = None,
        interaction_mode = None,
        session_mode = None,
        meetings = []
    ):
        super().__init__()
        self.buyers = buyers
        self.sellers = sellers
        self.num_sellers = len(self.sellers)
        self.meetings = meetings
        self.interaction_mode = interaction_mode
        if session_mode == None:
            raise Warning('Session needs mode')
        self.session_mode = session_mode
        self.conduct_session()
        self.get_stats()

    def conduct_session(self):
        if self.session_mode == 'one_shot':
            for i in range(min( len(self.buyers), len(self.sellers) )):
                buyer = choice(self.buyers)
                self.buyers.remove(buyer)
                seller = choice(self.sellers)
                self.sellers.remove(seller)

                self.meetings.append(
                    Meeting(
                        buyer = buyer,
                        seller = seller,
                        interaction_mode = self.interaction_mode
                    )
                )

                #Adjust prices after meeting
                last_price = self.meetings[-1].transaction_price
                success = True
                if last_price == None: #Fail
                    success = False

                #In one special case, set the new buyer price exactly
                if success == True and \
                    self.interaction_mode == 'seller_asks_buyer_decides':
                    buyer.adjust_price(set_price = last_price)
                else:
                    buyer.adjust_price(success = success)
                seller.adjust_price(success = success)

            #The number of sellers fluctuates, so sometimes buyers don't get matched
            #and need their expectation upated for the next day
            for buyer in self.buyers:
                buyer.goal_prices.append(buyer.goal_prices[-1])

        if self.session_mode == 'rounds' or self.session_mode == 'rounds_w_concessions':
            disqualified = []
            sellers_this_round = self.sellers
            buyers_this_round = self.buyers

            round_count = 0
            while len(buyers_this_round) > 0 and len(sellers_this_round) > 0:
                round_count += 1
                print(' Round ' + str(round_count))


                #Filter out impossible-to-please agents
                max_buyer_price = max([x.goal_prices[-1] for x in buyers_this_round])
                min_seller_price = min([x.goal_prices[-1] for x in sellers_this_round])

                print('  Max price: ' + str(max_buyer_price))
                disqualified += [x for x in sellers_this_round if x.goal_prices[-1] > max_buyer_price]
                sellers_this_round = [x for x in sellers_this_round if x.goal_prices[-1] <= max_buyer_price]
                print('  ' + str(len(sellers_this_round)) + ' sellers')

                print('  Min price: ' + str(min_seller_price))
                disqualified += [x for x in buyers_this_round if x.goal_prices[-1] < min_seller_price]
                buyers_this_round = [x for x in buyers_this_round if x.goal_prices[-1] >= min_seller_price]
                print('  ' + str(len(buyers_this_round)) + ' buyers')


                #Prep container for creatures who will go to next round
                buyers_next_round = []
                sellers_next_round = []

                #Create pairs
                for i in range(min(len(buyers_this_round), len(sellers_this_round))):
                    buyer = choice(buyers_this_round)
                    buyers_this_round.remove(buyer)
                    seller = choice(sellers_this_round)
                    sellers_this_round.remove(seller)

                    self.meetings.append(
                        Meeting(
                            buyer = buyer,
                            seller = seller,
                            interaction_mode = self.interaction_mode
                        )
                    )

                    last_price = self.meetings[-1].transaction_price

                    if last_price == None:
                        sellers_next_round.append(seller)
                        buyers_next_round.append(buyer)
                    else: #success!
                        if self.interaction_mode == 'seller_asks_buyer_decides':
                            buyer.adjust_price(set_price = last_price)
                        else:
                            buyer.adjust_price(success = True)
                        seller.adjust_price(success = True)


                #Put any extras in next round
                for buyer in buyers_this_round:
                    buyers_next_round.append(buyer)
                for seller in sellers_this_round:
                    sellers_next_round.append(seller)

                #Reset for next loop
                buyers_this_round = buyers_next_round
                sellers_this_round = sellers_next_round

            #Put leftovers in disqualified. Will sometimes make an agen adjust
            #price even when they never got a chance, but that will be fairly rare.
            #Main point is to make sure agents who have failed do end up
            #adjusting price
            for buyer in buyers_this_round:
                disqualified.append(buyer)
            for seller in sellers_this_round:
                disqualified.append(seller)

            if self.session_mode != 'rounds_w_concessions':
                #Agents who never made a deal adjust prices
                for agent in disqualified:
                    agent.adjust_price(success = False)
            else:
                #Try again, making a concession on price and using the final
                #price for the adjustment. Purpose of this is to get transaction
                #count up.
                buyers_this_round = [x for x in disqualified if x.type == 'buyer']
                sellers_this_round = [x for x in disqualified if x.type == 'seller']

                #Similar to loop from before, but always negotiate to see if a
                #deal is possible within base limits
                while len(buyers_this_round) > 0 and len(sellers_this_round) > 0:
                    round_count += 1
                    #print(' Round ' + str(round_count))

                    #Filter out impossible-to-please agents
                    max_buyer_price = max([x.goal_prices[-1] for x in buyers_this_round]) + PRICE_CONCESSION
                    min_seller_price = min([x.goal_prices[-1] for x in sellers_this_round]) - PRICE_CONCESSION

                    #print('  Max price: ' + str(max_buyer_price))
                    disqualified += [x for x in sellers_this_round if \
                                    max(x.goal_prices[-1] - PRICE_CONCESSION, x.price_limit) > max_buyer_price]
                    sellers_this_round = [x for x in sellers_this_round if \
                                    max(x.goal_prices[-1] - PRICE_CONCESSION, x.price_limit) <= max_buyer_price]
                    #print('  ' + str(len(sellers_this_round)) + ' sellers')

                    #print('  Min price: ' + str(min_seller_price))
                    disqualified += [x for x in buyers_this_round if \
                                    min(x.goal_prices[-1] + PRICE_CONCESSION, x.price_limit) < min_seller_price]
                    buyers_this_round = [x for x in buyers_this_round if \
                                    min(x.goal_prices[-1] + PRICE_CONCESSION, x.price_limit) >= min_seller_price]
                    #print('  ' + str(len(buyers_this_round)) + ' buyers')

                    #Prep container for creatures who will go to next round
                    buyers_next_round = []
                    sellers_next_round = []

                    #Create pairs
                    for i in range(min(len(buyers_this_round), len(sellers_this_round))):
                        buyer = choice(buyers_this_round)
                        buyers_this_round.remove(buyer)
                        seller = choice(sellers_this_round)
                        sellers_this_round.remove(seller)

                        self.meetings.append(
                            Meeting(
                                buyer = buyer,
                                seller = seller,
                                interaction_mode = 'buyer_gets_it'
                            )
                        )

                        last_price = self.meetings[-1].transaction_price

                        if last_price == None:
                            disqualified.append(buyer)
                            disqualified.append(seller)
                        else: #success!
                            buyer.adjust_price(set_price = last_price)
                            seller.adjust_price(set_price = last_price)

                    #Put any extras in next round
                    for buyer in buyers_this_round:
                        buyers_next_round.append(buyer)
                    for seller in sellers_this_round:
                        sellers_next_round.append(seller)

                    #Reset for next loop
                    buyers_this_round = buyers_next_round
                    sellers_this_round = sellers_next_round

                for agent in disqualified:
                    agent.adjust_price(success = False)



    def get_stats(self):
        total_price = 0
        self.num_transactions = 0
        self.failed_meetings = 0
        for meet in self.meetings:
            if meet.transaction_price != None:
                total_price += meet.transaction_price
                self.num_transactions += 1
            else:
                self.failed_meetings += 1
        if self.num_transactions > 0:
            self.avg_price = total_price / self.num_transactions
        else:
            self.avg_price = None


class Market(object):
    """docstring for Market."""
    def __init__(
        self,
        agents = None,
        num_buyers = 0,
        num_sellers = 0,
        price_range = [0, 100],
        initial_price = None,
        interaction_mode = 'negotiate',
        session_mode = 'rounds',
        fluid_sellers = True
    ):
        super().__init__()
        self.price_range = price_range
        self.initial_price = initial_price

        #Interaction modes
        #Seller price set, buyer accept or deny
        #Always walk away
        #Always negotiate
        #Mix walk away and negotiation
        self.interaction_mode = interaction_mode
        self.session_mode = session_mode

        self.agents = agents
        if self.agents == None:
            self.num_buyers = num_buyers
            self.num_sellers = num_sellers
            self.generate_agents()

        self.sessions = []
        self.fluid_sellers = fluid_sellers

    def get_point_on_supply_curve(self, shape = 'linear'):
        if shape == 'linear':
            return randrange(self.price_range[0], self.price_range[1] + 1)
        if shape == 'quadratic':
            x = randrange(self.price_range[0], self.price_range[1] + 1)
            #return math.floor(x ** 2 / (2 * self.price_range[1]) + x / 2)
            return math.floor(x ** 2 / (self.price_range[1]))
            #return math.floor(x ** 3 / self.price_range[1] ** 2)

    def get_point_on_demand_curve(self, shape = 'linear'):
        if shape == 'linear':
            return randrange(self.price_range[0], self.price_range[1] + 1)
        if shape == 'quadratic': #Same as supply, taking advantage of symmetry
            x = randrange(self.price_range[0], self.price_range[1] + 1)
            #return math.floor(x ** 2 / (2 * self.price_range[1]) + x / 2)
            return math.floor(x ** 2 / (self.price_range[1]))
            #return math.floor(x ** 3 / self.price_range[1] ** 2)

    def generate_agents(self):
        self.agents = []

        for i in range(self.num_buyers):
            new_buyer = Agent(
                type = 'buyer',
                price_limit = self.get_point_on_demand_curve(shape = 'linear'),
                initial_price = self.initial_price,
                interaction_mode = self.interaction_mode
            )
            self.agents.append(new_buyer)
        for i in range(self.num_sellers):
            new_seller = Agent(
                type = 'seller',
                price_limit = self.get_point_on_supply_curve(shape = 'linear'),
                initial_price = self.initial_price,
                interaction_mode = self.interaction_mode
            )
            self.agents.append(new_seller)

    def new_session(self, session_mode = None):
        if session_mode == None:
            session_mode = self.session_mode

        buyers = []
        sellers = []

        if len(self.sessions) == 0:
            expected_price = self.initial_price
        else:
            expected_price = self.sessions[-1].avg_price

        #Sorts agents into buyers and sellers. Could be more generalized and
        #make all agents able to buy or sell. Not now, though.
        for agent in self.agents:
            if agent.type == 'seller':
                if self.fluid_sellers == True and \
                    expected_price != None and \
                    expected_price <= agent.price_limit:
                    #If seller sits session out, add to its goal_prices list
                    #to keep them the same length
                    agent.goal_prices.append(agent.price_limit)
                else:
                    sellers.append(agent)
            if agent.type == 'buyer':
                buyers.append(agent)

        self.sessions.append(
            Session(
                buyers = buyers,
                sellers = sellers,
                interaction_mode = self.interaction_mode,
                session_mode = session_mode,
                meetings = []
                #For some reason, the default meetings value doesn't work,
                #It uses the meetings from the previous sim unless the
                #meetings kwarg is specified.
            )
        )
