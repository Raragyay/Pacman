# coding=utf-8
"""
Base entity class for pacman and ghosts
"""

from utility.PVector import PVector
from constants import DEFAULT_SPEED


class Entity:
    """
    Entity class that has basic interactions
    """

    def __init__(self, node, level):
        """
        """
        self.pos = self.node_to_pixel(node)
        self.speed = DEFAULT_SPEED  # For ghost movement
        self.direc = PVector(0, 0)
        self.level = level

        self.nearest_node = node

        self.max_anim_num = None  # Each class will implement this themselves
        self.anim_num = 0

    @staticmethod
    def node_to_pixel(node):
        """
        Utility
        :param node:
        :return:
        """
        return PVector(node.x * 16 + 8, node.y * 16 + 8)

    def pixel_to_node(self):
        """
        Utility
        :return:
        """
        return PVector(int(self.pos.x / 16), int(self.pos.y / 16))

    def is_on_node(self):
        """
        Utility
        :return:
        """
        return (self.pos.x - 8) % 16 == 0 and (self.pos.y - 8) % 16 == 0

    def move(self):
        """
        Used by ghost class
        :return:
        """
        self.pos += self.direc
        self.nearest_node = self.pixel_to_node()

    def top_left(self):
        """
        For drawing purposes
        :return:
        """
        return self.pos.x - 8, self.pos.y - 8

    def direc_to(self, pos: PVector):
        """
        Utility function
        :param pos:
        :return:
        """
        if self.nearest_node == pos:  # We're on the destination
            return PVector(0, 0)
        if self.level.tiles[self.nearest_node].teleport_to_tile == pos:
            return self.direc
        if abs(self.nearest_node - pos) <= PVector(1, 1):
            if self.nearest_node.x == pos.x:
                if self.nearest_node.y < pos.y:
                    return PVector(0, self.speed)  # Right
                else:
                    return PVector(0, -self.speed)  # Left
            elif self.nearest_node.y == pos.y:
                if self.nearest_node.x < pos.x:
                    return PVector(self.speed, 0)  # Down
                else:
                    return PVector(-self.speed, 0)  # Up
        # raise ValueError(
        #         "Position {} is not orthogonally adjacent to entity position: {}".format(pos, self.nearest_node))
        return None

    def update_surf(self):
        """
        Abstract
        :return:
        """
        raise NotImplementedError('Do not create raw entity objects.')

    def increment_frame_num(self):
        """
        Utility function
        :return:
        """
        if self.direc == PVector(0, 0):  # No incrementing if we're not moving.
            return
        self.anim_num += 1
        if self.anim_num > self.max_anim_num:
            self.anim_num = 0

    def update(self):
        """
        Abstract
        :return:
        """
        raise NotImplementedError('Do not create raw entity objects.')

    def check_teleport(self):
        """
        Teleport to the destination tile if we're standing on it
        :return:
        """
        if self.level.get_tile(self.nearest_node).teleport():
            self.nearest_node = self.level.get_tile(self.nearest_node).teleport_to_tile
            self.pos = self.node_to_pixel(self.nearest_node)

    def get_adj_nodes(self):
        """
        Used by exit_box to force our way out of the box.
        :return:
        """
        return [
            self.nearest_node + PVector(1, 0),
            self.nearest_node + PVector(0, 1),
            self.nearest_node + PVector(-1, 0),
            self.nearest_node + PVector(0, -1)]
