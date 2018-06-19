# coding=utf-8
"""
Pacman class. Represents the player.
"""
import os

import pygame

import constants
from utility import PVector
from constants import DEFAULT_SPEED, PELLET_VALS, MAX_CUT, BIG_PELLET_VAL
from entities import Entity


class Pacman(Entity):
    """
    Pacman class
    """

    def __init__(self, level):
        """
        :param level:
        """
        super().__init__(level.start_location(), level)

        self.surf = pygame.image.load(os.path.join(constants.SPRITE_FOLDER, 'pacman.gif')).convert()
        self.up_surf = [self.surf]
        self.down_surf = [self.surf]
        self.left_surf = [self.surf]
        self.right_surf = [self.surf]

        # Load surfaces
        for frame in range(1, 9):
            self.up_surf.append(
                pygame.image.load(os.path.join(constants.SPRITE_FOLDER, 'pacman-u {}.gif'.format(frame))).convert())
            self.down_surf.append(
                pygame.image.load(os.path.join(constants.SPRITE_FOLDER, 'pacman-d {}.gif'.format(frame))).convert())
            self.left_surf.append(
                pygame.image.load(os.path.join(constants.SPRITE_FOLDER, 'pacman-l {}.gif'.format(frame))).convert())
            self.right_surf.append(
                pygame.image.load(os.path.join(constants.SPRITE_FOLDER, 'pacman-r {}.gif'.format(frame))).convert())
        self.max_anim_num = 8  # Set max animation number

        # For corner cutting
        self.diagonal_move = self.direc

        self.cut_corner = False
        self.ghost_reverse = False

        self.dot_eat_timer = 0
        self.ate_big_dot = False
        self.ate_small_dot = False

        # For eating ghost score
        self.combo = 0

        # self.direc = PVector(-1, 0)

    def update(self):
        """
        Method that is called by game to update pacman
        :return:
        """
        self.reset_dots()
        self.get_key_strokes()
        self.move()
        self.consume_node()
        self.check_node()

    def get_key_strokes(self) -> None:
        """
        Get pressed keys and try to turn in each of the directions.
        Only one key is processed at one time to prevent phasing through walls.
        :return:
        """
        keys_pressed = pygame.key.get_pressed()
        if any(keys_pressed[key] for key in [pygame.K_d, pygame.K_RIGHT]):  # Right
            self.try_to_turn(PVector(DEFAULT_SPEED, 0))
            return
        if any(keys_pressed[key] for key in [pygame.K_a, pygame.K_LEFT]):  # Left
            self.try_to_turn(PVector(-DEFAULT_SPEED, 0))
            return
        if any(keys_pressed[key] for key in [pygame.K_w, pygame.K_UP]):  # Up
            self.try_to_turn(PVector(0, -DEFAULT_SPEED))
            return
        if any(keys_pressed[key] for key in [pygame.K_s, pygame.K_DOWN]):  # Down
            self.try_to_turn(PVector(0, DEFAULT_SPEED))
            return

    def try_to_turn(self, direc: PVector) -> None:  # BUG TESTED
        """
        Turns orthogonally if we're directly on the node
        Tries to cut the corner if possible
        :param direc:
        :return:
        """
        if self.level.is_safe(self.nearest_node + direc) and self.is_on_grid_line():
            if self.is_on_node():
                self.direc = direc  # Right angle turn
            elif self.is_turning(direc):
                if abs(self.pos % 16) < PVector(MAX_CUT, MAX_CUT):  # If we can cut

                    self.diagonal_move = self.direc + direc  # Move in both directions at once
                    self.cut_corner = True
                    self.direc = direc

    def is_on_grid_line(self):
        """
        Check that we are aligned with the vertical or horizontal grid to determine when to snap back to self.direc
        :return:
        """
        # vertical line check
        if (self.pos.y - 8) % 16 == 0:
            return True
        # horizontal line check
        if (self.pos.x - 8) % 16 == 0:
            return True
        return False

    def is_turning(self, direc):
        """
        Utility
        :param direc:
        :return:
        """
        return abs(direc) != abs(self.direc)

    def check_node(self):
        """
        Makes sure that we don't crash into a wall.
        :return:
        """
        if self.is_on_node():
            self.check_teleport()
            if not self.level.is_safe(self.nearest_node + self.direc):  # If it isn't safe anymore
                self.direc = PVector(0, 0)

    def consume_node(self):
        """
        Try to consume the node and if we do, add score and notify ghosts
        :return:
        """
        if self.level.get_tile_val(self.nearest_node) in PELLET_VALS:
            if self.level.get_tile_val(self.nearest_node) == BIG_PELLET_VAL:  # Big dot
                self.ate_big_dot = True
                self.combo = 0
                self.dot_eat_timer = 2
            else:  # Small dot
                self.dot_eat_timer = 1
                self.ate_small_dot = True

            self.level.set_tile(self.nearest_node, 0)  # Empty the tile

    def update_surf(self):
        """
        Update surfs based on Pacman's direction
        :return:
        """
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
        """
        Move pacman according to his state
        :return:
        """
        if self.dot_eat_timer != 0:  # Pause if we just ate a dot
            self.dot_eat_timer -= 1
            # print("ate dot")
        elif self.cut_corner:  # forcibly cut corner if we just gave the order
            # print(self.diagonal_move)
            self.cut_corner = False
            self.pos += self.diagonal_move
        elif self.is_on_grid_line():  # Otherwise just move normally
            self.pos += self.direc
        else:  # If we're not on grid line then move diagonally
            self.pos += self.diagonal_move

        self.nearest_node = self.pixel_to_node()  # Update nearest node

    def reset_dots(self):
        """

        :return:
        """
        if self.ate_big_dot:
            self.ate_big_dot = False
            # print('undid big dot eat')
        if self.ate_small_dot:
            self.ate_small_dot = False

    def increment_combo(self):
        """

        :return:
        """
        self.combo += 1

    def add_score(self):
        """

        :return:
        """
        score = 0
        if self.ate_big_dot:
            score += 50
        if self.ate_small_dot:
            score += 10
        return score
