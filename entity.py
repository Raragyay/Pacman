# coding=utf-8
from collections import deque

from PVector import PVector
from constants import default_speed


class Entity:
    def __init__(self, loc, level):
        """

        :param x: Node Location vertically
        :param y: Node location horizontally
        """
        self.pos = self.node_to_pixel(loc)
        self.speed = default_speed
        self.direc = PVector(0, self.speed)
        self.path = [PVector(0, self.speed)]
        self.level = level

        self.nearest_node = loc

    def node_to_pixel(self, node):
        return PVector(node.x * 16 + 8, node.y * 16 + 8)

    def pixel_to_node(self):
        return PVector(int((self.pos.x - 8) / 16), int((self.pos.y - 8) / 16))

    def check_node(self):
        if self.is_on_node():
            if len(self.path) > 1:
                self.path = self.path[1:]
            else:
                self.update_direc()
            self.set_direc()

    def is_on_node(self):
        return (self.pos.x - 8) % 16 == 0 and (self.pos.y - 8) % 16 == 0

    def set_direc(self):
        self.direc = self.path[0]

    def update_direc(self):
        raise NotImplementedError('Do not create raw entity objects.')

    def move(self):
        self.pos += self.direc
        self.nearest_node = self.pixel_to_node()

    def pixel_location(self):
        return self.pos.x - 8, self.pos.y - 8

    def direc_to(self, vec: PVector):
        if self.nearest_node.x == vec.x:
            if self.nearest_node.y < vec.y:
                return PVector(0, 1)
            else:
                return PVector(0, -1)
        elif self.nearest_node.y == vec.y:
            if self.nearest_node.x < vec.x:
                return PVector(1, 0)
            else:
                return PVector(-1, 0)
        raise ValueError
