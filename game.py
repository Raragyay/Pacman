# coding=utf-8
import pygame

from constants import GameMode
from level import Level
from pacman import Pacman


class Game:
    def __init__(self):
        pygame.init()
        screen = pygame.display.set_mode((1, 1))
        self.level_num = 0
        self.score = 0
        self.lives = 3
        self.clock = pygame.time.Clock()
        self.entities = []
        self.mode = GameMode.NORMAL
        self.level = Level()

        self.level.load_map(0)

        self.screen = pygame.display.set_mode((self.level.width() * 16, self.level.height() * 16))

    def run(self):
        self.setup()
        while True:
            self.check_quit()
            self.update_entities()
            self.draw_entities()
            self.draw_level()
            pygame.display.flip()
            self.clear()
            self.clock.tick(60)

    def setup(self):
        self.entities.append(Pacman(self.level.start_location(), self.level))

    def draw_level(self):
        for row in range(self.level.height()):
            for col in range(self.level.width()):
                surf = self.level.get_tile(col, row)
                self.screen.blit(surf, (col * 16, row * 16))

    def check_quit(self):
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                exit()

    def update_entities(self):
        for entity in self.entities:
            entity.update(self.mode)

    def draw_entities(self):
        for entity in self.entities:
            x,y=entity.top_left()
            self.screen.blit(entity.surf,(x,y))

    def clear(self):
        self.screen.fill((0,0,0))


if __name__ == '__main__':
    game = Game()
    game.run()
