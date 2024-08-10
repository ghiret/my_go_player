# test_dlgo.py

from dlgo.gotypes import Player, Point


def test_player_black_other():
    assert Player.black.other == Player.white


def test_player_white_other():
    assert Player.white.other == Player.black


def test_point_neighbors():
    p = Point(2, 3)
    expected_neighbors = [Point(1, 3), Point(3, 3), Point(2, 2), Point(2, 4)]
    assert p.neighbors() == expected_neighbors
