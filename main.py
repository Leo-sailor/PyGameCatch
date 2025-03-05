from random import randrange

import pygame as pg
from pygame.gfxdraw import pixel
from pygame.locals import *

from baseClasses import Vector2
from basket import Basket
from fallingObject import Ball, PIXELS_PER_METER
import os
import time
def load_image(file):
    #loads an image and prepares it
    main_dir = os.path.split(os.path.abspath(__file__))[0]
    file = os.path.join(main_dir, "data", file)
    try:
        surface = pg.image.load(file)
    except:
        raise SystemExit(f'Could not load image "{file}" {pg.get_error()}')
    return surface.convert()
pg.init()

def draw_score(score):
    font = pg.font.SysFont("Arial", 36)
    score_text = font.render(f"Score: {score}", True, (0,0,255))
    screen.blit(score_text, (10, 10))


# 0 - main menu, 1 playing, 2 end screen 4 quit, 5 - pause
GAMESTATE = 0

pg.init()
# display nonsense
fullscreen = False
scale_factor = 80
SCREENRECT = pg.Rect(0, 0,16*scale_factor, 9*scale_factor)
winstyle = RESIZABLE
bestdepth = pg.display.mode_ok(SCREENRECT.size, winstyle, 32)
screen = pg.display.set_mode(SCREENRECT.size, winstyle, bestdepth)
pg.display.set_caption("Pygame Catch")
pg.mouse.set_visible(1)

# create the background
bgdtile = load_image("BACK.jpg")
background = pg.transform.scale(bgdtile, SCREENRECT.size)
screen.blit(background, (0, 0))
pg.display.flip()

force_dt = False
balls =[]
last_time = time.time_ns()

main_dir = os.path.split(os.path.abspath(__file__))[0]
file = os.path.join(main_dir, "score.txt")
with open(file,"r") as f:
    max_score = float(f.readline())
    for line in f:
        if float(line) > max_score:
            max_score = float(line)

score = 0
catcher = Basket(int(SCREENRECT.width/10),int(SCREENRECT.height/20), SCREENRECT.width)
while GAMESTATE != 4:
    for event in pg.event.get():
        if event.type == pg.QUIT:
            GAMESTATE = 4
        if event.type == pg.VIDEORESIZE:
            SCREENRECT = pg.Rect(0, 0, event.w, event.h)
            background = pg.transform.scale(bgdtile, SCREENRECT.size)
            catcher.update_screen(SCREENRECT.width)
        if event.type == pg.KEYDOWN:
            if event.key == pg.K_SPACE and GAMESTATE == 1:
                ball = Ball(Vector2(0, 0), Vector2(randrange(3, 14), randrange(12, 25)), 1, 5, (255, 0, 0))
                while not ball.check_landing(screen.get_rect().width):
                    ball = Ball(Vector2(0, 0), Vector2(randrange(3, 14), randrange(12, 25)), 1, 5, (255, 0, 0))
                balls.append(ball)
                print("ball added")
            if event.key == pg.K_RETURN:
                if GAMESTATE in[0,3]:
                    GAMESTATE = 1
                    force_dt = True
                    score = 0
                    balls = []
                if GAMESTATE == 5:
                    GAMESTATE = 1
                    force_dt = True
            if event.key == pg.K_ESCAPE:
                if GAMESTATE == 1:
                    GAMESTATE = 5
                if GAMESTATE in [3,0]:
                    GAMESTATE =  4
            if event.key == pg.K_LEFT and GAMESTATE == 1:
                catcher -= d_t * PIXELS_PER_METER * 10
            if event.key == pg.K_RIGHT and GAMESTATE == 1:
                catcher += d_t * PIXELS_PER_METER * 10

    screen.fill((255,255,255))
    screen.blit(background, (0, 0))
    if GAMESTATE == 1:
        d_t = (time.time_ns() - last_time) * 10 **-9
        if force_dt:
            d_t = 0.01
            force_dt = False
        last_time = time.time_ns()
        to_remove = []
        for i,ball in enumerate(balls):
            ball.render(screen)
            if catcher.is_caught(ball):
                score += 1
            if not ball.update(d_t):
                to_remove.append(i)
        for i in reversed(to_remove):
            balls.pop(i)
        catcher.render(screen)
    elif GAMESTATE == 0:
        center = Vector2(screen.get_rect().width/2,screen.get_rect().height/2)
        r = pg.rect.Rect(*(center/2).tup(),*center.tup())
        pg.draw.rect(screen,(0,0,255),r)
        font = pg.font.SysFont("Arial", 36)
        text = font.render("Leo's Mediocre Catch Game !", True, (0, 0, 0))
        text.get_rect()
        screen.blit(text,(center+(-text.get_rect().width/2,-center.y/2.2)).tup())
        font = pg.font.SysFont("Arial", 20)
        text = font.render("Max Score: "+ str(max_score), True, (0, 0, 0))
        text.get_rect()
        screen.blit(text, (center + (-text.get_rect().width / 2, -center.y / 4)).tup())
        font = pg.font.SysFont("Arial", 36)
        text = font.render("Press Enter to Start", True, (0, 0, 0))
        text.get_rect()
        screen.blit(text, (center + (-text.get_rect().width / 2 - center.x/4, center.y / 2.8)).tup())
        text = font.render("Press Escape to Quit", True, (0, 0, 0))
        text.get_rect()
        screen.blit(text, (center + (-text.get_rect().width / 2 + center.x / 4, center.y / 2.8)).tup())

    pg.display.flip()



pg.quit()