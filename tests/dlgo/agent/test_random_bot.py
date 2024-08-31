"""
This file was initially generated using an AI language model (Claude 3.5 Sonnet),
as part of an educational project based on the book "Deep Learning and the Game of Go"
by Max Pumperla and Kevin Ferguson (Manning Publications, 2019).

The generated code has been reviewed, potentially modified, and adapted to fit the
project's requirements and to ensure correctness and adherence to the book's concepts.
"""

import pytest

from dlgo.agent.random_bot import RandomBot
from dlgo.gamestate import GameState
from dlgo.gotypes import Player, Point


@pytest.fixture
def game_state():
    # Initialize a game state with an empty 5x5 board.
    return GameState.new_game(5)


def test_select_move_empty_board(game_state):
    bot = RandomBot()
    move = bot.select_move(game_state)
    # We start with an empty board, so the first move is always valid.
    assert move.is_play
    assert game_state.is_valid_move(move), "The move selected should be valid."


def test_select_move_avoids_eyes(game_state, monkeypatch):
    bot = RandomBot()
    game_state = GameState.new_game(5)

    # Define a mock function to replace `is_point_an_eye`
    def mock_is_point_an_eye(board, point, player):
        return True  # Simulate that every point is an eye.

    # Use monkeypatch to replace `is_point_an_eye` in the bot's module
    monkeypatch.setattr("dlgo.agent.random_bot.is_point_an_eye", mock_is_point_an_eye)

    # Call the method under test
    move = bot.select_move(game_state)

    # Check if the bot chooses to pass
    assert move.is_pass, "The bot should pass if every point is an eye."


def test_select_move_when_no_valid_moves(game_state):
    bot = RandomBot()

    # Fill the board to make no moves valid.
    for r in range(1, game_state.board.num_rows + 1):
        for c in range(1, game_state.board.num_cols + 1):
            point = Point(row=r, col=c)
            game_state.board.place_stone(Player.black, point)

    move = bot.select_move(game_state)

    # Expect a pass move since there are no valid moves.
    assert move.is_pass, "The bot should pass if there are no valid moves."
