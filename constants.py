from enum import IntEnum

import pyghelper


# Fenêtre
WIDTH = 700
HEIGHT = 700
BG_TEXTURE = pyghelper.Image.create('resources/textures/bg.png')

# Etat de jeu
class GameState(IntEnum):
    GAME = 0
    MENU = 10
    TUTO = 20

# Général
BONDING_HEIGHT = [None, 15, 2 * 15 + 10, 3 * 15 + 2 * 10]
FONT_PATH = 'resources/font/betterpixels.ttf'
MAX_SCREENSHAKE = 20
SCREENSHAKE_COUNT = 7

# Spawn atome
SPAWN_BORDER_MARGIN_TOP = 50
SPAWN_BORDER_MARGIN_LEFT = 100
SPAWN_COLLIDES_MARGIN = 8
T0_SPAWN = 1.5 * 60
TINF_SPAWN = 3.5 * 60
MAX_SPAWN_AT_ONCE = 3
ONLY_HYDROGEN = 0
ONLY_OXYGEN = ONLY_HYDROGEN + 2
ONLY_NITROGEN = ONLY_OXYGEN + 4

ATOMS_COUNT_LIMIT = 25

# Textes
DISCOVERED_TEXT = (40, (10, 10), (200, 200, 200)) # Taille, position, couleur
## Score
TEXT_RIGHT_MARGIN = 10
SCORE_TEXT_Y = 10
SCORE_TEXT_SIZE = 40
SCORE_TEXT_COLOR = (200, 200, 200)

## Multiplier
MULTIPLIER_TEXT_Y = 40
def MULTIPLIER_TEXT_COLOR(multiplier):
    intensity = max(0, min(200, 200 / multiplier))
    return (200, intensity, intensity)

## Formules
FORMULA_TEXT_SIZE = 30
FORMULA_TEXT_POSITION = lambda n:(10, 55 + 20 * n)
def FORMULA_TEXT_COLOR(bonds_count):
    intensity = max(0, 200 - 20 * bonds_count)
    return (200, 200, intensity)

#Apparition atomes
APPEARING_DURATION = int(0.1 * 60)

# Hydrogène
H_RADIUS = 30
H_BONDS = 1
H_TEXTURES = [
    pyghelper.Image.create('resources/textures/atoms/hydrogen/hydrogen_0_bond.png'),
    pyghelper.Image.create('resources/textures/atoms/hydrogen/hydrogen_1_bond.png')
]
H_BOND_TEXTURES = [None,
    pyghelper.Image.create('resources/textures/bonds/hydrogen_bond.png')
]

# Oxygène
O_RADIUS = 35
O_BONDS = 2
O_TEXTURES = [
    pyghelper.Image.create('resources/textures/atoms/oxygen/oxygen_0_bond.png'),
    pyghelper.Image.create('resources/textures/atoms/oxygen/oxygen_1_bond.png'),
    pyghelper.Image.create('resources/textures/atoms/oxygen/oxygen_2_bond.png')
]
O_BOND_TEXTURES = [None,
    pyghelper.Image.create('resources/textures/bonds/oxygen_bond.png'),
    pyghelper.Image.create('resources/textures/bonds/oxygen_double_bond.png'),
]

# Azote
N_RADIUS = 40
N_BONDS = 3
N_TEXTURES = [
    pyghelper.Image.create('resources/textures/atoms/nitrogen/nitrogen_0_bond.png'),
    pyghelper.Image.create('resources/textures/atoms/nitrogen/nitrogen_1_bond.png'),
    pyghelper.Image.create('resources/textures/atoms/nitrogen/nitrogen_2_bond.png'),
    pyghelper.Image.create('resources/textures/atoms/nitrogen/nitrogen_3_bond.png')
]
N_BOND_TEXTURES = [None,
    pyghelper.Image.create('resources/textures/bonds/nitrogen_bond.png'),
    pyghelper.Image.create('resources/textures/bonds/nitrogen_double_bond.png'),
    pyghelper.Image.create('resources/textures/bonds/nitrogen_triple_bond.png'),
]

# Carbone
C_RADIUS = 45
C_BONDS = 4
C_TEXTURES = [
    pyghelper.Image.create('resources/textures/atoms/carbon/carbon_0_bond.png'),
    pyghelper.Image.create('resources/textures/atoms/carbon/carbon_1_bond.png'),
    pyghelper.Image.create('resources/textures/atoms/carbon/carbon_2_bond.png'),
    pyghelper.Image.create('resources/textures/atoms/carbon/carbon_3_bond.png'),
    pyghelper.Image.create('resources/textures/atoms/carbon/carbon_4_bond.png')
]
C_BOND_TEXTURES = [None,
    pyghelper.Image.create('resources/textures/bonds/carbon_bond.png'),
    pyghelper.Image.create('resources/textures/bonds/carbon_double_bond.png'),
    pyghelper.Image.create('resources/textures/bonds/carbon_triple_bond.png'),
]

