# coding=utf-8
"""
Utility class to store initial values
"""
from utility.PVector import PVector


class GhostInit:
    """
    Small class to hold values
    """
    def __init__(self):
        self.start: PVector = None
        self.corner_1: PVector = PVector(2, 2)
        self.corner_2: PVector = PVector(2, 2)

    def add_start(self, node: PVector):
        """

        :param node:
        :return:
        """
        self.start = node

    def add_corners(self, corner_1, corner_2):
        """

        :param corner_1:
        :param corner_2:
        :return:
        """
        self.corner_1 = corner_1
        self.corner_2 = corner_2

    def get_start(self):
        """
        Utility
        :return:
        """
        return self.start
