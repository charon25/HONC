import pyghelper


# Fenêtre
WIDTH = 700
HEIGHT = 700
BG_TEXTURE = pyghelper.Image.create('resources/textures/bg.png')

# Général
BONDING_HEIGHT = [None, 15, 2 * 15 + 10, 3 * 15 + 2 * 10]

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
