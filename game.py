# coding=utf-8
import pygame

from PVector import PVector
from constants import GameMode
from ghosts.ghost import Ghost
from ghosts.inky import Inky
from ghosts.pinky import Pinky
from ghosts.blinky import Blinky
from level import Level
from pacman import Pacman


class Game:
    def __init__(self):
        pygame.init()
        _ = pygame.display.set_mode((1, 1))
        self.level_num = 1
        self.score = 0
        self.clock = pygame.time.Clock()
        self.entities = []
        self.mode = GameMode.NORMAL
        self.level = Level()
        self.lives = 3

    def run(self):
        self.setup()
        while True:
            self.check_quit()
            if self.mode == GameMode.NORMAL:
                self.run_normal()
            self.draw_entities()
            self.draw_level()
            pygame.display.flip()
            self.clear()
            self.clock.tick(60)

    def run_normal(self):
        self.update_entities()
        self.check_win()
        self.check_loss()  # TODO Maybe move this somewhere else

    def reset(self):
        self.entities = []
        self.mode = GameMode.NORMAL
        self.level.load_map(self.level_num)
        self.screen = pygame.display.set_mode((self.level.width() * 16, self.level.height() * 16))
        self.reset_entities()

    def reset_entities(self):
        self.entities = []
        self.add_entities()

    def add_entities(self):
        self.entities.append(Pacman(self.level.start_location(), self.level))
        self.entities.append(Blinky(self.level, self.entities[0]))
        self.entities.append(Pinky(self.level, self.entities[0]))
        self.entities.append(Inky(self.level, self.entities[0], self.entities[1]))
        # TODO make list of ghosts

    def setup(self):
        Ghost.load_surfs()
        self.reset()

    def draw_level(self):
        for row in range(self.level.height()):
            for col in range(self.level.width()):
                surf = self.level.get_tile_surf(PVector(col, row))
                self.screen.blit(surf, (col * 16, row * 16))

    def check_quit(self):
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                exit()
            # To force win
            # if event.type=pygame.

    def update_entities(self):
        for entity in self.entities:
            entity.update(self.mode)

    def draw_entities(self):
        for entity in self.entities:
            if self.mode == GameMode.NORMAL or entity.surf == None:
                entity.update_surf()
            x, y = entity.top_left()
            self.screen.blit(entity.surf, (x, y))

    def clear(self):
        self.screen.fill(self.level.bg_colour)

    def check_win(self):
        if self.level.won():
            self.mode = GameMode.WAIT_AFTER_FINISH
            # transition time
            self.mode = GameMode.NORMAL
            self.level_num += 1
            try:
                self.reset()
            except FileNotFoundError:
                print("This is the end of the demo. Thanks for playing!")
                exit(0)

    def check_loss(self):
        if self.no_lives():
            print("This is the end of the demo. Thanks for playing!")
            exit(0)
        for ghost in self.entities[1:]:
            if ghost.collided_with_pacman():
                self.mode = GameMode.GHOST_HIT
                self.die()

    def no_lives(self):
        return self.lives <= 0

    def die(self):
        self.lives -= 1
        self.reset_entities()
        self.mode = GameMode.NORMAL


if __name__ == '__main__':
    game = Game()
    game.run()
