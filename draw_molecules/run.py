"""
Command-line interface for drawing chemicals.
"""
import argparse
import os
import shutil
import subprocess
import sys

import pybel

#from blender_chemicals.parse import process
from parse import process

def run():
    """This method is run by typing `blender-chemicals` into a terminal."""
    parser = argparse.ArgumentParser(description="Imports chemicals into "
                                     "Blender with Open Babel.")
    parser.add_argument('input', help="The file or smiles string to draw.")
    parser.add_argument('--format', type=str, default='auto', help="The "
                        "chemical format of the input file. Defaults to "
                        "'auto', which uses the file extension.")
    parser.add_argument('--convert-only', action='store_true', help="Converts "
                        "the input into a simplified JSON format and prints "
                        "to stdout. Does not draw.")
    parser.add_argument('--space-filling', action='store_true', help="Draws "
                        "a space-filling (instead of ball-and-stick) "
                        "representation.")
    parser.add_argument('--no-join', dest='join', action='store_false',
                        help="Skips joining the atoms/bonds into a single "
                        "mesh. Use if you want to individually edit atoms in "
                        "Blender, but note it will impair performance.")
    parser.add_argument('--join-colors', dest='join', action='store_const',
                        const = 'colors',
                        help="For each material (color), joins all objects "
                        "with that material. Cuts down on the number of "
                        "particle systems needed when morphing.")
    parser.add_argument('--no-hydrogens', dest='hydrogens',
                        action='store_false', help="Avoids drawing hydrogens.")
    parser.add_argument('--no-generate-coords', dest='generate_coords',
                        action='store_false', help="Skips generating 3D "
                        "coordinates.")
    parser.add_argument('--no-infer-bonds', dest='infer_bonds',
                        action='store_false', help="Skips inferring bonds.")

    args = parser.parse_args()

    try:
        with open(args.input) as in_file:
            data = in_file.read()
        is_file = True
    except IOError:
        data = args.input
        is_file = False

    if args.format == 'auto':
        chemformat = os.path.splitext(args.input)[1][1:] if is_file else 'smi'
    else:
        chemformat = args.format

    if not pybel.informats:
        sys.stderr.write("Open babel not properly installed. Exiting.\n")
        sys.exit()
    if chemformat not in pybel.informats:
        prefix = "Inferred" if args.format == 'auto' else "Supplied"
        formats = ', '.join(pybel.informats.keys())
        sys.stderr.write(("{} format '{}' not in available open babel formats."
                          "\n\nSupported formats:\n{}\n"
                          ).format(prefix, chemformat, formats))
        sys.exit()

    try:
        mol = pybel.readstring(chemformat, data)
    except OSError:
        prefix = "Inferred" if args.format == 'auto' else "Supplied"
        debug = ((" - Read input as file." if is_file else
                 " - Inferred input as string, not file.") +
                 "\n - {} format of '{}'.".format(prefix, chemformat))
        sys.stderr.write("Could not read molecule.\n\nDebug:\n" + debug + "\n")
        sys.exit()

    json_mol = process(mol, args.hydrogens, args.generate_coords,
                       args.infer_bonds, args.convert_only)
    if args.convert_only:
        print(json_mol)
        sys.exit()

    mac_path = '/Applications/blender.app/Contents/MacOS/./blender'
    if shutil.which('blender') is not None:
        blender = 'blender'
    elif os.path.isfile(mac_path):
        blender = mac_path
    else:
        sys.stderr.write("Could not find installed copy of Blender. Either "
                         "make sure it's on your path or copy the contents of "
                         "`draw.py` into a running blender instance.\n")
        sys.exit()

    root = os.path.normpath(os.path.dirname(__file__))
    script = os.path.join(root, 'draw.py')
    command = [blender, '--python', script, '--', json_mol]
    if args.space_filling:
        command.append('--space-filling')
    if args.join == False:
        command.append('--no-join')
    if args.join == 'colors':
        command.append('--join-colors')
    with open(os.devnull, 'w') as null:
        subprocess.Popen(command, stdout=null, stderr=null)


if __name__ == '__main__':
    run()
