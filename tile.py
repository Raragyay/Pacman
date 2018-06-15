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
        self.is_teleport = False
        self.teleport_to_tile = None

    def load_surface(self, edge_light_colour=(0, 0, 0, 0), fill_colour=(0, 0, 0, 0), edge_shadow_colour=(0, 0, 0, 0),
                     pellet_colour=(0, 0, 0, 0), ghost_colour=(0, 0, 0, 0), gif_location=constants.tile_folder):
        # pygame.init()
        # pygame.display.set_mode((1,1))
        if self.id in constants.NO_GIF_SURFACE:
            self.surface = pygame.Surface((16, 16))
            return

        if self.id in constants.TELEPORT_TILES:
            self.is_teleport = True

        self.surface = pygame.image.load(
                os.path.join(gif_location, self.name + '.gif')).convert()  # change default file location
        surface_size = self.surface.get_size()
        for x in range(surface_size[0]):
            for y in range(surface_size[1]):
                if self.surface.get_at((x, y)) == constants.default_edge_light_colour:
                    self.surface.set_at((x, y), edge_light_colour)
                elif self.surface.get_at((x, y)) == constants.default_fill_colour:
                    self.surface.set_at((x, y), fill_colour)
                elif self.surface.get_at((x, y)) == constants.default_edge_shadow_colour:
                    self.surface.set_at((x, y), edge_shadow_colour)
                elif self.surface.get_at((x, y)) == constants.default_pellet_colour:
                    self.surface.set_at((x, y), pellet_colour)
                elif self.surface.get_at((x, y)) == constants.default_ghost_colour:
                    self.surface.set_at((x, y), ghost_colour)

    def get_surf(self):
        return self.surface

    def copy(self):
        new_tile = Tile(self.id, self.name, self.desc)
        new_tile.surface = self.surface
        new_tile.teleport_to_tile = self.teleport_to_tile
        new_tile.is_teleport = self.is_teleport
        return new_tile

    def teleport(self):
        return self.is_teleport
