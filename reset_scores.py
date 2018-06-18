# coding=utf-8
import pickle

highscores = [
    ("CHOW", 0),
    ("CHOW", 0),
    ("CHOW", 0),
    ("CHOW", 0),
    ("CHOW", 0),
]

pickle.dump(highscores, open('resources/highscores.p', 'wb'))
