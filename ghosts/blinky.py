# coding=utf-8
from PVector import PVector
from ghosts.ghost import Ghost
from level import Level


class Blinky(Ghost):
    def __init__(self,loc:PVector,level:Level):
        super().__init__(loc,level)
        self.surf=
