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

    def update_texture(self, mouse_x, mouse_y, binding_atom: Atom = None, multiplicity=1):
        if self.is_none:
            return
        
        height = co.BONDING_HEIGHT[multiplicity]
        atom_x, atom_y = self.atom.x, self.atom.y
        distance = math.dist((mouse_x, mouse_y), (atom_x, atom_y))
        angle = -math.atan2(mouse_y - atom_y, mouse_x - atom_x) # radians

        self.texture = pyg.Surface((distance, height), flags=pyg.SRCALPHA)
        if binding_atom is None or self.atom.type == binding_atom.type:
            self.texture.blit(self.atom.get_bond_texture(multiplicity), pyg.Rect(0, 0, distance, height))
        else:
            dist_1, dist_2 = [distance // 2] * 2 if distance % 2 == 0 else ((distance + 1) // 2, distance // 2)
            self.texture.blit(self.atom.get_bond_texture(multiplicity), pyg.Rect(0, 0, dist_1, height))
            self.texture.blit(binding_atom.get_bond_texture(multiplicity), pyg.Rect(dist_1, 0, dist_2, height))
            pass
        self.texture = pyg.transform.rotate(self.texture, angle * 180 / math.pi) # angle in degrees

        width, height = self.texture.get_width(), self.texture.get_height()
        self.position = (
            atom_x - width / 2 + distance / 2 * math.cos(angle),
            atom_y - height / 2 - distance / 2 * math.sin(angle)
        )

        self.texture_ready = True