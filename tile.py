# coding=utf-8
import os

import pygame

import constants


class Tile:
    def __init__(self, id, name, desc):
        self.id = id
        self.name = name
        self.desc = desc
        # self.point_type = constants.PointType(id)
        self.surface = None

    def load_surface(self, edge_light_colour, fill_colour, edge_shadow_colour, pellet_colour):
        # pygame.init()
        # pygame.display.set_mode((1,1))
        if self.id in constants.NO_GIF_SURFACE:
            self.surface = pygame.Surface((16, 16))
            return

        self.surface = pygame.image.load(os.path.join(constants.tile_folder, self.name + '.gif')).convert()
        for y in range(16):
            for x in range(16):
                if self.surface.get_at((x, y)) == constants.default_edge_light_colour:
                    self.surface.set_at((x, y), edge_light_colour)
                elif self.surface.get_at((x, y)) == constants.default_fill_colour:
                    self.surface.set_at((x, y), fill_colour)
                elif self.surface.get_at((x, y)) == constants.default_edge_shadow_colour:
                    self.surface.set_at((x, y), edge_shadow_colour)
                elif self.surface.get_at((x, y)) == constants.default_pellet_colour:
                    self.surface.set_at((x, y), pellet_colour)

    def get_surf(self):
        return self.surface
