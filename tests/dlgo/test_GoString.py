"""
This file was initially generated using an AI language model (Claude 3.5 Sonnet),
as part of an educational project based on the book "Deep Learning and the Game of Go"
by Max Pumperla and Kevin Ferguson (Manning Publications, 2019).

The generated code has been reviewed, potentially modified, and adapted to fit the
project's requirements and to ensure correctness and adherence to the book's concepts.
"""

import pytest

from dlgo.gostring import GoString
from dlgo.gotypes import Player, Point


def test_gostring_init():
    gostring = GoString(Player.black, {Point(1, 1)}, {Point(1, 2), Point(2, 1)})
    assert gostring.color == Player.black
    assert gostring.stones == {Point(1, 1)}
    assert gostring.liberties == {Point(1, 2), Point(2, 1)}


def test_without_liberty():
    gostring = GoString(Player.black, {Point(1, 1)}, {Point(1, 2), Point(2, 1)})
    new_gostring = gostring.without_liberty(Point(1, 2))

    assert new_gostring.liberties == {Point(2, 1)}
    # Check that the original gostring still has all the liberties.
    assert gostring.liberties == {Point(1, 2), Point(2, 1)}


def test_without_liberty_nonexistent_liberty():
    gostring = GoString(Player.black, {Point(1, 1)}, {Point(1, 2), Point(2, 1)})
    with pytest.raises(ValueError):
        gostring.without_liberty(Point(3, 3))


def test_with_liberty():
    gostring = GoString(Player.black, {Point(1, 1)}, {Point(1, 2)})

    new_gostring = gostring.with_liberty(Point(2, 1))
    assert new_gostring.liberties == {Point(1, 2), Point(2, 1)}
    # The old liberty should still have the the single liberty.
    assert gostring.liberties == {Point(1, 2)}


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
