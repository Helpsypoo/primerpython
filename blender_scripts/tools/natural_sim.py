import imp
from random import uniform

import bobject
imp.reload(bobject)
from bobject import *

import helpers
imp.reload(helpers)
from helpers import *

DEFAULT_DAY_LENGTH = 400
BLENDER_UNITS_PER_WORLD_UNIT = 1 / 20
CREATURE_HEIGHT = 13

class CreatureDay(object):
    """docstring for CreatureDay."""
    def __init__(
        self,
        creature = None,
        date = 0
    ):
        if creature == None:
            raise Warning("CreatureDay must belong to a creature")
        self.creature = creature
        self.date = date
        self.locations = []
        self.headings = []
        self.fed = []
        self.energies = []

        self.death_time = None

class Creature(object):
    def __init__(
        self,
        speed = 1,
        size = 1,
        sense = 1,
        parent = None
    ):
        self.speed = speed
        self.size = size
        self.sense = sense
        self.parent = parent

        self.days = []

        self.bobject = None

    def new_day(self, date = 0):
        new_day = CreatureDay(creature = self, date = date)
        if len(self.days) == 0:
            new_day.locations.append([0, 0, CREATURE_HEIGHT * self.size])
            new_day.headings.append(0)
        else:
            new_day.locations.append(
                self.days[-1].locations[-1]
            )
            #TODO: Make this depend on first location. Creatures should start
            #heading toward the center... ish
            new_day.headings.append(0)

        new_day.fed.append(0)
        new_day.energies.append(100)

        self.days.append(new_day)


    def take_step(self):
        ##Update heading
        day = self.days[-1]

        day.headings.append(day.headings[-1] + uniform(-0.1, 0.1))
        day.locations.append([
            day.locations[-1][0] + math.cos(day.headings[-1]) * self.speed,
            day.locations[-1][1] + math.sin(day.headings[-1]) * self.speed,
            day.locations[-1][2]
        ])
        day.energies.append(day.energies[-1] - self.size - self.speed - self.sense)


    def add_to_blender(self, appear_time = None, world = None):
        #Note that this is not a subclass of bobject
        if appear_time == None:
            raise Warning("Must define appear_time to add creature to Blender")
        if world == None:
            raise Warning("Must define world to add creature to Blender")

        cre_bobj = import_object(
            'boerd_blob', 'creatures',
            location = scalar_mult_vec(
                self.days[0].locations[0],
                world.blender_units_per_world_unit
            ),
            scale = self.size,
            rotation_euler = [0, 0, self.days[0].headings[0]]
        )
        #Rotate creature so a ref_obj rotation_euler of [0, 0, 0] results in
        #an x-facing blob standing in the z direction
        cre_bobj.ref_obj.children[0].rotation_euler = [math.pi / 2, 0, math.pi / 2]

        #TODO: Make color depend on speed
        apply_material(cre_bobj.ref_obj.children[0].children[0], 'color3')

        #TODO: Make eye size depend on sense

        self.bobject = cre_bobj
        cre_bobj.add_to_blender(appear_time = appear_time)

class NaturalSim(object):
    """docstring for NaturalSim."""
    def __init__(
        self,
        food_count = 10,
        dimensions = [100, 100],
        day_length = DEFAULT_DAY_LENGTH,
        initial_creatures = None
    ):
        self.food_count = food_count
        self.dimensions = dimensions
        self.day_length = day_length
        self.date_records = []

        self.initial_creatures = initial_creatures
        if self.initial_creatures == None:
            self.initial_creatures = [Creature()]


    def gen_food_locs(self, date = None):
        locs = []
        for i in range(self.food_count):
            locs.append([
                uniform(-self.dimensions[0], self.dimensions[0]),
                uniform(-self.dimensions[1], self.dimensions[1]),
                3
            ])

        return locs

    def sim_next_day(self):
        date = len(self.date_records)

        if date == 0:
            creatures = self.initial_creatures
        else:
            #Find creatures that survived or were born yesterday
            pass

        for cre in creatures:
            cre.new_day(date = date)

        for t in range(self.day_length):
            for cre in creatures:
                #take step
                cre.take_step()
            #check for eating

        date_dict = {
            'date' : date,
            'food_locations' : self.gen_food_locs(),
            'creatures' : creatures,
            'anim_durations' : {
                'dawn' : 1, #Put out food
                'morning' : 1, #pause after setup
                'day' : 5, #creatures go at it
                'evening' : 1, #pause before reset
                'night' : 1 #reset
            }
        }
        self.date_records.append(date_dict)

