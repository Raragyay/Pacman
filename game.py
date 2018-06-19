# coding=utf-8
"""
The main class for the pacman game
"""
import logging
import os
import pickle
import sys
from typing import List

import pygame

from utility import PVector, Level, TextInput
from constants import ALL_GHOSTS_ALL_TIMES, GHOST_EAT_SCORE, GameMode, FONT_FOLDER, RESOURCE_FOLDER, GHOST_HIT_TIMER, \
    WAIT_FOR_READY_TIMER, DEFAULT_LIVES, STARTING_LEVEL, PACMAN_HIT_TIMER
from constants.game_state import GameState
from entities.ghosts.blinky import Blinky
from entities.ghosts.clyde import Clyde
from entities.ghosts.ghost import Ghost
from entities.ghosts.inky import Inky
from entities.ghosts.pinky import Pinky
from entities.pacman import Pacman


class Game:
    """
    Game class. Handles everything including pygame.
    """

    def __init__(self):
        pygame.init()
        _ = pygame.display.set_mode((1, 1))
        self.screen = None
        self.level = Level()
        self.level_num = STARTING_LEVEL
        self.score = 0

        self.clock = pygame.time.Clock()

        self.pacman: Pacman = None
        self.entities = []

        self.game_state = GameState.MAINGAME
        self.mode = GameMode.NORMAL

        self.lives = DEFAULT_LIVES
        self.ate_all = 0
        self.timer = 0

        self.score_list = None
        self.text_box: TextInput = None
        self.font: pygame.font.Font = None

        self.events: List = None
        self.keys_pressed = None

    def setup(self):
        """
        Setup fonts, text boxes, and sets game to main menu state.
        :return:
        """
        logging.debug('Setup beginning.')
        self.level.setup()
        Ghost.load_surfs()
        self.font = self.create_font(24)
        self.text_box = TextInput(initial_string='CHOW', font_family=os.path.join(FONT_FOLDER, 'visitor1.ttf'),
                                  font_size=24, text_color=(255, 255, 255), cursor_color=(100, 100, 100), max_length=10)
        pygame.display.set_caption('Pacman - Arthur Chen', 'Pacman')
        self.screen = pygame.display.set_mode((400, 400))  # For title screen
        self.game_state = GameState.MAINMENU

    def run(self):
        """
        Main game loop. This is the function that is called by main.py.
        :return:
        """
        self.setup()
        while True:
            self.get_events()  # Stored in self.events
            self.check_quit()  # Check for player pressing X button
            if self.game_state == GameState.MAINGAME:
                self.run_main_game()
            elif self.game_state == GameState.HIGHSCORE:
                self.run_highscore()
            elif self.game_state == GameState.MAINMENU:
                self.run_main_menu()
            pygame.display.flip()  # Update from buffer
            self.clear()  # Clear screen
            self.clock.tick(60)  # 60 ticks per second

    def run_main_game(self):
        """
        When the player is actually playing the game.
        :return:
        """
        if self.mode == GameMode.NORMAL:
            self.run_normal()  # Ghosts move, pacman move, etc
        elif self.mode == GameMode.WAIT_TO_START:
            self.run_wait_to_start()  # Just draws the ready symbol
        elif self.mode == GameMode.WAIT_AFTER_GHOST_HIT:
            self.run_wait_after_ghost_hit()  # Little delay after ghosts die
        elif self.mode == GameMode.WAIT_AFTER_PACMAN_HIT:
            self.run_wait_after_pacman_hit()
        self.draw_level()
        self.draw_entities()
        self.draw_numbers()

    def run_highscore(self):
        """
        Ask for name if name has not yet been obtained
        Otherwise, display highscores and prompt for restart
        :return:
        """
        if self.mode == GameMode.WAITING_FOR_NAME:
            self.update_highscores()
            self.draw_textbox()
            self.draw_query()
        elif self.mode == GameMode.SHOW_HIGHSCORE:
            self.draw_highscores(self.score_list)
            self.check_try_again()
            self.draw_quit_hint()
            self.check_q_quit()

    def run_main_menu(self):
        """
        Draw logo and prompt to start
        :return:
        """
        self.draw_pacman_logo()
        self.draw_begin_prompt()
        self.check_begin()

    def run_normal(self):
        """
        Add scores, update positions, and check for wins and losses
        :return:
        """
        self.update_entities()
        self.add_pacman_score()
        self.check_win()
        self.check_loss()

    def run_wait_to_start(self):
        """

        :return:
        """
        self.wait(WAIT_FOR_READY_TIMER)
        self.draw_ready_sign()
        self.check_loss()

    def run_wait_after_ghost_hit(self):
        """

        :return:
        """
        self.wait(GHOST_HIT_TIMER)

    def run_wait_after_pacman_hit(self):
        """
        Reset if we've waited long enough
        :return:
        """
        if self.wait(PACMAN_HIT_TIMER, GameMode.WAIT_TO_START):
            self.reset_entities()

    def start_round(self):
        """
        Reset most things except lives most memorably
        :return:
        """
        self.game_state = GameState.MAINGAME
        self.mode = GameMode.WAIT_TO_START
        self.level.load_map(self.level_num)
        self.screen = pygame.display.set_mode((self.level.width() * 16, self.level.height() * 16))
        self.reset_entities()
        self.ate_all = 0
        self.timer = 0
        logging.debug(self.screen.get_size())

    def reset_entities(self):
        """
        Removes entities then adds fresh entities back in
        :return:
        """
        self.entities = []
        self.add_entities()

    def add_entities(self):
        """
        Makes new pacman, then adds ghosts
        :return:
        """
        self.pacman = Pacman(self.level)
        self.entities.append(self.pacman)
        self.entities.append(Blinky(self.level, self.pacman))
        self.entities.append(Pinky(self.level, self.pacman))
        self.entities.append(Inky(self.level, self.pacman, self.entities[1]))
        self.entities.append(Clyde(self.level, self.pacman))

    def wait(self, limit, next_mode=GameMode.NORMAL):
        """
        Wait for specified amount of time, then transitions to the next mode
        :param limit:
        :param next_mode:
        :return:
        """
        self.timer += 1
        if self.timer >= limit:
            self.mode = next_mode
            self.timer = 0
            return True

    def draw_level(self):
        """
        Draws each tile in the level
        :return:
        """
        for row in range(self.level.height()):
            for col in range(self.level.width()):
                surf = self.level.get_tile_surf(PVector(col, row))
                self.screen.blit(surf, (col * 16, row * 16))

    def get_events(self):
        """
        Gets all the events for future processing
        :return:
        """
        self.events = pygame.event.get()
        self.keys_pressed = pygame.key.get_pressed()

    def check_quit(self):
        """
        Checks if the player pressed the red X button
        :return:
        """
        for event in self.events:
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit(0)
            # To force win
            # if event.type=pygame.

    def draw_ready_sign(self):
        """
        Draw the ready sign on the map
        :return:
        """
        self.screen.blit(self.level.get_ready_gif(),
                         self.level.get_ready_pos())

    def update_entities(self):
        """
        Updates all entities
        :return:
        """
        for entity in self.entities:
            entity.update()

    def draw_entities(self):
        """
        Updates entity surfs, then draws them on the screen
        :return:
        """
        for entity in self.entities:
            if self.mode == GameMode.NORMAL or entity.surf is None:
                entity.update_surf()
            x, y = entity.top_left()
            self.screen.blit(entity.surf, (x, y))

    def draw_numbers(self):
        """
        Draws lives and score
        :return:
        """
        self.draw_lives()
        self.draw_score()

    def draw_lives(self):
        """
        Draw lives on the bottom left
        :return:
        """
        for i in range(self.lives):
            self.screen.blit(self.level.get_life_gif(), (24 + i * 10 + 16, self.level.height() * 16 - 12))

    def draw_score(self):
        """
        Draws the score above lives
        :return:
        """
        for i, char in enumerate(str(self.score)):
            self.screen.blit(self.level.get_text_num(char), (24 + i * 9 + 16, self.level.height() * 16 - 24))

    def clear(self):
        """
        Clears the screen by washing it with black
        :return:
        """
        self.screen.fill(self.level.bg_colour)

    def check_win(self):
        """
        Check for all pellets eaten
        :return:
        """
        if self.level.won():
            # self.mode = GameMode.WAIT_AFTER_FINISH
            # transition time
            self.mode = GameMode.NORMAL
            self.level_num += 1
            try:
                self.start_round()
            except FileNotFoundError:  # If there are no more levels
                self.end()

    def check_loss(self):
        """
        Check for ghost collisions
        :return:
        """
        if self.no_lives():
            self.end()
            return
        for ghost in self.entities[1:]:
            if ghost.collided_with_pacman():
                if ghost.scared_timer and not ghost.dead():
                    self.add_ghost_hit_score()
                    self.wait_after_ghost_hit()
                    ghost.die()
                elif not ghost.dead():
                    self.die()

    def add_ghost_hit_score(self):
        """
        Check for combos and add score
        :return:
        """
        self.pacman.increment_combo()
        self.score += GHOST_EAT_SCORE * self.pacman.combo
        if self.pacman.combo == len(self.entities) - 1:  # If he ate all 4 ghosts
            self.ate_all += 1
            if self.ate_all == self.level.big_dot_num:
                self.score += ALL_GHOSTS_ALL_TIMES  # If you ate all 4 ghosts every single time you get a big bonus

    def wait_after_ghost_hit(self):
        """
        utility
        :return:
        """
        self.mode = GameMode.WAIT_AFTER_GHOST_HIT

    def add_pacman_score(self):
        """
        Utility
        :return:
        """
        self.score += self.pacman.add_score()

    def no_lives(self):
        """
        utility
        :return:
        """
        return self.lives <= 0

    def die(self):
        """
        Utility
        :return:
        """
        self.lives -= 1
        self.mode = GameMode.WAIT_AFTER_PACMAN_HIT

    def end(self):
        """
        Loads high scores and transitions game mode
        :return:
        """
        self.score_list = self.load_highscores()
        self.game_state = GameState.HIGHSCORE
        self.mode = GameMode.WAITING_FOR_NAME
        pygame.display.set_mode((400, 400))
        # print("This is the end of the demo. Thanks for playing!")
        # print(self.score)
        # exit(0)

    def update_highscores(self):
        """
        Updates text box. If user presses enter,
        Update high scores and changes game mode
        :return:
        """
        if self.text_box.update(self.events):
            self.score_list = self.insert_score(self.text_box.get_text(), self.score_list)
            self.save_highscores()
            self.mode = GameMode.SHOW_HIGHSCORE

    @staticmethod
    def load_highscores():
        """
        Utility
        :return:
        """
        return pickle.load(open(os.path.join(RESOURCE_FOLDER, 'highscores.p'), 'rb'))

    def save_highscores(self):
        """
        Utility
        Saves top 5
        :return:
        """
        pickle.dump(self.score_list[:5], open(os.path.join(RESOURCE_FOLDER, 'highscores.p'), 'wb'))

    def insert_score(self, name: str, curr_scores: List[tuple]):
        """
        Simple insert method
        :param name:
        :param curr_scores:
        :return:
        """
        for idx, entry in enumerate(curr_scores):
            if self.score > entry[1]:
                curr_scores.insert(idx, (name, self.score))
                curr_scores.pop(-1)
                break
        else:
            curr_scores.append((name, self.score))
        return curr_scores

    def check_q_quit(self):
        """
        Check for quit at high score
        :return:
        """
        if self.keys_pressed[pygame.K_q]:
            pygame.quit()
            exit(0)

    def draw_highscores(self, scores: List[tuple]):
        """
        Draws each line
        :param scores:
        :return:
        """
        list_surf = pygame.Surface((210, 26 * len(scores)))
        for i, entry in enumerate(scores):
            name_surf = self.render_text(entry[0])  # Name
            score_surf = self.render_text(str(entry[1]))  # Score
            line = pygame.Surface((210, 26))  # Line
            line.blit(name_surf, (0, 0))  # Left side of line
            line.blit(score_surf, (210 - score_surf.get_size()[0], 0))  # Right side of line
            list_surf.blit(line, (0, i * 26))
        self.screen.blit(list_surf, self.get_top_left(list_surf))

    def draw_textbox(self):
        """
        Draw input box
        :return:
        """
        surf = self.text_box.get_surface()
        self.screen.blit(surf, self.get_top_left(surf))

    def draw_quit_hint(self):
        """
        Draw quit hint
        :return:
        """
        text_surf = self.render_text("Press q to quit, r to try again", self.create_font(16))
        self.screen.blit(text_surf, self.vert_offset_middle(text_surf, PVector(0, 150)))

    def check_try_again(self):
        """
        Utility
        :return:
        """
        if self.keys_pressed[pygame.K_r]:
            self.start_game()

    def start_game(self):
        """
        Reset the whole game
        :return:
        """
        self.lives = DEFAULT_LIVES
        self.score = 0
        self.level_num = STARTING_LEVEL
        self.text_box.reset()
        self.start_round()

    def draw_query(self):
        """
        Draw query for text box entry
        :return:
        """
        text_surf = self.render_text("PLEASE ENTER YOUR NAME:")
        self.screen.blit(text_surf, self.vert_offset_middle(text_surf, PVector(0, -26)))

    def get_top_left(self, surf: pygame.Surface):
        """
        Utility
        :param surf:
        :return:
        """
        surf_half_size = PVector.from_tuple(surf.get_size()) / 2  # Center
        screen_center = PVector.from_tuple(self.screen.get_size()) / 2  # Center
        return PVector.to_tuple(screen_center - surf_half_size)  # Offset

    def vert_offset_middle(self, surf: pygame.Surface, offset: PVector):
        """
        Get Top Left but with vertical offset option
        :param surf:
        :param offset:
        :return:
        """
        return PVector.to_tuple(PVector.from_tuple(self.get_top_left(surf)) + offset)

    def render_text(self, text: str, font=None):
        """
        Utility to return surface with text on it
        :param text:
        :param font:
        :return:
        """
        if font is None:
            font = self.font
        return font.render(text, False, (255, 255, 255, 255))

    @staticmethod
    def create_font(size: int):
        """
        Create a font with custom size
        :param size:
        :return:
        """
        return pygame.font.Font(os.path.join(FONT_FOLDER, 'visitor1.ttf'), size)

    def draw_pacman_logo(self):
        """
        Utility
        :return:
        """
        logo = self.level.get_logo()
        self.screen.blit(logo, self.vert_offset_middle(logo, PVector(0, -100)))

    def draw_begin_prompt(self):
        """
        Draw Prompt to begin
        :return:
        """
        font = self.create_font(16)
        text = self.render_text('Press any key to begin', font)
        self.screen.blit(text, self.vert_offset_middle(text, PVector(0, 100)))

    def check_begin(self):
        """
        Utility
        :return:
        """
        if any(key for key in self.keys_pressed):
            self.start_game()


if __name__ == '__main__':
    game = Game()
    game.run()
