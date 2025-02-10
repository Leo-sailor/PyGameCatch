import math
from baseClasses import Vector2, dir_to_vector2

GRAVITY = 9.806
DENSITY = 1.225 #kg m^-3
PIXELS_PER_METER = 100

class FallingObject():
    def __init__(self, initial_position:Vector2, initial_velocity:Vector2,largest_dimension:float = 10, drag_coef: float = 0, mass:float = 1):
        # drag_coef = cross sec area * drag coefficent
        self.position = initial_position
        self.velocity = initial_velocity
        self.drag_coef = drag_coef
        self.mass = mass
        self.large_dim = largest_dimension
    def force_update_position(self, position) -> None:
        self.position = position
    def iterate(self,time: float) -> bool:
        acceleration = Vector2(0, -GRAVITY)
        drag_force = (abs(self.velocity)**2) * self.drag_coef * 0.5 * DENSITY
        acceleration += dir_to_vector2(-self.velocity.direction(), drag_force / self.mass)
        new_velocity =  acceleration * time
        self.position += (self.velocity+ new_velocity) * time * 0.5
        self.velocity += acceleration * time
        return self.position.y >= -self.large_dim

class Ball(FallingObject):
    def __init__(self, initial_position:Vector2, initial_velocity:Vector2, radius:float, mass:float):
        # radius in meters
        # mass > 0
        super().__init__(initial_position, initial_velocity,2*radius * PIXELS_PER_METER, math.pi * radius*radius * 0.5, mass)
        self.radius = radius