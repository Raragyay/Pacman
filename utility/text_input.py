# coding=utf-8
"""
Text input box.
"""
import os.path
import sys
from typing import List

import pygame
import pygame.locals as pl


class TextInput:
    """
    Surface that accepts events to render text and features cursor.
    """

    def __init__(self, initial_string="",
                 font_family="",
                 font_size=35,
                 anti_alias=True,
                 text_color=(0, 0, 0),
                 cursor_color=(0, 0, 1),
                 repeat_keys_initial_ms=400,
                 repeat_keys_interval_ms=35,
                 max_length=sys.maxsize):
        """

        :param initial_string: Initial string to be shown
        :param font_family: Font family to be used. Can be path to font object or builtin font name
        :param font_size: Font size
        :param anti_alias: Whether or not to use anti-aliasing to smooth out font
        :param text_color: Colour of text
        :param cursor_color: Colour of cursor
        :param repeat_keys_initial_ms: How long to wait before repeating keystrokes
        :param repeat_keys_interval_ms: How long to wait between keystrokes after starting to spam them
        :param max_length: Max length for text box
        """

        # Text related vars:
        self.anti_alias = anti_alias
        self.text_color = text_color
        self.font_size = font_size
        self.input_string = initial_string  # Inputted text
        self.max_length = max_length
        if not os.path.isfile(font_family):
            font_family = pygame.font.match_font(font_family)
        self.font_object = pygame.font.Font(font_family, font_size)

        # Text-surface will be created during the first update call:
        self.surface = pygame.Surface((1, 1))
        self.surface.set_alpha(0)  # Transparent background

        # Vars to make KeyDowns repeat after user pressed a key for some time:
        self.keyrepeat_counters = {}  # {event.key: (counter_int, event.unicode)} (look for "***")
        self.keyrepeat_initial_interval_ms = repeat_keys_initial_ms
        self.keyrepeat_interval_ms = repeat_keys_interval_ms

        # Cursor vars:
        self.cursor_surface = pygame.Surface((int(self.font_size / 20 + 1), self.font_size))
        self.cursor_surface.fill(cursor_color)
        self.cursor_position = len(initial_string)  # Inside text
        self.cursor_visible = True  # Switches every self.cursor_switch_ms
        self.cursor_switch_ms = 500
        self.cursor_ms_counter = 0

        self.clock = pygame.time.Clock()

    def update(self, events: List[pygame.event.Event]) -> bool:
        """

        :param events: List of pygame events to process
        :return: boolean
        """
        for event in events:
            if event.type == pygame.KEYDOWN:
                self.cursor_visible = True  # So the user sees where he writes

                # If counter does not exist, create counter for that key:
                if event.key not in self.keyrepeat_counters:
                    self.keyrepeat_counters[event.key] = [0, event.unicode]

                if event.key == pl.K_BACKSPACE:
                    self.input_string = self.input_string[:max(self.cursor_position - 1, 0)] + \
                                        self.input_string[self.cursor_position:]

                    # Subtract one from cursor_pos, but do not go below zero:
                    self.cursor_position = max(self.cursor_position - 1, 0)
                elif event.key == pl.K_DELETE:
                    self.input_string = self.input_string[:self.cursor_position] + \
                                        self.input_string[self.cursor_position + 1:]

                elif event.key == pl.K_RETURN:  # Enter key
                    return True

                elif event.key == pl.K_RIGHT:
                    # Add one to cursor_pos, but do not exceed len(input_string)
                    self.cursor_position = min(self.cursor_position + 1, len(self.input_string))

                elif event.key == pl.K_LEFT:
                    # Subtract one from cursor_pos, but do not go below zero:
                    self.cursor_position = max(self.cursor_position - 1, 0)

                elif event.key == pl.K_END:
                    self.cursor_position = len(self.input_string)

                elif event.key == pl.K_HOME:
                    self.cursor_position = 0

                elif len(self.input_string) < self.max_length:
                    # If no special key is pressed, add unicode of key to input_string
                    self.input_string = self.input_string[:self.cursor_position] + \
                                        event.unicode + \
                                        self.input_string[self.cursor_position:]
                    self.cursor_position += len(event.unicode)  # Some are empty, e.g. K_UP

            elif event.type == pl.KEYUP:
                # *** Because KeyUp doesn't include event.unicode, this dict is stored in such a weird way
                if event.key in self.keyrepeat_counters:
                    del self.keyrepeat_counters[event.key]

        # Update key counters:
        for key in self.keyrepeat_counters:
            self.keyrepeat_counters[key][0] += self.clock.get_time()  # Update clock
            # Generate new key events if enough time has passed:
            if self.keyrepeat_counters[key][0] >= self.keyrepeat_initial_interval_ms:
                self.keyrepeat_counters[key][0] = self.keyrepeat_initial_interval_ms - \
                                                  self.keyrepeat_interval_ms

                event_key, event_unicode = key, self.keyrepeat_counters[key][1]
                pygame.event.post(pygame.event.Event(pl.KEYDOWN, {
                    'key'    : event_key,
                    'unicode': event_unicode}))

        # Re-render text surface:
        self.surface = self.font_object.render(self.input_string, self.anti_alias, self.text_color)

        # Update self.cursor_visible
        self.cursor_ms_counter += self.clock.get_time()
        if self.cursor_ms_counter >= self.cursor_switch_ms:
            self.cursor_ms_counter %= self.cursor_switch_ms
            self.cursor_visible = not self.cursor_visible

        if self.cursor_visible:
            cursor_x_pos = self.font_object.size(self.input_string[:self.cursor_position])[0]
            # Check where the right side of the cursor pos is
            # Without this, the cursor is invisible when self.cursor_position > 0:
            if self.cursor_position > 0:
                cursor_x_pos -= self.cursor_surface.get_width()  # move it to top left
            self.surface.blit(self.cursor_surface, (cursor_x_pos, 0))

        self.clock.tick()  # To record time interval
        return False

    def get_surface(self) -> pygame.Surface:
        """
        :return: surface to blit
        """
        return self.surface

    def get_text(self) -> str:
        """
        To record username
        :return: username
        """
        return self.input_string

    def reset(self) -> None:
        """
        To reset username, so that Enter key is not still recorded.
        Otherwise, if the game restarted, username would be automatically given.
        :return: None
        """
        self.input_string = ""
        self.cursor_position = 0
        self.keyrepeat_counters = {}
