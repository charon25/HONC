import math
import random
from typing import List, Dict

import pygame as pyg
import pyghelper

from atoms import Atom, Carbon, Hydrogen, Nitrogen, Oxygen
from bonding import Bonding
import constants as co
from molecule import Molecule
from star import Star
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
        self.atoms: List[Atom] = list()
        self.bonding: Bonding = Bonding()
        self.bonds: Dict[int, Dict[int, List[pyg.Surface, List[int]]]] = dict()
        self.discovered_molecules: List[str] = list()
        self.discovered_molecules_bonds_count: Dict[str, int] = dict()
        self.total_atoms_count = 0

        # Spawn
        self.atom_spawn_cooldown = utils.atom_mean_over_time(0)

        # Etoiles
        self.star_cooldown = 1
        self.stars = []

        # Jeu
        if not restart:
            self.state: co.GameState = co.GameState.MENU
        self.weights = [1.0, 0.0, 0.0, 0.0]
        self.score = 0
        self.multiplier = 1.5
        self.discovered_text = None

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
        bonds_count = utils.get_bonds_count_from_formula(molecule.formula)
        self.score += bonds_count * self.multiplier
        if bonds_count > 1:
            self.multiplier += co.MULTIPLIER_ADD * bonds_count

        if not molecule.formula in self.discovered_molecules:
            self.discovered_molecules.append(molecule.formula)
            self.discovered_molecules_bonds_count[molecule.formula] = bonds_count
            self.discovered_molecules.sort(key=lambda formula:utils.get_bonds_count_from_formula(formula), reverse=True)
            self.score += co.SCORE_NEW_MOLECULE
            molecule_name = co.MOLECULE_NAMES[molecule.formula] if molecule.formula in co.MOLECULE_NAMES else molecule.formula
            self.discovered_text = [molecule_name, co.DISCOVER_TEXT_DURATION]
            
            print("New molecule :", molecule.formula)
            try:
                print("Name :", co.MOLECULE_NAMES[molecule.formula])
            except:
                print("!!!! Unknown formula !!!!")

    def click(self, data):
        if data['button'] == 3 and not self.bonding.is_none:
            self.bonding.disable()
            return

        mouse_x, mouse_y = data['pos']
        for atom in self.atoms:
            if atom.isAppearing():
                continue
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

    def draw_score_text(self):
        font = utils.get_font(co.SCORE_TEXT_SIZE)
        score_surface = font.render('Score: {:0.00f}'.format(self.score), False, co.SCORE_TEXT_COLOR)
        self.screen.blit(score_surface, (co.WIDTH - score_surface.get_width() - co.TEXT_RIGHT_MARGIN, co.SCORE_TEXT_Y))

        multipler_surface = font.render('(x{:.01f})'.format(self.multiplier), False, co.MULTIPLIER_TEXT_COLOR(self.multiplier))
        self.screen.blit(multipler_surface, (co.WIDTH - multipler_surface.get_width() - co.TEXT_RIGHT_MARGIN, co.MULTIPLIER_TEXT_Y))

    def draw_game(self):
        self.screen.blit(co.BG_TEXTURE, (0, 0))

        self.screen.blits([(star.texture, (star.x, star.y)) for star in self.stars])

        for _, bonds_dict in self.bonds.items():
            for _, (bond_texture, bond_position) in bonds_dict.items():
                self.screen.blit(bond_texture, bond_position)

        self.screen.blits([(atom.get_texture(), atom.getTopLeftCorner()) for atom in self.atoms])

        if self.bonding.texture_ready:
            self.screen.blit(self.bonding.texture, self.bonding.position)
        
        self.draw_score_text()
        utils.draw_text(self.screen, 'Discovered molecules', *co.DISCOVERED_TEXT, [False, False, True])
        for i, formula in enumerate(self.discovered_molecules):
            utils.draw_text(
                self.screen,
                formula,
                co.FORMULA_TEXT_SIZE,
                co.FORMULA_TEXT_POSITION(i),
                co.FORMULA_TEXT_COLOR(self.discovered_molecules_bonds_count[formula])
            )
        if self.discovered_text is not None:
            name = self.discovered_text[0]
            font = utils.get_font(co.DISCOVER_TEXT_SIZE)
            discovered_surface = font.render('You discovered: {}!'.format(name), False, co.DISCOVER_TEXT_COLOR)
            self.screen.blit(discovered_surface, ((co.WIDTH - discovered_surface.get_width()) // 2, co.DISCOVER_TEXT_Y))


    def hydrogen_count(self):
        return sum(type(atom) == Hydrogen for atom in self.atoms)

    def spawn_atom(self):
        self.atom_spawn_cooldown -= 1
        if self.atom_spawn_cooldown <= 0:
            self.atom_spawn_cooldown = random.gauss(utils.atom_mean_over_time(self.total_atoms_count), 1.0)
            if len(self.atoms) >= co.ATOMS_COUNT_LIMIT:
                return
            spawn_count = 1 + random.randrange(0, co.MAX_SPAWN_AT_ONCE)
            for _ in range(spawn_count):
                self.atoms.append(Atom.generate_random(self.atoms, self.weights))
            if self.hydrogen_count() < 3:
                self.atoms.append(Hydrogen.generate_random(self.atoms))
            self.weights = utils.weights_over_time(self.total_atoms_count)
            self.total_atoms_count += spawn_count

    def spawn_star(self):
        self.star_cooldown -= 1
        if self.star_cooldown <= 0:
            self.star_cooldown = 1
            if len(self.stars) > 25:
                return
            for i in range(3):
                radius = co.STAR_SPAWN_RADIUS * random.random()
                angle = random.random() * 2 * math.pi
                star_x, star_y = co.WIDTH // 2 + radius * math.cos(angle), co.HEIGHT // 2 + radius * math.sin(angle)
                star_vx = random.randint(co.STAR_SPEED_MIN, co.STAR_SPEED_MAX) * math.cos(angle)
                star_vy = random.randint(co.STAR_SPEED_MIN, co.STAR_SPEED_MAX) * math.sin(angle)
                star_texture = co.STAR_TEXTURES[random.randrange(0, 9)]
                self.stars.append(Star(star_x, star_y, star_vx, star_vy, star_texture))

    def manage_stars(self):
        for star in self.stars:
            star.move()
            if star.out:
                self.stars.remove(star)
    
    def loop_game(self):
        for atom in self.atoms:
            if not atom.isAppearing():
                continue
            atom.appear()

        self.spawn_atom()
        self.spawn_star()
        self.manage_stars()

        if self.multiplier > co.MULTIPLIER_MIN:
            self.multiplier *= co.MULTIPLIER_DECREASE
        if self.discovered_text is not None:
            self.discovered_text[1] -= 1
            if self.discovered_text[1] <= 0:
                self.discovered_text = None
        self.draw_game()
    def loop(self):
        self.clock.tick(60)
        self.events.listen()
        if self.state == co.GameState.GAME:
            self.loop_game()
        elif self.state == co.GameState.END:
            pass
        elif self.state == co.GameState.MENU:
            pass
        elif self.state == co.GameState.TUTO:
            pass
        
        pyg.display.update()
