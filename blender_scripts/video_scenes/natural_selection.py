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
            ('env', {'duration': 31}),
            ('spd', {'duration': 16}),
        ])
        super().__init__()

    def play(self):
        super().play()

        #self.intro()
        #self.environment()
        self.speed()

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

        #TODO:
        #Fix keyframing of constraints when creatures are reused
        #Fix scaledown when creatures die. Maybe only for reused bobjects.
        #Creatures can keep walking after being eaten. Fix that. Might be because
            #the homebound state sticks


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

    def speed(self):
        cues = self.subscenes['spd']
        st = cues['start']

        text = tex_bobject.TexBobject(
            '\\text{First trait: Speed}',
            location = [0, 6, 0],
            scale = 3,
            color = 'color2',
            centered = True
        )

        text.add_to_blender(appear_time = st + 1)

        blob = import_object(
            'boerd_blob', 'creatures',
            location = [0, -2, 0],
            scale = 4,
            wiggle = True
        )
        apply_material(blob.ref_obj.children[0].children[0], 'creature_color3')
        blob.add_to_blender(appear_time = st + 2)

        def f_blob():
            f_blob = import_object(
                'boerd_blob', 'creatures',
                location = [0, -2, 0],
                scale = 4,
                wiggle = True
            )
            apply_material(f_blob.ref_obj.children[0].children[0], 'creature_color7')
            mix = natural_sim.MUTATION_VARIATION / natural_sim.SPEED_PER_COLOR
            color = mix_colors(COLORS_SCALED[2], COLORS_SCALED[6], mix)
            obj = f_blob.ref_obj.children[0].children[0]
            f_blob.color_shift(
                duration_time = None,
                color = color,
                start_time = 0,
                shift_time = 1 / FRAME_RATE,
                obj = obj
            )
            f_blob.add_to_blender(appear_time = st + 3)
            f_blob.move_to(
                new_location = [8, -2, 0],
                start_time = st + 3
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
            apply_material(s_blob.ref_obj.children[0].children[0], 'creature_color8')
            mix = natural_sim.MUTATION_VARIATION / natural_sim.SPEED_PER_COLOR
            color = mix_colors(COLORS_SCALED[2], COLORS_SCALED[7], mix)
            obj = s_blob.ref_obj.children[0].children[0]
            s_blob.color_shift(
                duration_time = None,
                color = color,
                start_time = 0,
                shift_time = 1 / FRAME_RATE,
                obj = obj
            )
            s_blob.add_to_blender(appear_time = st + 4)
            s_blob.move_to(
                new_location = [-8, -2, 0],
                start_time = st + 4
            )

            return s_blob
        s_blob = s_blob()

        to_disappear = [f_blob, s_blob]
        for thing in to_disappear:
            thing.disappear(disappear_time = st + 6 + 0.5)

        blob.move_to(
            new_location = [-10, 0.5, 0],
            new_scale = 2,
            start_time = st + 6
        )

        rf_blob = import_object(
            'boerd_blob', 'creatures',
            location = [-10, 0.5, 0],
            scale = 2,
            wiggle = True
        )
        apply_material(rf_blob.ref_obj.children[0].children[0], 'creature_color3')
        rf_blob.add_to_blender(appear_time = st + 7)
        rf_blob.move_to(
            new_location = [-10, -5, 0],
            start_time = st + 7
        )
        obj = rf_blob.ref_obj.children[0].children[0]
        shift_frames = 60
        color_set = [COLORS_SCALED[6], COLORS_SCALED[4], COLORS_SCALED[3], COLORS_SCALED[5]]
        for i in range(4):
            rf_blob.color_shift(
                duration_time = None,
                color = color_set[i],
                start_time = st + 8 + i * shift_frames / 4 / FRAME_RATE,
                shift_time = shift_frames / 4,
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

            arrow.add_to_blender(appear_time = st + 10, transition_time = 2 * OBJECT_APPEARANCE_TIME)
            blob.move_to(
                new_angle = [0, math.pi / 2, 0],
                start_time = st + 9.8
            )
            blob.move_to(
                new_location = [4, 0.5, 0],
                start_time = st + 10,
                end_time = st + 11
            )
            blob.move_to(
                new_angle = [0, 0, 0],
                start_time = st + 10.7
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
            slow_time.add_to_blender(appear_time = st + 9)
            for i in range(1, len(time_exprs)):
                start_time = st + 10 + i * (1/len(time_exprs)) #1 is the movement duration
                slow_time.morph_figure(i, start_time = start_time)

            energy_exprs = [('\\text{Energy}=' + str(x)) for x in time]
            slow_energy = tex_bobject.TexBobject(
                *energy_exprs,
                location = [6, -0.5, 0],
                transition_type = 'instant'
            )
            slow_energy.add_to_blender(appear_time = st + 9)
            for i in range(1, len(energy_exprs)):
                start_time = st + 10 + i * (1/len(energy_exprs)) #1 is the movement duration
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

            arrow.add_to_blender(appear_time = st + 10, transition_time = OBJECT_APPEARANCE_TIME)
            rf_blob.move_to(
                new_angle = [0, math.pi / 2, 0],
                start_time = st + 9.8,
                end_time = st + 9.8 + 0.4
            )
            rf_blob.move_to(
                new_location = [4, -5, 0],
                start_time = st + 10,
                #end_time = st + 11
            )
            rf_blob.move_to(
                new_angle = [0, 0, 0],
                start_time = st + 10.3,
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
            fast_time.add_to_blender(appear_time = st + 9)
            for i in range(1, len(time_exprs)):
                start_time = st + 10 + i * (0.5/len(time_exprs)) #0.5 is the movement duration
                fast_time.morph_figure(i, start_time = start_time)

            energy_exprs = [('\\text{Energy}=' + str(x*4)) for x in time]
            fast_energy = tex_bobject.TexBobject(
                *energy_exprs,
                location = [6, -6, 0],
                transition_type = 'instant'
            )
            fast_energy.add_to_blender(appear_time = st + 9)
            for i in range(1, len(energy_exprs)):
                start_time = st + 10 + i * (0.5/len(energy_exprs)) #0.5 is the movement duration
                fast_energy.morph_figure(i, start_time = start_time)

            return fast_time, fast_energy, arrow

        slow_time, slow_energy, slow_arrow = slow_move()
        fast_time, fast_energy, fast_arrow = fast_move()

        for tex in [slow_time, fast_time]:
            tex.pulse(start_time = st + 12)

        for tex in [slow_energy, fast_energy]:
            tex.pulse(start_time = st + 13)

        #TODO: Pulse tex_bobjects along with speech
              #Make everything disappear
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
            thing.disappear(disappear_time = cues['end'] - (len(to_disappear) - 1 - i) * 0.05)