class DrawnNaturalSim(Bobject):
    def __init__(
        self,
        *subbobjects,
        sim = None,
        blender_units_per_world_unit = BLENDER_UNITS_PER_WORLD_UNIT,
        **kwargs
    ):
        super().__init__(*subbobjects, **kwargs)
        self.sim = sim
        if self.sim == None:
            sim_kwargs = {}
            for param in ['food_count', 'dimensions', 'day_length']:
                if param in kwargs:
                    sim_kwargs[param] = kwargs[param]
            self.sim = NaturalSim(**sim_kwargs)

        self.blender_units_per_world_unit = blender_units_per_world_unit

    def animate_days(self):
        for i, date_record in enumerate(self.sim.date_records):
            """Place food"""
            for i, loc in enumerate(date_record['food_locations']):
                nom = import_object(
                    'goodicosphere', 'primitives',
                    location = scalar_mult_vec(
                        loc,
                        self.blender_units_per_world_unit
                    ),
                    scale = 0.15
                )
                apply_material(nom.ref_obj.children[0], 'color7')
                nom.ref_obj.parent = self.ref_obj
                delay = i * date_record['anim_durations']['dawn'] / len(date_record['food_locations'])
                nom.add_to_blender(
                    appear_time = self.start_time + self.elapsed_time + delay
                )

            """Place new creatures"""

            if date_record['date'] == 0:
                for cre in date_record['creatures']:
                    cre.add_to_blender(
                        appear_time = self.start_time + self.elapsed_time,
                        world = self
                    )
                    cre.bobject.ref_obj.parent = self.ref_obj
            else:
                for cre in date_record['creatures']:
                    if cre not in self.sim.date_records[i - 1]:
                        cre.add_to_blender(
                            appear_time = self.start_time + self.elapsed_time,
                            world = self
                        )
                        cre.bobject.ref_obj.parent = self.ref_obj

            self.elapsed_time += date_record['anim_durations']['dawn'] + \
                                            date_record['anim_durations']['morning']

            """
            ANIMATE LOCATION AND HEADING
            DO IT HERE
            """
            for t in range(DEFAULT_DAY_LENGTH):
                time_of_day = t / DEFAULT_DAY_LENGTH * date_record['anim_durations']['day']
                anim_time = self.start_time + self.elapsed_time + time_of_day
                frame = anim_time * FRAME_RATE

                for cre in date_record['creatures']:
                    obj = cre.bobject.ref_obj
                    for candidate_day in cre.days:
                        if candidate_day.date == date_record['date']:
                            day = candidate_day
                            break

                    obj.location = scalar_mult_vec(
                        day.locations[t],
                        self.blender_units_per_world_unit
                    )
                    obj.keyframe_insert(data_path = 'location', frame = frame)
                    obj.rotation_euler = [0, 0, day.headings[t]]
                    obj.keyframe_insert(data_path = 'rotation_euler', frame = frame)




    def add_to_blender(
        self,
        start_delay = 1,
        **kwargs
    ):
        if 'appear_time' not in kwargs:
            raise Warning('Need appear_time to add natural sim.')
        self.start_time = kwargs['appear_time']

        self.elapsed_time = start_delay #Will add to this as phases are
                                             #animated to keep them sequential

        plane = import_object(
            'xyplane', 'primitives',
            scale = [
                self.sim.dimensions[0] * self.blender_units_per_world_unit,
                self.sim.dimensions[1] * self.blender_units_per_world_unit,
                0
            ],
            location = (0, 0, 0),
            #rotation_euler = [math.pi / 2, 0, 0],
            name = 'sim_plane'
        )
        #print(plane.ref_obj.scale)
        apply_material(plane.ref_obj.children[0], 'color2')
        self.add_subbobject(plane)

        super().add_to_blender(**kwargs)
        self.animate_days()
        #self.add_creatures_to_blender()
        #self.set_world_keyframes()
