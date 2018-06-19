# coding=utf-8
"""
Folder paths. Used mostly by CrossRef and Tile classes to load files.
"""
import os

BASE_FOLDER = os.path.join(os.path.dirname(__file__), r'..')

RESOURCE_FOLDER = os.path.join(BASE_FOLDER, 'resources')

LEVEL_FOLDER = os.path.join(RESOURCE_FOLDER, 'levels')
TILE_FOLDER = os.path.join(RESOURCE_FOLDER, 'tiles')
SPRITE_FOLDER = os.path.join(RESOURCE_FOLDER, 'sprites')
TEXT_FOLDER = os.path.join(RESOURCE_FOLDER, 'text')
FONT_FOLDER = os.path.join(RESOURCE_FOLDER, 'font')
LOG_FOLDER = os.path.join(RESOURCE_FOLDER, 'logs')

# Preliminary testing purposes.
if __name__ == '__main__':
    print(LEVEL_FOLDER)
    with open(os.path.join(LEVEL_FOLDER, r'level_0.txt'), 'r') as f:
        for line in f:
            print(line)
