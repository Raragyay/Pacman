# coding=utf-8
"""
Contains the tile class. This is, effectively, one picture. It also holds the teleportation tile if it is teleporting.
"""
import os

import pygame

from constants import DEFAULT_EDGE_LIGHT_COLOUR, DEFAULT_EDGE_SHADOW_COLOUR, DEFAULT_FILL_COLOUR, \
    DEFAULT_PELLET_COLOUR, DEFAULT_GHOST_COLOUR, TILE_FOLDER, NO_GIF_SURFACE, TELEPORT_TILES


class Tile:
    """
    Tile object to later blit onto screen.
    """

    def __init__(self, key, name, desc):
        """

        :param key: String or int, depending on whether or not it is text or a piece of the map
        :param name: Name for identifying in level logic
        :param desc: For debugging purposes
        """
        self.id = key  # Named key to prevent builtin shadowing
        self.name = name
        self.desc = desc
        self.surface = None
        self.is_teleport = False
        self.teleport_to_tile = None

    def load_surface(self, edge_light_colour=DEFAULT_EDGE_LIGHT_COLOUR, fill_colour=DEFAULT_FILL_COLOUR,
                     edge_shadow_colour=DEFAULT_EDGE_SHADOW_COLOUR,
                     pellet_colour=DEFAULT_PELLET_COLOUR, ghost_colour=DEFAULT_GHOST_COLOUR,
                     gif_location=TILE_FOLDER) -> None:
        """
        Loads a surface for tile, assuming that it should have one. Some tiles, such as blank tiles and default walls
        do not have surfaces.
        :param edge_light_colour: 4 element tuple
        :param fill_colour: 4 element tuple
        :param edge_shadow_colour: 4 element tuple
        :param pellet_colour: 4 element tuple
        :param ghost_colour: 4 element tuple
        :param gif_location: OS path, to load the gifs from.
        :return: None
        """
        # pygame.init()
        # pygame.display.set_mode((1,1))
        if self.id in NO_GIF_SURFACE:  # Create blank surface.
            self.surface = pygame.Surface((16, 16))
            return

        if self.id in TELEPORT_TILES:  # For Entity teleport check.
            self.is_teleport = True

        self.surface = pygame.image.load(
            os.path.join(gif_location, self.name + '.gif')).convert()  # load surface to convert

        surface_size = self.surface.get_size()  # For processing different size gifs for text gifs.

        for x in range(surface_size[0]):
            for y in range(surface_size[1]):
                # Colour conversion
                if self.surface.get_at((x, y)) == DEFAULT_EDGE_LIGHT_COLOUR:
                    self.surface.set_at((x, y), edge_light_colour)
                elif self.surface.get_at((x, y)) == DEFAULT_FILL_COLOUR:
                    self.surface.set_at((x, y), fill_colour)
                elif self.surface.get_at((x, y)) == DEFAULT_EDGE_SHADOW_COLOUR:
                    self.surface.set_at((x, y), edge_shadow_colour)
                elif self.surface.get_at((x, y)) == DEFAULT_PELLET_COLOUR:
                    self.surface.set_at((x, y), pellet_colour)
                elif self.surface.get_at((x, y)) == DEFAULT_GHOST_COLOUR:
                    self.surface.set_at((x, y), ghost_colour)

    def get_surf(self) -> pygame.Surface:
        """
        :return: Surface to display
        """
        return self.surface

    def copy(self) -> 'Tile':
        """
        Creates a copy of this tile. This is for teleport tile purposes, so that different tiles teleport to
        different spots.
        :return: A copy of this tile.
        """
        new_tile = Tile(self.id, self.name, self.desc)
        new_tile.surface = self.surface
        new_tile.teleport_to_tile = self.teleport_to_tile
        new_tile.is_teleport = self.is_teleport
        return new_tile

    def teleport(self) -> bool:
        """
        :return: If this tile should teleport an entity.
        """
        return self.is_teleport
