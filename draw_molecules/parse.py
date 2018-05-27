"""
Converts a pybel object to a simplified JSON format. Runs various checks to
ensure that locations, hydrogens, and bonds are specified.
"""
import json
from itertools import takewhile

import pybel
ob = pybel.ob

def process(mol, hydrogens=True, generate_coords=True,
            infer_bonds=True, pretty=False):
    """Performs a number of standard edits, then outputs simplified JSON.

    Args:
        mol: Input molecule, as an instance of `pybel.Molecule`.
        hydrogens: (Optional, default True) Includes hydrogen atoms, and infers
            missing hydrogens if True. Removes if False.
        generate_coords: (Optional, default True). Generates atom
            coordinates. Default behavior generates if no coordinates found or
            if molecule is reasonably small.
        infer_bonds: (Optional, default True) Calculates bond locations and
            bond orders. Default behaviors infers if no bond information
            exists.
        pretty: (Optional, default False) Pretty-prints the JSON output. Use
            when learning the code or creating custom scripts.
    Returns:
        A JSON-formatted string representing the molecule.
    """
    
    if hydrogens:
        mol.addh()
    else:
        mol.removeh()

    if generate_coords:
        if not mol.OBMol.HasNonZeroCoords() or len(mol.atoms) < 50:
            mol.make3D(steps=500)

    if infer_bonds:
        bonds = list(ob.OBMolBondIter(mol.OBMol))
        if not bonds:
            mol.OBMol.ConnectTheDots()
            mol.OBMol.PerceiveBondOrders()

    mol.OBMol.Center()

    obj = _pybel_to_object(mol)
    if pretty:
        json_obj = json.dumps(obj, indent=4, sort_keys=True, cls=CustomEncoder)
    else:
        json_obj = json.dumps(obj, separators=(',', ':'))
    return json_obj


def _pybel_to_object(molecule):
    """Converts a pybel molecule to json."""
    table = pybel.ob.OBElementTable()
    atoms = [{'element': table.GetSymbol(atom.atomicnum),
              'location': [float('{:.5f}'.format(c)) for c in atom.coords]}
             for atom in molecule.atoms]
    bonds = [{'atoms': [b.GetBeginAtom().GetIndex(),
                        b.GetEndAtom().GetIndex()],
              'order': b.GetBondOrder()}
             for b in ob.OBMolBondIter(molecule.OBMol)]
    return {'atoms': atoms, 'bonds': bonds}


class CustomEncoder(json.JSONEncoder):
    """Some small edits to pretty-printed json output.

     * Float decimals are truncated to six digits
     * [x, y, z] vectors are displayed on one line
     * Converts numpy arrays to lists and defined objects to dictionaries
     * Atoms and bonds are on one line each (looks more like other formats)
    """
    def default(self, obj):
        """Fired when an unserializable object is hit."""
        if hasattr(obj, '__dict__'):
            return obj.__dict__.copy()
        else:
            raise TypeError(("Object of type %s with value of %s is not JSON "
                            "serializable") % (type(obj), repr(obj)))

    def encode(self, obj):
        """Fired for every object."""
        s = super(CustomEncoder, self).encode(obj)
        # If uncompressed, postprocess for formatting
        if len(s.splitlines()) > 1:
            s = self.postprocess(s)
        return s

    def postprocess(self, json_string):
        """Displays each atom and bond entry on its own line."""
        is_compressing = False
        compressed = []
        spaces = 0
        for row in json_string.split('\n'):
            if is_compressing:
                if row.strip() == '{':
                    compressed.append(row.rstrip())
                elif (len(row) > spaces and row[:spaces] == ' ' * spaces and
                        row[spaces:].rstrip() in [']', '],']):
                    compressed.append(row.rstrip())
                    is_compressing = False
                else:
                    compressed[-1] += ' ' + row.strip()
            else:
                compressed.append(row.rstrip())
                if any(a in row for a in ['atoms', 'bonds']):
                    # Fix to handle issues that arise with empty lists
                    if '[]' in row:
                        continue
                    spaces = sum(1 for _ in takewhile(str.isspace, row))
                    is_compressing = True
        return '\n'.join(compressed)
