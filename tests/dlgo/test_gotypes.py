"""
This file was initially generated using an AI language model (Claude 3.5 Sonnet),
as part of an educational project based on the book "Deep Learning and the Game of Go"
by Max Pumperla and Kevin Ferguson (Manning Publications, 2019).

The generated code has been reviewed, potentially modified, and adapted to fit the
project's requirements and to ensure correctness and adherence to the book's concepts.
"""

from dlgo.gotypes import Player, Point


def test_player_black_other():
    assert Player.black.other == Player.white


def test_player_white_other():
    assert Player.white.other == Player.black


def test_point_neighbors():
    p = Point(2, 3)
    expected_neighbors = [Point(1, 3), Point(3, 3), Point(2, 2), Point(2, 4)]
    assert p.neighbors() == expected_neighbors
