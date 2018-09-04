from random import random, choice
from copy import deepcopy
import imp
import creature
import constants
import math
import collections
#import alone doesn't check for changes in cached files
imp.reload(creature)
#from creature import Creature
imp.reload(constants)
from constants import *

'''
A collection of creatures over time.
'''

class Population(object):
    genes = {
        'color' : collections.OrderedDict([
            ("creature_color_1" , {
                    "birth_modifier" : 0,
                    "replication_modifier" : 1,
                    "mutation_chance" : DEFAULT_MUTATION_CHANCE,
                    "death_modifier" : 1
            }),
            ("creature_color_2" , {
                    "birth_modifier" : 0,
                    "replication_modifier" : 1,
                    "mutation_chance" : DEFAULT_MUTATION_CHANCE,
                    "death_modifier" : 1
            }),
            ("creature_color_3" , {
                    "birth_modifier" : 0,
                    "replication_modifier" : 1,
                    "mutation_chance" : DEFAULT_MUTATION_CHANCE,
                    "death_modifier" : 1
            }),
            ("creature_color_4" , {
                    "birth_modifier" : 0,
                    "replication_modifier" : 1,
                    "mutation_chance" : DEFAULT_MUTATION_CHANCE,
                    "death_modifier" : 1
            })
        ]),
        'shape' : collections.OrderedDict([
            ("shape1" , {
                    "birth_modifier" : 0,
                    "replication_modifier" : 1,
                    "mutation_chance" : DEFAULT_MUTATION_CHANCE,
                    "death_modifier" : 1
            }),
            ("shape2" , {
                    "birth_modifier" : 0,
                    "replication_modifier" : 1,
                    "mutation_chance" : DEFAULT_MUTATION_CHANCE,
                    "death_modifier" : 1
            })
        ]),
        'size' : collections.OrderedDict([
            ("1" , {
                    "birth_modifier" : 0,
                    "replication_modifier" : 1,
                    "mutation_chance" : DEFAULT_MUTATION_CHANCE,
                    "death_modifier" : 1
            }),
            ("0.5" , {
                    "birth_modifier" : 0,
                    "replication_modifier" : 1,
                    "mutation_chance" : DEFAULT_MUTATION_CHANCE,
                    "death_modifier" : 1
            })
        ])
    }

    def __init__(self, **kwargs):
        #super().__init__()
        self.creatures = []

        #Using class attribute Population.genes as a default
        self.genes = deepcopy(Population.genes)
        if 'sim_duration' in kwargs:
            self.duration = kwargs['sim_duration']
        else:
            self.duration = DEFAULT_WORLD_DURATION
        if 'gene_updates' in kwargs:
            self.updates = kwargs['gene_updates']
        else:
            self.updates = []
        if 'initial_creatures' in kwargs:
            self.initial_creatures = kwargs['initial_creatures']
        else:
            self.initial_creatures = 10

        if 'pop_cap' in kwargs:
            self.pop_cap = kwargs['pop_cap']
        else:
            self.pop_cap = DEFAULT_POP_CAP

        if 'name' in kwargs:
            self.name = kwargs['name']
        else:
            self.name = 'population'

        #Each update arg should be of the form
        #update = [gene, allele, property, value, frame]
        # e.g., ['shape', 'shape1', 'replication_modifier', 2, 20]
        '''if gene_updates != None:
            self.updates = gene_updates
        else:
            self.updates = []'''

    def simulate(self):
        self.creatures = [] #clear creatures each time so one population
                            #object can be used to generate multiple sets of
                            #sim data
        print('Simulating ' + self.name)
        num = 1
        if isinstance(self.initial_creatures, int):
            for i in range(self.initial_creatures):
                cre = creature.Creature() #Creature with default alleles
                cre.birthday = 0
                cre.name = cre.alleles['color'] + " " + \
                           cre.alleles['shape'] + " " + str(num)
                self.creatures.append(cre)
                num += 1
        elif isinstance(self.initial_creatures, list):
            for cre in self.initial_creatures:
                cre.birthday = 0
                cre.name = cre.alleles['color'] + " " + \
                           cre.alleles['shape'] + " " + str(num)
                self.creatures.append(cre)
                num += 1

        #self.apply_updates(0) #Catches any gene property changes at time 0
        self.duration = int(self.duration) #Might be a float if calculated, idk.
        for t in range(0, self.duration):
            self.apply_updates(t)

            self.death(t)
            self.replicate(t)
            self.spontaneous_birth(t)

        #Make sure all creatures die at the end. :(
        #This makes things smoother elsewhere by ensuring deathday is a number
        for cre in self.creatures:
            if cre.deathday == None:
                cre.deathday = self.duration + 1

        print("There are " + str(len(self.creatures)) + " creatures total in " + \
                self.name)

    def list_possible_genotypes(self):
        #Actually returns a list of creatures, one with each possible genotype
        possible_creatures = [creature.Creature()]
        for gene in self.genes:
            new_possible_creatures = []
            for allele in self.genes[gene]:
                for cre in possible_creatures:
                    creature_copy_plus_allele = deepcopy(cre)
                    creature_copy_plus_allele.alleles[gene] = allele
                    new_possible_creatures.append(creature_copy_plus_allele)
            possible_creatures = new_possible_creatures

        return possible_creatures

    def apply_updates(self, t):
        for update in self.updates:
            if update[4] == t:
                self.genes[update[0]][update[1]][update[2]] = update[3]

    def spontaneous_birth(self, t):
        candidates = self.list_possible_genotypes()
        for candidate in candidates:
            birth_chance = BASE_BIRTH_CHANCE
            for gene in candidate.alleles:
                birth_chance *= \
                    self.genes[gene][candidate.alleles[gene]]['birth_modifier']

            #If birth chance is greater than one, interpret whole number part
            #as an additional sure birth
            #print("Birth chance: " + str(birth_chance))
            while birth_chance > 1:
                sibling = deepcopy(candidate)
                self.birth(sibling, t + 1)
                birth_chance -= 1

            birth_roll = random()
            if birth_roll < birth_chance:
                self.birth(candidate, t + 1)

    def birth(self, baby, t):
        self.creatures.append(baby)
        baby.birthday = t

        #Give creature a color+shape name with unique number
        #TODO Makes names more meaningful, e.g., by species, if needed.
        num = 1
        name_list = self.get_creature_names()
        for creature in self.creatures:
            if baby.alleles['color'] + " " + baby.alleles['shape'] + \
                    " " + str(num) in name_list:
                num += 1
            else:
                baby.name = baby.alleles['color'] + " " + \
                    baby.alleles['shape'] + " " + str(num)
                break

    def replicate(self, t):
        alive = [cre for cre in self.creatures if \
            cre.deathday == None or cre.deathday > t]
        for cre in alive:
            replication_chance = BASE_REPLICATION_CHANCE
            #Death chance is here because I decided to share the crowding
            #effect evenly between replication and death. We need the death
            #chance to calculate the overall effect.
            death_chance = BASE_DEATH_CHANCE

            for gene in cre.alleles:
                replication_chance *= \
                    self.genes[gene][cre.alleles[gene]]\
                                                    ['replication_modifier']
                death_chance *= \
                    self.genes[gene][cre.alleles[gene]]['death_modifier']
            crowding_rep_mod = (replication_chance - death_chance) / self.pop_cap / 2
            pop_size = self.count_creatures_at_t(t)

            replicate_roll = random()
            if replicate_roll < replication_chance - crowding_rep_mod * pop_size:
                baby = creature.Creature()
                self.creatures.append(baby)
                #Assign genes, checking for mutations
                for gene in self.genes:
                    mutation_roll = random()
                    chances = self.genes[gene][cre.alleles[gene]]['mutation_chance']
                    if isinstance(chances, (float, int)):
                        if mutation_roll < chances:
                            other_options = deepcopy(self.genes[gene])
                            other_options.pop(cre.alleles[gene])
                            baby.alleles[gene] = choice(list(other_options.keys()))
                        else:
                            baby.alleles[gene] = cre.alleles[gene]
                    #Allow for different odds of mutating to different alleles
                    elif isinstance(chances, list):
                        cumulative_chance = 0
                        for chance, allele in zip(chances, self.genes[gene]):
                            cumulative_chance += chance
                            if mutation_roll < cumulative_chance:
                                baby.alleles[gene] = allele
                                break
                            baby.alleles[gene] = cre.alleles[gene]

                    else:
                        raise Warning('Mutation chance must be number or list')


                baby.birthday = t + 1
                baby.parent = cre

                #Give creature a color+shape name with unique number
                num = 1
                name_list = self.get_creature_names()
                for cre in self.creatures:
                    if baby.alleles['color'] + " " + baby.alleles['shape'] + \
                                                " " + str(num) in name_list:
                        num += 1
                    else:
                        baby.name = baby.alleles['color'] + " " + \
                                    baby.alleles['shape'] + " " + str(num)
                        cre.children.append(baby.name)
                        break

    def death(self, t):
        alive = [cre for cre in self.creatures if \
                    cre.deathday == None and cre.birthday <= t]

        pop_size = self.count_creatures_at_t(t)
        #Old
        #Simple function that ramps death chance up around the population cap
        #Default cap is 3000, so it mostly functions to stop crashes/freezes
        #when I put in the wrong parameters.
        #crowding_death_mod = 1 + (pop_size / self.pop_cap) ** 10

        for creature in alive:
            death_chance = BASE_DEATH_CHANCE
            #Replication chance is here because I decided to share the crowding
            #effect evenly between replication and death. We need the replication
            #chance to calculate the overall effect.
            replication_chance = BASE_REPLICATION_CHANCE
            for gene in creature.alleles:
                death_chance *= \
                    self.genes[gene][creature.alleles[gene]]['death_modifier']
                replication_chance *= \
                    self.genes[gene][creature.alleles[gene]]['replication_modifier']
            crowding_death_mod = (replication_chance - death_chance) / self.pop_cap / 2
            death_roll = random()
            #print('Death chance: ' + str(death_chance))
            if death_roll < death_chance + crowding_death_mod * pop_size:
                creature.deathday = t + 1

    def get_creature_names(self):
        name_list = [creature.name for creature in self.creatures]
        return name_list

    def count_creatures_at_t(self, t, creatures = None):
        if creatures == None:
            creatures = self.creatures
        count = 0
        for creature in creatures:
            if creature.birthday <= t:
                count += 1
            #print(creature.deathday)
            if creature.deathday != None and creature.deathday <= t:
                count -= 1

        return count

    def get_creature_count_by_t(
        self,
        size = 'any',
        shape = 'any',
        color = 'any'
    ):
        #Get list of creatures according to requirements
        creatures_to_count = []
        for creature in self.creatures:
            add = True
            if size != 'any':
                if creature.alleles['size'] != size:
                    add = False
            if shape != 'any':
                if creature.alleles['shape'] != shape:
                    add = False
            if color != 'any':
                if creature.alleles['color'] != color:
                    add = False
            if add:
                creatures_to_count.append(creature)

        creature_count_by_t = []
        count = 0
        #print(self.duration)
        for t in range(self.duration + 1):
            count = self.count_creatures_at_t(t, creatures = creatures_to_count)
            creature_count_by_t.append(count)

        return creature_count_by_t

#For testing
def main():
    pop = Population()
    pop.simulate(self.duration)
    count = pop.get_creature_count_by_t()
    for i in range(self.duration):
        print(count[i])
    print("population.py successfully run")

if __name__ == "__main__":
    main()
