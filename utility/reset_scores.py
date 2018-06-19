# coding=utf-8
"""
Small script to reset all scores to 0 to see score ordering.
"""
import pickle

highscores = [
    ("CHOW", 0),
    ("CHOW", 0),
    ("CHOW", 0),
    ("CHOW", 0),
    ("CHOW", 0),
]

pickle.dump(highscores, open('resources/highscores.p', 'wb'))
