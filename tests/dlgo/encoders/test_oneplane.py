"""
This file was initially generated using an AI language model (Claude 3.5 Sonnet),
as part of an educational project based on the book "Deep Learning and the Game of Go"
by Max Pumperla and Kevin Ferguson (Manning Publications, 2019).

The generated code has been reviewed, potentially modified, and adapted to fit the
project's requirements and to ensure correctness and adherence to the book's concepts.
"""

import numpy as np
import pytest
from utils.test_board_utils import create_board_from_ascii

from dlgo.encoders.base import Encoder
from dlgo.encoders.oneplane import OnePlaneEncoder
from dlgo.goboard_slow import Board, GameState
from dlgo.gotypes import Player, Point


@pytest.fixture
def encoder():
    return OnePlaneEncoder((19, 19))


@pytest.fixture
def small_encoder():
    return OnePlaneEncoder((5, 5))


@pytest.fixture
def game_state():
    board = Board(19, 19)
    # Place some stones
    board.place_stone(Player.black, Point(3, 3))
    board.place_stone(Player.white, Point(16, 16))
    game = GameState(board, Player.black, None, None)

    return game


def test_encoder_name(encoder):
    assert encoder.name() == "oneplane"


def test_encoder_shape(encoder):
    assert encoder.shape() == (1, 19, 19)


def test_small_encoder_shape(small_encoder):
    assert small_encoder.shape() == (1, 5, 5)


def test_num_points(encoder):
    # 361 = 19*19
    assert encoder.num_points() == 361


def test_encode(encoder, game_state):
    encoded_board = encoder.encode(game_state)
    assert encoded_board.shape == (1, 19, 19)
    assert encoded_board[0, 2, 2] == 1  # Black stone at (3, 3)
    assert encoded_board[0, 15, 15] == -1  # White stone at (16, 16)
    assert encoded_board[0, 0, 0] == 0  # Empty point


def test_encode_point(encoder):
    assert encoder.encode_point(Point(1, 1)) == 0
    assert encoder.encode_point(Point(1, 2)) == 1
    assert encoder.encode_point(Point(2, 1)) == 19
    assert encoder.encode_point(Point(19, 19)) == 360


def test_decode_point_index(encoder):
    assert encoder.decode_point_index(0) == Point(1, 1)
    assert encoder.decode_point_index(1) == Point(1, 2)
    assert encoder.decode_point_index(19) == Point(2, 1)
    assert encoder.decode_point_index(360) == Point(19, 19)


def test_encode_empty_board(encoder):
    empty_game = GameState.new_game(19)
    encoded_board = encoder.encode(empty_game)
    assert np.all(encoded_board == 0)


def test_encode_specific_pattern(small_encoder):
    """
    Test the encode method of OnePlaneEncoder with a specific pattern on a 5x5 board.

    This test creates a 5x5 Go board with a specific pattern:
    - The first column (A) is filled with black stones
    - The second column (B) is empty
    - The third column (C) is filled with white stones
    - The rest of the board is empty

    It then uses the encoder to encode this game state and verifies that the encoding is correct.

    The test checks:
    1. The first column is encoded as 1 (black stones)
    2. The second column is encoded as 0 (empty)
    3. The third column is encoded as -1 (white stones)
    4. The rest of the board is encoded as 0 (empty)

    Parameters:
    small_encoder (OnePlaneEncoder): An instance of the OnePlaneEncoder class for a 5x5 board.

    Raises:
    AssertionError: If the encoded board does not meet the expected criteria.

    Note:
    This test assumes that the encoder uses 1 for black stones, -1 for white stones,
    and 0 for empty points. The board is represented as a 3D numpy array with shape (1, 5, 5).
    """
    ascii_board = """
      A B C D E
    5 B . W . .
    4 B . W . .
    3 B . W . .
    2 B . W . .
    1 B . W . .
    """
    board = create_board_from_ascii(ascii_board)
    game = GameState(board, Player.black, None, None)
    encoded_board = small_encoder.encode(game)

    expected_encoding = np.array([[1, 0, -1, 0, 0], [1, 0, -1, 0, 0], [1, 0, -1, 0, 0], [1, 0, -1, 0, 0], [1, 0, -1, 0, 0]])

    assert encoded_board.shape == (1, 5, 5), "Encoded board should be 1x5x5"
    assert np.array_equal(encoded_board[0], expected_encoding), "Encoded board does not match the expected pattern"
    assert np.sum(encoded_board == 1) == 5, "Should have 5 black stones"
    assert np.sum(encoded_board == -1) == 5, "Should have 5 white stones"
    assert np.sum(encoded_board == 0) == 15, "Should have 15 empty points"


def test_different_board_sizes():
    encoders = [OnePlaneEncoder((5, 5)), OnePlaneEncoder((9, 9)), OnePlaneEncoder((19, 19))]
    for encoder in encoders:
        game = GameState.new_game(encoder.board_width)
        encoded_board = encoder.encode(game)
        assert encoded_board.shape == encoder.shape()
        assert np.all(encoded_board == 0)


def test_get_encoder_by_name():
    # Test with integer board size
    encoder = Encoder.get_encoder_by_name("oneplane", 19)
    assert isinstance(encoder, OnePlaneEncoder)
    assert encoder.board_width == 19
    assert encoder.board_height == 19

    # Test with tuple board size
    encoder = Encoder.get_encoder_by_name("oneplane", (13, 13))
    assert isinstance(encoder, OnePlaneEncoder)
    assert encoder.board_width == 13
    assert encoder.board_height == 13

    # Test with invalid encoder name
    with pytest.raises(ImportError):
        Encoder.get_encoder_by_name("invalid_encoder", 19)
