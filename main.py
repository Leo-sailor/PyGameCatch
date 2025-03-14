from random import randrange
import pygame as pg
from pygame.locals import RESIZABLE
from baseClasses import Vector2
from basket import Basket
from fallingObject import Ball, PIXELS_PER_METER
import os
import time


QUIT = "Press Escape to Quit"


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
def display_game_text(current_score, lives_remaining):
    """Display the text of the game onto the screen"""
    font = pg.font.SysFont("Arial", 36)
    text = font.render(f"Current score: {current_score} Lives Remaining: {lives_remaining}", 1, (255, 255, 255))
    screen.blit(text, (10, 10))
# 0 - main menu, 1 playing, 2 end screen 4 quit, 5 - pause
gamestate = 0

# display waffle (just about works
fullscreen = False
scale_factor = 80
SCREENRECT = pg.Rect(0, 0, 16 * scale_factor, 9 * scale_factor)
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

# finds the all time max score from the file
main_dir = os.path.split(os.path.abspath(__file__))[0]
file = os.path.join(main_dir, "score.txt")
with open(file,"r") as f:
    max_score = float(f.readline())
    for line in f:
        if float(line) > max_score:
            max_score = float(line)

# initialize the variables ready for the game loop
force_dt = False
balls =[]
last_time = time.time_ns()
score = 0
CATCHER = Basket(int(SCREENRECT.width / 10), int(SCREENRECT.height / 20), SCREENRECT.width)
d_t = 0
lives = 5
last_ball_time = time.time_ns()
center = Vector2(screen.get_rect().width/2,screen.get_rect().height/2) # creates vecotr for the center of the screen

