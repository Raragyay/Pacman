# coding=utf-8
"""
Folder paths. Used mostly by CrossRef and Tile classes to load files.
"""
import os
import sys

base_folder = os.path.join(os.path.dirname(__file__), r'..')

resource_folder = os.path.join(base_folder, 'resources')
log_folder = os.path.join(base_folder, 'logs')

level_location = os.path.join(resource_folder, 'levels')
tile_folder = os.path.join(resource_folder, 'tiles')
sprite_folder = os.path.join(resource_folder, 'sprites')
text_folder = os.path.join(resource_folder, 'text')
font_folder = os.path.join(resource_folder, 'font')

# Preliminary testing purposes.
if __name__ == '__main__':
    print(level_location)
    with open(os.path.join(level_location, r'level_0.txt'), 'r') as f:
        for line in f:
            print(line)
