"""
This file was initially generated using an AI language model (Claude 3.5 Sonnet),
as part of an educational project based on the book "Deep Learning and the Game of Go"
by Max Pumperla and Kevin Ferguson (Manning Publications, 2019).

The generated code has been reviewed, potentially modified, and adapted to fit the
project's requirements and to ensure correctness and adherence to the book's concepts.
"""

import pytest

from dlgo.encoders.base import Encoder
from dlgo.goboard_slow import Board, GameState
from dlgo.gotypes import Player, Point


def test_encoder_methods():
    encoder = Encoder()

    with pytest.raises(NotImplementedError):
        encoder.name()

    with pytest.raises(NotImplementedError):
        board = Board(5, 5)
        game = GameState(board, Player.black, None, None)
        encoder.encode(game)

    with pytest.raises(NotImplementedError):
        encoder.encode_point(Point(1, 1))

    with pytest.raises(NotImplementedError):
        encoder.decode_point_index(0)

    with pytest.raises(NotImplementedError):
        encoder.num_points()

    with pytest.raises(NotImplementedError):
        encoder.shape()
