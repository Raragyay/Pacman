# coding=utf-8
"""
Main Run string
"""
import logging
import os

from constants import LOG_FOLDER, LOG_FORMAT, CUR_LOG_LEVEL
from game import Game

logging.basicConfig(filename=os.path.join(LOG_FOLDER, 'log.log'),
                    filemode='w',
                    format=LOG_FORMAT,
                    level=CUR_LOG_LEVEL)
game = Game()
game.run()
