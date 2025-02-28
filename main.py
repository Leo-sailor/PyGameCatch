import pygame as pg
from pygame.locals import *
from fallingObject import Ball
import os
import time
def load_image(file):
    """loads an image and prepares it """
    main_dir = os.path.split(os.path.abspath(__file__))[0]
    file = os.path.join(main_dir, "data", file)
    try:
        surface = pg.image.load(file)
    except:
        raise SystemExit(f'Could not load image "{file}" {pg.get_error()}')
    return surface.convert()

# 0 - main menu, 1 playing, 2 end screen
GAMESTATE = 0

pg.init()
# display nonsense
fullscreen = False
scale_factor = 80
SCREENRECT = pg.Rect(0, 0,16*scale_factor, 9*scale_factor)
winstyle = 0
bestdepth = pg.display.mode_ok(SCREENRECT.size, winstyle, 32)
screen = pg.display.set_mode(SCREENRECT.size, winstyle, bestdepth)
pg.display.set_caption("Pygame Catch")
pg.mouse.set_visible(1)

# create the background
bgdtile = load_image("BACK.jpg")
background = pg.transform.scale(bgdtile, SCREENRECT.size)
screen.blit(background, (0, 0))
pg.display.flip()
time.sleep(10)
pg.quit()