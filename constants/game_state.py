# coding=utf-8
"""
Game states. This is the first if statement check in the run function.
"""

from enum import Enum, unique


@unique
class GameState(Enum):
    """
    Game states. This differs from game mode in that it is higher level.
    """

    MAINGAME = 1
    HIGHSCORE = 2
    MAINMENU = 3
