# coding=utf-8
from enum import unique, Enum


@unique
class GhostState(Enum):
    CHASE = 0
    SCATTER = 1
    DEAD = 2
