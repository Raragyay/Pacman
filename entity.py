# coding=utf-8

from PVector import PVector
from constants import default_speed


class Entity:
    def __init__(self, loc, level):
        """
        """
        self.pos = self.node_to_pixel(loc)
        self.speed = default_speed
        self.direc = PVector(self.speed, 0)
        self.path = [self.direc]
        self.level = level

        self.nearest_node = loc

    def node_to_pixel(self, node):
        return PVector(node.x * 16 + 8, node.y * 16 + 8)

    def pixel_to_node(self):
        return PVector(int(self.pos.x / 16), int(self.pos.y / 16))

    # get the middle somehow
    # ex 16-31 should all return 1

    def check_node(self):
        if self.is_on_node():  # If we need to check our direction
            if len(self.path) > 1:  # Then if we already have our next direction set
                self.path = self.path[1:]
                # We'll take out our original direction, and set_direc will update our current direction
            else:
                self.update_direc()
                # If we only have one direction, which is the old one now, we need to add a new one on.
            self.set_direc()  # We're then going to update our current direction.

    def is_on_node(self):
        return (self.pos.x - 8) % 16 == 0 and (self.pos.y - 8) % 16 == 0

    def set_direc(self):
        self.direc = self.path[0]

    def update_direc(self):
        raise NotImplementedError('Do not create raw entity objects.')

    def move(self):
        self.pos += self.direc
        self.nearest_node = self.pixel_to_node()

    def top_left(self):
        return self.pos.x - 8, self.pos.y - 8

    def direc_to(self, pos: PVector):
        if self.nearest_node.x == pos.x:
            if self.nearest_node.y < pos.y:
                return PVector(0, 1)
            else:
                return PVector(0, -1)
        elif self.nearest_node.y == pos.y:
            if self.nearest_node.x < pos.x:
                return PVector(1, 0)
            else:
                return PVector(-1, 0)
        raise ValueError(
                "Position {} is not orthogonally adjacent to entity position: {}".format(pos, self.nearest_node))
