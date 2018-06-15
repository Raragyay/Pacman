# coding=utf-8

# coding=utf-8
from PVector import PVector
from ghosts.blinky import Blinky
from ghosts.ghost import Ghost
from level import Level
from pacman import Pacman


class Inky(Ghost):
    def __init__(self, level: Level, pacman: Pacman, blinky: Blinky):
        super().__init__(level, level.inky_start, pacman)
        self.convert_surfaces((128, 255, 255, 255))
        self.blinky = blinky

    def update_direc(self):
        self.direc = self.path_to(self.calc_target())
        # Ghost chases pacman current location
        # self.direc = self.closest_direction(self.pacman.nearest_node + self.pacman.direc * 4)
        # self.direc = PVector(0, 0)
        # self.path = self.bfs(self.pacman.nearest_node)

    def calc_target(self):
        pac_offset: PVector = self.pacman.nearest_node + self.pacman.direc * 2
        dist_from_blinky = pac_offset - self.blinky.nearest_node
        extended_loc = self.pacman.nearest_node + dist_from_blinky
        return extended_loc
