from unittest import TestCase

from PVector import PVector
from entity import Entity


class TestEntity(TestCase):
    def test_pixel_to_node(self):
        entity = Entity(PVector(1, 1), None)

        entity.pos = PVector(24, 24)  # middle of node (1,1)
        assert entity.pixel_to_node() == PVector(1, 1),entity.pixel_to_node()
        print("Passed test with {} that returned {}".format(entity.pos, PVector(1, 1)))

        entity.pos = PVector(16, 16)  # top left of node (1,1)
        assert entity.pixel_to_node() == PVector(1, 1),entity.pixel_to_node()
        print("Passed test with {} that returned {}".format(entity.pos, PVector(1, 1)))

        entity.pos = PVector(31, 31)  # bottom right of node (1,1)
        assert entity.pixel_to_node() == PVector(1, 1),entity.pixel_to_node()
        print("Passed test with {} that returned {}".format(entity.pos, PVector(1, 1)))
