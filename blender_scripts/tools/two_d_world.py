import sys
sys.path.append('C:\\Users\\justi\\Documents\\CodeProjects\\Blender')
import imp
#import bpy
import math
from copy import deepcopy
from random import random, uniform
import pickle
import datetime
import population
import constants

#import alone doesn't check for changes in cached files
imp.reload(population)
from population import Population
imp.reload(constants)
from constants import *

import helpers
imp.reload(helpers)
from helpers import *

'''
Instantiates a population and manages the addition and motion of creatures
on in a 2D world.
'''

class TwoDWorld(Population):
    #TODO Add kwargs handling so things like radius and duration can be changed
    #on instantiation
    #This really just extends the population class by adding spatial data
    def __init__ (self, overlap_okay = True, **kwargs):
        super().__init__(**kwargs)
        self.radius = WORLD_RADIUS #Could make this a kwarg
        self.overlap_okay = overlap_okay
        self.simulate()
        self.populate_spacetime()
        print('Spacetime populated')
        self.spin_creatures()
        self.blob_stuff()
        print("TwoDWorld initialized")

    def save_sim_result(self):
        now = datetime.datetime.now()
        name = "2D " + now.strftime('%Y%m%dT%H%M%S')
        #name = 'test'
        result = os.path.join(
            SIM_DIR,
            name
        ) + ".pkl"
        if not os.path.exists(result):
            print("Writing simulation to %s" % (result))
            with open(result, "wb") as outfile:
                pickle.dump(self, outfile, pickle.HIGHEST_PROTOCOL)
        else:
            raise Warning(str(result) + " already exists")

    def populate_spacetime(self):
        creatures = self.creatures
        for creature in creatures:
            creature.locations = [None] * (self.duration + 1) #duration+1 states
            creature.velocities = [None] * (self.duration + 1)
        for t in range(self.duration + 1): #duration steps, duration+1 states
            for creature in creatures:
                if t < creature.birthday:
                    pass
                elif t == creature.birthday:
                    creature.velocities[t] = [
                        uniform(-0.05, 0.05),
                        uniform(-0.05, 0.05),
                        0
                    ]
                    self.place_new_creature(creature, t)
                elif t <= creature.deathday:
                    #After birthday but before/on deathday

                    #update position
                    a = creature.locations[t-1]
                    b = creature.velocities[t-1]
                    try:
                        creature.locations[t] = list(map(sum, zip(a, b)))
                    except:
                        print()
                        print(creature.name, "time = " + str(t))
                        print("B-day: " + str(creature.birthday))
                        print(creature.locations[t-1])
                        print(creature.velocities[t-1])
                        print(creature.parent, creature.parent.deathday, creature.parent.locations[creature.birthday])
                        print(creature.locations)
                        print('location', a, type(a))
                        print('velocity', b, type(b))
                        raise Warning('Type mismatch?')

                    #if position is out of bounds or too near another creature,
                    #fix
                    if RENDER_QUALITY != 'low':
                        #This takes a while with many creatures (quadratic),
                        #so don't bother with collisions on low setting.
                        self.repulsion(creature, t)
                    self.prevent_escape(creature, t)
                    #prevent_escape should come last to make sure creatures
                    #can't push each other out after prevent_escape

                    #update velocity to be used when updating position
                    #in next frame
                    a = creature.velocities[t-1]
                    b = [
                        uniform(-0.01, 0.01),
                        uniform(-0.01, 0.01),
                        0
                    ]
                    creature.velocities[t] = list(map(sum, zip(a, b)))
                    #v_max = max(creature.velocities[t].length, v_max)

                    self.apply_friction(creature, t)
                else:
                    #On or after deathday, do nothing. Ya dead!
                    pass


    #COULD make these Creature methods, but they're really only relevant in the
    #context of a 2D world, so leaving them here.
    def place_new_creature(self, creature, t, repetitions = 0, overlap_okay = None):
        if overlap_okay == None:
            overlap_okay = self.overlap_okay

        #If the creature has a parent, create it on top of its parent
        if creature.parent != None:
            creature.locations[t] = creature.parent.locations[t]
        else:
            creature.locations[t] = [
                uniform(
                    -self.radius + float(creature.alleles['size']),
                    self.radius - float(creature.alleles['size'])
                ),
                uniform(
                    -self.radius + float(creature.alleles['size']),
                    self.radius - float(creature.alleles['size'])
                ),
                0
            ]

            if overlap_okay == False:
                #check for collisions
                creatures = self.creatures
                for other_creature in creatures:
                    if creature != other_creature and other_creature.locations and \
                                            other_creature.locations[t] != None:
                        separation_vector = add_lists_by_element(
                            creature.locations[t],
                            other_creature.locations[t],
                            subtract = True
                        )
                        if vec_len(separation_vector) < \
                                float(creature.alleles['size']) + \
                                float(other_creature.alleles['size']):
                                # + \
                                #CREATURE_BUBBLE_WIDTH:
                            if repetitions > 10:
                                '''
                                #This code was in progress when I decided it's not
                                #actually important to handle overpopulation well.
                                #If you want to handle it well, you'd need to
                                #exterminate the dead creature's whole lineage.
                                #Right now, the code just kills the creature itself.

                                for a in range(t, self.duration):
                                    creature.locations[a] = None
                                    creature.velocities[a] = None
                                creature.deathday = t

                                self.revoke_existence(creature)
                                '''
                                alive = [x for x in creatures if \
                                            x. birthday < t and x.deathday > t]
                                print("There are %s living creatures at time = %s" \
                                        % (len(alive), t))
                                print("Too crowded, had to allow overlap")

                                self.place_new_creature(creature, t, overlap_okay = True)

                                '''creature.deathday = t

                                alive = [x for x in creatures if \
                                            x. birthday < t and x.deathday > t]
                                print("There are %s living creatures at time = %s" \
                                        % (len(alive), t))

                                print("Too crowded. A baby starved to death...")'''
                                return
                            repetitions += 1
                            self.place_new_creature(creature, t, repetitions = repetitions)
                            break

    def prevent_escape(self, cre, t):
        #if creature goes out of bounds, reverse relevent component
        #of previous velocity and recalculate position
        if abs(cre.locations[t][0]) + float(cre.alleles['size']) > self.radius:
            cre.velocities[t-1][0] *= -BOUNCE_DAMP_FACTOR
            a = cre.locations[t-1]
            b = cre.velocities[t-1]
            cre.locations[t] = list(map(sum, zip(a, b)))
        if abs(cre.locations[t][1]) + float(cre.alleles['size']) > self.radius:
            cre.velocities[t-1][1] *= -BOUNCE_DAMP_FACTOR
            a = cre.locations[t-1]
            b = cre.velocities[t-1]
            cre.locations[t] = list(map(sum, zip(a, b)))

    def repulsion(self, creature, t):
        #if creatures are too close, add a small repulsion to
        #previous velocity and recalculate position
        creatures = self.creatures
        for other_creature in creatures:
            if creature != other_creature and \
            creatures.index(other_creature) < creatures.index(creature) and \
            other_creature.locations and \
            other_creature.locations[t] != None:
                separation_vector = add_lists_by_element(
                                        creature.locations[t],
                                        other_creature.locations[t],
                                        subtract = True
                                    )
                if vec_len(separation_vector) < \
                    float(creature.alleles['size']) + \
                    float(other_creature.alleles['size']) + \
                    CREATURE_BUBBLE_WIDTH:
                        nudge = 0.01
                        nudge_vector = get_unit_vec(separation_vector)
                        for i in range(len(nudge_vector)):
                            nudge_vector[i] *= nudge
                        creature.velocities[t-1] = add_lists_by_element(
                                                        creature.velocities[t-1],
                                                        nudge_vector)
                        other_creature.velocities[t] = add_lists_by_element(
                                                        other_creature.velocities[t],
                                                        nudge_vector,
                                                        subtract = True)
                        '''a = creature.locations[t-1]
                        b = nudge_vector
                        creature.locations[t] = list(map(sum, zip(a, b)))'''

                        '''a = other_creature.locations[t-1]
                        b = [-x for x in nudge_vector]
                        other_creature.locations[t] = list(map(sum, zip(a, b)))'''

    def apply_friction(self, creature, t):
        vel = creature.velocities[t]
        length = math.sqrt(vel[0] * vel[0] + vel[1] * vel[1] + vel[2] * vel[2])
        if length > 0.1:
            nudge_vector = get_unit_vec(vel)
            nudge = -0.05
            for i in range(len(nudge_vector)):
                nudge_vector[i] *= nudge
            a = creature.velocities[t]
            b = nudge_vector
            creature.velocities[t] = list(map(sum, zip(a, b)))
            #creature.velocities[t] -= nudge_vector

    def spin_creatures(self):
        creatures = self.creatures
        for creature in creatures:
            creature.rotation = [None] * self.duration
            creature.rotation_vel = [None] * self.duration
            for t in range(self.duration):
                if t < creature.birthday:
                    pass
                elif t == creature.birthday:
                    creature.rotation[t] = uniform(-60, 60)
                    creature.rotation_vel[t] = uniform(-0.1, 0.1)

                elif t < creature.deathday:
                    #update position
                    creature.rotation[t] = creature.rotation[t-1] + creature.rotation_vel[t-1]
                    creature.rotation_vel[t] = creature.rotation_vel[t-1] + uniform(-0.005, 0.005)

    def blob_stuff(self):
        creatures = self.creatures
        for creature in creatures:
            creature.head_angle = [None] * self.duration
            creature.head_angle_vel = [None] * self.duration
            for t in range(self.duration):
                if t < creature.birthday:
                    pass
                elif t == creature.birthday:
                    creature.head_angle[t] = [
                        1,
                        uniform(-0.005, 0.005),
                        uniform(-0.005, 0.005),
                        uniform(-0.005, 0)
                    ]
                    creature.head_angle_vel[t] = [
                        0,
                        uniform(-0.005, 0.005),
                        uniform(-0.005, 0.005),
                        uniform(-0.005, 0.005)
                    ]
                    #places new creature if there's room, otherwise kills it :(
                    #self.place_new_creature(creature, t)
                elif t < creature.deathday:
                    #After birthday but before deathday

                    #update position
                    a = creature.head_angle[t-1]
                    b = creature.head_angle_vel[t-1]
                    creature.head_angle[t] = list(map(sum, zip(a, b)))

                    #Hard max on head angles
                    extrema = [
                        [1, 1],
                        [-0.2, 0.2],
                        [-0.2, 0.2],
                        [-0.2, 0]
                    ]
                    a = creature.head_angle[t]
                    for i in range(1, len(creature.head_angle[t])):
                        if a[i] < extrema[i][0]:
                            a[i] = extrema[i][0]
                        if a[i] > extrema[i][1]:
                            a[i] = extrema[i][1]

                    #update velocity to be used when updating position
                    #in next frame
                    a = creature.head_angle_vel[t-1]
                    b = [
                        0,
                        uniform(-0.002, 0.002),
                        uniform(-0.002, 0.002),
                        uniform(-0.002, 0.002)
                    ]
                    #Shift the acceleration distribution toward neutral
                    for i in range(1, len(b)):
                        go_back = -creature.head_angle[t][i] / 1000
                        b[i] += go_back
                    creature.head_angle_vel[t] = list(map(sum, zip(a, b)))
