import math
import random
import time
from typing import List, Dict

import pygame as pyg
import pyghelper

from atoms import Atom, AtomType, Carbon, Electron, Hydrogen, Nitrogen, Oxygen
from bonding import Bonding
import constants as co
from molecule import Molecule
from particle import Particle
from star import Star
from tutorial import Tutorial
import utils


class Game:
    def __init__(self, screen):
        self.screen = screen
        self.clock = pyg.time.Clock()
        # Events
        self.events = pyghelper.EventManager()
        self.events.set_quit_callback(self.stop)

        # Sons
        self.setup_sounds()

        self.is_ended = False

    def setup_sounds(self):
        self.sounds: pyghelper.SoundManager = pyghelper.SoundManager()
        self.sounds.add_sound(co.SOUND_CLICK_PATH, co.SOUND_CLICK, volume=0.5)
        utils.add_multiple_sounds(self.sounds, co.SOUND_BOND_PATHS, co.SOUND_BOND, 0.4)
        utils.add_multiple_sounds(self.sounds, co.SOUND_BOND_PATHS, co.SOUND_BOND, 0.5)
        utils.add_multiple_sounds(self.sounds, co.SOUND_BOND_PATHS, co.SOUND_BOND, 0.3)
        utils.add_multiple_sounds(self.sounds, co.SOUND_MOLECULE_PATHS, co.SOUND_MOLECULE, 0.35)
        utils.add_multiple_sounds(self.sounds, co.SOUND_MOLECULE_NEW_PATHS, co.SOUND_MOLECULE_NEW, 0.55)
        self.sounds.add_sound(co.SOUND_ELECTRON_PATH, co.SOUND_ELECTRON, 0.4)
        self.sounds.add_sound(co.SOUND_HINT_PATH, co.SOUND_HINT, 0.4)

        self.sounds.add_music(co.MUSIC_PATH, co.MUSIC)
        self.sounds.play_music(co.MUSIC, loop=True, volume=0.2)

    def start(self, restart=False, tuto=False):
        # Atomes
        self.atoms: List[Atom] = list()
        self.bonding: Bonding = Bonding()
        self.bonds: Dict[int, Dict[int, List[pyg.Surface, List[int]]]] = dict()
        self.discovered_molecules: List[str] = list()
        self.discovered_molecules_bonds_count: Dict[str, int] = dict()
        self.total_atoms_count = 0
        self.atom_spawn_multiplier = 1.0
        self.electron_cooldown = 0

        # Spawn
        self.atom_spawn_cooldown = utils.atom_mean_over_time(0)

        # Etoiles
        self.star_cooldown = 1
        self.stars: List[Star] = list()

        # Screenshake
        def repeat_00():
            while True:
                yield (0, 0)
        self.offset = repeat_00()

        # Particules
        self.particles: List[Particle] = list()

        # Jeu
        self.tutorial: Tutorial = Tutorial()
        if not restart:
            self.state: co.GameState = co.GameState.MENU
        else:
            if tuto:
                self.state: co.GameState = co.GameState.TUTO
                self.tutorial: Tutorial = Tutorial()
            else:
                self.state: co.GameState = co.GameState.GAME
                self.tutorial.end()
        self.set_callbacks()
        self.weights = [1.0, 0.0, 0.0, 0.0]
        self.score = 0
        self.multiplier = 1.5
        self.discovered_text = None
        self.last_discovered_time = time.time()
        self.hint = ''

    def set_callbacks(self):
        if self.state == co.GameState.MENU:
            self.events.set_mousebuttondown_callback(self.click_menu)
            self.events.set_mousemotion_callback(utils.void)
        elif self.state == co.GameState.TUTO:
            self.events.set_mousebuttondown_callback(self.click_game)
            self.events.set_mousemotion_callback(self.mousemove_game)
        elif self.state == co.GameState.GAME:
            self.events.set_mousebuttondown_callback(self.click_game)
            self.events.set_mousemotion_callback(self.mousemove_game)
            self.events.set_keydown_callback(self.keydown)

    def keydown(self, data):
        if data['key'] == pyg.K_c:
            self.atoms.append(Carbon.generate_random(self.atoms))
        elif data['key'] == pyg.K_h:
            self.atoms.append(Hydrogen.generate_random(self.atoms))
        elif data['key'] == pyg.K_n:
            self.atoms.append(Nitrogen.generate_random(self.atoms))
        elif data['key'] == pyg.K_o:
            self.atoms.append(Oxygen.generate_random(self.atoms))
        elif data['key'] == pyg.K_DELETE:
            self.atoms = []

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

        self.bonding.update_texture(atom.x, atom.y, atom, multiplicity)
        self.add_bond(atom, self.bonding.atom)
        self.bonding.disable()
        
        self.sounds.play_sound(co.SOUND_BOND)

        if not atom.hasAvailableBonds() and not self.bonding.atom.hasAvailableBonds():
            molecule = Molecule.create_molecule(atom)
            if not molecule:
                return
            print(molecule.get_isoformula())
            self.remove_atoms(molecule)
            self.score_molecule(molecule)

    def remove_atoms(self, molecule: Molecule):
        for atom in molecule.atoms:
            if id(atom) in self.bonds:
                self.bonds.pop(id(atom))
            self.atoms.remove(atom)

    def score_molecule(self, molecule: Molecule):
        bonds_count = molecule.bonds_count
        if self.electron_cooldown <= 0:
            self.offset = self.screen_shake(2 * bonds_count)
        if self.state == co.GameState.TUTO:
            self.sounds.play_sound(co.SOUND_MOLECULE)  
            return

        self.score += bonds_count * self.multiplier
        if bonds_count > 1:
            self.multiplier += co.MULTIPLIER_ADD * bonds_count

        self.particles.extend(molecule.particles)

        if not molecule.formula in self.discovered_molecules:
            self.discover_molecule(molecule)
            self.sounds.play_sound(co.SOUND_MOLECULE_NEW)
        else:
            self.sounds.play_sound(co.SOUND_MOLECULE)            

    def discover_molecule(self, molecule: Molecule):
        self.discovered_molecules.append(molecule.formula)
        self.discovered_molecules_bonds_count[molecule.formula] = molecule.bonds_count
        self.discovered_molecules.sort(
            key=lambda formula:self.discovered_molecules_bonds_count[formula] if formula in self.discovered_molecules_bonds_count else 0,
            reverse=True
        )
        
        molecule_name = co.MOLECULE_NAMES[molecule.formula] if molecule.formula in co.MOLECULE_NAMES else molecule.formula
        self.discovered_text = [molecule_name, co.DISCOVER_TEXT_DURATION]
        
        self.score += co.SCORE_NEW_MOLECULE

        self.last_discovered_time = time.time()
        if self.hint == molecule.formula:
            self.hint = ''

    def click_menu(self, data):
        if data['button'] != 1:
            return
        
        mouse_x, mouse_y = data['pos']
        if co.MENU_BTN_X <= mouse_x <= co.MENU_BTN_X + co.MENU_BTN_SIZE and co.MENU_BTN_Y <= mouse_y <= co.MENU_BTN_Y + co.MENU_BTN_SIZE:
            self.sounds.play_sound(co.SOUND_CLICK)
            self.start(restart=True, tuto=False)

    def click_game(self, data):
        if data['button'] == 3:
            if not self.bonding.is_none:
                self.bonding.disable()
            return

        mouse_x, mouse_y = data['pos']

        if co.RESTART_BTN_POS_X <= mouse_x <= co.RESTART_BTN_POS_Y + co.RESTART_BTN_SIZE and co.RESTART_BTN_POS_Y <= mouse_y <= co.RESTART_BTN_POS_X + co.RESTART_BTN_SIZE:
            self.sounds.play_sound(co.SOUND_CLICK)
            self.start(restart=True, tuto=(self.state == co.GameState.TUTO))
        
        if self.tutorial.show_go_btn:
            if co.TUTO_FRAME3_BTN_X <= mouse_x <= co.TUTO_FRAME3_BTN_X + co.TUTO_FRAME3_BTN_WIDTH and co.TUTO_FRAME3_BTN_Y <= mouse_y <= co.TUTO_FRAME3_BTN_Y + co.TUTO_FRAME3_BTN_HEIGHT:
                self.sounds.play_sound(co.SOUND_CLICK)
                self.start(restart=True, tuto=False)

        for atom in self.atoms:
            if atom.isAppearing():
                continue
            if not atom.hasAvailableBonds():
                continue
            if atom.isTouching(mouse_x, mouse_y):
                if atom.type == AtomType.ELECTRON:
                    self.click_electron(electron=atom)
                    break
                if self.bonding.is_none:
                    self.bonding.enable(atom)
                else:
                    if atom != self.bonding.atom:
                        self.create_bond(atom)
                break

    def click_electron(self, electron: Electron):
        self.electron_cooldown = co.ELECTRON_DURATION
        self.atom_spawn_multiplier = co.ELECTRON_MULTIPLIER
        self.offset = self.screen_shake_electron()
        self.sounds.play_sound(co.SOUND_ELECTRON)
        self.atoms.remove(electron)

    def mousemove_game(self, data):
        if self.bonding.is_none:
            return
        
        self.bonding.update_texture(*data['pos'])
    
    def screen_shake(self, bonds_count):
        if bonds_count > co.MAX_SCREENSHAKE:
            bonds_count = co.MAX_SCREENSHAKE
        for _ in range(co.SCREENSHAKE_COUNT):
            yield (random.randint(-bonds_count, bonds_count), random.randint(-bonds_count, bonds_count))
        while True:
            yield (0, 0)

    def screen_shake_electron(self):
        for _ in range(co.ELECTRON_DURATION):
            yield (random.randint(-1, 1), random.randint(-1, 1))
        while True:
            yield (0, 0)

    def get_named_molecules_count(self):
        return sum(formula in co.MOLECULE_NAMES for formula in self.discovered_molecules)

    def draw_score_text(self, game_surface):
        font = utils.get_font(co.SCORE_TEXT_SIZE)
        score_surface = font.render('Score: {:0.00f}'.format(self.score), False, co.SCORE_TEXT_COLOR)
        game_surface.blit(score_surface, (co.WIDTH - score_surface.get_width() - co.TEXT_RIGHT_MARGIN, co.SCORE_TEXT_Y))

        multipler_surface = font.render('(x{:.01f})'.format(self.multiplier), False, co.MULTIPLIER_TEXT_COLOR(self.multiplier))
        game_surface.blit(multipler_surface, (co.WIDTH - multipler_surface.get_width() - co.TEXT_RIGHT_MARGIN, co.MULTIPLIER_TEXT_Y))

    def draw_game(self, tuto=False):
        game_surface = pyg.Surface((co.WIDTH, co.HEIGHT), pyg.SRCALPHA)
        game_surface.blit(co.BG_TEXTURE if not tuto else self.tutorial.texture, (0, 0))

        game_surface.blits([(star.texture, (star.x, star.y)) for star in self.stars])

        if tuto and self.tutorial.show_go_btn:
            game_surface.blit(co.TUTO_FRAME3_BTN_TEXTURE, (co.TUTO_FRAME3_BTN_X, co.TUTO_FRAME3_BTN_Y))
        
        if not tuto:
            utils.draw_text(game_surface, 'Discovered molecules ({}/{})'.format(self.get_named_molecules_count(), len(co.MOLECULE_NAMES)), *co.DISCOVERED_TEXT, [False, False, True])
            for i, formula in enumerate(self.discovered_molecules):
                utils.draw_text(
                    game_surface,
                    '{} ({})'.format(formula, co.MOLECULE_NAMES[formula]) if formula in co.MOLECULE_NAMES else formula,
                    co.FORMULA_TEXT_SIZE,
                    co.FORMULA_TEXT_POSITION(i),
                    co.FORMULA_TEXT_COLOR(self.discovered_molecules_bonds_count[formula])
                )


        game_surface.blits([(particle.texture, (particle.x, particle.y)) for particle in self.particles])

        for _, bonds_dict in self.bonds.items():
            for _, (bond_texture, bond_position) in bonds_dict.items():
                game_surface.blit(bond_texture, bond_position)

        game_surface.blits([(atom.get_texture(), atom.getTopLeftCorner()) for atom in self.atoms])
        
        if not tuto:
            self.draw_score_text(game_surface)

        if self.discovered_text is not None:
                name = self.discovered_text[0]
                font = utils.get_font(co.DISCOVER_TEXT_SIZE)
                discovered_surface = font.render('You discovered: {}!'.format(name), False, co.DISCOVER_TEXT_COLOR)
                game_surface.blit(discovered_surface, ((co.WIDTH - discovered_surface.get_width()) // 2, co.DISCOVER_TEXT_Y))

        if self.hint != '':
            font = utils.get_font(co.HINT_TEXT_SIZE)
            hint_surface = font.render('Hint: try to create {}'.format(self.hint), False, co.HINT_TEXT_COLOR)
            game_surface.blit(hint_surface, ((co.WIDTH - hint_surface.get_width()) // 2, co.HINT_TEXT_Y))

        if self.bonding.texture_ready:
            game_surface.blit(self.bonding.texture, self.bonding.position)

        game_surface.blit(co.RESTART_BTN_TEXTURE, (co.RESTART_BTN_POS_X, co.RESTART_BTN_POS_Y))

        self.screen.blit(game_surface, next(self.offset))

    def draw_menu(self):
        self.screen.blit(co.BG_TEXTURE, (0, 0))
        
        self.screen.blits([(star.texture, (star.x, star.y)) for star in self.stars])

        self.screen.blit(co.MENU_TEXTURE, (0, 0))

    def hydrogen_count(self):
        return sum(atom.type == AtomType.HYDROGEN for atom in self.atoms)
    
    def electron_count(self):
        return sum(atom.type == AtomType.ELECTRON for atom in self.atoms)

    def spawn_atoms(self):
        return
        self.atom_spawn_cooldown -= 1
        if len(self.atoms) < 3:
            self.atom_spawn_cooldown -= 1
        if self.atom_spawn_cooldown <= 0:
            self.atom_spawn_cooldown = random.gauss(utils.atom_mean_over_time(self.total_atoms_count), 1.0) * self.atom_spawn_multiplier
            if len(self.atoms) >= co.ATOMS_COUNT_LIMIT:
                return
            spawn_count = 1 + random.randrange(0, co.MAX_SPAWN_AT_ONCE)
            for _ in range(spawn_count):
                self.atoms.append(Atom.generate_random(self.atoms, self.weights))
            if self.hydrogen_count() < 3:
                self.atoms.append(Hydrogen.generate_random(self.atoms))
            self.weights = utils.weights_over_time(self.total_atoms_count)
            self.total_atoms_count += spawn_count

    def manage_electrons(self):
        return
        if self.electron_cooldown > 0:
            self.electron_cooldown -= 1
            if self.electron_cooldown <= 0:
                self.atom_spawn_multiplier = 1.0

        if self.electron_count() == 0 and random.random() < co.ELECTRON_PROBABILITY:
            self.atoms.append(Electron.generate_random(self.atoms))

    def spawn_star(self):
        self.star_cooldown -= 1
        if self.star_cooldown <= 0:
            self.star_cooldown = 1
            if len(self.stars) > 25:
                return
            for i in range(3):
                star_x, star_y, star_vx, star_vy = utils.generate_pos_velocity_in_disk(
                    co.STAR_SPAWN_RADIUS,
                    co.WIDTH // 2,
                    co.HEIGHT // 2,
                    random.randint(co.STAR_SPEED_MIN, co.STAR_SPEED_MAX),
                    random.randint(co.STAR_SPEED_MIN, co.STAR_SPEED_MAX)
                )
                star_texture = co.STAR_TEXTURES[random.randrange(0, 9)]
                self.stars.append(Star(star_x, star_y, star_vx, star_vy, star_texture))

    def manage_stars(self):
        for star in self.stars:
            star.move()
            if star.out:
                self.stars.remove(star)

    def show_hint(self):
        for formula in co.MOLECULE_NAMES:
            if not formula in self.discovered_molecules:
                self.hint = formula
                self.sounds.play_sound(co.SOUND_HINT)
                return


    def loop_game(self, tuto=False):
        for atom in self.atoms:
            if not atom.isAppearing():
                continue
            atom.appear()
        
        for particle in self.particles:
            particle.age()
            if particle.done:
                self.particles.remove(particle)

        if not tuto:
            self.spawn_atoms()
            self.manage_electrons()

            if self.multiplier > co.MULTIPLIER_MIN:
                self.multiplier *= co.MULTIPLIER_DECREASE
            if self.discovered_text is not None:
                self.discovered_text[1] -= 1
                if self.discovered_text[1] <= 0:
                    self.discovered_text = None
            
            if time.time() - self.last_discovered_time >= co.HINT_DURATION:
                self.last_discovered_time = time.time()
                if self.hint == '':
                    self.show_hint()

        if tuto:
            self.tutorial.age()
            if not self.tutorial.used:
                self.atoms.extend(self.tutorial.get_atoms())
            if self.tutorial.frame <= co.TUTO_LAST_ATOM_FRAME:
                if len(self.atoms) == 0:
                    self.tutorial.set_frame(self.tutorial.frame + 1)

        self.draw_game(tuto)

    def loop(self):
        self.clock.tick(60)
        self.events.listen()
        self.manage_stars()
        self.spawn_star()
        if self.state == co.GameState.GAME:
            self.loop_game()
        elif self.state == co.GameState.MENU:
            self.draw_menu()
        elif self.state == co.GameState.TUTO:
            self.loop_game(True)
        
        pyg.display.update()
