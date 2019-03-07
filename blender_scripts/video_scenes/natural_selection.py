import collections
import math
import bpy

import imp
#import scene
#imp.reload(scene)
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
            ('card', {'duration': 14}),
            ('intro', {'duration': 14}),
            ('env', {'duration': 31}),
            ('base_sim', {'duration': 31}),
            ('spd', {'duration': 16}),
            ('spd_sim', {'duration': 16}),
            ('pkmn', {'duration': 16}),
            ('selfish', {'duration': 16}),
            ('size', {'duration': 16}),
            ('sense', {'duration': 16}),
            ('all', {'duration': 40}),
            ('famine', {'duration': 40}),
            ('gradual', {'duration': 40}),
            ('wws', {'duration': 40}),
        ])
        super().__init__()

    def play(self):
        super().play()

        #self.intro()
        #self.environment()
        #self.base_sim()
        #self.speed()
        #self.speed_sim()
        #self.pokemon()
        #self.selfish_gene()
        #self.size()
        self.sense()
        #self.all_traits()
        #self.sudden_famine()
        #self.gradual_famine()
        #self.evolution_diagram()
        #self.recap()
        #self.end_card()
        #self.thumbnail()

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



        blob1.add_to_blender(appear_time = 1)

        second_blob_timing = 6
        blob1.move_to(new_location = [5, 0, 0], start_time = second_blob_timing)
        blob2.add_to_blender(appear_time = second_blob_timing)

        first_death_timing = 7
        blob1.disappear(disappear_time = first_death_timing + 0.5)

        third_blob_timing = 8
        blob3.add_to_blender(appear_time =  third_blob_timing)
        blob3.move_to(new_location = [5, 0, 0], start_time =  third_blob_timing)

        third_death_timing = 10
        blob3.disappear(disappear_time =  third_death_timing + 0.5)

        stats_timing = 12.5
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
            appear_time =  stats_timing,
            subbobject_timing = [0, 90],
        )

        rep_chance.morph_figure(1, start_time =  19)
        death_chance.morph_figure(1, start_time =  19)

        death_chance.disappear(disappear_time = 24 + 0.5)
        stats.tex_bobjects = [rep_chance]
        rep_chance.morph_figure(2, start_time =  24)

        blob2.move_to(new_location = [-10, 0, 0], start_time =  25)
        rep_chance.morph_figure(3, start_time =  25)

        #Prep for next scene
        to_disappear = [blob2]
        for i, thing in enumerate(to_disappear):
            thing.disappear(disappear_time = 28 - (len(to_disappear) - 1 - i) * 0.05)

        cam_obj = bpy.data.objects['Camera']
        cam_bobj = bobject.Bobject(
            location = cam_obj.location,
            #location = [25, 0, 0],
            #rotation_euler = [math.pi / 2, 0, math.pi / 2],
            name = "Camera Bobject"
        )
        cam_swivel = bobject.Bobject(
            cam_bobj,
            location = [0, 0, 0],
            #rotation_euler = [0, -16 * math.pi / 180, -math.pi / 2],
            name = 'Cam swivel'
        )
        cam_swivel.add_to_blender(appear_time = 0, animate = False)
        #cam_bobj.add_to_blender(appear_time = 0, animate = False)
        cam_obj.data.clip_end = 1000
        cam_obj.location = [0, 0, 0]
        cam_obj.parent = cam_bobj.ref_obj

        sim = natural_sim.DrawnNaturalSim(
            scale = 2,
            sim = 'all_mut_f100_[True, True, True]_19',
            #initial_creatures = 3,
            location = [0, 0, 0],
            #day_length_style = 'fixed_speed',
            day_length_style = 'fixed_length'
            #mutation_switches = [False, False, False]
        )
        sim.add_to_blender(
            appear_time = 29,
            start_day = 15,
            end_day = 15
        )
        cam_bobj.move_to(
            new_location = [0, 0, 25],
            #new_angle = [0, 0, 0],
            #new_angle = [math.pi / 2, 0, math.pi / 2],
            start_time = 29.5
        )
        cam_swivel.move_to(
            new_angle = [74 * math.pi / 180, 0, 0],
            #new_angle = [0, -16 * math.pi / 180, -math.pi / 2],
            start_time = 29.5
        )
        sim.disappear(disappear_time = 37.5)

    def environment(self):

        '''cam_bobj = bobject.Bobject(
            location = [25, 0, 0],
            rotation_euler = [math.pi / 2, 0, math.pi / 2],
            name = "Camera Bobject"
        )
        cam_swivel = bobject.Bobject(
            cam_bobj,
            location = [0, 0, 1.5],
            rotation_euler = [0, -16 * math.pi / 180, -math.pi / 2],
            name = 'Cam swivel'
        )
        #cam_bobj.add_to_blender(appear_time = 0, animate = False)
        cam_obj = bpy.data.objects['Camera']
        cam_obj.data.clip_end = 1000
        cam_obj.location = [0, 0, 0]
        cam_obj.parent = cam_bobj.ref_obj'''

        cam_bobj, cam_swivel = cam_and_swivel(
            cam_location = [25, 0, 0],
            cam_rotation_euler = [math.pi / 2, 0, math.pi / 2],
            cam_name = "Camera Bobject",
            swivel_location = [0, 0, 1.5],
            swivel_rotation_euler = [0, -16 * math.pi / 180, -math.pi / 2],
            swivel_name = 'Cam swivel',
            #control_sun = True
        )
        cam_swivel.add_to_blender(appear_time = 0, animate = False)

        sim = natural_sim.DrawnNaturalSim(
            scale = 4,
            #food_count = 10,
            #initial_energy = 1500,
            #dimensions = [75, 75],
            sim = 'ns_env_intro_4',
            #initial_creatures = 3,
            location = [0, 0, 0],
            #day_length_style = 'fixed_speed',
            day_length_style = 'fixed_length'
            #mutation_switches = [False, False, False]
        )
        sim.sim.date_records[0]['anim_durations'] = {
            'dawn' : 1, #Put out food and creatures
            'morning' : 0.5, #pause after setup
            'day' : 4, #creatures go at it
            'evening' : 0.5, #pause before reset
            'night' : 0.5 #reset
        }
        sim.sim.date_records[1]['anim_durations'] = {
            'dawn' : 0.5, #Put out food and creatures
            'morning' : 0.5, #pause after setup
            'day' : 3.5, #creatures go at it
            'evening' : 0.5, #pause before reset
            'night' : 0.5 #reset
        }
        sim.sim.date_records[2]['anim_durations'] = {
            'dawn' : 0.5, #Put out food and creatures
            'morning' : 0.5, #pause after setup
            'day' : 4, #creatures go at it
            'evening' : 0.5, #pause before reset
            'night' : 0.5 #reset
        }
        sim.sim.date_records[3]['anim_durations'] = {
            'dawn' : 0.5, #Put out food and creatures
            'morning' : 0, #pause after setup
            'day' : 2.5, #creatures go at it
            'evening' : 0.5, #pause before reset
            'night' : 0.5 #reset
        }
        sim.sim.date_records[4]['anim_durations'] = {
            'dawn' : 0.5, #Put out food and creatures
            'morning' : 0, #pause after setup
            'day' : 4.5, #creatures go at it
            'evening' : 0.5, #pause before reset
            'night' : 0.5 #reset
        }

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

        states = tex_bobject.TexBobject(
            '\\text{No food} \\rightarrow \\text{Death}',
            '\\text{One food} \\rightarrow \\text{Live on}',
            '\\text{Two food} \\rightarrow \\text{Replicate}',
            centered = True,
            location = [0, 0, 5],
            rotation_euler = [74 * math.pi / 180, 0, 0],
            scale = 2
        )

        sim.add_to_blender(appear_time = 42, start_delay = 2)
        #states.add_to_blender(appear_time = 51)
        #states.morph_figure(1, start_time = 56)
        #states.morph_figure(2, start_time = 62)

        #states.disappear(disappear_time = 71)
        sim.disappear(disappear_time = 71)

        #TODO:Spin cam swivel

        #Show new sim
        """sim = natural_sim.DrawnNaturalSim(
            scale = 2,
            food_count = 50,
            initial_creatures = 10,
            #sim = 'decay_to_low_food',
            sim = 'NAT20181031T145550',
            location = [0, 0, 0],
            #day_length_style = 'fixed_speed',
            day_length_style = 'fixed_length',
            mutation_switches = [True, True, True]
        )

        sim_length = 20
        for i in range(sim_length):
            save = False
            if i == sim_length - 1:
                save = True
            if i == 10:
                sim.sim.mutation_switches = [True, False, False]

            sim.sim.sim_next_day(save = save)

        print('Changing anim durations')
        for i, day in enumerate(sim.sim.date_records):
            fff = 2 ** i #fast-forward factor
            if fff > 64:
                fff = 64
            durs = day['anim_durations']
            print('Day ' + str(i))
            for key in durs:
                #durs[key] = max(durs[key] / fff, 1 / FRAME_RATE)
                durs[key] = durs[key] / fff
                print(key + ': ' + str(durs[key]))
            print()



        sim.add_to_blender(appear_time = st + 33)"""

        '''cre_counts = []
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
'''

    def base_sim(self):
        '''cues = self.subscenes['base_sim']
        st = cues['start']
        et = cues['end']'''

        cam_bobj, cam_swivel = cam_and_swivel(
            cam_location = [0, 0, 25],
            cam_rotation_euler = [0, 0, 0],
            cam_name = "Camera Bobject",
            swivel_location = [0, 0, 0],
            swivel_rotation_euler = [74 * math.pi / 180, 0, 0],
            swivel_name = 'Cam swivel',
            #control_sun = True
        )
        cam_swivel.add_to_blender(appear_time = 0)

        sim = natural_sim.DrawnNaturalSim(
            scale = 2,
            sim = 'base_sim_f100_[False, False, False]_6',
            #sim = 'ns_env_intro_3',
            location = [0, 0, 0],
            #day_length_style = 'fixed_speed',
            day_length_style = 'fixed_length'
        )
        #Sim was first run and saved with older, longer transition times
        for day in sim.sim.date_records:
            day['anim_durations']['dawn'] = 0.5
            day['anim_durations']['morning'] = 0.25
            day['anim_durations']['evening'] = 0.25
            day['anim_durations']['night'] = 0.5

        total_animation_length = 15
        uncorrected = 0
        for record in sim.sim.date_records:
            durs = record['anim_durations']
            uncorrected += sum(durs.values())

        correction_factor = total_animation_length / uncorrected

        for record in sim.sim.date_records:
            durs = record['anim_durations']
            for key in durs:
                durs[key] *= correction_factor



        cam_swivel.move_to(
            new_angle = [74 * math.pi / 180, 0,  2 * math.pi],
            start_time = 75,
            end_time = 92
        )

        """sim.move_to(
            start_time = st + 2 + total_animation_length + 1,
            new_location = [-5.5, 0, 0],
            new_scale = 1
        )"""
        cam_bobj.move_to(
            new_location = [6.35, 3, 39],
            start_time = 93.5,
        )
        #cam_swivel.move_to(
        #    new_angle = [0, - math.pi / 2, cam_swivel.ref_obj.rotation_euler[2]],
        #    start_time = st + 2 + total_animation_length + 1,
        #)

        count_by_day = []
        for record in sim.sim.date_records:
            count_by_day.append(len(record['creatures']))

        g = graph_bobject.GraphBobject(
            count_by_day,
            x_range = [0, 7],
            y_range = [0, 100],
            x_label = '\\text{Days}',
            y_label = '\\text{N}',
            y_label_pos = 'end',
            width = 8,
            height = 7,
            location = [15.6, -0.5, 0],
            centered = True,
            tick_step = [1, 20],
            rotation_euler = [74 * math.pi / 180, 0, 0],
            scale = 1.3
        )

        #g.add_to_blender(appear_time = 93)
        sim.add_to_blender(
            appear_time = 74,
            start_day = 0,
            #end_day = 0
        )

        '''g.move_to(
            new_location = [5, -0.5, 0],
            start_time = st + 2 + total_animation_length + 1
        )'''
        '''g.animate_function_curve(
            start_time = 95,
            end_time = 98
        )'''

        to_disappear = [sim, g]
        for i, thing in enumerate(to_disappear):
            thing.disappear(disappear_time = 117.5 - (len(to_disappear) - 1 - i) * 0.05)

    def speed(self):
        #ues = self.subscenes['spd']
        #st = cues['start']

        text = tex_bobject.TexBobject(
            '\\text{First trait}',
            '\\text{First trait: Speed}',
            location = [0, 6, 0],
            scale = 3,
            color = 'color2',
            centered = True
        )

        text.add_to_blender(appear_time = 118)
        text.morph_figure(1, start_time = 120)

        blob = import_object(
            'boerd_blob', 'creatures',
            location = [0, -2, 0],
            scale = 4,
            wiggle = True
        )
        dummy = natural_sim.Creature()
        dummy.apply_material_by_speed(
            obj = blob.ref_obj.children[0].children[0],
            bobj = blob,
            spd = 1,
        )
        #apply_material(blob.ref_obj.children[0].children[0], 'creature_color3')
        blob.add_to_blender(appear_time = 122)

        def f_blob():
            f_blob = import_object(
                'boerd_blob', 'creatures',
                location = [0, -2, 0],
                scale = 4,
                wiggle = True
            )
            '''apply_material(f_blob.ref_obj.children[0].children[0], 'creature_color7')
            mix = natural_sim.MUTATION_VARIATION / natural_sim.SPEED_PER_COLOR
            color = mix_colors(COLORS_SCALED[2], COLORS_SCALED[6], mix)
            obj = f_blob.ref_obj.children[0].children[0]
            f_blob.color_shift(
                duration_time = None,
                color = color,
                start_time = 0,
                shift_time = 1 / FRAME_RATE,
                obj = obj
            )'''

            dummy.apply_material_by_speed(
                obj = f_blob.ref_obj.children[0].children[0],
                bobj = f_blob,
                spd = 1.1,
            )

            f_blob.add_to_blender(appear_time = 127)
            f_blob.move_to(
                new_location = [8, -2, 0],
                start_time = 127
            )

            return f_blob
        f_blob = f_blob()

        def s_blob():
            s_blob = import_object(
                'boerd_blob', 'creatures',
                location = [0, -2, 0],
                scale = 4,
                wiggle = True
            )
            '''apply_material(s_blob.ref_obj.children[0].children[0], 'creature_color8')
            mix = natural_sim.MUTATION_VARIATION / natural_sim.SPEED_PER_COLOR
            color = mix_colors(COLORS_SCALED[2], COLORS_SCALED[7], mix)
            obj = s_blob.ref_obj.children[0].children[0]
            s_blob.color_shift(
                duration_time = None,
                color = color,
                start_time = 0,
                shift_time = 1 / FRAME_RATE,
                obj = obj
            )'''
            dummy.apply_material_by_speed(
                obj = s_blob.ref_obj.children[0].children[0],
                bobj = s_blob,
                spd = 0.9,
            )
            s_blob.add_to_blender(appear_time = 125.75)
            s_blob.move_to(
                new_location = [-8, -2, 0],
                start_time = 125.75
            )

            return s_blob
        s_blob = s_blob()

        to_disappear = [f_blob, s_blob]
        for thing in to_disappear:
            thing.disappear(disappear_time = 136)

        blob.move_to(
            new_location = [-10, 0.5, 0],
            new_scale = 2,
            start_time = 135.5
        )

        rf_blob = import_object(
            'boerd_blob', 'creatures',
            location = [-10, 0.5, 0],
            scale = 2,
            wiggle = True
        )
        apply_material(rf_blob.ref_obj.children[0].children[0], 'creature_color7')
        rf_blob.add_to_blender(appear_time = 136.5)
        rf_blob.move_to(
            new_location = [-10, -5, 0],
            start_time = 136.5
        )
        obj = rf_blob.ref_obj.children[0].children[0]
        shift_frames = 60
        color_set = [COLORS_SCALED[4], COLORS_SCALED[3], COLORS_SCALED[5]]
        num = len(color_set)
        for i in range(num):
            rf_blob.color_shift(
                duration_time = None,
                color = color_set[i],
                start_time = 137.5 + i * shift_frames / num / FRAME_RATE,
                shift_time = shift_frames / num,
                obj = obj
            )

        def slow_move():
            scale = 2
            arrow = gesture.Gesture(
                gesture_series = [
                    {
                        'type': 'arrow',
                        'points': {
                            'tail': (-11 / scale, 0.25, 0),
                            'head': (2 / scale, 0.25, 0)
                        }
                    },
                ],
                scale = scale,
                color = 'color2'
            )

            arrow.add_to_blender(appear_time = 139, transition_time = 2 * OBJECT_APPEARANCE_TIME)
            blob.move_to(
                new_angle = [0, math.pi / 2, 0],
                start_time = 139 - 0.2# st + 9.8
            )
            blob.move_to(
                new_location = [4, 0.5, 0],
                start_time = 139,
                end_time = 140
            )
            blob.move_to(
                new_angle = [0, 0, 0],
                start_time = 140 - 0.3#st + 10.7
            )

            time = list(range(0,11))
            time = [x/10 for x in time]
            time_exprs = [('\\text{Time}=' + str(x)) for x in time]
            print(time_exprs)

            slow_time = tex_bobject.TexBobject(
                *time_exprs,
                location = [6, 1, 0],
                transition_type = 'instant'
            )
            slow_time.add_to_blender(appear_time = 138)
            for i in range(1, len(time_exprs)):
                start_time = 139 + i * (1/len(time_exprs)) #1 is the movement duration
                slow_time.morph_figure(i, start_time = start_time)

            energy_exprs = [('\\text{Energy}=' + str(x)) for x in time]
            slow_energy = tex_bobject.TexBobject(
                *energy_exprs,
                location = [6, -0.5, 0],
                transition_type = 'instant'
            )
            slow_energy.add_to_blender(appear_time = 138)
            for i in range(1, len(energy_exprs)):
                start_time = 139 + i * (1/len(energy_exprs)) #1 is the movement duration
                slow_energy.morph_figure(i, start_time = start_time)

            return slow_time, slow_energy, arrow

        def fast_move():
            scale = 2
            arrow = gesture.Gesture(
                gesture_series = [
                    {
                        'type': 'arrow',
                        'points': {
                            'tail': (-11 / scale, -5.25 / scale, 0),
                            'head': (2 / scale, -5.25 / scale, 0)
                        }
                    },
                ],
                scale = scale,
                color = 'color2'
            )

            arrow.add_to_blender(appear_time = 139, transition_time = OBJECT_APPEARANCE_TIME)
            rf_blob.move_to(
                new_angle = [0, math.pi / 2, 0],
                start_time = 139 - 0.2,
                end_time = 139 - 0.2 + 0.4
            )
            rf_blob.move_to(
                new_location = [4, -5, 0],
                start_time = 139,
                #end_time = st + 11
            )
            rf_blob.move_to(
                new_angle = [0, 0, 0],
                start_time = 139.3,
            )

            time = list(range(0,6))
            time = [x/10 for x in time]
            time_exprs = [('\\text{Time}=' + str(x)) for x in time]
            print(time_exprs)

            fast_time = tex_bobject.TexBobject(
                *time_exprs,
                location = [6, -4.5, 0],
                transition_type = 'instant'
            )
            fast_time.add_to_blender(appear_time = 138)
            for i in range(1, len(time_exprs)):
                start_time = 139 + i * (0.5/len(time_exprs)) #0.5 is the movement duration
                fast_time.morph_figure(i, start_time = start_time)

            energy_exprs = [('\\text{Energy}=' + str(x*4)) for x in time]
            fast_energy = tex_bobject.TexBobject(
                *energy_exprs,
                location = [6, -6, 0],
                transition_type = 'instant'
            )
            fast_energy.add_to_blender(appear_time = 138)
            for i in range(1, len(energy_exprs)):
                start_time = 139 + i * (0.5/len(energy_exprs)) #0.5 is the movement duration
                fast_energy.morph_figure(i, start_time = start_time)

            return fast_time, fast_energy, arrow

        slow_time, slow_energy, slow_arrow = slow_move()
        fast_time, fast_energy, fast_arrow = fast_move()

        #for tex in [slow_time, fast_time]:
        #    tex.pulse(start_time = st + 12)

        #for tex in [slow_energy, fast_energy]:
        #    tex.pulse(start_time = st + 13)

        to_disappear = [
                        fast_energy,
                        fast_time,
                        rf_blob,
                        fast_arrow,
                        slow_energy,
                        slow_time,
                        blob,
                        slow_arrow,
                        text
                        ]
        for i, thing in enumerate(to_disappear):
            thing.disappear(disappear_time = 150 - (len(to_disappear) - 1 - i) * 0.05)

    def speed_sim(self):
        cues = self.subscenes['spd_sim']
        st = cues['start']
        et = cues['end']

        cam_bobj, cam_swivel = cam_and_swivel(
            cam_location = [0, 0, 25],
            cam_rotation_euler = [0, 0, 0],
            cam_name = "Camera Bobject",
            swivel_location = [0, 0, 0],
            swivel_rotation_euler = [74 * math.pi / 180, 0, 0],
            swivel_name = 'Cam swivel',
            #control_sun = True
        )
        cam_swivel.add_to_blender(appear_time = 0)

        sim = natural_sim.DrawnNaturalSim(
            scale = 2,
            sim = 'spd_mut_f100_[True, False, False]_69',
            #sim = 'ns_env_intro_3',
            location = [0, 0, 0],
            #day_length_style = 'fixed_speed',
            day_length_style = 'fixed_length'
        )

        first_day = 6

        #Set timing for first five days at 1 sec per day
        total_animation_length = 5
        uncorrected = 0
        for record in sim.sim.date_records:
            if record['date'] >= first_day and record['date'] < first_day + 5:
                durs = record['anim_durations']
                uncorrected += sum(durs.values())

        correction_factor = total_animation_length / uncorrected
        #print()
        #print('Correction factor for first section')
        #print(' ' + str(correction_factor))
        #print()

        for record in sim.sim.date_records:
            if record['date'] >= first_day and record['date'] < first_day + 5:
                durs = record['anim_durations']
                for key in durs:
                    #print(durs[key])
                    durs[key] *= correction_factor
                    #print(durs[key])
                    #print()

        #Set timing for the rest
        total_animation_length = 11
        uncorrected = 0
        for record in sim.sim.date_records:
            if record['date'] >= first_day + 5:
                durs = record['anim_durations']
                uncorrected += sum(durs.values())

        correction_factor = total_animation_length / uncorrected

        for record in sim.sim.date_records:
            if record['date'] >= first_day + 5:
                durs = record['anim_durations']
                for key in durs:
                    durs[key] *= correction_factor

        #Move camera instead of sim, because moving or displaced sims don't function
        #well.
        cam_swivel.move_to(
            start_time = 153.5 + 2,
            new_location = [0, 0, 2],
        )

        '''g = graph_bobject.GraphBobject(
            location = [-1, 0, 9.5],
            rotation_euler = [74 * math.pi / 180, 0, 0],
            width = 12,
            x_range = 2.2,
            x_label = '\\phantom{a}\\text{Speed}',
            x_label_pos = 'end',
            height = 4,
            y_range = 20,
            y_label = 'N',
            y_label_pos = 'along',
            tick_step = [0.5, 20],
            centered = True,
            include_y = True,
            arrows = 'positive'
        )'''


        '''g.add_to_blender(appear_time = 0)
        g.move_to(
            new_location = [-1, 0, 4.5],
            start_time = 153.5 + 2
        )'''
        '''
        def count_by_speed(date, speed_vals, nat_sim):
            counts = []
            creatures = nat_sim.date_records[date]['creatures']
            #print(len(creatures))
            for spd in speed_vals:
                #print()
                #print(spd)
                count = 0
                for cre in creatures:
                    print(str(spd) + '   ' + str(cre.speed))
                    if round(cre.speed, 1) == spd:
                        count += 1
                count = len([x for x in creatures if round(x.speed, 1) == spd])
                #print(count)
                counts.append(count)
                #print(counts)
                #print()
            return counts

        def make_graph_bars(speed_vals, appear_time, dx):
            bars = []
            for spd in speed_vals:
                #print(spd)
                bar = g.add_bar(
                    appear_time = appear_time,
                    x = spd,
                    value = 0,
                    dx = dx
                )
                dummy = natural_sim.Creature()
                dummy.apply_material_by_speed(
                    bobj = bar,
                    spd = spd,
                )

                bars.append(bar)

            return bars

        def update_graph_bars(start_time, bars, counts, end_time = None):
            for i, bar in enumerate(bars):
                g.update_bar(
                    bar = bar,
                    new_value = counts[i],
                    start_time = start_time,
                    end_time = end_time
                )

        speed_vals = [x/10 for x in range(23)]
        appear_time = 0
        dx = 0.08
        bars = make_graph_bars(speed_vals, appear_time, dx)
        #print(speed_vals)
        counts = count_by_speed(6, speed_vals, sim.sim)
        update_graph_bars(0, bars, counts)

        def draw_possible_states():
            #fast state
            start_time = 156
            counts = []
            for spd in speed_vals:
                dev = 0.2
                avg = 1.6
                count = 30 * math.exp(- (spd - avg) ** 2 / (2 * dev ** 2) )
                counts.append(count)
            update_graph_bars(start_time, bars, counts)

            start_time = 158
            counts = []
            for spd in speed_vals:
                dev = 0.2
                avg = 0.5
                count = 30 * math.exp(- (spd - avg) ** 2 / (2 * dev ** 2) )
                counts.append(count)
            update_graph_bars(start_time, bars, counts)

            start_time = 162.5
            counts = []
            for spd in speed_vals:
                dev = 0.2
                avg = 1
                count = 30 * math.exp(- (spd - avg) ** 2 / (2 * dev ** 2) )
                counts.append(count)
            update_graph_bars(start_time, bars, counts)

            start_time = 165
            counts = []
            for spd in speed_vals:
                dev = 0.2
                avg1 = 0.5
                avg2 = 1.6
                count = 15 * math.exp(- (spd - avg1) ** 2 / (2 * dev ** 2) ) + \
                        15 * math.exp(- (spd - avg2) ** 2 / (2 * dev ** 2) )
                counts.append(count)
            update_graph_bars(start_time, bars, counts)

        '''
        #draw_possible_states()

        first_day_start = 172
        sim_appearance_time = 150.5

        #Find proper duration for first morning pause to fill talking time
        initial_day_durs = sim.sim.date_records[first_day]['anim_durations']
        first_morning_dur = first_day_start - \
                           sim_appearance_time - \
                           initial_day_durs['dawn'] - \
                           1 #For standard start_delay on drawn sims
        initial_day_durs['morning'] = first_morning_dur








        #Correct sim appearance time for start_day after 6
        actual_start_day = 48
        for record in sim.sim.date_records:
            if record['date'] < actual_start_day and record['date'] >= first_day :
                durs = record['anim_durations']
                sim_appearance_time += sum(durs.values())



        #6 -> 27
        #27 -> 48
        #48 -> 69





        sim.add_to_blender(
            appear_time = sim_appearance_time,
            #start_day = first_day,
            #end_day = first_day + 21
            start_day = actual_start_day,
            end_day = actual_start_day + 21
        )

        '''#Update bars each day
        for day in sim.sim.date_records:
            date = day['date']
            if date == 6: #Don't regraph the old days
                start_time = first_day_start - OBJECT_APPEARANCE_TIME / FRAME_RATE
                end_time = first_day_start

                counts = count_by_speed(date, speed_vals, sim.sim)
                update_graph_bars(start_time, bars, counts, end_time = end_time)

                #One the first day, the bar actually appears at the end of the
                #morning pause instead of at the end of the dawn stage. So
                #subtracting the morning duration from start time, since it's
                #added during the following loop.
                start_time = first_day_start - day['anim_durations']['morning']

            elif date > 6: #Don't regraph the old days
                prev_day_anims = sim.sim.date_records[date - 1]['anim_durations']
                start_time += prev_day_anims['morning'] + \
                              prev_day_anims['day'] + \
                              prev_day_anims['evening'] + \
                              prev_day_anims['night']

                #print(len(sim.sim.date_records[i]['creatures']))
                #print(counts)
                end_time = start_time + day['anim_durations']['dawn']

                counts = count_by_speed(date, speed_vals, sim.sim)
                update_graph_bars(start_time, bars, counts, end_time = end_time)
                start_time += day['anim_durations']['dawn']'''


        cam_swivel.move_to(
            start_time = 190,
            end_time = 203,
            new_angle = [74 * math.pi / 180, 0, 10 * math.pi / 180]
        )
        cam_swivel.move_to(
            start_time = 203,
            end_time = 216,
            new_angle = [74 * math.pi / 180, 0, 0 * math.pi / 180]
        )

        end = 216
        to_disappear = [sim]
        for i, thing in enumerate(to_disappear):
            thing.disappear(disappear_time = end - (len(to_disappear) - 1 - i) * 0.05)

    def pokemon(self):
        #cues = self.subscenes['pkmn']
        #st = cues['start']

        what = tex_bobject.TexBobject(
            '\\text{What?}',
            '\\text{What? SQUIRTLE is evolving!}',
            '\\text{What? SQUIRTLE is }\\xcancel{\\text{evolving!}}',
            '\\text{What? SQUIRTLE is entering}',
            location = [-11.5, -4, 0],
            scale = 2,
            color = 'color2',
            #centered = True
        )
        dev = tex_bobject.TexBobject(
            '\\text{a new developmental stage!}',
            location = [-11.5, -4.5, 0],
            scale = 2,
            color = 'color2',
            #centered = True
        )
        but = tex_bobject.TexBobject(
            '\\text{(But, importantly, not evolving in the biological sense of the word!)}',
            location = [-11.5, -6.5, 0],
            scale = 0.87,
            color = 'color2',
            #centered = True
        )

        what.add_to_blender(appear_time = 217)
        what.morph_figure(1, start_time = 218)
        what.morph_figure(2, start_time = 219)
        what.morph_figure(3, start_time = 220)
        what.move_to(new_location = [-11.5, -2, 0], start_time = 220)
        dev.add_to_blender(appear_time = 220)
        but.add_to_blender(appear_time = 223)

        to_disappear = [what, dev, but]
        for i, thing in enumerate(to_disappear):
            #thing.disappear(disappear_time = 224 - (len(to_disappear) - 1 - i) * 0.05)
            thing.move_to(
                displacement = [54, 0, 0],
                start_time = 224,
                end_time = 225
            )

    def selfish_gene(self):
        cues = self.subscenes['selfish']
        st = cues['start']

        sim = natural_sim.DrawnNaturalSim(
            scale = 2,
            #sim = 'spd_mut_f100_[True, False, False]_49',
            sim = 'spd_mut_f100_[True, False, False]_69',
            location = [0, 0, 0],
            day_length_style = 'fixed_speed',
            #day_length_style = 'fixed_length'
        )

        count_by_day = []
        avg_speed_by_day = []
        for record in sim.sim.date_records:
            count_by_day.append(len(record['creatures']))

            speeds = [x.speed for x in record['creatures']]
            avg = sum(speeds) / len(speeds)
            avg_speed_by_day.append(avg)


        g = graph_bobject.GraphBobject(
            count_by_day,
            x_range = [0, 60],
            y_range = [0, 100],
            x_label = '\\text{Days}',
            y_label = '\\text{N}',
            y_label_pos = 'end',
            width = 10,
            height = 10,
            location = [6.5, -0.5, 0],
            centered = True,
            tick_step = [10, 20],
        )
        g.add_to_blender(appear_time = 225)
        g.animate_function_curve(
            start_time = 230,
            end_time = 232,
        )




        g2 = graph_bobject.GraphBobject(
            avg_speed_by_day,
            x_range = [0, 60],
            y_range = [0, 2],
            x_label = '\\text{Days}',
            y_label = '\\text{Avg. Speed}',
            y_label_pos = 'end',
            width = 10,
            height = 10,
            location = [-6.5, -0.5, 0],
            centered = True,
            tick_step = [10, 0.5],
        )
        g2.add_to_blender(appear_time = 225)
        g2.animate_function_curve(
            start_time = 227,
            end_time = 229,
        )

        sg = tex_bobject.TexBobject(
            '\\text{"Selfish gene"}',
            location = [-8.5, -2, 0],
            color = 'color2',
            scale = 1.5
        )
        sg.add_to_blender(appear_time = 238.5)

        to_disappear = [sg, g, g2]
        for i, thing in enumerate(to_disappear):
            thing.disappear(disappear_time = 258.5 - (len(to_disappear) - 1 - i) * 0.05)

    def size(self):
        #cues = self.subscenes['size']
        #st = cues['start']

        text = tex_bobject.TexBobject(
            '\\text{Second trait: Size}',
            location = [0, 6, 0],
            scale = 3,
            color = 'color2',
            centered = True
        )

        text.add_to_blender(appear_time = 265)

        plane = import_object(
            'xyplane', 'primitives',
            scale = [8, 8, 0],
            location = [0, -6.2, -2.5],
            rotation_euler = [math.pi / 2, 0, 0],
            name = 'sim_plane'
        )
        plane.add_to_blender(appear_time = 265.5)

        blob = import_object(
            'boerd_blob', 'creatures',
            location = [-5, -4, -5],
            scale = 2.5,
            wiggle = True
        )
        apply_material(blob.ref_obj.children[0].children[0], 'creature_color3')
        blob.add_to_blender(appear_time = 266)

        s_blob = import_object(
            'boerd_blob', 'creatures',
            location = [5, -4, 0],
            scale = 2.5,
            wiggle = True
        )
        apply_material(s_blob.ref_obj.children[0].children[0], 'creature_color3')
        s_blob.add_to_blender(appear_time = 266.5)

        #Grow
        blob.move_to(
            new_scale = 5,
            new_location = [-5, -1.5, -5],
            start_time = 267.5,
            end_time = 269.5
        )

        #Go eat the other blob
        blob.move_to(
            new_angle = [0, math.pi / 4, 0],
            start_time = 271.3
        )
        blob.move_to(
            new_location = [1, -1.5, -2.5],
            start_time = 271.5,
            end_time = 272.5
        )
        blob.blob_scoop(start_time = 272, duration = 1)
        blob.eat_animation(start_frame = 272 * FRAME_RATE, end_frame = 273 * FRAME_RATE)


        s_blob.move_to(
            new_location = [5, 1, 0],
            new_angle = [0, math.pi / 4, 0],
            new_scale = 1.25,
            start_time = 271.5 + 0.7,
            end_time = 271.5 + 0.7 + 0.3
        )
        s_blob.move_to(
            new_location = blob.ref_obj.location,
            new_scale = 0,
            start_time = 272.5,
            end_time = 272.5 + 0.3
        )

        #look back at camera
        blob.move_to(
            new_angle = [0, 0, 0],
            start_time = 274.5
        )


        plane.disappear(disappear_time = 280.5)


        cost = tex_bobject.TexBobject(
            '\\substack{ \\text{Energy cost} \\\\ \\text{per time step} } \\sim \\text{size}^3',
            '\\substack{ \\text{Energy cost} \\\\ \\text{per time step} } = \\text{size}^3\\text{speed}^2',
            '\\substack{ \\text{Energy cost} \\\\ \\text{per time step} } \\sim \\frac{1}{2}mv^2',
            '\\substack{ \\text{Energy cost} \\\\ \\text{per time step} } = \\text{size}^3\\text{speed}^2',
            location = [5, -2, 0],
            scale = 2,
            color = 'color2',
            centered = True
        )

        blob.move_to(
            new_location = [-8, -2, 0],
            start_time = 281
        )
        cost.add_to_blender(appear_time = 281)
        cost.morph_figure(1, start_time = 298)
        cost.move_to(new_location = [4.5, -2, 0], start_time = 298)
        blob.move_to(new_location = [-9.5, -2, 0], start_time = 298)
        cost.morph_figure(2, start_time = 305.5)
        cost.morph_figure(3, start_time = 307.5)

        cost.disappear(disappear_time = 312.5)

        s_blob2 = import_object(
            'boerd_blob', 'creatures',
            location = [18, -4, 0],
            rotation_euler = [0, - math.pi / 2, 0],
            scale = 2.5,
            wiggle = True
        )
        apply_material(s_blob2.ref_obj.children[0].children[0], 'creature_color7')
        s_blob2.add_to_blender(appear_time = 312.5)

        s_blob2.move_to(
            new_location = [-2, -4, 0],
            start_time = 313,#st + 13
            end_time = 314
        )
        s_blob2.move_to(
            new_angle = [0, math.pi / 2, 0],
            start_time = 313.7# st + 13.25
        )
        s_blob2.move_to(
            new_location = [18, -4, 0],
            start_time = 314,#st + 13.5
            end_time = 315
        )

        blob.move_to(
            new_angle = [0, math.pi / 2, 0],
            start_time = 313.8, #st + 13.3#4.8
            end_time = 314.5
        )
        blob.move_to(
            new_location = [0, -2, 0],
            start_time = 314.2,#st + 13.5,
            end_time = 315.2#st + 14
        )
        blob.move_to(
            new_angle = [0, 0, 0],
            start_time = 317#st + 15
        )

        to_disappear = [text, blob]
        for i, thing in enumerate(to_disappear):
            thing.disappear(disappear_time = 324 - (len(to_disappear) - 1 - i) * 0.05)

    def sense(self):
        #cues = self.subscenes['sense']
        #st = cues['start']

        text = tex_bobject.TexBobject(
            '\\text{Third trait: Sense}',
            location = [0, 6, 0],
            scale = 3,
            color = 'color2',
            centered = True
        )

        text.add_to_blender(appear_time = 325)

        blob = import_object(
            'boerd_blob', 'creatures',
            location = [7, -2, -5.5],
            #location = [0, -2, 0],
            rotation_euler = [0, -math.pi / 2, 0],
            scale = 4,
            wiggle = True
        )
        apply_material(blob.ref_obj.children[0].children[0], 'creature_color3')
        blob.add_to_blender(appear_time = 326)

        food = import_object(
            'goodicosphere', 'primitives',
            location = [-1, -5, 0],
            scale = 0.5
        )
        apply_material(food.ref_obj.children[0], 'color7')
        food.add_to_blender(appear_time = 326)

        torus = import_object(
            'flat_torus', 'primitives',
            location = [0, -0.9, 0],
            rotation_euler = [math.pi / 2, 0, 0],
            scale = 2.5
        )
        apply_material(torus.ref_obj.children[0], 'color2')
        torus.add_to_blender(appear_time = 327.5)
        torus.ref_obj.parent = blob.ref_obj

        blob.move_to(
            new_location = [3, -2, -5.5],
            start_time = 331,
            end_time = 332
        )
        exclaim = tex_bobject.TexBobject(
            '\\text{!}',
            location = [0, 1.3, 0],
            rotation_euler = [0, math.pi / 2, 0],
            scale = 0.75
        )
        exclaim.ref_obj.parent = blob.ref_obj
        exclaim.add_to_blender(appear_time = 332)
        exclaim.disappear(disappear_time = 333.5)








        blob.move_to(
            new_angle = [0, -math.pi / 8, 0],
            start_time = 332.8
        )
        exclaim.move_to(
            new_angle = [0, math.pi / 8, 0],
            start_time = 332.8
        )
        blob.move_to(
            new_location = [0, -2, 0],
            start_time = 333,
            end_time = 334
        )
        blob.move_to(
            new_angle = [0, 0, 0],
            start_time = 333.8
        )



        blob.blob_scoop(start_time = 333.5, duration = 1)
        food.move_to(new_location = [-1, -1, 4], start_time = 333.5, end_time = 333.8)
        food.move_to(
            new_location = [-0.5, -1, 0],
            new_scale = 0,
            start_time = 333.8,
            end_time = 334.1
        )
        blob.eat_animation(start_frame = 333.5 * FRAME_RATE, end_frame = 334.1 * FRAME_RATE)


        torus.move_to(
            new_scale = 3.5,
            start_time = 339,
            end_time = 341,
        )
        torus.move_to(
            new_scale = 1.5,
            start_time = 341,
            end_time = 343
        )
        torus.move_to(
            new_scale = 2.5,
            start_time = 343,
            end_time = 345,
        )

        eyes = []
        for obj in blob.ref_obj.children[0].children:
            if 'Eye' in obj.name:
                eyes.append(obj)
        for eye in eyes:
            eye.keyframe_insert(data_path = 'scale', frame = 339 * FRAME_RATE)
            eye.scale = [
                1.5,
                1.5,
                1.5,
            ]
            eye.keyframe_insert(data_path = 'scale', frame = 341 * FRAME_RATE)
            eye.scale = [
                0.5,
                0.5,
                0.5,
            ]
            eye.keyframe_insert(data_path = 'scale', frame = 343 * FRAME_RATE)
            eye.scale = [
                1,
                1,
                1,
            ]
            eye.keyframe_insert(data_path = 'scale', frame = 345 * FRAME_RATE)


        cost = tex_bobject.TexBobject(
            '\\substack{ \\text{Total cost} \\\\ \\text{per time step} } = ',
            location = [-3, -1, 0],
            scale = 1.5,
            color = 'color2',
            centered = False
        )
        eq = tex_bobject.TexBobject(
            '\\text{size}^3\\text{speed}^2',
            '\\text{size}^3\\text{speed}^2 + \\text{sense}',
            location = [4.5, -1, 0],
            scale = 1.125,
            color = 'color2',
            centered = False
        )
        blob.move_to(
            new_location = [-7, -2, 0],
            start_time = 345
        )
        cost.add_to_blender(appear_time = 345.5)
        eq.add_to_blender(appear_time = 347)
        eq.morph_figure(1, start_time = 350.5)

        to_disappear = [text, blob, cost, eq]
        for i, thing in enumerate(to_disappear):
            thing.disappear(disappear_time = 354 - (len(to_disappear) - 1 - i) * 0.05)

    def all_traits(self):
        #cues = self.subscenes['all']
        #st = cues['start']

        cam_bobj, cam_swivel = cam_and_swivel(
            cam_location = [0, 0, 34],
            cam_rotation_euler = [0, 0, 0],
            cam_name = "Camera Bobject",
            swivel_location = [0, 0, 4],
            swivel_rotation_euler = [74 * math.pi / 180, 0, 0],
            swivel_name = 'Cam swivel',
            #control_sun = True
        )
        cam_swivel.add_to_blender(appear_time = 0)

        sim = natural_sim.DrawnNaturalSim(
            scale = 1.5,
            sim = 'all_mut_f100_[True, True, True]_19',
            location = [-6.5, 0, 0],
            day_length_style = 'fixed_length'
        )

        first_day = 6
        total_animation_length = 14
        uncorrected = 0
        for record in sim.sim.date_records:
            if record['date'] >= first_day:
                durs = record['anim_durations']
                uncorrected += sum(durs.values())

        correction_factor = total_animation_length / uncorrected

        for record in sim.sim.date_records:
            if record['date'] >= first_day:
                durs = record['anim_durations']
                for key in durs:
                    durs[key] *= correction_factor

        g = graph_bobject.GraphBobject3D(
            x_range = [0, 2],
            y_range = [0, 2],
            z_range = [0, 2],
            x_label = '\\text{Size}',
            y_label = '\\text{Sense}',
            z_label = '\\text{Speed}',
            width = 10,
            height = 10,
            depth = 10,
            #location = [8, 8, 4],
            location = [0, 8, 4],
            rotation_euler = [math.pi / 2, 0, 0],
            centered = True,
            tick_step = 0.5
        )

        tex = tex_bobject.TexBobject(
            '\\text{All traits varying}',
            scale = 2,
            location = [-6.5, 0, 8],
            rotation_euler = [74 * math.pi / 180, 0, 0],
            color = 'color2',
            centered = True
        )
        tex.add_to_blender(appear_time = 377)

        def draw_sim():
            sim.add_to_blender(
                appear_time = 377,
                start_day = 6,#7
                #end_day = 19
            )

        def draw_graph():
            cam_swivel.move_to(
                new_angle = [74 * math.pi / 180, 0, 20 * math.pi / 180],
                start_time = 90
            )
            cam_swivel.move_to(
                new_angle = [74 * math.pi / 180, 0, -20 * math.pi / 180],
                start_time = 100,
                end_time = 105
            )
            cam_swivel.move_to(
                new_angle = [74 * math.pi / 180, 0, 0],
                start_time = 105,
                end_time = 107
            )


            g.add_to_blender(appear_time = 364)

            point = g.add_point_at_coord(
                coord = [1, 1, 1],
                appear_time = 368,
            )
            apply_material(point.ref_obj.children[0], 'creature_color7')

            g_blob = import_object(
                'boerd_blob', 'creatures',
                location = [-9, 0, 1.8],
                rotation_euler = [math.pi / 2, 0, 80 * math.pi / 180],
                scale = 2
            )
            apply_material(g_blob.ref_obj.children[0].children[0], 'creature_color7')
            g_blob.add_to_blender(appear_time = 369)

            g.animate_point(
                end_coord = [0, 0, 0],
                start_time = 371,
                point = point
            )
            g.animate_point(
                end_coord = [0, 0, 1 * g.z_scale_factor],
                start_time = 372.5,
                point = point
            )
            g.animate_point(
                end_coord = [1, 0, 1 * g.z_scale_factor],
                start_time = 373,
                point = point
            )
            g.animate_point(
                end_coord = [1, 1, 1 * g.z_scale_factor],
                start_time = 373.75,
                point = point
            )

            g.move_to(
                new_location = [8, 8, 0], #0 instead of 4 because it doesn't properly handle z centering
                start_time = 376.5
            )
            g_blob.disappear(disappear_time = 377)
            point.disappear(disappear_time = 376.5)

            def draw_sim_points():
                cres_with_points = []
                cre_counts = []
                records = sim.sim.date_records
                time = 378 #start time
                #graph_point_leftovers = []

                for date in range(6, len(records)):
                    print("Updating graph for day " + str(date))

                    #Delete points for creatures the died
                    to_delete = []
                    for cre in cres_with_points:
                        #print(' A creature has a point')
                        if cre not in records[date]['creatures']:
                            #print(' taking point from creature')
                            cre.point.disappear(
                                disappear_time = time + 0.5,
                                #Will need duration in actual scene
                            )
                            to_delete.append(cre)
                    for cre in to_delete:
                        cres_with_points.remove(cre)
                    #print(' Now ' + str(len(cres_with_points)) + " cres have points")

                    #Add points for new creatures
                    for cre in records[date]['creatures']:
                        #print(" There's a cre")
                        if cre not in cres_with_points:
                            #print(' Giving a point')
                            point = g.add_point_at_coord(
                                coord = [
                                    cre.size + uniform(-0.03, 0.03),
                                    cre.sense + uniform(-0.03, 0.03),
                                    cre.speed + uniform(-0.03, 0.03),
                                ],
                                appear_time = time,

                                #Will need duration in actual scene
                            )
                            '''apply_material(
                                point.ref_obj.children[0],
                                cre.bobject.ref_obj.children[0].children[0].active_material
                            )'''
                            dummy = natural_sim.Creature()
                            dummy.apply_material_by_speed(
                                bobj = point,
                                spd = cre.speed,
                            )
                            cre.point = point
                            cres_with_points.append(cre)
                            #print(' Now ' + str(len(cres_with_points)) + " cres have points")

                    #Add time after day
                    time += records[date]['anim_durations']['dawn'] + \
                            records[date]['anim_durations']['morning'] + \
                            records[date]['anim_durations']['day'] + \
                            records[date]['anim_durations']['evening'] + \
                            records[date]['anim_durations']['night']


            draw_sim_points()

        def focus_on_graph():
            sun = bpy.data.objects['Sun']
            sun_bobj = bobject.Bobject(objects = [sun])

            sun_bobj.move_to(
                start_time = 0,
                new_angle = [math.pi / 2, 0, 0]
            )
            sun_bobj.add_to_blender(appear_time = 0)

            sim.disappear(disappear_time = 395)
            g.move_to(
                start_time = 395,
                new_location = [0, 8, 0]
            )
            tex.disappear(disappear_time = 395)



            cam_swivel.move_to(
                start_time = 395.5,
                end_time = 397,
                new_angle = [90 * math.pi / 180, 0, math.pi / 2]
            )
            sun_bobj.move_to(
                start_time = 395.5,
                end_time = 397,
                new_angle = [math.pi / 2, 0, math.pi / 2]
            )

            labs = [g.x_label_bobject, g.y_label_bobject, g.z_label_bobject]
            labs = labs + g.tick_labels_x + g.tick_labels_y + g.tick_labels_z
            for lab in labs:
                lab.move_to(
                    start_time = 395.6,
                    end_time = 397.1,
                    new_angle = [0, math.pi / 2, 0]
                )
                if lab == g.z_label_bobject:
                    lab.move_to(
                        new_location = [0, 0, 11],
                        start_time = 395.6,
                        end_time = 397.1,
                    )
            #Prev avg speed = 1.87
            #Avg speed = 10.3
            prevg = tex_bobject.TexBobject(
                '\\text{Previous average speed = } 1.87',
                '\\text{Maximum sense = } 1.4',
                location = [0, -11.6, 9.9],
                rotation_euler = [90 * math.pi / 180, 0, math.pi / 2],
                color = 'color2',
            )
            newvg = tex_bobject.TexBobject(
                '\\text{New average speed = } 1.03',
                '\\text{Minimum sense = } 0.6',
                location = [0, -11.6, 8.6],
                rotation_euler = [90 * math.pi / 180, 0, math.pi / 2],
                color = 'color2'
            )
            prevg.add_to_blender(appear_time = 398)
            newvg.add_to_blender(appear_time = 399)

            prevg.disappear(disappear_time = 419)
            newvg.disappear(disappear_time = 419)


            max_sense = tex_bobject.TexBobject(
                '\\text{Maximum sense = } 1.4',
                location = [0, -11.6, 9.9],
                rotation_euler = [90 * math.pi / 180, 0, math.pi / 2],
                color = 'color2',
            )
            min_sense = tex_bobject.TexBobject(
                '\\text{Minimum sense = } 0.6',
                location = [0, -11.6, 8.6],
                rotation_euler = [90 * math.pi / 180, 0, math.pi / 2],
                color = 'color2'
            )
            avg_sense = tex_bobject.TexBobject(
                    '\\text{Average sense = } 1.15',
                    location = [0, -11.6, 7.3],
                    rotation_euler = [90 * math.pi / 180, 0, math.pi / 2],
                    color = 'color2'
            )

            max_sense.add_to_blender(appear_time = 431)
            min_sense.add_to_blender(appear_time = 432)

            avg_sense.add_to_blender(appear_time = 433)

            cam_swivel.move_to(
                start_time = 397,
                end_time = 419.5,
                new_angle = [90 * math.pi / 180, 0, 85 * math.pi / 180]
            )
            cam_swivel.move_to(
                start_time = 419.5,
                end_time = 442,
                new_angle = [90 * math.pi / 180, 0, 90 * math.pi / 180]
            )


            max_sense.disappear(disappear_time = 441.9)
            min_sense.disappear(disappear_time = 442)
            avg_sense.disappear(disappear_time = 442.1)
            cam_swivel.move_to(
                start_time = 442,
                end_time = 443,
                new_angle = [74 * math.pi / 180, 0, 0]
            )

            g.move_to(
                new_location = [8, 8, 0], #0 instead of 4 because it doesn't properly handle z centering
                start_time = 442,
                end_time = 443
            )

            for lab in labs:
                lab.move_to(
                    start_time = 442.1,
                    end_time = 443.1,
                    new_angle = [0, 0, 0]
                )
                if lab == g.z_label_bobject:
                    lab.move_to(
                        new_location = [0, 0, 10.5],
                        start_time = 442.1,
                        end_time = 443.1,
                    )
            sun_bobj.move_to(
                start_time = 442,
                end_time = 443,
                new_angle = [math.pi / 2, 0, 0]
            )


        draw_graph()
        #draw_sim()
        focus_on_graph()

    def sudden_famine(self):
        cues = self.subscenes['famine']
        st = 443 #cues['start']

        cam_bobj, cam_swivel = cam_and_swivel(
            cam_location = [0, 0, 34],
            cam_rotation_euler = [0, 0, 0],
            cam_name = "Camera Bobject",
            swivel_location = [0, 0, 4],
            swivel_rotation_euler = [74 * math.pi / 180, 0, 0],
            swivel_name = 'Cam swivel',
            #control_sun = True
        )
        cam_swivel.add_to_blender(appear_time = 0)


        sim = natural_sim.DrawnNaturalSim(
            scale = 1.5,
            sim = 'sudden_f10_[True, True, True]_23',
            location = [-6.5, 0, 0],
            day_length_style = 'fixed_length'
        )

        g = graph_bobject.GraphBobject3D(
            x_range = [0, 2],
            y_range = [0, 2],
            z_range = [0, 2],
            x_label = '\\text{Size}',
            y_label = '\\text{Sense}',
            z_label = '\\text{Speed}',
            width = 10,
            height = 10,
            depth = 10,
            location = [8, 8, 4],
            rotation_euler = [math.pi / 2, 0, 0],
            centered = True,
            tick_step = 0.5
        )

        tex = tex_bobject.TexBobject(
            #'\\text{Reduced food}',
            '\\text{Food count} =  100',
            '\\text{Food count} =  10',
            scale = 2,
            location = [-6.5, 0, 8],
            rotation_euler = [74 * math.pi / 180, 0, 0],
            color = 'color2',
            centered = True
        )
        tex.add_to_blender(appear_time = 447)
        tex.morph_figure(1, start_time = 448.5)



        first_day = 20

        #Set timing for first five days at 1 sec per day
        total_animation_length = 5
        uncorrected = 0
        for record in sim.sim.date_records:
            if record['date'] >= first_day:
                durs = record['anim_durations']
                uncorrected += sum(durs.values())

        correction_factor = total_animation_length / uncorrected

        for record in sim.sim.date_records:
            if record['date'] >= first_day:
                durs = record['anim_durations']
                for key in durs:
                    durs[key] *= correction_factor




        first_day_start = 461
        sim_appearance_time = 443

        #Find proper duration for first morning pause to fill talking time
        initial_day_durs = sim.sim.date_records[first_day]['anim_durations']
        first_morning_dur = first_day_start - \
                           sim_appearance_time - \
                           initial_day_durs['dawn'] - \
                           1 #For standard start_delay on drawn sims
        initial_day_durs['morning'] = first_morning_dur

        def draw_sim():
            sim.add_to_blender(
                appear_time = 443,
                start_day = 20,#7
                #end_day = 23
            )

        def draw_graph():
            g.add_to_blender(appear_time = 0)
            #Graphs have many tex_bobjects, whose speed is sensitive to the number of object in
            #Blender at the moment, so it's good to add the graph to blender before the sim.

            def draw_sim_points():
                cres_with_points = []
                cre_counts = []
                records = sim.sim.date_records
                time = 444 #start time
                #graph_point_leftovers = []

                #Assign points in start file
                #print()
                #print(g.ref_obj.name)

                #I didn't foresee the fact that random additions to points would
                #cause issues when I want to use the same graph in different scene.
                #These ares the locs from final version of the previous scene
                locs = [[1.19959557056427, 0.9703189134597778, 1.020974040031433], [1.204119086265564, 1.425511360168457, 1.1812005043029785], [1.3164743185043335, 1.273431658744812, 0.9055522680282593], [1.307760238647461, 0.9228394031524658, 0.9211083650588989], [1.408111572265625, 0.985110878944397, 0.5734765529632568], [1.2097967863082886, 1.229711651802063, 1.0113754272460938], [1.224846363067627, 0.7857423424720764, 0.7897409796714783], [1.0971119403839111, 1.1140503883361816, 1.1124258041381836], [1.4028091430664062, 1.4278273582458496, 1.0081310272216797], [1.2847728729248047, 0.7092758417129517, 0.6855748891830444], [1.3952150344848633, 1.1825109720230103, 1.39744234085083], [1.2872920036315918, 1.3270885944366455, 1.0866162776947021], [1.3044685125350952, 1.1224359273910522, 1.0855640172958374], [1.1864969730377197, 1.22417151927948, 1.018127202987671], [1.2000783681869507, 1.1753534078598022, 0.7902054786682129], [1.186108112335205, 1.2193348407745361, 0.973759114742279], [1.2765913009643555, 1.3089720010757446, 1.084298014640808], [1.381836175918579, 1.1962908506393433, 1.0080620050430298], [1.312105655670166, 1.2846379280090332, 1.317226767539978], [1.073990821838379, 1.270787000656128, 1.2949399948120117], [1.2163854837417603, 1.3743259906768799, 0.784053385257721], [1.1723737716674805, 1.2242356538772583, 1.2054738998413086], [1.3785524368286133, 1.4096506834030151, 1.0257009267807007], [1.3737915754318237, 1.1826667785644531, 1.1710566282272339], [1.2928353548049927, 1.0707526206970215, 1.0756503343582153], [1.518924355506897, 1.0998060703277588, 1.1059123277664185], [1.2993005514144897, 0.8921331763267517, 0.9004638195037842], [1.412189245223999, 1.3891831636428833, 0.9803748726844788], [1.3948076963424683, 0.8170769810676575, 0.999501645565033], [1.3286423683166504, 0.9115564823150635, 0.8868694305419922], [0.9770519137382507, 0.9861668348312378, 0.9863671660423279], [1.4861751794815063, 1.3047313690185547, 0.8939758539199829], [1.1809210777282715, 0.6025184392929077, 0.7883769869804382], [1.2902082204818726, 1.1014775037765503, 1.3050527572631836], [1.3762340545654297, 1.2019294500350952, 0.9961966276168823], [1.3036876916885376, 1.3040571212768555, 1.1132107973098755], [1.0829590559005737, 1.3129061460494995, 0.7106703519821167], [1.371167540550232, 1.4151160717010498, 0.9832428097724915], [1.410250186920166, 1.381046175956726, 1.3889288902282715], [1.2838892936706543, 1.1257176399230957, 1.3212934732437134], [1.5253435373306274, 1.0960781574249268, 1.1296186447143555], [1.3709173202514648, 0.973776638507843, 1.027558445930481], [1.4139313697814941, 1.014811396598816, 1.1736400127410889]]
                #points = [x for x in g.ref_obj.children if 'sphere' in x.name and x.hide == False]
                #for point in points:
                #    point.creature = None

                #print(points)

                for cre in records[19]['creatures']:
                    for loc in locs:
                        if abs(loc[0] - cre.size) <= 0.3 and \
                           abs(loc[1] - cre.sense) <= 0.3 and \
                           abs(loc[2] - cre.speed) <= 0.3:

                            point = g.add_point_at_coord(
                                coord = loc,
                                appear_time = 0,
                                #Will need duration in actual scene
                            )
                            dummy = natural_sim.Creature()
                            dummy.apply_material_by_speed(
                                bobj = point,
                                spd = cre.speed,
                            )
                            cre.point = point
                            cres_with_points.append(cre)
                            locs.remove(loc)
                            break

                for date in range(20, len(records)):
                    print("Updating graph for day " + str(date))

                    #Delete points for creatures the died
                    to_delete = []
                    for cre in cres_with_points:
                        #print(' A creature has a point')
                        if cre not in records[date]['creatures']:
                            #print(' taking point from creature')
                            cre.point.disappear(
                                disappear_time = time + 0.5,
                                #Will need duration in actual scene
                            )
                            to_delete.append(cre)
                    for cre in to_delete:
                        cres_with_points.remove(cre)
                    #print(' Now ' + str(len(cres_with_points)) + " cres have points")

                    #Add points for new creatures
                    for cre in records[date]['creatures']:
                        #print(" There's a cre")
                        if cre not in cres_with_points:
                            #print(' Giving a point')
                            point = g.add_point_at_coord(
                                coord = [
                                    cre.size + uniform(-0.03, 0.03),
                                    cre.sense + uniform(-0.03, 0.03),
                                    cre.speed + uniform(-0.03, 0.03),
                                ],
                                appear_time = time,

                                #Will need duration in actual scene
                            )
                            dummy = natural_sim.Creature()
                            dummy.apply_material_by_speed(
                                bobj = point,
                                spd = cre.speed,
                            )
                            cre.point = point
                            cres_with_points.append(cre)
                            #print(' Now ' + str(len(cres_with_points)) + " cres have points")

                    #Add time after day
                    time += records[date]['anim_durations']['dawn'] + \
                            records[date]['anim_durations']['morning'] + \
                            records[date]['anim_durations']['day'] + \
                            records[date]['anim_durations']['evening'] + \
                            records[date]['anim_durations']['night']

            draw_sim_points()



        draw_graph()
        draw_sim()

    def gradual_famine(self):
        #cues = self.subscenes['gradual']
        #st = cues['start']

        cam_bobj, cam_swivel = cam_and_swivel(
            cam_location = [0, 0, 34],
            cam_rotation_euler = [0, 0, 0],
            cam_name = "Camera Bobject",
            swivel_location = [0, 0, 4],
            swivel_rotation_euler = [74 * math.pi / 180, 0, 0],
            swivel_name = 'Cam swivel',
            #control_sun = True
        )
        cam_swivel.add_to_blender(appear_time = 0)

        sim = natural_sim.DrawnNaturalSim(
            scale = 1.5,
            sim = 'gradual_f10_[True, True, True]_201',
            location = [-6.5, 0, 0],
            day_length_style = 'fixed_length'
        )

        g = graph_bobject.GraphBobject3D(
            x_range = [0, 2],
            y_range = [0, 2],
            z_range = [0, 2],
            x_label = '\\text{Size}',
            y_label = '\\text{Sense}',
            z_label = '\\text{Speed}',
            width = 10,
            height = 10,
            depth = 10,
            location = [8, 8, 4],
            rotation_euler = [math.pi / 2, 0, 0],
            centered = True,
            tick_step = 0.5
        )

        '''tex = tex_bobject.TexBobject(
            '\\text{Food count} = 100',
            '\\substack {\\text{Gradually} \\\\ \\text{reduced food}}',
            scale = 2,
            location = [-6.5, 0, 8],
            rotation_euler = [74 * math.pi / 180, 0, 0],
            color = 'color2',
            centered = True
        )
        tex.add_to_blender(appear_time = 400)

        tex.morph_figure(1, start_time = 494)
        tex.move_to(
            new_scale = 2.8,
            start_time = 494
        )'''

        first_day = 20

        #Set timing for first five days at 1 sec per day
        total_animation_length = 15
        uncorrected = 0
        for record in sim.sim.date_records:
            if record['date'] >= first_day and record['date'] <= 196:
                durs = record['anim_durations']
                uncorrected += sum(durs.values())

        correction_factor = total_animation_length / uncorrected

        for record in sim.sim.date_records:
            if record['date'] >= first_day:
                durs = record['anim_durations']
                for key in durs:
                    durs[key] *= correction_factor




        first_day_start = 497.5
        sim_appearance_time = 400

        #Find proper duration for first morning pause to fill talking time
        initial_day_durs = sim.sim.date_records[first_day]['anim_durations']
        first_morning_dur = first_day_start - \
                           sim_appearance_time - \
                           initial_day_durs['dawn'] - \
                           1 #For standard start_delay on drawn sims
        initial_day_durs['morning'] = first_morning_dur

        def draw_sim():
            sim.add_to_blender(
                appear_time = 400,
                start_day = 20,#7
                end_day = 196
            )

        def draw_graph():
            g.add_to_blender(appear_time = 0)
            #Graphs have many tex_bobjects, whose speed is sensitive to the number of object in
            #Blender at the moment, so it's good to add the graph to blender before the sim.

            def draw_sim_points():
                cres_with_points = []
                cre_counts = []
                records = sim.sim.date_records
                time = 401 #start time
                #graph_point_leftovers = []

                #Assign points in start file
                #print()
                #print(g.ref_obj.name)

                #I didn't foresee the fact that random additions to points would
                #cause issues when I want to use the same graph in different scene.
                #These ares the locs from final version of the previous scene
                locs = [[1.204119086265564, 1.425511360168457, 1.1812005043029785], [1.408111572265625, 0.985110878944397, 0.5734765529632568], [1.2097967863082886, 1.229711651802063, 1.0113754272460938], [1.3952150344848633, 1.1825109720230103, 1.39744234085083], [1.2872920036315918, 1.3270885944366455, 1.0866162776947021], [1.3044685125350952, 1.1224359273910522, 1.0855640172958374], [1.1864969730377197, 1.22417151927948, 1.018127202987671], [1.2000783681869507, 1.1753534078598022, 0.7902054786682129], [1.186108112335205, 1.2193348407745361, 0.973759114742279], [1.381836175918579, 1.1962908506393433, 1.0080620050430298], [1.312105655670166, 1.2846379280090332, 1.317226767539978], [1.073990821838379, 1.270787000656128, 1.2949399948120117], [1.2163854837417603, 1.3743259906768799, 0.784053385257721], [1.1723737716674805, 1.2242356538772583, 1.2054738998413086], [1.3737915754318237, 1.1826667785644531, 1.1710566282272339], [1.518924355506897, 1.0998060703277588, 1.1059123277664185], [1.2993005514144897, 0.8921331763267517, 0.9004638195037842], [1.412189245223999, 1.3891831636428833, 0.9803748726844788], [1.3948076963424683, 0.8170769810676575, 0.999501645565033], [1.2902082204818726, 1.1014775037765503, 1.3050527572631836], [1.410250186920166, 1.381046175956726, 1.3889288902282715], [1.2838892936706543, 1.1257176399230957, 1.3212934732437134], [1.5253435373306274, 1.0960781574249268, 1.1296186447143555], [1.3709173202514648, 0.973776638507843, 1.027558445930481], [1.4139313697814941, 1.014811396598816, 1.1736400127410889], [1.0888365507125854, 1.2763532400131226, 1.294913411140442], [1.2983753681182861, 1.2767884731292725, 1.1173202991485596], [1.4969432353973389, 1.2728290557861328, 1.3119254112243652], [1.2206954956054688, 1.0020447969436646, 1.0112260580062866], [1.328333854675293, 1.3055939674377441, 1.1210356950759888], [1.3007124662399292, 1.098942756652832, 0.8850259184837341], [1.3089516162872314, 1.272914171218872, 0.908165693283081], [1.1822603940963745, 1.1883777379989624, 1.1888587474822998], [1.1719539165496826, 1.3896856307983398, 1.2201716899871826], [1.1192811727523804, 1.322360873222351, 0.8819512128829956], [1.2908812761306763, 1.0768579244613647, 1.110305905342102], [1.4058194160461426, 0.9724385142326355, 1.193057656288147], [1.4283770322799683, 0.973495602607727, 0.9739724397659302], [1.2854950428009033, 1.2989557981491089, 0.900986909866333], [1.4875723123550415, 0.899839460849762, 0.9164788126945496], [1.4079073667526245, 1.0063056945800781, 1.1976863145828247], [1.2819401025772095, 1.4956700801849365, 1.3281666040420532], [1.6245044469833374, 1.1967015266418457, 1.0003347396850586], [1.2701953649520874, 0.9278050661087036, 1.102436900138855], [1.5068249702453613, 0.8796652555465698, 1.0868481397628784]]
                #points = [x for x in g.ref_obj.children if 'sphere' in x.name and x.hide == False]
                #for point in points:
                #    point.creature = None

                #print(points)

                for cre in records[20]['creatures']:
                    for loc in locs:
                        if abs(loc[0] - cre.size) <= 0.3 and \
                           abs(loc[1] - cre.sense) <= 0.3 and \
                           abs(loc[2] - cre.speed) <= 0.3:

                            point = g.add_point_at_coord(
                                coord = loc,
                                appear_time = 0,
                                #Will need duration in actual scene
                            )
                            dummy = natural_sim.Creature()
                            dummy.apply_material_by_speed(
                                bobj = point,
                                spd = cre.speed,
                            )
                            cre.point = point
                            cres_with_points.append(cre)
                            locs.remove(loc)
                            break

                time += records[20]['anim_durations']['dawn'] + \
                        records[20]['anim_durations']['morning'] + \
                        records[20]['anim_durations']['day'] + \
                        records[20]['anim_durations']['evening'] + \
                        records[20]['anim_durations']['night']

                for date in range(196, 197):
                    print("Updating graph for day " + str(date))

                    durs = records[date]['anim_durations']
                    full_day_time = sum(durs.values())

                    #Delete points for creatures the died
                    to_delete = []
                    for cre in cres_with_points:
                        #print(' A creature has a point')
                        if cre not in records[date]['creatures']:
                            #print(' taking point from creature')
                            cre.point.disappear(
                                disappear_time = time + full_day_time / 2,
                                duration_frames = (full_day_time / 2) * FRAME_RATE
                                #Will need duration in actual scene
                            )
                            to_delete.append(cre)
                    for cre in to_delete:
                        cres_with_points.remove(cre)
                    #print(' Now ' + str(len(cres_with_points)) + " cres have points")

                    #Add points for new creatures
                    for cre in records[date]['creatures']:
                        #print(" There's a cre")
                        if cre not in cres_with_points:
                            #print(' Giving a point')
                            point = g.add_point_at_coord(
                                coord = [
                                    cre.size + uniform(-0.03, 0.03),
                                    cre.sense + uniform(-0.03, 0.03),
                                    cre.speed + uniform(-0.03, 0.03),
                                ],
                                appear_time = time,
                                duration = (full_day_time / 2) * FRAME_RATE
                                #Will need duration in actual scene
                            )
                            dummy = natural_sim.Creature()
                            dummy.apply_material_by_speed(
                                bobj = point,
                                spd = cre.speed,
                            )
                            cre.point = point
                            cres_with_points.append(cre)
                            #print(' Now ' + str(len(cres_with_points)) + " cres have points")

                    #Add time after day
                    time += full_day_time

            draw_sim_points()

        #sim.disappear(disappear_time = 513)
        #tex.disappear(disappear_time = 513)
        g.move_to(
            start_time = 513,
            new_location = [0, 8, 0]
        )

        draw_graph()
        #draw_sim()

        def post_look():

            cam_swivel.move_to(
                new_angle = [74 * math.pi / 180, 0, 10 * math.pi / 180],
                start_time = 514,
                end_time = 522
            )

            cam_swivel.move_to(
                new_angle = [math.pi / 2, 0, 0],
                start_time = 522,
                end_time = 524
            )


            cam_swivel.move_to(
                new_angle = [math.pi / 2, 0, math.pi / 2],
                start_time = 529.5,
                end_time = 532.5,
            )
            sun = bpy.data.objects['Sun']
            sun_bobj = bobject.Bobject(objects = [sun])
            sun_bobj.add_to_blender(appear_time = 0)
            sun_bobj.move_to(
                start_time = 0,
                new_angle = [math.pi / 2, 0, 0]
            )


            labs = [g.x_label_bobject, g.y_label_bobject, g.z_label_bobject]
            labs = labs + g.tick_labels_x + g.tick_labels_y + g.tick_labels_z

            for lab in labs:
                lab.move_to(
                    start_time = 529.5,
                    end_time = 532.5,
                    new_angle = [0, math.pi / 2, 0]
                )
                if lab == g.z_label_bobject:
                    lab.move_to(
                        new_location = [0, 0, 11],
                        start_time = 529.5,
                        end_time = 532.5,
                    )
            sun_bobj.move_to(
                start_time = 529.5,
                end_time = 532.5,
                new_angle = [math.pi / 2, 0, math.pi / 2]
            )





            cam_swivel.move_to(
                new_angle = [74 * math.pi / 180, 0, 0],
                start_time = 541,
                end_time = 554,
            )


            labs = [g.x_label_bobject, g.y_label_bobject, g.z_label_bobject]
            labs = labs + g.tick_labels_x + g.tick_labels_y + g.tick_labels_z

            for lab in labs:
                lab.move_to(
                    new_angle = [0, 0, 0],
                    start_time = 541,
                    end_time = 554,
                )
                if lab == g.z_label_bobject:
                    lab.move_to(
                        new_location = [0, 0, 10.5],
                        start_time = 541,
                        end_time = 554,
                    )
            sun_bobj.move_to(
                new_angle = [math.pi / 2, 0, 0],
                start_time = 541,
                end_time = 554,
            )

            def make_g2():
                sim2 = natural_sim.DrawnNaturalSim(
                    scale = 1.5,
                    sim = 'gradual_f10_[True, True, True]_201',
                    location = [-6.5, 0, 0],
                    day_length_style = 'fixed_length'
                )

                g2 = graph_bobject.GraphBobject3D(
                    x_range = [0, 2],
                    y_range = [0, 2],
                    z_range = [0, 2],
                    x_label = '\\text{Size}',
                    y_label = '\\text{Sense}',
                    z_label = '\\text{Speed}',
                    width = 10,
                    height = 10,
                    depth = 10,
                    location = [8, 8, 4],
                    rotation_euler = [math.pi / 2, 0, 0],
                    centered = True,
                    tick_step = 0.5
                )

                cres_with_points = []
                cre_counts = []
                time = 0 #start time
                records = sim2.sim.date_records
                for date in range(19, 20):
                    print("Updating graph for day " + str(date))

                    durs = records[date]['anim_durations']
                    full_day_time = sum(durs.values())

                    #Delete points for creatures the died
                    to_delete = []
                    for cre in cres_with_points:
                        #print(' A creature has a point')
                        if cre not in records[date]['creatures']:
                            #print(' taking point from creature')
                            cre.point.disappear(
                                disappear_time = time + full_day_time / 2,
                                duration_frames = (full_day_time / 2) * FRAME_RATE
                                #Will need duration in actual scene
                            )
                            to_delete.append(cre)
                    for cre in to_delete:
                        cres_with_points.remove(cre)
                    #print(' Now ' + str(len(cres_with_points)) + " cres have points")

                    #Add points for new creatures
                    for cre in records[date]['creatures']:
                        #print(" There's a cre")
                        if cre not in cres_with_points:
                            #print(' Giving a point')
                            point = g2.add_point_at_coord(
                                coord = [
                                    cre.size + uniform(-0.03, 0.03),
                                    cre.sense + uniform(-0.03, 0.03),
                                    cre.speed + uniform(-0.03, 0.03),
                                ],
                                appear_time = time,
                                duration = (full_day_time / 2) * FRAME_RATE
                                #Will need duration in actual scene
                            )
                            dummy = natural_sim.Creature()
                            dummy.apply_material_by_speed(
                                bobj = point,
                                spd = cre.speed,
                            )
                            cre.point = point
                            cres_with_points.append(cre)
                            #print(' Now ' + str(len(cres_with_points)) + " cres have points")

                    #Add time after day
                    time += full_day_time

                g2.add_to_blender(
                    appear_time = 555
                )
                g.move_to(
                    new_location = [-6.5, 8, 0],
                    start_time = 555
                )

                ten = tex_bobject.TexBobject(
                    '10 \\text{ food}',
                    location = [2, 4, 8],
                    rotation_euler = [math.pi / 2, 0, 0],
                    scale = 1.5,
                    centered = True,
                    color = 'color2'
                )
                hund = tex_bobject.TexBobject(
                    '100 \\text{ food}',
                    location = [9.5, 4, 8],
                    rotation_euler = [math.pi / 2, 0, 0],
                    centered = True,
                    scale = 1.5,
                    color = 'color2'
                )
                ten.add_to_blender(appear_time = 555)
                ten.move_to(new_location = [-4.5, 4, 8], start_time = 555)
                hund.add_to_blender(appear_time = 555)

                g.disappear(disappear_time = 559)
                g2.disappear(disappear_time = 559)
                ten.disappear(disappear_time = 559)
                hund.disappear(disappear_time = 559)


            make_g2()

            cam_swivel.move_to(
                new_angle = [74 * math.pi / 180, 0, -10 * math.pi / 180],
                start_time = 555,
                end_time = 559,
            )

        post_look()

    def evolution_diagram(self):
        evo = svg_bobject.SVGBobject(
            'human_evolution_scheme',
            scale = 0.4,
            location = [-2.5, -1.25, 0],
            centered = True,
            color = 'color2'
        )
        f = 30
        evo.add_to_blender(
            appear_time = 0,
            subbobject_timing = [5*f, 4*f, 3*f, f, 2*f, 6*f]
        )
        evo.disappear(disappear_time = 4)

    def recap(self):
        #cues = self.subscenes['wws']
        #st = cues['start']

        wws = tex_bobject.TexBobject(
            '\\text{What we saw}',
            location = [-12.5, 5.5, 0],
            scale = 2.5,
            color = 'color2'
        )
        wws.add_to_blender(appear_time = 604)

        blob = import_object(
            'boerd_blob', 'creatures',
            location = [11.5, -1, 0],
            rotation_euler = [0, - math.pi / 4, 0],
            wiggle = True,
            scale = 2
        )
        blob.add_to_blender(appear_time = 604.5)
        apply_material(blob.ref_obj.children[0].children[0], 'creature_color3')

        start_height = 3
        spacing = 1.5
        tex1 = tex_bobject.TexBobject(
            '\\cdot \\text{Selection happens via competition at carrying capacity}',
            location = [-11.5, start_height, 0],
            scale = 1,
            color = 'color2'
        )
        tex2 = tex_bobject.TexBobject(
            '\\cdot \\text{Populations evolve, not individuals}',
            location = [-11.5, start_height - spacing, 0],
            scale = 1,
            color = 'color2'
        )
        tex3 = tex_bobject.TexBobject(
            '\\cdot \\text{Selection is not for the good of the species}',
            location = [-11.5, start_height - spacing * 2, 0],
            scale = 1,
            color = 'color2'
        )
        tex4 = tex_bobject.TexBobject(
            '\\cdot \\text{A creature\'s environment includes other creatures}',
            location = [-11.5, start_height - spacing * 3, 0],
            scale = 1,
            color = 'color2'
        )
        tex5 = tex_bobject.TexBobject(
            '\\cdot \\text{Predictions are difficult}',
            location = [-11.5, start_height - spacing * 4, 0],
            scale = 1,
            color = 'color2'
        )
        tex6 = tex_bobject.TexBobject(
            '\\cdot \\text{Environmental changes alter which traits are favored}',
            location = [-11.5, start_height - spacing * 5, 0],
            scale = 1,
            color = 'color2'
        )
        tex7 = tex_bobject.TexBobject(
            '\\cdot \\text{There\'s no such thing as a \"more evolved\" creature}',
            location = [-11.5, start_height - spacing * 6, 0],
            scale = 1,
            color = 'color2'
        )

        tex_things = [
            tex1,
            tex2,
            tex3,
            tex4,
            tex5,
            tex6,
            tex7,
        ]

        delay = 0
        time_spacing = 1
        for tex in tex_things:
            tex.add_to_blender(appear_time = 605 + delay)
            delay += time_spacing

        to_disappear = [wws, blob] + tex_things
        for i, thing in enumerate(to_disappear):
            thing.disappear(disappear_time = 615 - (len(to_disappear) - 1 - i) * 0.05)

        altruism = tex_bobject.TexBobject(
            '\\text{Altruism?}',
            location = [0, -3, 0],
            scale = 3,
            color = 'color2',
            centered = True
        )
        sex = tex_bobject.TexBobject(
            '\\text{Sexual reproduction?}',
            location = [0, 3, 0],
            scale = 3,
            color = 'color2',
            centered = True
        )
        altruism.add_to_blender(appear_time = 618.5)
        sex.add_to_blender(appear_time = 617)

        to_disappear = [sex, altruism]
        for i, thing in enumerate(to_disappear):
            thing.disappear(disappear_time = 621.5 - (len(to_disappear) - 1 - i) * 0.05)

    def end_card(self):
        cues = self.subscenes
        scene_end = self.duration

        '''bpy.ops.mesh.primitive_plane_add()
        play_bar = bpy.context.object
        play_bar.scale[0] = 15
        play_bar.scale[1] = 90 / 720 * 8.4
        play_bar.location = [0, -8.4 + play_bar.scale[1], -0.01]

        bpy.ops.mesh.primitive_plane_add()
        vid_rec = bpy.context.object
        vid_rec.scale[0] = 410 / 1280 * 15
        vid_rec.scale[1] = 230 / 720 * 8.4
        vid_rec.location = [9, -3, -0.01]

        bpy.ops.mesh.primitive_cylinder_add()
        sub_cir = bpy.context.object
        sub_cir.scale = [98 / 1280 * 30, 98 / 1280 * 30, 0]
        sub_cir.location = [-11.5, -2.8, -0.01]

        #Whole end area
        bpy.ops.mesh.primitive_plane_add()
        end_area = bpy.context.object
        end_area.scale[0] = 1225 / 1280 * 15
        end_area.scale[1] = 518 / 720 * 8.4
        end_area.location = [0, 0.2, -0.05]'''




        logo = svg_bobject.SVGBobject(
            "Layer",
            #file_name = "PrimerLogoWhite",
            location = (-9.2, -3, 0),
            scale = 1.4
        )
        for bobj in logo.rendered_curve_bobjects:
            apply_material(bobj.ref_obj.children[0], 'color2')
        stroke = logo.rendered_curve_bobjects[0]
        apply_material(stroke.ref_obj.children[0], 'color3')
        logo.morph_chains[0][0].ref_obj.location[2] = -1
        logo.add_to_blender(
            appear_time = cues['card']['start'],
            #subbobject_timing = [90, 30, 40, 50, 60, 70, 80],
            subbobject_timing = [42, 30, 33, 36, 39, 42, 45],
            animate = True
        )


        reddit = import_object(
            'reddit', 'svgblend',
            scale = 2.297,
            location = (5, 4 - 0.5, 0)
        )
        reddit.add_to_blender(appear_time = 0)
        disc = tex_bobject.TexBobject(
            '\\text{/r/primerlearning}',
            location = [6.5, 2.5 - 0.5, 0],
            color = 'color2',
            scale = 0.8
        )
        disc.add_to_blender(appear_time = 0)

        patreon = import_object(
            'patreon', 'svgblend',
            scale = 2.297,
            location = (-11.5, 4 - 0.5, 0)
        )
        patreon.add_to_blender(appear_time = 0)
        thanks = tex_bobject.TexBobject(
            '\\text{Special thanks:}',
            location = [-8.8, 5.1, 0],
            color = 'color2'
        )
        thanks.add_to_blender(appear_time = 0)
        js = tex_bobject.TexBobject(
            '\\text{Jordan Scales}',
            location = [-8.3, 3.5, 0],
            color = 'color2',
            scale = 1.4
        )
        js.add_to_blender(appear_time = 1)

        '''cp = svg_bobject.SVGBobject(
            'chinese_patron',
            location = [-8.55, 3.1 - 0.5, 0],
            color = 'color2',
            scale = 0.085
        )
        cp.add_to_blender(appear_time = 1)'''

        links = tex_bobject.TexBobject(
            '\\text{(Links in the description)}',
            location = [0, 7.3, 0],
            centered = True,
            scale = 1,
        )
        links.add_to_blender(appear_time = 0)

        remaining = [reddit, disc, logo, patreon, thanks, js, links]
        for thing in remaining:
            thing.disappear(disappear_time = 2.5)

    def thumbnail(self):
        '''evo = svg_bobject.SVGBobject(
            'human_evolution_scheme',
            scale = 0.4,
            location = [-2.5, 3, 0],
            centered = True,
            color = 'color2'
        )
        evo.add_to_blender(appear_time = 0)'''

        '''blob = import_object(
            'boerd_blob', 'creatures',
            location = [9.2, 2.75, 0],
            scale = 3,
            wiggle = True
        )
        apply_material(blob.ref_obj.children[0].children[0], 'creature_color3')
        blob.blob_wave(
            start_time = 0,
            duration = 20
        )
        blob.add_to_blender(appear_time = 0)'''

        tex = tex_bobject.TexBobject(
            '\\text{Natural Selection} \\phantom{o}',
            location = [0, 8, -9.35],
            rotation_euler = [74 * math.pi / 180, 0, 0],
            scale = 2.8,
            centered = True,
            color = 'color2'
        )
        tex.add_to_blender(appear_time = 0)
        tex2 = tex_bobject.TexBobject(
            '\\text{Simulating} \\phantom{o}',
            location = [0, 8, 3.25],
            rotation_euler = [74 * math.pi / 180, 0, 0],
            scale = 2.8,
            centered = True,
            color = 'color2'
        )
        tex2.add_to_blender(appear_time = 0)


        cam_bobj, cam_swivel = cam_and_swivel(
            cam_location = [0, 0, 34],
            cam_rotation_euler = [0, 0, 0],
            cam_name = "Camera Bobject",
            swivel_location = [0, 0, 0],
            swivel_rotation_euler = [74 * math.pi / 180, 0, 0],
            swivel_name = 'Cam swivel',
            #control_sun = True
        )
        cam_swivel.add_to_blender(appear_time = 0)

        sim = natural_sim.DrawnNaturalSim(
            scale = 2,
            sim = 'all_mut_f100_[True, True, True]_19',
            #initial_creatures = 3,
            location = [0, 0, 0],
            #day_length_style = 'fixed_speed',
            day_length_style = 'fixed_length'
            #mutation_switches = [False, False, False]
        )
        sim.add_to_blender(
            appear_time = 29,
            start_day = 15,
            end_day = 15
        )
        cam_bobj.move_to(
            new_location = [0, 0, 25],
            #new_angle = [0, 0, 0],
            #new_angle = [math.pi / 2, 0, math.pi / 2],
            start_time = 29.5
        )
        cam_swivel.move_to(
            new_angle = [74 * math.pi / 180, 0, 0],
            #new_angle = [0, -16 * math.pi / 180, -math.pi / 2],
            start_time = 29.5
        )
        sim.disappear(disappear_time = 37.5)
