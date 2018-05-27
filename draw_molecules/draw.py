#!/usr/bin/env python
"""
Loads a json molecule and draws atoms in Blender.

Blender scripts are weird. Either run this inside of Blender or in a shell with
    blender foo.blend -P molecule_to_blender.py

The script expects an input file named "molecule.json" and should be in the
same directory as "atoms.json"

Written by Patrick Fuller, patrickfuller@gmail.com, 28 Nov 12
"""
import bpy
from math import acos
from mathutils import Vector
import json
import os
import sys

# Atomic radii from wikipedia, scaled to Blender radii (C = 0.4 units)
# http://en.wikipedia.org/wiki/Atomic_radii_of_the_elements_(data_page)
# Atomic colors from cpk
# http://jmol.sourceforge.net/jscolors/
PATH = os.path.dirname(os.path.realpath(__file__))
with open(os.path.join(PATH, 'atoms.json')) as in_file:
    atom_data = json.load(in_file)


def draw_molecule(molecule, center=(0, 0, 0), show_bonds=True, join=False):
    """Draws a JSON-formatted molecule in Blender.

    This method uses a couple of tricks from [1] to improve rendering speed.
    In particular, it minimizes the amount of unique meshes and materials,
    and doesn't draw until all objects are initialized.

    [1] https://blenderartists.org/forum/showthread.php
        ?273149-Generating-a-large-number-of-mesh-primitives

    Args:
        molecule: The molecule to be drawn, as a python object following the
            JSON convention set in this project.
        center: (Optional, default (0, 0, 0)) Cartesian center of molecule. Use
            to draw multiple molecules in different locations.
        show_bonds: (Optional, default True) Draws a ball-and-stick model if
            True, and a space-filling model if False.
        join: (Optional, default True) Joins the molecule into a single object.
            Set to False if you want to individually manipulate atoms/bonds.
    Returns:
        If run in a blender context, will return a visual object of the
        molecule.
    """
    shapes = []

    # If using space-filling model, scale up atom size and remove bonds

    # Add atom primitive
    bpy.ops.object.select_all(action='DESELECT')
    bpy.ops.mesh.primitive_uv_sphere_add()
    sphere = bpy.context.object

    # Initialize bond material if it's going to be used.
    if show_bonds:
        bpy.data.materials.new(name='bond')
        bpy.data.materials['bond'].diffuse_color = atom_data['bond']['color']
        bpy.data.materials['bond'].specular_intensity = 0.2
        bpy.ops.mesh.primitive_cylinder_add()
        cylinder = bpy.context.object
        cylinder.active_material = bpy.data.materials['bond']

    for atom in molecule['atoms']:
        if atom['element'] not in atom_data:
            atom['element'] = 'undefined'

        if atom['element'] not in bpy.data.materials:
            key = atom['element']
            bpy.data.materials.new(name=key)
            bpy.data.materials[key].diffuse_color = atom_data[key]['color']
            bpy.data.materials[key].specular_intensity = 0.2

        atom_sphere = sphere.copy()
        atom_sphere.data = sphere.data.copy()
        atom_sphere.location = [l + c for l, c in
                                zip(atom['location'], center)]
        scale = 1 if show_bonds else 2.5
        atom_sphere.dimensions = [atom_data[atom['element']]['radius'] *
                                  scale * 2] * 3
        atom_sphere.active_material = bpy.data.materials[atom['element']]
        bpy.context.scene.objects.link(atom_sphere)
        shapes.append(atom_sphere)

    for bond in (molecule['bonds'] if show_bonds else []):
        start = molecule['atoms'][bond['atoms'][0]]['location']
        end = molecule['atoms'][bond['atoms'][1]]['location']
        diff = [c2 - c1 for c2, c1 in zip(start, end)]
        cent = [(c2 + c1) / 2 for c2, c1 in zip(start, end)]
        mag = sum([(c2 - c1) ** 2 for c1, c2 in zip(start, end)]) ** 0.5

        v_axis = Vector(diff).normalized()
        v_obj = Vector((0, 0, 1))
        v_rot = v_obj.cross(v_axis)

        # This check prevents gimbal lock (ie. weird behavior when v_axis is
        # close to (0, 0, 1))
        if v_rot.length > 0.01:
            v_rot = v_rot.normalized()
            axis_angle = [acos(v_obj.dot(v_axis))] + list(v_rot)
        else:
            v_rot = Vector((1, 0, 0))
            axis_angle = [0] * 4

        if bond['order'] not in range(1, 4):
            sys.stderr.write("Improper number of bonds! Defaulting to 1.\n")
            bond['order'] = 1

        if bond['order'] == 1:
            trans = [[0] * 3]
        elif bond['order'] == 2:
            trans = [[1.4 * atom_data['bond']['radius'] * x for x in v_rot],
                     [-1.4 * atom_data['bond']['radius'] * x for x in v_rot]]
        elif bond['order'] == 3:
            trans = [[0] * 3,
                     [2.2 * atom_data['bond']['radius'] * x for x in v_rot],
                     [-2.2 * atom_data['bond']['radius'] * x for x in v_rot]]

        for i in range(bond['order']):
            bond_cylinder = cylinder.copy()
            bond_cylinder.data = cylinder.data.copy()
            bond_cylinder.dimensions = [atom_data['bond']['radius'] * scale *
                                        2] * 2 + [mag]
            bond_cylinder.location = [c + scale * v for c,
                                      v in zip(cent, trans[i])]
            bond_cylinder.rotation_mode = 'AXIS_ANGLE'
            bond_cylinder.rotation_axis_angle = axis_angle
            bpy.context.scene.objects.link(bond_cylinder)
            shapes.append(bond_cylinder)

    # Remove primitive meshes
    bpy.ops.object.select_all(action='DESELECT')
    sphere.select = True
    if show_bonds:
        cylinder.select = True
    # If the starting cube is there, remove it
    if 'Cube' in bpy.data.objects.keys():
        bpy.data.objects.get('Cube').select = True
    bpy.ops.object.delete()

    for shape in shapes:
        shape.select = True
    bpy.context.scene.objects.active = shapes[0]
    bpy.ops.object.shade_smooth()
    if join == 'True':
        bpy.ops.object.join()
    if join == 'colors':
        for mat in bpy.data.materials:
            for shape in bpy.data.objects:
                shape.select = False
                print(mat)
                if mat in list(shape.data.materials):
                    shape.select = True
                    bpy.context.scene.objects.active = shape
            bpy.ops.object.join()

    bpy.ops.object.origin_set(type='ORIGIN_GEOMETRY', center='MEDIAN')
    bpy.context.scene.update()


if __name__ == '__main__':
    """Uses Blender's limited argv interface to pass args from main script."""
    args = sys.argv[sys.argv.index('--') + 1:]
    show_bonds, join = True, True
    if '--space-filling' in args:
        show_bonds = False
        args.remove('--space-filling')
    if '--no-join' in args:
        join = False
        args.remove('--no-join')
    if '--join-colors' in args:
        join = 'colors'
        args.remove('--join-colors')

    try:
        with open(args[0]) as in_file:
            molecule = json.load(in_file)
    except IOError:
        molecule = json.loads(args[0])

    draw_molecule(molecule, show_bonds=show_bonds, join=join)
