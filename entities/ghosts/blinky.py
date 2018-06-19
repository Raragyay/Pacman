# coding=utf-8
"""
Blinky Class
"""
from entities.ghosts import Ghost
from entities import Pacman


class Blinky(Ghost):
    """
    Blinky class
    """

    def __init__(self, level, pacman: Pacman):
        super().__init__(level, level.blinky_start, pacman)  # Init ghost class
        self.convert_surfaces((255, 0, 0, 255))  # Red ghost

    def update_direc(self) -> None:
        """
        Ghost chases pacman current location
        :return:
        """
        self.direc = self.path_to(self.pacman.nearest_node)
