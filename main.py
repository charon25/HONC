import pygame
import pyghelper

pygame.init()
pygame.display.init()
screen = pyghelper.Window.create(width=700, height=700, title='GMTK 2021', icon_path='resources/icon.png')

from game import Game

pygame.init()

game = Game(screen)
game.start()

while not game.is_ended:
    game.loop()

game.stop()
