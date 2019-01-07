import collections
import math
from random import random, uniform, randrange
import bpy

import imp
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
import table_bobject
imp.reload(table_bobject)

import helpers
imp.reload(helpers)
from helpers import *

BLOB_VOLUME_DENSITY = 0.04

class SelfishGene(Scene):
    def __init__(self):
        self.subscenes = collections.OrderedDict([
            ('card', {'duration': 10})
        ])
        super().__init__()

    def play(self):
        super().play()

        #self.intro()
        self.quote()
        #self.replicating_creatures()
        #self.dna()
        #self.sexual_reproduction()
        #self.conjugation()
        #self.dna_is_what_replicates()
        #self.gene()
        #self.strategies()
        #self.end_card()
        #self.thumbnail()
        #self.banner_angled()

    def intro(self):
        sg = svg_bobject.SVGBobject(
            "selfish_gene_century",
            "selfish_gene_century_italic_bold",
            #location = (-5, 3.75, 0), #Centered position
            #scale = 0.26, #Centered scale
            location = [0, 3.25, 0],
            scale = 6,
            color = 'color2',
            centered = True
        )
        sg.add_to_blender(appear_time = 0)
        sg.morph_figure(1, start_time = 1)
        sg.move_to(new_location = [-0.1, 3.15, 0], start_time = 1)

        for i in range(7):
            sg.lookup_table[1][i].color_shift(
                color = COLORS_SCALED[5],
                start_time = 1,
                duration_time = None
            )

        sg.move_to(
            new_location = [-8, 5.25, 0],
            new_scale = 3,
            start_time = 2
        )

        bpy.ops.mesh.primitive_plane_add()
        rec = bpy.context.object
        rec.scale[0] = 8 / 2
        rec.scale[1] = 8 * 9 / 16 / 2
        rec.location = [0, 0, 0]
        loc = [-9.5, -4.75, 0]
        rec_bobj1 = bobject.Bobject(objects = [rec], location = loc)
        rec_bobj1.add_to_blender(appear_time = 3)
        dg = tex_bobject.TexBobject(
            "\\text{Define \"gene\"}",
            location = [-9.5, -1.75, 0],
            centered = True,
            scale = 1
        )
        dg.add_to_blender(appear_time = 3)


        bpy.ops.mesh.primitive_plane_add()
        rec = bpy.context.object
        rec.scale[0] = 8 / 2
        rec.scale[1] = 8 * 9 / 16 / 2
        rec.location = [0, 0, 0]
        loc = [0, -4.75, 0]
        rec_bobj2 = bobject.Bobject(objects = [rec], location = loc)
        rec_bobj2.add_to_blender(appear_time = 4)
        gs = tex_bobject.TexBobject(
            "\\text{Explore strategies}",
            location = [0, -1.75, 0],
            centered = True,
            scale = 1
        )
        gs.add_to_blender(appear_time = 4)

        bpy.ops.mesh.primitive_plane_add()
        rec = bpy.context.object
        rec.scale[0] = 8 / 2
        rec.scale[1] = 8 * 9 / 16 / 2
        rec.location = [0, 0, 0]
        loc = [9.5, -4.75, 0]
        rec_bobj3 = bobject.Bobject(objects = [rec], location = loc)
        rec_bobj3.add_to_blender(appear_time = 5)
        sa = tex_bobject.TexBobject(
            "\\text{Simulate strategies}",
            location = [9.5, -1.75, 0],
            centered = True,
            scale = 1
        )
        sa.add_to_blender(appear_time = 5)

        to_disappear = [
            sg, dg, rec_bobj1, gs, rec_bobj2, sa, rec_bobj3
        ]
        for i, thing in enumerate(to_disappear):
            thing.disappear(disappear_time = 6.5 - (len(to_disappear) - 1 - i) * 0.05)

    def quote(self):
        a = tex_bobject.TexBobject(
            "\\text{\"I'm not much of a diplomat.}",
            centered = True,
        )
        b = tex_bobject.TexBobject(
            "\\text{Actually, I think part of}",
            centered = True,
        )
        c = tex_bobject.TexBobject(
            "\\text{my trouble is I love truth}",
            centered = True,
        )
        d = tex_bobject.TexBobject(
            "\\text{too much.\"}",
            centered = True,
        )

        complex = tex_complex.TexComplex(
            a, b, c, d,
            multiline = True,
            location = [0, 1, 0],
            scale = 2,
            align_y = 'center'
        )
        complex.add_to_blender(
                appear_time = 0,
                animate = False,
                subbobject_timing = [0, 5, 10, 15]
        )

        rd = tex_bobject.TexBobject(
            "- \\text{Richard Dawkins}",
            centered = True,
            scale = 2,
            location = [3.25, -5.9, 0]
        )
        rd.add_to_blender(
            appear_time = 1
        )

        for i in range(1, 23):
            a.lookup_table[0][i].color_shift(
                color = COLORS_SCALED[5],
                start_time = 2,
                duration_time = None
            )

    def replicating_creatures(self):

        cam_bobj, cam_swivel = cam_and_swivel(
            cam_location = [0, 0, 32.8],
            cam_rotation_euler = [0, 0, 0],
            cam_name = "Camera Bobject",
            swivel_location = [0, 0, 0],
            swivel_rotation_euler = [0, 0, 0],
            swivel_name = 'Cam swivel',
            #control_sun = True
        )
        cam_swivel.add_to_blender(appear_time = -1)


        def blob_chain():
            blob1 = import_object(
                'boerd_blob', 'creatures',
                location = [-5, 0, 0],
                scale = 4,
                wiggle = True
            )
            apply_material(blob1.ref_obj.children[0].children[0], 'creature_color3')
            blob1.add_to_blender(appear_time = 48.5)

            last_blob = blob1
            i = 0
            num_cres = 6
            while i < num_cres - 1:
                next_blob = import_object(
                    'boerd_blob', 'creatures',
                    location = last_blob.ref_obj.location,
                    scale = 4,
                    wiggle = True
                )
                apply_material(next_blob.ref_obj.children[0].children[0], 'creature_color3')


                if i == num_cres - 2:
                    next_blob.blob_wave(start_time = 40, duration = 100)

                    meta = next_blob.ref_obj.children[0].children[0]
                    apply_material(meta, 'creature_color7')

                    mat_copy = meta.material_slots[0].material.copy()
                    meta.active_material = mat_copy
                    node_tree = mat_copy.node_tree
                    out = node_tree.nodes['Material Output']
                    princ = node_tree.nodes['Principled BSDF']
                    trans = node_tree.nodes.new(type = 'ShaderNodeBsdfTransparent')
                    mix = node_tree.nodes.new(type = 'ShaderNodeMixShader')

                    #scat = node_tree.nodes.new(type = 'ShaderNodeVolumeScatter')
                    #absorb = node_tree.nodes.new(type = 'ShaderNodeVolumeAbsorption')
                    #emit = node_tree.nodes.new(type = 'ShaderNodeEmission')
                    #add1 = node_tree.nodes.new(type = 'ShaderNodeAddShader')
                    #add2 = node_tree.nodes.new(type = 'ShaderNodeAddShader')

                    node_tree.links.new(mix.outputs[0], out.inputs[0])
                    node_tree.links.new(princ.outputs[0], mix.inputs[1])
                    node_tree.links.new(trans.outputs[0], mix.inputs[2])

                    #node_tree.links.new(add1.outputs[0], out.inputs[1])
                    #node_tree.links.new(emit.outputs[0], add1.inputs[0])
                    #node_tree.links.new(add2.outputs[0], add1.inputs[1])
                    #node_tree.links.new(scat.outputs[0], add2.inputs[0])
                    #node_tree.links.new(absorb.outputs[0], add2.inputs[1])

                    #for node in [scat, absorb, emit]:
                    #    node.inputs[0].default_value = COLORS_SCALED[6]
                    #    node.inputs[1].default_value = BLOB_VOLUME_DENSITY

                    mix.inputs[0].default_value = 0
                    mix.inputs[0].keyframe_insert(data_path = 'default_value', frame = 59 * FRAME_RATE)
                    mix.inputs[0].default_value = 1
                    mix.inputs[0].keyframe_insert(data_path = 'default_value', frame = 60 * FRAME_RATE)


                next_blob.add_to_blender(appear_time = i + 50.5)
                next_blob.move_to(
                    new_location = [
                        next_blob.ref_obj.location[0] + 10,
                        next_blob.ref_obj.location[1],
                        next_blob.ref_obj.location[2]
                    ],
                    start_time = i + 50.5
                )

                '''if i < num_cres - 2:
                    next_blob.disappear(disappear_time = num_cres + 5)'''

                last_blob = next_blob
                i += 1

            cam_swivel.add_to_blender(appear_time = -1)
            cam_swivel.move_to(
                new_location = [10 * (num_cres - 2), 0, 0],
                start_time = 50.5,
                end_time = num_cres + 50.5
            )

            cam_swivel.move_to(
                new_location = [10 * (num_cres - 2) + 4.85, 0, 0],
                start_time = 59,
                end_time = 60
            )
            cam_bobj.move_to(
                new_location = [0, 0, 4],
                start_time = 59,
                end_time = 60
            )

        blob_chain()

    def dna(self):

        cam_bobj, cam_swivel = cam_and_swivel(
            cam_location = [0, -1.4, 7], #32.8
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
            location = [0, -1.5, 0]
        )
        dna1_1.add_to_blender(
            appear_time = 0,
            animate = False,
        )

        dna2_1 = import_object(
            'dna_strand_2', 'biochem',
            scale = 1.5,
            location = [0, -1.5, 0]
        )
        dna2_1.add_to_blender(
            appear_time = 0,
            animate = False
        )

        dna1_1.de_explode(
            start_time = 61,
            duration = 3,
        )

        dna2_1.de_explode(
            start_time = 65,
            duration = 3,
        )

        cam_bobj.move_to(
            new_location = [0, -0.8, 10.7],
            start_time = 66,
            end_time = 67
        )
        dtex = tex_bobject.TexBobject(
            '\\text{Deoxyribonucleic Acid}',
            '\\text{DNA}',
            location = [0, 1.1, 0],
            centered = True
        )
        dtex.add_to_blender(appear_time = 67)
        dtex.morph_figure(1, start_time = 69.5)

        for d in [dna1_1, dna2_1]:
            d.spin(start_time = 0, spin_rate = 0.05)

        to_disappear = [dna1_1, dna2_1, dtex]
        for thing in to_disappear:
            thing.disappear(disappear_time = 71.5)

        for strand in [dna1_1, dna2_1]:#, dna1_2, dna2_2]:
            strand.tweak_colors_recursive()

    def sexual_reproduction(self):
        cam_bobj, cam_swivel = cam_and_swivel(
            cam_location = [0, 0, 32.8],
            cam_rotation_euler = [0, 0, 0],
            cam_name = "Camera Bobject",
            swivel_location = [0, 0, 0],
            swivel_rotation_euler = [0, 0, 0],
            swivel_name = 'Cam swivel',
            #control_sun = True
        )
        cam_swivel.add_to_blender(appear_time = -1)

        print('blob1 stuff')
        blob1 = import_object(
            'boerd_blob', 'creatures',
            location = [-19, 0, 0],
            scale = 3,
            wiggle = True
        )
        meta1 = blob1.ref_obj.children[0].children[0]
        apply_material(meta1, 'creature_color3')
        blob1.add_to_blender(appear_time = -1)
        eyes = [
            blob1.ref_obj.children[0].children[-2],
            blob1.ref_obj.children[0].children[-3],
        ]
        for eye in eyes:
            eye.scale = [
                1.3 * eye.scale[0],
                1.3 * eye.scale[1],
                1.3 * eye.scale[2],
            ]

        mat_copy1 = meta1.material_slots[0].material.copy()
        meta1.active_material = mat_copy1
        node_tree = mat_copy1.node_tree
        out1 = node_tree.nodes['Material Output']
        princ1 = node_tree.nodes['Principled BSDF']
        trans1 = node_tree.nodes.new(type = 'ShaderNodeBsdfTransparent')
        mix1 = node_tree.nodes.new(type = 'ShaderNodeMixShader')

        scat1 = node_tree.nodes.new(type = 'ShaderNodeVolumeScatter')
        absorb1 = node_tree.nodes.new(type = 'ShaderNodeVolumeAbsorption')
        emit1 = node_tree.nodes.new(type = 'ShaderNodeEmission')
        add1 = node_tree.nodes.new(type = 'ShaderNodeAddShader')
        add2 = node_tree.nodes.new(type = 'ShaderNodeAddShader')

        node_tree.links.new(mix1.outputs[0], out1.inputs[0])
        node_tree.links.new(princ1.outputs[0], mix1.inputs[1])
        node_tree.links.new(trans1.outputs[0], mix1.inputs[2])

        node_tree.links.new(add1.outputs[0], out1.inputs[1])
        node_tree.links.new(emit1.outputs[0], add1.inputs[0])
        node_tree.links.new(add2.outputs[0], add1.inputs[1])
        node_tree.links.new(scat1.outputs[0], add2.inputs[0])
        node_tree.links.new(absorb1.outputs[0], add2.inputs[1])

        for node in [scat1, absorb1, emit1]:
            node.inputs[0].default_value = princ1.inputs[0].default_value
            node.inputs[1].default_value = BLOB_VOLUME_DENSITY

        dna_scale = 0.75
        dna11 = import_object(
            'dna_two_strand_low_res', 'biochem',
            scale = dna_scale,
            location = add_lists_by_element(blob1.ref_obj.location, [-0.1, 0, 0])
        )
        dna12 = import_object(
            'dna_two_strand_low_res', 'biochem',
            scale = dna_scale,
            location = add_lists_by_element(blob1.ref_obj.location, [-0.7, -1.5, 0]),
            rotation_euler = [0, 0, 20 * math.pi / 180]
        )
        '''dna32 = import_object(
            'dna_two_strand_low_res', 'biochem',
            scale = dna_scale,
            location = add_lists_by_element(blob1.ref_obj.location, [-0.7, -1.5, 0]),
            rotation_euler = [0, 0, 20 * math.pi / 180]
        )'''
        dna13 = import_object(
            'dna_two_strand_low_res', 'biochem',
            scale = dna_scale,
            location = add_lists_by_element(blob1.ref_obj.location, [0.5, -1.5, 0]),
            rotation_euler = [0, 0, -20 * math.pi / 180]
        )
        '''dna33 = import_object(
            'dna_two_strand_low_res', 'biochem',
            scale = dna_scale,
            location = add_lists_by_element(blob1.ref_obj.location, [0.5, -1.5, 0]),
            rotation_euler = [0, 0, -20 * math.pi / 180]
        )'''

        dna_set1 = [
            dna11,
            dna12,
            dna13
        ]
        sign = 1
        for d in dna_set1:
            d.add_to_blender(appear_time = -1)
            d.spin(start_time = 0, spin_rate = sign * 0.05)
            sign *= -1

        def blob1_move():
            blob1.move_to(
                new_angle = [0, math.pi / 2, 0],
                start_time = 71 - 0.2# st + 9.8
            )
            blob1.move_to(
                new_angle = [0, 0, 0],
                start_time = 73 - 0.3#st + 10.7
            )
            blob1.eat_animation(
                start_frame = 72.5 * FRAME_RATE,
                end_frame = 75 * FRAME_RATE
            )
            blob1.blob_scoop(
                start_time = 72.5,
                duration = 2.5,
                top_pause_time = 1
            )

            for thing in [blob1] + dna_set1:
                thing.move_to(
                    displacement = [13, 0, 0],
                    start_time = 71,
                    end_time = 73
                )

        blob1_move()

        print('blob2 stuff')
        blob2 = import_object(
            'boerd_blob', 'creatures',
            location = [19, 0.35, 0],
            scale = 3.4,
            wiggle = True
        )
        meta2 = blob2.ref_obj.children[0].children[0]
        apply_material(meta2, 'creature_color4')
        blob2.add_to_blender(appear_time = -1)
        eyes = [
            blob2.ref_obj.children[0].children[-2],
            blob2.ref_obj.children[0].children[-3],
        ]
        for eye in eyes:
            eye.scale = [
                0.8 * eye.scale[0],
                0.8 * eye.scale[1],
                0.8 * eye.scale[2],
            ]

        mat_copy2 = meta2.material_slots[0].material.copy()
        meta2.active_material = mat_copy2
        node_tree = mat_copy2.node_tree
        out2 = node_tree.nodes['Material Output']
        princ2 = node_tree.nodes['Principled BSDF']
        trans2 = node_tree.nodes.new(type = 'ShaderNodeBsdfTransparent')
        mix2 = node_tree.nodes.new(type = 'ShaderNodeMixShader')

        scat2 = node_tree.nodes.new(type = 'ShaderNodeVolumeScatter')
        absorb2 = node_tree.nodes.new(type = 'ShaderNodeVolumeAbsorption')
        emit2 = node_tree.nodes.new(type = 'ShaderNodeEmission')
        add1 = node_tree.nodes.new(type = 'ShaderNodeAddShader')
        add2 = node_tree.nodes.new(type = 'ShaderNodeAddShader')

        node_tree.links.new(mix2.outputs[0], out2.inputs[0])
        node_tree.links.new(princ2.outputs[0], mix2.inputs[1])
        node_tree.links.new(trans2.outputs[0], mix2.inputs[2])

        node_tree.links.new(add1.outputs[0], out2.inputs[1])
        node_tree.links.new(emit2.outputs[0], add1.inputs[0])
        node_tree.links.new(add2.outputs[0], add1.inputs[1])
        node_tree.links.new(scat2.outputs[0], add2.inputs[0])
        node_tree.links.new(absorb2.outputs[0], add2.inputs[1])

        for node in [scat2, absorb2, emit2]:
            node.inputs[0].default_value = princ2.inputs[0].default_value
            node.inputs[1].default_value = BLOB_VOLUME_DENSITY

        dna21 = import_object(
            'dna_two_strand_low_res', 'biochem',
            scale = dna_scale,
            location = add_lists_by_element(blob2.ref_obj.location, [-0.1, 0, 0])
        )
        dna22 = import_object(
            'dna_two_strand_low_res', 'biochem',
            scale = dna_scale,
            location = add_lists_by_element(blob2.ref_obj.location, [-0.7, -1.5, 0]),
            rotation_euler = [0, 0, 20 * math.pi / 180]
        )
        dna23 = import_object(
            'dna_two_strand_low_res', 'biochem',
            scale = dna_scale,
            location = add_lists_by_element(blob2.ref_obj.location, [0.5, -1.5, 0]),
            rotation_euler = [0, 0, -20 * math.pi / 180]
        )

        dna_set2 = [
            dna21,
            dna22,
            dna23
        ]
        sign = -1
        for d in dna_set2:
            d.add_to_blender(appear_time = -1)
            d.spin(start_time = 0, spin_rate = sign * 0.05)
            sign *= -1

        def blob2_move():
            blob2.move_to(
                new_angle = [0, -math.pi / 2, 0],
                start_time = 71 - 0.2# st + 9.8
            )
            blob2.move_to(
                new_angle = [0, 0, 0],
                start_time = 73 - 0.3#st + 10.7
            )
            blob2.eat_animation(
                start_frame = 72.5 * FRAME_RATE,
                end_frame = 75 * FRAME_RATE
            )
            blob2.blob_scoop(
                start_time = 72.5,
                duration = 2.5,
                top_pause_time = 1
            )

            for thing in [blob2] + dna_set2:
                thing.move_to(
                    displacement = [-13, 0, 0],
                    start_time = 71,
                    end_time = 73
                )

        blob2_move()

        heart = import_object(
            'heart', 'misc',
            location = [0, 4, 0],
            scale = 3
        )
        apply_material(heart.ref_obj.children[0], 'creature_color6')
        heart.add_to_blender(appear_time = 73)
        heart.move_to(
            new_angle = [0, 10 * math.pi, 0],
            start_time = 72,
            end_time = 74
        )

        mix1.inputs[0].default_value = 0
        mix1.inputs[0].keyframe_insert(data_path = 'default_value', frame = 75 * FRAME_RATE)
        mix1.inputs[0].default_value = 1
        mix1.inputs[0].keyframe_insert(data_path = 'default_value', frame = 76 * FRAME_RATE)
        #mix1.inputs[0].keyframe_insert(data_path = 'default_value', frame = 300)
        #mix1.inputs[0].default_value = 0
        #mix1.inputs[0].keyframe_insert(data_path = 'default_value', frame = 360)


        mix2.inputs[0].default_value = 0
        mix2.inputs[0].keyframe_insert(data_path = 'default_value', frame = 75 * FRAME_RATE)
        mix2.inputs[0].default_value = 1
        mix2.inputs[0].keyframe_insert(data_path = 'default_value', frame = 76 * FRAME_RATE)
        #mix2.inputs[0].keyframe_insert(data_path = 'default_value', frame = 300)
        #mix2.inputs[0].default_value = 0
        #mix2.inputs[0].keyframe_insert(data_path = 'default_value', frame = 360)

        for thing in [blob1, blob2] + dna_set1 + dna_set2:
            thing.move_to(
                displacement = [0, 3.5, 0],
                start_time = 75.5
            )
        heart.move_to(
            #displacement = [0, 15, 0],
            new_location = [0, 5, 0],
            new_scale = 2,
            start_time = 75.5
        )

        source_blobs = [blob1, blob2]
        dest_blobs = []
        inheritance_matrix = [
            [1, 0, 0],
            [0, 1, 1],
            [1, 1, 0],
            [0, 0, 1],
        ]
        displacements = [
            [-0.1, 0, 0],
            [-0.7, -1.5, 0],
            [0.5, -1.5, 0]
        ]
        new_dna = []

        for i, a in enumerate(inheritance_matrix):
            print('Copying DNA to child ' + str(i))
            blob = import_object(
                'boerd_blob', 'creatures',
                location = [-9 + 6 * i, -4, 0],
                scale = 3 + a[1] * 0.4,
                wiggle = True
            )
            meta = blob.ref_obj.children[0].children[0]
            meta.active_material = source_blobs[a[0]].ref_obj.children[0].children[0].active_material

            eyes = [
                blob.ref_obj.children[0].children[-2],
                blob.ref_obj.children[0].children[-3],
            ]
            for eye in eyes:
                eye.scale = [
                    source_blobs[a[2]].ref_obj.children[0].children[-2].scale[0],
                    source_blobs[a[2]].ref_obj.children[0].children[-2].scale[1],
                    source_blobs[a[2]].ref_obj.children[0].children[-2].scale[2],
                ]

            blob.add_to_blender(appear_time = 76 + i / 2)
            dest_blobs.append(blob)

            for j in range(3):
                dna = import_object(
                    'dna_two_strand_low_res', 'biochem',
                    scale = dna_scale,
                    location = add_lists_by_element(
                        source_blobs[a[j]].ref_obj.location,
                        displacements[j]
                    )
                )
                dna.add_to_blender(appear_frame = 0)
                dna.de_explode(
                    start_time = 76 + i / 2,
                    duration = 0.5
                )
                dna.move_to(
                    start_time = 76.5 + i / 2,
                    new_location = add_lists_by_element(
                        blob.ref_obj.location,
                        displacements[j]
                    )
                )

                new_dna.append(dna)


        sign = -1
        for d in new_dna:
            d.spin(start_time = 0, spin_rate = sign * 0.05)
            sign *= -1


        mix1.inputs[0].keyframe_insert(data_path = 'default_value', frame = 79 * FRAME_RATE)
        mix1.inputs[0].default_value = 1
        mix1.inputs[0].keyframe_insert(data_path = 'default_value', frame = 79.5 * FRAME_RATE)


        mix2.inputs[0].keyframe_insert(data_path = 'default_value', frame = 79 * FRAME_RATE)
        mix2.inputs[0].default_value = 1
        mix2.inputs[0].keyframe_insert(data_path = 'default_value', frame = 79.5 * FRAME_RATE)


        top = source_blobs + dna_set1 + dna_set2 + [heart]
        for thing in top:
            thing.move_to(
                displacement = [0, 16, 0],
                start_time = 79.5,
                end_time = 80.5
            )

        bot = dest_blobs + new_dna
        for thing in bot:
            thing.move_to(
                displacement = [0, -16, 0],
                start_time = 79.5,
                end_time = 80.5
            )

        for strand in dna_set1 + dna_set2 + new_dna:
            strand.tweak_colors_recursive()

    def conjugation(self):
        cam_bobj, cam_swivel = cam_and_swivel(
            cam_location = [0, 0, 32.8],
            cam_rotation_euler = [0, 0, 0],
            cam_name = "Camera Bobject",
            swivel_location = [0, 0, 0],
            swivel_rotation_euler = [0, 0, 0],
            swivel_name = 'Cam swivel',
            #control_sun = True
        )
        cam_swivel.add_to_blender(appear_time = -1)

        bac1 = import_object(
            'bacteria', 'biochem',
            scale = 7.5,
            location = [-30, 10, 0],
            rotation_euler = [0, 0, 0]
        )
        bac1.add_to_blender(appear_time = -1)
        bac1.move_to(
            new_location = [-4.3, -1.3, 0],
            new_angle = [0, math.pi, -130 * math.pi / 180],
            start_time = 77.7,
            end_time = 83.5
        )

        bac1.move_to(
            new_location = [25, -23, 0],
            new_angle = [0, 2 * math.pi, -260 * math.pi / 180],
            start_time = 86.5,
            end_time = 92.3
        )

        bac2 = import_object(
            'bacteria', 'biochem',
            scale = 7.5,
            location = [30, -10, 0],
            rotation_euler = [0, math.pi / 2, 100 * math.pi / 180]
        )
        bac2.add_to_blender(appear_time = -1)
        bac2.move_to(
            new_location = [4.3, 1.3, 0],
            new_angle = [0, 0 * math.pi, 230 * math.pi / 180],
            start_time = 77.7,
            end_time = 83.5
        )

        bac2.move_to(
            new_location = [6, 23, 0],
            new_angle = [0, -1 * math.pi, 270 * math.pi / 180],
            start_time = 86.5,
            end_time = 92.3
        )


        cyl = import_object(
            'one_side_cylinder', 'primitives',
            rotation_euler = [0, math.pi / 2, 0],
            location = [0, -0.2, 0],
            scale = [0.05, 0.05, 0]
        )
        cyl.ref_obj.parent = bac2.ref_obj
        cyl.add_to_blender(appear_time = 0)
        apply_material(cyl.ref_obj.children[0], 'trans_color3', intensity = 0.2)


        cyl.move_to(
            new_scale = [0.05, 0.05, 1],
            start_time = 83.5,
            end_time = 84.5
        )
        cyl.move_to(
            new_scale = [0.05, 0.05, 0],
            start_time = 85.5,
            end_time = 86.5
        )

        dna = import_object(
            'dna_two_strand', 'biochem',
            location = [0, -0.2, 0],
            scale = 0.04,
            rotation_euler = [0, 0, math.pi / 2]
        )
        dna.ref_obj.parent = bac2.ref_obj
        dna.add_to_blender(appear_time = 0)
        dna.move_to(
            start_time = 84,
            end_time = 86,
            new_location = [1, -0.2, 0]
        )
        dna.disappear(disappear_time = 86)
        dna.spin(
            start_time = 0,
            spin_rate = 1
        )

        cam_bobj.move_to(
            new_location = [1, -0.5, 5],
            start_time = 83.5,
            end_time = 84.5
        )
        cam_bobj.move_to(
            new_location = [0, 0, 32.8],
            start_time = 85.5,
            end_time = 86.5
        )

        dna.tweak_colors_recursive()

    def dna_is_what_replicates(self):
        cam_bobj, cam_swivel = cam_and_swivel(
            cam_location = [0, -1.4, 7], #32.8
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
            appear_time = 91
        )

        dna2_1 = import_object(
            'dna_strand_2', 'biochem',
            scale = 1.5,
            location = [-0.25, -1.5, 0]
        )
        dna2_1.add_to_blender(
            appear_time = 91
        )

        '''cam_bobj.move_to(
            new_location = [0, -0.8, 10.7],
            start_time = 66,
            end_time = 67
        )'''

        #def replicate():
        blob1 = import_object(
            'boerd_blob', 'creatures',
            location = [0, 0, 0],
            scale = 6,
            wiggle = True
        )
        meta = blob1.ref_obj.children[0].children[0]
        apply_material(meta, 'creature_color7')
        blob1.add_to_blender(appear_time = 93.5, animate = False)

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

        mix.inputs[0].default_value = 1
        for node in [scat, absorb, emit]:
            node.inputs[0].default_value = princ.inputs[0].default_value
            node.inputs[1].default_value = 0
            node.inputs[1].keyframe_insert(data_path = 'default_value', frame = 93.5 * FRAME_RATE)
            node.inputs[1].default_value = BLOB_VOLUME_DENSITY
            node.inputs[1].keyframe_insert(data_path = 'default_value', frame = 94 * FRAME_RATE)

        cam_bobj.move_to(
            new_location = [0, 0, 32.8],
            start_time = 92.5,
            end_time = 93.5
        )

        blob2 = import_object(
            'boerd_blob', 'creatures',
            location = [0, 0, 0],
            scale = 6,
            wiggle = True
        )
        meta2 = blob2.ref_obj.children[0].children[0]
        blob2.add_to_blender(appear_time = 95.5)


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
            node.inputs[1].keyframe_insert(data_path = 'default_value', frame = 95.5 * FRAME_RATE)
            node.inputs[1].default_value = BLOB_VOLUME_DENSITY
            node.inputs[1].keyframe_insert(data_path = 'default_value', frame = 96 * FRAME_RATE)

        #Eyes
        eyel_1 = blob1.ref_obj.children[0].children[-2]
        eye_mat_copy_1 = eyel_1.material_slots[0].material.copy()
        eyel_1.active_material = eye_mat_copy_1
        eyer_1 = blob1.ref_obj.children[0].children[-3]
        eyer_1.active_material = eye_mat_copy_1

        node_tree = eye_mat_copy_1.node_tree
        trans = node_tree.nodes.new(type = 'ShaderNodeBsdfTransparent')
        mix = node_tree.nodes.new(type = 'ShaderNodeMixShader')
        out = node_tree.nodes['Material Output']
        diff = node_tree.nodes['Diffuse BSDF']

        node_tree.links.new(mix.outputs[0], out.inputs[0])
        node_tree.links.new(trans.outputs[0], mix.inputs[1])
        node_tree.links.new(diff.outputs[0], mix.inputs[2])

        mix.inputs[0].default_value = 0
        mix.inputs[0].keyframe_insert(data_path = 'default_value', frame = 93.5 * FRAME_RATE)
        mix.inputs[0].default_value = 1
        mix.inputs[0].keyframe_insert(data_path = 'default_value', frame = 94.5 * FRAME_RATE)

        eyel_2 = blob2.ref_obj.children[0].children[-2]
        eye_mat_copy_2 = eyel_2.material_slots[0].material.copy()
        eyel_2.active_material = eye_mat_copy_2
        eyer_2 = blob2.ref_obj.children[0].children[-3]
        eyer_2.active_material = eye_mat_copy_2

        node_tree = eye_mat_copy_2.node_tree
        trans = node_tree.nodes.new(type = 'ShaderNodeBsdfTransparent')
        mix = node_tree.nodes.new(type = 'ShaderNodeMixShader')
        out = node_tree.nodes['Material Output']
        diff = node_tree.nodes['Diffuse BSDF']

        node_tree.links.new(mix.outputs[0], out.inputs[0])
        node_tree.links.new(trans.outputs[0], mix.inputs[1])
        node_tree.links.new(diff.outputs[0], mix.inputs[2])

        mix.inputs[0].default_value = 0
        mix.inputs[0].keyframe_insert(data_path = 'default_value', frame = 95.5 * FRAME_RATE)
        mix.inputs[0].default_value = 1
        mix.inputs[0].keyframe_insert(data_path = 'default_value', frame = 96 * FRAME_RATE)

        dna2_1.move_to(new_location = [1.25, -1.5, 0], start_time = 93.5)
        dna1_1.move_to(new_location = [-1.75, -1.5, 0], start_time = 93.5)

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
            start_time = 94,
            duration = 1,
        )
        dna2_2.de_explode(
            start_time = 94,
            duration = 1,
        )

        blob2.move_to(new_location = [6, 0, 0], start_time = 95.5)
        blob1.move_to(new_location = [-6, 0, 0], start_time = 95.5)
        dna1_1.move_to(new_location = [-6, -1.5, 0], start_time = 95.5)
        dna2_1.move_to(new_location = [6, -1.5, 0], start_time = 95.5)
        dna1_2.move_to(new_location = [6, -1.5, 0], start_time = 95.5)
        dna2_2.move_to(new_location = [-6, -1.5, 0], start_time = 95.5)

        for d in [dna1_1, dna2_1, dna1_2, dna2_2]:
            d.spin(start_time = 0, spin_rate = 0.05)
            d.move_to(
                displacement = [0, 1.5, 0],
                start_time = 97
            )

        to_disappear = [dna1_1, dna2_1, dna1_2, dna2_2, blob1, blob2]
        for thing in to_disappear:
            thing.disappear(disappear_time = 97.5)

        for strand in [dna1_1, dna2_1, dna1_2, dna2_2]:
            strand.tweak_colors_recursive()

    def gene(self):

        def text():

            def gene_def():
                gene = tex_bobject.TexBobject(
                    '\\text{Gene?}',
                    '\\text{Gene:}',
                    centered = True,
                    scale = 5
                )
                gene.add_to_blender(appear_time = 98.5)

                #move to top and morph to definition
                gene.morph_figure(1, start_time = 100.5)
                gene.move_to(
                    new_location = [-11, 6.5, 0],
                    new_scale = 2,
                    start_time = 100.5
                )

                gene_def1 = tex_bobject.TexBobject(
                    '\\text{A section of DNA}',
                    '\\text{A section of DNA that lives inside a creature}',
                    '\\text{A } pattern \\text{ of DNA that lives inside a creature}',
                    '\\text{A } pattern \\text{ of DNA whose } copies \\text{ exist inside creatures}',
                    scale = 1
                )
                gene_def2 = tex_bobject.TexBobject(
                    '\\text{and determines one trait}',
                    '\\text{and determines one trait?}',
                    '\\text{and determines one trait}',
                    '\\text{and determine one trait}',
                    '\\text{and determine one trait. The } unit \\text{ of natural selection.}',
                    scale = 1
                )
                gene_def = tex_complex.TexComplex(
                    gene_def1,
                    multiline = True,
                    scale = 1,
                    location = [-10.5, 4.75, 0]
                )
                gene_def.add_to_blender(appear_time = 102, animate = False)

                gene_def1.morph_figure(1, start_time = 103)

                gene_def.add_tex_bobject(gene_def2)
                gene_def2.add_to_blender(appear_time = 104.5)
                gene_def.arrange_tex_bobjects(start_time = 104.5)

                gene_def2.morph_figure(1, start_time = 121)

                gene_def2.morph_figure(2, start_time = 160)

                gene_def1.morph_figure(2, start_time = 172.25)
                gene_def1.morph_figure(3, start_time = 174.25)
                gene_def2.morph_figure(3, start_time = 174.25)
                for i in range(1, 8):
                    char = gene_def1.lookup_table[2][i]
                    char.color_shift(
                        start_time = 172.25,
                        color = COLORS_SCALED[5],
                        duration_time = None
                    )

                for i in range(18, 24):
                    char = gene_def1.lookup_table[3][i]
                    char.color_shift(
                        start_time = 174.25,
                        color = COLORS_SCALED[5],
                        duration_time = None
                    )

                gene_def2.morph_figure(4, start_time = 187)

                for i in range(24, 28):
                    char = gene_def2.lookup_table[4][i]
                    char.color_shift(
                        start_time = 192.75,
                        color = COLORS_SCALED[5],
                        duration_time = None
                    )


            def term_flurry():
                strings = [
                    '\\text{mRNA}',
                    '\\text{tRNA}',
                    '\\text{rRNA}',
                    '\\text{Ribosomes}',
                    '\\text{Transcription}',
                    '\\text{Proteins}',
                    '\\text{Codons}',
                    '\\substack{\\text{Everything protiens do} \\\\ \\text{once they exist} }',
                ]
                tex_bobjs = []
                for string in strings:
                    t_bobj = tex_bobject.TexBobject(
                        string,
                        scale = 3,
                        centered = True,
                        location = [uniform(-1, 1) * 10, 20 + random() * 40, 0],
                    )
                    t_bobj.add_to_blender(appear_time = 0)
                    t_bobj.spin(start_frame = 0, axis = 2, spin_rate = uniform(-1, 1))
                    t_bobj.move_to(
                        displacement = [0, -80, 0],
                        start_time = 138,
                        end_time = 141
                    )

            #gene_def()
            term_flurry()

        def dna_stuff():
            gene1 = import_object(
                'dna_two_strand', 'biochem',
                location = [0, -2.75, 0],
                rotation_euler = [0, 0, 25 * math.pi / 180],
                scale = 4
            )
            gene1.add_to_blender(appear_time = 100.5)

            blob = import_object(
                'boerd_blob', 'creatures',
                location = [-9, -2.75, 0],
                scale = 4.5,
                wiggle = True
            )
            apply_material(blob.ref_obj.children[0].children[0], 'creature_color3')
            blob.add_to_blender(appear_time = 104)

            scale = 1
            arrow1 = gesture.Gesture(
                gesture_series = [
                    {
                        'type': 'arrow',
                        'points': {
                            'tail': (2 / scale, -2.75 / scale, 0),
                            'head': (6 / scale, -2.75 / scale, 0)
                        }
                    },
                    {
                        'type': 'arrow',
                        'points': {
                            'tail': (-2 / scale, 0.5 / scale, 0),
                            'head': (2 / scale, 0.5 / scale, 0)
                        }
                    },
                ],
                scale = scale,
            )
            trait1 = tex_bobject.TexBobject(
                '\\text{Trait}',
                location = [7, -2.75, 0],
                scale = 2,
            )

            one_trait_time = 105
            arrow1.add_to_blender(appear_time = one_trait_time)
            trait1.add_to_blender(appear_time = one_trait_time)
            gene1.move_to(
                new_location = [-2, -2.75, 0],
                start_time = one_trait_time
            )

            shift_trait_time = 106.5
            arrow1.morph_figure(1, start_time = shift_trait_time)
            trait1.move_to(new_location = [3, 0.5, 0], start_time = shift_trait_time)
            gene1.move_to(
                new_location = [-4, 0.5, 0],
                new_scale = 0.9,
                start_time = shift_trait_time
            )

            new_dna = []
            extra_dna = []
            object_bin = []
            extra_arrows = []
            for i in range(4):
                if i > 0: #Reserve i = 0 for changes to first line
                    gene = import_object(
                        'dna_two_strand_low_res', 'biochem',
                        location = [-4, 0.5 - 2.2 * i, 0],
                        rotation_euler = [0, 0, 25 * math.pi / 180],
                        scale = 0.9,
                    )
                    gene.add_to_blender(appear_time = shift_trait_time + 1 + 0.1 * i)
                    new_dna.append(gene)

                    scale = 1
                    arrow = gesture.Gesture(
                        gesture_series = [
                            {
                                'type': 'arrow',
                                'points': {
                                    'tail': (-2 / scale, 0.5 - 2.2 * i / scale, 0),
                                    'head': (2 / scale, 0.5 - 2.2 * i / scale, 0)
                                }
                            },
                        ],
                        scale = scale,
                    )
                    trait = tex_bobject.TexBobject(
                        '\\text{Trait}',
                        location = [3, 0.5 - 2.2 * i, 0],
                        scale = 2,
                    )

                    arrow.add_to_blender(appear_time = shift_trait_time + 2.5 + 0.1 * i)
                    trait.add_to_blender(appear_time = shift_trait_time + 2.5 + 0.1 * i)

                    object_bin.append(arrow)
                    object_bin.append(trait)

                addendum_time = 124
                if i == 0:
                    gene1.move_to(
                        displacement = [0.5, 0, 0],
                        start_time = addendum_time
                    )
                else:
                    gene.move_to(
                        displacement = [0.5, 0, 0],
                        start_time = addendum_time
                    )

                gene2 = import_object(
                    'dna_two_strand_low_res', 'biochem',
                    location = [-5, 0.25 - 2.2 * i, 0],
                    rotation_euler = [0, 0, 25 * math.pi / 180],
                    scale = 0.9,
                )
                gene2.add_to_blender(appear_time = 124)
                extra_dna.append(gene2)

                #Two-sided arrows to show gene interactions
                if i > 0:
                    string = '\\curvearrowleft'
                    if i % 2 == 0:
                        string = '\\curvearrowright'


                    tex = tex_bobject.TexBobject(
                        string,
                        location = [-2, 0.5 + 1.1 - 2.2 * i, 0],
                        rotation_euler = [0, 0, -math.pi / 2],
                        scale = 2,
                        centered = True
                    )
                    tex.add_to_blender(appear_time = 133.5)
                    extra_arrows.append(tex)
                    '''q = tex_bobject.TexBobject(
                        '\\text{?}',
                        location = [-4.3, 0.5 + 1-1 - 2.2 * i, 0],
                        scale = 0.5
                    )'''

            extra_arrow_tensor = [
                [[0, 2], [3, 1]],
                [[0, 3], [1, 0]],
                [[2, 1], [1, 3]]
            ]
            timings = [128.5, 131, 136.5]
            for i, row in enumerate(extra_arrow_tensor):
                color = 'color2'
                if i == 2:
                    color = 'color4'
                for pair in row:
                    scale = 1
                    arr = gesture.Gesture(
                        gesture_series = [
                            {
                                'type': 'arrow',
                                'points': {
                                    'tail': (-2 / scale, (0.5 - 2.2 * pair[0]) / scale, 0),
                                    'head': (2 / scale, (0.5 - 2.2 * pair[1]) / scale, 0)
                                }
                            },
                        ],
                        scale = scale,
                        color = color
                    )
                    arr.add_to_blender(appear_time = timings[i])
                    extra_arrows.append(arr)



            for d in new_dna + extra_dna + [gene1]:
                d.tweak_colors_recursive()
                d.spin(start_time = 0, spin_rate = -0.05)

            for d in new_dna + [gene1]:
                d.move_to(
                    displacement = [-0.5, 0, 0],
                    start_time = 160
                )

            for thing in extra_dna + extra_arrows:
                thing.disappear(disappear_time = 160.5)

            for thing in new_dna + extra_arrows + object_bin + [blob, gene1, arrow1, trait1]:
                thing.disappear(disappear_time = 168.5)

        def genes_are_information():
            final_helices = []
            ghosts = []
            info_time = 169
            for i in range(4):
                s1 = import_object(
                    'dna_strand_1_low_res', 'biochem',
                    scale = 2,
                    location = [-9 + 6 * i, -5.5, 0]
                )
                s2 = import_object(
                    'dna_strand_2_low_res', 'biochem',
                    scale = 2,
                    location = [-9 + 6 * i, -5.5, 0]
                )
                final_helices.append([s1, s2])

                if i == 0:
                    s1.add_to_blender(appear_time = info_time)
                else:
                    s1.add_to_blender(appear_time = 0)
                    s1.de_explode(
                        start_time = info_time  + i,
                        duration = 0.5
                    )

                if i == 3:
                    s2.add_to_blender(appear_time = info_time)
                else:
                    s2.add_to_blender(appear_time = 0)
                    s2.de_explode(
                        start_time = 1 + info_time  + i,
                        duration = 0.5
                    )

                #GHOSTS
                s1g = import_object(
                    'dna_strand_1_low_res', 'biochem',
                    scale = 2,
                    location = [-9 + 6 * i, -5.5, 0]
                )
                s2g = import_object(
                    'dna_strand_2_low_res', 'biochem',
                    scale = 2,
                    location = [-9 + 6 * i, -5.5, 0]
                )
                ghosts.append([s1g, s2g])

                if i == 0:
                    s1g.add_to_blender(appear_time = info_time)
                else:
                    s1g.add_to_blender(appear_time = 0)
                    s1g.de_explode(
                        start_time = info_time  + i ,
                        duration = 0.5
                    )

                if i == 3:
                    s2g.add_to_blender(appear_time = info_time)
                else:
                    s2g.add_to_blender(appear_time = 0)
                    s2g.de_explode(
                        start_time = 1 + info_time  + i ,
                        duration = 0.5
                    )

            mover = final_helices[3][1]
            moverg = ghosts[3][1]
            for i in range(4):
                mover.move_to(
                    new_location = [-9 + 6 * i, -5.5, 0],
                    start_time = info_time  + i  - 0.5,
                    end_time = info_time  + i
                )
                moverg.move_to(
                    new_location = [-9 + 6 * i, -5.5, 0],
                    start_time = info_time  + i  - 0.5,
                    end_time = info_time  + i
                )

            def make_clear_recursive(obj):
                apply_material(obj, 'trans_color2', intensity = 3)
                for child in obj.children:
                    make_clear_recursive(child)

            for gpair in ghosts:
                for ghost in gpair:
                    ghost.move_to(
                        new_location = [-8, 0, 0],
                        start_time = 173
                    )
                    ghost.spin(start_time = 0, spin_rate = 0.05)
                    make_clear_recursive(ghost.ref_obj.children[0])

            for pair in final_helices:
                for helix in pair:
                    helix.tweak_colors_recursive()
                    helix.spin(start_time = 0, spin_rate = 0.05)

            tgi = tex_bobject.TexBobject(
                '\\text{The gene itself}',
                location = [-3, 1, 0],
            )
            tgi.add_to_blender(appear_time = 174)
            scale = 1
            tgi_arrow = gesture.Gesture(
                gesture_series = [
                    {
                        'type': 'arrow',
                        'points': {
                            'tail': (-3.25 / scale, 0.75 / scale, 0),
                            'head': (-6 / scale, 0.2 / scale, 0)
                        }
                    },
                ],
                scale = scale,
            )
            tgi_arrow.add_to_blender(appear_time = 174)
            copies = tex_bobject.TexBobject(
                '\\text{Just copies}',
                location = [1.5, -1, 0],
                centered = True
            )
            copies.add_to_blender(appear_time = 175)
            arrow_coords = [
                [[-1, -1.3], [-7, -4.3]],
                [[ 0.5, -1.6],[ -1.5, -3.5]],
                [[ 2.5, -1.6],[ 3, -3.2]],
                [[ 4, -1.2],[ 7.5, -3.5]],
            ]
            for pair in arrow_coords:
                scale = 1
                copy_arrow = gesture.Gesture(
                    gesture_series = [
                        {
                            'type': 'arrow',
                            'points': {
                                'tail': (pair[0][0] / scale, pair[0][1] / scale, 0),
                                'head': (pair[1][0] / scale, pair[1][1] / scale, 0)
                            }
                        },
                    ],
                    scale = scale,
                )
                copy_arrow.add_to_blender(appear_time = 175)


        #text()
        #dna_stuff()
        genes_are_information()

    def strategies(self):
        cam_bobj, cam_swivel = cam_and_swivel(
            cam_location = [0, 0, 32.8], #32.8
            cam_rotation_euler = [0, 0, 0],
            cam_name = "Camera Bobject",
            swivel_location = [0, 0, 0],
            swivel_rotation_euler = [0, 0, 0],
            swivel_name = 'Cam swivel',
            #control_sun = True
        )

        cam_swivel.add_to_blender(appear_time = -1)

        gene = import_object(
            'dna_two_strand', 'biochem',
            scale = 6,
            location = [0, -0.5, 0]
        )
        gene.add_to_blender(appear_time = 194)

        def make_clear_recursive(obj):
            apply_material(obj, 'trans_color2', intensity = 3)
            for child in obj.children:
                make_clear_recursive(child)
        gene.spin(start_time = 0, spin_rate = 0.05)
        make_clear_recursive(gene.ref_obj.children[0])
        ghost_home = [-9, 3, 0]
        ghost_scale = 3.6
        gene.move_to(
            start_time = 199.5,
            new_location = ghost_home,
            new_scale = ghost_scale
        )

        strats = tex_bobject.TexBobject(
            '\\text{Strategies}',
            centered = True
        )
        carriers = tex_bobject.TexBobject(
            '\\begin{array}{@{}c@{}}\\text{Effect on} \\\\ \\text{carrier creatures} \\end{array}',
            centered = True
        )
        oc = tex_bobject.TexBobject(
            '\\begin{array}{@{}c@{}}\\text{Effect on} \\\\ \\text{other creatures} \\end{array}',
            centered = True
        )
        cf = tex_bobject.TexBobject(
            '\\text{Carrier-focused}',
            centered = True
        )
        cfp = tex_bobject.TexBobject(
            '\\boldsymbol{+}',
            centered = True,
            color = 'color7',
            scale = 2
        )
        cfm = tex_bobject.TexBobject(
            '\\boldsymbol{-}',
            centered = True,
            color = 'color6',
            scale = 2
        )
        ww = tex_bobject.TexBobject(
            '\\text{Win-win}',
            centered = True
        )
        wwp1 = tex_bobject.TexBobject(
            '\\boldsymbol{+}',
            centered = True,
            color = 'color7',
            scale = 2
        )
        wwp2 = tex_bobject.TexBobject(
            '\\boldsymbol{+}',
            centered = True,
            color = 'color7',
            scale = 2
        )
        a = tex_bobject.TexBobject(
            '\\text{Altruistic}',
            centered = True
        )
        am = tex_bobject.TexBobject(
            '\\boldsymbol{-}',
            centered = True,
            color = 'color6',
            scale = 2
        )
        ap = tex_bobject.TexBobject(
            '\\boldsymbol{+}',
            centered = True,
            color = 'color7',
            scale = 2
        )

        em = [
            [strats, carriers, oc],
            [cf, cfp, cfm],
            [ww, wwp1, wwp2],
            [a, am, ap],
        ]

        table = table_bobject.TableBobject(
            location = [-3, 6.5, 0],
            width = 14.7,
            element_matrix = em
        )

        table.add_to_blender(
            appear_time = 201,
            subbobject_timing = [
                30, 30, 30,
                240, 360, 495,
                1980, 2040, 2130,
                3900, 4230, 4065,
                0, 0
            ]
        )


        copy1 = import_object(
            'dna_two_strand_low_res', 'biochem',
            location = ghost_home,
            scale = ghost_scale
        )
        copy1.spin(start_time = 0, spin_rate = 0.05)
        copy1.add_to_blender(appear_time = 0)
        copy1.de_explode(
            start_time = 205,
            duration = 1
        )
        copy1.move_to(
            new_location = [-3, -5.6, 0],
            new_scale = 1,
            start_time = 206
        )
        copy1.tweak_colors_recursive()


        #Evil blob
        e_blob = import_object(
            'boerd_blob', 'creatures',
            scale = 2.5,
            location = [-3, -5, 0]
        )
        e_blob.add_to_blender(appear_time = 206.5, animate = False)

        def fade_blob_in(blob, time):
            meta = blob.ref_obj.children[0].children[0]
            apply_material(meta, 'creature_color3')

            mat_copy = meta.material_slots[0].material.copy()
            meta.active_material = mat_copy
            node_tree = mat_copy.node_tree
            out = node_tree.nodes['Material Output']
            princ = node_tree.nodes['Principled BSDF']
            trans = node_tree.nodes.new(type = 'ShaderNodeBsdfTransparent')
            mix = node_tree.nodes.new(type = 'ShaderNodeMixShader')

            node_tree.links.new(mix.outputs[0], out.inputs[0])
            node_tree.links.new(princ.outputs[0], mix.inputs[1])
            node_tree.links.new(trans.outputs[0], mix.inputs[2])

            mix.inputs[0].default_value = 1
            mix.inputs[0].keyframe_insert(data_path = 'default_value', frame = time * FRAME_RATE)
            mix.inputs[0].default_value = 0
            mix.inputs[0].keyframe_insert(data_path = 'default_value', frame = time * FRAME_RATE + OBJECT_APPEARANCE_TIME)

            scat = node_tree.nodes.new(type = 'ShaderNodeVolumeScatter')
            absorb = node_tree.nodes.new(type = 'ShaderNodeVolumeAbsorption')
            emit = node_tree.nodes.new(type = 'ShaderNodeEmission')
            add1 = node_tree.nodes.new(type = 'ShaderNodeAddShader')
            add2 = node_tree.nodes.new(type = 'ShaderNodeAddShader')

            node_tree.links.new(add1.outputs[0], out.inputs[1])
            node_tree.links.new(emit.outputs[0], add1.inputs[0])
            node_tree.links.new(add2.outputs[0], add1.inputs[1])
            node_tree.links.new(scat.outputs[0], add2.inputs[0])
            node_tree.links.new(absorb.outputs[0], add2.inputs[1])

            for node in [scat, absorb, emit]:
                node.inputs[0].default_value = princ.inputs[0].default_value
                node.inputs[1].default_value = BLOB_VOLUME_DENSITY
                node.inputs[1].keyframe_insert(data_path = 'default_value', frame = (time + 1) * FRAME_RATE)
                node.inputs[1].default_value = BLOB_VOLUME_DENSITY
                node.inputs[1].keyframe_insert(data_path = 'default_value', frame = (time + 2) * FRAME_RATE)


            #Eyes
            eyel_1 = blob.ref_obj.children[0].children[-2]
            eye_mat_copy_1 = eyel_1.material_slots[0].material.copy()
            eyel_1.active_material = eye_mat_copy_1
            eyer_1 = blob.ref_obj.children[0].children[-3]
            eyer_1.active_material = eye_mat_copy_1

            node_tree = eye_mat_copy_1.node_tree
            trans = node_tree.nodes.new(type = 'ShaderNodeBsdfTransparent')
            mix = node_tree.nodes.new(type = 'ShaderNodeMixShader')
            out = node_tree.nodes['Material Output']
            diff = node_tree.nodes['Diffuse BSDF']

            node_tree.links.new(mix.outputs[0], out.inputs[0])
            node_tree.links.new(trans.outputs[0], mix.inputs[1])
            node_tree.links.new(diff.outputs[0], mix.inputs[2])

            mix.inputs[0].default_value = 0
            mix.inputs[0].keyframe_insert(data_path = 'default_value', frame = time * FRAME_RATE)
            mix.inputs[0].default_value = 1
            mix.inputs[0].keyframe_insert(data_path = 'default_value', frame = time * FRAME_RATE + OBJECT_APPEARANCE_TIME)


        fade_blob_in(e_blob, 206.5)

        e_blob.evil_pose(
            start_time = 212.5,
            end_time = 216.5
        )

        psvsm = tex_bobject.TexBobject(
            '\\text{Passivism}',
            location = [-9.5, -3.5, 0],
            scale = 1.25,
            centered = True
        )
        psvsm.add_to_blender(appear_time = 239.75)

        e_blob.wince(
            start_time = 241.5,
            end_time = 246
        )

        ra = tex_bobject.TexBobject(
            '\\begin{array}{@{}c@{}}\\text{Reciprocal} \\\\ \\text{altruism} \\end{array}',
            location = [-9.5, -6, 0],
            scale = 1.25,
            centered = True
        )
        ra.add_to_blender(appear_time = 248.25)

        f_blob = import_object(
            'boerd_blob', 'creatures',
            location = [19, -5, 0],
            scale = 2.5,
        )
        meta = f_blob.ref_obj.children[0].children[0]
        apply_material(meta, 'creature_color3')
        blob_enter_time = 249.5
        f_blob.add_to_blender(appear_time = blob_enter_time - 1)

        def blob_enter():
            f_blob.move_to(
                new_angle = [0, -math.pi / 2, 0],
                start_time = blob_enter_time - 0.2# st + 9.8
            )
            f_blob.move_to(
                displacement = [-16, 0, 0],
                start_time = blob_enter_time - 1,
                end_time = blob_enter_time + 1
            )
            '''f_blob.move_to(
                new_angle = [0, 0, 0],
                start_time = blob_enter_time + 1 - 0.3#st + 10.7
            )'''

            e_blob.move_to(
                new_angle = [0, math.pi / 2, 0],
                start_time = blob_enter_time + 0.7
            )

        blob_enter()


        #The labels and ordering here are all fucked up! Enjoy parsing.
        gift1_time = 252
        gift1_end_time = 255.5
        f_blob.hold_object(
            start_time = gift1_time,
            end_time = gift1_end_time
        )
        gift1 = import_object(
            'gift_white', 'misc',
            location = [0, 0, 0],
            rotation_euler = [-math.pi / 2, 0, 0],
            scale = 0.28
        )
        gift1.add_to_blender(appear_time = gift1_time)
        gift1.move_to(
            new_location = [0, 0, 0.8],
            start_time = gift1_time
        )

        gift2_time = 250.5
        gift2_end_time = 261
        gift2 = import_object(
            'gift_white', 'misc',
            location = [0, 0, 0],
            rotation_euler = [-math.pi / 2, 0, 0],
            scale = 0.28
        )
        gift2.add_to_blender(appear_time = gift2_time)
        e_blob.hold_object(
            start_time = gift2_time,
            end_time = gift2_end_time
        )
        gift2.move_to(
            new_location = [0, 0, 0.8],
            start_time = gift2_time
        )
        gift1.ref_obj.parent = f_blob.ref_obj
        gift2.ref_obj.parent = e_blob.ref_obj

        #Gift away, bomb out
        gift1.move_to(
            start_time = gift1_end_time - 0.5,
            new_location = [0, 0, 0],
            new_scale = 0.22
        )
        gift1.disappear(disappear_time = gift1_end_time + 0.5)
        bomb_time = 257
        bomb_end_time = 261
        f_blob.hold_object(
            start_time = bomb_time,
            end_time = bomb_end_time
        )
        bomb = import_object(
            'bomb', 'misc',
            location = [0, 0, 0],
            rotation_euler = [-math.pi / 2, 0, 0],
            scale = 0.3
        )
        bomb.ref_obj.parent = f_blob.ref_obj
        bomb.add_to_blender(appear_time = bomb_time)
        bomb.move_to(
            new_location = [0, 0, 0.8],
            start_time = bomb_time
        )

        #Clean up
        for g in [gift2, bomb]:# gift1]:
            g.move_to(
                start_time = bomb_end_time - 0.5,
                new_location = [0, 0, 0],#2.37],
                new_scale = 0.29
            )
            g.disappear(disappear_time = bomb_end_time + 0.5)
        for blob in [e_blob, f_blob]:
            blob.move_to(
                start_time = bomb_end_time + 0.5,
                new_angle = [0, 0, 0]
            )

        psvsm.disappear(disappear_time = bomb_end_time + 0.5)
        ra.disappear(disappear_time = bomb_end_time + 0.5)

        #Moar gifts
        moar_start = 268
        moar_end = 282
        e_blob.move_to(
            new_angle = [0, math.pi / 2, 0],
            start_time = moar_start - 0.3
        )
        for i in range(moar_end - moar_start):
            e_blob.hold_object(
                start_time = moar_start + i,
                end_time = moar_start + 1 + i
            )
            gift = import_object(
                'gift_white', 'misc',
                location = [0, 0, 0],
                rotation_euler = [-math.pi / 2, 0, 0],
                scale = 0.28
            )
            gift.ref_obj.parent = e_blob.ref_obj
            gift.add_to_blender(appear_time = moar_start + i)
            gift.move_to(
                new_location = [0, 0, 0.8],
                start_time = moar_start + i
            )
            gift.move_to(
                new_location = [0.1, 0, 2.37],
                start_time = moar_start + i + 0.5
            )
            gift.disappear(disappear_time = moar_start + i + 1.5)

        e_blob.move_to(
            new_angle = [0, 0, 0],
            start_time = moar_end + 0.5
        )

        #More blobs
        other_blobs_time = 284
        other_blobs = []
        for i in range(2):
            blob = import_object(
                'boerd_blob', 'creatures',
                location = [9 - 18 * i, -5, 0],
                scale = 2.5,
            )
            meta = blob.ref_obj.children[0].children[0]
            apply_material(meta, 'creature_color3')
            blob.add_to_blender(appear_time = other_blobs_time)
            other_blobs.append(blob)

        blobs = [e_blob, f_blob] + other_blobs
        mix_matrix = [
            [3, 2, 0],
            [0, 3, 1],
            [2, 1, 2],
            [1, 0, 3],
        ]
        mix_start = 287
        for i, row in enumerate(mix_matrix):
            for j, dest in enumerate(row):
                blobs[i].move_to(
                    new_location = [-9 + dest * 6, -5, 0],
                    start_time = mix_start + j
                )
                if blobs[i] == e_blob:
                    copy1.move_to(
                        new_location = [-9 + dest * 6, -5.6, 0],
                        start_time = mix_start + j
                    )

        inc_fit_time = 294.25
        for blob in blobs:
            #Such elegant. Wow.
            if blob.ref_obj.location[0] == 9:
                blob.move_to(displacement = [1, 0, 0], start_time = inc_fit_time)
            elif blob.ref_obj.location[0] == 3:
                blob.move_to(displacement = [2, 0, 0], start_time = inc_fit_time)
            elif blob.ref_obj.location[0] == -3:
                blob.move_to(displacement = [3, 0, 0], start_time = inc_fit_time)
            elif blob.ref_obj.location[0] == -9:
                blob.move_to(displacement = [4, 0, 0], start_time = inc_fit_time)
                #don't judge me
                copy1.move_to(displacement = [4, 0, 0], start_time = inc_fit_time)

        inc_fit = tex_bobject.TexBobject(
            '\\begin{array}{@{}c@{}}\\text{Inclusive} \\\\ \\text{fitness} \\end{array}',
            location = [-10.5, -5, 0],
            scale = 1.25,
            centered = True
        )
        inc_fit.add_to_blender(appear_time = inc_fit_time)

        def make_red_recursive(obj):
            apply_material(obj, 'color6')
            for child in obj.children:
                make_red_recursive(child)

        dna_reveal_time = 300.5
        for blob in blobs:#[f_blob] + other_blobs:
            if blob != e_blob:
                d = import_object(
                    'dna_two_strand_low_res', 'biochem',
                    location = [
                        blob.ref_obj.location[0],
                        blob.ref_obj.location[1] - 0.6,
                        blob.ref_obj.location[2],
                    ],
                    scale = 1
                )
                d.spin(start_time = 0, spin_rate = 0.05)
                d.add_to_blender(appear_time = dna_reveal_time - 1)
                d.tweak_colors_recursive()

                if blob == f_blob or blob == other_blobs[0]:
                    make_red_recursive(d.ref_obj.children[0])

                #Make blob clear. I should really make this into a helper function
                #Or part of a blob class
                for child in blob.ref_obj.children:
                    if 'boerd_blob' in child.name:
                        meta = child.children[0]

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

                for node in [scat, absorb, emit]:
                    node.inputs[0].default_value = princ.inputs[0].default_value
                    node.inputs[1].default_value = BLOB_VOLUME_DENSITY

            else:
                for child in blob.ref_obj.children:
                    if 'boerd_blob' in child.name:
                        meta = child.children[0]

                mix = meta.active_material.node_tree.nodes['Mix Shader']
                #mix = blob.ref_obj.children[0].children[0].material_slots[0].material.node_tree.nodes['Mix Shader']

            mix.inputs[0].default_value = 0
            mix.inputs[0].keyframe_insert(data_path = 'default_value', frame = dna_reveal_time * FRAME_RATE)
            mix.inputs[0].default_value = 1
            mix.inputs[0].keyframe_insert(data_path = 'default_value', frame = (dna_reveal_time + 0.5) * FRAME_RATE)

        #Re-opaque-ify
        #opaque_time = 303
        '''disappear_time = 303
        for blob in blobs + [inc_fit]:
            blob.disappear(disappear_time = disappear_time + 0.5)'''
        '''for child in blob.ref_obj.children:
            if 'boerd_blob' in child.name:
                meta = child.children[0]

        mix = meta.active_material.node_tree.nodes['Mix Shader']

        mix.inputs[0].default_value = 1
        mix.inputs[0].keyframe_insert(data_path = 'default_value', frame = opaque_time * FRAME_RATE)
        mix.inputs[0].default_value = 0
        mix.inputs[0].keyframe_insert(data_path = 'default_value', frame = (opaque_time + 0.5) * FRAME_RATE)'''


        cam_swivel.move_to(
            new_location = [4.4, 2.9, 0],
            start_time = 306,
            end_time = 307
        )
        cam_bobj.move_to(
            new_location = [0, 0, 18],
            start_time = 306,
            end_time = 307
        )

        for p in [cfp, wwp1]:
            p.pulse(
                start_time = 310,
                duration_time = 4,
                factor = 1.5
            )
        for p in [wwp2, ap]:
            p.pulse(
                start_time = 311.25,
                duration_time = 2.75,
                factor = 1.5
            )
        for m in [cfm, am]:
            m.pulse(
                start_time = 313.5,
                duration_time = 3,
                factor = 1.5
            )

        cam_swivel.move_to(
            new_location = [-9, 2.9, 0],
            start_time = 317,
            end_time = 318
        )
        table.move_to(
            displacement = [3, 0, 0],
            start_time = 317,
            end_time = 318
        )

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

    def banner_angled(self):
        cam_bobj, cam_swivel = cam_and_swivel(
            cam_location = [0, 0, 32.8],
            cam_rotation_euler = [0, 0, 0],
            cam_name = "Camera Bobject",
            swivel_location = [0, 0, 0],
            swivel_rotation_euler = [70 * math.pi / 180, 0, 0],
            swivel_name = 'Cam swivel',
            control_sun = True
        )
        cam_swivel.add_to_blender(appear_time = -1)

        logo = svg_bobject.SVGBobject(
            "Layer",
            #file_name = "PrimerLogoWhite",
            location = [0, 0, 0],
            rotation_euler = [math.pi / 2, 0, 0],
            scale = 4,
            centered = True
        )
        for bobj in logo.rendered_curve_bobjects:
            apply_material(bobj.ref_obj.children[0], 'color2')
        stroke = logo.rendered_curve_bobjects[0]
        apply_material(stroke.ref_obj.children[0], 'color3')
        logo.morph_chains[0][0].ref_obj.location[2] = -1
        logo.add_to_blender(
            appear_time = -1,
            #subbobject_timing = [90, 30, 40, 50, 60, 70, 80],
            #subbobject_timing = [42, 30, 33, 36, 39, 42, 45],
            animate = False
        )

        b_blob = import_object(
            'boerd_blob', 'creatures',
            scale = 2,
            location = [2, -10, 0],
            rotation_euler = [math.pi / 2, 0, 0],
            wiggle = True
        )
        b_blob.add_to_blender(appear_time = 0)
        apply_material(b_blob.ref_obj.children[0].children[0], 'creature_color3')


        r_blob = import_object(
            'boerd_blob', 'creatures',
            scale = 2,
            location = [-7, -7, 0],
            rotation_euler = [math.pi / 2, 0, 100 * math.pi / 180],
            wiggle = True
        )
        r_blob.add_to_blender(appear_time = 0)
        apply_material(r_blob.ref_obj.children[0].children[0], 'creature_color6')

        g_blob = import_object(
            'boerd_blob', 'creatures',
            scale = 2,
            location = [-5, -5, 0],
            rotation_euler = [math.pi / 2, 0, -10 * math.pi / 180],
            wiggle = True
        )
        g_blob.add_to_blender(appear_time = 0)
        apply_material(g_blob.ref_obj.children[0].children[0], 'creature_color7')

        o_blob = import_object(
            'boerd_blob', 'creatures',
            scale = 2,
            location = [10, -6, 0],
            rotation_euler = [math.pi / 2, 0, math.pi / 2],
            wiggle = True
        )
        o_blob.add_to_blender(appear_time = 0)
        apply_material(o_blob.ref_obj.children[0].children[0], 'creature_color4')
