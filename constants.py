from enum import Enum

import pyghelper


# Fenêtre
WIDTH = 700
HEIGHT = 700
BG_TEXTURE = pyghelper.Image.create('resources/textures/bg.png')

# Etat de jeu
class GameState(Enum):
    GAME = 0
    MENU = 10
    TUTO = 20
    END = 30

# Général
BONDING_HEIGHT = [None, 15, 2 * 15 + 10, 3 * 15 + 2 * 10]
FONT_PATH = 'resources/font/betterpixels.ttf'

# Molécules
MOLECULE_NAMES = dict()
try:
    with open('resources/molecules.txt', 'r') as fi:
        for line in fi.readlines():
            formula, name = line.strip().split('\t')
            MOLECULE_NAMES[formula] = name
except:pass

# Spawn atome
SPAWN_BORDER_MARGIN = 30
SPAWN_COLLIDES_MARGIN = 8
T0_SPAWN = 1.5 * 60
TINF_SPAWN = 3.5 * 60
MAX_SPAWN_AT_ONCE = 3
ONLY_HYDROGEN = 3
ONLY_OXYGEN = ONLY_HYDROGEN + 8
ONLY_NITROGEN = ONLY_OXYGEN + 14

ATOMS_COUNT_LIMIT = 25

# Texte
DISCOVERED_TEXT = (40, (10, 10), (0, 0, 0)) # Taille, position, couleur
FORMULA_TEXT_SIZE = 30
FORMULA_TEXT_POSITION = lambda n:(10, 45 + 20 * n)
FORMULA_TEXT_COLOR = (0, 0, 0)

# Hydrogène
H_RADIUS = 30
H_BONDS = 1
H_TEXTURE = pyghelper.Image.create('resources/textures/atoms/hydrogen.png')
H_BOND_TEXTURES = [None,
    pyghelper.Image.create('resources/textures/bonds/hydrogen_bond.png')
]

# Oxygène
O_RADIUS = 35
O_BONDS = 2
O_TEXTURE = pyghelper.Image.create('resources/textures/atoms/oxygen.png')
O_BOND_TEXTURES = [None,
    pyghelper.Image.create('resources/textures/bonds/oxygen_bond.png'),
    pyghelper.Image.create('resources/textures/bonds/oxygen_double_bond.png'),
]

# Azote
N_RADIUS = 40
N_BONDS = 3
N_TEXTURE = pyghelper.Image.create('resources/textures/atoms/nitrogen.png')
N_BOND_TEXTURES = [None,
    pyghelper.Image.create('resources/textures/bonds/nitrogen_bond.png'),
    pyghelper.Image.create('resources/textures/bonds/nitrogen_double_bond.png'),
    pyghelper.Image.create('resources/textures/bonds/nitrogen_triple_bond.png'),
]

# Carbone
C_RADIUS = 45
C_BONDS = 4
C_TEXTURE = pyghelper.Image.create('resources/textures/atoms/carbon.png')
C_BOND_TEXTURES = [None,
    pyghelper.Image.create('resources/textures/bonds/carbon_bond.png'),
    pyghelper.Image.create('resources/textures/bonds/carbon_double_bond.png'),
    pyghelper.Image.create('resources/textures/bonds/carbon_triple_bond.png'),
]
