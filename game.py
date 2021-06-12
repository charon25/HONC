import math
import random
from typing import List, Dict

import pygame as pyg
import pyghelper

from atoms import Atom, Carbon, Hydrogen, Nitrogen, Oxygen
from bonding import Bonding
import constants as co
from molecule import Molecule
import utils


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

    def start(self, restart=False):
        # Atomes
        self.atoms: List[Atom] = []
        self.bonding: Bonding = Bonding()
        self.bonds: Dict[int, Dict[int, List[pyg.Surface, List[int]]]] = dict()
        self.discovered_molecules: List[str] = []
        self.total_atoms_count = 0

        # Spawn
        self.atom_spawn_cooldown = utils.atom_mean_over_time(0)

        # Jeu
        if not restart:
            self.state: co.GameState = co.GameState.MENU
        self.weights = [1.0, 0.0, 0.0, 0.0]

        self.temp()


    def temp(self):
        # for i in range(10):
        #     self.atoms.append(Atom.generate_random(self.atoms, [0.25, 0.25, 0.25, 0.25]))
        
        self.state = co.GameState.GAME


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

    def draw_game(self):
        self.screen.blit(co.BG_TEXTURE, (0, 0))
        for _, bonds_dict in self.bonds.items():
            for _, (bond_texture, bond_position) in bonds_dict.items():
                self.screen.blit(bond_texture, bond_position)
        for atom in self.atoms:
            self.screen.blit(atom.get_texture(), atom.getTopLeftCorner())
        if self.bonding.texture_ready:
            self.screen.blit(self.bonding.texture, self.bonding.position)

    def spawn_atom(self):
        self.atom_spawn_cooldown -= 1
        if self.atom_spawn_cooldown <= 0:
            self.atom_spawn_cooldown = random.gauss(utils.atom_mean_over_time(self.total_atoms_count), 1.0)
            if len(self.atoms) >= co.ATOMS_COUNT_LIMIT:
                return
            spawn_count = 1 + random.randrange(0, co.MAX_SPAWN_AT_ONCE)
            for _ in range(spawn_count):
                self.atoms.append(Atom.generate_random(self.atoms, self.weights))
            self.weights = utils.weights_over_time(self.total_atoms_count)
            self.total_atoms_count += spawn_count

    
    def loop(self):
        self.clock.tick(60)
        self.events.listen()
        if self.state == co.GameState.GAME:
            self.draw_game()
            self.spawn_atom()
        elif self.state == co.GameState.END:
            pass
        elif self.state == co.GameState.MENU:
            pass
        elif self.state == co.GameState.TUTO:
            pass
        
        pyg.display.update()
