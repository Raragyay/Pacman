# coding=utf-8
"""
Specific game modes. Used by Game class to determine what to draw and what to check for.
"""

from enum import Enum, unique


@unique
class GameMode(Enum):
    """
    Game modes.
    """

    NORMAL = 1
    WAIT_TO_START = 2
    WAIT_AFTER_GHOST_HIT = 3
    WAIT_AFTER_PACMAN_HIT = 4

    WAITING_FOR_NAME = 10
    SHOW_HIGHSCORE = 11
