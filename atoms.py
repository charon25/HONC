import pygame as pyg
import pyghelper

import constants as co


class Atom:
    def __init__(self, x_center, y_center, radius, max_bonds, texture):
        self.x = x_center
        self.y = y_center
        self.radius = radius
        self.max_bonds = max_bonds
        self.texture = texture

    def isTouching(self, x, y):
        return (self.x - x) ** 2 + (self.y - y) ** 2 <= self.radius ** 2
        
    def hasAvailableBonds(self):
        return len(self.links) < self.max_bonds

    def getTopLeftCorner(self):
        return (self.x - self.radius // 2, self.y - self.radius // 2)

class Hydrogen(Atom):
    def __init__(self, x_center, y_center):
        super().__init__(x_center, y_center, co.H_RADIUS, co.H_BONDS, co.H_TEXTURE)

class Oxygen(Atom):
    def __init__(self, x_center, y_center):
        super().__init__(x_center, y_center, co.O_RADIUS, co.O_BONDS, co.O_TEXTURE)

class Nitrogen(Atom):
    def __init__(self, x_center, y_center):
        super().__init__(x_center, y_center, co.N_RADIUS, co.N_BONDS, co.N_TEXTURE)

class Carbon(Atom):
    def __init__(self, x_center, y_center):
        super().__init__(x_center, y_center, co.C_RADIUS, co.C_BONDS, co.C_TEXTURE)

class Bond:
    pass
