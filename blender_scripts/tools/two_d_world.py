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
    #This really just extends the population class by adding spatial data
    def __init__ (
        self,
        overlap_okay = True,
        frames_per_time_step = 1,
        world_bound_points = [],
        bound_mode = 'rect',
        **kwargs
    ):
        super().__init__(**kwargs)
        #bound points must be listed in clockwise order for bound
        #detection to work
        self.world_bound_points = world_bound_points
        self.radius = WORLD_RADIUS
        self.bound_mode = bound_mode
        self.set_bounding_rect() #For generating creature placements

        self.overlap_okay = overlap_okay
        self.frames_per_time_step = frames_per_time_step
        self.animated_duration = self.duration * self.frames_per_time_step
        self.simulate()
        self.populate_spacetime()
        print('Spacetime populated')
        self.spin_creatures()
        self.blob_stuff()
        print("TwoDWorld initialized")

    def set_bounding_rect(self):
        if self.bound_mode == 'points':
            points = self.world_bound_points
            xmin = math.inf
            xmax = -math.inf
            ymin = math.inf
            ymax = -math.inf

            for point in points:
                if point[0] < xmin: xmin = point[0]
                if point[0] > xmax: xmax = point[0]
                if point[1] < ymin: ymin = point[1]
                if point[1] > ymax: ymax = point[1]

            self.bounding_rect = [
                [xmin, xmax],
                [ymin, ymax]
            ]

        if self.bound_mode == 'rect' or self.bound_mode == 'circle':
            self.bounding_rect = [
                [-self.radius, self.radius],
                [-self.radius, self.radius]
            ]
            self.radius = WORLD_RADIUS #Could make this a kwarg

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
            creature.birthframe = creature.birthday * self.frames_per_time_step
            creature.deathframe = creature.deathday * self.frames_per_time_step
            creature.locations = [None] * (self.animated_duration + 1) #duration+1 states
            creature.velocities = [None] * (self.animated_duration + 1)
        for t in range(self.animated_duration + 1): #duration steps, duration+1 states
            print('   Spacetime for frame ' + str(t))
            for creature in creatures:
                if t < creature.birthframe:
                    pass
                elif t == creature.birthframe:
                    creature.velocities[t] = [
                        uniform(-0.05, 0.05),
                        uniform(-0.05, 0.05),
                        0
                    ]
                    self.place_new_creature(creature, t)
                elif t <= creature.deathframe:
                    #After birthframe but before/on deathframe

                    #update position
                    a = creature.locations[t-1]
                    b = creature.velocities[t-1]
                    try:
                        creature.locations[t] = list(map(sum, zip(a, b)))
                    except:
                        print()
                        print(creature.name, "time = " + str(t))
                        print("B-frame: " + str(creature.birthframe))
                        print(creature.locations[t-1])
                        print(creature.velocities[t-1])
                        print(creature.parent, creature.parent.deathframe, creature.parent.locations[creature.birthframe])
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
                    #On or after deathframe, do nothing. Ya dead!
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
                uniform(self.bounding_rect[0][0], self.bounding_rect[0][1]),
                uniform(self.bounding_rect[1][0], self.bounding_rect[1][1]),
                0
            ]

            #Relevant if bounds are not rectangular
            if self.is_point_in_bounds(creature.locations[t]) == False:
                #raise Warning("asdpfkawe;rljasdfljkahsdflkjh")
                self.place_new_creature(creature, t, repetitions = repetitions)

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
                                #actually important to handle drawspace-based
                                #overpopulation well.
                                #If you want to handle it well, you'd need to
                                #exterminate the dead creature's whole lineage.
                                #Right now, the code just kills the creature itself.

                                for a in range(t, self.duration):
                                    creature.locations[a] = None
                                    creature.velocities[a] = None
                                creature.deathframe = t

                                self.revoke_existence(creature)
                                '''
                                alive = [x for x in creatures if \
                                            x.birthframe <= t and x.deathframe > t]
                                print("There are %s living creatures at frame = %s" \
                                        % (len(alive), t))
                                print("Too crowded, had to allow overlap")

                                self.place_new_creature(creature, t, overlap_okay = True)

                                '''creature.deathframe = t

                                alive = [x for x in creatures if \
                                            x. birthday < t and x.deathframe > t]
                                print("There are %s living creatures at time = %s" \
                                        % (len(alive), t))

                                print("Too crowded. A baby starved to death...")'''
                                return
                            repetitions += 1
                            self.place_new_creature(creature, t, repetitions = repetitions)
                            break

    def is_point_in_bounds(self, point):
        inside = True
        if self.bound_mode == 'rect':
            if point[0] < -self.radius or \
               point[0] > self.radius or \
               point[1] < -self.radius or \
               point[1] > self.radius:
               inside = False

        if self.bound_mode == 'circle':
            dist = vec_len(point)
            if dist > self.radius:
                inside = False

        if self.bound_mode == 'points':
            total_angle = 0
            bound_points = self.world_bound_points #Shorter!
            for i in range(len(bound_points)):
                a = add_lists_by_element(bound_points[i - 1], point, subtract = True)
                b = add_lists_by_element(bound_points[i], point, subtract = True)

                #left-handed since the decisions was made to list points in
                #clockwise order
                cross = cross_product(b, a)
                #Only works when figure is in xy-plane
                angle = math.atan2(cross[2], dot_product(b, a))
                #print(" " + str(angle))
                total_angle += angle

            #print(point)
            #print("Total angle: " + str(total_angle))

            if total_angle < 6.28: #some slight tolerance on 2 pi.
                inside = False

        return inside

    def prevent_escape(self, cre, t):
        #if creature goes out of bounds, reverse relevent component
        #of previous velocity and recalculate position
        if self.bound_mode == 'rect':
            #Could probably ditch this in favor of the more general thing below
            #Would need to set world bounding points somewhere first, though
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
        if self.bound_mode == 'circle':
            raise Warning('Not implemented')
        if self.bound_mode == 'points':
            if self.is_point_in_bounds(cre.locations[t]) == False:
                self.correct_velocity(cre, t)


    def correct_velocity(self, cre, t):
        #check which wall(s) were bumped
        #could also add point bouncing if things sneak through convex
        #corners, but seems rare
        pos = cre.locations[t]
        prev = cre.locations[t - 1] #prev must be inside if this works
        if self.is_point_in_bounds(prev) == False:
            pass
            #print("Previous: " + str(prev))
            #print("Current: " + str(pos))
            raise Warning('Even the previous point is not in bounds')

        bound_points = self.world_bound_points #Shorter!
        correction_vecs = []
        for i in range(len(bound_points)):
            #print()
            #print("Bound point")
            a = add_lists_by_element(prev, bound_points[i - 1], subtract = True)
            b = add_lists_by_element(prev, bound_points[i], subtract = True)
            c = add_lists_by_element(bound_points[i], bound_points[i - 1], subtract = True)
            #print(a, b, c)

            intersect = do_segments_intersect(
                [pos, prev],
                [bound_points[i], bound_points[i-1]]
            )
            if not intersect:
                continue #If no intersection, check next wall segment

            """
            Older code finding segment crosses in a weirder way
            Keeping because it could potentially be useful for sensing
            close segments and avoiding 'corrected' velocities that
            carry a creature across a different segment. That would only
            happen with very weird shapes that will probably never come
            up, though. ¯\_(ツ)_/¯
            """
            """#find perpendicular distance (height of triangle)
            area = vec_len(cross_product(b, a)) / 2
            base = vec_len(c)
            height = 2 * area / base
            #print(str(height))
            if height > 0.2: #Could generalize, but works for now.
                #print('Far')
                continue #Not this segment, NEXT
            #print("Close")


            #if angles adjacent to wall are obtuse, it's not that wall
            lengths = [vec_len(a), vec_len(b), vec_len(c)]
            for length in lengths:
                pass
                #print(str(length))
            if lengths[0] > math.sqrt(pow(lengths[1], 2) + pow(lengths[2], 2)) or \
               lengths[1] > math.sqrt(pow(lengths[0], 2) + pow(lengths[2], 2)):
               #print('Beyond segment')
               continue
            #print('In shadow of segment')"""



            #I guess we're bouncing.
            #A single bounce would reverse and damp the perpendicular
            #component, but since there could be multiple bounces,
            #just store the corrections and add after looping
            vel = cre.velocities[t - 1]
            c_norm = get_unit_vec(c)
            #print()
            #print('vel: ' + str(vel))
            #print('c_norm: ' + str(c_norm))
            para_vel = scalar_mult_vec(
                c_norm,
                dot_product(vel, c_norm)
            )
            #print('para_vel: ' + str(para_vel))
            perp_vel = add_lists_by_element(vel, para_vel, subtract = True)
            #print('perp_vel: ' + str(perp_vel))
            correction_vecs.append(
                scalar_mult_vec(
                    perp_vel,
                    - (1 + BOUNCE_DAMP_FACTOR)
                )
            )
            #print('correction_vec: ' + str(correction_vecs[-1]))
            #print()
            """print("Added a correction")
            print(correction_vecs)
            print()"""

        #
        uncorrected_vel = deepcopy(cre.velocities[t-1])
        for vec in correction_vecs:
            cre.velocities[t-1] = add_lists_by_element(
                deepcopy(cre.velocities[t-1]),
                vec
            )

        a = cre.locations[t - 1]
        b = cre.velocities[t - 1]
        if self.is_point_in_bounds(list(map(sum, zip(a, b)))) == False:
            pass
            print()
            print("Previous position: " + str(prev))
            print("Uncorrected position: " + str(cre.locations[t]))
            print("Corrected position: " + str(list(map(sum, zip(a, b)))))
            print(correction_vecs)
            print()
            print("Uncorrected vel: " + str(uncorrected_vel))
            print("Corrected vel: " + str(cre.velocities[t-1]))
            print()
            #raise Warning("Correction didn't work")

        cre.locations[t] = list(map(sum, zip(a, b)))

        #recursive in case the new velocity causes the creature to cross a
        #different wall. Relevant in (literal) corner cases.
        #Since velocity is damped, this shouldn't get infinite.
        if self.is_point_in_bounds(cre.locations[t]) == False:
            print("Adding another bounce")
            self.correct_velocity(cre, t)

    def repulsion(self, creature, t):
        #if creatures are too close, add a small repulsion to
        #previous velocity and recalculate position
        creatures = self.creatures
        alive = [x for x in creatures if \
                    x.birthframe <= t and x.deathframe > t]
        for other_creature in alive:
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
            creature.rotation = [None] * (self.animated_duration + 1)
            creature.rotation_vel = [None] * (self.animated_duration + 1)
            for t in range(self.animated_duration):
                if t < creature.birthframe:
                    pass
                elif t == creature.birthframe:
                    creature.rotation[t] = uniform(-60, 60)
                    creature.rotation_vel[t] = uniform(-0.001, 0.001)

                elif t < creature.deathframe:
                    #update position
                    creature.rotation[t] = creature.rotation[t-1] + creature.rotation_vel[t-1]

                    creature.rotation_vel[t] = creature.rotation_vel[t-1] + uniform(-0.0001, 0.0001)
                    if abs(creature.rotation_vel[t]) > 0.1:
                        creature.rotation_vel[t] = creature.rotation_vel[t] / \
                                    abs(creature.rotation_vel[t]) * 0.01

    def blob_stuff(self):
        creatures = self.creatures
        for creature in creatures:
            creature.head_angle = [None] * (self.animated_duration + 1)
            creature.head_angle_vel = [None] * (self.animated_duration + 1)
            for t in range(self.animated_duration):
                if t < creature.birthframe:
                    pass
                elif t == creature.birthframe:
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
                elif t < creature.deathframe:
                    #After birthframe but before deathframe

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
