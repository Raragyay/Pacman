# coding=utf-8
from unittest import TestCase

from tile import Tile


class TestTile(TestCase):
    def test_init(self):
        tile = Tile(0, 'Empty Tile', 'This is an empty tile')
        assert tile.id == 0
        assert tile.name == 'Empty Tile'
        assert tile.desc == 'This is an empty tile'

        tile = Tile(100, 'Horizontal Tile', 'Straight Horizontal Wall')
        assert tile.id == 100
        assert tile.name == 'Horizontal Tile'
        assert tile.desc == 'Straight Horizontal Wall'

    def test_surface(self):
        tile = Tile(100, 'wall-straight-h', 'Straight Horizontal Wall')
        assert tile.id == 100
        assert tile.name == 'wall-straight-h'
        assert tile.desc == 'Straight Horizontal Wall'
        tile.load_surface((255, 255, 255, 255), (255, 0, 0, 255), (0, 255, 0, 255), (0, 0, 255, 255))
        assert tile.get_surf().get_at((5, 5)) == (255, 0, 0, 255)
