from random import random, choice, shuffle
from helpers import save_sim_result

DEFAULT_NUM_CREATURES = 6
MUTATION_CHANCE = 0#.05
MUTATION_VARIATION = 0.1
TRAIT_MODE = 'binary' #float or binary
FOOD_VALUE = 2
BASE_FOOD = 0

SHARE_FRACTION = 1/2
TAKE_FRACTION = 3/4
SUCKER_FRACTION = 1/4
FIGHT_FRACTION = 1/2
FIGHT_COST = 16/16


class Creature(object):
    """docstring for Creature."""
    def __init__(self, fight_chance = None, parent = None):
        super().__init__()

        self.fight_chance = fight_chance
        self.parent = parent

        self.days_log = []

class Food(object):
    """docstring for Food."""

    def __init__(self, index = None):
        super().__init__()
        if index == None:
            raise Warning('Food object needs index')
        self.index = index
        self.interested_creatures = []
        self.eaten = False

class Day(object):
    """docstring for Day."""

    def __init__(self, date = None, food_count = None, creatures = None):
        super().__init__()
        self.date = date

        self.food_objects = []
        for i in range(food_count):
            self.food_objects.append(Food(index = i))
        self.creatures = creatures
        self.contests = []

    def simulate_day(self):
        #Morning
        for cre in self.creatures:
            cre.days_log.append(
                {
                    'date' : self.date,
                    'food' : None,
                    'score' : 0
                }
            )

            uneaten = [x for x in self.food_objects if x.eaten == False]
            if len(uneaten) > 0:
                target_food = choice(uneaten)
                target_food.interested_creatures.append(cre)
                cre.days_log[-1]['food'] = target_food
                if len(target_food.interested_creatures) == 2:
                    #Food is marked as eaten during the contest
                    self.contests.append(
                        Contest(
                            food = target_food,
                            contestants = target_food.interested_creatures,
                            date = self.date
                        )
                    )
                if len(target_food.interested_creatures) == 3:
                    raise Warning("Too many blobs on the dance floor")

        #Lone creatures eat their food
        for food in [x for x in self.food_objects if x.eaten == False]:
            num = len(food.interested_creatures)
            if num == 1:
                food.eaten = True
                food.interested_creatures[0].days_log[-1]['score'] += FOOD_VALUE
            elif num > 1:
                raise Warning('Food has ' + str(num) + ' interested creatures. Too many.')


        '''#Afternoon
        for cre in self.creatures:
            uneaten = [x for x in self.food_objects if x.eaten == False]
            if len(uneaten) > 0:
                target_food = choice(uneaten)
                target_food.interested_creatures.append(cre)
                cre.days_log[-1]['afternoon_food'] = target_food
                if len(target_food.interested_creatures) == 2:
                    self.afternoon_contests.append(
                        Contest(
                            food = target_food,
                            contestants = target_food.interested_creatures,
                            time = 'afternoon'
                        )
                    )

        #Lone creatures eat their food
        for food in [x for x in self.food_objects if x.eaten == False]:
            num = len(food.interested_creatures)
            if num == 1:
                food.eaten = True
                food.eaten_time = 'afternoon'
                food.interested_creatures[0].days_log[-1]['score'] += 1
            elif num > 1:
                raise Warning('Food has ' + str(num) + ' interested creatures. Too many.')'''

        self.update_creatures()

    def update_creatures(self):
        next = []

        for cre in self.creatures:
            score = cre.days_log[-1]['score']
            survival_roll = random()
            if score > survival_roll:
                next.append(cre)

            #if score > 1:
            reproduce_roll = random()
            if score > 1 + reproduce_roll:
                baby_fight_chance = cre.fight_chance
                mutation_roll = random()
                if MUTATION_CHANCE > mutation_roll:
                    if TRAIT_MODE == 'binary':
                        if baby_fight_chance == 1:
                            baby_fight_chance = 0
                        elif baby_fight_chance == 0:
                            baby_fight_chance = 1
                        else:
                            raise Warning('Baby fight chance should be 0 or 1 but is not')
                    elif TRAIT_MODE == 'float':
                        nudge = choice([MUTATION_VARIATION, - MUTATION_VARIATION])
                        baby_fight_chance += nudge
                        baby_fight_chance = max(baby_fight_chance, 0)
                        baby_fight_chance = min(baby_fight_chance, 1)
                    else:
                        raise Warning('Nonbinary fight chance not implemented')

                next.append(
                    Creature(
                        fight_chance = baby_fight_chance,
                        parent = cre
                    )
                )

        self.next_creatures = next


