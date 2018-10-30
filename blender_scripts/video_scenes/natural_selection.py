import collections
import math

import imp
import scene
imp.reload(scene)
from scene import Scene

import svg_bobject
imp.reload(svg_bobject)
import tex_bobject
imp.reload(tex_bobject)
import tex_complex
imp.reload(tex_complex)
import gesture
imp.reload(gesture)
import graph_bobject
imp.reload(graph_bobject)
import natural_sim
imp.reload(natural_sim)

import helpers
imp.reload(helpers)
from helpers import *

class NaturalSelectionScene(Scene):
    def __init__(self):
        self.subscenes = collections.OrderedDict([
            ('intro', {'duration': 14}),
            ('env', {'duration': 100}), #31
        ])
        super().__init__()

    def play(self):
        super().play()
        #self.subscenes
        #self.duration

        #self.intro()
        self.environment()

    def intro(self):
        cues = self.subscenes['intro']
        st = cues['start']

        blob1 = import_object(
            'boerd_blob', 'creatures',
            location = [0, 0, 0],
            scale = 4,
            wiggle = True
        )
        apply_material(blob1.ref_obj.children[0].children[0], 'creature_color3')

        blob2 = import_object(
            'boerd_blob', 'creatures',
            location = [-5, 0, 0],
            scale = 4,
            wiggle = True
        )
        apply_material(blob2.ref_obj.children[0].children[0], 'creature_color7')

        blob3 = import_object(
            'boerd_blob', 'creatures',
            location = [-5, 0, 0],
            scale = 4,
            wiggle = True
        )
        apply_material(blob3.ref_obj.children[0].children[0], 'creature_color7')



        blob1.add_to_blender(appear_time = st + 1)

        second_blob_timing = 2
        blob1.move_to(new_location = [5, 0, 0], start_time = st + second_blob_timing)
        blob2.add_to_blender(appear_time = st + second_blob_timing)

        first_death_timing = 3
        blob1.disappear(disappear_time = st + first_death_timing + 0.5)

        third_blob_timing = 4
        blob3.add_to_blender(appear_time = st + third_blob_timing)
        blob3.move_to(new_location = [5, 0, 0], start_time = st + third_blob_timing)

        third_death_timing = 5
        blob3.disappear(disappear_time = st + third_death_timing + 0.5)

        stats_timing = 6
        #blue stats
        rep_chance = tex_bobject.TexBobject(
            'R = 7\%',
            '\\cancel{R = 7\%}',
            '\\text{Traits}',
            '\\text{Traits} \\longleftrightarrow \\text{Environment}',
            color = 'color2'
        )
        death_chance = tex_bobject.TexBobject(
            'D = 5\%',
            '\\cancel{D = 5\%}',
            color = 'color2'
        )

        stats = tex_complex.TexComplex(
            rep_chance, death_chance,
            multiline = True,
            line_height = 1.4,
            location = [4 / blob2.ref_obj.scale[0], 0, 0],
            scale = 2 / blob2.ref_obj.scale[0],
            align_y = 'centered'
        )
        stats.ref_obj.parent = blob2.ref_obj
        stats.add_to_blender(
            appear_time = st + stats_timing,
            subbobject_timing = [0, 60],
        )

        rep_chance.morph_figure(1, start_time = st + stats_timing + 2)
        death_chance.morph_figure(1, start_time = st + stats_timing + 2)

        death_chance.disappear(disappear_time = st + stats_timing + 3 + 0.5)
        stats.tex_bobjects = [rep_chance]
        rep_chance.morph_figure(2, start_time = st + stats_timing + 3)

        blob2.move_to(new_location = [-10, 0, 0], start_time = st + stats_timing + 4)
        rep_chance.morph_figure(3, start_time = st + stats_timing + 4)





        #Prep for next scene
        to_disappear = [blob2]
        for i, thing in enumerate(to_disappear):
            thing.disappear(disappear_time = cues['end'] - (len(to_disappear) - 1 - i) * 0.05)

    def environment(self):
        cues = self.subscenes['env']
        st = cues['start']

        cam_bobj = bobject.Bobject(
            location = [25, 0, 0],
            rotation_euler = [math.pi / 2, 0, math.pi / 2],
            name = "Camera Bobject"
        )
        cam_swivel = bobject.Bobject(
            cam_bobj,
            location = [0, 0, 0],
            rotation_euler = [0, -16 * math.pi / 180, -math.pi / 2],
            name = 'Cam swivel'
        )
        cam_swivel.add_to_blender(appear_time = 0, animate = False)
        #cam_bobj.add_to_blender(appear_time = 0, animate = False)
        cam_obj = bpy.data.objects['Camera']
        cam_obj.data.clip_end = 1000
        cam_obj.location = [0, 0, 0]
        cam_obj.parent = cam_bobj.ref_obj


        sim = natural_sim.DrawnNaturalSim(
            scale = 4,
            food_count = 10,
            initial_energy = 1500,
            dimensions = [75, 75],
            sim = 'ns_env_intro_3',
            initial_creatures = 3,
            location = [0, 0, 0],
            day_length_style = 'fixed_speed',
            #day_length_style = 'fixed_length'
            mutation_switches = [False, False, False]
        )

        #This stuff was for stringing sims together with different initial
        #creatures
        """sim.sim.food_count = 2
        new_set = [
            natural_sim.Creature(
                size = 1,
                speed = 1,
                sense = 1
            ),
        ]
        for cre in new_set:
            cre.world = sim.sim

        sim.sim.mutation_switches = [False, False, False]
        sim.sim.initial_energy = 800
        sim.sim.sim_next_day(save = False)#, custom_creature_set = new_set)
        sim.sim.sim_next_day(save = True)"""

        sim.add_to_blender(appear_time = st)

        sim.disappear(disappear_time = st + 31)

        #TODO:Spin cam swivel

        #Show new sim
        sim = natural_sim.DrawnNaturalSim(
            scale = 2,
            food_count = 40,
            initial_creatures = 20,
            #sim = 'decay_to_low_food',
            #sim = 'f200_5base_30sp',
            location = [0, 0, 0],
            #day_length_style = 'fixed_speed',
            day_length_style = 'fixed_length',
            mutation_switches = [False, False, False]
        )

        sim_length = 20
        for i in range(sim_length):
            save = False
            if i == sim_length - 1:
                save = True
            if i == 10:
                sim.sim.mutation_switches = [True, False, False]

            sim.sim.sim_next_day(save = save)

        for day in sim.sim.date_records:
            day['anim_durations']['day'] = 3

        sim.add_to_blender(appear_time = st + 33)

        cre_counts = []
        records = sim.sim.date_records
        time = 2 #start time
        print(len(records))
        print()
        for date in range(len(records)):
            #Add count at date to list, for the counter tex_bobject
            if date == 10:
                print()
            cre_counts.append(str(len(records[date]['creatures'])))
            print(cre_counts[-1])
