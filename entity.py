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
        self.path = deque()
        self.level = level

        self.nearest_node = loc

    def node_to_pixel(self, node):
        return PVector(node.x * 16 + 8, node.y * 16 + 8)

    def pixel_to_node(self):
        return PVector(int((self.pos.x - 8) / 16), int((self.pos.y - 8) / 16))

    def update(self):
        self.move()
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
