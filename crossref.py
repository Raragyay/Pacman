# coding=utf-8
import logging
import os

from constants import file_paths, log_folder, log_format, cur_log_level
from tile import Tile


class CrossRef:
    def __init__(self):
        self.id_to_img = {}

    def load_cross_refs(self, edge_light_colour, fill_colour, edge_shadow_colour, pellet_colour):
        logging.basicConfig(filename=os.path.join(log_folder, 'cross_refs.log'),
                            filemode='w',
                            format=log_format,
                            level=cur_log_level)
        logging.info('Cross-references successfully opened')

        f = open(os.path.join(file_paths.base_folder, 'resources', 'crossref.txt'), 'r')

        for line in f.readlines():
            str_split_by_space = line.strip().split(' ')
            j = str_split_by_space[0]

            if not j or j == "'" or j == '#':
                use_line = False
                logging.debug("Skipping comment / whitespace line.")
            else:
                use_line = True

            if use_line:
                tile_id = int(str_split_by_space[0])
                logging.debug(tile_id)
                tile_name = str_split_by_space[1]
                tile_desc = ' '.join(str_split_by_space[2:])
                tile = Tile(tile_id, tile_name, tile_desc)
                tile.load_surface(edge_light_colour, fill_colour, edge_shadow_colour, pellet_colour)
                self.id_to_img[tile_id] = tile
        f.close()

    def get_tile(self, id):
        return self.id_to_img[id]