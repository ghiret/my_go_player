"""
This file was initially generated using an AI language model (Claude 3.5 Sonnet),
as part of an educational project based on the book "Deep Learning and the Game of Go"
by Max Pumperla and Kevin Ferguson (Manning Publications, 2019).

The generated code has been reviewed, potentially modified, and adapted to fit the
project's requirements and to ensure correctness and adherence to the book's concepts.
"""

from unittest.mock import Mock, patch

import pytest

from dlgo.gotypes import Player, Point
from dlgo.scoring import GameResult, Territory, _collect_region, compute_game_result
from misc.board_utils import create_board_from_ascii


def test_empty_territory():
    territory_map = {}
    territory = Territory(territory_map)
    assert territory.num_black_territory == 0
    assert territory.num_white_territory == 0
    assert territory.num_black_stones == 0
    assert territory.num_white_stones == 0
    assert territory.num_dame == 0
    assert territory.dame_points == []


def test_only_stones():
    territory_map = {
        Point(1, 1): Player.black,
        Point(1, 2): Player.white,
        Point(2, 1): Player.black,
        Point(2, 2): Player.white,
    }
    territory = Territory(territory_map)
    assert territory.num_black_territory == 0
    assert territory.num_white_territory == 0
    assert territory.num_black_stones == 2
    assert territory.num_white_stones == 2
    assert territory.num_dame == 0
    assert territory.dame_points == []


def test_only_territory():
    territory_map = {
        Point(1, 1): "territory_b",
        Point(1, 2): "territory_w",
        Point(2, 1): "territory_b",
        Point(2, 2): "territory_w",
    }
    territory = Territory(territory_map)
    assert territory.num_black_territory == 2
    assert territory.num_white_territory == 2
    assert territory.num_black_stones == 0
    assert territory.num_white_stones == 0
    assert territory.num_dame == 0
    assert territory.dame_points == []


def test_only_dame():
    territory_map = {
        Point(1, 1): "dame",
        Point(1, 2): "dame",
        Point(2, 1): "dame",
        Point(2, 2): "dame",
    }
    territory = Territory(territory_map)
    assert territory.num_black_territory == 0
    assert territory.num_white_territory == 0
    assert territory.num_black_stones == 0
    assert territory.num_white_stones == 0
    assert territory.num_dame == 4
    assert set(territory.dame_points) == {Point(1, 1), Point(1, 2), Point(2, 1), Point(2, 2)}


def test_mixed_territory():
    territory_map = {
        Point(1, 1): Player.black,
        Point(1, 2): "territory_b",
        Point(2, 1): Player.white,
        Point(2, 2): "territory_w",
        Point(3, 1): "dame",
        Point(3, 2): "dame",
    }
    territory = Territory(territory_map)
    assert territory.num_black_territory == 1
    assert territory.num_white_territory == 1
    assert territory.num_black_stones == 1
    assert territory.num_white_stones == 1
    assert territory.num_dame == 2
    assert set(territory.dame_points) == {Point(3, 1), Point(3, 2)}


def test_large_territory():
    territory_map = {
        Point(i, j): status
        for i in range(1, 10)
        for j in range(1, 10)
        for status in [Player.black, Player.white, "territory_b", "territory_w", "dame"]
    }
    territory = Territory(territory_map)
    assert (
        territory.num_black_territory
        + territory.num_white_territory
        + territory.num_black_stones
        + territory.num_white_stones
        + territory.num_dame
        == 81
    )


def test_black_wins():
    result = GameResult(b=72, w=70, komi=0.5)
    assert result.winner == Player.black
    assert result.winning_margin == 1.5
    assert str(result) == "B+1.5"


def test_white_wins():
    result = GameResult(b=60, w=65, komi=0.5)
    assert result.winner == Player.white
    assert result.winning_margin == 5.5
    assert str(result) == "W+5.5"


def test_tie_white_wins():
    result = GameResult(b=70, w=70, komi=0.5)
    assert result.winner == Player.white
    assert result.winning_margin == 0.5
    assert str(result) == "W+0.5"


def test_large_komi():
    result = GameResult(b=100, w=50, komi=50.5)
    assert result.winner == Player.white
    assert result.winning_margin == 0.5
    assert str(result) == "W+0.5"


def test_zero_komi():
    result = GameResult(b=75, w=75, komi=0)
    assert result.winner == Player.white
    assert result.winning_margin == 0
    assert str(result) == "W+0.0"


def test_negative_komi():
    result = GameResult(b=60, w=70, komi=-6.5)
    assert result.winner == Player.white
    assert result.winning_margin == 3.5
    assert str(result) == "W+3.5"


def test_large_score_difference():
    result = GameResult(b=100, w=20, komi=0.5)
    assert result.winner == Player.black
    assert result.winning_margin == 79.5
    assert str(result) == "B+79.5"


def test_exact_tie():
    result = GameResult(b=50, w=49, komi=1.0)
    assert result.winner == Player.white
    assert result.winning_margin == 0
    assert str(result) == "W+0.0"


