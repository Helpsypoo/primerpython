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

class LastVideoExp(Scene):
    def __init__(self):
        self.subscenes = collections.OrderedDict([
            ('pre_transplant', {'duration': 10}),
            #('post_transplant', {'duration': 10}),\
        ])
        super().__init__()

    def play(self):
        super().play()
        #self.subscenes
        #self.duration

        self.pre_transplant()

    def pre_transplant(self):
        #Stretch goal: Make blobs look around in a more directed way
        cues = self.subscenes['pre_transplant']

        make_image_background('colon_zoom_right.png')

        #Zoom out to effectively make the bacteria smaller
        zoom_out_factor = 2
        x_shift = 10.5
        cam_bobj = bobject.Bobject(
            location = [
                CAMERA_LOCATION[0],
                CAMERA_LOCATION[1],
                zoom_out_factor * CAMERA_LOCATION[2],
            ]
        )
        cam_bobj.add_to_blender(appear_time = 0)
        cam_obj = bpy.data.objects['Camera']
        cam_obj.location = [0, 0, 0]
        cam_obj.parent = cam_bobj.ref_obj

        colon_points = [
            [-5.498534679412842, -3.8365087509155273, 0],
            [-6.38494873046875, -3.227099657058716, 0],
            [-6.717353343963623, -2.146782875061035, 0],
            [-6.634251117706299, -0.9279640316963196, 0],
            [-6.551150321960449, 1.2049685716629028, 0],
            [-6.384949207305908, 2.4237873554229736, 0],
            [-6.218745708465576, 3.42100191116333, 0],
            [-6.440348148345947, 4.584420204162598, 0],
            [-6.274146556854248, 6.163344860076904, 0],
            [-5.249231338500977, 6.27414608001709, 0],
            [-4.196613788604736, 5.969441890716553, 0],
            [-3.227100133895874, 5.609334945678711, 0],
            [-2.063681125640869, 5.415432929992676, 0],
            [-0.9556646347045898, 5.332330703735352, 0],
            [0.26315388083457947, 5.24923038482666, 0],
            [1.5096733570098877, 5.332330703735352, 0],
            [2.589988946914673, 5.415432453155518, 0],
            [3.5318045616149902, 5.637035846710205, 0],
            [4.639822483062744, 6.052542209625244, 0],
            [5.637034893035889, 6.440348148345947, 0],
            [6.4957499504089355, 6.301846504211426, 0],
            [6.301847457885742, 4.667520999908447, 0],
            [6.495749473571777, 3.531803846359253, 0],
            [6.163345813751221, 2.4237871170043945, 0],
            [6.274145603179932, 0.7063607573509216, 0],
            [6.246445178985596, -1.1772679090499878, 0],
            [5.914041996002197, -2.8115925788879395, 0],
            [5.221530437469482, -3.947310209274292, 0],
            [4.55672025680542, -5.05532693862915, 0],
            [2.9223949909210205, -6.052542686462402, 0],
            [1.6481753587722778, -6.191044807434082, 0],
            [0.06925218552350998, -6.4403486251831055, 0],
            [-0.016619933769106865, -8.26026725769043, 0],
            [-0.9805952310562134, -7.828138828277588, 0],
            [-1.1135575771331787, -6.465278148651123, 0],
            [-0.9473539590835571, -5.434823036193848, 0],
            [-0.44874706864356995, -5.069177150726318, 0],
            [0.7146719098091125, -5.335101127624512, 0],
            [1.711885690689087, -5.733987808227539, 0],
            [2.742342472076416, -5.534544944763184, 0],
            [3.6065964698791504, -4.803253650665283, 0],
            [4.537330627441406, -3.83927845954895, 0],
            [5.035937309265137, -2.5096583366394043, 0],
            [5.401581287384033, -1.0138355493545532, 0],
            [5.534543514251709, 1.1135568618774414, 0],
            [5.501305103302002, 2.5428988933563232, 0],
            [5.468064785003662, 3.8060386180877686, 0],
            [5.069177150726318, 5.36834192276001, 0],
            [3.8060388565063477, 4.902975559234619, 0],
            [1.8448481559753418, 4.437607288360596, 0],
            [0.648189127445221, 4.171682834625244, 0],
            [-0.5152283310890198, 4.2049241065979, 0],
            [-1.645405888557434, 4.204923629760742, 0],
            [-2.8420634269714355, 4.736772060394287, 0],
            [-4.204924583435059, 5.102417945861816, 0],
            [-5.501304626464844, 5.401582717895508, 0],
            [-5.667506694793701, 4.969455242156982, 0],
            [-5.733987808227539, 3.6065945625305176, 0],
            [-5.733988285064697, 2.376697063446045, 0],
            [-5.634267330169678, 1.6786457300186157, 0],
            [-5.7672295570373535, 1.0470755100250244, 0],
            [-5.9334306716918945, -0.2493036538362503, 0],
            [-5.501305103302002, -1.8116075992584229, 0],
            [-5.035937786102295, -2.8753042221069336, 0],
            [-4.969456672668457, -3.506873369216919, 0],
        ]
        #Not sure exactly how this happened, but all those points are off by
        #a scale factor
        for i in range(len(colon_points)):
            new_point = deepcopy(colon_points[i])
            colon_points[i] = [
                new_point[0] * 1.45 * zoom_out_factor + x_shift,
                new_point[1] * 1.45 * zoom_out_factor,
                new_point[2] * 1.45 * zoom_out_factor,
            ]


        sim_duration = 500
        start_delay = 0.5
        frames_per_time_step = 1

        #initial_creature_count = 10
        blue_count = 90
        green_count = 10
        initial_creatures = []
        for i in range(blue_count):
            new_creature = creature.Creature(
                color = 'creature_color_1',
                shape = 'shape1',
                size = '0.5'
            )
            initial_creatures.append(new_creature)
        for i in range(green_count):
            new_creature = creature.Creature(
                color = 'creature_color_2',
                shape = 'shape1',
                size = '0.5'
            )
            initial_creatures.append(new_creature)
        sim = drawn_world.DrawnWorld(
            name = 'limited_sim',
            location = [0, 0, 0],
            scale = 0.7,
            start_delay = start_delay,
            frames_per_time_step = frames_per_time_step,
            sim_duration = sim_duration,
            spin_creatures = True,
            initial_creatures = initial_creatures,
            creature_model = ['bacteria', 'biochem'],
            #save = True,
            #load = 'o_logistic2',
            overlap_okay = True,
            gene_updates = [
                #Other alleles
                ['shape', 'shape1', 'birth_modifier', 1, 0],
                ['size', '0.5', 'birth_modifier', 1, 0],
                ['shape', 'shape1', 'mutation_chance', 0, 0],
                ['size', '0.5', 'mutation_chance', 0, 0],
                #Color 1 initial settings
                ['color', 'creature_color_1', 'birth_modifier', 900, 0],
                ['color', 'creature_color_1', 'death_modifier', 10, 0],
                ['color', 'creature_color_1', 'replication_modifier', 0, 0],
                ['color', 'creature_color_1', 'mutation_chance', 0, 0],
                #Color 2 initial settings
                ['color', 'creature_color_2', 'birth_modifier', 100, 0],
                ['color', 'creature_color_2', 'death_modifier', 10, 0],
                ['color', 'creature_color_2', 'replication_modifier', 0, 0],
                ['color', 'creature_color_2', 'mutation_chance', 0, 0],
                #Antibiotic
                ['color', 'creature_color_1', 'birth_modifier', 900, 120],
                ['color', 'creature_color_1', 'death_modifier', 90, 120],
                ['color', 'creature_color_2', 'birth_modifier', 100, 120],
                ['color', 'creature_color_2', 'death_modifier', 20, 120],
                #Color 2 dominates
                ['color', 'creature_color_1', 'birth_modifier', 400, 180],
                ['color', 'creature_color_1', 'death_modifier', 10, 180],
                ['color', 'creature_color_2', 'birth_modifier', 600, 180],
                ['color', 'creature_color_2', 'death_modifier', 10, 180],


            ],
            world_bound_points = colon_points,
            bound_mode = 'points',
            show_world = False
        )


        sim.add_to_blender(appear_time = 0)

        healthy = import_object(
            'bacteria', 'biochem',
            location = [-21.5, 10, 0],
            scale = 6
        )
        apply_material(healthy.ref_obj.children[0], 'creature_color3')
        healthy_text = tex_bobject.TexBobject(
            '\\text{Healthy Bacteria}',
            location = [-21.5, 3, 0],
            centered = True,
            scale = 2,
            color = 'color2'
        )

        healthy.add_to_blender(appear_time = 0)
        healthy_text.add_to_blender(appear_time = 0)



        unhealthy = import_object(
            'bacteria', 'biochem',
            location = [-21.5, -5, 0],
            scale = 6
        )
        apply_material(unhealthy.ref_obj.children[0], 'creature_color7')
        clos = tex_bobject.TexBobject(
            '\\text{Clostridium}',
            color = 'color2',
            centered = True
        )
        diff = tex_bobject.TexBobject(
            '\\text{difficile}',
            color = 'color2',
            centered = True
        )
        unhealthy_text = tex_complex.TexComplex(
            clos, diff,
            location = [-21.5, -13, 0],
            centered = True,
            scale = 2,
            multiline = True,
        )
        unhealthy_text.add_to_blender(appear_time = 0)
        unhealthy.add_to_blender(appear_time = 0)

        #Prep for next scene
        to_disappear = []
        for i, thing in enumerate(to_disappear):
            thing.disappear(disappear_time = cues['end'] - (len(to_disappear) - 1 - i) * 0.05)


        """print()
        points = [
            [2, 0, 0],
            [0, 0, 0],
            [-0.1, 0.5, 0],
            [-0.4594877792145916, -5.443530545247961, 0.0],
            [-5.066866886029154, -4.334055768904699, 0],
            [5, 4, 0]
        ]
        for point in points:
            print(sim.is_point_in_bounds(point))
            print()
        print()"""
