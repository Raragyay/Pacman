# coding=utf-8
"""
Pinky class
"""
from entities.ghosts import Ghost
from entities import Pacman


class Pinky(Ghost):
    """
    Pinky tries to predict Pacman position
    """

    def __init__(self, level, pacman: Pacman):
        super().__init__(level, level.pinky_start, pacman)
        self.convert_surfaces((255, 128, 255, 255))

    def update_direc(self):
        """
        Predicts 4 tiles ahead
        :return:
        """
        self.direc = self.path_to(self.pacman.nearest_node + self.pacman.direc * 4)