class Contest(object):
    """docstring for Contest."""

    def __init__(self, contestants = None, food = None, date = None):
        super().__init__()
        self.contestants = contestants
        self.food = food
        self.date = date

        self.outcome = None
        self.winner = None

        #Determine strategies
        strat_0 = strat_1 = 'share'
        if self.contestants[0].fight_chance > random():
            strat_0 = 'fight'
        if self.contestants[1].fight_chance > random():
            strat_1 = 'fight'

        #Determine payouts
        if strat_0 == 'fight' and strat_1 == 'fight':
            #winner_index = choice([0, 1])
            #self.contestants[winner_index].days_log[-1]['score'] += 1
            self.contestants[0].days_log[-1]['score'] += BASE_FOOD + FOOD_VALUE * FIGHT_FRACTION - FIGHT_COST
            self.contestants[1].days_log[-1]['score'] += BASE_FOOD + FOOD_VALUE * FIGHT_FRACTION - FIGHT_COST
            self.outcome = 'fight'
        if strat_0 == 'fight' and strat_1 == 'share':
            self.contestants[0].days_log[-1]['score'] += BASE_FOOD + FOOD_VALUE * TAKE_FRACTION
            self.contestants[1].days_log[-1]['score'] += BASE_FOOD + FOOD_VALUE * SUCKER_FRACTION
            self.outcome = 'take'
            self.winner = self.contestants[0]
        if strat_0 == 'share' and strat_1 == 'fight':
            self.contestants[1].days_log[-1]['score'] += BASE_FOOD + FOOD_VALUE * TAKE_FRACTION
            self.contestants[0].days_log[-1]['score'] += BASE_FOOD + FOOD_VALUE * SUCKER_FRACTION
            self.outcome = 'take'
            self.winner = self.contestants[1]
        if strat_0 == 'share' and strat_1 == 'share':
            self.contestants[0].days_log[-1]['score'] += BASE_FOOD + FOOD_VALUE * SHARE_FRACTION
            self.contestants[1].days_log[-1]['score'] += BASE_FOOD + FOOD_VALUE * SHARE_FRACTION
            self.outcome = 'share'

        self.food.eaten = True

class World(object):
    """docstring for World."""

    def __init__(self, initial_creatures = None, food_count = 100):
        super().__init__()

        self.initial_creatures = initial_creatures
        if self.initial_creatures == None:
            self.generate_creatures()
        self.food_count = food_count

        self.calendar = []

    def new_day(
        self,
        food_count = None,
        save = False,
        filename = None,
        filename_seed = None
    ):
        if len(self.calendar) == 0:
            creatures = self.initial_creatures
        else:
            creatures = self.calendar[-1].next_creatures

        if food_count == None:
            food_count = self.food_count

        day = Day(
            creatures = creatures,
            date = len(self.calendar),
            food_count = food_count
        )

        day.simulate_day()
        self.calendar.append(day)

        if save == True:
            save_sim_result(self, filename, filename_seed, type = 'HAWKDOVE')


    def generate_creatures(self):
        self.initial_creatures = []
        for i in range(DEFAULT_NUM_CREATURES):
            cre = Creature(
                fight_chance = 0#i % 2
            )

            self.initial_creatures.append(cre)

        shuffle(self.initial_creatures)
