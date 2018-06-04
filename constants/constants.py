# coding=utf-8
import logging

from constants.point_type import PointType

log_format = '%(levelname)s %(asctime)s %(message)s'
cur_log_level = logging.DEBUG
NO_GIF_SURFACE = {23}
PELLET_VALS = {2, 3}
ACCESSIBLE_TILES = {0, 2, 3, 20, 21}
WALL_VAL = 100

default_edge_light_colour = (255, 206, 255, 255)
default_fill_colour = (132, 0, 132, 255)
default_edge_shadow_colour = (255, 0, 255, 255)
default_pellet_colour = (128, 0, 128, 255)
default_ghost_colour = (255, 0, 0, 255)
default_bg_colour = (0, 0, 0, 255)

default_speed = 1

min_wall_id = 100
max_wall_id = 199