while gamestate != 4:
    for event in pg.event.get():
        if event.type == pg.QUIT:
            gamestate = 4
        if event.type == pg.VIDEORESIZE:
            SCREENRECT = pg.Rect(0, 0, event.w, event.h)
            background = pg.transform.scale(bgdtile, SCREENRECT.size)
            CATCHER.update_screen(SCREENRECT.width)
            center = Vector2(screen.get_rect().width / 2, screen.get_rect().height / 2)
        if event.type == pg.KEYDOWN:
            if event.key == pg.K_RETURN:
                if gamestate in[0, 3]:
                    gamestate = 1
                    force_dt = True
                    last_ball_time = time.time_ns()
                    score = 0
                    lives = 5
                    balls = []
                if gamestate == 5:
                    gamestate = 1
                    last_ball_time = time.time_ns()
                    force_dt = True
            if event.key == pg.K_ESCAPE:
                if gamestate == 1:
                    print("paused")
                    gamestate = 5
                elif gamestate in [3, 0, 5]:
                    print("quitting")
                    if score > max_score:
                        max_score = score
                    gamestate =  4

    screen.fill((255,255,255))
    screen.blit(background, (0, 0))
    if gamestate == 1:
        interval = 2 - (score * 0.019)
        now = time.time_ns()
        if (now-last_ball_time) *(10**-9) > interval:
            ball = Ball(Vector2(0, 0), Vector2(randrange(3, 14), randrange(12, 25)),
                        1, 5, (255, 0, 0))
            while not ball.check_landing(screen.get_rect().width):
                ball = Ball(Vector2(0, 0), Vector2(randrange(3, 14), randrange(12, 25)), 1, 5, (255, 0, 0))
            balls.append(ball)
            last_ball_time = now

        d_t = (time.time_ns() - last_time) * 10 **-9
        if force_dt:
            d_t = 0.01
            force_dt = False
        last_time = time.time_ns()
        keys = pg.key.get_pressed()
        if keys[pg.K_LEFT] or keys[pg.K_a]:
            CATCHER -= (d_t * PIXELS_PER_METER * 10)
        if keys[pg.K_RIGHT]or keys[pg.K_d]:
            CATCHER += (d_t * PIXELS_PER_METER * 10)
        display_game_text(score,lives)
        to_remove = set()
        for i,ball in enumerate(balls):
            ball.render(screen)
            if CATCHER.is_caught(ball):
                score += 1
                print("ball Caught")
                to_remove.add(i)
            if not ball.update(d_t):
                to_remove.add(i)
                lives -= 1
                print("ball removed")
        to_remove_list = list(to_remove)
        to_remove_list.sort(reverse=True)
        for i in to_remove_list:
            balls.pop(i)
        CATCHER.render(screen)
        if lives<=1:
            gamestate = 3
    elif gamestate == 0:
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
        font = pg.font.SysFont("Arial", 20)
        text = font.render("Aim: catch as many red balls in the black container as possible", True, (0, 0, 0))
        text.get_rect()
        screen.blit(text, (center + (-text.get_rect().width / 2, (-center.y / 4) + 25)).tup())
        font = pg.font.SysFont("Arial", 20)
        text = font.render("Controls: Use left and right arrow keys to move the container", True, (0, 0, 0))
        text.get_rect()
        screen.blit(text, (center + (-text.get_rect().width / 2, (-center.y / 4) + 50)).tup())
        font = pg.font.SysFont("Arial", 36)
        text = font.render("Press Enter to Start", True, (0, 0, 0))
        text.get_rect()
        screen.blit(text, (center + (-text.get_rect().width / 2 - center.x/4, center.y / 2.8)).tup())
        text = font.render(QUIT, True, (0, 0, 0))
        text.get_rect()
        screen.blit(text, (center + (-text.get_rect().width / 2 + center.x / 4, center.y / 2.8)).tup())
    elif gamestate == 3:
        if score > max_score:
            max_score = score
        r = pg.rect.Rect(*(center/2).tup(),*center.tup())
        pg.draw.rect(screen,(0,0,255),r)
        font = pg.font.SysFont("Arial", 50)
        text = font.render("Game Over!", True, (0, 0, 0))
        text.get_rect()
        screen.blit(text,(center+(-text.get_rect().width/2,-center.y/2.2)).tup())
        font = pg.font.SysFont("Arial", 20)
        text = font.render("Max Score: "+ str(max_score) + "    Your Score: " + str(score), True, (0, 0, 0))
        text.get_rect()
        screen.blit(text, (center + (-text.get_rect().width / 2, -center.y / 4.5)).tup())
        font = pg.font.SysFont("Arial", 36)
        text = font.render("Press Enter to Restart", True, (0, 0, 0))
        text.get_rect()
        screen.blit(text, (center + (-text.get_rect().width / 2 - center.x/4, center.y / 2.8)).tup())
        text = font.render(QUIT, True, (0, 0, 0))
        text.get_rect()
        screen.blit(text, (center + (-text.get_rect().width / 2 + center.x / 4, center.y / 2.8)).tup())
    elif gamestate ==5:
        r = pg.rect.Rect(*(center / 2).tup(), *center.tup())
        pg.draw.rect(screen, (0, 0, 255), r)
        font = pg.font.SysFont("Arial", 50)
        text = font.render("Game Paused!", True, (0, 0, 0))
        text.get_rect()
        screen.blit(text, (center + (-text.get_rect().width / 2, -center.y / 2.2)).tup())
        font = pg.font.SysFont("Arial", 20)
        text = font.render("Max Score: " + str(max_score) + "    Your Current Score: " + str(score), True, (0, 0, 0))
        text.get_rect()
        screen.blit(text, (center + (-text.get_rect().width / 2, -center.y / 4.5)).tup())
        font = pg.font.SysFont("Arial", 36)
        text = font.render("Press Enter to Resume", True, (0, 0, 0))
        text.get_rect()
        screen.blit(text, (center + (-text.get_rect().width / 2 - center.x / 4, center.y / 2.8)).tup())
        text = font.render(QUIT, True, (0, 0, 0))
        text.get_rect()
        screen.blit(text, (center + (-text.get_rect().width / 2 + center.x / 4, center.y / 2.8)).tup())

    pg.display.flip()

with open(file,"a") as f:
    f.writelines(["\n" +str(max_score)])

pg.quit()