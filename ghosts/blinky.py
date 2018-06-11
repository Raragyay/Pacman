# coding=utf-8
from ghosts.ghost import Ghost
from level import Level
from pacman import Pacman


class Blinky(Ghost):
    def __init__(self, level: Level, pacman: Pacman):
        super().__init__(level.blinky_start, level, pacman)
        self.convert_surfaces((255, 0, 0, 255))

    def update_direc(self):
        # Ghost chases pacman current location
        self.direc = self.closest_direction(self.pacman.nearest_node)
        # self.path = self.bfs(self.pacman.nearest_node)
