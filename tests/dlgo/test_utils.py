"""
This file was initially generated using an AI language model (Claude 3.5 Sonnet),
as part of an educational project based on the book "Deep Learning and the Game of Go"
by Max Pumperla and Kevin Ferguson (Manning Publications, 2019).

The generated code has been reviewed, potentially modified, and adapted to fit the
project's requirements and to ensure correctness and adherence to the book's concepts.
"""

from contextlib import redirect_stdout
from io import StringIO

import pytest

from dlgo.board import Board
from dlgo.gotypes import Player, Point
from dlgo.move import Move
from dlgo.utils import point_from_coords, print_board, print_move


def capture_print_output(func, *args, **kwargs):
    f = StringIO()
    with redirect_stdout(f):
        func(*args, **kwargs)
    return f.getvalue().strip()


def test_print_move_pass():
    player = Player.black
    move = Move(is_pass=True)
    output = capture_print_output(print_move, player, move)
    assert output == "Player.black passes"


def test_print_move_resign():
    player = Player.white
    move = Move(is_resign=True)
    output = capture_print_output(print_move, player, move)
    assert output == "Player.white resigns"


def test_print_move_regular():
    player = Player.black
    point = Point(row=3, col=3)
    move = Move(point=point)
    output = capture_print_output(print_move, player, move)
    assert output == "Player.black C3"


def test_print_larger_board():
    board = Board(5, 5)
    board.place_stone(Player.black, Point(1, 1))
    board.place_stone(Player.white, Point(5, 5))
    expected_output = """
 5  .  .  .  .  W
 4  .  .  .  .  .
 3  .  .  .  .  .
 2  .  .  .  .  .
 1  B  .  .  .  .
    A  B  C  D  E
""".strip()
    actual_output = capture_print_output(print_board, board)
    # Strip trailing whitespace from each line of actual_output
    actual_output = "\n".join(line.rstrip() for line in actual_output.split("\n"))
    assert actual_output == expected_output


def test_print_board_with_single_stone():
    board = Board(3, 3)
    board.place_stone(Player.black, Point(2, 2))
    expected_output = """
 3  .  .  .
 2  .  B  .
 1  .  .  .
    A  B  C
    """.strip()
    actual_output = capture_print_output(print_board, board)
    # Strip trailing whitespace from each line of actual_output
    actual_output = "\n".join(line.rstrip() for line in actual_output.split("\n"))
    assert actual_output == expected_output


def test_point_from_coords():
    assert point_from_coords("A1") == Point(row=1, col=1)
    assert point_from_coords("B2") == Point(row=2, col=2)
    assert point_from_coords("C3") == Point(row=3, col=3)
    assert point_from_coords("D4") == Point(row=4, col=4)
    assert point_from_coords("E5") == Point(row=5, col=5)
    assert point_from_coords("J10") == Point(row=10, col=9)
    assert point_from_coords("K11") == Point(row=11, col=10)
    assert point_from_coords("T19") == Point(row=19, col=19)
