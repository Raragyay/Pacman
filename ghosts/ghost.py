# coding=utf-8
import os

import pygame

import constants
from PVector import PVector
from entity import Entity
from level import Level


class Ghost(Entity):
    surfs = ()  # The default frames are a class variable and are modified

    def __init__(self, loc: PVector, level: Level):
        super().__init__(loc, level)
        self.surf = []

    def convert_surfaces(self, target_clr):
        for surf in Ghost.surfs:
            convert_surf = surf.copy()


    @classmethod
    def load_surfs(cls):
        for frame_num in range(1, 7):
            surf = pygame.image.load(os.path.join(constants.sprite_folder, f'ghost {frame_num}.gif')).convert()
            cls.surfs += (surf,)
