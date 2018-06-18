import os

from constants import resource_folder

highscores = [
    ("CHOW", 15000),
    ("CHOW", 6020),
    ("CHOW", 4000),
    ("CHOW", 3000),
    ("CHOW", 2000),
]
import pickle

pickle.dump(highscores, open('resources/highscores.p', 'wb'))
