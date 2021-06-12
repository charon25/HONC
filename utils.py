import pygame as pyg

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
    return [54 / 123, 33 / 123, 21 / 123, 15 / 123]

def get_font(size, bold, italic, underline):
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
