import math
from random import random, choice, shuffle
from helpers import save_sim_result

DEFAULT_NUM_CREATURES = 11000
MUTATION_CHANCE = 0.01
MUTATION_VARIATION = 0.1
TRAIT_MODE = 'float' #float or binary
FOOD_VALUE = 1
BASE_FOOD = 0


SHARE_FRACTION = 1/2
HAWK_TAKE_FRACTION = 3/4
SUCKER_FRACTION = 1/4
FIGHT_FRACTION = 0


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

        self.creatures = creatures


        food_count = int(math.floor(len(creatures)) / 2) #Make sure there's a food for every
                                               #two creatures. Except there will
                                               #be an odd one out. But they
                                               #survive anyway


        self.food_objects = []
        for i in range(food_count):
            self.food_objects.append(Food(index = i))
        self.contests = []

    def simulate_day(self):
        #Morning

        shuffled_cres = self.creatures.copy()
        shuffle(shuffled_cres)

        for cre in shuffled_cres:
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
            raise Warning('Should be node of these')
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

        scores = []
        nums = []
        for i in range(11):
            score = 0
            num = 0
            for cre in self.creatures:
                if int(cre.fight_chance * 10) == i:
                    score += cre.days_log[-1]['score']
                    num += 1
            scores.append(score)
            nums.append(num)

        total = sum(scores)

        nums_offspring = []
        for score in scores:
            frac = score / total
            num_offspring = round(frac * DEFAULT_NUM_CREATURES)
            nums_offspring.append(num_offspring)

        '''avgs = []
        for num, score in zip(nums, scores):
            if num > 0:
                avgs.append(score/num)
            else:
                avgs.append(0)
        print(avgs)
        offsprings_per = []
        for num, num_offspring in zip(nums, nums_offspring):
            if num > 0:
                offsprings_per.append(num_offspring/num)
            else:
                offsprings_per.append(0)
        print(offsprings_per)
        print()'''

        next = []
        for i, num_offspring in enumerate(nums_offspring):
            baby_fight_chance = i / 10
            for i in range(num_offspring):
                mutation_roll = random()
                if MUTATION_CHANCE > mutation_roll:
                    if TRAIT_MODE == 'binary':
                        raise Warning('Check baby fight chance')
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
            self.contestants[0].days_log[-1]['score'] += BASE_FOOD + FOOD_VALUE * FIGHT_FRACTION
            self.contestants[1].days_log[-1]['score'] += BASE_FOOD + FOOD_VALUE * FIGHT_FRACTION
            self.outcome = 'fight'
        if strat_0 == 'fight' and strat_1 == 'share':
            self.contestants[0].days_log[-1]['score'] += BASE_FOOD + FOOD_VALUE * HAWK_TAKE_FRACTION
            self.contestants[1].days_log[-1]['score'] += BASE_FOOD + FOOD_VALUE * SUCKER_FRACTION
            self.outcome = 'take'
            self.winner = self.contestants[0]
        if strat_0 == 'share' and strat_1 == 'fight':
            self.contestants[1].days_log[-1]['score'] += BASE_FOOD + FOOD_VALUE * HAWK_TAKE_FRACTION
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
                fight_chance = (i % 11) / 10
            )
            '''if i % 2 == 0:
                cre = Creature(
                    fight_chance = 0
                )
            else:
                cre = Creature(
                    fight_chance = 1
                )'''

            self.initial_creatures.append(cre)

        shuffle(self.initial_creatures)
