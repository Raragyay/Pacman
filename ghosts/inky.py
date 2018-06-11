# coding=utf-8

# coding=utf-8
from PVector import PVector
from ghosts.ghost import Ghost
from level import Level
from pacman import Pacman


class Inky(Ghost):
    def __init__(self, level: Level, pacman: Pacman):
        super().__init__(level.inky_start, level, pacman)
        self.convert_surfaces((128, 255, 255, 255))

    def update_direc(self):
        if self.in_ghost_box():
            self.direc = self.closest_direction(self.level.ghost_door)
            return
        # Ghost chases pacman current location
        # self.direc = self.closest_direction(self.pacman.nearest_node + self.pacman.direc * 4)
        self.direc = PVector(0, 0)
        # self.path = self.bfs(self.pacman.nearest_node)
