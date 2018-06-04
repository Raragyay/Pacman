# coding=utf-8
import logging
import os

from PVector import PVector
from constants import level_location, log_folder, log_format, cur_log_level, default_fill_colour, \
    default_edge_shadow_colour, default_pellet_colour, default_edge_light_colour, PELLET_VALS, default_bg_colour, \
    ACCESSIBLE_TILES, WALL_VAL
from crossref import CrossRef
from fruit import Fruit


class Level:
    """
    Use dictionary to represent map.
    """

    def __init__(self):
        self.level_width = 0
        self.level_height = 0
        self.edge_light_colour = default_edge_light_colour  # Yellow
        self.edge_shadow_colour = default_edge_shadow_colour  # Orange
        self.fill_colour = default_fill_colour  # Cyan
        self.pellet_colour = default_pellet_colour  # White
        self.bg_colour = default_bg_colour

        self.tiles = {}
        self.tile_vals = {}
        self.edges = {}

        self.pellets = 0
        self.power_pellet_blink_timer = 0
        self.fruit = Fruit()

        self.cross_ref = CrossRef()

        self.pacman_start = None

    def setup(self):
        pass

    def set_tile(self, coords, val):
        assert coords in self.tile_vals, f'The coordinates given of {coords} were not in the map.'
        self.tile_vals[coords] = val
        self.tiles[coords] = self.cross_ref.get_tile(val)

    def load_map(self, level_num):
        """
        Resets the level class and loads a new map
        :param level_num: The level number
        #TODO modularify
        """
        self.tile_vals = {}  # Reset map
        self.pellets = 0  # Reset Pellet Number

        f = open(os.path.join(level_location, r'level_' + str(level_num) + '.txt'), 'r')
        logging.basicConfig(filename=os.path.join(log_folder, 'level_creation.log'),
                            filemode='w',
                            format=log_format,
                            level=cur_log_level)
        logging.info('Level {} successfully opened'.format(level_num))  # log

        line_num = -1
        row_num = 0
        use_line = False
        is_reading_level_data = False

        for line in f:
            line_num += 1

            str_split_by_space = line.strip().split(' ')

            identifier = str_split_by_space[0]

            if not identifier or identifier == "'":
                logging.debug('Skipping empty line')
                use_line = False
            elif identifier == '#':
                logging.debug('This is a divider or attribute line.')
                use_line = False
                status = self.write_attr(str_split_by_space)  # TODO Turn this into a function to process status
                if status == -1:
                    logging.warning(
                            'Received unknown data at line {}: {}'.format(line_num + 1, ' '.join(str_split_by_space)))
                elif status > 0:
                    is_reading_level_data = not is_reading_level_data
                    if status == 1:
                        row_num = 0
            elif not is_reading_level_data:
                logging.warning(
                        'Received unknown data at line {}: {}'.format(line_num + 1, ' '.join(str_split_by_space)))
            else:  # This means that we are reading the level data.
                use_line = True

            if use_line:
                logging.debug('{} tiles in row {}'.format(len(str_split_by_space), row_num))
                assert len(str_split_by_space) == self.level_width, \
                    'width of row {} is different from width described in file, {}'.format(
                            len(str_split_by_space), self.level_width)
                for col in range(self.level_width):
                    self.init_tile(PVector(col, row_num), str_split_by_space[col])
                row_num += 1
        self.cross_ref.load_cross_refs(self.edge_light_colour, self.fill_colour, self.edge_shadow_colour,
                                       self.pellet_colour)
        self.attach_tiles()
        f.close()

    def write_attr(self, information):
        """
        Writes an attribute of the map to the level.
        :param information: An array of strings, taken from the file.
        :return: void
        """
        attr = information[1]

        if attr == 'lvlwidth':  # Set the level width
            self.level_width = int(information[2])
        elif attr == 'lvlheight':
            self.level_height = int(information[2])
        elif 'colour' in attr:
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
        elif attr == 'fruittype':
            self.fruit.fruit_type = int(information[2])
        elif attr == 'startleveldata':
            logging.debug('Now reading level data.')
            return 1  # Toggles is_reading_level_data and sets row_num to 0.
        elif attr == 'endleveldata':
            logging.debug('Level data has been read.')
            return 2
        else:
            return -1
        return 0

    def get_colour_vals(self):
        return self.edge_light_colour, self.fill_colour, self.edge_shadow_colour, self.pellet_colour

    def init_tile(self, node: PVector, tile_value):
        self.tile_vals[node] = int(tile_value)

    def attach_tiles(self):
        for key, value in self.tile_vals.items():
            tile = self.cross_ref.get_tile(int(value))
            if self.accessible(value):  # Build edges if it is something that the ghosts or pacman will pass through
                edges = self.get_surrounding_accessibles(key)
                self.edges[key] = edges
            if value == WALL_VAL:
                is_wall_around = self.get_wall_binary(key)
                tile = self.cross_ref.get_tile(is_wall_around)
            if tile.name == "start":
                self.pacman_start = key  # TODO Set to empty after initialized pacman location
                self.set_tile(key, 0)
                continue
            self.tiles[key] = tile

    def get_surrounding_accessibles(self, node: PVector) -> set:
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
        return not self.out_of_bounds(node) and self.accessible(self.tile_vals[node])

    def is_wall(self, node: PVector):
        return not self.out_of_bounds(node) and self.tile_vals[node] == WALL_VAL

    def out_of_bounds(self, node: PVector) -> bool:
        return node.x < 0 or node.x > self.level_width - 1 or node.y < 0 or node.y > self.level_height - 1

    def accessible(self, val):
        return val in ACCESSIBLE_TILES

    def won(self):
        for tile_val in self.tile_vals.values():
            if tile_val in PELLET_VALS:
                return False
        return True

    def get_tile_val(self, node):
        return self.tile_vals[node]

    def get_tile(self, node):
        return self.tiles[node].get_surf()

    def width(self):
        return self.level_width

    def height(self):
        return self.level_height

    def start_location(self):
        return self.pacman_start


if __name__ == '__main__':
    level = Level()
    level.load_map(0)
