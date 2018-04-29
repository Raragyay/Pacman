# coding=utf-'8'

from enum import Enum, unique
"""NOT USED ANYMORE"""

@unique
class PointType(Enum):
    EMPTY = '000'
    DOOR = '001'
    PELLET = '002'
    POWERPELLET = '003'
    START = '004'

    DOORHORI = '020'
    DOORVERT = '021'
    SHOWLOGO = '022'
    HIGHSCORE = '023'

    WALL_STRAIGHT_H = '100'
    WAll_STRAIGHT_V = '101'

    WALL_CORNER_LL = '105'
    WALL_CORNER_LR = '106'
    WALL_CORNER_UL = '107'
    WALL_CORNER_UR = '108'

    WALL_END_B = '110'
    WALL_END_L = '111'
    WALL_END_R = '112'
    WALL_END_T = '113'

    WALL_NUB='120'

    WALL_T_BOT='130'
    WALL_T_LEFT='131'
    WALL_T_RIGHT = '132'
    WALL_T_TOP = '133'

    WALL_X='140'
