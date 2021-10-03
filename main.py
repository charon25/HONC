import pygame
import pyghelper

WIDTH = 1000
HEIGHT = 700

pygame.init()
pygame.display.init()
screen = pyghelper.Window.create(width=WIDTH, height=HEIGHT, title='GMTK 2021', icon_path='resources/icon.png')

from game import Game

pygame.init()

game = Game(screen)
game.start()

while not game.is_ended:
    game.loop()

game.stop()
