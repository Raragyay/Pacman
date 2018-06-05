# coding=utf-8
import os
from collections import deque

import pygame

import constants
from PVector import PVector
from entity import Entity
from level import Level
from tile import Tile


class Ghost(Entity):
    surfs = ()  # The default frames are a class variable and are modified

    def __init__(self, loc: PVector, level: Level):
        super().__init__(loc, level)
        self.surf_list = []
        self.surf = None
        self.max_anim_num = 5
        if not Ghost.surfs:
            Ghost.load_surfs()

    def convert_surfaces(self, target_clr):
        for surf in Ghost.surfs:
            new_surf = surf.copy()
            new_surf.load_surface(ghost_colour=target_clr, gif_location=constants.sprite_folder)
            self.surf_list.append(new_surf)

    @classmethod
    def load_surfs(cls):
        for frame_num in range(1, 7):
            cls.surfs += (Tile(frame_num, f'ghost {frame_num}', f'Frame {frame_num} of ghost'),)

    def update(self, game_mode):
        pass

    def update_surf(self):
        self.increment_frame_num()
        self.surf = self.surf_list[self.anim_num].surface

    def bfs(self, target):
        queue = deque([(self.nearest_node, [self.nearest_node])])
        # Every element is a tuple of the current node and the path that it took INCLUDING START
        while queue:
            current, path = queue.popleft()
            if current == target:
                return self.build_direc(path)
            for node in self.level.edges[current]:
                queue.append((node, path+[current]))
        return None

    def build_direc(self,node_path):
        direc_path=[]
        if len(node_path)==1:
            raise ValueError('Ghost is already on Pacman, but has not won yet. ')
        for idx, node in node_path:
            if idx==len(node_path)-1:
                break
            direc_path.append(node.direc_to(node_path[idx+1]))
