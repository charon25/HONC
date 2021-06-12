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

# Spawn atome
SPAWN_BORDER_MARGIN_TOP = 50
SPAWN_BORDER_MARGIN_LEFT = 100
SPAWN_COLLIDES_MARGIN = 8
T0_SPAWN = 1.5 * 60
TINF_SPAWN = 3.5 * 60
MAX_SPAWN_AT_ONCE = 3
ONLY_HYDROGEN = 0#3
ONLY_OXYGEN = ONLY_HYDROGEN + 0#8
ONLY_NITROGEN = ONLY_OXYGEN + 0#14

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
            MOLECULE_NAMES[formula] = name
except:pass

# Etoile
STAR_TEXTURES = [
    pyghelper.Image.create('resources/textures/stars/{}.png'.format(index))
    for index in range(1, 10)
]
STAR_SPAWN_RADIUS = 200
STAR_SPEED_MIN = 20
STAR_SPEED_MAX = 40

# Score
SCORE_NEW_MOLECULE = 27.8
MULTIPLIER_ADD = 0.12
MULTIPLIER_DECREASE = 1 - 0.00068
MULTIPLIER_MIN = 0.2

# Texte découverte
DISCOVER_TEXT_DURATION = 60 * 3
DISCOVER_TEXT_SIZE = 35
DISCOVER_TEXT_Y = 665
DISCOVER_TEXT_COLOR = (120, 120, 200)
