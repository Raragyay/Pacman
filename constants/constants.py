# coding=utf-8
"""
Constant parameters for most game values. Provides a central place to modify values.
"""
import logging

# Logging formats
log_format = '%(levelname)s %(asctime)s %(message)s'
cur_log_level = logging.INFO

# Level loading parameters
NO_GIF_SURFACE = {23, 10, 11, 12, 13, 22}
PELLET_VALS = {2, 3}
BIG_PELLET_VAL = 3
TELEPORT_TILES = {20, 21}
ACCESSIBLE_TILES = {0, 2, 3, 4, 10, 11, 12, 13, 20, 21, 22}
WALL_VAL = 100
GHOST_DOOR = 1

# Ghost-related values and scoring
GHOST_EAT_SCORE = 200
ALL_GHOSTS_ALL_TIMES = 12000
WAIT_FOR_READY_TIMER = 120
GHOST_HIT_TIMER = 30
SCARED_TICKS = 300

# Colour modifications
default_edge_light_colour = (255, 206, 255, 255)
default_fill_colour = (132, 0, 132, 255)
default_edge_shadow_colour = (255, 0, 255, 255)
default_pellet_colour = (128, 0, 128, 255)
default_ghost_colour = (255, 0, 0, 255)
default_bg_colour = (0, 0, 0, 255)

# Corner-cutting
max_cut = 16

# Game running parameters
default_speed = 1
DEFAULT_LIVES = 1
STARTING_LEVEL = 1
