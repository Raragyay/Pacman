# coding=utf-8

class PVector:
    def __init__(self, x, y):
        """
        :param x: Horizontal Location or Velocity
        :param y: Vertical Location or Velocity
        """
        self.x = x
        self.y = y

    def __str__(self):
        return "A PVector (x,y): {},{}".format(self.x, self.y)

    __repr__ = __str__

    def __add__(self, other):
        return PVector(self.x + other.x, self.y + other.y)

    def __sub__(self, other):
        return PVector(self.x - other.x, self.y - other.y)

    def __eq__(self, other):
        return self.x == other.x and self.y == other.y

    def __hash__(self):
        return hash(str(self))

    def direc_to(self, other):
        return other - self
