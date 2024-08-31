"""
This file was initially generated using an AI language model (Claude 3.5 Sonnet),
as part of an educational project based on the book "Deep Learning and the Game of Go"
by Max Pumperla and Kevin Ferguson (Manning Publications, 2019).

The generated code has been reviewed, potentially modified, and adapted to fit the
project's requirements and to ensure correctness and adherence to the book's concepts.
"""

import math
from typing import List
from unittest.mock import Mock, patch

import pytest

from dlgo.agent.mcts_agent import MCTSAgent, uct_score
from dlgo.gamestate import GameState
from dlgo.gotypes import Player, Point
from dlgo.move import Move
from misc.board_utils import create_board_from_ascii


def test_uct_score_typical_case():
    result = uct_score(parent_rollouts=100, child_rollouts=10, win_pct=0.6, temperature=1.0)
    expected = 0.6 + 1.0 * math.sqrt(math.log(100) / 10)
    assert math.isclose(result, expected, rel_tol=1e-9)


def test_uct_score_zero_temperature():
    result = uct_score(parent_rollouts=100, child_rollouts=10, win_pct=0.5, temperature=0.0)
    assert result == 0.5


def test_uct_score_high_temperature():
    result = uct_score(parent_rollouts=100, child_rollouts=10, win_pct=0.5, temperature=2.0)
    expected = 0.5 + 2.0 * math.sqrt(math.log(100) / 10)
    assert math.isclose(result, expected, rel_tol=1e-9)


def test_uct_score_equal_rollouts():
    result = uct_score(parent_rollouts=100, child_rollouts=100, win_pct=0.7, temperature=1.0)
    expected = 0.7 + 1.0 * math.sqrt(math.log(100) / 100)
    assert math.isclose(result, expected, rel_tol=1e-9)


def test_uct_score_large_numbers():
    result = uct_score(parent_rollouts=1000000, child_rollouts=100000, win_pct=0.9, temperature=0.5)
    expected = 0.9 + 0.5 * math.sqrt(math.log(1000000) / 100000)
    assert math.isclose(result, expected, rel_tol=1e-9)


def test_uct_score_win_pct_bounds():
    assert 0 <= uct_score(parent_rollouts=100, child_rollouts=10, win_pct=0.0, temperature=1.0) <= 1
    assert uct_score(parent_rollouts=100, child_rollouts=10, win_pct=1.0, temperature=1.0) > 1


def test_uct_score_error_child_rollouts_zero():
    with pytest.raises(AssertionError, match="child_rollouts must be positive, got 0"):
        uct_score(parent_rollouts=100, child_rollouts=0, win_pct=0.5, temperature=1.0)


def test_uct_score_error_parent_rollouts_zero():
    with pytest.raises(AssertionError, match="parent_rollouts must be positive, got 0"):
        uct_score(parent_rollouts=0, child_rollouts=10, win_pct=0.5, temperature=1.0)


def test_uct_score_error_negative_rollouts():
    with pytest.raises(AssertionError, match="parent_rollouts must be positive, got -1"):
        uct_score(parent_rollouts=-1, child_rollouts=10, win_pct=0.5, temperature=1.0)
    with pytest.raises(AssertionError, match="child_rollouts must be positive, got -1"):
        uct_score(parent_rollouts=100, child_rollouts=-1, win_pct=0.5, temperature=1.0)


def test_uct_score_error_invalid_win_pct():
    with pytest.raises(AssertionError, match="win_pct must be between 0 and 1, got -0.1"):
        uct_score(parent_rollouts=100, child_rollouts=10, win_pct=-0.1, temperature=1.0)
    with pytest.raises(AssertionError, match="win_pct must be between 0 and 1, got 1.1"):
        uct_score(parent_rollouts=100, child_rollouts=10, win_pct=1.1, temperature=1.0)


def test_uct_score_error_negative_temperature():
    with pytest.raises(AssertionError, match="temperature must be non-negative, got -1.0"):
        uct_score(parent_rollouts=100, child_rollouts=10, win_pct=0.5, temperature=-1.0)


class MockMCTSNode:
    def __init__(self, num_rollouts=100, winning_frac=0.5, move=None):
        self.num_rollouts = num_rollouts
        self._winning_frac = winning_frac
        self.move = move

    def winning_frac(self, player):
        return self._winning_frac

    def set_num_rollouts(self, num):
        self.num_rollouts = num

    def set_winning_frac(self, frac):
        self._winning_frac = frac


def test_pick_best_move_single_child():
    agent = MCTSAgent(num_rounds=10, temperature=0.8)
    children = [MockMCTSNode(move=Move.play(Point(1, 1)), winning_frac=0.7)]
    best_move = agent.pick_best_move(children, Player.black)
    assert best_move == Move.play(Point(1, 1))


def test_pick_best_move_multiple_children():
    agent = MCTSAgent(num_rounds=10, temperature=0.8)
    children = [
        MockMCTSNode(move=Move.play(Point(1, 1)), winning_frac=0.3),
        MockMCTSNode(move=Move.play(Point(2, 2)), winning_frac=0.5),
        MockMCTSNode(move=Move.play(Point(3, 3)), winning_frac=0.7),
    ]
    best_move = agent.pick_best_move(children, Player.black)
    assert best_move == Move.play(Point(3, 3))


