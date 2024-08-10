import pytest

from dlgo.agent.helpers import is_point_an_eye
from dlgo.gotypes import Player, Point
from misc.board_utils import create_board_from_ascii


def test_is_point_an_eye():

    # Initial board setup
    ascii_board = """
      1 2 3 4 5
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
