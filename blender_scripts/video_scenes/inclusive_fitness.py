import collections
import math
from random import random, uniform, randrange
import bpy

import imp
#import scene
#imp.reload(scene)
from scene import Scene

import bobject
imp.reload(bobject)
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
import table_bobject
imp.reload(table_bobject)


import blobject
imp.reload(blobject)
from blobject import Blobject

import helpers
imp.reload(helpers)
from helpers import *

import constants
imp.reload(constants)
from constants import SIM_DIR


class InclusiveFitness(Scene):
    def __init__(self):
        self.subscenes = collections.OrderedDict([
            ('card', {'duration': 10000})
        ])
        super().__init__()

    def play(self):
        super().play()

        #self.intro()
        #self.sim_rules()
        ##NEVERMIND self.traits()
        ##NEVERMIND self.diverse_stalling_sim()
        ##NEVERMINDs elf.fast_altruism()
        ##NEVERMIND self.big_altruism()
        ##NEVERMIND self.altruism_trait()
        #self.how_to_be_altruistic()
        #self.random_altruism_sim()
        #self.less_punishing()
        #self.net_positive_sim()
        #self.need_targeting()
        #self.how_to_coordinate()
        #self.green_beard()
        #self.green_beard_sim()
        #self.separate_genes()
        #self.separate_genes_sim()
        #self.kin_selection_intro()
        self.hamilton()
        #self.lies()
        #self.kin_selection_sim()
        ##NEVERMIND self.kin_distance_sim()
        #self.gene_v_creature()
        #self.recap()
        #self.end_card()
        #self.thumbnail()
        #self.try_simulations()

    def try_simulations(self):
        food_count = 100
        def set_initial_creatures():
            initial_creatures = []
            for i in range(math.floor(food_count / 10)):
                initial_creatures.append(
                    natural_sim.Creature(
                        size = 1,# + randrange(-5, 6) * natural_sim.MUTATION_VARIATION,
                        speed = 1,# + randrange(-5, 6) * natural_sim.MUTATION_VARIATION,
                        sense = 1,# + randrange(-5, 6) * natural_sim.MUTATION_VARIATION,
                        green_beard = True
                    )
                )
                initial_creatures.append(
                    natural_sim.Creature(
                        size = 1,# + randrange(-5, 6) * natural_sim.MUTATION_VARIATION,
                        speed = 1,# + randrange(-5, 6) * natural_sim.MUTATION_VARIATION,
                        sense = 1,# + randrange(-5, 6) * natural_sim.MUTATION_VARIATION,
                        green_beard = False
                    )
                )
            return initial_creatures

        sims = []
        num_sims = 1
        num_days = 10
        for i in range(num_sims):
            print('------------------------- BEGIN SIM NUMBER ' + str(i + 1) + ' of ' + str(num_sims) + ' -------------------------')
            sim = natural_sim.DrawnNaturalSim(
                mutation_switches = {
                     'speed' : False,
                     'size' : False,
                     'sense' : False,
                     'altruist' : False,
                     'green_beard' : True,
                     'gbo' : False,
                     'a_gb' : False,
                     'kin_altruist' : False,
                     'kin_radius' : False,
                },
                scale = 1.5,
                food_count = food_count,
                initial_creatures = set_initial_creatures(),
                #sim = 'gb_30',
                location = [-6.5, 0, 0],
                day_length_style = 'fixed_length'
            )

            '''for i in range(num_days):
                save = False
                if i == 9:
                    save = True
                sim.sim.sim_next_day(save = save, filename = 'gb_30')'''

            sims.append(sim)


        tot_food_given_away = 0
        tot_food_giving_attempts = 0
        tot_martyrs = 0
        #Update bars each day
        for date in range(num_days):
            total_counts_for_date = [0, 0]
            print('Stats for day ' + str(date))
            for single_sim in sims:
                print(' ----------------------')
                counts = InclusiveFitness.count_by_vals(date, 'green_beard', [True, False], single_sim.sim)
                print(' Counts: ' + str(counts))
                total_counts_for_date[0] += counts[0]
                total_counts_for_date[1] += counts[1]



                tot_speed = 0
                tot_size = 0
                tot_sense = 0
                cres = single_sim.sim.date_records[date]['creatures']
                for cre in cres:
                    tot_speed += cre.speed
                    tot_size += cre.size
                    tot_sense += cre.sense

                avg_speed = tot_speed / len(cres)
                print(' Avg speed: ' + str(avg_speed))
                avg_size = tot_size / len(cres)
                print(' Avg size: ' + str(avg_size))
                avg_sense = tot_sense / len(cres)
                print(' Avg sense: ' + str(avg_sense))

                for rec in single_sim.sim.date_records:
                    if rec['date'] == date:
                        print(' Daily food given ' + str(rec['food_given_away']))
                        print(' Daily attempts ' + str(rec['food_giving_attempts']))
                        print(' Daily martyrs ' + str(rec['martyrs']))
                        tot_food_given_away += rec['food_given_away']
                        tot_food_giving_attempts += rec['food_giving_attempts']
                        tot_martyrs += rec['martyrs']

            print('----------------------')
            print('Altruism stats')
            print(' Food given ' + str(tot_food_given_away))
            print(' Attempts ' + str(tot_food_giving_attempts))
            print(' Martyrs ' + str(tot_martyrs))
            print('----------------------')
            print('Total counts')
            print('' + str(total_counts_for_date))
            print()

            avgs_for_date = [[],[]]
            avgs_for_date[0] = total_counts_for_date[0] / len(sims)
            avgs_for_date[1] = total_counts_for_date[1] / len(sims)

        try:
            print(natural_sim.SAMARITAN_RATIO)
        except:
            pass

    def intro(self):
        sotf = svg_bobject.SVGBobject(
            "Sot_Fittest_century_3stack",
            "So__t_Fittest_century_3stack",
            "So__t_Friendliest_century_3stack",
            "Sot_Friendliest_q_century_3stack",
            #location = (-5, 3.75, 0), #Centered position
            #scale = 0.26, #Centered scale
            location = [0, 0, 0],
            scale = 5,
            color = 'color2',
            centered = 'x_and_y'
        )
        sotf.add_to_blender(appear_time = 0)

        sotf.morph_figure(1, start_time = 4.5, duration = 2.5 * FRAME_RATE)

        blob = blobject.Blobject(
            location = [-1.05, -0.2, 0],
            scale = 3,
        )
        blob.add_to_blender(appear_time = 6.5)
        blob.hello(
            start_time = 7.5,
            end_time = 9.5
        )
        blob.show_mouth(
            start_time = 7.5
        )
        blob.hold_gift(
            start_time = 11
        )


        blob.move_head(
            start_time = 13,
            attack = 0.2,
            rotation_quaternion = [1, -0.05, 0, 0]
        )
        blob.move_head(
            start_time = 13.2,
            attack = 0.2,
            rotation_quaternion = [1, 0.05, 0, 0]
        )
        blob.move_head(
            start_time = 13.4,
            attack = 0.2,
            rotation_quaternion = [1, -0.05, 0, 0]
        )
        blob.move_head(
            start_time = 13.6,
            attack = 0.2,
            rotation_quaternion = [1, 0, 0, 0]
        )

        jump_dur = 0.3
        for i in range(3):
            blob.move_to(
                displacement = [0, 0.2, 0],
                start_time = 16 + i * jump_dur,
                end_time = 16 + i * jump_dur + jump_dur / 3,
            )
            blob.move_to(
                displacement = [0, -0.2, 0],
                start_time = 16 + i * jump_dur + jump_dur / 3,
                end_time = 16 + (i + 1) * jump_dur,
            )

        dna = import_object(
            'dna_two_strand', 'biochem',
            location = [0, 0, 0],
        )
        dna.add_to_blender(appear_time = 0)
        dna.tweak_colors_recursive()

        sotf.morph_figure(2, start_time = 12.5)
        for i in range(13, 24):
            char = sotf.lookup_table[2][i]
            char.color_shift(
                color = COLORS_SCALED[4],
                start_time = 12.5,
                duration_time = None
            )
        for i in range(24, 25):
            char = sotf.lookup_table[3][i]
            char.color_shift(
                color = COLORS_SCALED[4],
                start_time = 12.5,
                duration_time = None
            )
        sotf.morph_figure(3, start_time = 15.5)

        to_disappear = [sotf, blob]
        end = 19
        for i, thing in enumerate(to_disappear):
            thing.disappear(disappear_time = end - (len(to_disappear) - 1 - i) * 0.05)

    def sim_rules(self):
        cam_bobj, cam_swivel = cam_and_swivel(
            cam_location = [0, 0, 34],
            cam_rotation_euler = [0, 0, 0],
            cam_name = "Camera Bobject",
            swivel_location = [0, 0, 0],
            swivel_rotation_euler = [74 * math.pi / 180, 0, 0],
            swivel_name = 'Cam swivel',
            #control_sun = True
        )
        cam_swivel.add_to_blender(appear_time = -1, animate = False)

        world = natural_sim.DrawnNaturalSim(
            scale = 2.8,
            food_count = 50,
            #initial_energy = 1500,
            #dimensions = [75, 75],
            sim = 'if_world_intro',
            #initial_creatures = 3,
            location = [0, 0, 0],
            day_length_style = 'fixed_speed',
            #day_length_style = 'fixed_length'
        )
        num_days = 10
        '''for i in range(num_days):
            save = False
            if i == num_days - 1:
                save = True
            world.sim.sim_next_day(save = save)'''

        for date in range(num_days):
            world.sim.date_records[date]['anim_durations'] = {
                'dawn' : 1, #Put out food and creatures
                'morning' : 0.5, #pause after setup
                'day' : 2, #creatures go at it
                'evening' : 0.5, #pause before reset
                'night' : 0.5 #reset
            }
        world.add_to_blender(appear_time = 24, start_delay = 1)

        cam_swivel.move_to(
            new_location = [0, 0, 2.8],
            start_time = 38
        )

        nf = tex_bobject.TexBobject(
            '\\text{No food} \\longrightarrow \\text{Death}',
            location = [0, 10, 9],
            rotation_euler = cam_swivel.ref_obj.rotation_euler,
            centered = True,
            scale = 2
        )
        of = tex_bobject.TexBobject(
            '\\text{One food} \\longrightarrow \\text{Live on}',
            location = [0, 10, 6.25],
            rotation_euler = cam_swivel.ref_obj.rotation_euler,
            centered = True,
            scale = 2
        )
        tf = tex_bobject.TexBobject(
            '\\text{Two or more} \\longrightarrow \\text{Replicate}',
            location = [0, 10, 3.5],
            rotation_euler = cam_swivel.ref_obj.rotation_euler,
            centered = True,
            scale = 2
        )
        nf.add_to_blender(appear_time = 39)
        of.add_to_blender(appear_time = 40)
        tf.add_to_blender(appear_time = 41)


        to_disappear = [world, nf, of, tf]
        for i, thing in enumerate(to_disappear):
            thing.disappear(disappear_time = 46.5 - (len(to_disappear) - 1 - i) * 0.05)

    def traits(self):
        blob = Blobject(
            location = [7.5, 0, 0],
            scale = 4,
            wiggle = True,
            mouth = True
        )
        blob.add_to_blender(appear_time = 1)

        speed = tex_bobject.TexBobject(
            '\\text{Speed}',
            '\\text{Speed}\\uparrow',
            location = [-12, 5, 0],
            #rotation_euler = cam_swivel.ref_obj.rotation_euler,
            centered = False,
            scale = 4
        )
        size = tex_bobject.TexBobject(
            '\\text{Size}',
            '\\text{Size}\\uparrow',
            location = [-12, 0, 0],
            #rotation_euler = cam_swivel.ref_obj.rotation_euler,
            centered = False,
            scale = 4
        )
        sense = tex_bobject.TexBobject(
            '\\text{Sense}',
            '\\text{Sense}\\uparrow',
            location = [-12, -5, 0],
            #rotation_euler = cam_swivel.ref_obj.rotation_euler,
            centered = False,
            scale = 4
        )

        speed.add_to_blender(appear_time = 2)
        size.add_to_blender(appear_time = 3)
        sense.add_to_blender(appear_time = 4)

        speed.morph_figure(1, start_time = 5)
        obj = blob.ref_obj.children[0].children[0]
        shift_frames = 60
        color_set = [COLORS_SCALED[6], COLORS_SCALED[4], COLORS_SCALED[3], COLORS_SCALED[5]]
        num = len(color_set)
        for i in range(num):
            blob.color_shift(
                duration_time = None,
                color = color_set[i],
                start_time = 5 + i * shift_frames / num / FRAME_RATE,
                shift_time = shift_frames / num,
                obj = obj
            )

        size.morph_figure(1, start_time = 7)
        blob.move_to(new_scale = 7, start_time = 7)

        sense.morph_figure(1, start_time = 9)
        eyes = []
        for obj in blob.ref_obj.children[0].children:
            if 'Eye' in obj.name:
                eyes.append(obj)
        for eye in eyes:
            eye.keyframe_insert(data_path = 'scale', frame = 9 * FRAME_RATE)
            eye.scale = [
                1.5,
                1.5,
                1.5,
            ]
            eye.keyframe_insert(data_path = 'scale', frame = 9.5 * FRAME_RATE)

        to_disappear = [blob, sense, size, speed]
        for i, thing in enumerate(to_disappear):
            thing.disappear(disappear_time = 13 - (len(to_disappear) - 1 - i) * 0.05)

    def diverse_stalling_sim(self):
        cam_bobj, cam_swivel = cam_and_swivel(
            cam_location = [0, 0, 34],
            cam_rotation_euler = [0, 0, 0],
            cam_name = "Camera Bobject",
            swivel_location = [0, 0, 0],
            swivel_rotation_euler = [74 * math.pi / 180, 0, 0],
            swivel_name = 'Cam swivel',
            #control_sun = True
        )
        cam_swivel.add_to_blender(appear_time = -1, animate = False)

        world = natural_sim.DrawnNaturalSim(
            scale = 2.8,
            food_count = 50,
            #initial_energy = 1500,
            #dimensions = [75, 75],
            #sim = 'ns_env_intro_4',
            #initial_creatures = 3,
            location = [0, 0, 0],
            day_length_style = 'fixed_speed',
            #day_length_style = 'fixed_length'
        )
        num_days = 1
        for i in range(num_days):
            save = False
            if i == num_days - 1:
                save = True
            world.sim.sim_next_day(save = save)

        world.sim.date_records[0]['anim_durations'] = {
            'dawn' : 1, #Put out food and creatures
            'morning' : 0.5, #pause after setup
            'day' : 2, #creatures go at it
            'evening' : 0.5, #pause before reset
            'night' : 0.5 #reset
        }
        world.add_to_blender(appear_time = 0, start_delay = 1)


        world.disappear(disappear_time = 13)

    def fast_altruism(self):
        t = tex_bobject.TexBobject(
            '\\text{Way 1:}',
            '\\text{Way 1: Leave food for others}',
            centered = True,
            scale = 2,
            location = [0, 6, 0]
        )
        t.add_to_blender(appear_time = 0)
        t.morph_figure(1, start_time = 2)

        food = import_object(
            'goodicosphere', 'primitives',
            location = [0, -6, 0],
            scale = 0.5
        )
        apply_material(food.ref_obj.children[0], 'color7')
        food.add_to_blender(appear_time = 0)

        s_blob = Blobject(
            location = [10, -2.7, -10],
            rotation_euler = [0, -45 * math.pi / 180, 0],
            scale = 4,
            #mat = 'creature_color8',
            mouth = True
        )
        s_blob.add_to_blender(appear_time = 1)
        pursuit_start = 2
        s_blob.hold_object(start_time = pursuit_start)
        s_blob.move_head(
            start_time = pursuit_start,
            rotation_quaternion = [1, 0, 0.1, -0.1]
        )
        s_blob.move_to(
            new_location = [
                food.ref_obj.location[0],
                s_blob.ref_obj.location[1],
                food.ref_obj.location[2],
            ],
            start_time = pursuit_start,
            end_time = 40
        )

        for fc in s_blob.ref_obj.animation_data.action.fcurves:
            if fc.data_path == 'location':
                for kp in fc.keyframe_points:
                    kp.interpolation = 'LINEAR'



        nom_start = pursuit_start
        nom_duration = 0.5
        num_noms = 100
        initial_mouth_scale = list(s_blob.mouth.scale)
        s_blob.mouth.keyframe_insert(
            data_path = 'scale',
            frame = nom_start * FRAME_RATE
        )
        for i in range(num_noms):
            s_blob.mouth.scale[1] = 0.1
            s_blob.mouth.keyframe_insert(
                data_path = 'scale',
                frame = (nom_start + (i + 0.5) * nom_duration) * FRAME_RATE
            )
            s_blob.mouth.scale[1] = initial_mouth_scale[1]
            s_blob.mouth.keyframe_insert(
                data_path = 'scale',
                frame = (nom_start + (i + 1) * nom_duration) * FRAME_RATE
            )





        f_blob = Blobject(
            location = [-22, s_blob.ref_obj.location[1], -5],
            rotation_euler = [0, 90 * math.pi / 180, 0],
            scale = 4,
            mat = 'creature_color4',
        )
        f_blob.add_to_blender(appear_time = 0)
        f_blob.move_to(
            new_location = [
                -5,
                f_blob.ref_obj.location[1],
                f_blob.ref_obj.location[2],
            ],
            start_time = 4,
            end_time = 5
        )

        #Look at food
        f_blob.move_to(
            new_angle = [0, 45 * math.pi / 180, 0],
            start_time = 6
        )
        f_blob.move_head(
            rotation_quaternion = [1, 0, 0, -0.2],
            start_time = 6
        )

        #Look at slow blob
        f_blob.move_to(
            new_angle = [0, 115 * math.pi / 180, 0],
            start_time = 7
        )
        f_blob.move_head(
            rotation_quaternion = [1, 0, 0, 0],
            start_time = 7
        )

        #Look at food
        f_blob.move_to(
            new_angle = [0, 45 * math.pi / 180, 0],
            start_time = 8
        )
        f_blob.move_head(
            rotation_quaternion = [1, 0, 0, -0.2],
            start_time = 8
        )

        #Look at camera
        f_blob.move_to(
            new_angle = [0, 0, 0],
            start_time = 9
        )
        f_blob.move_head(
            rotation_quaternion = [1, 0, 0, 0],
            start_time = 9
        )

        f_blob.wince(
            start_time = 10.5,
            end_time = 12
        )

        #leave
        f_blob.move_to(
            start_time = 12,
            new_angle = [0, - math.pi / 2, 0]
        )
        f_blob.move_to(
            start_time = 12.3,
            new_location = [-22, s_blob.ref_obj.location[1], -5],
        )

        to_disappear = [t, s_blob, food]
        for i, thing in enumerate(to_disappear):
            thing.disappear(disappear_time = 15 - (len(to_disappear) - 1 - i) * 0.05)

    def big_altruism(self):
        t = tex_bobject.TexBobject(
            '\\text{Way 2:}',
            '\\text{Way 2: Not cannibalism}',
            '\\text{Way 2: Not cannibalism?}',
            '\\text{Way 2: Not cannibalism!}',
            centered = True,
            scale = 2,
            location = [0, 6, 0]
        )
        t.add_to_blender(appear_time = 0)
        t.morph_figure(1, start_time = 2)
        t.morph_figure(2, start_time = 4)
        t.morph_figure(3, start_time = 6)

        l_blob = Blobject(
            mat = 'creature_color6',
            scale = 1,
            location = [-7, -5.5, 0]
        )
        l_blob.add_to_blender(appear_time = 0)
        #Displace actual model
        l_blob.ref_obj.children[0].location = [-3, 0, 0]
        l_blob.spin(
            start_time = 0,
            end_time = 1000 #Why not?
        )
        l_blob.blob_wave(
            start_time = 0,
            duration = 100
        )



        b_blob = Blobject(
            mat = 'creature_color7',
            scale = 5,
            location = [-3, 0, 0]
        )
        #b_blob.add_to_blender(appear_time = 0)
        b_handle = bobject.Bobject(
            b_blob,
            location = [22, -2, 0],
            rotation_euler = [0, - math.pi / 2, 0],
            name = 'handle'
        )
        b_handle.add_to_blender(appear_time = 0)

        b_handle.move_to(
            new_location = [
                5,
                b_handle.ref_obj.location[1],
                b_handle.ref_obj.location[2],
        ],
            start_time = 4,
            end_time = 5
        )

        b_blob.move_head(
            rotation_quaternion = [1, 0, 0.1, -0.2],
            start_time = 6,
        )
        b_blob.move_head(
            rotation_quaternion = [1, 0, 0, 0],
            start_time = 7,
        )
        b_handle.spin(
            start_time = 7,
            end_time = 100000000
        )
        b_blob.blob_wave(
            start_time = 7,
            duration = 100
        )

        to_disappear = [t, l_blob, b_handle]
        for i, thing in enumerate(to_disappear):
            thing.disappear(disappear_time = 15 - (len(to_disappear) - 1 - i) * 0.05)

    def altruism_trait(self):
        blob = Blobject(
            location = [7.5, 0, 0],
            scale = 6,
            #wiggle = True,
            mouth = True
        )
        traits = tex_bobject.TexBobject(
            '\\underline{\\text{Traits}}',
            location = [-12.75, 5, 0],
            #rotation_euler = cam_swivel.ref_obj.rotation_euler,
            centered = False,
            scale = 3
        )
        speed = tex_bobject.TexBobject(
            '\\text{Speed}',
            location = [-12, 2, 0],
            #rotation_euler = cam_swivel.ref_obj.rotation_euler,
            centered = False,
            scale = 2
        )
        size = tex_bobject.TexBobject(
            '\\text{Size}',
            location = [-12, -0.25, 0],
            #rotation_euler = cam_swivel.ref_obj.rotation_euler,
            centered = False,
            scale = 2
        )
        sense = tex_bobject.TexBobject(
            '\\text{Sense}',
            location = [-12, -2.5, 0],
            #rotation_euler = cam_swivel.ref_obj.rotation_euler,
            centered = False,
            scale = 2
        )

        blob.add_to_blender(appear_time = 0)
        traits.add_to_blender(appear_time = 0)
        speed.add_to_blender(appear_time = 0.2)
        size.add_to_blender(appear_time = 0.4)
        sense.add_to_blender(appear_time = 0.6)


        at = tex_bobject.TexBobject(
            '\\text{Altruism chance}',
            location = [-12, -4.75, 0],
            #rotation_euler = cam_swivel.ref_obj.rotation_euler,
            centered = False,
            scale = 2,
            color = 'color5'
        )

        #blob.move_to(displacement = [0, 2, 0], start_time = 5)
        #speed.move_to(displacement = [0, 1, 0], start_time = 5)
        #size.move_to(displacement = [0, 2, 0], start_time = 5)
        #sense.move_to(displacement = [0, 3, 0], start_time = 5)
        at.add_to_blender(appear_time = 3)

        blob.evil_pose(
            start_time = 5,
            end_time = 7
        )

        blob.hold_gift(start_time = 7)
        blob.move_to(start_time = 7, new_angle = [0, -15 * math.pi / 180, 0])

    def how_to_be_altruistic(self):
        #cues = self.subscenes['sense']
        #st = cues['start']

        text = tex_bobject.TexBobject(
            '\\text{Option 1: Go home and reproduce}',
            location = [0, 5.5, 0],
            scale = 2,
            color = 'color2',
            centered = True
        )
        text.add_to_blender(appear_time = 56.5)
        text.move_to(
            new_location = [0, 6.5, 0],
            start_time = 25
        )
        text2 = tex_bobject.TexBobject(
            '\\text{Option 2: Give away precious food}',
            location = [0, 4, 0],
            scale = 2,
            color = 'color2',
            centered = True
        )
        text2.add_to_blender(appear_time = 61.5)


        blob = Blobject(
            mat = 'creature_color3',
            scale = 4,
            location = [18, -3.5, -22],
            rotation_euler = [0, -math.pi / 8, 0],
            #wiggle = True
        )
        blob.add_to_blender(appear_time = 51)


        food = import_object(
            'goodicosphere', 'primitives',
            location = [4, -6.5, 0],
            scale = 0.5
        )
        apply_material(food.ref_obj.children[0], 'color7')
        food.add_to_blender(appear_time = 50.6)

        food2 = import_object(
            'goodicosphere', 'primitives',
            location = [10, -6.5, -11],
            scale = 0.5
        )
        apply_material(food2.ref_obj.children[0], 'color7')
        food2.add_to_blender(appear_time = 50.7)


        start = 51.5
        stop = 55
        blob.move_to(
            new_location = [5, -3.5, 0],
            start_time = start,
            end_time = stop
        )

        blob.blob_scoop(start_time = start + (stop - start) * 1.5 / 4, duration = (stop - start) / 4)
        blob.eat_animation(
            start_frame = (start + (stop - start) * 1.5 / 4) * FRAME_RATE,
            end_frame = (start + (stop - start) * 2.1 / 4) * FRAME_RATE
        )
        food2.move_to(
            new_location = [10, -2.5, -7],
            start_time = start + (stop - start) * 1.5 / 4,
            end_time = start + (stop - start) * 1.8 / 4
        )
        food2.move_to(
            new_location = [10.5, -2.5, -11],
            new_scale = 0,
            start_time = start + (stop - start) * 1.8 / 4,
            end_time = start + (stop - start) * 2.1 / 4
        )

        blob.blob_scoop(start_time = start + (stop - start) * 3.5 / 4, duration = 1)
        food.move_to(
            new_location = [3.65, -2.5, 4],
            start_time = start + (stop - start) * 3.5 / 4,
            end_time = start + (stop - start) * 3.8 / 4
        )
        food.move_to(
            new_location = [4.5, -2.5, 0],
            new_scale = 0,
            start_time = start + (stop - start) * 3.8 / 4,
            end_time = stop + (stop - start) * 0.1 / 4
        )
        blob.eat_animation(
            start_frame = (start + (stop - start) * 3.5 / 4) * FRAME_RATE,
            end_frame = (stop + (stop - start) * 0.1 / 4) * FRAME_RATE
        )
        #Face ahead
        blob.move_to(
            new_angle = [0, 0, 0],
            start_time = stop
        )

        rep_indicator = tex_bobject.TexBobject(
            '\\substack{\\text{Replication} \\\\ \\text{chance}} = 0\\%',
            '\\substack{\\text{Replication} \\\\ \\text{chance}} = 100\\%',
            '\\substack{\\text{Replication} \\\\ \\text{chance}} = 0\\%',
            location = [18, 1, -22],
            scale = 0.8,
            color = 'color2',
            centered = True
        )
        rep_indicator.add_to_blender(appear_time = 51.3)
        for i in range(18, 20):
            char = rep_indicator.lookup_table[0][i]
            char.color_shift(
                color = COLORS_SCALED[5],
                start_time = -1,
                duration_time = None
            )

        rep_indicator.move_to(
            new_location = [5, 1, 0],
            start_time = start,
            end_time = stop
        )
        rep_indicator.morph_figure(1, start_time = stop)
        for i in range(18, 22):
            char = rep_indicator.lookup_table[1][i]
            char.color_shift(
                color = COLORS_SCALED[6],
                start_time = stop,
                duration_time = None
            )


        #Start to walk away
        blob.move_to(
            new_angle = [0, -math.pi / 4, 0],
            start_time = 56.5
        )
        #Walk away
        blob.move_to(
            new_angle = [0, math.pi / 2, 0],
            start_time = 58.2
        )
        blob.move_to(
            new_location = [11, -3.5, 0],
            start_time = 58.5,
            end_time = 61
        )
        rep_indicator.move_to(
            new_location = [11, 1, 0],
            start_time = 58.5,
            end_time = 61
        )

        #Look down
        blob.move_head(
            rotation_quaternion = [1, 0, 0, -0.3],
            start_time = 61.5
        )

        #Turn back
        blob.move_head(
            rotation_quaternion = [1, 0, 0, 0],
            start_time = 62.6
        )
        blob.move_to(
            new_angle = [0, -math.pi / 2, 0],
            start_time = 62.7
        )
        blob.move_to(
            new_location = [5, -3.5, 0],
            start_time = 63,
            end_time = 65.5
        )
        rep_indicator.move_to(
            new_location = [5, 1, 0],
            start_time = 63,
            end_time = 65.5
        )



        l_blob = Blobject(
            mat = 'creature_color3',
            scale = 4,
            location = [-5, -3.5, -3]
        )
        l_blob.add_to_blender(appear_time = 50.5)
        #Displace actual model
        l_blob.ref_obj.children[0].location = [-3/4, 0, 0]
        l_blob.move_to(
            new_angle = [0, 2 * math.pi * (44 + 1/4), 0],
            start_time = 0,
            end_time = 66.5
        )
        make_animations_linear(l_blob.ref_obj, data_paths = ['rotation_euler'])
        l_blob.blob_wave(
            start_time = 0,
            duration = 66.5
        )
        surv_indicator = tex_bobject.TexBobject(
            '\\substack{\\text{Survival} \\\\ \\text{chance}} = 0\\%',
            '\\substack{\\text{Survival} \\\\ \\text{chance}} = 100\\%',
            location = [
                0,
                1 / l_blob.ref_obj.scale[0] / l_blob.ref_obj.children[0].scale[0] - l_blob.ref_obj.location[1],
                0
            ],
            rotation_euler = [0, -math.pi / 2, 0],
            scale = 0.8 / l_blob.ref_obj.scale[0] / l_blob.ref_obj.children[0].scale[0],
            color = 'color2',
            centered = True
        )
        surv_indicator.ref_obj.parent = l_blob.ref_obj.children[0]
        for i in range(15, 17):
            char = surv_indicator.lookup_table[0][i]
            char.color_shift(
                color = COLORS_SCALED[5],
                start_time = -1,
                duration_time = None
            )
        surv_indicator.add_to_blender(appear_time = 27)
        surv_indicator.move_to(
            new_angle = [0, -2 * math.pi * (44 + 1/4), 0],
            start_time = 0,
            end_time = 66.5
        )
        make_animations_linear(surv_indicator.ref_obj, data_paths = ['rotation_euler'])


        blob.hold_object(start_time = 67, end_time = 67.5)
        food.move_to(
            new_location = [0, -2.5, 0],
            new_scale = 0.5,
            start_time = 67,
            end_time = 67.3
        )
        food.move_to(
            new_location = [-5, -2.5, 0],
            new_scale = 0,
            start_time = 67.3,
            end_time = 67.6
        )
        blob.eat_animation(start_frame = 67 * FRAME_RATE, end_frame = 67.5 * FRAME_RATE)
        l_blob.eat_animation(start_frame = 67.2 * FRAME_RATE, end_frame = 67.9 * FRAME_RATE)
        rep_indicator.morph_figure(2, start_time = 67)
        for i in range(18, 20):
            char = rep_indicator.lookup_table[2][i]
            char.color_shift(
                color = COLORS_SCALED[5],
                start_time = 67,
                duration_time = None
            )
        surv_indicator.morph_figure(1, start_time = 67.2)
        for i in range(15, 19):
            char = surv_indicator.lookup_table[1][i]
            char.color_shift(
                color = COLORS_SCALED[6],
                start_time = 67.2,
                duration_time = None
            )

        '''rep_indicator.morph_figure(3, start_time = 60)
        for i in range(18, 21):
            char = rep_indicator.lookup_table[3][i]
            char.color_shift(
                color = COLORS_SCALED[4],
                start_time = 67,
                duration_time = None
            )'''

        to_disappear = [text, text2, l_blob, surv_indicator, blob, rep_indicator]
        disappear_time = 71.5
        for i, thing in enumerate(to_disappear):
            thing.disappear(disappear_time = disappear_time - (len(to_disappear) - 1 - i) * 0.05)

    def count_by_vals(date, to_count, vals, nat_sim):
        counts = []
        creatures = nat_sim.date_records[date]['creatures']
        for val in vals:
            count = 0
            if to_count == 'altruist':
                count = len([x for x in creatures if x.altruist == val])
            elif to_count == 'green_beard':
                count = len([x for x in creatures if x.green_beard == val])
            if to_count == 'sep_green_beard':
                count = len([x for x in creatures if x.gbo == val[0] and x.a_gb == val[1]])
            elif to_count == 'kin_altruist':
                count = len([x for x in creatures if x.kin_altruist == val])
            counts.append(count)
        return counts

    def make_graph_bars(graph, num_bars, appear_time, bar_width):
        bars = []
        space_width = (graph.x_range[1] - num_bars * bar_width) / (num_bars + 1)
        for i in range(num_bars):
            if i == 0:
                color = 'color3'
            elif i == num_bars - 1:
                color = 'color6'
            elif i == 1:
                color = 'color7'
            elif i == 2:
                color = 'color4'
            bar = graph.add_bar(
                appear_time = appear_time,
                x = (1 + i) * space_width + bar_width * (0.5 + i),
                value = 0,
                dx = bar_width,
                color = color
            )
            bars.append(bar)
        return bars

    def update_graph_bars(graph, start_time, bars, counts, end_time = None, fractional = True):
        if fractional == True:
            total = sum(counts)
            for i, bar in enumerate(bars):
                graph.update_bar(
                    bar = bar,
                    new_value = counts[i] / total * 100,
                    start_time = start_time,
                    end_time = end_time
                )
        else:
            for i, bar in enumerate(bars):
                graph.update_bar(
                    bar = bar,
                    new_value = counts[i],
                    start_time = start_time,
                    end_time = end_time
                )

    def simulation_scene(
        self,
        animate_graph = True,
        animate_sim = False,
        sim_name = None,
        scene_open_time = 0,
        simulation_start_time = 10,
        sim_speed_up_factor = 1,
        sim_start_date = 0,
        sim_end_date = None,
        label_complex = None,
        graph_label_strings = [],
        graph_type = None,
        vals_to_count = [True, False],
        num_bars = 2,
        bar_width = 0.5,
        states_to_draw = [],
        outro_length = 10,
        outro_sway = True
    ):
        '''if animate_graph:
            cam_control_sun = True
        if animate_sim:
            cam_control_sun = True
        if animate_graph == True and animate_sim == True:
            print('WARNING: Animating both graph and sim. Lighting will be off for graph and tex!')'''

        cam_bobj, cam_swivel = cam_and_swivel(
            cam_location = [0, 0, 34],
            cam_rotation_euler = [0, 0, 0],
            cam_name = "Camera Bobject",
            swivel_location = [0, 0, 4],
            swivel_rotation_euler = [74 * math.pi / 180, 0, 0],
            swivel_name = 'Cam swivel',
            control_sun = False #cam_control_sun
        )
        cam_swivel.add_to_blender(appear_time = -1)



        #Make and animate simulation animation
        sim = natural_sim.DrawnNaturalSim(
            sim = sim_name,
            scale = 1.5,
            location = [-6.5, 0, 0],
            day_length_style = 'fixed_length'
        )

        to_disappear = [sim]

        if sim_end_date == None:
            sim_end_date = len(sim.sim.date_records) - 1

        for record in sim.sim.date_records:
            durs = record['anim_durations']
            for key in durs:
                durs[key] /= sim_speed_up_factor

        #Prep simulation durations. Important even when sim isn't animated,
        #because the graph needs to sync its updates
        sim_appearance_time = scene_open_time
        first_day_start = simulation_start_time
        #Find proper duration for first morning pause to fill talking time
        initial_day_durs = sim.sim.date_records[0]['anim_durations']
        first_morning_dur = first_day_start - \
                           sim_appearance_time - \
                           initial_day_durs['dawn'] - \
                           sim.start_delay
        initial_day_durs['morning'] = first_morning_dur

        if animate_graph == True:
            #Simluation_label
            label_complex.add_to_blender(appear_time = scene_open_time)
            to_disappear.append(label_complex)



            #Graph
            g = graph_bobject.GraphBobject(
                location = [2, -4, 0],
                rotation_euler = [74 * math.pi / 180, 0, 0],
                width = 10,
                x_range = num_bars,
                x_label = '\\phantom{a}',
                height = 10,
                y_range = 100,
                y_label = '\\%\\text{ Creatures}',
                y_label_pos = 'end',
                tick_step = [10, 50],
                #include_y = True,
                arrows = False,
                padding = 0
            )
            to_disappear.append(g)

            graph_appear_time = scene_open_time

            space_width = (g.x_range[1] - num_bars * bar_width) / (num_bars + 1)
            bars = InclusiveFitness.make_graph_bars(g, num_bars, graph_appear_time, bar_width)

            y_offset = -0.7
            lab_scale = 1
            if num_bars == 4:
                y_offset = -0.4
                lab_scale = 0.6

            for i, string in enumerate(graph_label_strings):
                lab = tex_bobject.TexBobject(
                    string,
                    location = [
                        ((1 + i) * space_width + (0.5 + i) * bar_width) * g.width / g.x_range[1],
                        y_offset,
                        0
                    ],
                    color = 'color5',
                    centered = 'top_centered',
                    scale = lab_scale
                )
                g.add_subbobject(lab)


            g.add_to_blender(appear_time = graph_appear_time)

            for state in states_to_draw:
                InclusiveFitness.update_graph_bars(g, state[0], bars, state[1], fractional = False)


            time_so_far = scene_open_time + sim.start_delay
            for day in sim.sim.date_records:
                date = day['date']
                if date < sim_start_date:
                    time_so_far += day['anim_durations']['dawn'] + \
                                day['anim_durations']['morning'] + \
                                day['anim_durations']['day'] + \
                                day['anim_durations']['evening'] + \
                                day['anim_durations']['night']

                if date >= sim_start_date and date <= sim_end_date:
                    start_time = time_so_far
                    end_time = start_time + day['anim_durations']['dawn']

                    if date == 0:
                        end_time += day['anim_durations']['morning']
                        start_time = end_time - OBJECT_APPEARANCE_TIME / FRAME_RATE

                    counts = InclusiveFitness.count_by_vals(date, graph_type, vals_to_count, sim.sim)
                    InclusiveFitness.update_graph_bars(g, start_time, bars, counts, end_time = end_time)
                    time_so_far += day['anim_durations']['dawn'] + \
                                    day['anim_durations']['morning'] + \
                                    day['anim_durations']['day'] + \
                                    day['anim_durations']['evening'] + \
                                    day['anim_durations']['night']

                    if date == sim_end_date:
                        graph_end_time = time_so_far

        if animate_sim == True:
            sim.add_to_blender(
                appear_time = sim_appearance_time,
                start_day = sim_start_date,
                end_day = sim_end_date
            )
            sim_end_time = sim.elapsed_time + scene_open_time

        if animate_graph and animate_sim:
            print(str(graph_end_time) + ' ' + str(sim_end_time))
            if abs(graph_end_time - sim_end_time) > 0.01: #
                raise Warning('Sim and graph animations not in sync: ' + str(graph_end_time) + ' ' + str(sim_end_time))
            outro_start_time = graph_end_time
        elif animate_graph:
            outro_start_time = graph_end_time
        elif animate_sim:
            outro_start_time = sim_end_time + scene_open_time
        else:
            raise Warning('Not animating graph or sim')

        if outro_sway == True:
            if outro_length < 2:
                raise Warning('Outro too short for swaying')
            sway_start_time = outro_start_time + 1
            sway_length = outro_length - 2
            num_sways = max(math.floor(sway_length / 10), 1)
            time_per_sway = sway_length / (num_sways + 1)
            for i in range(num_sways):
                sway_sign = (i%2 - 0.5) * 2
                cam_swivel.move_to(
                    start_time = sway_start_time + i * time_per_sway,
                    end_time = sway_start_time + (i + 1) * time_per_sway,
                    new_angle = [74 * math.pi / 180, 0, sway_sign * 5 * math.pi / 180]
                )
            cam_swivel.move_to(
                start_time = sway_start_time + sway_length - time_per_sway,
                end_time = sway_start_time + sway_length,
                new_angle = [74 * math.pi / 180, 0, 0 * math.pi / 180]
            )

        end = outro_start_time + outro_length
        for i, thing in enumerate(to_disappear):
            thing.disappear(disappear_time = end - (len(to_disappear) - 1 - i) * 0.05)

        bpy.data.scenes["Scene"].frame_start = scene_open_time * FRAME_RATE
        bpy.data.scenes["Scene"].frame_end = end * FRAME_RATE - 1

        if animate_graph == True:
            #Add camera to layer 2
            bpy.ops.object.lamp_add(type = LAMP_TYPE)
            lamp = bpy.context.object
            lamp.data.node_tree.nodes[1].inputs[1].default_value = 1.57
            lamp_bobj = bobject.Bobject(
                objects = [lamp],
                rotation_euler = [74 * math.pi / 180, 0, 0]
            )
            lamp_bobj.add_to_blender(appear_time = -1)

            #Set up layers
            def move_to_layer_recursive(obj, layer = None):
                for child in obj.children:
                    move_to_layer_recursive(child, layer = layer)
                obj.layers[layer] = True
                for i in range(20):
                    obj.layers[i] = (i == layer)

            for bobj in [g, label_complex, lamp_bobj]:
                move_to_layer_recursive(bobj.ref_obj, layer = 1)

            bpy.context.scene.layers[1] = True

        return outro_start_time, cam_bobj
        #To let scenes do other things based on the sim end time, which isn't
        #explicity set in the params.

    def random_altruism_sim(self):
        tex = tex_bobject.TexBobject(
            '\\text{Altruism v1}',
            scale = 2,
            #location = [-6.5, 0, 8],
            #rotation_euler = [74 * math.pi / 180, 0, 0],
            color = 'color2',
            centered = True
        )
        #tex.add_to_blender(appear_time = 1)

        mut = tex_bobject.TexBobject(
            '\\text{Mutation chance: } 5\\%',
            scale = 1,
            #location = [-6.5, 0, 8],
            #rotation_euler = [74 * math.pi / 180, 0, 0],
            color = 'color2',
            centered = True
        )

        comp = tex_complex.TexComplex(
            tex, mut,
            location = [-6.5, 0, 8],
            rotation_euler = [74 * math.pi / 180, 0, 0],
            centered = True,
            multiline = True,
            line_height = 1.4
        )

        states_to_draw = [
            [73.5 , [50,0]],
            [79 ,[50, 50]],
            [87 ,[10, 90]],
            [89 ,[90, 10]],
            [92 ,[50 , 50]],
        ]





        self.simulation_scene(
            animate_graph = True,
            animate_sim = False,
            sim_name = 'random_20',
            scene_open_time = 72,
            simulation_start_time = 98,
            sim_speed_up_factor = 5,
            sim_start_date = 0,
            sim_end_date = 1,
            label_complex = comp,
            graph_label_strings = ['\\text{Altruistic}', '\\text{Not}'],
            graph_type = 'altruist',
            num_bars = 2,
            states_to_draw = states_to_draw,
            outro_length = 11.5,
            outro_sway = True
        )

    def less_punishing(self):
        cam_bobj, cam_swivel = cam_and_swivel(
            cam_location = [0, -3, 24.5],
            cam_rotation_euler = [0, 0, 0],
            cam_name = "Camera Bobject",
            swivel_location = [0, 0, 0],
            swivel_rotation_euler = [0, 0, 0],
            swivel_name = 'Cam swivel',
            #control_sun = True
        )
        cam_swivel.add_to_blender(appear_time = 0)

        blob = Blobject(
            mat = 'creature_color3',
            scale = 4,
            location = [18, -3.5, -22],
            rotation_euler = [0, -math.pi / 8, 0],
            #wiggle = True
        )
        blob.add_to_blender(appear_time = 111.5)


        food = import_object(
            'goodicosphere', 'primitives',
            location = [4, -6.5, 0],
            scale = 0.5
        )
        apply_material(food.ref_obj.children[0], 'color7')
        food.add_to_blender(appear_time = 111.1)

        food2 = import_object(
            'goodicosphere', 'primitives',
            location = [10, -6.5, -11],
            scale = 0.5
        )
        apply_material(food2.ref_obj.children[0], 'color7')
        food2.add_to_blender(appear_time = 111.2)


        start = 112 #51.5
        stop = 115.5 #55
        blob.move_to(
            new_location = [5, -3.5, 0],
            start_time = start,
            end_time = stop
        )

        blob.blob_scoop(start_time = start + (stop - start) * 1.5 / 4, duration = (stop - start) / 4)
        blob.eat_animation(
            start_frame = (start + (stop - start) * 1.5 / 4) * FRAME_RATE,
            end_frame = (start + (stop - start) * 2.1 / 4) * FRAME_RATE
        )
        food2.move_to(
            new_location = [10, -2.5, -7],
            start_time = start + (stop - start) * 1.5 / 4,
            end_time = start + (stop - start) * 1.8 / 4
        )
        food2.move_to(
            new_location = [10.5, -2.5, -11],
            new_scale = 0,
            start_time = start + (stop - start) * 1.8 / 4,
            end_time = start + (stop - start) * 2.1 / 4
        )

        blob.blob_scoop(start_time = start + (stop - start) * 3.5 / 4, duration = 1)
        food.move_to(
            new_location = [3.65, -2.5, 4],
            start_time = start + (stop - start) * 3.5 / 4,
            end_time = start + (stop - start) * 3.8 / 4
        )
        food.move_to(
            new_location = [4.5, -2.5, 0],
            new_scale = 0,
            start_time = start + (stop - start) * 3.8 / 4,
            end_time = stop + (stop - start) * 0.1 / 4
        )
        blob.eat_animation(
            start_frame = (start + (stop - start) * 3.5 / 4) * FRAME_RATE,
            end_frame = (stop + (stop - start) * 0.1 / 4) * FRAME_RATE
        )
        #Face ahead
        blob.move_to(
            new_angle = [0, 0, 0],
            start_time = stop
        )

        rep_indicator = tex_bobject.TexBobject(
            '\\substack{\\text{Replication} \\\\ \\text{chance}} = 0\\%',
            '\\substack{\\text{Replication} \\\\ \\text{chance}} = 100\\%',
            '\\substack{\\text{Replication} \\\\ \\text{chance}} = 0\\%',
            '\\substack{\\text{Replication} \\\\ \\text{chance}} = 50\\%',
            location = [18, 1, -22],
            scale = 0.8,
            color = 'color2',
            centered = True
        )
        rep_indicator.add_to_blender(appear_time = 111.8)
        for i in range(18, 20):
            char = rep_indicator.lookup_table[0][i]
            char.color_shift(
                color = COLORS_SCALED[5],
                start_time = -1,
                duration_time = None
            )

        rep_indicator.move_to(
            new_location = [5, 1, 0],
            start_time = start,
            end_time = stop
        )
        rep_indicator.morph_figure(1, start_time = stop)
        for i in range(18, 22):
            char = rep_indicator.lookup_table[1][i]
            char.color_shift(
                color = COLORS_SCALED[6],
                start_time = stop,
                duration_time = None
            )
        '''#Walk away
        blob.move_to(
            new_angle = [0, math.pi / 2, 0],
            start_time = 41
        )
        blob.move_to(
            new_location = [11, -3.5, 0],
            start_time = 41.5
        )
        rep_indicator.move_to(
            new_location = [11, 1, 0],
            start_time = 41.5
        )
        blob.move_head(
            rotation_quaternion = [1, 0, 0, -0.3],
            start_time = 42
        )

        blob.move_head(
            rotation_quaternion = [1, 0, 0, 0],
            start_time = 43
        )'''

        #Turn back
        '''blob.move_head(
            rotation_quaternion = [1, 0, 0, 0],
            start_time = 62.6
        )'''
        blob.move_to(
            new_angle = [0, -math.pi / 2, 0],
            start_time = 116.5
        )
        '''blob.move_to(
            new_location = [5, -3.5, 0],
            start_time = 63,
            end_time = 65.5
        )'''
        '''rep_indicator.move_to(
            new_location = [5, 1, 0],
            start_time = 63,
            end_time = 65.5
        )'''



        l_blob = Blobject(
            mat = 'creature_color3',
            scale = 4,
            location = [-5, -3.5, -3]
        )
        l_blob.add_to_blender(appear_time = 111)
        #Displace actual model
        l_blob.ref_obj.children[0].location = [-3/4, 0, 0]
        l_blob.move_to(
            new_angle = [0, 2 * math.pi * (44 + 1/4), 0],
            start_time = 0,
            end_time = 117
        )
        make_animations_linear(l_blob.ref_obj, data_paths = ['rotation_euler'])
        l_blob.blob_wave(
            start_time = 0,
            duration = 117
        )
        surv_indicator = tex_bobject.TexBobject(
            '\\substack{\\text{Survival} \\\\ \\text{chance}} = 0\\%',
            '\\substack{\\text{Survival} \\\\ \\text{chance}} = 100\\%',
            location = [
                0,
                1 / l_blob.ref_obj.scale[0] / l_blob.ref_obj.children[0].scale[0] - l_blob.ref_obj.location[1],
                0
            ],
            rotation_euler = [0, -math.pi / 2, 0],
            scale = 0.8 / l_blob.ref_obj.scale[0] / l_blob.ref_obj.children[0].scale[0],
            color = 'color2',
            centered = True
        )
        surv_indicator.ref_obj.parent = l_blob.ref_obj.children[0]
        for i in range(15, 17):
            char = surv_indicator.lookup_table[0][i]
            char.color_shift(
                color = COLORS_SCALED[5],
                start_time = -1,
                duration_time = None
            )
        surv_indicator.add_to_blender(appear_time = 0)
        surv_indicator.move_to(
            new_angle = [0, -2 * math.pi * (44 + 1/4), 0],
            start_time = 0,
            end_time = 117
        )
        make_animations_linear(surv_indicator.ref_obj, data_paths = ['rotation_euler'])


        blob.hold_object(start_time = 118, end_time = 118.5)
        food.move_to(
            new_location = [0, -2.5, 0],
            new_scale = 0.5,
            start_time = 118,
            end_time = 118.3
        )
        food.move_to(
            new_location = [-5, -2.5, 0],
            new_scale = 0,
            start_time = 118.3,
            end_time = 118.6
        )
        blob.eat_animation(start_frame = 118 * FRAME_RATE, end_frame = 118.5 * FRAME_RATE)
        l_blob.eat_animation(start_frame = 118.2 * FRAME_RATE, end_frame = 118.9 * FRAME_RATE)
        rep_indicator.morph_figure(2, start_time = 118)
        for i in range(18, 20):
            char = rep_indicator.lookup_table[2][i]
            char.color_shift(
                color = COLORS_SCALED[5],
                start_time = 118,
                duration_time = None
            )
        surv_indicator.morph_figure(1, start_time = 118.2)
        for i in range(15, 19):
            char = surv_indicator.lookup_table[1][i]
            char.color_shift(
                color = COLORS_SCALED[6],
                start_time = 118.2,
                duration_time = None
            )

        rep_indicator.morph_figure(3, start_time = 119.5)
        for i in range(18, 21):
            char = rep_indicator.lookup_table[3][i]
            char.color_shift(
                color = COLORS_SCALED[4],
                start_time = 119.5,
                duration_time = None
            )

        blob.move_to(
            new_angle = [0, 0, 0],
            start_time = 124.5
        )
        actual_blob = l_blob.ref_obj.children[0]
        actual_blob.keyframe_insert(data_path="rotation_euler", frame = 124.5 * FRAME_RATE)
        actual_blob.rotation_euler = [
            0,
            actual_blob.rotation_euler[1] - math.pi / 2,
            0
        ]
        actual_blob.keyframe_insert(data_path="rotation_euler", frame = 125 * FRAME_RATE)
        make_animations_linear(actual_blob, data_paths = ['rotation_euler'])
        surv_indicator.move_to(
            new_angle = [0, surv_indicator.ref_obj.rotation_euler[1] + math.pi / 2, 0],
            start_time = 124.5
        )

        positive = tex_bobject.TexBobject(
            #'150 \\%',
            '\\substack{\\text{Net} \\\\ \\text{Positive!}}',
            scale = 2.4,
            location = [0, -0.5, 0],
            centered = True
        )
        positive.add_to_blender(appear_time = 132.5)

        for b in [blob, l_blob]:
            b.blob_wave(
                start_time = 132.5,
                duration = 10
            )
            b.show_mouth(start_time = 132.5)

        to_disappear = [blob, rep_indicator, l_blob, surv_indicator, positive]
        for i, thing in enumerate(to_disappear):
            thing.disappear(disappear_time = 137.5 - (len(to_disappear) - 1 - i) * 0.05)

    def net_positive_sim(self):
        tex = tex_bobject.TexBobject(
            '\\text{Net positive altruism}',
            #'\\begin{array}{@{}c@{}}\\text{Net positive} \\\\ \\text{altruism} \\end{array}',
            scale = 1.5,
            #location = [-6.5, 0, 8],
            #rotation_euler = [74 * math.pi / 180, 0, 0],
            color = 'color2',
            centered = True
        )
        mut = tex_bobject.TexBobject(
            '\\text{Mutation chance: } 5\\%',
            scale = 1,
            #location = [-6.5, 0, 8],
            #rotation_euler = [74 * math.pi / 180, 0, 0],
            color = 'color2',
            centered = True
        )
        cost = tex_bobject.TexBobject(
            '\\text{Altruism cost: } 50\\%',
            scale = 1,
            location = [0, 0.2, 0],
            #rotation_euler = [74 * math.pi / 180, 0, 0],
            color = 'color2',
            centered = True
        )

        comp = tex_complex.TexComplex(
            tex, mut, cost,
            location = [-6.5, 0, 8],
            rotation_euler = [74 * math.pi / 180, 0, 0],
            centered = True,
            multiline = True,
            line_height = 1.4
        )


        states_to_draw = []

        self.simulation_scene(
            animate_graph = True,
            animate_sim = True,
            sim_name = 'net_positive_20',
            scene_open_time = 138,
            simulation_start_time = 144,
            sim_speed_up_factor = 5,
            sim_start_date = 0,
            sim_end_date = None,
            label_complex = comp,
            graph_label_strings = ['\\text{Altruistic}', '\\text{Not}'],
            graph_type = 'altruist',
            num_bars = 2,
            states_to_draw = states_to_draw,
            outro_length = 3,
            outro_sway = False
        )

    def need_targeting(self):
        cam_bobj, cam_swivel = cam_and_swivel(
            cam_location = [0, -1.5, 7], #32.8
            cam_rotation_euler = [0, 0, 0],
            cam_name = "Camera Bobject",
            swivel_location = [0, 0, 0],
            swivel_rotation_euler = [0, 0, 0],
            swivel_name = 'Cam swivel',
            #control_sun = True
        )

        cam_swivel.add_to_blender(appear_time = -1)

        #def dna():
        dna1_1 = import_object(
            'dna_strand_1', 'biochem',
            scale = 1.5,
            location = [-0.25, -1.5, 0]
        )
        dna1_1.add_to_blender(
            appear_time = 150
        )

        dna2_1 = import_object(
            'dna_strand_2', 'biochem',
            scale = 1.5,
            location = [-0.25, -1.5, 0]
        )
        dna2_1.add_to_blender(
            appear_time = 150
        )

        '''cam_bobj.move_to(
            new_location = [0, -0.8, 10.7],
            start_time = 133,
            end_time = 133
        )'''

        ###
        #Blob 1 Stuff
        ###
        blob1 = blobject.Blobject(
            location = [0, 0, 0],
            scale = 6,
            wiggle = True
        )
        meta = blob1.ref_obj.children[0].children[0]
        apply_material(meta, 'creature_color3')
        blob1.add_to_blender(appear_time = 0, animate = False)

        #All these nodes are a bit overkill since I'm not fading from the
        #solid surface material
        mat_copy = meta.material_slots[0].material.copy()
        meta.active_material = mat_copy
        node_tree = mat_copy.node_tree
        out = node_tree.nodes['Material Output']
        princ = node_tree.nodes['Principled BSDF']
        trans = node_tree.nodes.new(type = 'ShaderNodeBsdfTransparent')
        mix = node_tree.nodes.new(type = 'ShaderNodeMixShader')

        scat = node_tree.nodes.new(type = 'ShaderNodeVolumeScatter')
        absorb = node_tree.nodes.new(type = 'ShaderNodeVolumeAbsorption')
        emit = node_tree.nodes.new(type = 'ShaderNodeEmission')
        add1 = node_tree.nodes.new(type = 'ShaderNodeAddShader')
        add2 = node_tree.nodes.new(type = 'ShaderNodeAddShader')

        node_tree.links.new(mix.outputs[0], out.inputs[0])
        node_tree.links.new(princ.outputs[0], mix.inputs[1])
        node_tree.links.new(trans.outputs[0], mix.inputs[2])

        node_tree.links.new(add1.outputs[0], out.inputs[1])
        node_tree.links.new(emit.outputs[0], add1.inputs[0])
        node_tree.links.new(add2.outputs[0], add1.inputs[1])
        node_tree.links.new(scat.outputs[0], add2.inputs[0])
        node_tree.links.new(absorb.outputs[0], add2.inputs[1])

        #Make another copy before adding keyframes
        mat_copy2 = mat_copy.copy()
        mat_copy3 = mat_copy.copy()

        mix.inputs[0].default_value = 1
        for node in [scat, absorb, emit]:
            node.inputs[0].default_value = princ.inputs[0].default_value
            node.inputs[1].default_value = 0
            node.inputs[1].keyframe_insert(data_path = 'default_value', frame = 153.5 * FRAME_RATE)
            node.inputs[1].default_value = BLOB_VOLUME_DENSITY
            node.inputs[1].keyframe_insert(data_path = 'default_value', frame = 154 * FRAME_RATE)

        mix.inputs[0].keyframe_insert(data_path = 'default_value', frame = 156.5 * FRAME_RATE)
        mix.inputs[0].default_value = 0
        mix.inputs[0].keyframe_insert(data_path = 'default_value', frame = 157 * FRAME_RATE)

        cam_bobj.move_to(
            new_location = [0, 0, 32.8],
            start_time = 153.5,
            end_time = 154.5
        )


        ###
        #Blob 2 Stuff
        ###
        blob2 = blobject.Blobject(
            location = [0, 0, 0],
            scale = 6,
            wiggle = True
        )
        meta2 = blob2.ref_obj.children[0].children[0]
        blob2.add_to_blender(appear_time = 0)


        meta2.active_material = mat_copy2
        node_tree = mat_copy2.node_tree
        mix2 = node_tree.nodes['Mix Shader']

        scat2 = node_tree.nodes['Volume Scatter']
        absorb2 = node_tree.nodes['Volume Absorption']
        emit2 = node_tree.nodes['Emission']

        mix2.inputs[0].default_value = 1
        for node in [scat2, absorb2, emit2]:
            node.inputs[0].default_value = princ.inputs[0].default_value
            node.inputs[1].default_value = 0
            node.inputs[1].keyframe_insert(data_path = 'default_value', frame = 155.5 * FRAME_RATE)
            node.inputs[1].default_value = BLOB_VOLUME_DENSITY
            node.inputs[1].keyframe_insert(data_path = 'default_value', frame = 156 * FRAME_RATE)

        mix2.inputs[0].keyframe_insert(data_path = 'default_value', frame = 156.5 * FRAME_RATE)
        mix2.inputs[0].default_value = 0
        mix2.inputs[0].keyframe_insert(data_path = 'default_value', frame = 157 * FRAME_RATE)

        ###
        #Eye stuff
        ###
        eyel_1 = blob1.ref_obj.children[0].children[-2]
        eye_mat_copy_1 = eyel_1.material_slots[0].material.copy()
        eyel_1.active_material = eye_mat_copy_1
        eyer_1 = blob1.ref_obj.children[0].children[-3]
        eyer_1.active_material = eye_mat_copy_1

        node_tree = eye_mat_copy_1.node_tree
        trans = node_tree.nodes.new(type = 'ShaderNodeBsdfTransparent')
        e_mix_1 = node_tree.nodes.new(type = 'ShaderNodeMixShader')
        out = node_tree.nodes['Material Output']
        diff = node_tree.nodes['Diffuse BSDF']

        node_tree.links.new(e_mix_1.outputs[0], out.inputs[0])
        node_tree.links.new(trans.outputs[0], e_mix_1.inputs[1])
        node_tree.links.new(diff.outputs[0], e_mix_1.inputs[2])

        e_mix_1.inputs[0].default_value = 0
        e_mix_1.inputs[0].keyframe_insert(data_path = 'default_value', frame = 153.5 * FRAME_RATE)
        e_mix_1.inputs[0].default_value = 1
        e_mix_1.inputs[0].keyframe_insert(data_path = 'default_value', frame = 154 * FRAME_RATE)

        eyel_2 = blob2.ref_obj.children[0].children[-2]
        eye_mat_copy_2 = eyel_2.material_slots[0].material.copy()
        eyel_2.active_material = eye_mat_copy_2
        eyer_2 = blob2.ref_obj.children[0].children[-3]
        eyer_2.active_material = eye_mat_copy_2

        node_tree = eye_mat_copy_2.node_tree
        trans = node_tree.nodes.new(type = 'ShaderNodeBsdfTransparent')
        e_mix_2 = node_tree.nodes.new(type = 'ShaderNodeMixShader')
        out = node_tree.nodes['Material Output']
        diff = node_tree.nodes['Diffuse BSDF']

        node_tree.links.new(e_mix_2.outputs[0], out.inputs[0])
        node_tree.links.new(trans.outputs[0], e_mix_2.inputs[1])
        node_tree.links.new(diff.outputs[0], e_mix_2.inputs[2])

        e_mix_2.inputs[0].default_value = 0
        e_mix_2.inputs[0].keyframe_insert(data_path = 'default_value', frame = 155.5 * FRAME_RATE)
        e_mix_2.inputs[0].default_value = 1
        e_mix_2.inputs[0].keyframe_insert(data_path = 'default_value', frame = 156 * FRAME_RATE)

        ###
        #Blob 3 Stuff
        ###
        blob3 = blobject.Blobject(
            location = [18, 0, 0],
            scale = 6,
            wiggle = True
        )
        meta3 = blob3.ref_obj.children[0].children[0]
        blob3.add_to_blender(appear_time = 157)


        meta3.active_material = mat_copy3
        node_tree = mat_copy3.node_tree
        mix3 = node_tree.nodes['Mix Shader']

        scat3 = node_tree.nodes['Volume Scatter']
        absorb3 = node_tree.nodes['Volume Absorption']
        emit3 = node_tree.nodes['Emission']

        mix3.inputs[0].default_value = 0
        for node in [scat3, absorb3, emit3]:
            node.inputs[0].default_value = princ.inputs[0].default_value
            node.inputs[1].default_value = 0
            node.inputs[1].default_value = BLOB_VOLUME_DENSITY
            #node.inputs[1].keyframe_insert(data_path = 'default_value', frame = 95.5 * FRAME_RATE)
            #node.inputs[1].keyframe_insert(data_path = 'default_value', frame = 96 * FRAME_RATE)

        cam_bobj.move_to(
            new_location = [6, 0, 45],
            start_time = 156.5,
            end_time = 157.5
        )

        #Moar gifts
        moar_start = 157
        num_gifts = 2
        time_per_gift = 1.5
        for i in range(num_gifts):
            if i == 0:
                j = -1
            else:
                j = 1
            blob2.move_to(
                new_angle = [0, j * math.pi / 2, 0],
                start_time = moar_start - 0.3 + i * time_per_gift
            )
            blob2.hold_object(
                start_time = moar_start + i * time_per_gift,
                end_time = moar_start + 1 + i * time_per_gift
            )
            gift = import_object(
                'gift_white', 'misc',
                location = [0, 0, 0],
                rotation_euler = [-math.pi / 2, 0, 0],
                scale = 0.28
            )
            gift.ref_obj.parent = blob2.ref_obj
            gift.add_to_blender(appear_time = moar_start + i * time_per_gift)
            gift.move_to(
                new_location = [0, 0, 0.8],
                start_time = moar_start + i * time_per_gift
            )
            gift.move_to(
                new_location = [j * 0.1, 0, 2],
                start_time = moar_start + i * time_per_gift + 0.5
            )
            gift.disappear(disappear_time = moar_start + i * time_per_gift + 1, duration_frames = OBJECT_APPEARANCE_TIME / 2)

        blob2.move_to(
            new_angle = [0, 0, 0],
            start_time = moar_start + num_gifts * time_per_gift
        )


        #Retransparentify
        for mix_shader in [mix, mix2, mix3]:
            mix_shader.inputs[0].keyframe_insert(data_path = 'default_value', frame = 161 * FRAME_RATE)
            mix_shader.inputs[0].default_value = 1
            mix_shader.inputs[0].keyframe_insert(data_path = 'default_value', frame = 161.5 * FRAME_RATE)

        blob3.evil_pose(
            start_time = 164,
            end_time = 176.5
        )

        dna2_1.move_to(new_location = [1.25, -1.5, 0], start_time = 154.5)
        dna1_1.move_to(new_location = [-1.75, -1.5, 0], start_time = 154.5)

        dna1_2 = import_object(
            'dna_strand_1', 'biochem',
            scale = 1.5,
            location = [1.25, -1.5, 0],
        )
        dna1_2.add_to_blender(appear_time = 0)
        dna2_2 = import_object(
            'dna_strand_2', 'biochem',
            scale = 1.5,
            location = [-1.75, -1.5, 0],
        )
        dna2_2.add_to_blender(appear_time = 0)
        dna1_2.de_explode(
            start_time = 155,
            duration = 0.5,
        )
        dna2_2.de_explode(
            start_time = 155,
            duration = 0.5,
        )

        dna_3 = import_object(
            'dna_two_strand', 'biochem',
            scale = 1.5,
            location = [18, -1.5, 0]
        )
        dna_3.add_to_blender(appear_time = 158)

        def make_red_recursive(obj):
            apply_material(obj, 'color6')
            for child in obj.children:
                make_red_recursive(child)

        make_red_recursive(dna_3.ref_obj.children[0])

        blob2.move_to(new_location = [6, 0, 0], start_time = 155.5)
        blob1.move_to(new_location = [-6, 0, 0], start_time = 155.5)

        dna1_1.move_to(new_location = [-6, -1.5, 0], start_time = 155.5)
        dna2_1.move_to(new_location = [6, -1.5, 0], start_time = 155.5)
        dna1_2.move_to(new_location = [6, -1.5, 0], start_time = 155.5)
        dna2_2.move_to(new_location = [-6, -1.5, 0], start_time = 155.5)

        #for d in [dna1_1, dna2_1, dna1_2, dna2_2, dna_3]:
        #    d.spin(start_time = 0, spin_rate = 0.05)


        to_disappear = [dna1_1, dna2_1, dna1_2, dna2_2, blob1, blob2, blob3, dna_3]
        for thing in to_disappear:
            thing.disappear(disappear_time = 177)

        for strand in [dna1_1, dna2_1, dna1_2, dna2_2, dna_3]:
            print(strand)
            strand.tweak_colors_recursive()
            strand.move_to(
                displacement = [0, 1.5, 0],
                start_time = 176.5
            )
            strand.spin(
                start_time = 150,
                end_time = 180,
                spin_rate = 0.05
            )

    def how_to_coordinate(self):
        htc = tex_bobject.TexBobject(
            '\\text{How to coordinate your copies}',
            location = [0, 6, 0],
            scale = 2,
            centered = True
        )
        #htc.add_to_blender(appear_time = 0)

        edge = 10
        dna1 = import_object(
            'dna_two_strand', 'biochem',
            scale = 3,
            location = [-edge, -4, 0]
        )
        dna2 = import_object(
            'dna_two_strand', 'biochem',
            scale = 3,
            location = [-edge/3, -4, 0]
        )
        dna3 = import_object(
            'dna_two_strand', 'biochem',
            scale = 3,
            location = [edge/3, -4, 0]
        )
        dna4 = import_object(
            'dna_two_strand', 'biochem',
            scale = 3,
            location = [edge, -4, 0]
        )

        flurry = [htc, dna1, dna2, dna3, dna4]
        flurry_start_time = 177.5
        last_start = 180
        f_spacing = (last_start - flurry_start_time) / (len(flurry) - 1)
        for i, thing in enumerate(flurry):
            time = flurry_start_time + i * f_spacing
            thing.de_explode(
                start_time = flurry_start_time + i * f_spacing,
                duration = 1,
            )
            thing.add_to_blender(appear_time = time - 5)


        odt = tex_bobject.TexBobject(
            '\\text{1. Produce an outwardly detectable trait}',
            location = [-10, 3.75, 0],
            scale = 1.2
        )
        odt.add_to_blender(appear_time = 184.5)
        att = tex_bobject.TexBobject(
            '\\begin{array}{ll}\\text{2. Produce altruism toward creatures} \\\\ \\phantom{2...}\\text{with the trait from \#1} \\end{array}',
            location = [-10, 1.5, 0],
            scale = 1.2
        )
        att.add_to_blender(appear_time = 190)

        for d in [dna1, dna2, dna3, dna4]:
            d.tweak_colors_recursive()
            d.spin(start_time = 0, spin_rate = 0.05)

        to_disappear = [dna4, dna3, dna2, dna1, att, odt, htc]
        end = 195.75
        for i, thing in enumerate(to_disappear):
            thing.disappear(disappear_time = end - (len(to_disappear) - 1 - i) * 0.05)

    def green_beard(self):
        blob = Blobject(
            scale = 7,
            location = [0, 0, 0],
            #wiggle = True,
            mouth = True
        )

        nb_time = 196.5
        b_time = 195
        #a_dur = 2
        blob.add_to_blender(appear_time = nb_time)
        blob.hello(
            start_time = nb_time,
            end_time = nb_time + 1.5
        )

        blob.add_beard(
            start_time = b_time,
            mat = 'color7',
            duration = 6
        )
        blob.disappear(disappear_time = 203)

        '''beard = import_object(
            'beard', 'misc',
            location = [0.86383, -1.79778, 0.29876],
            rotation_euler = [-40.8 * math.pi / 180, 68.3 * math.pi / 180, -5.77 * math.pi / 180],
            scale = [1.377, 1.377, 0.685]
        )
        beard.ref_obj.parent = blob.ref_obj.children[0]
        beard.ref_obj.parent_bone = blob.ref_obj.children[0].pose.bones["brd_bone_neck"].name
        beard.ref_obj.parent_type = 'BONE'
        beard.add_to_blender(appear_time = 0)'''

    def green_beard_sim(self):
        tex = tex_bobject.TexBobject(
            #'\\text{Reduced food}',
            '\\text{Green beard altruism}',
            scale = 1.5,
            #location = [-6.5, 0, 8],
            #rotation_euler = [74 * math.pi / 180, 0, 0],
            color = 'color2',
            centered = True
        )
        mut = tex_bobject.TexBobject(
            '\\text{Mutation chance: } 5\\%',
            scale = 1,
            #location = [-6.5, 0, 8],
            #rotation_euler = [74 * math.pi / 180, 0, 0],
            color = 'color2',
            centered = True
        )
        cost = tex_bobject.TexBobject(
            '\\text{Altruism cost: } 50\\%',
            scale = 1,
            location = [0, 0.2, 0],
            #rotation_euler = [74 * math.pi / 180, 0, 0],
            color = 'color2',
            centered = True
        )
        comp = tex_complex.TexComplex(
            tex, mut, cost,
            location = [-6.5, 0, 8],
            rotation_euler = [74 * math.pi / 180, 0, 0],
            centered = True,
            multiline = True,
            line_height = 1.4
        )


        states_to_draw = [
            [205.5, [50,0]],
            [211, [50, 50]],
            [218, [90, 10]],
            [221, [10, 90]],
            [222.5, [50 , 50]],
        ]


        outro_start_time = self.simulation_scene(
            animate_graph = True,
            animate_sim = True,
            sim_name = 'gb_30',
            scene_open_time = 202 ,
            simulation_start_time = 223.5,
            sim_speed_up_factor = 5,
            sim_start_date = 14,
            sim_end_date = 28,
            label_complex = comp,
            graph_label_strings = ['\\text{Green beard}', '\\text{Not}'],
            graph_type = 'green_beard',
            num_bars = 2,
            states_to_draw = states_to_draw,
            outro_length = 33,
            outro_sway = True
        )

        inc_fit = tex_bobject.TexBobject(
            '\\begin{array}{@{}c@{}}\\text{\"Inclusive} \\\\ \\text{fitness\"} \\end{array}',
            scale = 1.6,
            location = [10.055, -1.4, 9.55],
            rotation_euler = [74 * math.pi / 180, 0, 0],
            color = 'color2',
            centered = True
        )
        inc_fit.add_to_blender(appear_time = outro_start_time + 19.5)
        inc_fit.disappear(disappear_time = outro_start_time + 33)

    def separate_genes(self):
        g_pos = [0, -0.5, 0]
        gene1_1 = import_object(
            'dna_strand_1', 'biochem',
            location = g_pos,
            #rotation_euler = [0, 0, 25 * math.pi / 180],
            scale = 5
        )
        gene1_2 = import_object(
            'dna_strand_2', 'biochem',
            location = g_pos,
            #rotation_euler = [0, 0, 25 * math.pi / 180],
            scale = 5
        )

        #for gene in [gene1_1, gene1_2]:
        gene1_1.add_to_blender(appear_time = 0)
        gene1_1.de_explode(start_time = 277.5, duration = 1)
        gene1_2.add_to_blender(appear_time = 0)
        gene1_2.de_explode(start_time = 278.5, duration = 1)


        scale = 2
        tail1 = [-2.5, 1.5]
        head1 = [3.5, 3]
        trait_pos = [4.5, 3.25, 0]
        tail2 = [-3.5, 3.25]
        head2 = [3.5, 3.25]
        arrow1 = gesture.Gesture(
            gesture_series = [
                {
                    'type': 'arrow',
                    'points': {
                        'tail': (tail1[0] / scale, tail1[1] / scale, 0),
                        'head': (head1[0] / scale, head1[1] / scale, 0)
                    }
                },
                {
                    'type': 'arrow',
                    'points': {
                        'tail': (tail2[0] / scale, tail2[1] / scale, 0),
                        'head': (head2[0] / scale, head2[1] / scale, 0)
                    }
                }
            ],
            scale = scale,
        )
        trait1 = tex_bobject.TexBobject(
            '\\text{Trait}',
            location = trait_pos,
            scale = 3,
        )
        arrow2 = gesture.Gesture(
            gesture_series = [
                {
                    'type': 'arrow',
                    'points': {
                        'tail': (tail1[0] / scale, -tail1[1] / scale, 0),
                        'head': (head1[0] / scale, -head1[1] / scale, 0)
                    }
                },
                {
                    'type': 'arrow',
                    'points': {
                        'tail': (tail2[0] / scale, -tail2[1] / scale, 0),
                        'head': (head2[0] / scale, -head2[1] / scale, 0)
                    }
                }
            ],
            scale = scale,
        )
        trait2 = tex_bobject.TexBobject(
            '\\text{Trait}',
            location = [
                trait_pos[0],
                -trait_pos[1],
                trait_pos[2],
            ],
            scale = 3,
        )

        two_trait_time = 280
        for gene in [gene1_1, gene1_2]:
            gene.move_to(
                start_time = two_trait_time - 0.5,
                new_location = [-7.5, -0.5, 0]
            )
        arrow1.add_to_blender(appear_time = two_trait_time)
        trait1.add_to_blender(appear_time = two_trait_time)
        arrow2.add_to_blender(appear_time = two_trait_time)
        trait2.add_to_blender(appear_time = two_trait_time)


        two_gene_time = 286.5
        arrow1.morph_figure(1, two_gene_time)
        arrow2.morph_figure(1, two_gene_time)
        for gene in [gene1_1, gene1_2]:
            gene.move_to(
                new_location = [
                    gene.ref_obj.location[0],
                    3.25,
                    gene.ref_obj.location[2],
                ],
                start_time = two_gene_time,
                new_scale = 2.9
            )

        gene2 = import_object(
            'dna_two_strand_low_res', 'biochem',
            location = [
                gene1_1.ref_obj.location[0],
                -gene1_1.ref_obj.location[1],
                gene1_1.ref_obj.location[2],
            ],
            #rotation_euler = [0, 0, 25 * math.pi / 180],
            scale = 2.9
        )
        gene2.add_to_blender(appear_time = two_gene_time)


        for d in [gene1_1, gene1_2, gene2]:
            d.tweak_colors_recursive()
            d.spin(start_time = 0, spin_rate = 0.05)

        '''to_disappear = [gene1_1, gene1_2, gene2, arrow1, arrow2, trait1, trait2]
        end = 289.5
        for i, thing in enumerate(to_disappear):
            thing.disappear(disappear_time = end)'''

    def separate_genes_sim(self):
        tex = tex_bobject.TexBobject(
            '\\begin{array}{@{}c@{}}\\text{Separated green} \\\\ \\text{beard traits} \\end{array}',
            scale = 1.5,
            location = [-6.5, 0, 8],
            rotation_euler = [74 * math.pi / 180, 0, 0],
            color = 'color2',
            centered = True
        )
        tex.add_to_blender(appear_time = 290.5)
        mut = tex_bobject.TexBobject(
            '\\text{Mutation chance: } 5\\%',
            scale = 1,
            #location = [-6.5, 0, 8],
            #rotation_euler = [74 * math.pi / 180, 0, 0],
            color = 'color2',
            centered = True
        )
        cost = tex_bobject.TexBobject(
            '\\text{Altruism cost: } 50\\%',
            scale = 1,
            location = [0, 0.2, 0],
            #rotation_euler = [74 * math.pi / 180, 0, 0],
            color = 'color2',
            centered = True
        )
        comp = tex_complex.TexComplex(
            mut, cost,
            location = [-6.5, 0, 5.75],
            rotation_euler = [74 * math.pi / 180, 0, 0],
            centered = True,
            multiline = True,
            line_height = 1.2
        )

        states_to_draw = [
            [300, [25, 0, 0, 0]],
            [300.75, [25, 0, 0, 25,]],
            [301.5, [25, 25, 0, 25,]],
            [302.75, [25, 25, 25, 25,]],
        ]

        scale = 2
        arrow1 = gesture.Gesture(
            gesture_series = [
                {
                    'type': 'arrow',
                    'points': {
                        'tail': (5.8 / scale, 7 / scale, 3.9 / scale),
                        'head': (5.8 / scale, 3.5 / scale, 3.9 / scale)
                    }
                },
            ],
            scale = scale,
            rotation_euler = [74 * math.pi / 180, 0, 0],
        )

        arrow2 = gesture.Gesture(
            gesture_series = [
                {
                    'type': 'arrow',
                    'points': {
                        'tail': (10.55 / scale, 7.6 / scale, 3.9 / scale),
                        'head': (10.55 / scale, 4.1 / scale, 3.9 / scale)
                    }
                },
            ],
            scale = scale,
            rotation_euler = [74 * math.pi / 180, 0, 0],
        )

        outro_start_time = self.simulation_scene(
            animate_graph = True,
            animate_sim = True,
            sim_name = 'separate_traits',
            scene_open_time = 290.5,
            simulation_start_time = 307.5,
            sim_speed_up_factor = 5,
            sim_start_date = 0,
            sim_end_date = None,
            label_complex = comp,
            graph_label_strings = [
                '\\begin{array}{@{}c@{}}\\text{Green} \\\\ \\text{beard} \\\\ \\text{altruism} \\end{array}',
                '\\begin{array}{@{}c@{}}\\text{Just} \\\\ \\text{green} \\\\ \\text{beard} \\end{array}',
                '\\begin{array}{@{}c@{}}\\text{Just} \\\\ \\text{altruism} \\end{array}',
                '\\text{Neither}',
            ],
            graph_type = 'sep_green_beard',
            vals_to_count = [
                [True, True],
                [True, False],
                [False, True],
                [False, False],
            ],
            num_bars = 4,
            bar_width = 0.5,
            states_to_draw = states_to_draw,
            outro_length = 11,
            outro_sway = True
        )

        arrow1.add_to_blender(appear_time = outro_start_time + 6.5)
        arrow2.add_to_blender(appear_time = outro_start_time + 6.5)
        arrow2.disappear(disappear_time = outro_start_time + 9.5)

    def kin_selection_intro(self):
        blob = blobject.Blobject(
            location = [0, -1, 0],
            scale = 6
        )
        blob.add_to_blender(appear_time = 323)
        blob.add_beard(mat = 'color7')

        #Idle movements
        blob.move_head(
            start_time = 327.5,
            rotation_quaternion = [1, -0.1, -0.1, 0]
        )
        blob.move_head(
            start_time = 329,
            attack = 1,
            rotation_quaternion = [1, 0.1, 0.1, 0]
        )

        #Shake head
        blob.move_head(
            start_time = 331.5,
            attack = 0.3,
            rotation_quaternion = [1, 0, 0, 0]
        )
        blob.move_head(
            start_time = 332,
            attack = 0.125,
            rotation_quaternion = [1, 0, -0.1, 0]
        )
        blob.move_head(
            start_time = 332.125,
            attack = 0.125,
            rotation_quaternion = [1, 0, 0.1, 0]
        )
        blob.move_head(
            start_time = 332.25,
            attack = 0.125,
            rotation_quaternion = [1, 0, -0.1, 0]
        )
        blob.move_head(
            start_time = 332.375,
            attack = 0.125,
            rotation_quaternion = [1, 0, 0, 0]
        )

        ks = tex_bobject.TexBobject(
            '\\text{Kin altruism}',
            '\\text{Kin selection}',
            location = [0, 5, 0],
            scale = 4.5,
            centered = True
        )
        ks.add_to_blender(appear_time = 334.25)
        blob.move_to(
            new_location = [0, -3, 0],
            new_scale = 4,
            start_time = 334.25
        )
        ks.morph_figure(1, start_time = 336.25)

        blob.beard.disappear(
            disappear_time = 341,
            duration_frames = 2 * OBJECT_APPEARANCE_TIME
        )

        blob.move_to(
            new_location = [-5, -3, 0],
            start_time = 342.5
        )

        w_blob = blobject.Blobject(
            location = [5, -3, 0],
            scale = 4,
        )
        w_blob.add_to_blender(appear_time = 343)
        w_blob.dance(
            start_time = 344,
            end_time = 360,
        )

        blob.move_head(
            start_time = 344,
            rotation_quaternion = [1, 0, 0.4, 0]
        )
        blob.move_to(
            new_angle = [0, math.pi / 4, 0],
            start_time = 344
        )
        '''blob.move_head(
            start_time = 347,
            rotation_quaternion = [1, 0.1, -0.25, -0.2]
        )
        blob.move_head(
            start_time = 348,
            rotation_quaternion = [1, 0, 0.4, 0]
        )'''
        '''blob.move_head(
            start_time = 9,
            rotation_quaternion = [1, 0.1, -0.25, -0.2]
        )'''
        blob.wince(
            start_time = 346,
            end_time = 349
        )



        sg = import_object(
            'sunglasses', 'misc',
            location = [1.17, -1.03, 0.44],
            rotation_euler = [0, 68.4 * math.pi / 180, 0],
            scale = 1,
        )
        sg.ref_obj.parent = w_blob.ref_obj.children[0]
        sg.ref_obj.parent_bone = w_blob.ref_obj.children[0].pose.bones["brd_bone_neck"].name
        sg.ref_obj.parent_type = 'BONE'
        sg.add_to_blender(
            appear_time = 0
        )
        '''sg.move_to(
            start_time = cues['green']['start'] + 59,
            displacement = [0, -3, 0]
        )'''

    def hamilton(self):
        tex = tex_bobject.TexBobject(
            '\\text{Kin altruism}',
            scale = 2,
            #location = [-6.5, 0, 8],
            #rotation_euler = [74 * math.pi / 180, 0, 0],
            color = 'color2',
            centered = True
        )
        #tex.add_to_blender(appear_time = 5)
        mut = tex_bobject.TexBobject(
            '\\text{Mutation chance: } 5\\%',
            scale = 1,
            #location = [-6.5, 0, 8],
            #rotation_euler = [74 * math.pi / 180, 0, 0],
            color = 'color2',
            centered = True
        )
        cost = tex_bobject.TexBobject(
            '\\text{Altruism cost: } 50\\%',
            scale = 1,
            #rotation_euler = [74 * math.pi / 180, 0, 0],
            color = 'color2',
            centered = True
        )
        comp = tex_complex.TexComplex(
            tex, mut, cost,
            location = [-6.5, 0, 8],
            #location = [-6.5, 0, 5.75],
            rotation_euler = [74 * math.pi / 180, 0, 0],
            centered = True,
            multiline = True,
            line_height = 1.4
        )

        states_to_draw = [
            [349.5, [50, 0]],
            [350, [50, 50]],
        ]
        first_day_start = 364
        sim_appearance_time = 339

        '''outro_start_time, cam_bobj = self.simulation_scene(
            animate_graph = False,
            animate_sim = True,
            sim_name = '100f_100d_low_2',
            scene_open_time = 339,
            simulation_start_time = 364,
            sim_speed_up_factor = 5,
            sim_start_date = 39,
            sim_end_date = 59,
            label_complex = comp,
            graph_label_strings = ['\\text{Kin altruist}', '\\text{Not}'],
            graph_type = 'kin_altruist',
            num_bars = 2,
            states_to_draw = states_to_draw,
            outro_length = 22,
            outro_sway = False
        )'''

        '''g.move_to(
            new_location = [18, -4, 0],
            start_time = 360
        )'''

        show_rule = True
        if show_rule == True:
            rule = tex_bobject.TexBobject(
                'C<rP',
                'C<rP',
                'C<rP',
                'C<rP',
                'C<0.95 \\cdot P',
                '0.5 < 0.95 \\cdot P',
                '0.5 < 0.95 \\cdot 1',
                #location = [6.5, -1, 4.5],
                #rotation_euler = [74 * math.pi / 180, 0, 0],
                centered = True,
                #scale = 3
            )
            rules_complex = tex_complex.TexComplex(
                rule,
                location = [6.5, -1.25, 3.5],
                rotation_euler = [74 * math.pi / 180, 0, 0],
                centered = True,
                scale = 3
            )

            annotations = True
            if annotations == True:
                rules_complex.add_annotation(
                    targets = [
                        0, #tex_bobject
                        [
                            [0, 0, 0, None],  #form, first char, last char
                            [1, 0, 0],
                            [2, 0, 0],
                            [3, 0, 0],
                            [4, 0, 0],
                            [5, 0, 2, 'arrow'],
                            [6, 0, 2, 'arrow'],
                        ],
                    ],
                    labels = [
                        [],
                        ['\\text{Cost to}', '\\text{participate}'],
                        ['\\text{Cost to}', '\\text{participate}'],
                        ['\\text{Cost to}', '\\text{participate}'],
                        ['\\text{Cost to}', '\\text{participate}'],
                        ['\\text{Cost to}', '\\text{participate}'],
                        ['\\text{Cost to}', '\\text{participate}'],
                    ],
                    alignment = 'top',
                    gest_scale = 0.6
                )
                rules_complex.add_annotation(
                    targets = [
                        0, #tex_bobject
                        [
                            [0, 3, 3, None],  #form, first char, last char
                            [1, 3, 3, None],
                            [2, 3, 3],
                            [3, 3, 3],
                            [4, 7, 7],
                            [5, 9, 9],
                            [6, 9, 9],
                        ],
                    ],
                    labels = [
                        [],
                        [],
                        ['\\text{Payoff for}', '\\text{winning}'],
                        ['\\text{Payoff for}', '\\text{winning}'],
                        ['\\text{Payoff for}', '\\text{winning}'],
                        ['\\text{Payoff for}', '\\text{winning}'],
                        ['\\text{Payoff for}', '\\text{winning}'],
                    ],
                    alignment = 'top',
                    gest_scale = 0.6
                )
                rules_complex.add_annotation(
                    targets = [
                        0, #tex_bobject
                        [
                            [0, 2, 2, None],  #form, first char, last char
                            [1, 2, 2, None],
                            [2, 2, 2, None],
                            [3, 2, 2],
                            [4, 2, 5, 'arrow'],
                            [5, 4, 7, 'arrow'],
                            [6, 4, 7, 'arrow'],
                        ],
                    ],
                    labels = [
                        [],
                        [],
                        [],
                        ['\\text{Win rate}'],
                        ['\\text{Win rate}'],
                        ['\\text{Win rate}'],
                        ['\\text{Win rate}'],
                    ],
                    alignment = 'bottom',
                    gest_scale = 0.6
                )

            rules_complex.add_to_blender(appear_time = 373)
            rule.morph_figure(1, start_time = 375.5)
            rule.morph_figure(2, start_time = 377.5)
            rule.morph_figure(3, start_time = 379)

            rules_complex.move_to(
                start_time = 386.5,
                new_scale = 2,
                new_location = [6.5, -1.7, 1.9]
            )

            hr = tex_bobject.TexBobject(
                '\\text{\"Hamilton\'s Rule\"}',
                location = [6.5, 0.5, 9.56],
                rotation_euler = [74 * math.pi / 180, 0, 0],
                scale = 2,
                centered = True
            )
            hr.add_to_blender(appear_time = 386.5)

            #Mutation chance is 1 - win chance
            mut_focus_start = 391
            mut_focus_end = 399
            mut.pulse(
                start_time = mut_focus_start,
                duration_time = mut_focus_end - mut_focus_start
            )
            for i in range(15, 17):
                char = mut.lookup_table[0][i]
                char.color_shift(
                    color = COLORS_SCALED[3],
                    start_time = mut_focus_start,
                    duration_time = mut_focus_end - mut_focus_start
                )
            rule.morph_figure(4, start_time = 397.5)

            cost_focus_start = 401
            cost_focus_end = 404.5
            cost.pulse(
                start_time = cost_focus_start,
                duration_time = cost_focus_end - cost_focus_start
            )
            for i in range(13, 16):
                char = cost.lookup_table[0][i]
                char.color_shift(
                    color = COLORS_SCALED[3],
                    start_time = cost_focus_start,
                    duration_time = cost_focus_end - cost_focus_start
                )
            rule.morph_figure(5, start_time = 402.25)
            rule.morph_figure(6, start_time = 406.75)

            #Pulse payout
            for i in range(4, 10):
                char = rule.lookup_table[6][i]
                char.color_shift(
                    color = COLORS_SCALED[3],
                    start_time = 417.5,
                    duration_time = 1
                )

            #Cost pulse
            for i in range(0, 3):
                char = rule.lookup_table[6][i]
                char.color_shift(
                    color = COLORS_SCALED[3],
                    start_time = 419,
                    duration_time = 1
                )

            rules_complex.disappear(disappear_time = 425)
            hr.disappear(disappear_time = 425)

        '''g.move_to(
            new_location = [2, -4, 0],
            start_time = 425
        )'''

        orig = list(cam_bobj.ref_obj.location)
        cam_bobj.move_to(
            new_location = [4.86, -4.5, 9.2],
            start_time = outro_start_time + 1,
            end_time = outro_start_time + 6
        )

        cam_bobj.move_to(
            new_location = orig,
            start_time = outro_start_time + 9
        )

    def lies(self):
        h = tex_bobject.TexBobject(
            '\\text{HAMILTON\'S RULE IS A}',
            centered = True,
            scale = 2.5
        )
        l = tex_bobject.TexBobject(
            '\\text{LIE}',
            centered = True,
            scale = 12
        )

        to_add = [h, l]
        for thing in to_add:
            thing.add_to_blender(appear_time = 0)

        '''h = tex_bobject.TexBobject(
            '\\text{HAMILTON\'S}',
            centered = True,
            scale = 4
        )
        ria = tex_bobject.TexBobject(
            '\\text{RULE IS A}',
            centered = True,
            scale = 2.5
        )
        l = tex_bobject.TexBobject(
            '\\text{LIE}',
            centered = True,
            scale = 12
        )

        to_add = [h, ria, l]
        for thing in to_add:
            thing.add_to_blender(appear_time = 0)'''

    def kin_selection_sim(self):
        tex = tex_bobject.TexBobject(
            '\\text{Kin altruism}',
            scale = 2,
            #location = [-6.5, 0, 8],
            #rotation_euler = [74 * math.pi / 180, 0, 0],
            color = 'color2',
            centered = True
        )
        #tex.add_to_blender(appear_time = 5)
        mut = tex_bobject.TexBobject(
            '\\text{Mutation chance: } 1\\%',
            scale = 1,
            #location = [-6.5, 0, 8],
            #rotation_euler = [74 * math.pi / 180, 0, 0],
            color = 'color2',
            centered = True
        )
        cost = tex_bobject.TexBobject(
            '\\text{Altruism cost: } 10\\%',
            scale = 1,
            #rotation_euler = [74 * math.pi / 180, 0, 0],
            color = 'color2',
            centered = True
        )
        comp = tex_complex.TexComplex(
            tex, mut, cost,
            location = [-6.5, 0, 8],
            #location = [-6.5, 0, 5.75],
            rotation_euler = [74 * math.pi / 180, 0, 0],
            centered = True,
            multiline = True,
            line_height = 1.4
        )

        states_to_draw = []


        outro_start_time = self.simulation_scene(
            animate_graph = True,
            animate_sim = True,
            sim_name = '100f_100d_1',
            scene_open_time = 0 ,
            simulation_start_time = 3,
            sim_speed_up_factor = 5,
            sim_start_date = 39,
            sim_end_date = 59,
            label_complex = comp,
            graph_label_strings = ['\\text{Kin altruist}', '\\text{Not}'],
            graph_type = 'kin_altruist',
            num_bars = 2,
            states_to_draw = states_to_draw,
            outro_length = 2,
            outro_sway = False
        )


        #comp.add_to_blender(appear_time = 0)

        for i in range(15, 17):
            char = mut.lookup_table[0][i]
            char.color_shift(
                color = COLORS_SCALED[6],
                start_time = 0,
                duration_time = None
            )

        for i in range(13, 16):
            char = cost.lookup_table[0][i]
            char.color_shift(
                color = COLORS_SCALED[6],
                start_time = 0,
                duration_time = None
            )

    def kin_distance_sim(self):
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

        food_count = 100
        initial_creatures = []
        #for i in range(math.floor(food_count / 4)):
        for i in range(25):
            initial_creatures.append(
                natural_sim.Creature(
                    size = 1 + randrange(-5, 6) * natural_sim.MUTATION_VARIATION,
                    speed = 1 + randrange(-5, 6) * natural_sim.MUTATION_VARIATION,
                    sense = 1 + randrange(-5, 6) * natural_sim.MUTATION_VARIATION,
                    kin_radius = 0.2
                )
            )
            initial_creatures.append(
                natural_sim.Creature(
                    size = 1 + randrange(-5, 6) * natural_sim.MUTATION_VARIATION,
                    speed = 1 + randrange(-5, 6) * natural_sim.MUTATION_VARIATION,
                    sense = 1 + randrange(-5, 6) * natural_sim.MUTATION_VARIATION,
                    kin_radius = 0.2
                )
            )

        sim = natural_sim.DrawnNaturalSim(
            mutation_switches = {
                 'speed' : True,
                 'size' : True,
                 'sense' : True,
                 'altruist' : False,
                 'green_beard' : False,
                 'kin_radius' : True,
            },
            scale = 1.5,
            food_count = food_count,
            initial_creatures = initial_creatures,
            #sim = 'NAT20190212T124649',
            location = [-6.5, 0, 0],
            day_length_style = 'fixed_length'
        )

        for i in range(10):
            save = False
            if i == 999:
                save = True
            sim.sim.sim_next_day(save = save)


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
        tex.add_to_blender(appear_time = 1)

        #Move camera instead of sim, because moving or displaced sims don't function
        #well.
        dist_avgs = []
        spd_avgs = []
        size_avgs = []
        sense_avgs = []
        for date in sim.sim.date_records:
            num = len(date['creatures'])
            print(num)
            tot = sum([x.kin_radius for x in date['creatures']])
            if num > 0:
                dist_avgs.append(tot/num)
            else:
                dist_avgs.append(0)

            tot = sum([x.speed for x in date['creatures']])
            if num > 0:
                spd_avgs.append(tot/num)
            else:
                spd_avgs.append(0)

            tot = sum([x.size for x in date['creatures']])
            if num > 0:
                size_avgs.append(tot/num)
            else:
                size_avgs.append(0)

            tot = sum([x.sense for x in date['creatures']])
            if num > 0:
                sense_avgs.append(tot/num)
            else:
                sense_avgs.append(0)


        g = graph_bobject.GraphBobject(
            dist_avgs,
            location = [2, -4, 0],
            rotation_euler = [74 * math.pi / 180, 0, 0],
            #rotation_euler = [math.pi / 2, 0, 0],
            width = 10,
            x_range = len(sim.sim.date_records),
            x_label = '\\text{Day}',
            x_label_pos = 'end',
            height = 10,
            y_range = 2,
            y_label = '\\text{Avg distance}',
            y_label_pos = 'end',
            tick_step = [100, 0.5],
            #centered = True,
            include_y = True,
            arrows = True,
            padding = 0
        )
        g.add_to_blender(appear_time = 0)

        g.add_new_function_and_curve(spd_avgs, color = 4)
        g.add_new_function_and_curve(size_avgs, color = 6)
        g.add_new_function_and_curve(sense_avgs, color = 7)


        end = 500
        to_disappear = [sim]
        for i, thing in enumerate(to_disappear):
            thing.disappear(disappear_time = end - (len(to_disappear) - 1 - i) * 0.05)

    def gene_v_creature(self):
        blob = blobject.Blobject(
            location = [-6, 0, 0],
            scale = 5
        )
        blob.add_to_blender(appear_time = 485)

        blob.move_head(
            start_time = 488,
            rotation_quaternion = [1, 0, 0.4, 0]
        )
        blob.move_to(
            new_angle = [0, math.pi / 4, 0],
            start_time = 488
        )
        blob.move_head(
            start_time = 489.5,
            rotation_quaternion = [1, 0.1, 0.2, -0.3]
        )
        blob.move_head(
            start_time = 492,
            rotation_quaternion = [1, 0, 0.4, 0]
        )

        blob.move_to(
            new_angle = [0, 0, 0],
            #new_location = [0, 0, 0],
            start_time = 495
        )
        blob.move_head(
            start_time = 495,
            rotation_quaternion = [1, 0, 0, 0]
        )

        blob.show_mouth(
            start_time = 498
        )
        blob.move_to(
            new_angle = [0, math.pi / 4, 0],
            start_time = 498
        )
        blob.hello(
            start_time = 498.5,
            end_time = 499.5
        )


        blob2 = blobject.Blobject(
            location = [20, 0, 0],
            rotation_euler = [0, - math.pi / 2, 0],
            scale = 5
        )
        blob2.add_to_blender(appear_time = 485)
        blob2.move_to(
            new_location = [4, 0, 0],
            start_time = 497,
            end_time = 499
        )

        jump_dur = 0.3
        jump_start = 499.5
        for i in range(3):
            blob2.move_to(
                displacement = [0, 0.2, 0],
                start_time = jump_start + i * jump_dur,
                end_time = jump_start + i * jump_dur + jump_dur / 3,
            )
            blob2.move_to(
                displacement = [0, -0.2, 0],
                start_time = jump_start + i * jump_dur + jump_dur / 3,
                end_time = jump_start + (i + 1) * jump_dur,
            )

        blob2.blob_wave(
            start_time = 501,
            duration = 10
        )
        blob2.move_to(
            new_angle = [0, 9 * math.pi, 0],
            start_time = 501,
            end_time = 506
        )
        make_animations_linear(blob2.ref_obj, data_paths = ['rotation_euler'])

        dna = import_object(
            'dna_two_strand', 'biochem',
            location = [6, 0, 0],
            scale = 4
        )
        dna.add_to_blender(appear_time = 486)
        dna.tweak_colors_recursive()
        dna.spin(
            start_time = 0,
            end_time = 1000,
            spin_rate = 0.05
        )
        dna.disappear(disappear_time = 495)

        end = 505.5
        to_disappear = [blob, blob2]
        for i, thing in enumerate(to_disappear):
            thing.disappear(disappear_time = end - (len(to_disappear) - 1 - i) * 0.05)

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
        apply_material(vid_rec, 'color6')

        bpy.ops.mesh.primitive_cylinder_add()
        sub_cir = bpy.context.object
        sub_cir.scale = [98 / 1280 * 30, 98 / 1280 * 30, 0]
        sub_cir.location = [-11, 3.2, -0.01]

        #Whole end area
        bpy.ops.mesh.primitive_plane_add()
        end_area = bpy.context.object
        end_area.scale[0] = 1225 / 1280 * 15
        end_area.scale[1] = 518 / 720 * 8.4
        end_area.location = [0, 0.2, -0.15]'''

        logo = svg_bobject.SVGBobject(
            "Layer",
            #file_name = "PrimerLogoWhite",
            location = (-8.7, 3, 0),
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

        patreon = import_object(
            'patreon', 'svgblend',
            scale = 2.297,
            location = (-11, -3, 0),
            name = 'Patreon'
        )
        patreon.add_to_blender(appear_time = 0)
        thanks = tex_bobject.TexBobject(
            '\\text{Special thanks:}',
            location = [-8.35, -1.4, 0],
            color = 'color2'
        )
        thanks.add_to_blender(appear_time = 0)
        js = tex_bobject.TexBobject(
            '\\text{Jordan Scales}',
            location = [-7.8, -2.75, 0],
            color = 'color2',
            scale = 1
        )
        js.add_to_blender(appear_time = 0.5)

        bmkw = tex_bobject.TexBobject(
            '\\text{Kairui Wang}',
            location = [-7.8, -4, 0],
            color = 'color2',
            scale = 1
        )
        bmkw.add_to_blender(appear_time = 0.75)

        ap = tex_bobject.TexBobject(
            '\\text{Anonymous Patrons}',
            location = [-7.8, -5.25, 0],
            color = 'color2',
            scale = 1
        )
        ap.add_to_blender(appear_time = 1)


        remaining = [logo, patreon, thanks, js, bmkw, ap]
        for thing in remaining:
            thing.disappear(disappear_time = 2.5)

    def thumbnail(self):
        sg = svg_bobject.SVGBobject(
            "the_selfish_gene_century_italic",
            #location = (-5, 3.75, 0), #Centered position
            #scale = 0.26, #Centered scale
            location = [-6.7, 4.9, 0],
            scale = 4.6,
            color = 'color2',
            centered = True
        )
        sg.add_to_blender(appear_time = 0)

        for i in range(3, 10):
            sg.lookup_table[0][i].color_shift(
                color = COLORS_SCALED[5],
                start_time = -1,
                duration_time = None
            )


        d = import_object(
            'dna_two_strand', 'biochem',
            location = [7, 0, 0],#[7, 0, 0],
            rotation_euler = [0, 0, 0 * math.pi / 180],
            scale = 7
        )
        d.add_to_blender(appear_time = 0)

        d.spin(start_time = 0, spin_rate = 0.1)
        #d.tweak_colors_recursive()

        '''gd = import_object(
            'dna_two_strand', 'biochem',
            location = [7, 3.5, 0],#[7, 0, 0],
            rotation_euler = [0, 0, -90 * math.pi / 180],
            scale = 4.5#7
        )
        gd.add_to_blender(appear_time = 0)

        gd.spin(start_time = 0, spin_rate = 0.1)'''

        def make_clear_recursive(obj):
            apply_material(obj, 'trans_color2', intensity = 0.7)
            for child in obj.children:
                make_clear_recursive(child)

        make_clear_recursive(d.ref_obj.children[0])
