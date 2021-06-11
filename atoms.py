import pygame as pyg
import pyghelper

import constants as co


class Hydrogen:
    def __init__(self, x_center, y_center):
        self.x = x_center
        self.y = y_center
        self.links = []

    def isTouching(self, x, y):
        return (self.x - x) ** 2 + (self.y - y) ** 2 <= co.H_RADIUS ** 2

    def hasAvailableBonds(self):
        return len(self.links) < co.H_BONDS

class Oxygen:
    def __init__(self, x_center, y_center):
        self.x = x_center
        self.y = y_center
        self.links = []

    def isTouching(self, x, y):
        return (self.x - x) ** 2 + (self.y - y) ** 2 <= co.O_RADIUS ** 2

    def hasAvailableBonds(self):
        return len(self.links) < co.O_BONDS

class Nitrogen:
    def __init__(self, x_center, y_center):
        self.x = x_center
        self.y = y_center
        self.links = []

    def isTouching(self, x, y):
        return (self.x - x) ** 2 + (self.y - y) ** 2 <= co.N_RADIUS ** 2

    def hasAvailableBonds(self):
        return len(self.links) < co.N_BONDS

class Carbon:
    def __init__(self, x_center, y_center):
        self.x = x_center
        self.y = y_center
        self.links = []

    def isTouching(self, x, y):
        return (self.x - x) ** 2 + (self.y - y) ** 2 <= co.C_RADIUS ** 2

    def hasAvailableBonds(self):
        return len(self.links) < co.C_BONDS
