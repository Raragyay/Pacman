# coding=utf-8

from PVector import PVector


class GhostInit:
    def __init__(self):
        self.start: PVector = None
        self.corner_1: PVector = None
        self.corner_2: PVector = None

    def add_start(self, node: PVector):
        self.start = node

    def add_corners(self, corner_1, corner_2):
        self.corner_1 = corner_1
        self.corner_2 = corner_2

    def get_start(self):
        return self.start
