# coding=utf-8

from PVector import PVector
from constants import default_speed
from level import Level


class Entity:
    level: Level
    nearest_node: PVector

    def __init__(self, loc, level):
        """
        """
        self.pos = self.node_to_pixel(loc)
        self.speed = default_speed  # TODO USE THIS? YES FOR GHOST
        self.direc = PVector(0, 0)
        self.level = level

        self.nearest_node = loc
        self.max_anim_num = None
        self.anim_num = 0

    def node_to_pixel(self, node):
        return PVector(node.x * 16 + 8, node.y * 16 + 8)

    def pixel_to_node(self):
        return PVector(int(self.pos.x / 16), int(self.pos.y / 16))

    # get the middle somehow
    # ex 16-31 should all return 1
    # done

    def check_node(self):
        if self.is_on_node():  # If we need to check our direction
            self.check_teleport()
            if len(self.path) > 1:  # Then if we already have our next direction set
                self.path = self.path[1:]
                # We'll take out our original direction, and set_direc will update our current direction
            else:
                self.update_direc()
                # If we only have one direction, which is the old one now, we need to add a new one on.
            self.set_direc()  # We're then going to update our current direction.

    def is_on_node(self):
        return (self.pos.x - 8) % 16 == 0 and (self.pos.y - 8) % 16 == 0

    def set_direc(self):  # OUTDATED
        self.direc = self.path[0]

    def update_direc(self):
        raise NotImplementedError('Do not create raw entity objects.')

    def move(self):
        self.pos += self.direc
        self.nearest_node = self.pixel_to_node()

    def top_left(self):
        return self.pos.x - 8, self.pos.y - 8

    def direc_to(self, pos: PVector):
        if self.nearest_node == pos:
            return PVector(0, 0)
        if abs(self.nearest_node - pos) <= PVector(1, 1):
            if self.nearest_node.x == pos.x:
                if self.nearest_node.y < pos.y:
                    return PVector(0, self.speed)
                else:
                    return PVector(0, -self.speed)
            elif self.nearest_node.y == pos.y:
                if self.nearest_node.x < pos.x:
                    return PVector(self.speed, 0)
                else:
                    return PVector(-self.speed, 0)
        # raise ValueError(
        #         "Position {} is not orthogonally adjacent to entity position: {}".format(pos, self.nearest_node))
        return None

    def update_surf(self):
        raise NotImplementedError('Do not create raw entity objects.')

    def increment_frame_num(self):
        if self.direc == PVector(0, 0):
            return
        self.anim_num += 1
        if self.anim_num > self.max_anim_num:
            self.anim_num = 0

    def update(self):
        raise NotImplementedError('Do not create raw entity objects.')

    def check_teleport(self):
        if self.level.get_tile(self.nearest_node).teleport():
            self.nearest_node = self.level.get_tile(self.nearest_node).teleport_to_tile
            self.pos = self.node_to_pixel(self.nearest_node)

    def get_adj_nodes(self):
        return [
            self.nearest_node + PVector(1, 0),
            self.nearest_node + PVector(0, 1),
            self.nearest_node + PVector(-1, 0),
            self.nearest_node + PVector(0, -1)]
