# coding=utf-8
from math import ceil, floor, sqrt


class PVector:
    def __init__(self, x=0.0, y=0.0):
        """
        :param x: Horizontal Location or Velocity
        :param y: Vertical Location or Velocity
        """
        self.x = x
        self.y = y

    def __str__(self):
        return "PVector (x,y): {},{}".format(self.x, self.y)

    def __repr__(self):
        return f'{self.x} {self.y}'

    def __add__(self, other):
        return PVector(self.x + other.x, self.y + other.y)

    def __sub__(self, other):
        return PVector(self.x - other.x, self.y - other.y)

    def __eq__(self, other):
        return other and self.x == other.x and self.y == other.y

    def __ne__(self, other):
        return self.x != other.x and self.y != other.y

    def __hash__(self):
        return hash((self.x, self.y))

    def __abs__(self):
        return PVector(abs(self.x), abs(self.y))

    def __mul__(self, scalar: int):
        return PVector(self.x * scalar, self.y * scalar)

    def __truediv__(self, scalar: int):
        return PVector(self.x / scalar, self.y / scalar)

    def __floordiv__(self, scalar: int):
        return PVector(self.x // scalar, self.y // scalar)

    def __mod__(self, scalar: int):
        return PVector(self.x % scalar, self.y % scalar)

    def __ceil__(self):
        return PVector(ceil(self.x), ceil(self.y))

    def __round__(self):
        if self.x < 0:
            new_x = floor(self.x)
        else:
            new_x = ceil(self.x)
        if self.y < 0:
            new_y = floor(self.y)
        else:
            new_y = ceil(self.y)
        return PVector(new_x, new_y)

    def __lt__(self, other):
        return self.x < other.x and self.y < other.y

    def __le__(self, other):
        return self.x <= other.x and self.y <= other.y

    def direc_to(self, other):
        # This is only used to build directions for BFS, which is no longer being used.
        return other - self

    def dist_from(self, other):
        manhattan = abs(self - other)
        euclidean = sqrt(manhattan.x ** 2 + manhattan.y ** 2)
        return euclidean

    @staticmethod
    def from_tuple(tup: tuple):
        return PVector(tup[0], tup[1])

    @staticmethod
    def to_tuple(vec):
        return vec.x, vec.y
