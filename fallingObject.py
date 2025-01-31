from baseClasses import Vector
GRAVITY = 9.806

class FallingObject:
    def __init__(self, initial_position:Vector, initial_velocity:Vector):
        self.position = initial_position
        self.velocity = initial_velocity