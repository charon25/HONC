from typing import List

import pygame as pyg
import pyghelper

from atoms import Atom


def get_formula(molecule: List[Atom]):
    atoms_count = {'C': 0, 'H': 0, 'N': 0,'O': 0}
    for atom in molecule:
        atoms_count[atom.get_symbol()] += 1
    
    formula = []
    for symbol, count in atoms_count.items():
        if count == 0:
            continue
        if count == 1:
            formula.append(symbol)
        else:
            formula.extend([symbol, str(count)])
    
    return ''.join(formula)

def get_molecule(starting_atom: Atom):
    """Return False if not in a molecule, return the molecule otherwise."""

    queue = [starting_atom]
    in_molecule = []

    while len(queue) > 0:
        atom: Atom = queue.pop(0)
        if atom.hasAvailableBonds():
            return False
        for neighbor in atom.bonds:
            if not neighbor in in_molecule:
                in_molecule.append(neighbor)
                queue.append(neighbor)
    
    return (in_molecule, get_formula(in_molecule))
