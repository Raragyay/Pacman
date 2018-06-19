# coding=utf-8
"""
Holds PVector class for specialized math.
"""
from math import ceil, floor, sqrt


class PVector:
    """
    Main class for all velocities and positions. Used for nodes, pixel positions, and velocities.
    """

    def __init__(self, x=0.0, y=0.0):
        """
        Top left is (0,0)
        :param x: Horizontal Location or Velocity
        :param y: Vertical Location or Velocity
        """
        self.x = x
        self.y = y

    def __str__(self):
        return "PVector (x,y): {},{}".format(self.x, self.y)

    def __repr__(self):
        return f'{self.x} {self.y}'

    def __add__(self, other: 'PVector') -> 'PVector':
        return PVector(self.x + other.x, self.y + other.y)

    def __sub__(self, other: 'PVector') -> 'PVector':
        return PVector(self.x - other.x, self.y - other.y)

    def __eq__(self, other: 'PVector') -> bool:
        return other and self.x == other.x and self.y == other.y

    def __ne__(self, other: 'PVector') -> bool:
        return self.x != other.x and self.y != other.y

    def __hash__(self) -> int:
        return hash((self.x, self.y))

    def __abs__(self) -> 'PVector':
        return PVector(abs(self.x), abs(self.y))

    def __mul__(self, scalar: int) -> 'PVector':
        return PVector(self.x * scalar, self.y * scalar)

    def __truediv__(self, scalar: int) -> 'PVector':
        return PVector(self.x / scalar, self.y / scalar)

    def __floordiv__(self, scalar: int) -> 'PVector':
        return PVector(self.x // scalar, self.y // scalar)

    def __mod__(self, scalar: int) -> 'PVector':
        return PVector(self.x % scalar, self.y % scalar)

    def __ceil__(self) -> 'PVector':
        return PVector(ceil(self.x), ceil(self.y))

    def __round__(self) -> 'PVector':
        if self.x < 0:
            new_x = floor(self.x)
        else:
            new_x = ceil(self.x)
        if self.y < 0:
            new_y = floor(self.y)
        else:
            new_y = ceil(self.y)
        return PVector(new_x, new_y)

    def __lt__(self, other: 'PVector') -> bool:
        return self.x < other.x and self.y < other.y

    def __le__(self, other: 'PVector') -> bool:
        return self.x <= other.x and self.y <= other.y

    def direc_to(self, other: 'PVector') -> 'PVector':
        """
        This is only used to build directions for BFS, which is no longer being used.
        :param other: PVector
        :return: PVector
        """
        return other - self

    def dist_from(self, other: 'PVector') -> float:
        """
        Calculate euclidean distance between two points
        :param other: PVector
        :return: float value
        """
        manhattan = abs(self - other)
        euclidean = sqrt(manhattan.x ** 2 + manhattan.y ** 2)
        return euclidean

    @staticmethod
    def from_tuple(tup: tuple) -> 'PVector':
        """
        Converts tuple to PVector
        :param tup: Two element tuple
        :return: PVector
        """
        return PVector(tup[0], tup[1])

    @staticmethod
    def to_tuple(vec: 'PVector') -> tuple:
        """
        Converts PVector to tuple
        :param vec: PVector
        :return: tuple
        """
        return vec.x, vec.y
