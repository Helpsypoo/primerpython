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
import creature
imp.reload(creature)
import drawn_world
imp.reload(drawn_world)
import population
imp.reload(population)
import gesture
imp.reload(gesture)
import graph_bobject
imp.reload(graph_bobject)
import tex_complex
imp.reload(tex_complex)

import helpers
imp.reload(helpers)
from helpers import *

#'''
class WTEThumbnail(Scene):
    def __init__(self):

        self.subscenes = collections.OrderedDict([
            ('logo', {'duration': 1.25})
        ])
        super().__init__()

    def play(self):
        super().play()
        cues = self.subscenes
        scene_end = self.duration

        bobj = import_object(
            'boerd_blob', 'creatures',
            scale = 10,
            location = [-5.5, -8.5, 0],
            rotation_euler = [0, math.pi * 45 / 180, 0]
        )
        bobj.ref_obj.children[0].children[2].data.resolution = 0.1
        bobj.add_to_blender(
            appear_time = -1,
        )
        apply_material(
            bobj.ref_obj,
            'creature_color3',
            recursive = True,
            type_req = 'META'
        )
        bone = bobj.ref_obj.children[0].pose.bones[3]
        bone.rotation_quaternion = [1, 0, 0.1, 0.15]


        earth = import_object(
            'earth', 'planets',
            location = (11, 0, 0),
            scale = 10,
            name = 'earth',
            rotation_euler = [math.pi * 19 / 180, math.pi * -36 / 180, 0]
        )
        earth.add_to_blender(
            appear_time = -1,
            animate = True
        )

        why = tex_bobject.TexBobject(
            "\\text{Why?}",
            location = [-6.5, 4, 0],
            scale = 5,
            centered = True
        )
        why.add_to_blender(appear_time = -1)


        world = bpy.context.scene.world
        nodes = world.node_tree.nodes
        nodes.new(type = 'ShaderNodeMixRGB')
        nodes.new(type = 'ShaderNodeTexImage')
        nodes.new(type = 'ShaderNodeTexCoord')

        path_mix_input = nodes[2].inputs[2]

        for l in world.node_tree.links:
            if l.to_socket == path_mix_input:
               world.node_tree.links.remove(l)

        world.node_tree.links.new(nodes[5].outputs[0], nodes[2].inputs[2])
        world.node_tree.links.new(nodes[4].outputs[0], nodes[5].inputs[1])
        world.node_tree.links.new(nodes[6].outputs[0], nodes[5].inputs[2])
        world.node_tree.links.new(nodes[7].outputs[5], nodes[6].inputs[0])

        stars_path = os.path.join(IMG_DIR, 'milky-way-and-starry-night-sky.jpg')
        try:
            img = bpy.data.images.load(stars_path)
        except:
            raise NameError("Cannot load image %s" % path)
        nodes[6].image = img

        nodes[5].inputs[0].default_value = 0


        #Keyframes for background transition
        #nodes[4].outputs[0].keyframe_insert(data_path = 'default_value', frame = planets_start)
        nodes[4].outputs[0].default_value = (0, 0, 0, 1)
        #nodes[4].outputs[0].keyframe_insert(data_path = 'default_value', frame = planets_start + 60)

        #nodes[5].inputs[0].keyframe_insert(data_path = 'default_value', frame = planets_start + 60)
        nodes[5].inputs[0].default_value = 1
        #nodes[5].inputs[0].keyframe_insert(data_path = 'default_value', frame = planets_start + 120)
        #nodes[5].inputs[0].keyframe_insert(data_path = 'default_value', frame = planets_end - 90)
        #nodes[5].inputs[0].default_value = 0
        #nodes[5].inputs[0].keyframe_insert(data_path = 'default_value', frame = planets_end - 30)

        #nodes[4].outputs[0].keyframe_insert(data_path = 'default_value', frame = planets_end - 30)
        #nodes[4].outputs[0].default_value = COLORS_SCALED[0]
        #nodes[4].outputs[0].keyframe_insert(data_path = 'default_value', frame = planets_end + 30)
