import pygame as pg
from pygame import SurfaceType

from fallingObject import FallingObject
class Basket():
    def __init__(self, width: int, height: int, screen_width: int):
        self.width = width
        self.height = height
        self.left_coord = (screen_width-width/2)
        self.left_limit = 0
        self.right_limit = screen_width - width
    def __add__(self, other):
        if isinstance(other,int):
            self.left_coord += other
            self.limit_space()
    def __sub__(self, other):
        if isinstance(other,int):
            self.left_coord -= other
            self.limit_space()
    def render(self,screen: SurfaceType):
        r = pg.rect.Rect(self.left_coord,screen.get_rect().height - self.height,self.width,self.height)
        pg.draw.rect(screen, (0, 0, 0), r)
    def update_screen(self,width):
        self.right_limit = width - self.width
    def limit_space(self):
        if self.left_coord > self.right_limit:
            self.left_coord = self.right_limit
        elif self.left_coord < self.left_limit:
            self.left_coord = self.left_limit
    def is_caught(self, item: FallingObject):
        if item.position.y > 0.2:
            return False
        if self.left_coord <= item.position.x <= self.left_coord+ self.width:
            return True
        else:
            return False

