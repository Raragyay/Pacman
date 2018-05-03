# coding=utf-8
import os
import random
from collections import deque

import constants
from PVector import PVector
from constants import GameMode, default_speed, min_wall_id, max_wall_id
from entity import Entity
import pygame

from level import Level
from tile import Tile


class Pacman(Entity):
    def __init__(self, loc: PVector, level: Level):
        super().__init__(loc, level)
        self.surf = pygame.image.load(os.path.join(constants.sprite_folder, 'pacman.gif')).convert()
        # directions=['u','d','l','r']

    def get_key_strokes(self, game_mode: GameMode) -> None:
        if game_mode == GameMode.NORMAL:  # TODO only randomize if it has no moves
            keys_pressed = pygame.key.get_pressed()
            if any(keys_pressed[key] for key in [pygame.K_d, pygame.K_RIGHT]):
                self.update_path(PVector(default_speed, 0))
            if any(keys_pressed[key] for key in [pygame.K_a, pygame.K_LEFT]):
                self.update_path(PVector(-default_speed, 0))
            if any(keys_pressed[key] for key in [pygame.K_w, pygame.K_UP]):
                self.update_path(PVector(0, -default_speed))
            if any(keys_pressed[key] for key in [pygame.K_d, pygame.K_DOWN]):
                self.update_path(PVector(0, default_speed))

    def update_path(self, vec: PVector) -> None:
        if len(self.path) == 0:
            self.path = [self.direc, vec]
        elif len(self.path) == 1:
            self.path.append(vec)
        else:
            self.path[1] = vec

    def update_direc(self):
        if self.is_safe(self.nearest_node + self.direc):
            self.path[0] = self.direc
            return
        self.path[0] = random.choice(self.find_valid_adj_nodes())

    def find_valid_adj_nodes(self):
        node_list = []
        # Try Right Side
        for node in self.get_adj_nodes():
            if self.is_safe(node):
                node_list.append(self.direc_to(node))
        return node_list

    def out_of_bounds(self, vec: PVector) -> bool:
        return vec.x < 0 or vec.x > self.level.width() - 1 or vec.y < 0 or vec.y > self.level.height() - 1

    def is_wall(self, tile: int):
        return min_wall_id <= tile < max_wall_id

    def get_adj_nodes(self):
        return [
            self.nearest_node + PVector(1, 0),
            self.nearest_node + PVector(0, 1),
            self.nearest_node + PVector(-1, 0),
            self.nearest_node + PVector(0, -1)]

    def is_safe(self, node: PVector) -> bool:
        return not self.out_of_bounds(node) and not self.is_wall(self.level.get_tile_val(node.x, node.y))

    def update(self, game_mode):
        self.get_key_strokes(game_mode)
        self.check_node()
        self.move()
