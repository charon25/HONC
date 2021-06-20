from collections import Counter
import random
from typing import List

import pygame as pyg
import pyghelper

from atoms import Atom
import constants as co
from particle import Particle
import utils

class Molecule:
    def __init__(self):
        self.atoms: List[Atom] = []
        self.formula = ''
        self.bonds_count = 0

    def add_atom(self, atom: Atom):
        self.atoms.append(atom)

    def end(self):
        self.formula = Molecule.get_formula(self)
        self.bonds_count = Molecule.get_bonds_count(self)
        self.particles = Molecule.generate_particles(self)

    def get_isoformula(self):
        atoms = []
        for atom in self.atoms:
            atoms.append((atom.get_symbol(), atom.get_signature()))
        atoms.sort()

        formula = []
        for (atom, signature), count in Counter(atoms).items():
            formula.append('{}({}:{})'.format(
                '' if count == 1 else count,
                atom,
                signature
            ))

        return ''.join(formula)

    @staticmethod
    def create_molecule(starting_atom: Atom):
        """Return False if not in a molecule, return the molecule otherwise."""

        queue = [starting_atom]
        molecule = Molecule()

        while len(queue) > 0:
            atom: Atom = queue.pop(0)
            if atom.hasAvailableBonds():
                return False
            for neighbor in atom.bonds:
                if not neighbor in molecule.atoms:
                    molecule.add_atom(neighbor)
                    queue.append(neighbor)
        
        molecule.end()
        return molecule

    @staticmethod
    def get_formula(molecule):
        atoms_count = {'C': 0, 'H': 0, 'N': 0,'O': 0}
        for atom in molecule.atoms:
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

    @staticmethod
    def get_bonds_count(molecule):
        count = 0
        for atom in molecule.atoms:
            count += atom.max_bonds

        return count // 2

    @staticmethod
    def generate_particles(molecule):
        particles = []
        for atom in molecule.atoms:
            n = random.randint(co.PARTICLE_COUNT_BY_ATOM[atom.type.value] - 2, co.PARTICLE_COUNT_BY_ATOM[atom.type.value] + 2)
            for _ in range(n):
                part_x, part_y, part_vx, part_vy = utils.generate_pos_velocity_in_disk(
                    atom.radius,
                    atom.x, atom.y,
                    random.randint(-1, 1), random.randint(-1, 1)
                )
                particles.append(Particle(part_x, part_y, part_vx, part_vy, co.PARTICLE_TEXTURES[random.randrange(3)]))
        
        return particles
