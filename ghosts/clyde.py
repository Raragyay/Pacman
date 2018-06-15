# coding=utf-8
from PVector import PVector
from ghosts.ghost import Ghost
from level import Level
from pacman import Pacman


class Clyde(Ghost):
    def __init__(self, level: Level, pacman: Pacman):
        super().__init__(level, level.clyde_start, pacman)
        self.convert_surfaces((255, 128, 0, 255))

    def update_direc(self):
        # Ghost chases pacman current location
        if abs(self.nearest_node - self.pacman.nearest_node) < PVector(8, 8):
            # self.reverse()
            self.scatter()
        else:
            self.direc = self.path_to(self.pacman.nearest_node + self.pacman.direc * 4)
        # self.path = self.bfs(self.pacman.nearest_node)
