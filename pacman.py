# coding=utf-8
import os
import random

import pygame

import constants
from PVector import PVector
from constants import GameMode, default_speed, max_wall_id, min_wall_id, PELLET_VALS
from entity import Entity
from level import Level


class Pacman(Entity):
    def __init__(self, loc: PVector, level: Level):
        """
        The idea for the pacman object is that it will first check if it is on a turning point.

        If it is on a turning point, then it will check if it can go in the direction mentioned
        :param loc:
        :param level:
        """
        super().__init__(loc, level)
        self.surf = pygame.image.load(os.path.join(constants.sprite_folder, 'pacman.gif')).convert()
        self.up_surf = [self.surf]
        self.down_surf = [self.surf]
        self.left_surf = [self.surf]
        self.right_surf = [self.surf]
        for frame in range(1, 9):
            self.up_surf.append(
                    pygame.image.load(os.path.join(constants.sprite_folder, 'pacman-u {}.gif'.format(frame))).convert())
            self.down_surf.append(
                    pygame.image.load(os.path.join(constants.sprite_folder, 'pacman-d {}.gif'.format(frame))).convert())
            self.left_surf.append(
                    pygame.image.load(os.path.join(constants.sprite_folder, 'pacman-l {}.gif'.format(frame))).convert())
            self.right_surf.append(
                    pygame.image.load(os.path.join(constants.sprite_folder, 'pacman-r {}.gif'.format(frame))).convert())
        self.max_anim_num=8

    def get_key_strokes(self) -> None:
        keys_pressed = pygame.key.get_pressed()
        if any(keys_pressed[key] for key in [pygame.K_d, pygame.K_RIGHT]):
            self.update_path(PVector(default_speed, 0))
        if any(keys_pressed[key] for key in [pygame.K_a, pygame.K_LEFT]):
            self.update_path(PVector(-default_speed, 0))
        if any(keys_pressed[key] for key in [pygame.K_w, pygame.K_UP]):
            self.update_path(PVector(0, -default_speed))
        if any(keys_pressed[key] for key in [pygame.K_s, pygame.K_DOWN]):
            self.update_path(PVector(0, default_speed))

    def update_path(self, vec: PVector) -> None:
        if len(self.path) == 1:
            self.path.append(vec)
        else:
            self.path[1] = vec

    def update_direc(self):
        if self.level.is_safe(self.nearest_node + self.direc):
            self.path[0] = self.direc
            return
        self.path[0] = random.choice(self.find_valid_adj_nodes())

    def find_valid_adj_nodes(self):
        node_list = []
        # Try Right Side
        for node in self.get_adj_nodes():
            if self.level.is_safe(node):
                node_list.append(self.direc_to(node))
        return node_list

    def get_adj_nodes(self):
        return [
            self.nearest_node + PVector(1, 0),
            self.nearest_node + PVector(0, 1),
            self.nearest_node + PVector(-1, 0),
            self.nearest_node + PVector(0, -1)]

    def check_node(self):
        if self.is_on_node():
            self.consume_node()
            if len(self.path) > 1 and self.level.is_safe(self.nearest_node + self.path[1]):
                self.path = self.path[1:]
                self.set_direc()
            elif not self.level.is_safe(self.nearest_node + self.direc):
                self.direc = PVector(0, 0)

    def update(self, game_mode):
        if game_mode == GameMode.NORMAL:
            self.get_key_strokes()
            self.check_node()
            self.move()

    def consume_node(self):
        if self.level.get_tile_val(self.nearest_node) in PELLET_VALS:
            self.level.set_tile(self.nearest_node, 0)

    def update_surf(self):
        self.increment_frame_num()
        if self.direc == PVector(self.speed, 0):
            self.surf = self.right_surf[self.anim_num]
            return
        if self.direc == PVector(-self.speed, 0):
            self.surf = self.left_surf[self.anim_num]
            return
        if self.direc == PVector(0, self.speed):
            self.surf = self.down_surf[self.anim_num]
            return
        if self.direc == PVector(0, -self.speed):
            self.surf = self.up_surf[self.anim_num]
            return
