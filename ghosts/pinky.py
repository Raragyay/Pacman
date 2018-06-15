# coding=utf-8
from PVector import PVector
from ghosts.ghost import Ghost
from level import Level
from pacman import Pacman


class Pinky(Ghost):
    def __init__(self, level: Level, pacman: Pacman):
        super().__init__(level, level.pinky_start, pacman)
        self.convert_surfaces((255, 128, 255, 255))

    def update_direc(self):
        # Ghost chases pacman current location
        self.direc = self.path_to(self.pacman.nearest_node + self.pacman.direc * 4)
        # self.path = self.bfs(self.pacman.nearest_node)
