# coding=utf-8
"""
Contains CrossRef class to load all graphical components.
"""
import logging
import os

from constants import BASE_FOLDER, TEXT_FOLDER
from utility import Tile


class CrossRef:
    """
    This class takes care of all the graphical IO.
    """

    def __init__(self):
        """
        Initializes class variable id_to_img.
        This variable maps integers (for map tiles) and strings (for logos and numbers) to Tile objects, ]
        which have a surface, ID, name, and description. The tiles are then retrieved by the get_tile function
        to be displayed on the screen.
        """
        self.id_to_img = {}
        # self.wall_binary_to_img={}

    def load_cross_refs(self, edge_light_colour, fill_colour, edge_shadow_colour, pellet_colour) -> None:
        """
        Loads all tiles from crossref.txt in the resources folder. Each entry is loaded from the tiles folder,
        then colour conversions are applied.
        :param edge_light_colour: Colour to convert to for the 'light' side, usually the top of the wall
        :param fill_colour: The colour of the main part of the wall
        :param edge_shadow_colour: Colour for the 'dark' side of the wall.
        :param pellet_colour: Colour to change pellets to, if applicable.
        :return: None
        """
        logging.info('Cross-references successfully opened')

        f = open(os.path.join(BASE_FOLDER, 'resources', 'crossref.txt'), 'r')  # Open cross references

        for line in f.readlines():
            str_split_by_space = line.strip().split(' ')  # Split into a list
            j = str_split_by_space[0]  # Get the identifier to decide whether or not to use

            if not j or j == "'" or j == '#':
                use_line = False
                logging.debug("Skipping comment / whitespace line.")
            else:
                use_line = True

            if use_line:
                tile_id = int(str_split_by_space[0])
                if len(str_split_by_space[0]) == 4:
                    # If it is 4 length value, then it is a binary value for a wall.
                    # We don't want to touch that because int conversion will make some of them the same as tile values.
                    tile_id = str_split_by_space[0]

                # logging.debug(tile_id)
                tile_name = str_split_by_space[1]
                tile_desc = ' '.join(str_split_by_space[2:])
                tile = Tile(tile_id, tile_name, tile_desc)  # Create tile
                tile.load_surface(edge_light_colour, fill_colour, edge_shadow_colour, pellet_colour)  # Convert colours
                self.id_to_img[tile_id] = tile
        f.close()

    def get_tile(self, key) -> Tile:
        """
        :param key: ID that is in dictionary.
        :return: Tile with corresponding ID
        """
        return self.id_to_img[key]

    def load_text_imgs(self) -> None:
        """
        Loads text gifs from text folder.
        :return: None
        """
        for filename in os.listdir(TEXT_FOLDER):
            img_name = filename.split('.')[0]
            logging.debug(img_name)
            tile = Tile(None, img_name, filename)
            tile.load_surface(gif_location=TEXT_FOLDER)  # No colours specified means that no colours get changed.
            self.id_to_img[img_name] = tile
