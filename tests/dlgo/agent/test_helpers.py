"""
This file was initially generated using an AI language model (Claude 3.5 Sonnet),
as part of an educational project based on the book "Deep Learning and the Game of Go"
by Max Pumperla and Kevin Ferguson (Manning Publications, 2019).

The generated code has been reviewed, potentially modified, and adapted to fit the
project's requirements and to ensure correctness and adherence to the book's concepts.
"""

import pytest

from dlgo.agent.helpers import is_point_an_eye
from dlgo.gotypes import Player, Point
from misc.board_utils import create_board_from_ascii


def test_is_point_an_eye_on_occupied_point():

    # Initial board setup
    ascii_board = """
      A B C
    1 B . .
    2 . . .
    3 . . .
    """

    board = create_board_from_ascii(ascii_board)

    point1 = Point(1, 1)
    assert not is_point_an_eye(board, point1, Player.white), "Point (1, 1) is not an eye as it is occuppied"


def test_is_point_an_eye():

    # Initial board setup
    ascii_board = """
      A B C D E
    1 . . . . .
    2 . . . . .
    3 . B B B B
    4 B W W W W
    5 B W . W .
    """

    board = create_board_from_ascii(ascii_board)

    point1 = Point(5, 3)
    assert is_point_an_eye(board, point1, Player.white), "Point (5, 3) is an eye for White"
    assert not is_point_an_eye(board, point1, Player.black), "Point (5, 3) is not an eye for Black"

    point1 = Point(5, 5)
    assert is_point_an_eye(board, point1, Player.white), "Point (5, 5) is an eye for White"
    assert not is_point_an_eye(board, point1, Player.black), "Point (5, 5) is not an eye for Black"

    point1 = Point(1, 1)
    assert not is_point_an_eye(board, point1, Player.white), "Point (1, 1) is not an eye for White"
    assert not is_point_an_eye(board, point1, Player.black), "Point (1, 1) is not an eye for Black"


def test_is_point_an_eye_with_eyes_in_the_middle():

    # Initial board setup
    ascii_board = """
      A B C D E F G H
    1 . . . . . . . .
    2 . . B B B B . B
    3 . . B W W W B .
    4 . . B W . W B .
    5 . . . W W . W B
    6 . . . B W W W B
    7 . . B . B B B .
    8 . . . . . . . .
    """

    board = create_board_from_ascii(ascii_board)

    point1 = Point(4, 5)
    assert is_point_an_eye(board, point1, Player.white), "Point (4, 5) is an eye for White"
    assert not is_point_an_eye(board, point1, Player.black), "Point (4, 5) is not an eye for Black"

    point1 = Point(5, 6)
    assert not is_point_an_eye(board, point1, Player.white), "Point (5, 6) is an eye for White"
    assert not is_point_an_eye(board, point1, Player.black), "Point (5, 6) is not an eye for Black"

    point1 = Point(7, 8)
    assert not is_point_an_eye(board, point1, Player.white), "Point (7, 8) is not an eye for White"
    assert not is_point_an_eye(board, point1, Player.black), "Point (7, 8) is not an eye for Black"
