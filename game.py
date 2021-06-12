import math
from typing import List, Dict

import pygame as pyg
import pyghelper

from atoms import Atom, Bonding, Carbon, Hydrogen, Nitrogen, Oxygen
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
        self.bonding: Bonding = Bonding()
        self.bonds: Dict[int, List[pyg.Surface, List[int]]] = {}

        self.temp()
    
    def temp(self):
        self.atoms.append(Hydrogen(0, 0))
        self.atoms.append(Carbon(350, 350))

    def stop(self):
        self.is_ended = True
        pyghelper.Window.close()

    def click(self, data):
        if data['button'] == 3 and not self.bonding.is_none:
            self.bonding.disable()
            return

        mouse_x, mouse_y = data['pos']
        for atom in self.atoms:
            if atom.isTouching(mouse_x, mouse_y):
                if self.bonding.is_none:
                    self.bonding.enable(atom)
                else:
                    if atom.hasAvailableBonds():
                        atom.bind(self.bonding.atom)
                        self.bonding.atom.bind(atom)
                        self.bonding.update_texture(atom.x, atom.y)
                        self.bonds[id(self.bonding.atom)] = (self.bonding.texture, self.bonding.position)
                        self.bonding.disable()
                break

    def mousemove(self, data):
        if self.bonding.is_none:
            return
        
        self.bonding.update_texture(*data['pos'])

    def draw(self):
        self.screen.blit(co.BG_TEXTURE, (0, 0))
        for _, (bond_texture, bond_position) in self.bonds.items():
            self.screen.blit(bond_texture, bond_position)
        for atom in self.atoms:
            self.screen.blit(atom.get_texture(), atom.getTopLeftCorner())
        if self.bonding.texture_ready:
            self.screen.blit(self.bonding.texture, self.bonding.position)

    def loop(self):
        self.clock.tick(60)
        self.events.listen()
        self.draw()
        pyg.display.update()
