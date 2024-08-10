import pytest

from dlgo.goboard_slow import Board, GoString
from dlgo.gotypes import Player, Point
from misc.board_utils import create_board_from_ascii


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

    ascii_board = """
      A B C D E
    1 . W . . .
    2 W B W . .
    3 . W . . .
    4 . . . . .
    5 . . . . .
    """

    board = create_board_from_ascii(ascii_board)
    assert board.get(Point(2, 2)) is None

    # White pieces should still be there
    assert board.get(Point(1, 2)) == Player.white
    assert board.get(Point(2, 3)) == Player.white
    assert board.get(Point(2, 1)) == Player.white
    assert board.get(Point(3, 2)) == Player.white


def test_capture_multiple_stones():
    ascii_board = """
      A B C D E
    1 . W W . .
    2 W B B W .
    3 . W W . .
    4 . . . . .
    5 . . . . .
    """
    board = create_board_from_ascii(ascii_board)
    assert board.get(Point(2, 2)) is None
    assert board.get(Point(2, 3)) is None

    # White pieces should still be there
    assert board.get(Point(1, 2)) == Player.white
    assert board.get(Point(1, 3)) == Player.white
    assert board.get(Point(2, 1)) == Player.white
    assert board.get(Point(2, 4)) == Player.white
    assert board.get(Point(3, 2)) == Player.white
    assert board.get(Point(3, 3)) == Player.white


def test_get_go_string():
    ascii_board = """
      A B C D E
    1 . . . . .
    2 . B B . .
    3 . . . . .
    4 . . . . .
    5 . . . . .
    """
    board = create_board_from_ascii(ascii_board)
    go_string = board.get_go_string(Point(2, 2))
    assert isinstance(go_string, GoString)
    assert go_string.color == Player.black
    assert Point(2, 2) in go_string.stones
    assert Point(2, 3) in go_string.stones


def test_merge_go_strings():

    ascii_board = """
      A B C D E
    1 . . . . .
    2 . B B B .
    3 . . . . .
    4 . . . . .
    5 . . . . .
    """
    board = create_board_from_ascii(ascii_board)
    go_string = board.get_go_string(Point(2, 2))
    assert len(go_string.stones) == 3
    assert Point(2, 2) in go_string.stones
    assert Point(2, 3) in go_string.stones
    assert Point(2, 4) in go_string.stones


def test_liberty_count():
    ascii_board = """
      A B C D E
    1 . . . . .
    2 . B . . .
    3 . . . . .
    4 . . . . .
    5 . . . . .
    """
    board = create_board_from_ascii(ascii_board)
    go_string = board.get_go_string(Point(2, 2))
    assert go_string.num_liberties == 4

    board.place_stone(Player.black, Point(2, 1))
    go_string = board.get_go_string(Point(2, 2))
    assert go_string.num_liberties == 5


def create_board_with_stones():
    ascii_board = """
      A B C D E F G
    1 . . . . . . .
    2 . . B W . . .
    3 . B . . W . .
    4 . . B W . . .
    5 . . . . . . .
    6 . . . . . . .
    7 . . . . . . .
    """
    board = create_board_from_ascii(ascii_board)
    return board


def test_get_go_string_with_None_():
    board = Board(3, 3)

    go_string = board.get_go_string(None)

    assert go_string is None


def test_board_equality():
    # Create two boards with the same configuration
    board1 = create_board_with_stones()
    board2 = create_board_with_stones()

    # They should be equal
    assert board1 == board2, "Boards with the same configuration should be equal"

    # Add a stone to one board
    board1.place_stone(Player.black, Point(3, 3))

    # They should no longer be equal
    assert board1 != board2, "Boards with different configurations should not be equal"

    # Add the same stone to the second board
    board2.place_stone(Player.black, Point(3, 3))

    # They should be equal again
    assert board1 == board2, "Boards should be equal after adding the same stone"


def test_board_equality_with_different_order():
    board1 = create_board_with_stones()
    board2 = create_board_with_stones()

    # Add stones in different order
    board1.place_stone(Player.black, Point(3, 3))
    board1.place_stone(Player.white, Point(3, 4))

    board2.place_stone(Player.white, Point(3, 4))
    board2.place_stone(Player.black, Point(3, 3))

    # They should still be equal
    assert board1 == board2, "Boards should be equal regardless of the order of stone placement"


def test_board_inequality():
    board1 = create_board_with_stones()
    board2 = create_board_with_stones()

    # Add different stones
    board1.place_stone(Player.black, Point(3, 3))
    board2.place_stone(Player.white, Point(3, 3))

    # They should not be equal
    assert board1 != board2, "Boards with different stone colors at the same position should not be equal"


def test_board_equality_after_capture():
    board1 = Board(5, 5)
    board2 = Board(5, 5)

    # Set up a capture scenario
    for board in [board1, board2]:
        board.place_stone(Player.black, Point(2, 2))
        board.place_stone(Player.black, Point(3, 1))
        board.place_stone(Player.white, Point(1, 2))
        board.place_stone(Player.white, Point(2, 1))
        board.place_stone(Player.white, Point(2, 3))
        board.place_stone(Player.white, Point(3, 2))

    # Capture the black stone
    board1.place_stone(Player.white, Point(3, 3))
    board2.place_stone(Player.white, Point(3, 3))

    # They should be equal after capture
    assert board1 == board2, "Boards should be equal after the same capture occurs"
