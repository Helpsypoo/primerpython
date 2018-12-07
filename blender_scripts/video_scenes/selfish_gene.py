import collections
import math
from random import random, uniform, randrange
import bpy

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

class SelfishGene(Scene):
    def __init__(self):
        self.subscenes = collections.OrderedDict([
            ('card', {'duration': 1000})
        ])
        super().__init__()

    def play(self):
        super().play()

        #self.intro()
        #self.replicating_creatures()
        #self.dna()
        #self.sexual_reproduction()
        #self.conjugation()
        #self.gene()
        self.strategies()
        #self.end_card()
        #self.thumbnail()

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
            "\\text{Gene strategies}",
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
            "\\text{Simulate altruism}",
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
            blob1.add_to_blender(appear_time = 0)

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
                    next_blob.blob_wave(start_time = i + 1, duration = 10)

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
                    #    node.inputs[1].default_value = 0.08

                    mix.inputs[0].default_value = 0
                    mix.inputs[0].keyframe_insert(data_path = 'default_value', frame = (num_cres + 3) * FRAME_RATE)
                    mix.inputs[0].default_value = 1
                    mix.inputs[0].keyframe_insert(data_path = 'default_value', frame = (num_cres + 5) * FRAME_RATE)


                next_blob.add_to_blender(appear_time = i + 1)
                next_blob.move_to(
                    new_location = [
                        next_blob.ref_obj.location[0] + 10,
                        next_blob.ref_obj.location[1],
                        next_blob.ref_obj.location[2]
                    ],
                    start_time = i + 1
                )

                if i < num_cres - 2:
                    next_blob.disappear(disappear_time = num_cres + 5)

                last_blob = next_blob
                i += 1

            cam_swivel.add_to_blender(appear_time = -1)
            cam_swivel.move_to(
                new_location = [10 * (num_cres - 2), 0, 0],
                start_time = 1,
                end_time = num_cres
            )

            cam_swivel.move_to(
                new_location = [10 * (num_cres - 2) + 4.85, 0, 0],
                start_time = num_cres + 3,
                end_time = num_cres + 5
            )
            cam_bobj.move_to(
                new_location = [0, 0, 4],
                start_time = num_cres + 3,
                end_time = num_cres + 5
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
            start_time = 1,
            duration = 1,
        )

        dna2_1.de_explode(
            start_time = 2.5,
            duration = 1,
        )

        cam_bobj.move_to(
            new_location = [0, -0.8, 10.7],
            start_time = 4,
            end_time = 5
        )
        dtex = tex_bobject.TexBobject(
            '\\text{Deoxyribonucleic Acid}',
            '\\text{DNA}',
            location = [0, 1.2, 0],
            centered = True
        )
        dtex.add_to_blender(appear_time = 5)
        dtex.morph_figure(1, start_time = 7)
        dtex.disappear(disappear_time = 9)

        #def replicate():
        blob1 = import_object(
            'boerd_blob', 'creatures',
            location = [0, 0, 0],
            scale = 6,
            wiggle = True
        )
        meta = blob1.ref_obj.children[0].children[0]
        apply_material(meta, 'creature_color7')
        blob1.add_to_blender(appear_time = 0)

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
            node.inputs[1].keyframe_insert(data_path = 'default_value', frame = 9 * FRAME_RATE)
            node.inputs[1].default_value = 0.08
            node.inputs[1].keyframe_insert(data_path = 'default_value', frame = 10 * FRAME_RATE)

        cam_bobj.move_to(
            new_location = [0, 0, 32.8],
            start_time = 9,
            end_time = 10
        )

        blob2 = import_object(
            'boerd_blob', 'creatures',
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
            node.inputs[1].keyframe_insert(data_path = 'default_value', frame = 12 * FRAME_RATE)
            node.inputs[1].default_value = 0.08
            node.inputs[1].keyframe_insert(data_path = 'default_value', frame = 12.5 * FRAME_RATE)

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
        mix.inputs[0].keyframe_insert(data_path = 'default_value', frame = 9 * FRAME_RATE)
        mix.inputs[0].default_value = 1
        mix.inputs[0].keyframe_insert(data_path = 'default_value', frame = 10 * FRAME_RATE)

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
        mix.inputs[0].keyframe_insert(data_path = 'default_value', frame = 12 * FRAME_RATE)
        mix.inputs[0].default_value = 1
        mix.inputs[0].keyframe_insert(data_path = 'default_value', frame = 12.5 * FRAME_RATE)

        dna2_1.move_to(new_location = [1.5, -1.5, 0], start_time = 10)
        dna1_1.move_to(new_location = [-1.5, -1.5, 0], start_time = 10)

        dna1_2 = import_object(
            'dna_strand_1', 'biochem',
            scale = 1.5,
            location = [1.5, -1.5, 0],
        )
        dna1_2.add_to_blender(appear_time = 0)
        dna2_2 = import_object(
            'dna_strand_2', 'biochem',
            scale = 1.5,
            location = [-1.5, -1.5, 0],
        )
        dna2_2.add_to_blender(appear_time = 0)
        dna1_2.de_explode(
            start_time = 11,
            duration = 1,
        )
        dna2_2.de_explode(
            start_time = 11,
            duration = 1,
        )

        blob2.move_to(new_location = [6, 0, 0], start_time = 12)
        blob1.move_to(new_location = [-6, 0, 0], start_time = 12)
        dna1_1.move_to(new_location = [-6, -1.5, 0], start_time = 12)
        dna2_1.move_to(new_location = [6, -1.5, 0], start_time = 12)
        dna1_2.move_to(new_location = [6, -1.5, 0], start_time = 12)
        dna2_2.move_to(new_location = [-6, -1.5, 0], start_time = 12)

        for d in [dna1_1, dna2_1, dna1_2, dna2_2]:
            d.spin(start_time = 0, spin_rate = 0.1)

        to_disappear = [dna1_1, dna2_1, dna1_2, dna2_2, blob1, blob2]
        for thing in to_disappear:
            thing.disappear(disappear_time = 15)

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
            node.inputs[1].default_value = 0.08

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
            d.spin(start_time = 0, spin_rate = sign * 0.1)
            sign *= -1

        def blob1_move():
            blob1.move_to(
                new_angle = [0, math.pi / 2, 0],
                start_time = 0 - 0.2# st + 9.8
            )
            blob1.move_to(
                new_angle = [0, 0, 0],
                start_time = 1 - 0.3#st + 10.7
            )
            blob1.eat_animation(
                start_frame = 0.5 * FRAME_RATE,
                end_frame = 3.5 * FRAME_RATE
            )
            blob1.blob_scoop(
                start_time = 0.5,
                duration = 3,
                top_pause_time = 1
            )

            for thing in [blob1] + dna_set1:
                thing.move_to(
                    displacement = [13, 0, 0],
                    start_time = 0,
                    end_time = 1
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
            node.inputs[1].default_value = 0.08

        dna21 = import_object(
            'dna_two_strand_low_res', 'biochem',
            scale = dna_scale,
            location = add_lists_by_element(blob2.ref_obj.location, [-0.1, 0, 0])
        )
        '''#Will turn out to be a copy that moves later.
        dna31 = import_object(
            'dna_two_strand_low_res', 'biochem',
            scale = dna_scale,
            location = add_lists_by_element(blob2.ref_obj.location, [-0.1, 0, 0])
        )'''
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
            d.spin(start_time = 0, spin_rate = sign * 0.1)
            sign *= -1

        def blob2_move():
            blob2.move_to(
                new_angle = [0, -math.pi / 2, 0],
                start_time = 0 - 0.2# st + 9.8
            )
            blob2.move_to(
                new_angle = [0, 0, 0],
                start_time = 1 - 0.3#st + 10.7
            )
            blob2.eat_animation(
                start_frame = 0.5 * FRAME_RATE,
                end_frame = 3.5 * FRAME_RATE
            )
            blob2.blob_scoop(
                start_time = 0.5,
                duration = 3,
                top_pause_time = 1
            )

            for thing in [blob2] + dna_set2:
                thing.move_to(
                    displacement = [-13, 0, 0],
                    start_time = 0,
                    end_time = 1
                )

        blob2_move()

        heart = import_object(
            'heart',
            location = [0, 4, 0],
            scale = 3
        )
        apply_material(heart.ref_obj.children[0], 'creature_color6')
        heart.add_to_blender(appear_time = 1)
        heart.move_to(
            new_angle = [0, 10 * math.pi, 0],
            start_time = 0,
            end_time = 2
        )

        mix1.inputs[0].default_value = 0
        mix1.inputs[0].keyframe_insert(data_path = 'default_value', frame = 5 * FRAME_RATE)
        mix1.inputs[0].default_value = 1
        mix1.inputs[0].keyframe_insert(data_path = 'default_value', frame = 6 * FRAME_RATE)
        #mix1.inputs[0].keyframe_insert(data_path = 'default_value', frame = 300)
        #mix1.inputs[0].default_value = 0
        #mix1.inputs[0].keyframe_insert(data_path = 'default_value', frame = 360)


        mix2.inputs[0].default_value = 0
        mix2.inputs[0].keyframe_insert(data_path = 'default_value', frame = 5 * FRAME_RATE)
        mix2.inputs[0].default_value = 1
        mix2.inputs[0].keyframe_insert(data_path = 'default_value', frame = 6 * FRAME_RATE)
        #mix2.inputs[0].keyframe_insert(data_path = 'default_value', frame = 300)
        #mix2.inputs[0].default_value = 0
        #mix2.inputs[0].keyframe_insert(data_path = 'default_value', frame = 360)

        for thing in [blob1, blob2] + dna_set1 + dna_set2:
            thing.move_to(
                displacement = [0, 3.5, 0],
                start_time = 5
            )
        heart.move_to(
            displacement = [0, 15, 0],
            start_time = 5,
            end_time = 7
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

            blob.add_to_blender(appear_time = 8 + i)
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
                    start_time = 8 + i,
                    duration = 0.5
                )
                dna.move_to(
                    start_time = 8 + i,
                    new_location = add_lists_by_element(
                        blob.ref_obj.location,
                        displacements[j]
                    )
                )

                new_dna.append(dna)


        sign = -1
        for d in new_dna:
            d.spin(start_time = 0, spin_rate = sign * 0.1)
            sign *= -1


        mix1.inputs[0].keyframe_insert(data_path = 'default_value', frame = 12 * FRAME_RATE)
        mix1.inputs[0].default_value = 1
        mix1.inputs[0].keyframe_insert(data_path = 'default_value', frame = 13 * FRAME_RATE)


        mix2.inputs[0].keyframe_insert(data_path = 'default_value', frame = 12 * FRAME_RATE)
        mix2.inputs[0].default_value = 1
        mix2.inputs[0].keyframe_insert(data_path = 'default_value', frame = 13 * FRAME_RATE)


        top = source_blobs + dna_set1 + dna_set2
        for thing in top:
            thing.move_to(
                displacement = [0, 16, 0],
                start_time = 14,
                end_time = 15
            )

        bot = dest_blobs + new_dna
        for thing in bot:
            thing.move_to(
                displacement = [0, -16, 0],
                start_time = 14,
                end_time = 15
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
            start_time = -1,
            end_time = 3
        )

        bac1.move_to(
            new_location = [10, -12, 0],
            new_angle = [0, 2 * math.pi, -260 * math.pi / 180],
            start_time = 6,
            end_time = 10
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
            start_time = -1,
            end_time = 3
        )

        bac2.move_to(
            new_location = [5, 12, 0],
            new_angle = [0, -1 * math.pi, 270 * math.pi / 180],
            start_time = 6,
            end_time = 10
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
            new_scale = [0.05, 0.05, 0.6],
            start_time = 3,
            end_time = 4
        )
        cyl.move_to(
            new_scale = [0.05, 0.05, 0],
            start_time = 5.7,
            end_time = 6.7
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
            start_time = 4,
            end_time = 5,
            new_location = [1, -0.2, 0]
        )
        dna.disappear(disappear_time = 5)
        dna.spin(
            start_time = 0,
            spin_rate = 0.5
        )

        cam_bobj.move_to(
            new_location = [1, -0.5, 9],
            start_time = 3,
            end_time = 4
        )
        cam_bobj.move_to(
            new_location = [0, 0, 32.8],
            start_time = 5.5,
            end_time = 6.5
        )

        dna.tweak_colors_recursive()

    def gene(self):
        dna_time = 2.5
        creature_time = 4
        one_trait_time = 5
        complex_model_time = 15
        pattern_time = 25

        info_time = 40

        def text():
            gene = tex_bobject.TexBobject(
                '\\text{Gene?}',
                '\\text{Gene:}',
                centered = True,
                scale = 5
            )
            gene.add_to_blender(appear_time = 0)

            #move to top and morph to definition
            gene.morph_figure(1, start_time = 2)
            gene.move_to(
                new_location = [-11, 6.5, 0],
                new_scale = 2,
                start_time = 2
            )

            gene_def1 = tex_bobject.TexBobject(
                '\\text{A section of DNA}',
                '\\text{A section of DNA that lives inside a creature}',
                '\\text{A } pattern \\text{ of DNA whose } copies \\text{ exist inside creatures}',
                scale = 1
            )
            gene_def2 = tex_bobject.TexBobject(
                '\\text{and determines one trait}',
                '\\text{and determines one trait?}',
                '\\text{and determine one trait}',
                scale = 1
            )
            gene_def = tex_complex.TexComplex(
                gene_def1,
                multiline = True,
                scale = 1,
                location = [-10.5, 4.75, 0]
            )
            gene_def.add_to_blender(appear_time = dna_time, animate = False)

            gene_def1.morph_figure(1, start_time = creature_time)

            gene_def.add_tex_bobject(gene_def2)
            gene_def2.add_to_blender(appear_time = one_trait_time)
            gene_def.arrange_tex_bobjects(start_time = one_trait_time)

            gene_def2.morph_figure(1, start_time = complex_model_time)

            gene_def1.morph_figure(2, start_time = pattern_time)
            gene_def2.morph_figure(2, start_time = pattern_time)
            for i in range(1, 8):
                char = gene_def1.lookup_table[2][i]
                char.color_shift(
                    start_time = pattern_time,
                    color = COLORS_SCALED[5],
                    duration_time = None
                )

            for i in range(18, 24):
                char = gene_def1.lookup_table[2][i]
                char.color_shift(
                    start_time = pattern_time,
                    color = COLORS_SCALED[5],
                    duration_time = None
                )


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
                    location = [uniform(-1, 1) * 10, 20 + random() * 20, 0],
                )
                t_bobj.add_to_blender(appear_time = 0)
                t_bobj.spin(start_frame = 0, axis = 2, spin_rate = uniform(-1, 1) * 2)
                t_bobj.move_to(
                    displacement = [0, -60, 0],
                    start_time = complex_model_time + 5,
                    end_time = complex_model_time + 8
                )

        def dna_stuff():
            gene1 = import_object(
                'dna_two_strand', 'biochem',
                location = [0, -2.75, 0],
                scale = 4
            )
            gene1.add_to_blender(appear_time = 0)

            blob = import_object(
                'boerd_blob', 'creatures',
                location = [-9, -2.75, 0],
                scale = 4.5,
                wiggle = True
            )
            apply_material(blob.ref_obj.children[0].children[0], 'creature_color3')
            blob.add_to_blender(appear_time = creature_time)

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

            arrow1.add_to_blender(appear_time = one_trait_time)
            trait1.add_to_blender(appear_time = one_trait_time)
            gene1.move_to(
                new_location = [-2, -2.75, 0],
                start_time = one_trait_time
            )

            arrow1.morph_figure(1, start_time = one_trait_time + 1)
            trait1.move_to(new_location = [3, 0.5, 0], start_time = one_trait_time + 1)
            gene1.move_to(
                new_location = [-4, 0.5, 0],
                new_scale = 0.9,
                start_time = one_trait_time + 1
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
                        rotation_euler = [0, 0, randrange(-1, 2, 1) * 25 * math.pi / 180],
                        scale = 0.9,
                    )
                    gene.add_to_blender(appear_time = one_trait_time + 2)
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

                    arrow.add_to_blender(appear_time = one_trait_time + 2)
                    trait.add_to_blender(appear_time = one_trait_time + 2)

                    object_bin.append(arrow)
                    object_bin.append(trait)

                if i == 0:
                    gene1.move_to(
                        displacement = [0.5, 0, 0],
                        start_time = one_trait_time + 3
                    )
                else:
                    gene.move_to(
                        displacement = [0.5, 0, 0],
                        start_time = one_trait_time + 3
                    )

                gene2 = import_object(
                    'dna_two_strand_low_res', 'biochem',
                    location = [-5, 0.5 - 2.2 * i, 0],
                    scale = 0.9,
                )
                gene2.add_to_blender(appear_time = one_trait_time + 3)
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
                    tex.add_to_blender(appear_time = one_trait_time + 4)
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
            timings = [6, 7, 8]
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
                    arr.add_to_blender(appear_time = one_trait_time + timings[i])
                    extra_arrows.append(arr)



            for d in new_dna + extra_dna + [gene1]:
                d.tweak_colors_recursive()
                d.spin(start_time = 0, spin_rate = -0.1)

            for d in new_dna + [gene1]:
                d.move_to(
                    displacement = [-0.5, 0, 0],
                    start_time = one_trait_time + 9.5
                )

            for thing in extra_dna + extra_arrows:
                thing.disappear(disappear_time = one_trait_time + 10)

        def genes_are_information():
            final_helices = []
            ghosts = []
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
                        start_time = info_time + i,
                        duration = 0.5
                    )

                if i == 3:
                    s2.add_to_blender(appear_time = info_time)
                else:
                    s2.add_to_blender(appear_time = 0)
                    s2.de_explode(
                        start_time = 1 + info_time + i,
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
                        start_time = info_time + i,
                        duration = 0.5
                    )

                if i == 3:
                    s2g.add_to_blender(appear_time = info_time)
                else:
                    s2g.add_to_blender(appear_time = 0)
                    s2g.de_explode(
                        start_time = 1 + info_time + i,
                        duration = 0.5
                    )

            mover = final_helices[3][1]
            moverg = ghosts[3][1]
            for i in range(4):
                mover.move_to(
                    new_location = [-9 + 6 * i, -5.5, 0],
                    start_time = info_time + i - 0.5,
                    end_time = info_time + i
                )
                moverg.move_to(
                    new_location = [-9 + 6 * i, -5.5, 0],
                    start_time = info_time + i - 0.5,
                    end_time = info_time + i
                )

            def make_clear_recursive(obj):
                apply_material(obj, 'trans_color2', intensity = 3)
                for child in obj.children:
                    make_clear_recursive(child)

            for gpair in ghosts:
                for ghost in gpair:
                    ghost.move_to(
                        new_location = [-8, 0, 0],
                        start_time = info_time + 5
                    )
                    ghost.spin(start_time = 0, spin_rate = 0.1)
                    make_clear_recursive(ghost.ref_obj.children[0])

            for pair in final_helices:
                for helix in pair:
                    helix.tweak_colors_recursive()
                    helix.spin(start_time = 0, spin_rate = 0.1)

            tgi = tex_bobject.TexBobject(
                '\\text{The gene itself}',
                location = [-3, 1, 0],
            )
            tgi.add_to_blender(appear_time = info_time + 10)
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
            tgi_arrow.add_to_blender(appear_time = info_time + 10.5)
            copies = tex_bobject.TexBobject(
                '\\text{Just copies}',
                location = [1.5, -1, 0],
                centered = True
            )
            copies.add_to_blender(appear_time = info_time + 11)
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
                copy_arrow.add_to_blender(appear_time = info_time + 11.5)


        text()
        dna_stuff()
        genes_are_information()

    def strategies(self):


        strats = tex_bobject.TexBobject(
            '\\text{Strategies}'
        )

        table = bobject.Bobject()


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
        sg = svg_bobject.SVGBobject(
            "the_selfish_gene_century_italic",
            #location = (-5, 3.75, 0), #Centered position
            #scale = 0.26, #Centered scale
            location = [0, 0, 0],
            scale = 1,
            color = 'color2',
            centered = True
        )
        sg.add_to_blender(appear_time = 0)
