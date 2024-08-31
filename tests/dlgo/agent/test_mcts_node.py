from typing import List

"""
This file was initially generated using an AI language model (Claude 3.5 Sonnet),
as part of an educational project based on the book "Deep Learning and the Game of Go"
by Max Pumperla and Kevin Ferguson (Manning Publications, 2019).

The generated code has been reviewed, potentially modified, and adapted to fit the
project's requirements and to ensure correctness and adherence to the book's concepts.
"""
from unittest.mock import Mock, patch

import pytest

from dlgo.agent.mcts_node import MCTSNode
from dlgo.board import Board
from dlgo.goboard_slow import GameState
from dlgo.gotypes import Player, Point
from dlgo.move import Move


@pytest.fixture
def game_state():
    board = Board(19, 19)
    return GameState.new_game(19)


@pytest.fixture
def mcts_node(game_state):
    return MCTSNode(game_state)


def test_init(game_state):
    node = MCTSNode(game_state)
    assert node.game_state == game_state
    assert node.parent is None
    assert node.move is None
    assert node.win_counts == {Player.black: 0, Player.white: 0}
    assert node.num_rollouts == 0
    assert isinstance(node.children, list)
    assert len(node.children) == 0
    assert isinstance(node.unvisited_moves, list)


def test_add_random_child(mcts_node):
    point = Point(3, 3)
    move = Move.play(point)
    mcts_node.unvisited_moves = [move]
    new_game_state = mcts_node.game_state.apply_move(move)

    child = mcts_node.add_random_child()

    assert isinstance(child, MCTSNode)
    assert child.parent == mcts_node
    assert child.move == move
    assert child.game_state.board == new_game_state.board
    assert child.game_state.next_player == new_game_state.next_player
    assert mcts_node.children == [child]
    assert mcts_node.unvisited_moves == []


def test_record_win(mcts_node):
    initial_black_wins = mcts_node.win_counts[Player.black]
    initial_white_wins = mcts_node.win_counts[Player.white]
    initial_rollouts = mcts_node.num_rollouts

    mcts_node.record_win(Player.black)
    assert mcts_node.win_counts[Player.black] == initial_black_wins + 1
    assert mcts_node.win_counts[Player.white] == initial_white_wins
    assert mcts_node.num_rollouts == initial_rollouts + 1

    mcts_node.record_win(Player.white)
    assert mcts_node.win_counts[Player.black] == initial_black_wins + 1
    assert mcts_node.win_counts[Player.white] == initial_white_wins + 1
    assert mcts_node.num_rollouts == initial_rollouts + 2


def test_can_add_child(mcts_node):
    mcts_node.unvisited_moves = []
    assert not mcts_node.can_add_child()

    mcts_node.unvisited_moves = [Move.play(Point(3, 3))]
    assert mcts_node.can_add_child()


def test_is_terminal(mcts_node):
    # Non-terminal state
    assert not mcts_node.is_terminal()

    # Terminal state (two consecutive passes)
    mcts_node.game_state = mcts_node.game_state.apply_move(Move.pass_turn())
    mcts_node.game_state = mcts_node.game_state.apply_move(Move.pass_turn())
    assert mcts_node.is_terminal()


def test_winning_frac(mcts_node):
    mcts_node.win_counts[Player.black] = 3
    mcts_node.win_counts[Player.white] = 7
    mcts_node.num_rollouts = 10

    assert mcts_node.winning_frac(Player.black) == 0.3
    assert mcts_node.winning_frac(Player.white) == 0.7
