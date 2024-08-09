import pytest

from dlgo.go_types import Player, Point
from dlgo.goboard_slow import GoString


def test_gostring_init():
    gostring = GoString(Player.black, {Point(1, 1)}, {Point(1, 2), Point(2, 1)})
    assert gostring.color == Player.black
    assert gostring.stones == {Point(1, 1)}
    assert gostring.liberties == {Point(1, 2), Point(2, 1)}


def test_remove_liberty():
    gostring = GoString(Player.black, {Point(1, 1)}, {Point(1, 2), Point(2, 1)})
    gostring.remove_liberty(Point(1, 2))

    assert gostring.liberties == {Point(2, 1)}


def test_remove_nonexistent_liberty():
    gostring = GoString(Player.black, {Point(1, 1)}, {Point(1, 2), Point(2, 1)})
    with pytest.raises(ValueError):
        gostring.remove_liberty(Point(3, 3))


def test_add_liberty():
    gostring = GoString(Player.black, {Point(1, 1)}, {Point(1, 2)})

    gostring.add_liberty(Point(2, 1))
    assert gostring.liberties == {Point(1, 2), Point(2, 1)}


def test_merged_with():
    gostring1 = GoString(Player.black, {Point(1, 1)}, {Point(1, 2), Point(2, 1)})
    gostring2 = GoString(Player.black, {Point(1, 2)}, {Point(1, 1), Point(1, 3)})
    merged = gostring1.merged_with(gostring2)
    assert merged.color == Player.black
    assert merged.stones == {Point(1, 1), Point(1, 2)}
    assert merged.liberties == {Point(2, 1), Point(1, 3)}


def test_merged_with_different_colors():
    gostring1 = GoString(Player.black, {Point(1, 1)}, {Point(1, 2), Point(2, 1)})
    gostring2 = GoString(Player.white, {Point(1, 2)}, {Point(1, 1), Point(1, 3)})
    with pytest.raises(ValueError):
        gostring1.merged_with(gostring2)


def test_num_liberties():
    gostring = GoString(Player.black, {Point(1, 1)}, {Point(1, 2), Point(2, 1)})
    assert gostring.num_liberties == 2


def test_eq():
    gostring1 = GoString(Player.black, {Point(1, 1)}, {Point(1, 2), Point(2, 1)})
    gostring2 = GoString(Player.black, {Point(1, 1)}, {Point(1, 2), Point(2, 1)})
    gostring3 = GoString(Player.white, {Point(1, 1)}, {Point(1, 2), Point(2, 1)})
    assert gostring1 == gostring2
    assert gostring1 != gostring3
    assert gostring1 != "not a GoString"
