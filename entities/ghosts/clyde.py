# coding=utf-8
"""
Clyde class
"""
from utility import PVector
from entities.ghosts import Ghost
from entities import Pacman


class Clyde(Ghost):
    """
    Clyde Ghost. The scaredy-cat
    """

    def __init__(self, level, pacman: Pacman):
        super().__init__(level, level.clyde_start, pacman)
        self.convert_surfaces((255, 128, 0, 255))  # Orange-ish

    def update_direc(self) -> None:
        """
        Chases pacman if far away but runs away to corner if too close.
        :return:
        """

        if abs(self.nearest_node - self.pacman.nearest_node) < PVector(8, 8):  # If Clyde is too close, he runs away
            self.scatter()
        else:
            self.direc = self.path_to(self.pacman.nearest_node)  # Otherwise he behaves like blinky
