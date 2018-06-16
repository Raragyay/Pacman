# coding=utf-8
import os

import pygame


class TextInput:
    def __init__(self, initial_string="",
                 font_family="",
                 font_size=35,
                 antialias=True,
                 text_colour=(0, 0, 0),
                 cursor_colour=(0, 0, 1),
                 repeat_keys_initial_ms=400,
                 repeat_keys_interval_ms=35
                 ):
        """

        :param initial_string:
        :param font_family:
        :param font_size:
        :param antialias:
        :param text_color:
        :param cursor_color:
        :param repeat_keys_initial_ms:
        :param repeat_keys_interval_ms:
        """
        self.antialias = antialias
        self.text_colour = text_colour
        self.font_size = font_size
        self.input_string = initial_string
        if not os.path.isfile(font_family):
            font_family = pygame.font.match_font(font_family)
        self.font_object = pygame.font.Font(font_family, font_size)

        self.surface = pygame.Surface((1, 1))
        self.surface.set_alpha(0)

        def update(self, events):
