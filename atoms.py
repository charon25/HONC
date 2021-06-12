from enum import Enum
import math
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
        
    def hasAvailableBonds(self):
        return len(self.bonds) < self.max_bonds

    def getTopLeftCorner(self):
        return (self.x - self.radius, self.y - self.radius)

    def get_texture(self):
        if self.type == AtomType.HYDROGEN:
            return co.H_TEXTURE
        elif self.type == AtomType.OXYGEN:
            return co.O_TEXTURE
        elif self.type == AtomType.NITROGEN:
            return co.N_TEXTURE
        elif self.type == AtomType.CARBON:
            return co.C_TEXTURE

    def get_bond_texture(self):
        return co.H_BOND_TEXTURE
        if self.type == AtomType.HYDROGEN:
            return co.H_BOND_TEXTURE

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


class Hydrogen(Atom):
    def __init__(self, x_center, y_center):
        super().__init__(x_center, y_center, co.H_RADIUS, co.H_BONDS)

class Oxygen(Atom):
    def __init__(self, x_center, y_center):
        super().__init__(x_center, y_center, co.O_RADIUS, co.O_BONDS)

class Nitrogen(Atom):
    def __init__(self, x_center, y_center):
        super().__init__(x_center, y_center, co.N_RADIUS, co.N_BONDS)

class Carbon(Atom):
    def __init__(self, x_center, y_center):
        super().__init__(x_center, y_center, co.C_RADIUS, co.C_BONDS)

class Bonding:
    def __init__(self):
        self.is_none = True
        self.texture_ready = False
        self.atom: Atom = None
        self.texture = None
        self.position = None

    def enable(self, atom: Atom):
        self.is_none = False
        self.atom = atom

    def disable(self):
        self.is_none = True
        self.texture_ready = False

    def update_texture(self, mouse_x, mouse_y):
        if self.is_none:
            return
        
        atom_x, atom_y = self.atom.x, self.atom.y
        distance = math.dist((mouse_x, mouse_y), (atom_x, atom_y))
        angle = -math.atan2(mouse_y - atom_y, mouse_x - atom_x) # radians

        self.texture = pyg.Surface((distance, co.BONDING_HEIGHT), flags=pyg.SRCALPHA)
        self.texture.blit(self.atom.get_bond_texture(), pyg.Rect(0, 0, distance, co.BONDING_HEIGHT))
        self.texture = pyg.transform.rotate(self.texture, angle * 180 / math.pi) # angle in degrees

        width, height = self.texture.get_width(), self.texture.get_height()
        self.position = (
            atom_x - width / 2 + distance / 2 * math.cos(angle),
            atom_y - height / 2 - distance / 2 * math.sin(angle)
        )

        self.texture_ready = True
