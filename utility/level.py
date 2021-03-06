# coding=utf-8
"""
Level class
"""
import logging
import os

import pygame

from utility import PVector, Tile, CrossRef
from constants import LEVEL_FOLDER, DEFAULT_FILL_COLOUR, \
    DEFAULT_EDGE_SHADOW_COLOUR, DEFAULT_PELLET_COLOUR, DEFAULT_EDGE_LIGHT_COLOUR, PELLET_VALS, DEFAULT_BG_COLOUR, \
    ACCESSIBLE_TILES, WALL_VAL, BIG_PELLET_VAL
from entities import GhostInit


class Level:
    """
    This class holds all the information for a single map level.
    """

    def __init__(self):
        self.level_width = 0
        self.level_height = 0

        # Colour values
        self.edge_light_colour = DEFAULT_EDGE_LIGHT_COLOUR  # Yellow
        self.edge_shadow_colour = DEFAULT_EDGE_SHADOW_COLOUR  # Orange
        self.fill_colour = DEFAULT_FILL_COLOUR  # Cyan
        self.pellet_colour = DEFAULT_PELLET_COLOUR  # White
        self.bg_colour = DEFAULT_BG_COLOUR

        self.tiles = {}
        self.tile_vals = {}
        self.edges = {}

        self.pellets = 0
        self.big_dot_num = 0
        self.fruit_id = None

        self.cross_ref = CrossRef()

        self.pacman_start = None
        self.blinky_start = GhostInit()
        self.pinky_start = GhostInit()
        self.clyde_start = GhostInit()
        self.inky_start = GhostInit()
        self.ghost_door = None
        self.ready_gif_top_left = None
        self.ghost_box = set()

    def setup(self) -> None:
        """
        Load text images, which don't need colours.
        :return: None
        """
        self.cross_ref.load_text_imgs()

    def set_tile(self, coords, val) -> None:
        """
        Add tile value and tile object to the respective dictionaries.
        :param coords: PVector
        :param val: Tile id
        :return: None
        """
        assert coords in self.tile_vals, f'The coordinates given of {coords} were not in the map.'
        self.tile_vals[coords] = val
        self.tiles[coords] = self.cross_ref.get_tile(val)

    def load_map(self, level_num):
        """
        Resets the level class and loads a new map
        :param level_num: The level number
        """
        self.reset()

        f = open(os.path.join(LEVEL_FOLDER, r'level_' + str(level_num) + '.txt'), 'r')
        logging.info('Level {} successfully opened'.format(level_num))  # log

        line_num = 0
        row_num = 0
        use_line = False
        is_reading_level_data = False

        for line in f:
            line_num += 1

            str_split_by_space = line.strip().split(' ')  # Read line and get identifier

            identifier = str_split_by_space[0]

            if not identifier or identifier == "'":
                logging.debug('Skipping empty line')
                use_line = False
            elif identifier == '#':
                logging.debug('This is a divider or attribute line.')
                use_line = False
                status = self.write_attr(str_split_by_space)  # Add attribute.
                if status == -1:  # Check for errors
                    logging.warning(
                        'Received unknown data at line {}: {}'.format(line_num, ' '.join(str_split_by_space)))
                elif status > 0:  # Check for level reading. Toggle and start reading if it tells object to.
                    is_reading_level_data = not is_reading_level_data
                    if status == 1:
                        row_num = 0
            elif not is_reading_level_data:
                logging.warning(
                    'Received unknown data at line {}: {}'.format(line_num, ' '.join(str_split_by_space)))
            else:  # This means that we are reading the level data.
                use_line = True

            if use_line:
                logging.debug('{} tiles in row {}'.format(len(str_split_by_space), row_num))

                assert len(str_split_by_space) == self.level_width, \
                    'width of row {} is different from width described in file, {}'.format(
                        len(str_split_by_space), self.level_width)
                # Make sure that the number of tiles in row is correct, to avoid empty spaces.

                for col in range(self.level_width):
                    self.init_tile(PVector(col, row_num), str_split_by_space[col])
                    # Create the tile vals. Tile objects will be added later

                row_num += 1

        self.cross_ref.load_cross_refs(self.edge_light_colour, self.fill_colour, self.edge_shadow_colour,
                                       self.pellet_colour)  # Now that we have the colours, we can create the tiles.
        self.attach_tiles()  # Add tile objects
        self.build_ghost_box()
        # Create ghost box for ghosts to check if they should exit the box,
        # since ghost door is technically a wall.
        f.close()  # Close file
        self.assert_start_positions()  # Make sure that all required positions are there.
        # print(len(self.edges[self.ghost_door]))

    def write_attr(self, information) -> int:
        """
        Writes an attribute of the map to the level.
        :param information: An array of strings, taken from the file.
        :return: None
        """
        attr = information[1]

        if attr == 'lvlwidth':  # Set the level width
            self.level_width = int(information[2])
        elif attr == 'lvlheight':  # Set the level height
            self.level_height = int(information[2])
        elif 'colour' in attr:  # Set one of the colour attributes
            red = int(information[2])
            green = int(information[3])
            blue = int(information[4])
            colour_tup = (red, green, blue, 255)

            if attr == 'edgecolour':
                self.edge_light_colour = colour_tup
                self.edge_shadow_colour = colour_tup
            elif attr == 'edgelightcolour':
                self.edge_light_colour = colour_tup
            elif attr == 'edgeshadowcolour':
                self.edge_shadow_colour = colour_tup
            elif attr == 'fillcolour':
                self.fill_colour = colour_tup
            elif attr == 'pelletcolour':
                self.pellet_colour = colour_tup
            elif attr == 'bgcolour':
                self.bg_colour = colour_tup
            else:
                return -1  # An error has occurred

        elif 'ghost' in attr:  # Add ghost corners for scatter mode
            corner_1 = PVector(int(information[2]), int(information[3]))
            corner_2 = PVector(int(information[4]), int(information[5]))
            if 'blinky' in attr:
                self.blinky_start.add_corners(corner_1, corner_2)
            if 'pinky' in attr:
                self.pinky_start.add_corners(corner_1, corner_2)
            if 'inky' in attr:
                self.inky_start.add_corners(corner_1, corner_2)
            if 'clyde' in attr:
                self.clyde_start.add_corners(corner_1, corner_2)
        elif attr == 'fruittype':  # Add fruit type for point values
            self.fruit_id = int(information[2])
        elif attr == 'startleveldata':
            logging.debug('Now reading level data.')
            return 1  # Toggles is_reading_level_data and sets row_num to 0.
        elif attr == 'endleveldata':
            logging.debug('Level data has been read.')
            return 2
        else:  # An error has occurred
            return -1
        return 0  # No problems

    def init_tile(self, node: PVector, tile_value: str) -> None:
        """
        Add the tile to tile values to later be added as an object
        :param node: PVector for location on map
        :param tile_value:
        :return: None
        """
        self.tile_vals[node] = int(tile_value)

    def attach_tiles(self) -> None:
        """
        Attaches all tile values to the correct tile objects. Handles special tile checking and teleport checking.
        :return:
        """
        for key, value in self.tile_vals.items():
            tile = self.cross_ref.get_tile(int(value)).copy()
            if self.accessible(value):
                self.build_edges(key)
                # Build edges if it is something that the ghosts or pacman will pass through
            if value == WALL_VAL:
                is_wall_around = self.get_wall_binary(key)  # Get surrounding wall binary
                tile = self.cross_ref.get_tile(is_wall_around)  # Get corresponding wall value.
            if tile.teleport():
                teleport_to_tile = self.calc_teleport(key)  # Calculate destination tile
                tile.teleport_to_tile = teleport_to_tile
                self.edges[key].add(teleport_to_tile)  # To make sure edges are consistent
            if tile.name == 'ghost-door':
                self.build_edges(key)
                self.ghost_door = key
            if tile.name == "start":
                self.pacman_start = key
                self.set_tile(key, 0)
                self.build_edges(key)
                continue
            if tile.name == 'ghost-blinky':
                self.blinky_start.add_start(key)
                self.set_tile(key, 0)
                self.build_edges(key)
                continue
            if tile.name == 'ghost-pinky':
                self.pinky_start.add_start(key)
                self.set_tile(key, 0)
                self.build_edges(key)
                continue
            if tile.name == 'ghost-inky':
                self.inky_start.add_start(key)
                self.set_tile(key, 0)
                self.build_edges(key)
                continue
            if tile.name == 'ghost-clyde':
                self.clyde_start.add_start(key)
                self.set_tile(key, 0)
                self.build_edges(key)
                continue
            if tile.id in PELLET_VALS:
                if tile.id == BIG_PELLET_VAL:
                    self.big_dot_num += 1
                self.pellets += 1
            if tile.name == 'ready':
                self.ready_gif_top_left: tuple = (key.x * 16 + 8 - 20, key.y * 16 + 8 - 5)
                # * 16 for pixel location
                # + 8 for center of node
                # - 20 for half of the gif width
                # - 5 for half of the gif height
                self.set_tile(key, 0)
                self.build_edges(key)
                continue

            self.tiles[key] = tile
        self.edges[self.ghost_door] -= {self.inky_start.get_start(), self.pinky_start.get_start(),
                                        self.clyde_start.get_start()}  # Make sure that ghost_door only has one exit.

    def build_edges(self, node: PVector) -> None:
        """
        Utility function to build edges
        :param node:
        :return:
        """
        edges = self.get_surrounding_accessibles(node)
        self.edges[node] = edges

    def build_ghost_box(self):
        """
        Create ghost box for ghost logic processing.
        :return:
        """
        self.ghost_box = {self.ghost_door, self.inky_start.get_start(), self.pinky_start.get_start(),
                          self.clyde_start.get_start()}

    def calc_teleport(self, node: PVector) -> PVector:
        """
        Calculate the destination teleport
        :param node: PVector
        :return: Destination
        """
        assert node.x == 0 or node.x == self.level_width - 1 or node.y == 0 or node.y == self.level_height - 1
        # Make sure it is on the edge of the map
        # Horizontal teleport
        if node.x == 0:
            return PVector(self.level_width - 1, node.y)
        if node.x == self.level_width - 1:
            return PVector(0, node.y)

        # Vertical Teleport
        if node.y == 0:
            return PVector(node.x, self.level_height - 1)
        if node.y == self.level_height - 1:
            return PVector(node.x, 0)

    def get_surrounding_accessibles(self, node: PVector) -> set:
        """
        Gets surrounding nodes that are safe
        :param node:
        :return: set of safe nodes to be added to edges dictionary
        """
        safe_nodes = set()
        # Left
        if self.is_safe(node + PVector(1, 0)):
            safe_nodes.add(node + PVector(1, 0))
        # Right
        if self.is_safe(node + PVector(-1, 0)):
            safe_nodes.add(node + PVector(-1, 0))
        # Down
        if self.is_safe(node + PVector(0, 1)):
            safe_nodes.add(node + PVector(0, 1))
        # Up
        if self.is_safe(node + PVector(0, -1)):
            safe_nodes.add(node + PVector(0, -1))
        return safe_nodes

    def get_wall_binary(self, node: PVector) -> str:
        """
        Get surrounding tiles and check if they are walls.
        :param node:
        :return:
        """
        surrounding = ''
        # Left
        if self.is_wall(node + PVector(-1, 0)):
            surrounding += '1'
        else:
            surrounding += '0'
        # Right
        if self.is_wall(node + PVector(1, 0)):
            surrounding += '1'
        else:
            surrounding += '0'
        # Up
        if self.is_wall(node + PVector(0, -1)):
            surrounding += '1'
        else:
            surrounding += '0'
        # Down
        if self.is_wall(node + PVector(0, 1)):
            surrounding += '1'
        else:
            surrounding += '0'
        return surrounding

    def is_safe(self, node: PVector) -> bool:
        """
        Utility function
        :param node:
        :return:
        """
        return not self.out_of_bounds(node) and self.accessible(self.tile_vals[node])

    def is_wall(self, node: PVector) -> bool:
        """
        Utility Function
        :param node:
        :return:
        """
        return not self.out_of_bounds(node) and self.tile_vals[node] == WALL_VAL

    def out_of_bounds(self, node: PVector) -> bool:
        """
        Utility Function
        :param node:
        :return:
        """
        return node.x < 0 or node.x > self.level_width - 1 or node.y < 0 or node.y > self.level_height - 1

    @staticmethod
    def accessible(val: int) -> bool:
        """
        Utility Function
        :param val:
        :return:
        """
        return val in ACCESSIBLE_TILES

    def won(self) -> bool:
        """
        Check if all pellets have been eaten
        :return:
        """
        for tile_val in self.tile_vals.values():
            if tile_val in PELLET_VALS:
                return False
        return True

    def assert_start_positions(self) -> None:
        """
        Make sure that all needed values are filled.
        :return:
        """
        assert self.ghost_door is not None, "No ghost door found."
        assert self.pacman_start is not None, "No start position for Pacman found."
        assert self.blinky_start.get_start() is not None, "No start position for Blinky found."
        assert self.pinky_start.get_start() is not None, "No start position for Pinky found."
        assert self.clyde_start.get_start() is not None, "No start position for Clyde found."
        assert self.inky_start.get_start() is not None, "No start position for Inky found."
        assert self.ready_gif_top_left is not None, "No position for ready gif found."
        assert self.ghost_box != set(), "Empty Ghost box"

    def get_tile_val(self, node: PVector) -> int:
        """

        :param node:
        :return:
        """
        return self.tile_vals[node]

    def get_tile_surf(self, node: PVector) -> pygame.Surface:
        """

        :param node:
        :return:
        """
        return self.tiles[node].get_surf()

    def get_tile(self, node: PVector) -> Tile:
        """

        :param node:
        :return:
        """
        return self.tiles[node]

    def width(self) -> int:
        """

        :return: width of level
        """
        return self.level_width

    def height(self) -> int:
        """

        :return: height of level
        """
        return self.level_height

    def start_location(self) -> PVector:
        """

        :return: starting location for pacman
        """
        return self.pacman_start

    def reset(self) -> None:
        """
        Reset level for new level loading
        :return:
        """
        self.tile_vals = {}  # Reset map
        self.tiles = {}
        self.edges = {}
        self.pellets = 0  # Reset Pellet Number
        self.big_dot_num = 0
        self.pacman_start = None
        self.blinky_start = GhostInit()
        self.pinky_start = GhostInit()
        self.clyde_start = GhostInit()
        self.inky_start = GhostInit()
        self.ghost_door = None
        self.ready_gif_top_left = None
        self.ghost_box = set()
        self.fruit_id = None
        self.edge_light_colour = DEFAULT_EDGE_LIGHT_COLOUR  # Yellow
        self.edge_shadow_colour = DEFAULT_EDGE_SHADOW_COLOUR  # Orange
        self.fill_colour = DEFAULT_FILL_COLOUR  # Cyan
        self.pellet_colour = DEFAULT_PELLET_COLOUR  # White
        self.bg_colour = DEFAULT_BG_COLOUR

    def get_surf(self, key) -> pygame.Surface:
        """

        :param key:
        :return:
        """
        return self.cross_ref.get_tile(key).get_surf()

    def get_life_gif(self) -> pygame.Surface:
        """

        :return:
        """
        return self.get_surf('life')

    def get_text_num(self, char: str) -> pygame.Surface:
        """

        :param char: A number to get surface for
        :return:
        """
        return self.get_surf(char)

    def get_ready_gif(self) -> pygame.Surface:
        """

        :return:
        """
        return self.get_surf('ready')

    def get_ready_pos(self) -> tuple:
        """

        :return:
        """
        return self.ready_gif_top_left

    def get_logo(self) -> pygame.Surface:
        """

        :return:
        """
        return self.get_surf('logo')


# Testing purposes
if __name__ == '__main__':
    level = Level()
    level.load_map(0)
