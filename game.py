import math
from typing import List, Dict

import pygame as pyg
import pyghelper

from atoms import Atom, Carbon, Hydrogen, Nitrogen, Oxygen
from bonding import Bonding
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
        self.bonds: Dict[int, Dict[int, List[pyg.Surface, List[int]]]] = dict()
        self.discovered_molecules: List[str] = []

        self.temp()
    
    def temp(self):
        for i in range(10):
            self.atoms.append(Atom.generate_random(self.atoms, [0.25, 0.25, 0.25, 0.25]))
        # self.atoms.append(Hydrogen(500, 350))
        # self.atoms.append(Hydrogen(200, 350))
        # self.atoms.append(Carbon(350, 200))
        # self.atoms.append(Carbon(350, 400))

    def stop(self):
        self.is_ended = True
        pyghelper.Window.close()

    def add_bond(self, atom_1: Atom, atom_2: Atom):
        index_1, index_2 = id(atom_1), id(atom_2)
        if index_1 < index_2:
            index_1, index_2 = index_2, index_1

        if not index_1 in self.bonds:
            self.bonds[index_1] = dict()
        self.bonds[index_1][index_2] = (self.bonding.texture, self.bonding.position)

    def replace_bond(self, atom_1: Atom, atom_2: Atom):
        index_1, index_2 = id(atom_1), id(atom_2)
        if index_1 < index_2:
            index_1, index_2 = index_2, index_1
        


    def create_bond(self, atom: Atom):
        multiplicity = atom.get_multiplicity(self.bonding.atom)
        if multiplicity == 3:
            return

        atom.bind(self.bonding.atom)
        self.bonding.atom.bind(atom)
        multiplicity += 1

        self.bonding.update_texture(atom.x, atom.y, multiplicity)
        self.add_bond(atom, self.bonding.atom)
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
                    if atom != self.bonding.atom:
                        self.create_bond(atom)
                break

    def mousemove(self, data):
        if self.bonding.is_none:
            return
        
        self.bonding.update_texture(*data['pos'])

    def draw(self):
        self.screen.blit(co.BG_TEXTURE, (0, 0))
        for _, bonds_dict in self.bonds.items():
            for _, (bond_texture, bond_position) in bonds_dict.items():
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