#'''
'''
class ROThumbnail(Scene):
    def __init__(self):
        self.subscenes = collections.OrderedDict([
            ('logo', {'duration': 1.25})
        ])
        super().__init__()

    def play(self):
        super().play()
        cues = self.subscenes
        scene_end = self.duration

        bobj = import_object(
            'boerd_blob', 'creatures',
            scale = 3,
            location = [-6.7, 2.5, 0],
            rotation_euler = [0, math.pi * 45 / 180, 0]
        )
        bobj.ref_obj.children[0].children[2].data.resolution = 0.1
        bobj.add_to_blender(
            appear_frame = 0,
        )
        apply_material(
            bobj.ref_obj,
            'creature_color3',
            recursive = True,
            type_req = 'META'
        )
        bone = bobj.ref_obj.children[0].pose.bones[3]
        bone.rotation_quaternion = [1, 0.1, 0, -0.25]


        why = tex_bobject.TexBobject(
            "\\text{Replicators Only}",
            location = [0, 5, 0],
            scale = 3,
            centered = True
        )
        #why.add_to_blender(appear_frame = 0)



        #Way more than necessary here, but borrowing code from a more complex scene

        #Transition to N-t graph
        def exp_func(x): return 5 * math.exp(0.1 * x)
        #def exp_func(x): return 15 * math.exp(0.1 * x) - 10
        graph2 = graph_bobject.GraphBobject(
            exp_func,
            x_range = [0, 20],
            y_range = [0, 75],
            tick_step = [5, 25],
            width = 22,
            height = 11,
            x_label = 't',
            x_label_pos = 'end',
            y_label = 'N',
            y_label_pos = 'end',
            location = [-0.7, -1, 0], #(6.5, -2.5, 0),
            centered = True,
            arrows = True,
            scale = 1,
            high_res_curve_indices = [0, 1, 2]
        )

        frames_per_time_step = 15
        start_delay = 1.5
        sim_duration = 20

        initial_creature_count = 5
        initial_creatures = []
        for i in range(initial_creature_count):
            new_creature = creature.Creature()
            initial_creatures.append(new_creature)
        sim = drawn_world.DrawnWorld(
            name = 'blob1_sim',
            location = [0, -2.5, 0],
            scale = 0.4,
            #appear_frame = cues['ntgraph']['start'] + 180,
            start_delay = start_delay,
            frames_per_time_step = frames_per_time_step,
            #save = True,
            #load = 'ro_not_extinction',
            sim_duration = sim_duration,
            initial_creatures = initial_creatures,
            gene_updates = [
                ['color', 'creature_color_1', 'birth_modifier', 0, 0],
                ['shape', 'shape1', 'birth_modifier', 0, 0],
                ['size', '1', 'birth_modifier', 0, 0],
                ['color', 'creature_color_1', 'mutation_chance', 0, 0],
                ['shape', 'shape1', 'mutation_chance', 0, 0],
                ['size', '1', 'mutation_chance', 0, 0],
                ['color', 'creature_color_1', 'death_modifier', 200, 0],
                ['color', 'creature_color_1', 'replication_modifier', 300, 0],
            ],
            pauses = [
                [0, 1]
            ]
        )
        graph2.add_to_blender(appear_time = 0)

        #Predicted curve
        """graph2.animate_function_curve(
            start_time = cues['ntgraph']['start'] + 0.5,
            end_time = cues['ntgraph']['start'] + 1.5,
            #uniform_along_x = True,
            index = 0
        )"""

        #Many sims
        num_sims = 40
        for i in range(num_sims):
            sim.simulate()
            func = sim.get_creature_count_by_t()
            #print(func)
            graph2.add_new_function_and_curve(
                func,
                curve_mat_modifier = 'fade',
                z_shift = -0.05
            )
        graph2.animate_all_function_curves(
            start_time = 0,
            end_time = 1,
            start_window = 0.5,
            uniform_along_x = True,
            skip = 3
        )
'''
'''
class IntroImage(Scene):
    def __init__(self):

        self.subscenes = collections.OrderedDict([
            ('logo', {'duration': 1.25})
        ])
        super().__init__()

    def play(self):
        super().play()
        cues = self.subscenes
        scene_end = self.duration

        logo = svg_bobject.SVGBobject(
            "Layer",
            #file_name = "PrimerLogoWhite",
            location = (-7.45, 1.5, 0),
            scale = 2
        )
        for bobj in logo.rendered_curve_bobjects:
            apply_material(bobj.ref_obj.children[0], 'color2')
        stroke = logo.rendered_curve_bobjects[0]
        apply_material(stroke.ref_obj.children[0], 'color3')
        logo.morph_chains[0][0].ref_obj.location[2] = -1
        logo.add_to_blender(
            appear_time = cues['logo']['start'],
            #subbobject_timing = [90, 30, 40, 50, 60, 70, 80],
            subbobject_timing = [42, 30, 33, 36, 39, 42, 45],
            animate = True
        )
        logo.disappear(disappear_time = scene_end)
'''
'''
class TheGoal(Scene):
    def __init__(self):
        self.subscenes = collections.OrderedDict([
            ('sim', {'duration': 33})
        ])
        super().__init__()

    def play(self):
        super().play()
        cues = self.subscenes
        scene_end = self.duration


        rhs = tex_bobject.TexBobject(
            "\\dfrac{B}{D - R}",
            "\\dfrac{\\xcancel{B}}{D - R}",
            centered = True,
            vert_align_centers = False
        )
        equals = tex_bobject.TexBobject(
            "\!=",
            centered = True
        )
        lhs = tex_bobject.TexBobject(
            "N",
            centered = True
        )
        equation = tex_complex.TexComplex(
            lhs, equals, rhs,
            centered = True,
            scale = 1.5,
            location = (-7.5, 0, 0)
        )

        initial_creature_count = 5
        initial_creatures = []
        for i in range(initial_creature_count):
            new_creature = creature.Creature()
            initial_creatures.append(new_creature)
        sim = drawn_world.DrawnWorld(
            name = 'blob1_sim',
            location = [6.5, 0, 0],
            scale = 0.6,
            #appear_frame = cues['sim']['start'],
            start_delay = 30,
            #save = True,
            #load = 'wte_eq_replication',
            sim_duration_seconds = cues['sim']['duration'],
            initial_creatures = initial_creatures,
            gene_updates = [
                ['color', 'creature_color_1', 'birth_modifier', 30, 0],
                ['shape', 'shape1', 'birth_modifier', 1, 0],
                ['size', '1', 'birth_modifier', 1, 0],
                ['color', 'creature_color_1', 'mutation_chance', 0, 0],
                ['shape', 'shape1', 'mutation_chance', 0, 0],
                ['size', '1', 'mutation_chance', 0, 0],
                ['color', 'creature_color_1', 'death_modifier', 6, 0],
                ['color', 'creature_color_1', 'replication_modifier', 4, 0],
            ],
            #counter_alignment = 'top_left',
            #creature_model = ['stanford_bunny', 'creatures']
        )

        equation.add_to_blender(appear_time = cues['sim']['start'] + 2)
        #rhs.morph_figure(1, start_frame = 60)


        sim.add_to_blender(
            appear_time = cues['sim']['start'] + 2,
            animate = True
        )

        B = rhs.lookup_table[0][0]
        B.pulse(
            time = cues['sim']['start'] + 11,
            duration = 5 * FRAME_RATE,
        )
        B.color_shift(
            start_time = cues['sim']['start'] + 11,
            duration = 5 * FRAME_RATE,
            color = COLORS_SCALED[3]
        )

        spontaneous = tex_bobject.TexBobject(
            '\\substack{\\text{Spontaneous} \\\\ \\text{birth chance}}',
            location = (-5.5, 5.5, 0),
            centered = True,
            color = 'color2'
        )
        spontaneous.add_to_blender(appear_time = cues['sim']['start'] + 11)

        spont_arrow = gesture.Gesture(
            gesture_series = [
                #{
                #    'type': 'bracket',
                #    'points': {
                #        'annotation_point': (-5.5, 4, 0),
                #        'left_point': (-6.5, 2, 0),
                #        'right_point': (-4.5, 2, 0)
                #    }
                #}
                {
                    'type': 'arrow',
                    'points': {
                        'tail': (-5.5, 4.25, 0),
                        'head': (-5.5, 2.25, 0)
                    }
                }
            ],
            color = 'color2'
        )
        spont_arrow.add_to_blender(appear_time = cues['sim']['start'] + 11)
        """spont_arrow.subbobjects[0].color_shift(
            start_time = cues['sim']['start'] + 10,
            duration = 2 * OBJECT_APPEARANCE_TIME,
            color = COLORS_SCALED[3]
        )
        for bobj in spontaneous.subbobjects:
            bobj.color_shift(
                start_time = cues['sim']['start'] + 10,
                duration = 2 * OBJECT_APPEARANCE_TIME,
                color = COLORS_SCALED[3]
            )"""

        R = rhs.lookup_table[0][4]
        R.pulse(
            time = cues['sim']['start'] + 17,
            duration = 4 * FRAME_RATE
        )
        R.color_shift(
            start_time = cues['sim']['start'] + 17,
            duration = 4 * FRAME_RATE,
            color = COLORS_SCALED[3]
        )
        replication = tex_bobject.TexBobject(
            '\\substack{\\text{Replication} \\\\ \\text{chance}}',
            location = (-5, -5.5, 0),
            centered = True,
            color = 'color2'
        )
        replication.add_to_blender(appear_time = cues['sim']['start'] + 17,)

        rep_arrow = gesture.Gesture(
            gesture_series = [
                #{
                #    'type': 'bracket',
                #    'points': {
                #        'annotation_point': (-5.5, 4, 0),
                #        'left_point': (-6.5, 2, 0),
                #        'right_point': (-4.5, 2, 0)
                #    }
                #}
                {
                    'type': 'arrow',
                    'points': {
                        'tail': (-5, -4.25, 0),
                        'head': (-4.2, -2.25, 0)
                    }
                }
            ],
            color = 'color2'
        )
        rep_arrow.add_to_blender(appear_time = cues['sim']['start'] + 17)
        """rep_arrow.subbobjects[0].color_shift(
            start_frame = 120,
            duration = 4 * FRAME_RATE,
            color = COLORS_SCALED[3]
        )
        for bobj in replication.subbobjects:
            bobj.color_shift(
                start_time = cues['sim']['start'] + 17,
                duration = 4 * FRAME_RATE,
                color = COLORS_SCALED[3]
            )"""

        rhs.morph_figure(1, start_time = cues['sim']['start'] + 27)
        cross1 = rhs.lookup_table[1][1]
        apply_material(cross1.ref_obj.children[0], 'color6')
        cross2 = rhs.lookup_table[1][0]
        apply_material(cross2.ref_obj.children[0], 'color6')

        remaining = [equation, sim, spont_arrow, spontaneous, replication, rep_arrow]
        for thing in remaining:
            thing.disappear(disappear_time = scene_end)
'''
'''
class ThereWillBeGraphs(Scene):
    def __init__(self):
        self.subscenes = collections.OrderedDict([
            #('delay', {'duration': 0.5}),
            ('sim', {'duration': 8.5}),
        ])
        super().__init__()

    def play(self):
        super().play()
        cues = self.subscenes
        scene_end = self.duration

        start_delay = 0.5
        sim_duration = 60
        #frames_per_time_step = 5
        #sim_duration_frames = sim_duration * frames_per_time_step

        initial_creature_count = 10
        initial_creatures = []
        for i in range(initial_creature_count):
            new_creature = creature.Creature()
            initial_creatures.append(new_creature)
        sim = drawn_world.DrawnWorld(
            name = 'blob1_sim',
            location = [-7.5, 0, 0],
            scale = 0.6,
            #appear_frame = cues['sim']['start'],
            start_delay = start_delay,
            frames_per_time_step = 7,
            #save = True,
            #load = 'wte_eq_replication',
            sim_duration = sim_duration,
            initial_creatures = initial_creatures,
            gene_updates = [
                ['color', 'creature_color_1', 'birth_modifier', 1000, 0],
                ['shape', 'shape1', 'birth_modifier', 1, 0],
                ['size', '1', 'birth_modifier', 1, 0],
                ['color', 'creature_color_1', 'mutation_chance', 0, 0],
                ['shape', 'shape1', 'mutation_chance', 0, 0],
                ['size', '1', 'mutation_chance', 0, 0],
                ['color', 'creature_color_1', 'death_modifier', 100, 0],
                #['color', 'creature_color_1', 'replication_modifier', 10, 0],
            ]
        )
        sim.add_to_blender(appear_time = cues['sim']['start'])

        func = sim.get_creature_count_by_t()
        graph = graph_bobject.GraphBobject(
            func,
            x_range = [0, sim_duration],
            y_range = [0, 20],
            tick_step = [20, 10],
            width = 10,
            height = 5,
            x_label = 't',
            x_label_pos = 'end',
            y_label = 'N',
            y_label_pos = 'along',
            location = (7, -4.5, 0),
            centered = True,
            arrows = True
        )
        graph.add_to_blender(appear_time = cues['sim']['start'])
        graph.animate_function_curve(
            start_time = cues['sim']['start'] + start_delay,
            end_time = cues['sim']['start'] + start_delay + 7,
            uniform_along_x = True
        )
        appear_coord = [0, func[0], 0]
        point = graph.add_point_at_coord(
            coord = appear_coord,
            appear_time = cues['sim']['start'],
            axis_projections = True,
            track_curve = 0
        )
        graph.animate_point(
            end_coord = [sim_duration, 0, 0],
            start_time = cues['sim']['start'] + start_delay,
            end_time = cues['sim']['start'] + start_delay + 7,
            point = point
        )
        #Rate-number graph
        def func2(x): return 1 - x / 10
        graph2 = graph_bobject.GraphBobject(
            func2,
            x_range = [0, 20],
            y_range = [-1, 1],
            tick_step = [5, 1],
            width = 10,
            height = 5,
            x_label = 'N',
            x_label_pos = 'end',
            y_label = '\\Delta',
            y_label_pos = 'end',
            location = (7, 2.5, 0),
            centered = True,
            arrows = True
        )
        graph2.add_to_blender(appear_time = cues['sim']['start'])
        appear_coord = [func[0], func2(func[0]), 0]
        point2 = graph2.add_point_at_coord(
            coord = appear_coord,
            appear_time = cues['sim']['start'],
            axis_projections = True,
            track_curve = 0
        )
        graph2.multi_animate_point(
            start_time = cues['sim']['start'] + start_delay,
            point = point2,
            x_of_t = func, #Not func2. This uses the sim data to inform movements
            frames_per_time_step = sim.frames_per_time_step
        )

        remaining = [sim, graph, graph2]
        for thing in remaining:
            thing.disappear(disappear_time = scene_end)
'''
'''
class ChickenEgg(Scene):
    def __init__(self):
        self.subscenes = collections.OrderedDict([
            ('scene', {'duration': 11.5})
        ])
        super().__init__()

    def play(self):
        super().play()
        cues = self.subscenes
        scene_end = self.duration

        chicken = import_object(
            'chicken',
            scale = 4,
            location = (0, 0, 0)
        )
        chicken.add_to_blender(appear_time = cues['scene']['start'])

        chicken.move_to(
            new_location = [-7, 0, 0],
            start_time = cues['scene']['start'] + 3
        )

        egg = import_object(
            'egg',
            scale = 4,
            location = (7, 0, 0)
        )
        egg.add_to_blender(appear_time = cues['scene']['start'] + 3)

        top_arrow = gesture.Gesture(
            gesture_series = [
                {
                    'type': 'arrow',
                    'points': {
                        'tail': (-1.5, 1.5, 0),
                        'head': (1.5, 1.5, 0)
                    }
                }
            ],
            scale = 2
        )
        top_arrow.add_to_blender(appear_time = cues['scene']['start'] + 4)

        bottom_arrow = gesture.Gesture(
            gesture_series = [
                {
                    'type': 'arrow',
                    'points': {
                        'head': (-1.5, -1.5, 0),
                        'tail': (1.5, -1.5, 0)
                    }
                }
            ],
            scale = 2
        )
        bottom_arrow.add_to_blender(appear_time = cues['scene']['start'] + 4)

        wha = tex_bobject.TexBobject(
            '\\text{?}',
            centered = True,
            location = (0, 0, 0),
            scale = 3
        )
        wha.add_to_blender(appear_time = cues['scene']['start'] + 6)

        remaining = [chicken, egg, top_arrow, bottom_arrow, wha]
        for thing in remaining:
            thing.disappear(disappear_time = scene_end)
'''
'''
class FirstKindOfGraph(Scene):
    def __init__(self):
        self.subscenes = collections.OrderedDict([
            ('one_sim', {'duration': 7}),
            ('two_sims', {'duration': 7}),
            ('three_sims', {'duration': 12})
        ])
        super().__init__()

    def play(self):
        super().play()
        cues = self.subscenes
        scene_end = self.duration

        frames_per_time_step = 5
        start_delay = 0.5
        sim_duration = 60

        initial_creature_count = 10
        initial_creatures = []
        for i in range(initial_creature_count):
            new_creature = creature.Creature()
            initial_creatures.append(new_creature)
        sim = drawn_world.DrawnWorld(
            name = 'blob1_sim',
            location = [-7.5, 0, 0],
            scale = 0.6,
            #appear_time = cues['one_sim']['start'],
            start_delay = start_delay,
            frames_per_time_step = frames_per_time_step,
            #save = True,
            #load = 'wte_eq_replication',
            sim_duration = sim_duration,
            initial_creatures = initial_creatures,
            gene_updates = [
                ['color', 'creature_color_1', 'birth_modifier', 1000, 0],
                ['shape', 'shape1', 'birth_modifier', 1, 0],
                ['size', '1', 'birth_modifier', 1, 0],
                ['color', 'creature_color_1', 'mutation_chance', 0, 0],
                ['shape', 'shape1', 'mutation_chance', 0, 0],
                ['size', '1', 'mutation_chance', 0, 0],
                ['color', 'creature_color_1', 'death_modifier', 100, 0],
                #['color', 'creature_color_1', 'replication_modifier', 10, 0],
            ]
        )
        sim.add_to_blender(appear_time = cues['one_sim']['start'])

        func = sim.get_creature_count_by_t()
        graph = graph_bobject.GraphBobject(
            func,
            x_range = [0, sim_duration],
            y_range = [0, 20],
            tick_step = [20, 5],
            width = 10,
            height = 10,
            x_label = '\\text{Time}',
            x_label_pos = 'along',
            y_label = '\\text{Number}',
            y_label_pos = 'end',
            location = (7, 0, 0),
            centered = True,
            arrows = True
        )
        graph.add_to_blender(appear_time = cues['one_sim']['start'])
        graph.animate_function_curve(
            start_time = cues['one_sim']['start'] + start_delay,
            end_time = cues['one_sim']['start'] + start_delay + sim.animated_duration / FRAME_RATE,
            uniform_along_x = True
        )
        appear_coord = [0, func[0], 0]
        point = graph.add_point_at_coord(
            coord = appear_coord,
            appear_time = 0,
            axis_projections = True,
            track_curve = 0
        )
        graph.animate_point(
            end_coord = [sim_duration, 0, 0],
            start_time = cues['one_sim']['start'] + start_delay,
            end_time = cues['one_sim']['start'] + start_delay + sim.animated_duration / FRAME_RATE,
            point = point
        )

        sim.move_to(
            new_location = (-9, -4.2, 0),
            new_scale = 0.35,
            end_time = cues['one_sim']['end']
        )
        graph.move_to(
            new_location = (-9, 3.7, 0),
            new_scale = 0.6,
            end_time = cues['one_sim']['end']
        )



        #Two sims
        frames_per_time_step = 5
        start_delay = 0.5
        sim_duration = 60

        initial_creature_count = 10
        initial_creatures = []
        for i in range(initial_creature_count):
            new_creature = creature.Creature()
            initial_creatures.append(new_creature)
        sim2 = drawn_world.DrawnWorld(
            name = 'blob1_sim',
            location = [0, -4.2, 0],
            scale = 0.35,
            #appear_time = cues['two_sims']['start'],
            start_delay = start_delay,
            frames_per_time_step = frames_per_time_step,
            #save = True,
            #load = 'wte_eq_replication',
            sim_duration = sim_duration,
            initial_creatures = initial_creatures,
            gene_updates = [
                ['color', 'creature_color_1', 'birth_modifier', 1000, 0],
                ['shape', 'shape1', 'birth_modifier', 1, 0],
                ['size', '1', 'birth_modifier', 1, 0],
                ['color', 'creature_color_1', 'mutation_chance', 0, 0],
                ['shape', 'shape1', 'mutation_chance', 0, 0],
                ['size', '1', 'mutation_chance', 0, 0],
                ['color', 'creature_color_1', 'death_modifier', 100, 0],
                #['color', 'creature_color_1', 'replication_modifier', 10, 0],
            ]
        )
        sim2.add_to_blender(appear_time = cues['two_sims']['start'])

        func2 = sim2.get_creature_count_by_t()
        graph2 = graph_bobject.GraphBobject(
            func2,
            x_range = [0, sim_duration],
            y_range = [0, 20],
            tick_step = [20, 5],
            width = 10,
            height = 10,
            x_label = '\\text{Time}',
            x_label_pos = 'along',
            y_label = '\\text{Number}',
            y_label_pos = 'end',
            location = (0, 3.7, 0),
            centered = True,
            arrows = True,
            scale = 0.6
        )
        graph2.add_to_blender(appear_time = cues['two_sims']['start'])
        graph2.animate_function_curve(
            start_time = cues['two_sims']['start'] + start_delay,
            end_time = cues['two_sims']['start'] + start_delay + sim2.animated_duration / FRAME_RATE,
            uniform_along_x = True
        )
        appear_coord = [0, func2[0], 0]
        point = graph2.add_point_at_coord(
            coord = appear_coord,
            appear_time = 0,
            axis_projections = True,
            track_curve = 0
        )
        graph2.animate_point(
            end_coord = [sim_duration, 0, 0],
            start_time = cues['two_sims']['start'] + start_delay,
            end_time = cues['two_sims']['start'] + start_delay + sim2.animated_duration / FRAME_RATE,
            point = point
        )

        #Three sims
        frames_per_time_step = 5
        start_delay = 0.5
        sim_duration = 60

        initial_creature_count = 10
        initial_creatures = []
        for i in range(initial_creature_count):
            new_creature = creature.Creature()
            initial_creatures.append(new_creature)
        sim3 = drawn_world.DrawnWorld(
            name = 'blob1_sim',
            location = [9, -4.2, 0],
            scale = 0.35,
            #appear_time = cues['three_sims']['start'],
            start_delay = start_delay,
            frames_per_time_step = frames_per_time_step,
            #save = True,
            #load = 'wte_eq_replication',
            sim_duration = sim_duration,
            initial_creatures = initial_creatures,
            gene_updates = [
                ['color', 'creature_color_1', 'birth_modifier', 1000, 0],
                ['shape', 'shape1', 'birth_modifier', 1, 0],
                ['size', '1', 'birth_modifier', 1, 0],
                ['color', 'creature_color_1', 'mutation_chance', 0, 0],
                ['shape', 'shape1', 'mutation_chance', 0, 0],
                ['size', '1', 'mutation_chance', 0, 0],
                ['color', 'creature_color_1', 'death_modifier', 100, 0],
                #['color', 'creature_color_1', 'replication_modifier', 10, 0],
            ]
        )
        sim3.add_to_blender(appear_time = cues['three_sims']['start'])

        func3 = sim3.get_creature_count_by_t()
        graph3 = graph_bobject.GraphBobject(
            func3,
            x_range = [0, sim_duration],
            y_range = [0, 20],
            tick_step = [20, 5],
            width = 10,
            height = 10,
            x_label = '\\text{Time}',
            x_label_pos = 'along',
            y_label = '\\text{Number}',
            y_label_pos = 'end',
            location = (9, 3.7, 0),
            centered = True,
            arrows = True,
            scale = 0.6
        )
        graph3.add_to_blender(appear_time = cues['three_sims']['start'])
        graph3.animate_function_curve(
            start_time = cues['three_sims']['start'] + start_delay,
            end_time = cues['three_sims']['start'] + start_delay + sim3.animated_duration / FRAME_RATE,
            uniform_along_x = True
        )
        appear_coord = [0, func3[0], 0]
        point = graph3.add_point_at_coord(
            coord = appear_coord,
            appear_time = 0,
            axis_projections = True,
            track_curve = 0
        )
        graph3.animate_point(
            end_coord = [sim_duration, 0, 0],
            start_time = cues['three_sims']['start'] + start_delay,
            end_time = cues['three_sims']['start'] + start_delay + sim3.animated_duration / FRAME_RATE,
            point = point
        )

        remaining = [sim, graph, sim2, graph2, sim3, graph3]
        for thing in remaining:
            thing.disappear(disappear_time = scene_end)
'''
'''
class FunctionTime(Scene):
    def __init__(self):
        self.subscenes = collections.OrderedDict([
            ('graph', {'duration': 25}),
        ])
        super().__init__()

    def play(self):
        super().play()
        cues = self.subscenes
        scene_end = self.duration

        def func(x):
            return 3 + 2 * x - x * x / 1.55 + x ** 3 / 20

        graph = graph_bobject.GraphBobject(
            func,
            x_range = [0, 10],
            y_range = [0, 10],
            tick_step = [5, 5],
            width = 10,
            height = 10,
            x_label = 'x',
            x_label_pos = 'end',
            y_label = 'y',
            y_label_pos = 'end',
            location = (0, -1, 0),
            centered = True,
            arrows = True
        )
        graph.add_to_blender(appear_time = cues['graph']['start'] + 2)
        arrow = gesture.Gesture(
            gesture_series = [
                {
                    'type': 'arrow',
                    'points': {
                        'head': (-3, 5.3, 0),
                        'tail': (0, 5.3, 0)
                    }
                },
                {
                    'type': 'arrow',
                    'points': {
                        'head': (6.5, -4, 0),
                        'tail': (6.5, -1, 0)
                    }
                }
            ],
            color = 'color2'
        )
        arrow.add_to_blender(appear_time = cues['graph']['start'] + 6)
        graph.y_label_bobject.pulse(
            time = cues['graph']['start'] + 6,
            duration = 120
        )
        graph.y_label_bobject.subbobjects[0].color_shift(
            start_time = cues['graph']['start'] + 6,
            duration = 120,
            color = COLORS_SCALED[3],
            #shift_time = OBJECT_APPEARANCE_TIME / 2
        )
        arrow.morph_figure(1, start_time = cues['graph']['start'] + 8)
        graph.x_label_bobject.pulse(
            time = cues['graph']['start'] + 8,
            duration = 240
        )
        graph.x_label_bobject.subbobjects[0].color_shift(
            start_time = cues['graph']['start'] + 8,
            duration = 240,
            color = COLORS_SCALED[3],
            #shift_time = OBJECT_APPEARANCE_TIME / 2
        )

        graph.move_to(
            new_location = (-7.5, -1, 0),
            start_time = cues['graph']['start'] + 13
        )
        arrow.disappear(
            disappear_time = cues['graph']['start'] + 13
        )

        func_eq = tex_bobject.TexBobject(
            'y = f(x)',
            location = (7.5, 3, 0),
            centered = True,
            scale = 2
        )
        func_eq.add_to_blender(
            appear_time = cues['graph']['start'] + 17
        )

        x_step = 0.1
        x = 0
        x_values = []
        y_values = []
        while x <= 10:
            x_values.append(str(x))
            x += x_step
            x = round(x, 1)
            y = round(func(x), 1)
            y_values.append(str(y))

        x = tex_bobject.TexBobject(
            *x_values,
            location = (10.2, -3, 0),
            transition_type = 'instant',
            centered = True,
            scale = 2,
            color = 'color2'
        )
        x.add_to_blender(
            appear_time = cues['graph']['start'] + 19
        )
        x_arrow = gesture.Gesture(
            gesture_series = [
                {
                    'type': 'arrow',
                    'points': {
                        'tail': (10.2, -1.5, 0),
                        'head': (10.2, 1, 0)
                    }
                }
            ],
            color = 'color2'
        )
        x_arrow.add_to_blender(appear_time = cues['graph']['start'] + 19)

        y = tex_bobject.TexBobject(
            *y_values,
            location = (4, -3, 0),
            transition_type = 'instant',
            centered = True,
            scale = 2,
            color = 'color2'
        )
        y.add_to_blender(
            appear_time = cues['graph']['start'] + 20
        )
        y_arrow = gesture.Gesture(
            gesture_series = [
                {
                    'type': 'arrow',
                    'points': {
                        'head': (4, -1.5, 0),
                        'tail': (4, 1, 0)
                    }
                }
            ],
            color = 'color2'
        )
        y_arrow.add_to_blender(appear_time = cues['graph']['start'] + 20)

        graph.animate_function_curve(
            start_time = cues['graph']['start'] + 21,
            end_time = cues['graph']['start'] + 23,
            uniform_along_x = True
        )
        appear_coord = [0, func(0), 0]
        point = graph.add_point_at_coord(
            coord = appear_coord,
            appear_time = cues['graph']['start'] + 20,
            axis_projections = True,
            track_curve = 0
        )
        graph.animate_point(
            end_coord = [10, 0, 0],
            start_time = cues['graph']['start'] + 21,
            end_time = cues['graph']['start'] + 23,
            point = point
        )

        start_time = cues['graph']['start'] + 21
        end_time = cues['graph']['start'] + 23
        time_step = (end_time - start_time) / (len(x_values) - 1)
        for i in range(1, len(x_values)):
            x.morph_figure(i, start_time = start_time + i * time_step)
            y.morph_figure(i, start_time = start_time + i * time_step)

        remaining = [graph, func_eq, x, y, x_arrow, y_arrow]
        for thing in remaining:
            thing.disappear(disappear_time = scene_end)
'''
'''
class EquationToFunction(Scene):
    def __init__(self):
        self.subscenes = collections.OrderedDict([
            ('sim', {'duration': 24.5}),
            ('equation', {'duration': 24}),
        ])
        super().__init__()

    def play(self):
        super().play()
        cues = self.subscenes
        scene_end = self.duration

        #Equation
        lhs = tex_bobject.TexBobject(
            "\\text{Birth rate}",
            "\\text{Birth rate} - \\text{Death rate}",
            #"B",
            #"\\dfrac{B}{D}",
            centered = True
        )
        equals = tex_bobject.TexBobject(
            "\!=",
            #"\!<",
            #"\!=",
            #"\!>",
            #"\!=",
            centered = True
        )
        rhs = tex_bobject.TexBobject(
            "\\text{Death rate}",
            "0",
            #"\\text{Number} \\times \\text{Death rate per creature}",
            #"\\text{Number} \\times 0.1",
            #"\\text{Number} \\times \\text{Death rate per creature}",
            #N \\times D",
            #"\\dfrac{N \\times D}{D}",
            #"N",
            centered = True
        )
        equation = tex_complex.TexComplex(
            lhs, equals, rhs,
            centered = True,
            location = (0, 0, 0),
            scale = 1.5
        )

        equation.add_to_blender(
            appear_time = cues['sim']['start'] + 3,
            animate = False,
            subbobject_timing = [0, 60, 120]
        )

        equation.move_to(
            new_location = (0, 6.5, 0),
            #new_scale = 1,
            start_time = cues['sim']['start'] + 5.5
        )

        start_delay = 0.5
        sim_duration = 246
        #frames_per_time_step = 5
        #sim_duration_frames = sim_duration * frames_per_time_step

        initial_creature_count = 10
        initial_creatures = []
        for i in range(initial_creature_count):
            new_creature = creature.Creature()
            initial_creatures.append(new_creature)
        sim = drawn_world.DrawnWorld(
            name = 'blob1_sim',
            location = [0, -1.5, 0],
            scale = 0.6,
            #appear_time = cues['sim']['start'] + 180,
            start_delay = start_delay,
            frames_per_time_step = 10,
            #save = True,
            load = 'ro_equation_to_function',
            sim_duration = sim_duration,
            initial_creatures = initial_creatures,
            gene_updates = [
                ['color', 'creature_color_1', 'birth_modifier', 0, 0],
                ['shape', 'shape1', 'birth_modifier', 1, 0],
                ['size', '1', 'birth_modifier', 1, 0],
                ['color', 'creature_color_1', 'death_modifier', 0, 0],
                ['color', 'creature_color_1', 'replication_modifier', 0, 0],
                ['color', 'creature_color_1', 'death_modifier', 500, 13],
                ['color', 'creature_color_1', 'birth_modifier', 5000, 14],
                ['color', 'creature_color_1', 'death_modifier', 0, 14],
                ['color', 'creature_color_1', 'birth_modifier', 0, 15],
                ['color', 'creature_color_1', 'death_modifier', 10, 21],
                ['color', 'creature_color_1', 'birth_modifier', 100, 21],
            ],
            pauses = [
                #[9, 5], #pause
                [14, 15], #show death
                #[15, 8], #show life
                #[12] #carry on
            ]
        )
        sim.add_to_blender(appear_time = cues['sim']['start'] + 5.5)

        #Manipulate equation
        lhs.morph_figure(1, start_time = cues['equation']['start'])
        rhs.morph_figure(1, start_time = cues['equation']['start'])

        equals2 = tex_bobject.TexBobject(
            "\!=",
            centered = True
        )
        slhs = tex_bobject.TexBobject(
            "\\Delta",
            centered = True
        )
        #equals2.superbobject = equation
        #slhs.superbobject = equation
        #equals2.ref_obj.parent = equation.ref_obj
        #slhs.ref_obj.parent = equation.ref_obj
        equation.add_tex_bobject(equals2, index = 0)
        equation.add_tex_bobject(slhs, index = 0)
        equals2.add_to_blender(appear_time = cues['equation']['start'] + 1.25)
        slhs.add_to_blender(appear_time = cues['equation']['start'] + 1.25)
        #equation.subbobjects = [slhs, equals2, lhs, equals, rhs]
        equation.arrange_tex_bobjects(start_time = cues['equation']['start'] + 1.25)
        tot = tex_bobject.TexBobject(
            "\\text{Total}",
            centered = True,
            color = 'color2'
        )
        exp = tex_bobject.TexBobject(
            "\\text{expected}",
            centered = True,
            color = 'color2'
        )
        cha = tex_bobject.TexBobject(
            "\\text{change}",
            centered = True,
            color = 'color2'
        )
        total_change_annotation = tex_complex.TexComplex(
            tot, exp, cha,
            location = (-11.5, 0, 0),
            centered = True,
            scale = 1,
            multiline = True,
            color = 'color2'
        )
        total_change_annotation.add_to_blender(
            appear_time = cues['equation']['start'] + 4
        )
        arrow = gesture.Gesture(
            gesture_series = [
                {
                    'type': 'arrow',
                    'points': {
                        'tail': (-11.5, 2.2, 0),
                        'head': (-11.5, 5.2, 0)
                    }
                },
                {
                    'type': 'arrow',
                    'points': {
                        'tail': (-11, 2.2, 0),
                        'head': (-10.25, 5.2, 0)
                    }
                }
            ],
            color = 'color2'
        )
        arrow.add_to_blender(
            appear_time = cues['equation']['start'] + 4
        )
        birth_rate_bobjs = []
        for i in range(0, 9):
            birth_rate_bobjs.append(lhs.lookup_table[0][i])
        for bobj in birth_rate_bobjs:
            bobj.color_shift(
                color = COLORS_SCALED[3],
                start_time = cues['equation']['start'] + 6,
                duration = 90
            )
        death_rate_bobjs = []
        for i in range(10, 19):
            death_rate_bobjs.append(lhs.lookup_table[1][i])
        for bobj in death_rate_bobjs:
            bobj.color_shift(
                color = COLORS_SCALED[3],
                start_time = cues['equation']['start'] + 7.5,
                duration = 90
            )
        delta = slhs.lookup_table[0][0]
        delta.color_shift(
            color = COLORS_SCALED[3],
            start_time = cues['equation']['start'] + 9,
            duration = 120
        )
        eq = equals.lookup_table[0][0]
        eq.color_shift(
            color = COLORS_SCALED[3],
            start_time = cues['equation']['start'] + 12,
            duration = None
        )
        zero = rhs.lookup_table[0][0]
        zero.color_shift(
            color = COLORS_SCALED[3],
            start_time = cues['equation']['start'] + 12,
            duration = None
        )

        equals.disappear(disappear_time = cues['equation']['start'] + 16)
        rhs.disappear(disappear_time = cues['equation']['start'] + 16)

        equation.subbobjects = [slhs, equals2, lhs]
        equation.arrange_tex_bobjects(
            start_time = cues['equation']['start'] + 16,
            end_time = cues['equation']['start'] + 16 + 0.5
        )
        arrow.morph_figure(1, start_time = cues['equation']['start'] + 16)


        to_disappear = [sim, arrow, total_change_annotation]
        for thing in to_disappear:
            thing.disappear(disappear_time = scene_end)
'''
'''
class InTermsOfN(Scene):
    def __init__(self):
        self.subscenes = collections.OrderedDict([
            ('graph', {'duration': 16}),
            ('birth_rate', {'duration': 13}),
            ('death_rate', {'duration': 8}),
            ('condense', {'duration': 24}),
        ])
        super().__init__()

    def play(self):
        super().play()
        cues = self.subscenes
        scene_end = self.duration

        rhs = tex_bobject.TexBobject(
            "\\text{Birth rate} - \\text{Death rate}",
            "f(N)",
            "\\text{Birth rate} - \\text{Death rate}",
            "B + R \\times N - \\text{Death rate}",
            "B + R \\times N - \\text{Death rate}",
            "B + R \\times N - \\text{Death rate}",
            "B + R \\times N - D \\times N",
            "B + R \\times N - D \\times N",
            "B + (R-D) \\times N",
            "B + (R-D) \\times N",
            "B + (R-D) \\times N",
            "B + (R-D) \\times N",
            centered = True
        )
        equals = tex_bobject.TexBobject(
            "\!=",
            centered = True
        )
        lhs = tex_bobject.TexBobject(
            "\\Delta",
            "\\Delta",
            "\\Delta",
            centered = True
        )

        equation = tex_complex.TexComplex(
            lhs, equals, rhs,
            location = (0, 6.5, 0),
            scale = 1.5,
            centered = True
        )


        equation.add_annotation( #Total birth rate
            targets = [
                2, #tex_bobject
                [
                    [0, 0, 0, None],  #form, first char, last char
                    [1, 0, 0, None],
                    [2, 0, 4, None],
                    [3, 0, 4],
                    [4, 0, 4],
                    [5, 0, 4],
                    [6, 0, 4],
                    [7, 0, 4, None],
                    [8, 0, 4, None],
                    [9, 0, 4, None],
                    [10, 0, 4, None],
                    [11, 0, 4, None],
                ],
            ],
            labels = [
                [],
                [],
                [],
                ['\\text{Total}', '\\text{birth rate} \\phantom{blurghh}'],
                ['\\text{Total}', '\\text{birth rate} \\phantom{blurghh}'],
                ['\\text{Total}', '\\text{birth rate} \\phantom{blurghh}'],
                ['\\text{Total}', '\\text{birth rate} \\phantom{blurghh}'],
                [],
                [],
                [],
                [],
                [],
            ],
            alignment = 'top'
        )
        equation.add_annotation( #Net expected change
            targets = [
                2, #tex_bobject
                [
                    [0, 0, 0, None],  #form, first char, last char
                    [1, 0, 0, None],
                    [2, 0, 0, None],
                    [3, 0, 0, None],
                    [4, 0, 0, None],
                    [5, 0, 0, None],
                    [6, 0, 0, None],
                    [7, 0, 0, None],
                    [8, 2, 6, None],
                    [9, 2, 6],
                    [10, 2, 6],
                    [11, 2, 6],
                ],
            ],
            labels = [
                [],
                [],
                [],
                [],
                [],
                [],
                [],
                [],
                [],
                ['\\text{Net expected}', '\\text{change per}', '\\text{creature}'],
                ['\\text{Net expected}', '\\text{change per}', '\\text{creature}'],
                ['\\text{Net expected}', '\\text{change per}', '\\text{creature}'],
            ],
            alignment = 'top'
        )
        equation.add_annotation( #Spontaneous birth rate
            targets = [
                2, #tex_bobject
                [
                    [0, 0, 0, None],
                    [1, 0, 0, None],
                    [2, 0, 0, None],
                    [3, 0, 0, None],
                    [4, 0, 0],
                    [5, 0, 0],
                    [6, 0, 0],
                    [7, 0, 0],
                    [8, 0, 0],
                    [9, 0, 0],
                    [10, 0, 0],
                    [11, 0, 0],
                ],
            ],
            labels = [
                [],
                [],
                [],
                [],
                ['\\text{Spontaneous}', '\\text{birth rate} \\phantom{blurghh}'],
                ['\\text{Spontaneous}', '\\text{birth rate} \\phantom{blurghh}'],
                ['\\text{Spontaneous}', '\\text{birth rate} \\phantom{blurghh}'],
                ['\\text{Spontaneous}', '\\text{birth rate} \\phantom{blurghh}'],
                ['\\text{Spontaneous}', '\\text{birth rate} \\phantom{blurghh}'],
                ['\\text{Spontaneous}', '\\text{birth rate} \\phantom{blurghh}'],
                ['\\text{Spontaneous}', '\\text{birth rate} \\phantom{blurghh}'],
                ['\\text{Spontaneous}', '\\text{birth rate} \\phantom{blurghh}'],
            ],
            alignment = 'bottom',
            angle = math.pi / 4
        )
        equation.add_annotation( #Replication rate
            targets = [
                2, #tex_bobject
                [
                    [0, 0, 0, None],
                    [1, 0, 0, None],
                    [2, 0, 0, None],
                    [3, 0, 0, None],
                    [4, 2, 4, None],
                    [5, 2, 4],
                    [6, 2, 4],
                    [7, 1, 1, None],
                    [8, 1, 1, None],
                    [9, 1, 1, None],
                    [10, 1, 1, None],
                    [11, 1, 1, None],
                ],
            ],
            labels = [
                [],
                [],
                [],
                [],
                [],
                ['\\text{Replication}', '\\text{rate}'],
                ['\\text{Replication}', '\\text{rate}'],
                [],
                [],
                [],
                [],
                [],
            ],
            alignment = 'bottom'
        )
        equation.add_annotation( #Number of creatures
            targets = [
                2, #tex_bobject
                [
                    [0, 0, 0, None],
                    [1, 0, 0, None],
                    [2, 0, 0, None],
                    [3, 0, 0, None],
                    [4, 0, 0, None],
                    [5, 0, 0, None],
                    [6, 0, 0, None],
                    [7, 0, 0, None],
                    [8, 0, 0, None],
                    [9, 0, 0, None],
                    [10, 8, 8],
                    [11, 8, 8, None],
                ],
            ],
            labels = [
                [],
                [],
                [],
                [],
                [],
                [],
                [],
                [],
                [],
                [],
                ['\\text{Number}', '\\text{of creatures}'],
                [],
            ],
            alignment = 'bottom'
        )
        equation.add_annotation( #Total death rate
            targets = [
                2, #tex_bobject
                [
                    [0, 0, 0, None],
                    [1, 0, 0, None],
                    [2, 0, 0, None],
                    [3, 0, 0, None],
                    [4, 6, 10, None],
                    [5, 6, 10, None],
                    [6, 6, 8],
                    [7, 6, 8, None],
                    [8, 0, 0, None],
                    [9, 0, 0, None],
                    [10, 0, 0, None],
                    [11, 0, 0, None],
                ],
            ],
            labels = [
                [],
                [],
                [],
                [],
                [],
                [],
                ['\\text{total}', '\\text{death rate}'],
                [],
                [],
                [],
                [],
                [],
            ],
            alignment = 'top'
        )
        equation.add_annotation( #Total expected change
            targets = [
                0, #tex_bobject
                [
                    [0, 0, 0, None],
                    [1, 0, 0],
                    [2, 0, 0, None],
                ],
            ],
            labels = [
                [],
                ['\\text{Total}', '\\text{expected}', '\\text{change}'],
                [],
            ],
            alignment = 'top'
        )

        equation.add_to_blender(
            appear_time = cues['graph']['start'] - 0.5,
            animate = False
        )

        graph = graph_bobject.GraphBobject(
            #func,
            x_range = [0, 10],
            y_range = [0, 10],
            tick_step = [None, None],
            width = 9,
            height = 9,
            x_label = 'N',
            x_label_pos = 'end',
            y_label = '\\Delta',
            y_label_pos = 'end',
            location = (0, -2, 0),
            centered = True,
            arrows = True,
        )
        graph.add_to_blender(appear_time = cues['graph']['start'] + 2)

        deltas = [lhs.lookup_table[0][0], graph.y_label_bobject.subbobjects[0]]
        for delta in deltas:
            delta.pulse(
                time = cues['graph']['start'] + 4,
                duration = 120
            )
            delta.color_shift(
                start_time = cues['graph']['start'] + 4,
                duration = 120,
                #shift_time = OBJECT_APPEARANCE_TIME / 2,
                color = COLORS_SCALED[3]
            )

        rhs.morph_figure(1, start_time = cues['graph']['start'] + 9)

        Ns = [rhs.lookup_table[1][2], graph.x_label_bobject.subbobjects[0]]

        for N in Ns:
            N.pulse(
                time = cues['graph']['start'] + 10,
                duration = 120
            )
            N.color_shift(
                start_time = cues['graph']['start'] + 10,
                duration = 120,
                #shift_time = OBJECT_APPEARANCE_TIME / 2,
                color = COLORS_SCALED[3]
            )

        rhs.morph_figure(2, start_time = cues['graph']['end'])

        graph.disappear(disappear_time = cues['graph']['end'] + 0.5)
        equation.move_to(
            new_location = (0, 0, 0),
            start_time = cues['graph']['end']
        )

        rhs.morph_figure(3, start_time = cues['birth_rate']['start'] + 1)
        rhs.morph_figure(4, start_time = cues['birth_rate']['start'] + 2.25)

        B = rhs.lookup_table[2][0]
        B.pulse(
            time = cues['birth_rate']['start'] + 2.25,
            duration = 120
        )
        B.color_shift(
            start_time = cues['birth_rate']['start'] + 2.25,
            duration = 120,
            #shift_time = OBJECT_APPEARANCE_TIME / 2,
            color = COLORS_SCALED[3]
        )
        rhs.morph_figure(5, start_time = cues['birth_rate']['start'] + 5.5)

        R = rhs.lookup_table[2][2]
        R.pulse(
            time = cues['birth_rate']['start'] + 7.5,
            duration = 120
        )
        R.color_shift(
            start_time = cues['birth_rate']['start'] + 7.5,
            duration = 120,
            #shift_time = OBJECT_APPEARANCE_TIME / 2,
            color = COLORS_SCALED[3]
        )
        N = rhs.lookup_table[2][4]
        N.pulse(
            time = cues['birth_rate']['start'] + 11.5,
            duration = 120
        )
        N.color_shift(
            start_time = cues['birth_rate']['start'] + 11.5,
            duration = 120,
            shift_time = OBJECT_APPEARANCE_TIME / 2,
            color = COLORS_SCALED[3]
        )


        #Death rate
        rhs.morph_figure(6, start_time = cues['death_rate']['start'] + 1.5)

        D = rhs.lookup_table[4][6]
        D.pulse(
            time = cues['death_rate']['start'] + 3,
            duration = 120
        )
        D.color_shift(
            start_time = cues['death_rate']['start'] + 3,
            duration = 120,
            #shift_time = OBJECT_APPEARANCE_TIME / 2,
            color = COLORS_SCALED[3]
        )
        N = rhs.lookup_table[4][8]
        N.pulse(
            time = cues['death_rate']['start'] + 5.5,
            duration = 120
        )
        N.color_shift(
            start_time = cues['death_rate']['start'] + 5.5,
            duration = 120,
            #shift_time = OBJECT_APPEARANCE_TIME / 2,
            color = COLORS_SCALED[3]
        )

        #Condense
        rhs.morph_figure(7, start_time = cues['condense']['start'] + 0)
        rhs.morph_figure(8, start_time = cues['condense']['start'] + 1)
        R = rhs.lookup_table[8][3]
        R.pulse(
            time = cues['condense']['start'] + 4.5,
            duration = 60
        )
        R.color_shift(
            start_time = cues['condense']['start'] + 4.5,
            duration = 60,
            #shift_time = OBJECT_APPEARANCE_TIME / 2,
            color = COLORS_SCALED[3]
        )
        D = rhs.lookup_table[8][5]
        D.pulse(
            time = cues['condense']['start'] + 5,
            duration = 60
        )
        D.color_shift(
            start_time = cues['condense']['start'] + 5,
            duration = 60,
            #shift_time = OBJECT_APPEARANCE_TIME / 2,
            color = COLORS_SCALED[3]
        )
        R.pulse(
            time = cues['condense']['start'] + 5.5,
            duration = 60
        )
        R.color_shift(
            start_time = cues['condense']['start'] + 5.5,
            duration = 60,
            #shift_time = OBJECT_APPEARANCE_TIME / 2,
            color = COLORS_SCALED[3]
        )
        D.pulse(
            time = cues['condense']['start'] + 6,
            duration = 60
        )
        D.color_shift(
            start_time = cues['condense']['start'] + 6,
            duration = 60,
            #shift_time = OBJECT_APPEARANCE_TIME / 2,
            color = COLORS_SCALED[3]
        )
        rhs.morph_figure(9, start_time = cues['condense']['start'] + 7)

        rhs.morph_figure(10, start_time = cues['condense']['start'] + 18)
        lhs.morph_figure(1, start_time = cues['condense']['start'] + 21 )
        lhs.morph_figure(2, start_time = cues['condense']['end'] - 0.5)
        rhs.morph_figure(11, start_time = cues['condense']['end'] - 0.5)

        equation.move_to(
            new_location = (7.5, 0, 0),
            new_scale = 1,
            start_time = cues['condense']['end'] - 0.5
        )

        """to_disappear = [
            total_change_annotation,
            tot_arrow,
            num_annotation,
            num_arrow
        ]
        for bobj in to_disappear:
            bobj.disappear(disappear_time = cues['condense']['start'] + 5)"""

        graph = graph_bobject.GraphBobject(
            #func,
            x_range = [0, 10],
            y_range = [-1, 2],
            tick_step = [5, 1],
            width = 10,
            height = 10,
            x_label = 'N',
            x_label_pos = 'end',
            y_label = '\\Delta',
            y_label_pos = 'end',
            location = (-7.5, -1, 0),
            centered = True,
            arrows = True,
        )
        graph.add_to_blender(appear_time = cues['condense']['end'] - 0.5)

        """Ns = [rhs.lookup_table[5][8], graph.x_label_bobject.subbobjects[0]]

        for N in Ns:
            N.pulse(
                frame = cues['condense']['start'] + 360,
                duration = 60
            )
            N.color_shift(
                start_frame = cues['condense']['start'] + 360,
                duration = 60,
                shift_time = OBJECT_APPEARANCE_TIME / 2,
                color = COLORS_SCALED[3]
            )

        deltas = [lhs.lookup_table[0][0], graph.y_label_bobject.subbobjects[0]]
        for delta in deltas:
            delta.pulse(
                frame = cues['condense']['start'] + 420,
                duration = 60
            )
            delta.color_shift(
                start_frame = cues['condense']['start'] + 420,
                duration = 60,
                shift_time = OBJECT_APPEARANCE_TIME / 2,
                color = COLORS_SCALED[3]
            )"""
'''
'''
class FirstRateCurve(Scene):
    def __init__(self):
        self.subscenes = collections.OrderedDict([
            ('graph', {'duration': 53}),
            ('ntgraph', {'duration': 20.5}),
        ])
        super().__init__()

    def play(self):
        super().play()
        cues = self.subscenes
        scene_end = self.duration

        def func(x):
            return 1 - 0.2 * x

        graph = graph_bobject.GraphBobject(
            func,
            x_range = [0, 10],
            y_range = [-1, 2],
            tick_step = [5, 1],
            width = 10,
            height = 10,
            x_label = 'N',
            x_label_pos = 'end',
            y_label = '\\Delta',
            y_label_pos = 'end',
            location = (-7.5, -1, 0),
            centered = True,
            arrows = True,
        )
        graph.add_to_blender(appear_time = cues['graph']['start'] - 0.5)

        rhs = tex_bobject.TexBobject(
            "B + (R-D) \\times N",
            "1 + (R-D) \\times N",
            "1 + (R-0.2) \\times N",
            "1 + (0-0.2) \\times N",
            "1 + (0-0.2) \\times N",
            "1 + (0-0.2) \\times N",
            centered = True
        )
        equals = tex_bobject.TexBobject(
            "\!=",
            centered = True
        )
        lhs = tex_bobject.TexBobject(
            "\\Delta",
            centered = True
        )
        equation = tex_complex.TexComplex(
            lhs, equals, rhs,
            location = (7.5, 0, 0),
            scale = 1,
            centered = True
        )
        equation.add_annotation(
            targets = [
                2, #tex_bobject
                [
                    [0, 0, 0],  #form, first char, last char
                    [1, 0, 0],
                    [2, 0, 0],
                    [3, 0, 0],
                    [4, 0, 0, None],
                    [5, 0, 0],
                ],
            ],
            labels = [
                ['\\text{Spontaneous}', '\\text{birth rate} \\phantom{blurghh}'],
                ['\\text{Spontaneous}', '\\text{birth rate} \\phantom{blurghh}'],
                ['\\text{Spontaneous}', '\\text{birth rate} \\phantom{blurghh}'],
                ['\\text{Spontaneous}', '\\text{birth rate} \\phantom{blurghh}'],
                [],
                ['\\text{Spontaneous}', '\\text{birth rate} \\phantom{blurghh}'],
            ],
            alignment = 'bottom',
            angle = math.pi / 4
        )
        equation.add_annotation(
            targets = [
                2, #tex_bobject
                [
                    [0, 2, 6],  #form, first char, last char
                    [1, 2, 6],
                    [2, 2, 8],
                    [3, 3, 3],
                    [4, 3, 3, None],
                    [5, 3, 3],
                ],
            ],
            labels = [
                ['\\text{Net expected}', '\\text{change per}', '\\text{creature}'],
                ['\\text{Net expected}', '\\text{change per}', '\\text{creature}'],
                ['\\text{Net expected}', '\\text{change per}', '\\text{creature}'],
                ['\\text{Replication chance}', '\\text{per creature}'],
                [],
                ['\\text{Replication chance}', '\\text{per creature}'],
            ],
            alignment = 'top'
        )
        equation.add_annotation(
            targets = [
                2, #tex_bobject
                [
                    [0, 5, 5, None],  #form, first char, last char
                    [1, 5, 5, None],
                    [2, 5, 7, 'arrow'],
                    [3, 5, 7, 'arrow'],
                    [4, 5, 7, None],
                    [5, 5, 7, 'arrow'],
                ],
            ],
            labels = [
                [],
                [],
                ['\\text{Death chance}', '\\text{per creature}'],
                ['\\text{Death chance}', '\\text{per creature}'],
                [],
                ['\\text{Death chance}', '\\text{per creature}'],
            ],
            alignment = 'bottom'
        )
        equation.add_to_blender(
            appear_time = cues['graph']['start'] - OBJECT_APPEARANCE_TIME,
            animate = False
        )

        #Morph to example
        rhs.morph_figure(1, start_time = cues['graph']['start'] + 5.5)
        rhs.morph_figure(2, start_time = cues['graph']['start'] + 12.5)
        rhs.morph_figure(3, start_time = cues['graph']['start'] + 19)

        appear_coord = [0, 0, 0]
        point = graph.add_point_at_coord(
            coord = appear_coord,
            appear_time = cues['graph']['start'] + 26,
            axis_projections = True,
            track_curve = 0
        )
        sbr = rhs.lookup_table[3][0]
        sbr.color_shift(
            start_time = cues['graph']['start'] + 28.5,
            #duratino = 120
        )
        graph.animate_function_curve(
            start_time = cues['graph']['start'] + 30.5,
            end_time = cues['graph']['start'] + 35,
            uniform_along_x = True,
            index = 0
        )
        graph.animate_point(
            end_coord = [10, 0, 0],
            start_time = cues['graph']['start'] + 30.5,
            end_time = cues['graph']['start'] + 35,
            point = point
        )
        ncpc = []
        for i in range(2, 9):
            ncpc.append(rhs.lookup_table[3][i])
        for bobj in ncpc:
            bobj.color_shift(
                start_time = cues['graph']['start'] + 33
            )

        graph.animate_point(
            end_coord = [5, 0, 0],
            start_time = cues['graph']['start'] + 35.5,
            end_time = cues['graph']['start'] + 36,
            point = point
        )
        eq_arrow = gesture.Gesture(
            gesture_series = [
                {
                    'type': 'arrow',
                    'points': {
                        'tail': (-7, 0, 0),
                        'head': (-7.4, -1.8, 0)
                    }
                },
                {
                    'type': 'arrow',
                    'points': {
                        'tail': (-7, -1.5, 0),
                        'head': (-7.4, -3.3, 0)
                    }
                },
                {
                    'type': 'arrow',
                    'points': {
                        'tail': (-9.5, -1.1, 0),
                        'head': (-9.9, -2.9, 0)
                    }
                },
                {
                    'type': 'arrow',
                    'points': {
                        'tail': (-7, 0, 0),
                        'head': (-7.4, -1.8, 0)
                    }
                }
            ],
            color = 'color2'
        )
        eq_arrow.add_to_blender(
            appear_time = cues['graph']['start'] + 36
        )
        equilibrium = tex_bobject.TexBobject(
            '\\substack{\\text{Equilibrium} \\\\ \\text{point}}',
            '\\substack{\\text{"Stable"} \\\\ \\text{Equilibrium} \\\\ \\text{point}}',
            location = (-6.8, 1.2, 0),
            centered = True,
            color = 'color2'
        )
        equilibrium.add_to_blender(appear_time = cues['graph']['start'] + 39.5)

        #Below equilibrium
        graph.animate_point(
            end_coord = [2.5, 0, 0],
            start_time = cues['graph']['start'] + 40,# 48,
            end_time = cues['graph']['start'] + 40.5,#48.5,
            point = point,
            track_curve = False
        )
        graph.animate_point(
            end_coord = [2.5, 0.5, 0],
            start_time = cues['graph']['start'] + 41.5, #50,
            end_time = cues['graph']['start'] + 42, #50.5,
            point = point,
            track_curve = False
        )
        graph.animate_point(
            end_coord = [5, 0, 0],
            start_time = cues['graph']['start'] + 42.5,#53,
            end_time = cues['graph']['start'] + 43,#53.5,
            point = point,
            track_curve = 0
        )
        #Above equilibrium
        graph.animate_point(
            end_coord = [7.5, 0, 0],
            start_time = cues['graph']['start'] + 43.5,#56,
            end_time = cues['graph']['start'] + 44,#56.5,
            point = point,
            track_curve = False
        )
        graph.animate_point(
            end_coord = [7.5, -0.5, 0],
            start_time = cues['graph']['start'] + 44.5,#57.5,
            end_time = cues['graph']['start'] + 45,#58,
            point = point,
            track_curve = False
        )
        graph.animate_point(
            end_coord = [5, 0, 0],
            start_time = cues['graph']['start'] + 45.5,#59,
            end_time = cues['graph']['start'] + 46,#59.5,
            point = point,
            track_curve = 0
        )

        stable = tex_bobject.TexBobject(
            '\\text{"Stable"}',
            location = (-6.8, 2.5, 0),
            centered = True,
            scale = 0.67,
            color = 'color2'
        )
        stable.add_to_blender(appear_time = cues['graph']['start'] + 46.5)#65)

        x_of_t = [4, 6, 4, 6, 5]
        graph.multi_animate_point(
            point = point,
            x_of_t = x_of_t,
            frames_per_time_step = 60,
            start_time = cues['graph']['start'] + 47.5#74
        )


        #Transition to N-t graph
        rhs.morph_figure(4, start_time = cues['graph']['end'])
        equation.move_to(
            start_time = cues['graph']['end'],
            new_scale = 1.5,
            new_location = (0, 6, 0)
        )
        graph.move_to(
            start_time = cues['graph']['end'],
            new_scale = 0.9,
            new_location = (-7.5, -2.5, 0)
        )
        eq_arrow.morph_figure(1, start_time = cues['graph']['end'])
        equilibrium.move_to(
            start_time = cues['graph']['end'],
            new_location = (-6.8, -0.3, 0)
        )
        stable.move_to(
            start_time = cues['graph']['end'],
            new_location = (-6.8, 1, 0)
        )

        #N-t graph

        def func2(x): return 5
        graph2 = graph_bobject.GraphBobject(
            func2,
            x_range = [0, 100],
            y_range = [0, 10],
            tick_step = [20, 5],
            width = 10,
            height = 10,
            x_label = 't',
            x_label_pos = 'end',
            y_label = 'N',
            y_label_pos = 'end',
            location = (6.5, -2.5, 0),
            centered = True,
            arrows = True,
            scale = 0.9,
            high_res_curve_indices = [1]
        )
        graph2.add_to_blender(appear_time = cues['ntgraph']['start'])
        eq_arrow.subbobjects[0].color_shift(
            start_time = cues['ntgraph']['start'] + 1
        )
        graph2.animate_function_curve(
            start_time = cues['ntgraph']['start'] + 3.5,
            end_time = cues['ntgraph']['start'] + 6.5,
            #uniform_along_x = True,
            index = 0
        )



        frames_per_time_step = 3
        start_delay = 0.5
        sim_duration = 100

        initial_creature_count = 5
        initial_creatures = []
        for i in range(initial_creature_count):
            new_creature = creature.Creature()
            initial_creatures.append(new_creature)
        sim = drawn_world.DrawnWorld(
            name = 'blob1_sim',
            location = [0, -2.5, 0],
            scale = 0.4,
            #appear_frame = cues['ntgraph']['start'] + 180,
            start_delay = start_delay,
            frames_per_time_step = frames_per_time_step,
            #save = True,
            #load = 'wte_eq_replication',
            sim_duration = sim_duration,
            initial_creatures = initial_creatures,
            gene_updates = [
                ['color', 'creature_color_1', 'birth_modifier', 1000, 0],
                ['shape', 'shape1', 'birth_modifier', 1, 0],
                ['size', '1', 'birth_modifier', 1, 0],
                ['color', 'creature_color_1', 'mutation_chance', 0, 0],
                ['shape', 'shape1', 'mutation_chance', 0, 0],
                ['size', '1', 'mutation_chance', 0, 0],
                ['color', 'creature_color_1', 'death_modifier', 200, 0],
                #['color', 'creature_color_1', 'replication_modifier', 10, 0],
            ]
        )
        sim.add_to_blender(appear_time = cues['ntgraph']['start'] + 7)
        equation.move_to(
            start_time = cues['ntgraph']['start'] + 7,
            new_location = (0, 5, 0)
        )
        graph.move_to(
            start_time = cues['ntgraph']['start'] + 7,
            new_scale = 0.6,
            new_location = (-10, -2.5, 0)
        )
        eq_arrow.morph_figure(2, start_time = cues['ntgraph']['start'] + 7)
        equilibrium.move_to(
            start_time = cues['ntgraph']['start'] + 7,
            new_location = (-9.3, 0.1, 0)
        )
        stable.move_to(
            start_time = cues['ntgraph']['start'] + 7,
            new_location = (-9.3, 1.4, 0)
        )
        graph2.move_to(
            start_time = cues['ntgraph']['start'] + 7,
            new_scale = 0.6,
            new_location = (9, -2.5, 0)
        )

        func3 = sim.get_creature_count_by_t()
        graph2.add_new_function_and_curve(
            func3,
            curve_mat_modifier = 'fade',
            z_shift = -0.05
        )

        graph2.animate_function_curve(
            start_time = cues['ntgraph']['start'] + 7.5,
            end_time = cues['ntgraph']['start'] + 12.5,
            uniform_along_x = True,
            index = 1
        )
        appear_coord2 = [0, func3[0], 0]
        point2 = graph2.add_point_at_coord(
            coord = appear_coord2,
            appear_time = cues['ntgraph']['start'] + 7,
            axis_projections = True,
            track_curve = 1
        )
        graph2.animate_point(
            end_coord = [100, 0, 0],
            start_time = cues['ntgraph']['start'] + 7.5,
            end_time = cues['ntgraph']['start'] + 12.5,
            point = point2
        )
        point2.disappear(disappear_time = cues['ntgraph']['start'] + 13)
        point2.axis_projections[0].disappear(disappear_time = cues['ntgraph']['start'] + 13)
        point2.axis_projections[1].disappear(disappear_time = cues['ntgraph']['start'] + 13)
        graph.multi_animate_point(
            start_time = cues['ntgraph']['start'] + 7.5,
            point = point,
            x_of_t = func3,
            frames_per_time_step = sim.frames_per_time_step
        )
        point.disappear(disappear_time = cues['ntgraph']['start'] + 13)
        point.axis_projections[0].disappear(disappear_time = cues['ntgraph']['start'] + 13)
        point.axis_projections[1].disappear(disappear_time = cues['ntgraph']['start'] + 13)

        #Many sims
        num_sims = 40
        for i in range(num_sims):
            sim.simulate()
            func = sim.get_creature_count_by_t()
            graph2.add_new_function_and_curve(
                func,
                curve_mat_modifier = 'fade',
                z_shift = -0.05
            )
        graph2.animate_all_function_curves(
            start_time = cues['ntgraph']['start'] + 14,
            end_time = cues['ntgraph']['start'] + 19,
            start_window = 0.5,
            uniform_along_x = True,
            skip = 2
        )

        #Prep for next scene
        equation.move_to(
            start_time = cues['ntgraph']['end'] - 0.5,
            new_location = [7.5, 0, 0],
            new_scale = 1
        )
        rhs.morph_figure(5, start_time = cues['ntgraph']['end'] - 0.5)
        graph.move_to(
            start_time = cues['ntgraph']['end'] - 0.5,
            new_location = [-7.5, -1, 0],
            new_scale = 1
        )
        eq_arrow.morph_figure(3, start_time = cues['ntgraph']['end'] - 0.5)
        stable.move_to(
            start_time = cues['ntgraph']['end'] - 0.5,
            new_location = (-6.8, 2.5, 0)
        )
        equilibrium.move_to(
            start_time = cues['ntgraph']['end'] - 0.5,
            new_location = (-6.8, 1.2, 0)
        )

        to_disappear = [graph2, sim]
        for thing in to_disappear:
            thing.disappear(disappear_time = cues['ntgraph']['end'] - 0.5)
'''
'''
class AddReplication(Scene):
    def __init__(self):
        self.subscenes = collections.OrderedDict([
            ('graph', {'duration': 2}),
            ('ntgraph', {'duration': 15}),
        ])
        super().__init__()

    def play(self):
        super().play()
        cues = self.subscenes
        scene_end = self.duration

        def func(x):
            return 1 - 0.2 * x

        def func2(x):
            return 1 - 0.1 * x

        def func3(x):
            return 1

        graph = graph_bobject.GraphBobject(
            func, func2, func3,
            x_range = [0, 10],
            y_range = [-1, 2],
            tick_step = [5, 1],
            width = 10,
            height = 10,
            x_label = 'N',
            x_label_pos = 'end',
            y_label = '\\Delta',
            y_label_pos = 'end',
            location = (-7.5, -1, 0),
            centered = True,
            arrows = True,
        )
        graph.add_to_blender(appear_time = cues['graph']['start'] - 0.5)

        rhs = tex_bobject.TexBobject(
            "1 + (0-0.2) \\times N",
            "1 + (0.1-0.2) \\times N",
            "1 + (0.2-0.2) \\times N",
            "1 + (0.2-0.2) \\times N",
            "1 + (0.2-0.2) \\times N",
            centered = True
        )
        equals = tex_bobject.TexBobject(
            "\!=",
            centered = True
        )
        lhs = tex_bobject.TexBobject(
            "\\Delta",
            centered = True
        )
        equation = tex_complex.TexComplex(
            lhs, equals, rhs,
            location = (7.5, 0, 0),
            scale = 1,
            centered = True
        )
        equation.add_annotation(
            targets = [
                2, #tex_bobject
                [
                    [0, 0, 0],  #form, first char, last char
                    [1, 0, 0],
                    [2, 0, 0],
                    [3, 0, 0, None],
                    [4, 0, 0],
                ],
            ],
            labels = [
                ['\\text{Spontaneous}', '\\text{birth rate} \\phantom{blurghh}'],
                ['\\text{Spontaneous}', '\\text{birth rate} \\phantom{blurghh}'],
                ['\\text{Spontaneous}', '\\text{birth rate} \\phantom{blurghh}'],
                [],
                ['\\text{Spontaneous}', '\\text{birth rate} \\phantom{blurghh}'],
            ],
            alignment = 'bottom',
            angle = [math.pi / 4, 0, 0, 0, 0]
        )
        equation.add_annotation(
            targets = [
                2, #tex_bobject
                [
                    [0, 3, 3],
                    [1, 3, 5, 'arrow'],  #form, first char, last char
                    [2, 3, 5, 'arrow'],
                    [3, 3, 5, None],
                    [4, 3, 5, 'arrow'],
                ],
            ],
            labels = [
                ['\\text{Replication chance}', '\\text{per creature}'],
                ['\\text{Replication chance}', '\\text{per creature}'],
                ['\\text{Replication chance}', '\\text{per creature}'],
                [],
                ['\\text{Replication chance}', '\\text{per creature}'],
            ],
            alignment = 'top'
        )
        equation.add_annotation(
            targets = [
                2, #tex_bobject
                [
                    [0, 5, 7, 'arrow'],
                    [1, 7, 9, 'arrow'],
                    [2, 7, 9, 'arrow'],
                    [3, 7, 9, None],
                    [4, 7, 9, 'arrow'],
                ],
            ],
            labels = [
                ['\\text{Death chance}', '\\text{per creature}'],
                ['\\text{Death chance}', '\\text{per creature}'],
                ['\\text{Death chance}', '\\text{per creature}'],
                [],
                ['\\text{Death chance}', '\\text{per creature}'],
            ],
            alignment = 'bottom'
        )
        equation.add_to_blender(
            appear_time = cues['graph']['start'] - 0.5,
            animate = False
        )
        eq_arrow = gesture.Gesture(
            gesture_series = [
                {
                    'type': 'arrow',
                    'points': {
                        'tail': (-7, 0, 0),
                        'head': (-7.6, -1.8, 0)
                    }
                },
                {
                    'type': 'arrow',
                    'points': {
                        'tail': (-3.5, 0, 0),
                        'head': (-3.5, -1.8, 0)
                    }
                }
            ],
            color = 'color2'
        )
        eq_arrow.add_to_blender(
            appear_time = cues['graph']['start'] - 0.5
        )
        #eq_arrow.morph_figure(1, start_time = cues['graph']['start'] + 900)
        equilibrium = tex_bobject.TexBobject(
            '\\substack{\\text{Equilibrium} \\\\ \\text{point}}',
            '\\substack{\\text{"Stable"} \\\\ \\text{Equilibrium} \\\\ \\text{point}}',
            location = (-6.8, 1.2, 0),
            centered = True,
            color = 'color2'
        )
        equilibrium.add_to_blender(appear_time = cues['graph']['start'] - 0.5)

        stable = tex_bobject.TexBobject(
            '\\text{"Stable"}',
            location = (-6.8, 2.5, 0),
            centered = True,
            scale = 0.67,
            color = 'color2'
        )
        stable.add_to_blender(appear_time = cues['graph']['start'] - 0.5)


        #Morph to example
        rhs.morph_figure(1, start_time = cues['graph']['start'] )#+ 3)
        graph.morph_curve(1, start_time = cues['graph']['start'] )#+ 3)

        eq_arrow.morph_figure(1, start_time = cues['graph']['start'] )#+ 3)
        equilibrium.move_to(
            start_time = cues['graph']['start'],#3,
            new_location = (-3.5, 1.2, 0)
        )
        stable.move_to(
            start_time = cues['graph']['start'],#3,
            new_location = (-3.5, 2.4, 0)
        )

        #Transition to flat line
        rhs.morph_figure(2, start_time = cues['graph']['start'] + 1)#14)
        graph.morph_curve(2, start_time = cues['graph']['start'] + 1)#14)
        eq_arrow.disappear(disappear_time = cues['graph']['start'] + 1.5)#14.5)
        equilibrium.disappear(disappear_time = cues['graph']['start'] + 1.5)#14.5)
        stable.disappear(disappear_time = cues['graph']['start'] + 1.5)#14.5)


        #Transition to N-t graph
        rhs.morph_figure(3, start_time = cues['graph']['start'] + 2)#27)
        equation.move_to(
            start_time = cues['graph']['start'] + 2,#27,
            new_scale = 1.5,
            new_location = (0, 6, 0)
        )
        graph.move_to(
            start_time = cues['graph']['start'] + 2,#27,
            new_scale = 0.9,
            new_location = (-7.5, -2.5, 0)
        )

        def exp_func(x): return 5 + x
        graph2 = graph_bobject.GraphBobject(
            exp_func,
            x_range = [0, 100],
            y_range = [0, 150],
            tick_step = [20, 30],
            width = 10,
            height = 10,
            x_label = 't',
            x_label_pos = 'end',
            y_label = 'N',
            y_label_pos = 'end',
            location = (6.5, -2.5, 0),
            centered = True,
            arrows = True,
            scale = 0.9
        )
        graph2.add_to_blender(appear_time = cues['ntgraph']['start'])

        appear_coord = [0, 1, 0]
        point = graph.add_point_at_coord(
            coord = appear_coord,
            appear_time = cues['ntgraph']['start'] + 1,
            axis_projections = True,
            track_curve = None
        )
        x_of_t = [
            [0, [0, 1, 0]],
            [60, [10, 1, 0]],
            [120, [0, 1, 0]],
            [180, [10, 1, 0]],
            [240, [0, 1, 0]],
            [300, [10, 1, 0]],
        ]
        graph.multi_animate_point(
            point = point,
            x_of_t = x_of_t,
            #frames_per_time_step = 30,
            start_time = cues['ntgraph']['start'] + 1,
            full_coords = True
        )
        point.disappear(disappear_time = cues['ntgraph']['start'] + 7)
        point.axis_projections[0].disappear(disappear_time = cues['ntgraph']['start'] + 7)
        point.axis_projections[1].disappear(disappear_time = cues['ntgraph']['start'] + 7)


        graph2.animate_function_curve(
            start_time = cues['ntgraph']['start'] + 7.5,
            end_time = cues['ntgraph']['start'] + 8.5,
            #uniform_along_x = True,
            index = 0
        )


        #frames_per_time_step = 3
        #start_delay = 60
        sim_duration = 100

        initial_creature_count = 5
        initial_creatures = []
        for i in range(initial_creature_count):
            new_creature = creature.Creature()
            initial_creatures.append(new_creature)
        sim = population.Population(
            #name = 'blob1_sim',
            #location = [0, -2.5, 0],
            #scale = 0.4,
            #appear_time = cues['ntgraph']['start'] + 180,
            #start_delay = start_delay,
            #times_per_time_step = frames_per_time_step,
            #save = True,
            #load = 'wte_eq_replication',
            sim_duration = sim_duration,
            initial_creatures = initial_creatures,
            gene_updates = [
                ['color', 'creature_color_1', 'birth_modifier', 1000, 0],
                ['shape', 'shape1', 'birth_modifier', 1, 0],
                ['size', '1', 'birth_modifier', 1, 0],
                ['color', 'creature_color_1', 'mutation_chance', 0, 0],
                ['shape', 'shape1', 'mutation_chance', 0, 0],
                ['size', '1', 'mutation_chance', 0, 0],
                ['color', 'creature_color_1', 'death_modifier', 200, 0],
                ['color', 'creature_color_1', 'replication_modifier', 200, 0],
            ] #LIES
        )
        """sim.add_to_blender(appear_time = cues['ntgraph']['start'] + 180)
        equation.move_to(
            start_time = cues['ntgraph']['start'] + 180,
            new_location = (0, 5, 0)
        )
        graph.move_to(
            start_time = cues['ntgraph']['start'] + 180,
            new_scale = 0.6,
            new_location = (-10, -2.5, 0)
        )
        graph2.move_to(
            start_time = cues['ntgraph']['start'] + 180,
            new_scale = 0.6,
            new_location = (9, -2.5, 0)
        )"""


        #data = sim.get_creature_count_by_t()
        #graph2.add_new_function_and_curve(data)

        """graph2.animate_function_curve(
            start_time = cues['ntgraph']['start'] + 240,
            end_time = cues['ntgraph']['start'] + 540,
            uniform_along_x = True,
            index = 1
        )
        appear_coord2 = [0, data[0], 0]
        point2 = graph2.add_point_at_coord(
            coord = appear_coord2,
            appear_time = cues['ntgraph']['start'] + 180,
            axis_projections = True,
            track_curve = 1
        )
        graph2.animate_point(
            end_coord = [100, 0, 0],
            start_time = cues['ntgraph']['start'] + 240,
            end_time = cues['ntgraph']['start'] + 540,
            point = point2
        )"""
        #Many sims
        if RENDER_QUALITY == 'high':
            num_sims = 40
        else:
            num_sims = 1
        for i in range(num_sims):
            sim.simulate()
            func = sim.get_creature_count_by_t()
            graph2.add_new_function_and_curve(
                func,
                curve_mat_modifier = 'fade',
                z_shift = -0.05
            )
        graph2.animate_all_function_curves(
            start_time = cues['ntgraph']['start'] + 9,
            end_time = cues['ntgraph']['start'] + 14,
            start_window = 0.5,
            uniform_along_x = True,
            skip = 1
        )

        spread = gesture.Gesture(
            gesture_series = [
                {
                    'type': 'bracket',
                    'points': {
                        'annotation_point': (11.5, -1, 0),
                        'left_point': (10.5, 2, 0),
                        'right_point': (10.5, -4, 0)
                    }
                }
            ]
        )
        spread.add_to_blender(
            appear_time = cues['ntgraph']['start'] + 14
        )


        #Prep for next scene
        equation.move_to(
            start_time = cues['ntgraph']['end'] - 0.5,
            new_location = [7.5, 0, 0],
            new_scale = 1
        )
        rhs.morph_figure(4, start_time = cues['ntgraph']['end'] - 0.5)
        graph.move_to(
            start_time = cues['ntgraph']['end'] - 0.5,
            new_location = [-7.5, -1, 0],
            new_scale = 1
        )

        to_disappear = [graph2, spread]
        for thing in to_disappear:
            thing.disappear(disappear_time = cues['ntgraph']['end'])
'''
'''
class Exponential(Scene):
    def __init__(self):
        self.subscenes = collections.OrderedDict([
            ('graph', {'duration': 9.5}),
            ('ntgraph', {'duration': 7.5}),
        ])
        super().__init__()

    def play(self):
        super().play()
        cues = self.subscenes
        scene_end = self.duration

        def func(x):
            return 1

        def func2(x):
            return 1 + 0.1 * x

        graph = graph_bobject.GraphBobject(
            func, func2,
            x_range = [0, 10],
            y_range = [-1, 2],
            tick_step = [5, 1],
            width = 10,
            height = 10,
            x_label = 'N',
            x_label_pos = 'end',
            y_label = '\\Delta',
            y_label_pos = 'end',
            location = (-7.5, -1, 0),
            centered = True,
            arrows = True,
        )
        graph.add_to_blender(appear_time = cues['graph']['start'] - 0.5)

        rhs = tex_bobject.TexBobject(
            "1 + (0.2-0.2) \\times N",
            "1 + (0.3-0.2) \\times N",
            "1 + (0.3-0.2) \\times N",
            "1 + (0.3-0.2) \\times N",
            centered = True
        )
        equals = tex_bobject.TexBobject(
            "\!=",
            centered = True
        )
        lhs = tex_bobject.TexBobject(
            "\\Delta",
            centered = True
        )
        equation = tex_complex.TexComplex(
            lhs, equals, rhs,
            location = (7.5, 0, 0),
            scale = 1,
            centered = True
        )
        equation.add_annotation(
            targets = [
                2, #tex_bobject
                [
                    [0, 0, 0],  #form, first char, last char
                    [1, 0, 0],
                    [2, 0, 0, None],
                    [3, 0, 0],
                ],
            ],
            labels = [
                ['\\text{Spontaneous}', '\\text{birth rate} \\phantom{blurghh}'],
                ['\\text{Spontaneous}', '\\text{birth rate} \\phantom{blurghh}'],
                [],
                ['\\text{Spontaneous}', '\\text{birth rate} \\phantom{blurghh}'],
            ],
            alignment = 'bottom'
        )
        equation.add_annotation(
            targets = [
                2, #tex_bobject
                [
                    [0, 3, 5, 'arrow'],  #form, first char, last char
                    [1, 3, 5, 'arrow'],
                    [2, 3, 5, None],
                    [3, 3, 5, 'arrow'],
                ],
            ],
            labels = [
                ['\\text{Replication chance}', '\\text{per creature}'],
                ['\\text{Replication chance}', '\\text{per creature}'],
                [],
                ['\\text{Replication chance}', '\\text{per creature}'],
            ],
            alignment = 'top'
        )
        equation.add_annotation(
            targets = [
                2, #tex_bobject
                [
                    [0, 7, 9, 'arrow'],
                    [1, 7, 9, 'arrow'],
                    [2, 7, 9, None],
                    [3, 7, 9, 'arrow'],
                ],
            ],
            labels = [
                ['\\text{Death chance}', '\\text{per creature}'],
                ['\\text{Death chance}', '\\text{per creature}'],
                [],
                ['\\text{Death chance}', '\\text{per creature}'],
            ],
            alignment = 'bottom'
        )
        equation.add_to_blender(
            appear_time = cues['graph']['start'] - 0.5,
            animate = False
        )

        #Morph to example
        rhs.morph_figure(1, start_time = cues['graph']['start'] + 1)
        graph.morph_curve(1, start_time = cues['graph']['start'] + 1)

        appear_coord = [0, 1, 0]
        point = graph.add_point_at_coord(
            coord = appear_coord,
            appear_time = cues['graph']['start'] + 2,
            axis_projections = True,
            track_curve = None
        )

        num_shifts = 8
        #frames_per_shift = 60

        coords = [[0, 1, 0]]
        for i in range(num_shifts):
            x = coords[i][0] + coords[i][1]
            y = 1 + 0.1 * x
            coords.append([x, y, 0])

        x_of_t = []
        #for i, coord in enumerate(coords):
        #x_of_t.append([0, coords[0]])
        x_of_t.append([0, coords[1]])
        x_of_t.append([60, coords[2]])
        x_of_t.append([120, coords[3]])
        x_of_t.append([180, coords[4]])
        x_of_t.append([240, coords[5]])
        x_of_t.append([300, coords[6]])
        x_of_t.append([360, coords[7]])


        graph.multi_animate_point(
            point = point,
            x_of_t = x_of_t,
            #frames_per_time_step = 30,
            start_time = cues['graph']['start'] + 3,
            full_coords = True
        )
        point.disappear(disappear_time = cues['graph']['start'] + 10)
        point.axis_projections[0].disappear(disappear_time = cues['graph']['start'] + 10)
        point.axis_projections[1].disappear(disappear_time = cues['graph']['start'] + 10)


        #Transition to N-t graph
        rhs.morph_figure(2, start_time = cues['graph']['start'] + 9.5)
        equation.move_to(
            start_time = cues['graph']['start'] + 9.5,
            new_scale = 1.5,
            new_location = (0, 6, 0)
        )
        graph.move_to(
            start_time = cues['graph']['start'] + 9.5,
            new_scale = 0.9,
            new_location = (-7.5, -2.5, 0)
        )

        #def exp_func(x): return 105 * math.exp(0.01 * x) - 100
        def exp_func(x): return 15 * math.exp(0.1 * x) - 10
        graph2 = graph_bobject.GraphBobject(
            exp_func,
            x_range = [0, 40],
            y_range = [0, 1200],
            tick_step = [10, 300],
            width = 10,
            height = 10,
            x_label = 't',
            x_label_pos = 'end',
            y_label = 'N',
            y_label_pos = 'end',
            location = (6.5, -2.5, 0),
            centered = True,
            arrows = True,
            scale = 0.9
        )
        graph2.add_to_blender(appear_time = cues['ntgraph']['start'])


        graph2.animate_function_curve(
            start_time = cues['ntgraph']['start'] + 0.5,
            end_time = cues['ntgraph']['start'] + 1.5,
            #uniform_along_x = True,
            index = 0
        )


        #frames_per_time_step = 3
        #start_delay = 60
        sim_duration = 40

        initial_creature_count = 5
        initial_creatures = []
        for i in range(initial_creature_count):
            new_creature = creature.Creature()
            initial_creatures.append(new_creature)
        sim = population.Population(
            #name = 'blob1_sim',
            #location = [0, -2.5, 0],
            #scale = 0.4,
            #appear_frame = cues['ntgraph']['start'] + 180,
            #start_delay = start_delay,
            #frames_per_time_step = frames_per_time_step,
            #save = True,
            #load = 'wte_eq_replication',
            duration = sim_duration,
            initial_creatures = initial_creatures,
            gene_updates = [
                ['color', 'creature_color_1', 'birth_modifier', 1000, 0],
                ['shape', 'shape1', 'birth_modifier', 1, 0],
                ['size', '1', 'birth_modifier', 1, 0],
                ['color', 'creature_color_1', 'mutation_chance', 0, 0],
                ['shape', 'shape1', 'mutation_chance', 0, 0],
                ['size', '1', 'mutation_chance', 0, 0],
                ['color', 'creature_color_1', 'death_modifier', 200, 0],
                ['color', 'creature_color_1', 'replication_modifier', 300, 0],
            ] #LIES
        )
        """sim.add_to_blender(appear_time = cues['ntgraph']['start'] + 180)
        equation.move_to(
            start_time = cues['ntgraph']['start'] + 180,
            new_location = (0, 5, 0)
        )
        graph.move_to(
            start_time = cues['ntgraph']['start'] + 180,
            new_scale = 0.6,
            new_location = (-10, -2.5, 0)
        )
        graph2.move_to(
            start_time = cues['ntgraph']['start'] + 180,
            new_scale = 0.6,
            new_location = (9, -2.5, 0)
        )"""


        #data = sim.get_creature_count_by_t()
        #graph2.add_new_function_and_curve(data)

        """graph2.animate_function_curve(
            start_time = cues['ntgraph']['start'] + 240,
            end_time = cues['ntgraph']['start'] + 540,
            uniform_along_x = True,
            index = 1
        )
        appear_coord2 = [0, data[0], 0]
        point2 = graph2.add_point_at_coord(
            coord = appear_coord2,
            appear_time = cues['ntgraph']['start'] + 180,
            axis_projections = True,
            track_curve = 1
        )
        graph2.animate_point(
            end_coord = [100, 0, 0],
            start_time = cues['ntgraph']['start'] + 240,
            end_time = cues['ntgraph']['start'] + 540,
            point = point2
        )"""
        #Many sims
        if RENDER_QUALITY == 'high':
            num_sims = 40
        else:
            num_sims = 1
        for i in range(num_sims):
            sim.simulate()
            func = sim.get_creature_count_by_t()
            graph2.add_new_function_and_curve(
                func,
                curve_mat_modifier = 'fade',
                z_shift = -0.05
            )
        graph2.animate_all_function_curves(
            start_time = cues['ntgraph']['start'] + 1.5,
            end_time = cues['ntgraph']['start'] + 6.5,
            start_window = 0.5,
            uniform_along_x = True,
            skip = 1
        )

        top_y = graph2.tick_labels_y[-1]
        top_y.pulse(
            time = cues['ntgraph']['start'] + 4.5
        )
        y_nums = top_y.subbobjects
        for num in y_nums:
            num.color_shift(
                start_time = cues['ntgraph']['start'] + 4.5
            )

        spread = gesture.Gesture(
            gesture_series = [
                {
                    'type': 'bracket',
                    'points': {
                        'annotation_point': (11.5, -1, 0),
                        'left_point': (10.5, 2, 0),
                        'right_point': (10.5, -4, 0)
                    }
                }
            ]
        )
        spread.add_to_blender(
            appear_time = cues['ntgraph']['start'] + 6.5
        )

        #Prep for next scene
        equation.move_to(
            start_time = cues['ntgraph']['end'] - 0.5,
            new_location = [7.5, 0, 0],
            new_scale = 1
        )
        rhs.morph_figure(3, start_time = cues['ntgraph']['end'] - 0.5)
        graph.move_to(
            start_time = cues['ntgraph']['end'] - 0.5,
            new_location = [-7.5, -1, 0],
            new_scale = 1
        )

        to_disappear = [graph2, spread]
        for thing in to_disappear:
            thing.disappear(disappear_time = cues['ntgraph']['end'])
'''
'''
class Extinction(Scene):
    def __init__(self):
        self.subscenes = collections.OrderedDict([
            ('graph', {'duration': 6}),
            ('ntgraph', {'duration': 19.5}),
        ])
        super().__init__()

    def play(self):
        super().play()
        cues = self.subscenes
        scene_end = self.duration

        def func(x):
            return 1 + 0.1 * x

        def func2(x):
            return 0.1 * x

        graph = graph_bobject.GraphBobject(
            func, func2,
            x_range = [0, 10],
            y_range = [-1, 2],
            tick_step = [5, 1],
            width = 10,
            height = 10,
            x_label = 'N',
            x_label_pos = 'end',
            y_label = '\\Delta',
            y_label_pos = 'end',
            location = (-7.5, -1, 0),
            centered = True,
            arrows = True,
        )
        graph.add_to_blender(appear_time = cues['graph']['start'] - 0.5)

        rhs = tex_bobject.TexBobject(
            "1 + (0.3-0.2) \\times N",
            "0 + (0.3-0.2) \\times N",
            "0 + (0.3-0.2) \\times N",
            centered = True
        )
        equals = tex_bobject.TexBobject(
            "\!=",
            centered = True
        )
        lhs = tex_bobject.TexBobject(
            "\\Delta",
            centered = True
        )
        equation = tex_complex.TexComplex(
            lhs, equals, rhs,
            location = (7.5, 0, 0),
            scale = 1,
            centered = True
        )
        equation.add_annotation(
            targets = [
                2, #tex_bobject
                [
                    [0, 0, 0],  #form, first char, last char
                    [1, 0, 0],
                    [2, 0, 0, None],
                ],
            ],
            labels = [
                ['\\text{Spontaneous}', '\\text{birth rate} \\phantom{blurghh}'],
                ['\\text{Spontaneous}', '\\text{birth rate} \\phantom{blurghh}'],
                [],
            ],
            alignment = 'bottom'
        )
        equation.add_annotation(
            targets = [
                2, #tex_bobject
                [
                    [0, 3, 5, 'arrow'],  #form, first char, last char
                    [1, 3, 5, 'arrow'],
                    [2, 3, 5, None],
                ],
            ],
            labels = [
                ['\\text{Replication chance}', '\\text{per creature}'],
                ['\\text{Replication chance}', '\\text{per creature}'],
                [],
            ],
            alignment = 'top'
        )
        equation.add_annotation(
            targets = [
                2, #tex_bobject
                [
                    [0, 7, 9, 'arrow'],
                    [1, 7, 9, 'arrow'],
                    [2, 7, 9, None],
                ],
            ],
            labels = [
                ['\\text{Death chance}', '\\text{per creature}'],
                ['\\text{Death chance}', '\\text{per creature}'],
                [],
            ],
            alignment = 'bottom'
        )
        equation.add_to_blender(
            appear_time = cues['graph']['start'] - 0.5,
            animate = False
        )

        #Get rid of B
        rhs.morph_figure(1, start_time = cues['graph']['start'])
        graph.morph_curve(1, start_time = cues['graph']['start'])

        appear_coord = [5, 0.5, 0]
        point = graph.add_point_at_coord(
            coord = appear_coord,
            appear_time = cues['graph']['start'] + 0.5,
            axis_projections = True,
            track_curve = None
        )

        num_shifts = 3
        frames_per_shift = 60

        coords = [[5, 0.5, 0]]
        for i in range(num_shifts):
            x = coords[i][0] + coords[i][1]
            y = 0.1 * x
            coords.append([x, y, 0])

        coords.append([0, 0, 0])

        x_of_t = []
        for i, coord in enumerate(coords):
            time = i * frames_per_shift
            x_of_t.append([time, coord])

        #Wiggle
        #time = time + 60

        num_wiggles = 2
        time_per_wiggle = 20
        for i in range(num_wiggles):
            x_of_t.append([time + time_per_wiggle * i, [0.1, 0, 0]])
            x_of_t.append([time + time_per_wiggle * i + time_per_wiggle / 2, [-0.1, 0, 0]])
        x_of_t.append([time + time_per_wiggle * num_wiggles, [0, 0, 0]])
        x_of_t.append([time + time_per_wiggle * num_wiggles + time_per_wiggle / 2, [0, 0, 0]])
        #Last one is here because the last shift (currently) automatically takes
        #the default transition time, regardless of time values. Using the last
        #one to add another keyframe and speed up the final transition.


        graph.multi_animate_point(
            point = point,
            x_of_t = x_of_t,
            #frames_per_time_step = 30,
            start_time = cues['graph']['start'],
            full_coords = True
        )


        extinction = tex_bobject.TexBobject(
            '\\text{Extinction}',
            location = [-7, -5, 0],
            centered = True,
            color = 'color2'
        )
        ex_arrow = gesture.Gesture(
            gesture_series = [
                {
                    'type' : 'arrow',
                    'points' : {
                        'head' : [-10.5, -3, 0],
                        'tail' : [-8, -4.3, 0],
                    }
                }
            ],
            color = 'color2'
        )
        extinction.add_to_blender(appear_time = cues['graph']['start'] + 5)
        ex_arrow.add_to_blender(appear_time = cues['graph']['start'] + 5)

        point.disappear(disappear_time = cues['graph']['start'] + 6)
        point.axis_projections[0].disappear(disappear_time = cues['graph']['start'] + 6)
        point.axis_projections[1].disappear(disappear_time = cues['graph']['start'] + 6)

        extinction.disappear(disappear_time = cues['graph']['start'] + 6)
        ex_arrow.disappear(disappear_time = cues['graph']['start'] + 6)

        #Transition to N-t graph
        def exp_func(x): return 2 * math.exp(0.1 * x)
        #def exp_func(x): return 15 * math.exp(0.1 * x) - 10
        graph2 = graph_bobject.GraphBobject(
            exp_func,
            x_range = [0, 20],
            y_range = [0, 30],
            tick_step = [5, 10],
            width = 10,
            height = 10,
            x_label = 't',
            x_label_pos = 'end',
            y_label = 'N',
            y_label_pos = 'end',
            location = (9, -2.5, 0), #(6.5, -2.5, 0),
            centered = True,
            arrows = True,
            scale = 0.6,
            high_res_curve_indices = [0, 1, 2]
        )

        frames_per_time_step = 15
        start_delay = 1.5
        sim_duration = 20

        initial_creature_count = 2
        initial_creatures = []
        for i in range(initial_creature_count):
            new_creature = creature.Creature()
            initial_creatures.append(new_creature)
        sim = drawn_world.DrawnWorld(
            name = 'blob1_sim',
            location = [0, -2.5, 0],
            scale = 0.4,
            #appear_frame = cues['ntgraph']['start'] + 180,
            start_delay = start_delay,
            frames_per_time_step = frames_per_time_step,
            #save = True,
            load = 'ro_not_extinction',
            sim_duration = sim_duration,
            initial_creatures = initial_creatures,
            gene_updates = [
                ['color', 'creature_color_1', 'birth_modifier', 0, 0],
                ['shape', 'shape1', 'birth_modifier', 0, 0],
                ['size', '1', 'birth_modifier', 0, 0],
                ['color', 'creature_color_1', 'mutation_chance', 0, 0],
                ['shape', 'shape1', 'mutation_chance', 0, 0],
                ['size', '1', 'mutation_chance', 0, 0],
                ['color', 'creature_color_1', 'death_modifier', 200, 0],
                ['color', 'creature_color_1', 'replication_modifier', 300, 0],
            ],
            pauses = [
                [0, 1]
            ]
        )
        rhs.morph_figure(2, start_time = cues['ntgraph']['start'])
        equation.move_to(
            start_time = cues['ntgraph']['start'],
            new_location = (0, 5, 0),
            new_scale = 1.5,
        )
        graph.move_to(
            start_time = cues['ntgraph']['start'],
            new_scale = 0.6,
            new_location = (-10, -2.5, 0)
        )
        graph2.add_to_blender(appear_time = cues['ntgraph']['start'])

        sim.add_to_blender(appear_time = cues['ntgraph']['start'])
        """graph2.move_to(
            start_frame = cues['ntgraph']['start'] + 180,
            new_scale = 0.6,
            new_location = (9, -2.5, 0)
        )"""
        """func = sim.get_creature_count_by_t()
        print(func)
        graph2.add_new_function_and_curve(
            func,
            curve_mat_modifier = 'fade',
            z_shift = -0.05
        )"""

        #Predicted curve
        graph2.animate_function_curve(
            start_time = cues['ntgraph']['start'] + 0.5,
            end_time = cues['ntgraph']['start'] + 1.5,
            #uniform_along_x = True,
            index = 0
        )


        #Animate sim data and points
        data = sim.get_creature_count_by_t()
        print(data)
        graph2.add_new_function_and_curve(
            data,
            curve_mat_modifier = 'fade',
            z_shift = -0.05,
        )
        graph2.animate_function_curve(
            start_time = cues['ntgraph']['start'] + 2,
            end_time = cues['ntgraph']['start'] + 7,
            uniform_along_x = True,
            index = 1
        )
        #nt graph highlight point
        appear_coord2 = [0, data[0], 0]
        point2 = graph2.add_point_at_coord(
            coord = appear_coord2,
            appear_time = cues['ntgraph']['start'] + 1.5,
            axis_projections = True,
            track_curve = 1
        )
        graph2.animate_point(
            end_coord = [20, 0, 0],
            start_time = cues['ntgraph']['start'] + 2,
            end_time = cues['ntgraph']['start'] + 7,
            point = point2
        )
        #delta graph highlight point
        appear_coord21 = [data[0], func2(data[0]), 0]
        point21 = graph.add_point_at_coord(
            coord = appear_coord21,
            appear_time = cues['ntgraph']['start'] + 1.5,
            axis_projections = True,
            track_curve = 1
        )
        graph.multi_animate_point(
            start_time = cues['ntgraph']['start'] + 2,
            #end_time = cues['ntgraph']['start'] + 480,
            point = point21,
            frames_per_time_step = frames_per_time_step,
            x_of_t = data, #Not func2. This uses the sim data to inform movements
        )

        sim.disappear(
            disappear_time = cues['ntgraph']['start'] + 7.5 + 1/60,
            #animate = False
        )
        #point 21 shoots off and an arrow appears
        point21.disappear(disappear_time = cues['ntgraph']['start'] + 5)
        point21.axis_projections[0].disappear(disappear_time = cues['ntgraph']['start'] + 5)
        point21.axis_projections[1].disappear(disappear_time = cues['ntgraph']['start'] + 5)
        zoom_arrow = gesture.Gesture(
            gesture_series = [
                {
                    'type' : 'arrow',
                    'points' : {
                        'head' : [-6, -5/6, 0],
                        'tail' : [-8, -1.5, 0],
                    }
                }
            ],
            color = 'color2'
        )
        zoom_arrow.add_to_blender(appear_time = cues['ntgraph']['start'] + 4.5)

        #point 2 disappears after
        point2.disappear(disappear_time = cues['ntgraph']['start'] + 7.5)
        point2.axis_projections[0].disappear(disappear_time = cues['ntgraph']['start'] + 7.5)
        point2.axis_projections[1].disappear(disappear_time = cues['ntgraph']['start'] + 7.5)
        zoom_arrow.disappear(disappear_time = cues['ntgraph']['start'] + 7.5)

        #Second sim
        sim2 = drawn_world.DrawnWorld(
            name = 'blob1_sim',
            location = [0, -2.5, 0],
            scale = 0.4,
            #appear_frame = cues['ntgraph']['start'] + 180,
            start_delay = 0.5,
            frames_per_time_step = frames_per_time_step,
            #save = True,
            load = 'ro_extinction',
            sim_duration = sim_duration,
            initial_creatures = initial_creatures,
            gene_updates = [
                ['color', 'creature_color_1', 'birth_modifier', 0, 0],
                ['shape', 'shape1', 'birth_modifier', 0, 0],
                ['size', '1', 'birth_modifier', 0, 0],
                ['color', 'creature_color_1', 'mutation_chance', 0, 0],
                ['shape', 'shape1', 'mutation_chance', 0, 0],
                ['size', '1', 'mutation_chance', 0, 0],
                ['color', 'creature_color_1', 'death_modifier', 200, 0],
                ['color', 'creature_color_1', 'replication_modifier', 300, 0],
            ] #LIES
        )
        sim2.add_to_blender(
            appear_time = cues['ntgraph']['start'] + 7.5,
            #animate = False
        )

        data2 = sim2.get_creature_count_by_t()
        print(data2)
        graph2.add_new_function_and_curve(
            data2,
            curve_mat_modifier = 'fade',
            z_shift = -0.05,
        )
        graph2.animate_function_curve(
            start_time = cues['ntgraph']['start'] + 8,
            end_time = cues['ntgraph']['start'] + 13,
            uniform_along_x = True,
            index = 2
        )
        #nt graph highlight point
        appear_coord3 = [0, data2[0], 0]
        point3 = graph2.add_point_at_coord(
            coord = appear_coord3,
            appear_time = cues['ntgraph']['start'] + 7.5,
            axis_projections = True,
            track_curve = 2
        )
        graph2.animate_point(
            end_coord = [20, 0, 0],
            start_time = cues['ntgraph']['start'] + 8,
            end_time = cues['ntgraph']['start'] + 13,
            point = point3
        )
        #delta graph highlight point
        appear_coord31 = [data2[0], func2(data2[0]), 0]
        point31 = graph.add_point_at_coord(
            coord = appear_coord31,
            appear_time = cues['ntgraph']['start'] + 7.5,
            axis_projections = True,
            track_curve = 1
        )
        graph.multi_animate_point(
            start_time = cues['ntgraph']['start'] + 8,
            #end_time = cues['ntgraph']['start'] + 480,
            point = point31,
            frames_per_time_step = frames_per_time_step,
            x_of_t = data2, #Not func2. This uses the sim data to inform movements
        )

        point3.disappear(disappear_time = cues['ntgraph']['start'] + 13.5)
        point3.axis_projections[0].disappear(disappear_time = cues['ntgraph']['start'] + 13.5)
        point3.axis_projections[1].disappear(disappear_time = cues['ntgraph']['start'] + 13.5)
        point31.disappear(disappear_time = cues['ntgraph']['start'] + 13.5)
        point31.axis_projections[0].disappear(disappear_time = cues['ntgraph']['start'] + 13.5)
        point31.axis_projections[1].disappear(disappear_time = cues['ntgraph']['start'] + 13.5)

        #data = sim.get_creature_count_by_t()
        #graph2.add_new_function_and_curve(data)

        """graph2.animate_function_curve(
            start_time = cues['ntgraph']['start'] + 240,
            end_time = cues['ntgraph']['start'] + 540,
            uniform_along_x = True,
            index = 1
        )
        appear_coord2 = [0, data[0], 0]
        point2 = graph2.add_point_at_coord(
            coord = appear_coord2,
            appear_time = cues['ntgraph']['start'] + 180,
            axis_projections = True,
            track_curve = 1
        )
        graph2.animate_point(
            end_coord = [100, 0, 0],
            start_time = cues['ntgraph']['start'] + 240,
            end_time = cues['ntgraph']['start'] + 540,
            point = point2
        )"""
        #Many sims
        if RENDER_QUALITY == 'high':
            num_sims = 40
        else:
            num_sims = 1
        for i in range(num_sims):
            sim.simulate()
            func = sim.get_creature_count_by_t()
            #print(func)
            graph2.add_new_function_and_curve(
                func,
                curve_mat_modifier = 'fade',
                z_shift = -0.05
            )
        graph2.animate_all_function_curves(
            start_time = cues['ntgraph']['start'] + 14,
            end_time = cues['ntgraph']['start'] + 19,
            start_window = 0.5,
            uniform_along_x = True,
            skip = 3
        )

        """spread = gesture.Gesture(
            gesture_series = [
                {
                    'type': 'bracket',
                    'points': {
                        'annotation_point': (11.5, -1, 0),
                        'left_point': (10.5, 2, 0),
                        'right_point': (10.5, -4, 0)
                    }
                }
            ]
        )
        spread.add_to_blender(
            appear_time = cues['ntgraph']['start'] + 23
        )"""

        #Prep for next scene
        to_disappear = [equation, graph, sim2, graph2]
        for thing in to_disappear:
            thing.disappear(disappear_time = cues['ntgraph']['end'])
'''
'''
class EndCard(Scene):
    def __init__(self):
        self.subscenes = collections.OrderedDict([
            ('card', {'duration': 3}),
        ])
        super().__init__()

    def play(self):
        super().play()
        cues = self.subscenes
        scene_end = self.duration

        bpy.ops.mesh.primitive_plane_add()
        play_bar = bpy.context.object
        play_bar.scale[0] = 15
        play_bar.scale[1] = 90 / 720 * 8.4
        play_bar.location = [0, -8.4 + play_bar.scale[1], 0]

        bpy.ops.mesh.primitive_plane_add()
        vid_rec = bpy.context.object
        vid_rec.scale[0] = 410 / 1280 * 15
        vid_rec.scale[1] = 230 / 720 * 8.4
        vid_rec.location = [9, -3, 0]

        """bpy.ops.mesh.primitive_plane_add()
        end_area = bpy.context.object
        end_area.scale[0] = 1225 / 1280 * 15
        end_area.scale[1] = 518 / 720 * 8.4
        end_area.location = [0, 0.2, -0.1]"""

        bpy.ops.mesh.primitive_cylinder_add()
        sub_cir = bpy.context.object
        sub_cir.scale = [98 / 1280 * 30, 98 / 1280 * 30, 0]
        sub_cir.location = [-11.5, -2.8, 0]



        logo = svg_bobject.SVGBobject(
            "Layer",
            #file_name = "PrimerLogoWhite",
            location = (-9.2, -1.87, 0),
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
            location = (5, 4, 0)
        )
        reddit.add_to_blender(appear_time = 0)
        disc = tex_bobject.TexBobject(
            '\\text{/r/primerlearning}',
            location = [6.5, 2.5, 0],
            color = 'color2',
            scale = 0.8
        )
        disc.add_to_blender(appear_time = 0)

        patreon = import_object(
            'patreon', 'svgblend',
            scale = 2.297,
            location = (-11.5, 4, 0)
        )
        patreon.add_to_blender(appear_time = 0)
        thanks = tex_bobject.TexBobject(
            '\\text{Special thanks:}',
            location = [-9, 5.1, 0],
            color = 'color2'
        )
        thanks.add_to_blender(appear_time = 0)
        js = tex_bobject.TexBobject(
            '\\text{The one}',
            '\\text{The only}',
            '\\text{Jordan Scales}',
            location = [-9.1, 3.1, 0],
            color = 'color2',
            scale = 1.4
        )
        js.add_to_blender(appear_time = 1)
        js.morph_figure(1, start_time = 1.5)
        js.morph_figure(2, start_time = 2)

        remaining = [reddit, disc, logo, patreon, thanks, js]
        for thing in remaining:
            thing.disappear(disappear_time = scene_end)
'''
