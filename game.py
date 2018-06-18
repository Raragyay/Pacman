# coding=utf-8
import os
import pickle
import sys
from typing import List

import pygame

from PVector import PVector
from constants import ALL_GHOSTS_ALL_TIMES, GHOST_EAT_SCORE, GameMode, font_folder, resource_folder
from constants.constants import GHOST_HIT_TIMER, WAIT_FOR_READY_TIMER
from constants.game_state import GameState
from ghosts.blinky import Blinky
from ghosts.clyde import Clyde
from ghosts.ghost import Ghost
from ghosts.inky import Inky
from ghosts.pinky import Pinky
from level import Level
from pacman import Pacman
from text_input import TextInput


class Game:
    def __init__(self):
        pygame.init()
        _ = pygame.display.set_mode((1, 1))
        self.level_num = 1
        self.score = 0
        self.clock = pygame.time.Clock()
        self.entities = []
        self.game_state = GameState.MAINGAME
        self.mode = GameMode.NORMAL
        self.level = Level()
        self.lives = 1
        self.ate_all = 0
        self.timer = 0
        self.score_list = None
        self.text_box: TextInput = None
        self.font = None
        self.events = None

    def setup(self):
        self.level.setup()
        Ghost.load_surfs()
        self.font = pygame.font.Font(os.path.join(font_folder, 'visitor1.ttf'), 24)
        self.score_list = self.load_highscores()
        self.text_box = TextInput(initial_string='CHOW', font_family=os.path.join(font_folder, 'visitor1.ttf'),
                                  font_size=24, text_color=(255, 255, 255), cursor_color=(100, 100, 100), max_length=10)
        self.reset()

    def run(self):
        self.setup()
        while True:
            self.get_events()
            self.check_quit()
            if self.game_state == GameState.MAINGAME:
                self.run_main_game()
            elif self.game_state == GameState.HIGHSCORE:
                self.run_highscore()
            pygame.display.flip()
            self.clear()
            self.clock.tick(60)
            # print(self.clock.get_fps())

    def run_main_game(self):
        if self.mode == GameMode.NORMAL:
            self.run_normal()
        elif self.mode == GameMode.WAIT_TO_START:
            self.run_wait_to_start()
        elif self.mode == GameMode.WAIT_AFTER_GHOST_HIT:
            self.run_wait_after_ghost_hit()
        self.draw_level()
        self.draw_entities()
        self.draw_numbers()

    def run_highscore(self):
        if self.mode == GameMode.WAITING_FOR_NAME:
            self.update_highscores()
            self.draw_textbox()
            self.draw_query()
        elif self.mode == GameMode.SHOW_HIGHSCORE:
            self.draw_highscores(self.score_list)
            if self.check_try_again():
                pass
            self.draw_quit_hint()
            self.check_q_quit()

    def run_normal(self):
        self.update_entities()
        self.add_pacman_score()
        self.check_win()
        self.check_loss()  # TODO Maybe move this somewhere else

    def run_wait_to_start(self):
        self.wait(WAIT_FOR_READY_TIMER)
        self.draw_ready_sign()

    def run_wait_after_ghost_hit(self):
        self.wait(GHOST_HIT_TIMER)

    def reset(self):
        self.entities = []
        self.mode = GameMode.WAIT_TO_START
        self.level.load_map(self.level_num)
        self.screen = pygame.display.set_mode((self.level.width() * 16, self.level.height() * 16))
        self.reset_entities()
        self.ate_all = 0
        self.timer = 0
        self.text_box.clear_text()

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

    def wait(self, limit):
        self.timer += 1
        if self.timer >= limit:
            self.mode = GameMode.NORMAL
            self.timer = 0
            # TODO set to 0? YES

    def draw_level(self):
        for row in range(self.level.height()):
            for col in range(self.level.width()):
                surf = self.level.get_tile_surf(PVector(col, row))
                self.screen.blit(surf, (col * 16, row * 16))

    def get_events(self):
        self.events = pygame.event.get()

    def check_quit(self):
        for event in self.events:
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit(0)
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
                self.end()

    def check_loss(self):
        if self.no_lives():
            self.end()
        for ghost in self.entities[1:]:
            if ghost.collided_with_pacman():
                if ghost.scared_timer and not ghost.dead():
                    self.add_ghost_hit_score()
                    self.wait_after_ghost_hit()
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

    def wait_after_ghost_hit(self):
        self.mode = GameMode.WAIT_AFTER_GHOST_HIT

    def add_pacman_score(self):
        self.score += self.pacman.add_score()

    def no_lives(self):
        return self.lives <= 0

    def die(self):
        self.lives -= 1
        self.reset_entities()
        self.mode = GameMode.NORMAL

    def end(self):
        self.game_state = GameState.HIGHSCORE
        self.mode = GameMode.WAITING_FOR_NAME
        self.update_highscores()
        # print("This is the end of the demo. Thanks for playing!")
        # print(self.score)
        # exit(0)

    def update_highscores(self):
        if self.text_box.update(self.events):
            self.score_list = self.insert_score(self.text_box.get_text(), self.score_list)
            self.save_highscores()
            self.mode = GameMode.SHOW_HIGHSCORE

    def load_highscores(self):
        return pickle.load(open(os.path.join(resource_folder, 'highscores.p'), 'rb'))

    def save_highscores(self):
        pickle.dump(self.score_list, open(os.path.join(resource_folder, 'highscores.p'), 'wb'))

    def insert_score(self, name: str, curr_scores: List[tuple]):
        for idx, entry in enumerate(curr_scores):
            if self.score > entry[1]:
                curr_scores.insert(idx, (name, self.score))
                curr_scores.pop(-1)
                break
        else:
            curr_scores.append((name, self.score))
        return curr_scores

    def check_q_quit(self):
        keys_pressed = pygame.key.get_pressed()

        if keys_pressed[pygame.K_q]:
            pygame.quit()
            exit(0)

    def draw_highscores(self, scores: List[tuple]):
        list_surf = pygame.Surface((210, 26 * len(scores)))
        for i, entry in enumerate(scores):
            render_str = entry[0] + (15 - len(entry[0]) - len(str(entry[1]))) * ' ' + str(entry[1])
            list_surf.blit(self.render_text(render_str), (0, i * 26))
        self.screen.blit(list_surf, self.get_top_left(list_surf))

    def draw_textbox(self):
        surf = self.text_box.get_surface()
        self.screen.blit(surf, self.get_top_left(surf))

    def draw_quit_hint(self):
        pass

    def check_try_again(self):
        pass

    def draw_query(self):
        text_surf = self.render_text("PLEASE ENTER YOUR NAME:")
        self.screen.blit(text_surf, PVector.to_tuple(PVector.from_tuple(self.get_top_left(text_surf)) - PVector(0, 26)))

    def get_top_left(self, surf: pygame.Surface):
        surf_half_size = PVector.from_tuple(surf.get_size()) / 2
        screen_center = PVector.from_tuple(self.screen.get_size()) / 2
        return PVector.to_tuple(screen_center - surf_half_size)

    def render_text(self, text: str):
        return self.font.render(text, False, (255, 255, 255, 255))


if __name__ == '__main__':
    game = Game()
    game.run()
