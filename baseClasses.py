import math
from typing import TypeVarTuple


class Vector2:
    def __init__(self, x, y):
        self.x = x
        self.y = y
    def __add__(self, other):
        if isinstance(other, Vector2):
            return Vector2(self.x + other.x, self.y + other.y)
        if isinstance(other, tuple):
            return Vector2(self.x + other[0], self.y + other[1])
    def __abs__(self):
        return (self.x ** 2 + self.y ** 2) ** 0.5
    def __sub__(self, other):
        if isinstance(other, Vector2):
            return Vector2(self.x - other.x, self.y - other.y)
    def __mul__(self, scalar):
        return Vector2(self.x * scalar, self.y * scalar)
    def __truediv__(self, scalar):
        return Vector2(self.x / scalar, self.y / scalar)
    def __str__(self):
        return f"Vector({self.x}, {self.y})"
    def __repr__(self):
        return f"Vector({self.x}, {self.y})"
    def __eq__(self, other):
        if isinstance(other, Vector2):
            return self.x == other.x and self.y == other.y
        return False
    def dot(self, other):
        if isinstance(other, Vector2):
            return self.x * other.x + self.y * other.y
        return None
    def __len__(self):
        return abs(self)
    def normalize(self):
        magnitude = abs(self)
        if magnitude > 0:
            return self / magnitude
    def direction(self):
        if self.y == 0 and self.x == 0:
            return 0
        angle_rad = math.atan2(self.y, self.x)
        angle_deg = math.degrees(angle_rad)
        return (90 - angle_deg) % 360
    def tup(self):
        return (self.x,self.y)
def dir_to_vector2(direction: float, magnitude: float) -> Vector2:
    # compass direction
    direction /= 180/math.pi
    if magnitude < 0:
        direction -=math.pi
        magnitude*=-1
    x = math.sin(direction) * magnitude
    y = math.cos(direction) * magnitude
    if abs(x)< 10**-8:
        x = 0
    if abs(y)< 10**-8:
        y = 0
    return Vector2(x,y)
if __name__ == '__main__':
    vectors = [Vector2(0,0),Vector2(0,1),Vector2(1,1),Vector2(1,0),Vector2(0,-1),Vector2(-1,-1),Vector2(-1,0)]
    expected = [0,0,45,90,180,225,270]
    for i in range(0,len(vectors)):
        print("Vector: "+ str(vectors[i]) + " expected: "+ str(expected[i])+ " got: "+ str(vectors[i].direction()))
    vectors = [(0,1),(0,0),(90,1),(180,1),(270,1),(360,1),(-90,1),(-270,1)]
    expected = [(0,1),(0,0),(1,0),(0,-1),(-1,0),(0,1),(-1,0),(1,0)]
    for i in range(0, len(vectors)):
        print("Dir,Mag : " + str(vectors[i]) + " expected: " + str(expected[i]) + " got: " + str(dir_to_vector2(*vectors[i])))