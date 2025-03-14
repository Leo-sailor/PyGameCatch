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
        """Construct a falling object object
        initial_position - (Vector 2) initial position of the object
        initial_velocity - (Vector 2) initial velocity of the object
        largest_dimension - (float) maximum dimension of the object in meters
        drag_coef - (float) drag coefficient of the object (optional, default 0)
        mass - (float) mass of the object (kg) (optional, default 1)
        extras -  extra parameters for initialization of the sprite, like image, colorkey, etc."""
        super().__init__(*extras)
        self.position = initial_position
        self.velocity = initial_velocity
        self.drag_coef = drag_coef
        self.mass = mass
        self.large_dim = largest_dimension
    def force_update_position(self, position:Vector2) -> None:
        self.position = position
    def update(self,time: float) -> bool:
        """Update position of the falling object assuming time as passed, returns whether the ball is still on screen
        time - in seconds"""
        assert time>0
        acceleration = Vector2(0, -GRAVITY)
        new_velocity =  acceleration * time
        # calculating new velocity assuming constant acceleration over the time duration 'time'.
        self.position += (self.velocity+ new_velocity) * time * 0.5
        #guesstimate new position cause
        self.velocity += acceleration * time
        # if the object goes fully off screen  return False
        return self.position.y >= -self.large_dim
    def check_landing(self,screen_width):
        """ checks if the ball has landed on the ground
        screen_width - width of the screen in pixels"""
        max_distance = (screen_width/PIXELS_PER_METER)+1
        # see how far the ball can go with current dimentions
        time_until_same_level = (self.velocity.y /9.8)
        distance_until_same_level = time_until_same_level * self.velocity.x
        # see how far the ball was planning on going
        #return false if it was going to far
        return max_distance > distance_until_same_level
    def render(self, screen):
        return True

class Ball(FallingObject):
    def __init__(self, initial_position:Vector2, initial_velocity:Vector2, radius:float, mass:float, color: Tuple[int, int,int]):
        """Construct a Ball object
        initial_position - Vector2 initial position
        initial_velocity - Vector2 initial velocity
        radius - meters
        mass - kg"""
        assert mass>0
        assert radius>0
        super().__init__(initial_position, initial_velocity,2*radius, math.pi * radius*radius * 0.5, mass)
        self.radius = radius
        self.color = color
    def render(self, screen: SurfaceType):
        """ renders the ball onto the provided screen
        screen - SurfaceType screen to draw onto"""
        height = screen.get_rect().height
        # prepareing to invert the y axis
        pg.draw.circle(screen, self.color, (int(self.position.x*PIXELS_PER_METER), height - int(self.position.y*PIXELS_PER_METER)), int(self.radius*PIXELS_PER_METER))
        # ints used as a form of lazy quick rounding
        return True