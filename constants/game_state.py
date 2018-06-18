# coding=utf-8

from enum import Enum, unique


@unique
class GameState(Enum):
    """
    Game modes.
    """

    MAINGAME = 1
    HIGHSCORE = 2
