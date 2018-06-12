# coding=utf-8

# coding=utf-8
from PVector import PVector
from ghosts.ghost import Ghost
from level import Level
from pacman import Pacman


class Pinky(Ghost):
    def __init__(self, level: Level, pacman: Pacman):
        super().__init__(level.pinky_start, level, pacman)
        self.convert_surfaces((255, 128, 255, 255))
        self.direc = PVector(1, 0)

    def update_direc(self):
        if self.in_ghost_box():
            self.exit_box()
            return
        # Ghost chases pacman current location
        self.direc = self.closest_direction(self.pacman.nearest_node + self.pacman.direc * 4)
        # self.path = self.bfs(self.pacman.nearest_node)
