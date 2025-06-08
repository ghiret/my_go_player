import numpy as np
import pytest

from scripts.generate_mcts_games import generate_game


def test_generate_game_invalid_board_size():
    with pytest.raises(ValueError):
        generate_game(7, 100, 60, 0.8)


def test_generate_game_invalid_rounds():
    with pytest.raises(ValueError):
        generate_game(9, 0, 60, 0.8)


def test_generate_game_invalid_max_moves():
    with pytest.raises(ValueError):
        generate_game(9, 100, 0, 0.8)


def test_generate_game_invalid_temperature():
    with pytest.raises(TypeError):
        generate_game(9, 100, 60, 0)
    with pytest.raises(ValueError):
        generate_game(9, 100, 60, 1.1)


def test_generate_game_invalid_types():
    with pytest.raises(TypeError):
        generate_game("9", 100, 60, 0.8)
    with pytest.raises(TypeError):
        generate_game(9, "100", 60, 0.8)
    with pytest.raises(TypeError):
        generate_game(9, 100, "60", 0.8)
    with pytest.raises(TypeError):
        generate_game(9, 100, 60, "0.8")


# Optionally, a smoke test for a very small game (board_size=5, rounds=1, max_moves=1)
def test_generate_game_smoke():
    boards, moves = generate_game(5, 1, 1, 0.8)
    assert isinstance(boards, np.ndarray)
    assert isinstance(moves, np.ndarray)
    # Should have at least one board and one move (or zero if game ends immediately)
    assert boards.shape[0] == moves.shape[0]
    assert boards.shape[1:] == (1, 5, 5)
    assert moves.shape[1] == 25
