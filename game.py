import math
from typing import List

import pygame as pyg
import pyghelper

from atoms import Atom, Hydrogen, Nitrogen, Carbon
import constants as co


class Game:
    def __init__(self, screen):
        self.screen = screen
        self.clock = pyg.time.Clock()
        # Events
        self.events = pyghelper.EventManager()
        self.events.set_quit_callback(self.stop)
        self.events.set_mousebuttondown_callback(self.click)
        self.events.set_mousemotion_callback(self.mousemove)

        self.is_ended = False

    def start(self):
        self.atoms: List[Atom] = []
        self.bonding = None
        self.bonding_texture = None

        self.temp()
    
    def temp(self):
        self.atoms.append(Hydrogen(0, 0))
        self.atoms.append(Carbon(100, 100))

    def stop(self):
        self.is_ended = True
        pyghelper.Window.close()

    def click(self, data):
        mouse_x, mouse_y = data['pos']
        for atom in self.atoms:
            if atom.isTouching(mouse_x, mouse_y):
                if self.bonding is None:
                    self.bonding = atom
                else:
                    pass # Create the bond and set bonding to None if bond is succesful
                break

    def mousemove(self, data):
        if self.bonding is None:
            return
        
        mouse_x, mouse_y = data['pos']
        atom_x, atom_y = self.bonding.x, self.bonding.y
        distance = math.dist((mouse_x, mouse_y), (atom_x, atom_y))
        angle = -math.atan2(mouse_y - atom_y, mouse_x - atom_x) * 180 / math.pi
        self.bonding_texture = pyg.transform.rotozoom(co.H_BOND_TEXTURE, angle, distance / 50)

    def draw(self):
        self.screen.blit(co.BG_TEXTURE, (0, 0))
        for atom in self.atoms:
            self.screen.blit(atom.texture, atom.getTopLeftCorner())
        if self.bonding is not None and self.bonding_texture is not None:
            self.screen.blit(self.bonding_texture, self.bonding.getTopLeftCorner())
            # self.screen.blit()

    def loop(self):
        self.clock.tick(60)
        self.events.listen()
        self.draw()
        pyg.display.update()
