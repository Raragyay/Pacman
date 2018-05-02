# coding=utf-8
import random

from PVector import PVector
from constants import GameMode, default_speed, min_wall_id, max_wall_id
from entity import Entity
import pygame

from level import Level
from tile import Tile


class Pacman(Entity):
    def __init__(self, loc: PVector, level: Level):
        super().__init__(loc, level)
        directions=['u','d','l','r']

    def get_key_strokes(self, game_mode: GameMode) -> None:
        if game_mode == GameMode.NORMAL:
            keys_pressed = pygame.key.get_pressed()
            if any(keys_pressed[key] for key in [pygame.K_d, pygame.K_RIGHT]):
                self.update_path(PVector(0, default_speed))
            if any(keys_pressed[key] for key in [pygame.K_a, pygame.K_LEFT]):
                self.update_path(PVector(0, -default_speed))
            if any(keys_pressed[key] for key in [pygame.K_w, pygame.K_UP]):
                self.update_path(PVector(-default_speed, 0))
            if any(keys_pressed[key] for key in [pygame.K_d, pygame.K_RIGHT]):
                self.update_path(PVector(default_speed, 0))

    def update_path(self, vec: PVector) -> None:
        self.path[1] = vec

    def update_direc(self):
        self.path[0] = random.choice(self.find_valid_adj_nodes())

    def find_valid_adj_nodes(self):
        node_list = []
        # Try Right Side
        for node in self.get_adj_nodes():
            if not self.out_of_bounds(node) and not self.is_wall(self.level.get_tile_val(node)):
                node_list.append(node)
        return node_list

    def out_of_bounds(self, vec: PVector) -> bool:
        return vec.x < 0 or vec.x > self.level.height() - 1 or vec.y < 0 or vec.y > self.level.width() - 1

    def is_wall(self, tile: Tile):
        return min_wall_id <= tile.id < max_wall_id

    def get_adj_nodes(self):
        return [
            self.nearest_node + PVector(1, 0),
            self.nearest_node + PVector(0, 1),
            self.nearest_node + PVector(-1, 0),
            self.nearest_node + PVector(0, -1)]
