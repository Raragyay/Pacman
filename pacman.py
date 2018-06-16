# coding=utf-8
import os
import random
from math import ceil

import pygame

import constants
from PVector import PVector
from constants import GameMode, default_speed, PELLET_VALS, max_cut, BIG_PELLET_VAL
from entity import Entity
from level import Level


class Pacman(Entity):
    def __init__(self, level: Level):
        """
        The idea for the pacman object is that it will first check if it is on a turning point.

        If it is on a turning point, then it will check if it can go in the direction mentioned
        :param level:
        """
        super().__init__(level.start_location(), level)
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
        self.max_anim_num = 8

        self.diagonal_move = self.direc
        self.cut_corner = False
        self.ghost_reverse = False
        self.dot_eat_timer = 0
        self.ate_big_dot = False
        self.ate_small_dot = False
        self.combo = 0

        # self.direc = PVector(-1, 0)

    def get_key_strokes(self) -> None:
        # for event in pygame.event.get():
        #     if event.type==pygame.KEYDOWN:
        #         if event.key in [pygame.K_d, pygame.K_RIGHT]:
        #             self.try_to_turn(PVector(default_speed, 0))
        #         if event.key in  [pygame.K_a, pygame.K_LEFT]:
        #             self.try_to_turn(PVector(-default_speed, 0))
        #         if event.key in  [pygame.K_w, pygame.K_UP]:
        #             self.try_to_turn(PVector(0, -default_speed))
        #         if event.key in  [pygame.K_s, pygame.K_DOWN]:
        #             self.try_to_turn(PVector(0, default_speed))
        keys_pressed = pygame.key.get_pressed()
        if any(keys_pressed[key] for key in [pygame.K_d, pygame.K_RIGHT]):
            self.try_to_turn(PVector(default_speed, 0))
            return
        if any(keys_pressed[key] for key in [pygame.K_a, pygame.K_LEFT]):
            self.try_to_turn(PVector(-default_speed, 0))
            return
        if any(keys_pressed[key] for key in [pygame.K_w, pygame.K_UP]):
            self.try_to_turn(PVector(0, -default_speed))
            return
        if any(keys_pressed[key] for key in [pygame.K_s, pygame.K_DOWN]):
            self.try_to_turn(PVector(0, default_speed))
            return

    def update_path(self, vec: PVector) -> None:  # OUTDATED
        if len(self.path) == 1:
            self.path.append(vec)
        else:
            self.path[1] = vec

    def try_to_turn(self, direc: PVector) -> None:  # BUG TESTED
        if self.level.is_safe(self.nearest_node + direc) and self.is_on_grid_line():
            if self.is_on_node():
                self.direc = direc
            elif self.is_turning(direc):
                self.consume_node()
                if abs(self.pos % 16) < PVector(max_cut,
                                                max_cut):  # If we can cut
                    # New direc will be based on the objective direction
                    dist_from_center = self.pos.dist_from(self.node_to_pixel(self.nearest_node))
                    # pixels_in_new_direc=direc*dist_from_center
                    pixel_dist = self.node_to_pixel(self.nearest_node) - self.pos

                    self.diagonal_move = pixel_dist / dist_from_center + direc
                    self.cut_corner = True
                    self.direc = direc
            else:
                self.direc = direc

    def is_on_grid_line(self):
        # vertical line check
        if (self.pos.y - 8) % 16 == 0:
            return True
        # horizontal line check
        if (self.pos.x - 8) % 16 == 0:
            return True
        return False

    def is_turning(self, direc):
        return abs(direc) != abs(self.direc)

    def is_diagonal_move(self):
        return self.direc != PVector(0, 0)

    def update_direc(self):  # OUTDATED
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

    def check_node(self):
        if self.is_on_node():
            self.check_teleport()
            if not self.level.is_safe(self.nearest_node + self.direc):
                self.direc = PVector(0, 0)

    def update(self):
        self.reset_dots()
        self.get_key_strokes()
        self.move()
        self.consume_node()
        self.check_node()

    def consume_node(self):
        if self.level.get_tile_val(self.nearest_node) in PELLET_VALS:
            if self.level.get_tile_val(self.nearest_node) == BIG_PELLET_VAL:  # Big dot
                self.ate_big_dot = True
                self.combo = 0
                self.dot_eat_timer = 2
            else:  # Small dot
                self.dot_eat_timer = 1
                self.ate_small_dot = True

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

    def move(self):
        if self.dot_eat_timer != 0:
            self.dot_eat_timer -= 1
            # print("ate dot")
        elif self.cut_corner:
            # print(self.diagonal_move)
            self.cut_corner = False
            self.pos += self.diagonal_move
        elif self.is_on_grid_line():
            self.pos += self.direc
        else:
            self.pos += self.diagonal_move

        self.nearest_node = self.pixel_to_node()

    def reset_dots(self):
        if self.ate_big_dot:
            self.ate_big_dot = False
            # print('undid big dot eat')
        if self.ate_small_dot:
            self.ate_small_dot = False

    def increment_combo(self):
        self.combo += 1

    def add_score(self):
        score = 0
        if self.ate_big_dot:
            score += 50
        if self.ate_small_dot:
            score += 10
        return score
