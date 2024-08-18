import math
from typing import List, Optional

import pytest

from dlgo.agent.mcts_agent import MCTSAgent, uct_score
from dlgo.goboard_slow import Move
from dlgo.gotypes import Player, Point


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
    def __init__(self, winning_frac: float, move: Optional[Move] = None):
        self.winning_frac_value = winning_frac
        self.move = move

    def winning_frac(self, player: Player) -> float:
        return self.winning_frac_value


def test_pick_best_move_single_child():
    agent = MCTSAgent(num_rounds=10, temperature=0.8)
    children = [MockMCTSNode(0.7, Move.play(Point(1, 1)))]
    best_move = agent.pick_best_move(children, Player.black)
    assert best_move == Move.play(Point(1, 1))


def test_pick_best_move_multiple_children():
    agent = MCTSAgent(num_rounds=10, temperature=0.8)
    children = [
        MockMCTSNode(0.3, Move.play(Point(1, 1))),
        MockMCTSNode(0.5, Move.play(Point(2, 2))),
        MockMCTSNode(0.7, Move.play(Point(3, 3))),
    ]
    best_move = agent.pick_best_move(children, Player.black)
    assert best_move == Move.play(Point(3, 3))


def test_pick_best_move_tie():
    agent = MCTSAgent(num_rounds=10, temperature=0.8)
    children = [
        MockMCTSNode(0.5, Move.play(Point(1, 1))),
        MockMCTSNode(0.5, Move.play(Point(2, 2))),
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
        MockMCTSNode(-0.1, Move.play(Point(1, 1))),
        MockMCTSNode(-0.2, Move.play(Point(2, 2))),
        MockMCTSNode(-0.05, Move.play(Point(3, 3))),
    ]
    best_move = agent.pick_best_move(children, Player.black)
    assert best_move == Move.play(Point(3, 3))


def test_pick_best_move_all_zero():
    agent = MCTSAgent(num_rounds=10, temperature=0.8)
    children = [
        MockMCTSNode(0, Move.play(Point(1, 1))),
        MockMCTSNode(0, Move.play(Point(2, 2))),
        MockMCTSNode(0, Move.play(Point(3, 3))),
    ]
    best_move = agent.pick_best_move(children, Player.black)
    assert best_move in [Move.play(Point(1, 1)), Move.play(Point(2, 2)), Move.play(Point(3, 3))]


def test_pick_best_move_different_players():
    agent = MCTSAgent(num_rounds=10, temperature=0.8)
    children = [
        MockMCTSNode(0.3, Move.play(Point(1, 1))),
        MockMCTSNode(0.5, Move.play(Point(2, 2))),
        MockMCTSNode(0.7, Move.play(Point(3, 3))),
    ]
    best_move_black = agent.pick_best_move(children, Player.black)
    best_move_white = agent.pick_best_move(children, Player.white)
    assert best_move_black == best_move_white == Move.play(Point(3, 3))
