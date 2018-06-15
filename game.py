# coding=utf-8
import pygame

from PVector import PVector
from constants import GameMode, GHOST_EAT_SCORE, ALL_GHOSTS_ALL_TIMES
from ghosts.clyde import Clyde
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
        self.ate_all = 0

    def run(self):
        self.setup()
        while True:
            self.check_quit()
            if self.mode == GameMode.NORMAL:
                self.run_normal()
            elif self.mode == GameMode.WAIT_TO_START:
                self.run_wait_to_start()
            self.draw_level()
            self.draw_entities()
            self.draw_numbers()
            pygame.display.flip()
            self.clear()
            self.clock.tick(60)
            # print(self.clock.get_fps())

    def run_normal(self):
        self.update_entities()
        self.add_pacman_score()
        self.check_win()
        self.check_loss()  # TODO Maybe move this somewhere else

    def run_wait_to_start(self):
        self.draw_ready_sign()

    def reset(self):
        self.entities = []
        self.mode = GameMode.WAIT_TO_START
        self.level.load_map(self.level_num)
        self.screen = pygame.display.set_mode((self.level.width() * 16, self.level.height() * 16))
        self.reset_entities()
        self.ate_all = 0

    def reset_entities(self):
        self.entities = []
        self.add_entities()

    def add_entities(self):
        self.pacman = Pacman(self.level)
        self.entities.append(self.pacman)
        self.entities.append(Blinky(self.level, self.pacman))
        self.entities.append(Pinky(self.level, self.pacman))
        self.entities.append(Inky(self.level, self.pacman, self.entities[1]))
        self.entities.append(Clyde(self.level, self.pacman))
        # TODO make list of ghosts

    def setup(self):
        self.level.setup()
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

    def draw_ready_sign(self):
        self.screen.blit(self.level.get_ready_gif(),
                         self.level.get_ready_pos())

    def update_entities(self):
        for entity in self.entities:
            entity.update()

    def draw_entities(self):
        for entity in self.entities:
            if self.mode == GameMode.NORMAL or entity.surf == None:
                entity.update_surf()
            x, y = entity.top_left()
            self.screen.blit(entity.surf, (x, y))

    def draw_numbers(self):
        self.draw_lives()
        self.draw_score()

    def draw_lives(self):
        for i in range(self.lives):
            self.screen.blit(self.level.get_life_gif(), (24 + i * 10 + 16, self.level.height() * 16 - 12))

    def draw_score(self):
        for i, char in enumerate(str(self.score)):
            self.screen.blit(self.level.get_text_num(char), (24 + i * 9 + 16, self.level.height() * 16 - 24))

    def clear(self):
        self.screen.fill(self.level.bg_colour)

    def check_win(self):
        if self.level.won():
            # self.mode = GameMode.WAIT_AFTER_FINISH
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
            print(self.score)
            exit(0)
        for ghost in self.entities[1:]:
            if ghost.collided_with_pacman():
                if ghost.scared_timer and not ghost.dead():
                    self.add_ghost_hit_score()
                    ghost.die()
                elif not ghost.dead():
                    # self.mode = GameMode.GHOST_HIT  # I'm not sure if it's supposed to be used for this
                    self.die()

    def add_ghost_hit_score(self):
        self.pacman.increment_combo()
        self.score += GHOST_EAT_SCORE * self.pacman.combo
        if self.pacman.combo == len(self.entities) - 1:  # If he ate all 4 ghosts
            self.ate_all += 1
            if self.ate_all == self.level.big_dot_num:
                self.score += ALL_GHOSTS_ALL_TIMES

    def add_pacman_score(self):
        self.score += self.pacman.add_score()

    def no_lives(self):
        return self.lives <= 0

    def die(self):
        self.lives -= 1
        self.reset_entities()
        self.mode = GameMode.NORMAL


if __name__ == '__main__':
    game = Game()
    game.run()
