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


class InclusiveFitness(Scene):
    def __init__(self):
        self.subscenes = collections.OrderedDict([
            ('card', {'duration': 100})
        ])
        super().__init__()

    def play(self):
        super().play()

        #self.intro()
        #self.sim_rules()
        #self.traits()
        #self.diverse_stalling_sim()
        #self.fast_altruism()
        #self.big_altruism()
        #self.altruism_trait()
        #self.random_altruism_sim()
        #self.green_beard()
        #self.green_beard_sim()
        self.kin_selection_sim()
        #self.kin_distance_sim()
        #self.end_card()
        #self.thumbnail()

    def intro(self):
        return

        for i, thing in enumerate(to_disappear):
            thing.disappear(disappear_time = 6.5 - (len(to_disappear) - 1 - i) * 0.05)

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
            #sim = 'ns_env_intro_4',
            #initial_creatures = 3,
            location = [0, 0, 0],
            day_length_style = 'fixed_speed',
            #day_length_style = 'fixed_length'
            mutation_switches = {
                 'speed' : False,
                 'size' : False,
                 'sense' : False,
                 'altruist' : False,
                 'green_beard' : False,
                 'kin_radius' : False,
            },
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

        cam_swivel.move_to(
            new_location = [0, 0, 2.8],
            start_time = 3
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
            '\\text{Two+ food} \\longrightarrow \\text{Replicate}',
            location = [0, 10, 3.5],
            rotation_euler = cam_swivel.ref_obj.rotation_euler,
            centered = True,
            scale = 2
        )
        texts = [nf, of, tf]
        for i, t in enumerate(texts):
            t.add_to_blender(appear_time = 3.5 + 0.25 * i)


        to_disappear = [world] + texts
        for i, thing in enumerate(to_disappear):
            thing.disappear(disappear_time = 9 - (len(to_disappear) - 1 - i) * 0.05)

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
            end_time = 100000000 #Why not?
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

    def random_altruism_sim(self):
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
            mutation_switches = {
                 'speed' : False,
                 'size' : False,
                 'sense' : False,
                 'altruist' : True,
                 'green_beard' : False,
                 'kin_radius' : False,
            },
            scale = 1.5,
            food_count = 50,
            #sim = 'altruism_test',
            location = [-6.5, 0, 0],
            day_length_style = 'fixed_length'
        )

        for i in range(200):
            save = False
            if i == 49:
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


        g = graph_bobject.GraphBobject(
            location = [2, -4, 0],
            rotation_euler = [74 * math.pi / 180, 0, 0],
            #rotation_euler = [math.pi / 2, 0, 0],
            width = 10,
            x_range = 2,
            x_label = '\\phantom{a}',
            #x_label_pos = 'end',
            height = 10,
            y_range = 100,
            y_label = '\\%\\text{ Creatures}',
            y_label_pos = 'end',
            tick_step = [10, 50],
            #centered = True,
            include_y = True,
            arrows = False,
            padding = 0
        )

        #Way more complicated than it needs to be.
        bar_width = 0.5
        num_bars = 2
        space_width = (g.x_range[1] - num_bars * bar_width) / (num_bars + 1)

        alt_tex = tex_bobject.TexBobject(
            '\\text{Altruistic}',
            location = [
                (space_width + bar_width / 2) * g.width / g.x_range[1],
                -0.7,
                0
            ],
            color = 'color5',
            centered = True,
            #scale = 0.8
        )
        g.add_subbobject(alt_tex)

        not_tex = tex_bobject.TexBobject(
            '\\text{Not}',
            location = [
                (2 * space_width + bar_width * 1.5) * g.width / g.x_range[1],
                -0.7,
                0
            ],
            color = 'color5',
            centered = True,
            #scale = 0.8
        )
        g.add_subbobject(not_tex)

        g.add_to_blender(appear_time = 0)

        def count_by_vals(date, vals, nat_sim):
            counts = []
            creatures = nat_sim.date_records[date]['creatures']
            #print(len(creatures))
            for val in vals:
                #print()
                #print(spd)
                count = 0
                '''for cre in creatures:
                    print(str(val) + '   ' + str(cre.speed))
                    if cre.altruist == val:
                        count += 1'''
                count = len([x for x in creatures if x.altruist == val])
                #print(count)
                counts.append(count)
                #print(counts)
                #print()
            return counts

        '''bar_width = 0.5
        num_bars = 2
        space_width = (g.x_range[1] - num_bars * bar_width) / (num_bars + 1)'''

        def make_graph_bars(num_bars, appear_time, bar_width):
            bars = []
            space_width = (g.x_range[1] - num_bars * bar_width) / (num_bars + 1)
            for i in range(num_bars):
                #print(spd)
                bar = g.add_bar(
                    appear_time = appear_time,
                    x = (1 + i) * space_width + bar_width * (0.5 + i),
                    value = 0,
                    dx = bar_width
                )
                '''dummy = natural_sim.Creature()
                dummy.apply_material_by_speed(
                    bobj = bar,
                    spd = bar_width,
                )'''

                bars.append(bar)

            return bars

        def update_graph_bars(start_time, bars, counts, end_time = None):
            total = sum(counts)
            for i, bar in enumerate(bars):
                g.update_bar(
                    bar = bar,
                    new_value = counts[i] / total * 100,
                    start_time = start_time,
                    end_time = end_time
                )

        #speed_vals = [x/10 for x in range(23)]
        appear_time = 0
        bars = make_graph_bars(num_bars, appear_time, bar_width)
        #print(speed_vals)
        #counts = count_by_vals(9, [True, False], sim.sim)
        #update_graph_bars(0, bars, counts)

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

        #draw_possible_states()

        '''first_day_start = 172
        sim_appearance_time = 150.5

        #Find proper duration for first morning pause to fill talking time
        initial_day_durs = sim.sim.date_records[0]['anim_durations']
        first_morning_dur = first_day_start - \
                           sim_appearance_time - \
                           initial_day_durs['dawn'] - \
                           1 #For standard start_delay on drawn sims
        initial_day_durs['morning'] = first_morning_dur'''

        '''sim.add_to_blender(
            appear_time = 0,
            #start_day = first_day,
            #end_day = first_day + 21
            #start_day = actual_start_day,
            #end_day = actual_start_day + 21
        )'''

        #Update bars each day
        for day in sim.sim.date_records:
            date = day['date']
            if date == 0:
                start_time = 1 - OBJECT_APPEARANCE_TIME / FRAME_RATE
                end_time = 1

                counts = count_by_vals(date, [True, False], sim.sim)
                print(counts)
                update_graph_bars(start_time, bars, counts, end_time = end_time)

                #One the first day, the bar actually appears at the end of the
                #morning pause instead of at the end of the dawn stage. So
                #subtracting the morning duration from start time, since it's
                #added during the following loop.
                start_time = 1 - day['anim_durations']['morning']

            elif date > 0: #Don't regraph the old days
                prev_day_anims = sim.sim.date_records[date - 1]['anim_durations']
                start_time += prev_day_anims['morning'] + \
                              prev_day_anims['day'] + \
                              prev_day_anims['evening'] + \
                              prev_day_anims['night']

                #print(len(sim.sim.date_records[i]['creatures']))
                print(counts)
                end_time = start_time + day['anim_durations']['dawn']

                counts = count_by_vals(date, [True, False], sim.sim)
                update_graph_bars(start_time, bars, counts, end_time = end_time)
                start_time += day['anim_durations']['dawn']

        #Cam swaying
        '''cam_swivel.move_to(
            start_time = 190,
            end_time = 203,
            new_angle = [74 * math.pi / 180, 0, 10 * math.pi / 180]
        )
        cam_swivel.move_to(
            start_time = 203,
            end_time = 216,
            new_angle = [74 * math.pi / 180, 0, 0 * math.pi / 180]
        )'''

        end = 500
        to_disappear = [sim]
        for i, thing in enumerate(to_disappear):
            thing.disappear(disappear_time = end - (len(to_disappear) - 1 - i) * 0.05)

    def green_beard(self):

        blob = Blobject(wiggle = True, mouth = True)
        blob.add_to_blender(appear_time = 0)
        blob.add_beard(mat = 'color7')
        blob.hello(start_time = 0, end_time = 4)

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
        def set_initial_creatures():
            initial_creatures = []
            for i in range(math.floor(food_count / 4)):
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
        num_sims = 3
        for i in range(num_sims):
            print('------------------------- BEGIN SIM NUMBER ' + str(i + 1) + ' of ' + str(num_sims) + ' -------------------------')
            sim = natural_sim.DrawnNaturalSim(
                mutation_switches = {
                     'speed' : False,
                     'size' : False,
                     'sense' : False,
                     'altruist' : False,
                     'green_beard' : True,
                     'kin_altruist' : False,
                     'kin_radius' : False,
                },
                scale = 1.5,
                food_count = food_count,
                initial_creatures = set_initial_creatures(),
                #sim = 'altruism_test',
                location = [-6.5, 0, 0],
                day_length_style = 'fixed_length'
            )

            for i in range(100):
                save = False
                #if i == 99:
                #    save = True
                sim.sim.sim_next_day(save = save)

            sims.append(sim)

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


        g = graph_bobject.GraphBobject(
            location = [2, -4, 0],
            rotation_euler = [74 * math.pi / 180, 0, 0],
            #rotation_euler = [math.pi / 2, 0, 0],
            width = 10,
            x_range = 2,
            x_label = '\\phantom{a}',
            #x_label_pos = 'end',
            height = 10,
            y_range = 100,
            y_label = '\\%\\text{ Creatures}',
            y_label_pos = 'end',
            tick_step = [10, 50],
            #centered = True,
            include_y = True,
            arrows = False,
            padding = 0
        )

        #Way more complicated than it needs to be.
        bar_width = 0.5
        num_bars = 2
        space_width = (g.x_range[1] - num_bars * bar_width) / (num_bars + 1)

        alt_tex = tex_bobject.TexBobject(
            '\\text{Green beard}',
            location = [
                (space_width + bar_width / 2) * g.width / g.x_range[1],
                -0.7,
                0
            ],
            color = 'color5',
            centered = True,
            #scale = 0.8
        )
        g.add_subbobject(alt_tex)

        not_tex = tex_bobject.TexBobject(
            '\\text{Not}',
            location = [
                (2 * space_width + bar_width * 1.5) * g.width / g.x_range[1],
                -0.7,
                0
            ],
            color = 'color5',
            centered = True,
            #scale = 0.8
        )
        g.add_subbobject(not_tex)

        g.add_to_blender(appear_time = 0)

        def count_by_vals(date, vals, nat_sim):
            counts = []
            creatures = nat_sim.date_records[date]['creatures']
            #print(len(creatures))
            for val in vals:
                #print()
                #print(spd)
                count = 0
                '''for cre in creatures:
                    print(str(val) + '   ' + str(cre.speed))
                    if cre.altruist == val:
                        count += 1'''
                count = len([x for x in creatures if x.green_beard == val])
                #print(count)
                counts.append(count)
                #print(counts)
                #print()
            return counts

        '''bar_width = 0.5
        num_bars = 2
        space_width = (g.x_range[1] - num_bars * bar_width) / (num_bars + 1)'''

        def make_graph_bars(num_bars, appear_time, bar_width):
            bars = []
            space_width = (g.x_range[1] - num_bars * bar_width) / (num_bars + 1)
            for i in range(num_bars):
                #print(spd)
                bar = g.add_bar(
                    appear_time = appear_time,
                    x = (1 + i) * space_width + bar_width * (0.5 + i),
                    value = 0,
                    dx = bar_width
                )
                '''dummy = natural_sim.Creature()
                dummy.apply_material_by_speed(
                    bobj = bar,
                    spd = bar_width,
                )'''

                bars.append(bar)

            return bars

        def update_graph_bars(start_time, bars, counts, end_time = None):
            total = sum(counts)
            for i, bar in enumerate(bars):
                g.update_bar(
                    bar = bar,
                    new_value = counts[i] / total * 100,
                    start_time = start_time,
                    end_time = end_time
                )

        #speed_vals = [x/10 for x in range(23)]
        appear_time = 0
        bars = make_graph_bars(num_bars, appear_time, bar_width)
        #print(speed_vals)
        #counts = count_by_vals(9, [True, False], sim.sim)
        #update_graph_bars(0, bars, counts)

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

        #draw_possible_states()

        '''first_day_start = 172
        sim_appearance_time = 150.5

        #Find proper duration for first morning pause to fill talking time
        initial_day_durs = sim.sim.date_records[0]['anim_durations']
        first_morning_dur = first_day_start - \
                           sim_appearance_time - \
                           initial_day_durs['dawn'] - \
                           1 #For standard start_delay on drawn sims
        initial_day_durs['morning'] = first_morning_dur'''

        '''sim.add_to_blender(
            appear_time = 0,
            #start_day = first_day,
            #end_day = first_day + 21
            #start_day = actual_start_day,
            #end_day = actual_start_day + 21
        )'''

        #Update bars each day
        for day in sims[0].sim.date_records:
            date = day['date']
            if date == 0:
                start_time = 1 - OBJECT_APPEARANCE_TIME / FRAME_RATE
                end_time = 1

                total_counts_for_date = [0, 0]
                print('Counts for day ' + str(date))
                for single_sim in sims:
                    counts = count_by_vals(date, [True, False], single_sim.sim)
                    print(' ' + str(counts))
                    total_counts_for_date[0] += counts[0]
                    total_counts_for_date[1] += counts[1]
                print(' ----------------------')
                print(' ' + str(total_counts_for_date))
                avgs_for_date = [[],[]]
                avgs_for_date[0] = total_counts_for_date[0] / len(sims)
                avgs_for_date[1] = total_counts_for_date[1] / len(sims)
                update_graph_bars(start_time, bars, avgs_for_date, end_time = end_time)

                #One the first day, the bar actually appears at the end of the
                #morning pause instead of at the end of the dawn stage. So
                #subtracting the morning duration from start time, since it's
                #added during the following loop.
                start_time = 1 - day['anim_durations']['morning']

            elif date > 0: #Don't regraph the old days
                prev_day_anims = sim.sim.date_records[date - 1]['anim_durations']
                start_time += prev_day_anims['morning'] + \
                              prev_day_anims['day'] + \
                              prev_day_anims['evening'] + \
                              prev_day_anims['night']

                #print(len(sim.sim.date_records[i]['creatures']))
                #print(counts)
                end_time = start_time + day['anim_durations']['dawn']

                total_counts_for_date = [0, 0]
                print('Counts for day ' + str(date))
                for single_sim in sims:
                    counts = count_by_vals(date, [True, False], single_sim.sim)
                    print(' ' + str(counts))
                    total_counts_for_date[0] += counts[0]
                    total_counts_for_date[1] += counts[1]
                print(' ----------------------')
                print(' ' + str(total_counts_for_date))
                avgs_for_date = [[],[]]
                avgs_for_date[0] = total_counts_for_date[0] / len(sims)
                avgs_for_date[1] = total_counts_for_date[1] / len(sims)
                update_graph_bars(start_time, bars, avgs_for_date, end_time = end_time)
                start_time += day['anim_durations']['dawn']

        #Cam swaying
        '''cam_swivel.move_to(
            start_time = 190,
            end_time = 203,
            new_angle = [74 * math.pi / 180, 0, 10 * math.pi / 180]
        )
        cam_swivel.move_to(
            start_time = 203,
            end_time = 216,
            new_angle = [74 * math.pi / 180, 0, 0 * math.pi / 180]
        )'''

        end = 500
        to_disappear = [sim]
        for i, thing in enumerate(to_disappear):
            thing.disappear(disappear_time = end - (len(to_disappear) - 1 - i) * 0.05)

    def kin_selection_sim(self):
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
        def set_initial_creatures():
            initial_creatures = []
            for i in range(math.floor(food_count / 4)):
                initial_creatures.append(
                    natural_sim.Creature(
                        size = 1,# + randrange(-5, 6) * natural_sim.MUTATION_VARIATION,
                        speed = 1,# + randrange(-5, 6) * natural_sim.MUTATION_VARIATION,
                        sense = 1,# + randrange(-5, 6) * natural_sim.MUTATION_VARIATION,
                        kin_altruist = True
                    )
                )
                initial_creatures.append(
                    natural_sim.Creature(
                        size = 1,# + randrange(-5, 6) * natural_sim.MUTATION_VARIATION,
                        speed = 1,# + randrange(-5, 6) * natural_sim.MUTATION_VARIATION,
                        sense = 1,# + randrange(-5, 6) * natural_sim.MUTATION_VARIATION,
                        kin_altruist = False
                    )
                )
            return initial_creatures

        sims = []
        num_sims = 10
        for i in range(num_sims):
            print('------------------------- BEGIN SIM NUMBER ' + str(i + 1) + ' of ' + str(num_sims) + ' -------------------------')
            sim = natural_sim.DrawnNaturalSim(
                mutation_switches = {
                     'speed' : False,
                     'size' : False,
                     'sense' : False,
                     'altruist' : False,
                     'green_beard' : False,
                     'kin_altruist' : True,
                     'kin_radius' : False,
                },
                scale = 1.5,
                food_count = food_count,
                initial_creatures = set_initial_creatures(),
                #sim = 'altruism_test',
                location = [-6.5, 0, 0],
                day_length_style = 'fixed_length'
            )

            for i in range(100):
                save = False
                #if i == 99:
                #    save = True
                sim.sim.sim_next_day(save = save)

            sims.append(sim)

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


        g = graph_bobject.GraphBobject(
            location = [2, -4, 0],
            rotation_euler = [74 * math.pi / 180, 0, 0],
            #rotation_euler = [math.pi / 2, 0, 0],
            width = 10,
            x_range = 2,
            x_label = '\\phantom{a}',
            #x_label_pos = 'end',
            height = 10,
            y_range = 100,
            y_label = '\\%\\text{ Creatures}',
            y_label_pos = 'end',
            tick_step = [10, 50],
            #centered = True,
            include_y = True,
            arrows = False,
            padding = 0
        )

        #Way more complicated than it needs to be.
        bar_width = 0.5
        num_bars = 2
        space_width = (g.x_range[1] - num_bars * bar_width) / (num_bars + 1)

        alt_tex = tex_bobject.TexBobject(
            '\\text{Kin altruist}',
            location = [
                (space_width + bar_width / 2) * g.width / g.x_range[1],
                -0.7,
                0
            ],
            color = 'color5',
            centered = True,
            #scale = 0.8
        )
        g.add_subbobject(alt_tex)

        not_tex = tex_bobject.TexBobject(
            '\\text{Not}',
            location = [
                (2 * space_width + bar_width * 1.5) * g.width / g.x_range[1],
                -0.7,
                0
            ],
            color = 'color5',
            centered = True,
            #scale = 0.8
        )
        g.add_subbobject(not_tex)

        g.add_to_blender(appear_time = 0)

        def count_by_vals(date, vals, nat_sim):
            counts = []
            creatures = nat_sim.date_records[date]['creatures']
            #print(len(creatures))
            for val in vals:
                #print()
                #print(spd)
                count = 0
                '''for cre in creatures:
                    print(str(val) + '   ' + str(cre.speed))
                    if cre.altruist == val:
                        count += 1'''
                count = len([x for x in creatures if x.kin_altruist == val])
                #print(count)
                counts.append(count)
                #print(counts)
                #print()
            return counts

        '''bar_width = 0.5
        num_bars = 2
        space_width = (g.x_range[1] - num_bars * bar_width) / (num_bars + 1)'''

        def make_graph_bars(num_bars, appear_time, bar_width):
            bars = []
            space_width = (g.x_range[1] - num_bars * bar_width) / (num_bars + 1)
            for i in range(num_bars):
                #print(spd)
                bar = g.add_bar(
                    appear_time = appear_time,
                    x = (1 + i) * space_width + bar_width * (0.5 + i),
                    value = 0,
                    dx = bar_width
                )
                '''dummy = natural_sim.Creature()
                dummy.apply_material_by_speed(
                    bobj = bar,
                    spd = bar_width,
                )'''

                bars.append(bar)

            return bars

        def update_graph_bars(start_time, bars, counts, end_time = None):
            total = sum(counts)
            for i, bar in enumerate(bars):
                g.update_bar(
                    bar = bar,
                    new_value = counts[i] / total * 100,
                    start_time = start_time,
                    end_time = end_time
                )

        #speed_vals = [x/10 for x in range(23)]
        appear_time = 0
        bars = make_graph_bars(num_bars, appear_time, bar_width)
        #print(speed_vals)
        #counts = count_by_vals(9, [True, False], sim.sim)
        #update_graph_bars(0, bars, counts)

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

        #draw_possible_states()

        '''first_day_start = 172
        sim_appearance_time = 150.5

        #Find proper duration for first morning pause to fill talking time
        initial_day_durs = sim.sim.date_records[0]['anim_durations']
        first_morning_dur = first_day_start - \
                           sim_appearance_time - \
                           initial_day_durs['dawn'] - \
                           1 #For standard start_delay on drawn sims
        initial_day_durs['morning'] = first_morning_dur'''

        '''sim.add_to_blender(
            appear_time = 0,
            #start_day = first_day,
            #end_day = first_day + 21
            #start_day = actual_start_day,
            #end_day = actual_start_day + 21
        )'''

        #Update bars each day
        for day in sims[0].sim.date_records:
            date = day['date']

            total_counts_for_date = [0, 0]
            print('Stats for day ' + str(date))
            for single_sim in sims:
                print(' ----------------------')
                counts = count_by_vals(date, [True, False], single_sim.sim)
                print(' Counts: ' + str(counts))
                total_counts_for_date[0] += counts[0]
                total_counts_for_date[1] += counts[1]
                print(' ----------------------')
                counts = count_by_vals(date, [True, False], single_sim.sim)
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

            print(' ----------------------')
            print(' Total counts')
            print(' ' + str(total_counts_for_date))
            print()

            avgs_for_date = [[],[]]
            avgs_for_date[0] = total_counts_for_date[0] / len(sims)
            avgs_for_date[1] = total_counts_for_date[1] / len(sims)

            if date == 0:
                start_time = 1 - OBJECT_APPEARANCE_TIME / FRAME_RATE
                end_time = 1

                update_graph_bars(start_time, bars, avgs_for_date, end_time = end_time)

                #On the first day, the bar actually appears at the end of the
                #morning pause instead of at the end of the dawn stage. So
                #subtracting the morning duration from start time, since it's
                #added during the following loop.
                start_time = 1 - day['anim_durations']['morning']

            elif date > 0: #Don't regraph the old days
                prev_day_anims = sim.sim.date_records[date - 1]['anim_durations']
                start_time += prev_day_anims['morning'] + \
                              prev_day_anims['day'] + \
                              prev_day_anims['evening'] + \
                              prev_day_anims['night']

                #print(len(sim.sim.date_records[i]['creatures']))
                #print(counts)
                end_time = start_time + day['anim_durations']['dawn']

                update_graph_bars(start_time, bars, avgs_for_date, end_time = end_time)
                start_time += day['anim_durations']['dawn']

        try:
            print(natural_sim.SAMARITAN_RATIO)
        except:
            pass

        #Cam swaying
        '''cam_swivel.move_to(
            start_time = 190,
            end_time = 203,
            new_angle = [74 * math.pi / 180, 0, 10 * math.pi / 180]
        )
        cam_swivel.move_to(
            start_time = 203,
            end_time = 216,
            new_angle = [74 * math.pi / 180, 0, 0 * math.pi / 180]
        )'''

        end = 500
        to_disappear = [sim]
        for i, thing in enumerate(to_disappear):
            thing.disappear(disappear_time = end - (len(to_disappear) - 1 - i) * 0.05)

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

        food_count = 1000
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

    def end_card(self):
        cues = self.subscenes
        scene_end = self.duration

        bpy.ops.mesh.primitive_plane_add()
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
        end_area.location = [0, 0.2, -0.15]

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

        ap = tex_bobject.TexBobject(
            '\\text{Anonymous Patrons}',
            location = [-7.8, -4, 0],
            color = 'color2',
            scale = 1
        )
        ap.add_to_blender(appear_time = 0.75)


        remaining = [logo, patreon, thanks, js, ap]
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
