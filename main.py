# coding=utf-8
import logging
import os

from constants import log_folder, log_format, cur_log_level
from game import Game

logging.basicConfig(filename=os.path.join(log_folder, 'log.log'),
                    filemode='w',
                    format=log_format,
                    level=cur_log_level)
game = Game()
game.run()
