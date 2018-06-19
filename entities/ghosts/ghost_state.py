# coding=utf-8
"""
Readable states instead of numbers
"""
from enum import unique, Enum


@unique
class GhostState(Enum):
    """
    For Ghost update logic
    """
    CHASE = 0
    SCATTER = 1
    DEAD = 2
