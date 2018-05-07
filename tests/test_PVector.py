# coding=utf-8
from unittest import TestCase

from PVector import PVector


class TestPVector(TestCase):
    def test_init(self):
        vec = PVector(1, 0)
        assert vec.x == 1
        assert vec.y == 0

        vec = PVector(500, 149)
        assert vec.x == 500
        assert vec.y == 149

    def test_add(self):
        vec = PVector(10, 10)
        assert vec.x == vec.y
        vec += PVector(5, 6)
        assert vec.x != vec.y
        assert vec.x == 15
        assert vec.y == 16

        added_vec = PVector(20, 20)
        assert vec + PVector(5, 4) == added_vec