def test_pick_best_move_tie():
    agent = MCTSAgent(num_rounds=10, temperature=0.8)
    children = [
        MockMCTSNode(move=Move.play(Point(1, 1)), winning_frac=0.5),
        MockMCTSNode(move=Move.play(Point(2, 2)), winning_frac=0.5),
    ]
    best_move = agent.pick_best_move(children, Player.black)
    assert best_move in [Move.play(Point(1, 1)), Move.play(Point(2, 2))]


def test_pick_best_move_no_children():
    agent = MCTSAgent(num_rounds=10, temperature=0.8)
    best_move = agent.pick_best_move([], Player.black)
    assert best_move is None


def test_pick_best_move_negative_fractions():
    agent = MCTSAgent(num_rounds=10, temperature=0.8)
    children = [
        MockMCTSNode(move=Move.play(Point(1, 1)), winning_frac=-0.1),
        MockMCTSNode(move=Move.play(Point(2, 2)), winning_frac=-0.2),
        MockMCTSNode(move=Move.play(Point(3, 3)), winning_frac=-0.05),
    ]
    best_move = agent.pick_best_move(children, Player.black)
    assert best_move == Move.play(Point(3, 3))


def test_pick_best_move_all_zero():
    agent = MCTSAgent(num_rounds=10, temperature=0.8)
    children = [
        MockMCTSNode(move=Move.play(Point(1, 1)), winning_frac=0),
        MockMCTSNode(move=Move.play(Point(2, 2)), winning_frac=0),
        MockMCTSNode(move=Move.play(Point(3, 3)), winning_frac=0),
    ]
    best_move = agent.pick_best_move(children, Player.black)
    assert best_move in [Move.play(Point(1, 1)), Move.play(Point(2, 2)), Move.play(Point(3, 3))]


def test_pick_best_move_different_players():
    agent = MCTSAgent(num_rounds=10, temperature=0.8)
    children = [
        MockMCTSNode(move=Move.play(Point(1, 1)), winning_frac=0.3),
        MockMCTSNode(move=Move.play(Point(2, 2)), winning_frac=0.5),
        MockMCTSNode(move=Move.play(Point(3, 3)), winning_frac=0.7),
    ]
    best_move_black = agent.pick_best_move(children, Player.black)
    best_move_white = agent.pick_best_move(children, Player.white)
    assert best_move_black == best_move_white == Move.play(Point(3, 3))


def test_select_child_single_child():
    agent = MCTSAgent(num_rounds=10, temperature=1.0)
    child = MockMCTSNode(num_rollouts=50, winning_frac=0.6)
    children = [child]

    with patch("dlgo.agent.mcts_agent.uct_score", return_value=0.8):
        selected = agent.select_child(children, Player.black, 1.0)

    assert selected == child


def test_select_child_multiple_children():
    agent = MCTSAgent(num_rounds=10, temperature=1.0)
    child1 = MockMCTSNode(num_rollouts=30, winning_frac=0.4)
    child2 = MockMCTSNode(num_rollouts=40, winning_frac=0.6)
    child3 = MockMCTSNode(num_rollouts=30, winning_frac=0.5)
    children = [child1, child2, child3]

    uct_scores = [0.7, 0.9, 0.8]
    with patch("dlgo.agent.mcts_agent.uct_score", side_effect=uct_scores):
        selected = agent.select_child(children, Player.black, 1.0)

    assert selected == child2


def test_select_child_no_children():
    agent = MCTSAgent(num_rounds=10, temperature=1.0)
    children = []

    selected = agent.select_child(children, Player.black, 1.0)

    assert selected is None


def test_select_child_equal_scores():
    agent = MCTSAgent(num_rounds=10, temperature=1.0)
    child1 = MockMCTSNode(num_rollouts=50, winning_frac=0.5)
    child2 = MockMCTSNode(num_rollouts=50, winning_frac=0.5)
    children = [child1, child2]

    with patch("dlgo.agent.mcts_agent.uct_score", return_value=0.8):
        selected = agent.select_child(children, Player.black, 1.0)

    assert selected in [child1, child2]


def test_select_child_different_rollouts():
    agent = MCTSAgent(num_rounds=10, temperature=1.0)
    child1 = MockMCTSNode(num_rollouts=10, winning_frac=0.6)
    child2 = MockMCTSNode(num_rollouts=90, winning_frac=0.5)
    children = [child1, child2]

    uct_scores = [0.9, 0.8]
    with patch("dlgo.agent.mcts_agent.uct_score", side_effect=uct_scores):
        selected = agent.select_child(children, Player.black, 1.0)

    assert selected == child1


def test_select_move_empty_board():
    ascii_board = """
      A B C
    1 . . .
    2 . . .
    3 . . .
    """
    board = create_board_from_ascii(ascii_board)
    game_state = GameState(board, Player.black, None, None)
    agent = MCTSAgent(num_rounds=10, temperature=1.0)

    with patch.object(MCTSAgent, "select_child", return_value=Mock()), patch.object(
        MCTSAgent, "simulate_random_game", return_value=Player.black
    ), patch.object(MCTSAgent, "pick_best_move", return_value=Move.play(Point(2, 2))):

        selected_move = agent.select_move(game_state)

    assert selected_move == Move.play(Point(2, 2))
