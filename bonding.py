import math

import pygame as pyg

from atoms import Atom
import constants as co


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

    def update_texture(self, mouse_x, mouse_y, multiplicity=1):
        if self.is_none:
            return
        
        height = co.BONDING_HEIGHT[multiplicity]
        atom_x, atom_y = self.atom.x, self.atom.y
        distance = math.dist((mouse_x, mouse_y), (atom_x, atom_y))
        angle = -math.atan2(mouse_y - atom_y, mouse_x - atom_x) # radians

        self.texture = pyg.Surface((distance, height), flags=pyg.SRCALPHA)
        if multiplicity > 1:print(self.atom.get_bond_texture(multiplicity))
        self.texture.blit(self.atom.get_bond_texture(multiplicity), pyg.Rect(0, 0, distance, height))
        self.texture = pyg.transform.rotate(self.texture, angle * 180 / math.pi) # angle in degrees

        width, height = self.texture.get_width(), self.texture.get_height()
        self.position = (
            atom_x - width / 2 + distance / 2 * math.cos(angle),
            atom_y - height / 2 - distance / 2 * math.sin(angle)
        )

        self.texture_ready = True