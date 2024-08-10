from contextlib import redirect_stdout
from io import StringIO

import pytest

from dlgo.goboard_slow import Board
from dlgo.gotypes import Player, Point
from misc.board_utils import create_board_from_ascii, print_board


def test_create_empty_board():
    ascii_board = """
      1 2 3
    1 . . .
    2 . . .
    3 . . .
    """
    board = create_board_from_ascii(ascii_board)
    assert board.num_rows == 3
    assert board.num_cols == 3
    for row in range(1, 4):
        for col in range(1, 4):
            assert board.get(Point(row, col)) is None


def test_create_board_with_stones():
    ascii_board = """
      1 2 3
    1 B . W
    2 . B .
    3 W . B
    """
    board = create_board_from_ascii(ascii_board)
    assert board.get(Point(1, 1)) == Player.black
    assert board.get(Point(1, 3)) == Player.white
    assert board.get(Point(2, 2)) == Player.black
    assert board.get(Point(3, 1)) == Player.white
    assert board.get(Point(3, 3)) == Player.black
    assert board.get(Point(2, 1)) is None


def test_create_larger_board():
    ascii_board = """
      1 2 3 4 5
    1 . . . . .
    2 . B W . .
    3 . B W . .
    4 . B W . .
    5 . . . . .
    """
    board = create_board_from_ascii(ascii_board)
    assert board.num_rows == 5
    assert board.num_cols == 5
    for row in range(2, 5):
        assert board.get(Point(row, 2)) == Player.black
        assert board.get(Point(row, 3)) == Player.white


def test_create_board_with_extra_whitespace():
    ascii_board = """
        1   2   3
    1   .   .   .
    2   B   .   W
    3   .   .   .
    """
    board = create_board_from_ascii(ascii_board)
    assert board.num_rows == 3
    assert board.num_cols == 3
    assert board.get(Point(2, 1)) == Player.black
    assert board.get(Point(2, 3)) == Player.white


def test_create_board_without_column_numbers():
    ascii_board = """
    1 . . .
    2 B . W
    3 . . .
    """
    board = create_board_from_ascii(ascii_board)
    assert board.num_rows == 3
    assert board.num_cols == 3
    assert board.get(Point(2, 1)) == Player.black
    assert board.get(Point(2, 3)) == Player.white


def test_create_board_with_invalid_characters():
    ascii_board = """
      1 2 3
    1 X . O
    2 . Y .
    3 Z . Q
    """
    with pytest.raises(ValueError):
        create_board_from_ascii(ascii_board)


def test_create_board_with_inconsistent_rows():
    ascii_board = """
      1 2 3
    1 . . .
    2 . . . .
    3 . .
    """
    with pytest.raises(ValueError):
        create_board_from_ascii(ascii_board)


def test_create_board_from_empty_string():
    with pytest.raises(ValueError):
        create_board_from_ascii("")


def test_create_board_from_single_line():
    ascii_board = "1 B W B"
    with pytest.raises(ValueError):
        create_board_from_ascii(ascii_board)


def capture_print_output(func, *args, **kwargs):
    f = StringIO()
    with redirect_stdout(f):
        func(*args, **kwargs)
    return f.getvalue().strip()


def test_print_empty_board():
    board = Board(3, 3)
    expected_output = """
  1 2 3
1 . . .
2 . . .
3 . . .
""".strip()
    actual_output = capture_print_output(print_board, board)
    assert actual_output == expected_output


def test_print_board_with_stones():
    board = Board(3, 3)
    board.place_stone(Player.black, Point(1, 1))
    board.place_stone(Player.white, Point(2, 2))
    board.place_stone(Player.black, Point(3, 3))
    expected_output = """
  1 2 3
1 B . .
2 . W .
3 . . B
""".strip()
    actual_output = capture_print_output(print_board, board)
    assert actual_output == expected_output


def test_print_larger_board():
    board = Board(5, 5)
    board.place_stone(Player.black, Point(1, 1))
    board.place_stone(Player.white, Point(5, 5))
    expected_output = """
  1 2 3 4 5
1 B . . . .
2 . . . . .
3 . . . . .
4 . . . . .
5 . . . . W
""".strip()
    actual_output = capture_print_output(print_board, board)
    assert actual_output == expected_output


def test_print_board_with_single_stone():
    board = Board(3, 3)
    board.place_stone(Player.black, Point(2, 2))
    expected_output = """
  1 2 3
1 . . .
2 . B .
3 . . .
""".strip()
    actual_output = capture_print_output(print_board, board)
    assert actual_output == expected_output


def test_print_board_with_edge_stones():
    board = Board(3, 3)
    board.place_stone(Player.black, Point(1, 1))
    board.place_stone(Player.white, Point(1, 3))
    board.place_stone(Player.black, Point(3, 1))
    board.place_stone(Player.white, Point(3, 3))
    expected_output = """
  1 2 3
1 B . W
2 . . .
3 B . W
""".strip()
    actual_output = capture_print_output(print_board, board)
    assert actual_output == expected_output
