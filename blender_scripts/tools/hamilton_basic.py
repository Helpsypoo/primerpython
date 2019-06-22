from random import random, choice, shuffle

class Creature(object):
    """docstring for Creature."""
    def __init__(
        self,
        altruist = None,
        parents = None,
        mate_chance = None
    ):
        super().__init__()
        self.altruist = altruist
        if self.altruist == None:
            raise Warning("Altruism genotype not set")

        self.parents = parents
        self.mate_chance = mate_chance
        self.mating = False

class World(object):
    """docstring for World."""

    def __init__(
        self,
        num_initial_creatures = 10000,
        initial_frac_altruists = 0.1,
        base_mate_chance = 2/3,
        offspring = 3, #Per mating pair
        mate_chance_cost = 1/12,
        mate_chance_benefit = 1/3,
        completed_days = 0,
    ):
        super().__init__()
        self.num_initial_creatures = num_initial_creatures
        self.base_mate_chance = base_mate_chance
        self.offspring = offspring
        self.mate_chance_cost = mate_chance_cost
        self.mate_chance_benefit = mate_chance_benefit

        self.creatures = []
        for i in range(num_initial_creatures):
            alt = False
            if random() < initial_frac_altruists:
                alt = True
            self.creatures.append(
                Creature(
                    altruist = alt,
                    mate_chance = self.base_mate_chance
                )
            )
        self.completed_days = completed_days
        print_summary(self.completed_days, self.creatures)

    def new_generation(self):
        altruists = [x for x in self.creatures if x.altruist == True]
        for cre in altruists:
            #Each altruist helps one sibling at a cost to itself
            siblings = [x for x in self.creatures if x.parents == cre.parents]
            if len(siblings) > 0:
                recipient = choice(siblings)
                recipient.mate_chance += self.mate_chance_benefit
                cre.mate_chance -= self.mate_chance_cost

        for cre in self.creatures:
            #Decide who mates
            if random() < cre.mate_chance:
                cre.mating = True

        maters = [x for x in self.creatures if x.mating == True]
        shuffle(maters)
        next_creatures = []
        while len(maters) > 2:
            p1 = maters.pop(0)
            p2 = maters.pop(0)
            for j in range(3):
                next_creatures.append(
                    Creature(
                        altruist = choice([p1.altruist, p2.altruist]),
                        mate_chance = self.base_mate_chance,
                        parents = [p1, p2]
                    )
                )

        self.creatures = next_creatures
        self.completed_days += 1
        print_summary(self.completed_days, self.creatures)

def print_summary(days, creatures):
    string = 'Gen ' + str(days) + ': '

    num_creatures = len(creatures)
    altruists = [x for x in creatures if x.altruist == True]
    frac_altruists = len(altruists) / num_creatures


    string += str(num_creatures) + ' total, '
    string += str(round(frac_altruists * 100)) + '% altruists'

    print(string)


def main():
    world = World()

    num_gens = 30
    for i in range(num_gens):
        world.new_generation()

main()
