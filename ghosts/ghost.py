# coding=utf-8
from collections import deque

import constants
from PVector import PVector
from constants import GameMode
from entity import Entity
from level import Level
from pacman import Pacman
from tile import Tile


class Ghost(Entity):
    surfs = ()  # The default frames are a class variable and are modified
    ghost_box = set()

    def __init__(self, loc: PVector, level: Level, pacman: Pacman):
        super().__init__(loc, level)
        self.surf_list = []
        self.surf = None
        self.max_anim_num = 5
        self.pacman = pacman
        if not Ghost.surfs:
            Ghost.load_surfs()
        if not Ghost.ghost_box:  # TODO ADD GHOST BOX TO LEVEL INSTEAD OF GHOST CLASS
            Ghost.load_ghost_box(level)

    def convert_surfaces(self, target_clr: tuple) -> None:
        for surf in Ghost.surfs:
            new_surf = surf.copy()
            new_surf.load_surface(ghost_colour=target_clr, gif_location=constants.sprite_folder)
            self.surf_list.append(new_surf)

    @classmethod
    def load_surfs(cls):
        for frame_num in range(1, 7):
            cls.surfs += (Tile(frame_num, f'ghost {frame_num}', f'Frame {frame_num} of ghost'),)

    @classmethod
    def load_ghost_box(cls, level: Level):
        cls.ghost_box = {level.pinky_start, level.inky_start, level.clyde_start,
                         level.ghost_door}

    def update(self, game_mode: GameMode):
        if game_mode == GameMode.NORMAL:
            self.move()
            self.check_node()

    def check_node(self):
        if self.is_on_node():  # If we need to check our direction
            self.check_teleport()
            self.update_direc()

    def update_surf(self):
        self.increment_frame_num()
        self.surf = self.surf_list[self.anim_num].surface

    def closest_direction(self, target):
        dist = {}
        for node in self.level.edges[self.nearest_node]:
            if self.direc_to(node) == self.direc * -1:  # Cannot go backwards
                continue
            dist[self.direc_to(node)] = node.dist_from(target)
        sorted_dist = sorted(dist.keys(), key=dist.get)
        return sorted_dist[0]

    def bfs(self, target):
        queue = deque([(self.nearest_node, [self.nearest_node])])
        # Every element is a tuple of the current node and the path that it took INCLUDING START
        while queue:
            current, path = queue.popleft()
            if current == target:
                return self.build_direc(path)
            for node in self.level.edges[current]:
                queue.append((node, path + [node]))
        return None

    def build_direc(self, node_path):
        direc_path = []
        if len(node_path) == 1:
            raise ValueError('Ghost is already on Pacman, but has not won yet. ')
        for idx, node in enumerate(node_path):
            if idx == len(node_path) - 1:
                break
            direc_path.append(node.direc_to(node_path[idx + 1]))
        return direc_path

    def collided_with_pacman(self):
        # sprite_dist = abs(self.pos - self.pacman.pos)
        # if sprite_dist.x < 15 and sprite_dist.y < 15:
        #     return True
        return self.nearest_node == self.pacman.nearest_node

    def in_ghost_box(self):
        return self.nearest_node in Ghost.ghost_box

    def exit_box(self):
        if self.nearest_node == self.level.ghost_door:  # Let's get out of the ghost box. And never go back
            assert len(self.level.edges[
                           self.level.ghost_door]) == 1, "There is more than 1 exit for the ghost door. \
                           The ghosts don't know which way to go!"
            outside, = self.level.edges[self.level.ghost_door]
            self.direc = self.direc_to(outside)
        elif self.level.ghost_door in self.get_adj_nodes():  # We're almost out of the ghost box.
            self.direc = self.direc_to(self.level.ghost_door)
        else:  # Find node that is closest to the exit.
            self.direc = self.closest_direction(self.level.ghost_door)
