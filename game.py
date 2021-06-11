import pygame as pyg
import pyghelper

import constants as co
from atoms import Hydrogen


class Game:
    def __init__(self):
        self.clock = pyg.time.Clock()
        self.events = pyghelper.EventManager()
        self.events.set_quit_callback(self.stop)
        self.events.set_mousebuttondown_callback(self.click)

        self.is_ended = False

    def start(self):
        self.screen = pyghelper.Window.create(width=co.WIDTH, height=co.HEIGHT, title='GMTK 2021')
        self.atoms = []

        self.temp()
    
    def temp(self):
        self.atoms.append(Hydrogen(0, 0))

    def stop(self):
        self.is_ended = True
        pyghelper.Window.close()

    def click(self, data):
        if data['button'] != 1:
            return
        mouse_x, mouse_y = data['pos']
        for atom in self.atoms:
            if atom.isTouching(mouse_x, mouse_y):
                print("a")

    def loop(self):
        self.clock.tick(60)
        self.events.listen()
