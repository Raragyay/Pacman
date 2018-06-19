# coding=utf-8
"""
Inky class
"""
from entities.ghosts import Ghost, Blinky
from entities import Pacman
from utility import PVector


class Inky(Ghost):
    """
    Inky class
    """

    def __init__(self, level, pacman: Pacman, blinky: Blinky):
        super().__init__(level, level.inky_start, pacman)
        self.convert_surfaces((128, 255, 255, 255))
        self.blinky = blinky

    def update_direc(self):
        """
        Special targeting that uses separate function
        :return:
        """
        self.direc = self.path_to(self.calc_target())
        # Ghost chases pacman current location
        # self.direc = self.closest_direction(self.pacman.nearest_node + self.pacman.direc * 4)
        # self.direc = PVector(0, 0)
        # self.path = self.bfs(self.pacman.nearest_node)

    def calc_target(self):
        """

        :return:
        """
        # Take pacman position, predict two tiles ahead
        pac_offset: PVector = self.pacman.nearest_node + self.pacman.direc * 2
        # Draw line from blinky to prediction
        dist_from_blinky = pac_offset - self.blinky.nearest_node
        # Double that line
        extended_loc = self.pacman.nearest_node + dist_from_blinky
        return extended_loc
