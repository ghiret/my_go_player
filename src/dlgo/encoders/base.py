"""
This file is based on code from the book "Deep Learning and the Game of Go"
by Max Pumperla and Kevin Ferguson (Manning Publications, 2019).
Original code repository: https://github.com/maxpumperla/deep_learning_and_the_game_of_go

The code may have been modified and adapted for educational purposes.
"""

import importlib

from dlgo.goboard_slow import GameState
from dlgo.gotypes import Point


class Encoder:
    def name(self):
        raise NotImplementedError()

    def encode(self, game_state: GameState):
        raise NotImplementedError()

    def encode_point(self, point: Point):
        raise NotImplementedError()

    def decode_point_index(self, index):
        raise NotImplementedError()

    def num_points(self):
        raise NotImplementedError()

    def shape(self):
        raise NotImplementedError()


def get_encoder_by_name(name, board_size):
    if isinstance(board_size, int):
        board_size = (board_size, board_size)
    module = importlib.import_module("dlgo.encoders." + name)
    constructor = getattr(module, "create")
    return constructor(board_size)
