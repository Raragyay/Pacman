# coding=utf-8
import os

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
        self.surf=None
        self.max_anim_num=5
        if not Ghost.surfs:
            Ghost.load_surfs()

    def convert_surfaces(self, target_clr):
        for surf in Ghost.surfs:
            new_surf = surf.copy()
            new_surf.load_surface(ghost_colour=target_clr,gif_location=constants.sprite_folder)
            self.surf_list.append(new_surf)

    @classmethod
    def load_surfs(cls):
        for frame_num in range(1, 7):
            cls.surfs += (Tile(frame_num, f'ghost {frame_num}', f'Frame {frame_num} of ghost'),)

    def update(self,game_mode):
        pass

    def update_surf(self):
        self.increment_frame_num()
        self.surf=self.surf_list[self.anim_num].surface