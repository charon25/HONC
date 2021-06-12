from enum import Enum
import math
import random
from typing import List

import pygame as pyg
import pyghelper

import constants as co

class AtomType(Enum):
    HYDROGEN = co.H_BONDS
    OXYGEN = co.O_BONDS
    NITROGEN = co.N_BONDS
    CARBON = co.C_BONDS
    

class Atom:
    def __init__(self, x_center, y_center, radius, max_bonds):
        self.x = x_center
        self.y = y_center
        self.radius = radius
        self.max_bonds = max_bonds
        self.type: AtomType = AtomType(self.max_bonds)
        self.bonds: List[Atom] = []

    def isTouching(self, x, y):
        return (self.x - x) ** 2 + (self.y - y) ** 2 <= self.radius ** 2

    def isColliding(self, x, y, radius):
        return (self.x - x) ** 2 + (self.y - y) ** 2 <= (self.radius + radius + co.SPAWN_COLLIDES_MARGIN) ** 2
        
    def hasAvailableBonds(self):
        return len(self.bonds) < self.max_bonds

    def getTopLeftCorner(self):
        return (self.x - self.radius, self.y - self.radius)

    def get_texture(self):
        if self.type == AtomType.HYDROGEN:
            return co.H_TEXTURES[len(self.bonds)]
        elif self.type == AtomType.OXYGEN:
            return co.O_TEXTURES[len(self.bonds)]
        elif self.type == AtomType.NITROGEN:
            return co.N_TEXTURES[len(self.bonds)]
        elif self.type == AtomType.CARBON:
            return co.C_TEXTURES[len(self.bonds)]

    def get_bond_texture(self, multiplicity):
        if self.type == AtomType.HYDROGEN:
            return co.H_BOND_TEXTURES[multiplicity]
        elif self.type == AtomType.OXYGEN:
            return co.O_BOND_TEXTURES[multiplicity]
        elif self.type == AtomType.NITROGEN:
            return co.N_BOND_TEXTURES[multiplicity]
        elif self.type == AtomType.CARBON:
            return co.C_BOND_TEXTURES[multiplicity]

    def get_symbol(self):
        if self.type == AtomType.HYDROGEN:
            return 'H'
        elif self.type == AtomType.OXYGEN:
            return 'O'
        elif self.type == AtomType.NITROGEN:
            return 'N'
        elif self.type == AtomType.CARBON:
            return 'C'

    def bind(self, atom):
        self.bonds.append(atom)

    def get_multiplicity(self, atom):
        return sum(bonded_atom == atom for bonded_atom in self.bonds)

    @staticmethod
    def generate_random(previous_atoms, weights: List[float] = [0.25, 0.25, 0.25, 0.25]):
        weights = [weights[0], weights[0]+weights[1], weights[0]+weights[1]+weights[2], weights[0]+weights[1]+weights[3]]
        r = random.random()
        if r < weights[0]:
            return Hydrogen.generate_random(previous_atoms)
        elif r < weights[1]:
            return Oxygen.generate_random(previous_atoms)
        elif r < weights[2]:
            return Nitrogen.generate_random(previous_atoms)
        else:
            return Carbon.generate_random(previous_atoms)


class Hydrogen(Atom):
    def __init__(self, x_center, y_center):
        super().__init__(x_center, y_center, co.H_RADIUS, co.H_BONDS)

    @staticmethod
    def generate_random(previous_atoms):
        while True:
            x = random.randrange(co.SPAWN_BORDER_MARGIN + co.H_RADIUS, co.WIDTH - co.SPAWN_BORDER_MARGIN - co.H_RADIUS)
            y = random.randrange(co.SPAWN_BORDER_MARGIN + co.H_RADIUS, co.HEIGHT - co.SPAWN_BORDER_MARGIN - co.H_RADIUS)
            if all(not atom.isColliding(x, y, co.H_RADIUS) for atom in previous_atoms):
                break
        return Hydrogen(x, y)

class Oxygen(Atom):
    def __init__(self, x_center, y_center):
        super().__init__(x_center, y_center, co.O_RADIUS, co.O_BONDS)

    @staticmethod
    def generate_random(previous_atoms):
        while True:
            x = random.randrange(co.SPAWN_BORDER_MARGIN + co.O_RADIUS, co.WIDTH - co.SPAWN_BORDER_MARGIN - co.O_RADIUS)
            y = random.randrange(co.SPAWN_BORDER_MARGIN + co.O_RADIUS, co.HEIGHT - co.SPAWN_BORDER_MARGIN - co.O_RADIUS)
            if all(not atom.isColliding(x, y, co.O_RADIUS) for atom in previous_atoms):
                break
        return Oxygen(x, y)

class Nitrogen(Atom):
    def __init__(self, x_center, y_center):
        super().__init__(x_center, y_center, co.N_RADIUS, co.N_BONDS)

    @staticmethod
    def generate_random(previous_atoms):
        while True:
            x = random.randrange(co.SPAWN_BORDER_MARGIN + co.N_RADIUS, co.WIDTH - co.SPAWN_BORDER_MARGIN - co.N_RADIUS)
            y = random.randrange(co.SPAWN_BORDER_MARGIN + co.N_RADIUS, co.HEIGHT - co.SPAWN_BORDER_MARGIN - co.N_RADIUS)
            if all(not atom.isColliding(x, y, co.N_RADIUS) for atom in previous_atoms):
                break
        return Nitrogen(x, y)

class Carbon(Atom):
    def __init__(self, x_center, y_center):
        super().__init__(x_center, y_center, co.C_RADIUS, co.C_BONDS)

    @staticmethod
    def generate_random(previous_atoms):
        while True:
            x = random.randrange(co.SPAWN_BORDER_MARGIN + co.C_RADIUS, co.WIDTH - co.SPAWN_BORDER_MARGIN - co.C_RADIUS)
            y = random.randrange(co.SPAWN_BORDER_MARGIN + co.C_RADIUS, co.HEIGHT - co.SPAWN_BORDER_MARGIN - co.C_RADIUS)
            if all(not atom.isColliding(x, y, co.C_RADIUS) for atom in previous_atoms):
                break
        return Carbon(x, y)

