# coding=utf-8

from enum import Enum, unique


@unique
class GameMode(Enum):
    """
    Game modes.
    """

    NORMAL = 1
    WAIT_TO_START = 2
