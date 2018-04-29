# coding=utf-8
from collections import deque

from PVector import PVector
from constants import constants


class Entity:
    def __init__(self, loc):
        """

        :param x: Pixel Location vertically
        :param y: Pixel location horizontally
        """
        self.pos = loc
        self.speed = constants.default_speed
        self.direc = PVector(0,self.speed)
        self.path = deque()

        self.set_nearest_node(loc)

    def set_nearest_node(self, loc):
        self.nearest_node = PVector(int((loc.x + 8) / 16), int((loc.y + 8) / 16))

    def move(self):
        self.pos += self.direc
        if self.is_on_node():
            if self.path:
                self.path = self.path[1:]
                self.set_direc()
            else:
                self.update_direc()

    def is_on_node(self):
        return self.pos.x % 16 == 0 and self.pos.y % 16 == 0

    def set_direc(self):
        self.direc = self.path[0]

    def update_direc(self):
        raise NotImplementedError('Do not create raw entity objects.')