# Molécules
MOLECULE_NAMES = dict()
ATOM_BONDS_COUNT = {'C': C_BONDS, 'H': H_BONDS, 'N': N_BONDS, 'O': O_BONDS}
try:
    with open('resources/molecules.txt', 'r') as fi:
        for line in fi.readlines():
            formula, name = line.strip().split('\t')
            if not formula in MOLECULE_NAMES:
                MOLECULE_NAMES[formula] = name
except:pass

# Etoile
STAR_TEXTURES = [
    pyghelper.Image.create('resources/textures/stars/{}.png'.format(index))
    for index in range(1, 10)
]
STAR_SPAWN_RADIUS = 200
STAR_SPEED_MIN = 5
STAR_SPEED_MAX = 12

# Score
SCORE_NEW_MOLECULE = 27.8
MULTIPLIER_ADD = 0.09
MULTIPLIER_DECREASE = 1 - 0.00068
MULTIPLIER_MIN = 0.2

# Texte découverte
DISCOVER_TEXT_DURATION = 60 * 3.5
DISCOVER_TEXT_SIZE = 45
DISCOVER_TEXT_Y = 620
DISCOVER_TEXT_COLOR = (120, 120, 200)

# Particules
PARTICLE_TEXTURES = [
    pyghelper.Image.create('resources/textures/particles/{}.png'.format(index))
    for index in range(1, 4)
]
PARTICLE_DURATION = int(0.4 * 60)
PARTICLE_COUNT_BY_ATOM = [None, 4, 6, 8, 10]

# Bouton restart
RESTART_BTN_TEXTURE = pyghelper.Image.create('resources/textures/restart_btn.png')
RESTART_BTN_SIZE = 30
RESTART_BTN_POS_X = WIDTH - RESTART_BTN_SIZE - 5
RESTART_BTN_POS_Y = HEIGHT - RESTART_BTN_SIZE - 5

#Menu
MENU_TEXTURE = pyghelper.Image.create('resources/textures/menu.png')
## Bouton Menu
MENU_BTN_X = 252
MENU_BTN_Y = 356
MENU_BTN_SIZE = 200

# Tuto
TUTO_TEXT_SIZE = 40
TUTO_TEXT_Y = lambda n:165 + 40 * n
TUTO_FRAMES_TEXTS = [
    ['Click successively on two atoms', 'to join them together'],
    ['Each atom has a maximum number of bonds', 'H = 1 | O = 2 | N = 3 | C = 4'],
    ['You can create double or triple bonds'],
    [
        'Score points by creating big molecules',
        'but don\'t take too much time',
        'or your multiplier will go down!',
        '',
        'You can get bonus points',
        'by discovering new molecules',
        '',
        'Pick up electrons to enter a spawning frenzy!']
]
TUTO_LAST_ATOM_FRAME = 2
## Frame 0
TUTO_FRAME0_ATOMS = [
    (216, HEIGHT // 2),
    (WIDTH - 216, HEIGHT // 2)
]
## Frame 1
TUTO_FRAME1_ATOMS = [
    (WIDTH // 2, 350),
    (216, 500),
    (WIDTH - 216, 500)
]
## Frame 2
TUTO_FRAME2_ATOMS = [
    (216, HEIGHT // 2),
    (WIDTH - 216, HEIGHT // 2)
]
## Frame 3
TUTO_FRAME3_DURATION = int(2.5 * 60)
TUTO_FRAME3_BTN_TEXTURE = pyghelper.Image.create('resources/textures/play_btn.png')
TUTO_FRAME3_BTN_WIDTH = 300
TUTO_FRAME3_BTN_HEIGHT = 80
TUTO_FRAME3_BTN_X = (WIDTH - TUTO_FRAME3_BTN_WIDTH) // 2
TUTO_FRAME3_BTN_Y = 540

# Effets sonores
## Clic
SOUND_CLICK = 'click'
SOUND_CLICK_PATH = 'resources/audio/sounds/simple_click.wav'

## Liaison
SOUND_BOND = 'bond'
SOUND_BOND_PATHS = [
    'resources/audio/sounds/bond/{}.wav'.format(index)
    for index in range(1, 5)
]

## Molécule
SOUND_MOLECULE = 'molecule'
SOUND_MOLECULE_PATHS = [
    'resources/audio/sounds/molecule/{}.wav'.format(index)
    for index in range(1, 4)
]
SOUND_MOLECULE_NEW = 'molecule_new'
SOUND_MOLECULE_NEW_PATHS = [
    'resources/audio/sounds/molecule/new/{}.wav'.format(index)
    for index in range(1, 4)
]

## Electron
SOUND_ELECTRON = 'electron'
SOUND_ELECTRON_PATH = 'resources/audio/sounds/electron.wav'

## Hint
SOUND_HINT = 'hint'
SOUND_HINT_PATH = 'resources/audio/sounds/hint.wav'

# Electron
ELECTRON_RADIUS = 16
ELECTRON_TEXTURE = pyghelper.Image.create('resources/textures/electron.png')
ELECTRON_PROBABILITY = 1 / (60 * 10)
ELECTRON_MULTIPLIER = 0.2
ELECTRON_DURATION = 2 * 60

# Indice
HINT_DURATION = 20
HINT_TEXT_SIZE = 35
HINT_TEXT_Y = 665
HINT_TEXT_COLOR = (230, 230, 230)
