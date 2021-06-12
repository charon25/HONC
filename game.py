import math
from typing import List, Dict

import pygame as pyg
import pyghelper

from atoms import Atom, Bonding, Carbon, Hydrogen, Nitrogen, Oxygen
import constants as co
from molecule import Molecule


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
        self.discovered_molecules: List[str] = []

        self.temp()
    
    def temp(self):
        self.atoms.append(Hydrogen(500, 350))
        self.atoms.append(Hydrogen(200, 350))
        self.atoms.append(Oxygen(350, 200))
        self.atoms.append(Oxygen(350, 400))

    def stop(self):
        self.is_ended = True
        pyghelper.Window.close()

    def create_bond(self, atom):
        atom.bind(self.bonding.atom)        
        self.bonding.atom.bind(atom)
        self.bonding.update_texture(atom.x, atom.y)
        self.bonds[id(self.bonding.atom)] = (self.bonding.texture, self.bonding.position)
        self.bonding.disable()
        if not atom.hasAvailableBonds() and not self.bonding.atom.hasAvailableBonds():
            molecule = Molecule.create_molecule(atom)
            if not molecule:
                return
            self.remove_atoms(molecule)
            self.score_molecule(molecule)

    def remove_atoms(self, molecule: Molecule):
        for atom in molecule.atoms:
            if id(atom) in self.bonds:
                self.bonds.pop(id(atom))
            self.atoms.remove(atom)

    def score_molecule(self, molecule: Molecule):
        if not molecule.formula in self.discovered_molecules:
            self.discovered_molecules.append(molecule.formula)
            print("New molecule :", molecule.formula)

    def click(self, data):
        if data['button'] == 3 and not self.bonding.is_none:
            self.bonding.disable()
            return

        mouse_x, mouse_y = data['pos']
        for atom in self.atoms:
            if not atom.hasAvailableBonds():
                continue
            if atom.isTouching(mouse_x, mouse_y):
                if self.bonding.is_none:
                    self.bonding.enable(atom)
                else:
                    self.create_bond(atom)
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
