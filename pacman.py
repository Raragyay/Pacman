# coding=utf-8
from PVector import PVector
from constants import GameMode
from entity import Entity
import pygame


class Pacman(Entity):
    def __init__(self, loc):
        super().__init__(loc)

    def get_key_strokes(self, game_mode):
        if game_mode == GameMode.NORMAL:
            keys_pressed=pygame.key.get_pressed()
            if any(keys_pressed[key] for key in [pygame.K_d,pygame.K_RIGHT]):
                self.update_path(PVector(0, 1))
            if any(keys_pressed[key] for key in [pygame.K_a,pygame.K_LEFT]):
                self.update_path(PVector(0, 1))
            if any(keys_pressed[key] for key in [pygame.K_w,pygame.K_UP]):
                self.update_path(PVector(0, 1))
            if any(keys_pressed[key] for key in [pygame.K_d,pygame.K_RIGHT]):
                self.update_path(PVector(0, 1))


    def update_path(self, vec):
        self.path[1] = vec
