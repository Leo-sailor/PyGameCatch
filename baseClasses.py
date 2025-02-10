import math


class Vector2:
    def __init__(self, x, y):
        self.x = x
        self.y = y
    def __add__(self, other):
        if isinstance(other, Vector2):
            return Vector2(self.x + other.x, self.y + other.y)
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
        rad = math.atan(self.x/self.y)
        deg = rad*180/math.pi
        return deg
def dir_to_vector2(direction: float, magnitude: float) -> Vector2:
    # compass direction
    direction /= 180/math.pi
    if magnitude < 0:
        direction -=math.pi
        magnitude*=-1#
    x = math.sin(direction) * magnitude
    y = math.cos(direction) * magnitude
    return Vector2(x,y)