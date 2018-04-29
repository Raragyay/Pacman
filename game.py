# coding=utf-8
import pygame

from constants import GameMode
from crossref import CrossRef
from level import Level


class Game:
    def __init__(self):
        pygame.init()
        screen=pygame.display.set_mode((1,1)) #Todo: ADJUST
        self.level_num = 0
        self.score = 0
        self.lives = 3

        self.mode = GameMode.NORMAL
        self.cross_ref = CrossRef()
        self.level = Level()

        self.level.load_map(0)
        a, b, c, d = self.level.get_colour_vals()
        self.cross_ref.load_cross_refs(a, b, c, d)

        self.screen=pygame.display.set_mode((self.level.width()*16,self.level.height()*16))

    def draw(self):
        for row in range(self.level.height()):
            for col in range(self.level.width()):
                tile_val=self.level.get_tile(row,col)
                surf=self.cross_ref.get_tile(tile_val).get_surf()
                self.screen.blit(surf,(col*16,row*16))


if __name__ == '__main__':
    game = Game()
    while True:
        for event in pygame.event.get():
            if event.type==pygame.QUIT:
                pygame.quit()
                exit()
        game.draw()
        pygame.display.flip()
        pygame.time.Clock().tick(60)
