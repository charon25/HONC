import math
import random

import pygame as pyg
import pyghelper
import re

import constants as co


def atom_mean_over_time(n):
    return co.TINF_SPAWN + (co.T0_SPAWN - co.TINF_SPAWN) / (1 + 0.08 * n)

def weights_over_time(n):
    if n < co.ONLY_HYDROGEN:
        return [1, 0, 0, 0]
    if n < co.ONLY_OXYGEN:
        return [6 / 12, 6 / 12, 0, 0]
    if n < co.ONLY_NITROGEN:
        return [16 / 41, 16 / 41, 9 / 41, 0]
    return [45 / 123, 36 / 123, 24 / 123, 18 / 123]

def get_font(size, bold=False, italic=False, underline=False):
    try:
        font = pyg.font.Font(co.FONT_PATH, size)
    except:
        font = pyg.font.SysFont("arial", size)
    font.set_bold(bold)
    font.set_italic(italic)
    font.set_underline(underline)
    return font
    
def draw_text(screen, text, size, pos, color, flags=[]):
    if len(flags) < 3:
        flags += [False] * (3 - len(flags))
    font: pyg.font.Font = get_font(size, flags[0], flags[1], flags[2])
    img = font.render(text, False, color)
    screen.blit(img, pos)

def get_bonds_count_from_formula(formula):
    return sum(co.ATOM_BONDS_COUNT[atom] * (int(count) if count != '' else 1) for atom, count in re.findall(r'(\w)(\d*)', formula)) // 2

def generate_pos_velocity_in_disk(disk_radius, x_center, y_center, vx, vy):
    radius = disk_radius * random.random()
    angle = random.random() * 2 * math.pi

    return (
        x_center + radius * math.cos(angle),
        y_center + radius * math.sin(angle),
        vx * math.cos(angle),
        vy * math.sin(angle)
    )

def add_multiple_sounds(sound_manager: pyghelper.SoundManager, sounds, sound_name, volume=1.0):
    for path in sounds:
        sound_manager.add_sound(path, sound_name, volume=volume)

def void(args):
    pass
