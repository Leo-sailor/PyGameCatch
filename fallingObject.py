import math
from typing import Tuple

from pygame import SurfaceType

from baseClasses import Vector2, dir_to_vector2
import pygame as pg
GRAVITY = 9.806
DENSITY = 1.225 #kg m^-3
PIXELS_PER_METER = 50

class FallingObject(pg.sprite.Sprite):
    def __init__(self, initial_position:Vector2, initial_velocity:Vector2,largest_dimension:float = 10, drag_coef: float = 0, mass:float = 1,*extras):
        # drag_coef = cross sec area * drag coefficent
        super().__init__(*extras)
        self.position = initial_position
        self.velocity = initial_velocity
        self.drag_coef = drag_coef
        self.mass = mass
        self.large_dim = largest_dimension
    def force_update_position(self, position) -> None:
        self.position = position
    def update(self,time: float) -> bool:
        acceleration = Vector2(0, -GRAVITY)
        new_velocity =  acceleration * time
        self.position += (self.velocity+ new_velocity) * time * 0.5
        self.velocity += acceleration * time
        return self.position.y >= -self.large_dim
    def check_landing(self,screen_width):
        max_distance = (screen_width/PIXELS_PER_METER)+1
        time_until_same_level = (self.velocity.y /9.8)
        distance_until_same_level = time_until_same_level * self.velocity.x
        return max_distance > distance_until_same_level
    def render(self, screen):
        return True

class Ball(FallingObject):
    def __init__(self, initial_position:Vector2, initial_velocity:Vector2, radius:float, mass:float, color: Tuple[int, int,int]):
        # radius - meters
        # mass > 0
        super().__init__(initial_position, initial_velocity,2*radius, math.pi * radius*radius * 0.5, mass)
        self.radius = radius
        self.color = color
    def render(self, screen: SurfaceType):
        height = screen.get_rect().height
        pg.draw.circle(screen, self.color, (int(self.position.x*PIXELS_PER_METER), height - int(self.position.y*PIXELS_PER_METER)), int(self.radius*PIXELS_PER_METER))
        return True