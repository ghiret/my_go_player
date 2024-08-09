import pytest

from dlgo.go_types import Player, Point
from dlgo.goboard_slow import Board, GoString


@pytest.fixture
def empty_board():
    return Board(19, 19)


def test_board_initialization(empty_board):
    assert empty_board.num_rows == 19
    assert empty_board.num_cols == 19
    assert len(empty_board._grid) == 0


def test_is_on_grid():
    board = Board(5, 5)

    # Test valid points
    assert board.is_on_grid(Point(1, 1)), "Point (1,1) should be on grid"
    assert board.is_on_grid(Point(5, 5)), "Point (5,5) should be on grid"
    assert board.is_on_grid(Point(3, 3)), "Point (3,3) should be on grid"

    # Test invalid points
    assert not board.is_on_grid(Point(0, 0)), "Point (0,0) should not be on grid"
    assert not board.is_on_grid(Point(6, 6)), "Point (6,6) should not be on grid"
    assert not board.is_on_grid(Point(0, 3)), "Point (0,3) should not be on grid"
    assert not board.is_on_grid(Point(3, 0)), "Point (3,0) should not be on grid"
    assert not board.is_on_grid(Point(6, 3)), "Point (6,3) should not be on grid"
    assert not board.is_on_grid(Point(3, 6)), "Point (3,6) should not be on grid"


def test_place_stone(empty_board):
    point = Point(3, 3)
    empty_board.place_stone(Player.black, point)
    assert empty_board.get(point) == Player.black


def test_place_stone_occupied(empty_board):
    point = Point(3, 3)
    empty_board.place_stone(Player.black, point)
    with pytest.raises(AssertionError):
        empty_board.place_stone(Player.white, point)


def test_capture_stone():
    board = Board(5, 5)
    board.place_stone(Player.black, Point(2, 2))
    board.place_stone(Player.white, Point(1, 2))
    board.place_stone(Player.white, Point(2, 1))
    board.place_stone(Player.white, Point(2, 3))
    board.place_stone(Player.white, Point(3, 2))
    assert board.get(Point(2, 2)) is None


def test_capture_multiple_stones():
    board = Board(5, 5)
    board.place_stone(Player.black, Point(2, 2))
    board.place_stone(Player.black, Point(2, 3))
    board.place_stone(Player.white, Point(1, 2))
    board.place_stone(Player.white, Point(1, 3))
    board.place_stone(Player.white, Point(2, 1))
    board.place_stone(Player.white, Point(2, 4))
    board.place_stone(Player.white, Point(3, 2))
    board.place_stone(Player.white, Point(3, 3))
    assert board.get(Point(2, 2)) is None
    assert board.get(Point(2, 3)) is None


def test_get_go_string():
    board = Board(5, 5)
    board.place_stone(Player.black, Point(2, 2))
    board.place_stone(Player.black, Point(2, 3))
    go_string = board.get_go_string(Point(2, 2))
    assert isinstance(go_string, GoString)
    assert go_string.color == Player.black
    assert Point(2, 2) in go_string.stones
    assert Point(2, 3) in go_string.stones


def test_merge_go_strings():
    board = Board(5, 5)
    board.place_stone(Player.black, Point(2, 2))
    board.place_stone(Player.black, Point(2, 3))
    board.place_stone(Player.black, Point(2, 4))
    go_string = board.get_go_string(Point(2, 2))
    assert len(go_string.stones) == 3
    assert Point(2, 2) in go_string.stones
    assert Point(2, 3) in go_string.stones
    assert Point(2, 4) in go_string.stones


def test_liberty_count():
    board = Board(5, 5)
    board.place_stone(Player.black, Point(2, 2))
    go_string = board.get_go_string(Point(2, 2))
    assert go_string.num_liberties == 4
    board.place_stone(Player.black, Point(2, 1))
    go_string = board.get_go_string(Point(2, 2))
    assert go_string.num_liberties == 5