@pytest.mark.parametrize(
    "b, w, komi, expected_winner, expected_margin, expected_str",
    [
        (72, 70, 0.5, Player.black, 1.5, "B+1.5"),
        (60, 65, 0.5, Player.white, 5.5, "W+5.5"),
        (70, 70, 0.5, Player.white, 0.5, "W+0.5"),
        (100, 50, 50.5, Player.white, 0.5, "W+0.5"),
        (75, 75, 0, Player.white, 0, "W+0.0"),
        (100, 20, 0.5, Player.black, 79.5, "B+79.5"),
        (50, 49, 1.0, Player.white, 0, "W+0.0"),
    ],
)
def test_game_result_parametrized(b, w, komi, expected_winner, expected_margin, expected_str):
    result = GameResult(b=b, w=w, komi=komi)
    assert result.winner == expected_winner
    assert result.winning_margin == expected_margin
    assert str(result) == expected_str


@pytest.fixture
def mock_game_state():
    return Mock()


def test_compute_game_result():
    mock_game_state = Mock()
    mock_territory = Mock()
    mock_territory.num_black_territory = 10
    mock_territory.num_black_stones = 5
    mock_territory.num_white_territory = 8
    mock_territory.num_white_stones = 4

    with patch("dlgo.scoring.evaluate_territory", return_value=mock_territory):
        result = compute_game_result(mock_game_state)

    assert isinstance(result, GameResult)
    assert result.b == 15  # 10 territory + 5 stones
    assert result.w == 12  # 8 territory + 4 stones
    assert result.komi == 7.5
    assert result.winner == Player.white  # White wins due to komi
    assert result.winning_margin == 4.5
    assert str(result) == "W+4.5"


def test_compute_game_result_calls_evaluate_territory():
    mock_game_state = Mock()
    mock_territory = Mock()
    mock_territory.num_black_territory = 0
    mock_territory.num_black_stones = 0
    mock_territory.num_white_territory = 0
    mock_territory.num_white_stones = 0

    with patch("dlgo.scoring.evaluate_territory", return_value=mock_territory) as mock_evaluate:
        compute_game_result(mock_game_state)

    mock_evaluate.assert_called_once_with(mock_game_state.board)


def test_collect_single_stone():
    board = create_board_from_ascii(
        """
      A B C
    1 . . .
    2 . B .
    3 . . .
    """
    )
    points, borders = _collect_region(Point(2, 2), board)
    assert points == [Point(2, 2)]
    assert borders == {None, None, None, None}


def test_collect_multiple_stones():
    board = create_board_from_ascii(
        """
      A B C D
    1 . . . .
    2 . B B .
    3 . B B .
    4 . . . .
    """
    )
    points, borders = _collect_region(Point(2, 2), board)
    assert set(points) == {Point(2, 2), Point(2, 3), Point(3, 2), Point(3, 3)}

    assert borders == {None}


def test_collect_with_borders():
    board = create_board_from_ascii(
        """
      A B C D
    1 . W . .
    2 W B B .
    3 . B B .
    4 . . W .
    """
    )
    points, borders = _collect_region(Point(2, 2), board)
    assert set(points) == {Point(2, 2), Point(2, 3), Point(3, 2), Point(3, 3)}
    assert borders == {Player.white, None}


def test_collect_at_edge():
    board = create_board_from_ascii(
        """
      A B C
    1 B B .
    2 B B .
    3 . . .
    """
    )
    points, borders = _collect_region(Point(1, 1), board)
    assert set(points) == {Point(1, 1), Point(1, 2), Point(2, 1), Point(2, 2)}
    assert borders == {None}


def test_collect_surrounded():
    board = create_board_from_ascii(
        """
      A B C
    1 . W .
    2 W B W
    3 . W .
    """
    )
    points, borders = _collect_region(Point(2, 2), board)
    assert points == [Point(2, 2)]
    assert borders == {Player.white}


def test_collect_large_region():
    board = create_board_from_ascii(
        """
      A B C D E
    1 B . . . .
    2 B B . . .
    3 B B B . .
    4 B B B B .
    5 B B B B B
    """
    )
    points, borders = _collect_region(Point(1, 1), board)
    assert len(points) == 15  # Sum of 1 to 5
    assert None in borders  # Edge of the board
    assert Player.black not in borders


def test_revisit_point():
    board = create_board_from_ascii(
        """
      A B C
    1 B B .
    2 B B .
    3 . . .
    """
    )
    visited = {Point(1, 1): True}
    points, borders = _collect_region(Point(2, 2), board, visited)
    assert set(points) == {Point(2, 2), Point(1, 2), Point(2, 1)}
    assert borders == {None}
    assert Point(1, 1) not in points


def test_collect_empty_region():
    board = create_board_from_ascii(
        """
      A B C
    1 . . .
    2 . . .
    3 . . .
    """
    )
    points, borders = _collect_region(Point(2, 2), board)

    assert len(points) == 9
    assert borders == set()
