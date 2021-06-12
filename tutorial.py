from typing import List

import pygame as pyg

from atoms import Atom, Hydrogen, Nitrogen, Oxygen
import constants as co
import utils


class Tutorial:
    def __init__(self):
        self.texture = None
        self.atoms: List[Atom] = list()
        self.used = False
        self.cooldown = 0
        self.set_frame(0)

    def set_frame(self, frame):
        self.frame = frame
        print(frame)
        self.texture = co.BG_TEXTURE.copy()
        font = utils.get_font(co.TUTO_TEXT_SIZE)

        for i, text in enumerate(co.TUTO_FRAMES_TEXTS[frame]):
            text_surface = font.render(text, False, (200, 200, 200))
            self.texture.blit(text_surface, ((co.WIDTH - text_surface.get_width()) // 2, co.TUTO_TEXT_Y(i)))
        
        
        self.atoms: List[Atom] = list()
        if frame == 0:
            self.atoms.append(Hydrogen(*co.TUTO_FRAME0_ATOMS[0]))
            self.atoms.append(Hydrogen(*co.TUTO_FRAME0_ATOMS[1]))
        elif frame == 1:
            self.atoms.append(Oxygen(*co.TUTO_FRAME1_ATOMS[0]))
            self.atoms.append(Oxygen(*co.TUTO_FRAME1_ATOMS[1]))
            self.atoms.append(Oxygen(*co.TUTO_FRAME1_ATOMS[2]))
        elif frame == 2:
            self.atoms.append(Nitrogen(*co.TUTO_FRAME2_ATOMS[0]))
            self.atoms.append(Nitrogen(*co.TUTO_FRAME2_ATOMS[1]))
        elif frame == 3:
            self.cooldown = co.TUTO_FRAME3_DURATION

        self.used = False
    
    def get_atoms(self):
        self.used = True
        return self.atoms

    def age(self):
        if self.cooldown > 0:
            self.cooldown -= 1
