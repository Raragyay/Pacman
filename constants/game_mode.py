# coding=utf-8

from enum import Enum, unique


@unique
class GameMode(Enum):
    """
    Game modes.
    """

    NORMAL = 1
    GHOST_HIT = 2
    GAME_OVER = 3
    WAIT_TO_START = 4
    WAIT_AFTER_GHOST = 5
    WAIT_AFTER_FINISH = 6
