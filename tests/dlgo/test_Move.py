"""
This file was initially generated using an AI language model (Claude 3.5 Sonnet),
as part of an educational project based on the book "Deep Learning and the Game of Go"
by Max Pumperla and Kevin Ferguson (Manning Publications, 2019).

The generated code has been reviewed, potentially modified, and adapted to fit the
project's requirements and to ensure correctness and adherence to the book's concepts.
"""

import pytest

from dlgo.gotypes import Point
from dlgo.move import Move


def test_move_play():
    point = (3, 3)
    move = Move.play(point)
    assert move.point == point
    assert move.is_play
    assert not move.is_pass
    assert not move.is_resign


def test_move_pass():
    move = Move.pass_turn()
    assert move.point is None
    assert not move.is_play
    assert move.is_pass
    assert not move.is_resign


def test_move_resign():
    move = Move.resign()
    assert move.point is None
    assert not move.is_play
    assert not move.is_pass
    assert move.is_resign


def test_move_init_play():
    point = (4, 4)
    move = Move(point=point)
    assert move.point == point
    assert move.is_play
    assert not move.is_pass
    assert not move.is_resign


def test_move_init_pass():
    move = Move(is_pass=True)
    assert move.point is None
    assert not move.is_play
    assert move.is_pass
    assert not move.is_resign


def test_move_init_resign():
    move = Move(is_resign=True)
    assert move.point is None
    assert not move.is_play
    assert not move.is_pass
    assert move.is_resign


def test_move_equality():
    point1 = Point(3, 3)
    point2 = Point(3, 3)
    point3 = Point(4, 4)

    move1 = Move.play(point1)
    move2 = Move.play(point2)
    move3 = Move.play(point3)
    move4 = Move.pass_turn()
    move5 = Move.resign()

    assert move1 == move2  # Same point
    assert move1 != move3  # Different points
    assert move1 != move4  # Play vs Pass
    assert move1 != move5  # Play vs Resign
    assert move4 != move5  # Pass vs Resign

    # Test equality with non-Move objects
    assert move1 != point1
    assert move1 != "not a move"


def test_move_hash():
    point1 = Point(3, 3)
    point2 = Point(3, 3)
    point3 = Point(4, 4)

    move1 = Move.play(point1)
    move2 = Move.play(point2)
    move3 = Move.play(point3)
    move4 = Move.pass_turn()
    move5 = Move.resign()

    # Same moves should have the same hash
    assert hash(move1) == hash(move2)

    # Different moves should have different hashes
    assert hash(move1) != hash(move3)
    assert hash(move1) != hash(move4)
    assert hash(move1) != hash(move5)
    assert hash(move4) != hash(move5)


def test_move_in_set():
    point1 = Point(3, 3)
    point2 = Point(3, 3)
    point3 = Point(4, 4)

    move1 = Move.play(point1)
    move2 = Move.play(point2)
    move3 = Move.play(point3)
    move4 = Move.pass_turn()
    move5 = Move.resign()

    move_set = {move1, move2, move3, move4, move5}

    # Set should contain 4 unique moves (move1 and move2 are considered equal)
    assert len(move_set) == 4

    # Check membership
    assert move1 in move_set
    assert Move.play(Point(3, 3)) in move_set
    assert Move.play(Point(5, 5)) not in move_set


def test_move_as_dict_key():
    point1 = Point(3, 3)
    point2 = Point(3, 3)
    point3 = Point(4, 4)

    move1 = Move.play(point1)
    move2 = Move.play(point2)
    move3 = Move.play(point3)
    move4 = Move.pass_turn()
    move5 = Move.resign()

    move_dict = {move1: "play (3,3)", move3: "play (4,4)", move4: "pass", move5: "resign"}

    assert len(move_dict) == 4
    assert move_dict[move1] == "play (3,3)"
    assert move_dict[move2] == "play (3,3)"  # move2 is equal to move1
    assert move_dict[Move.play(Point(3, 3))] == "play (3,3)"
    assert move_dict[move4] == "pass"
    assert move_dict[move5] == "resign"

    with pytest.raises(KeyError):
        _ = move_dict[Move.play(Point(5, 5))]
