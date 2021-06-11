import pygame as pyg
import pyghelper

import constants as co


class Game:
    def __init__(self):
        self.clock = pyg.time.Clock()
        self.events = pyghelper.EventManager()
        self.events.set_quit_callback(self.stop)

        self.is_ended = False

    def start(self):
        self.screen = pyghelper.Window.create(width=700, height=700, title='GMTK 2021')
        pass

    def stop(self):
        self.is_ended = True
        pyghelper.Window.close()


    def loop(self):
        self.clock.tick(60)
        self.events.listen()