"""
This file is based on code from the book "Deep Learning and the Game of Go"
by Max Pumperla and Kevin Ferguson (Manning Publications, 2019).
Original code repository: https://github.com/maxpumperla/deep_learning_and_the_game_of_go

The code may have been modified and adapted for educational purposes.
"""

import numpy as np

from dlgo.encoders.base import Encoder
from dlgo.gamestate import GameState
from dlgo.gotypes import Point


class OnePlaneEncoder(Encoder):
    def __init__(self, board_size):
        self.board_width, self.board_height = board_size
        self.num_planes = 1

    def name(self):
        return "oneplane"

    def encode(self, game_state: GameState):
        """
        Fill a matrix with 1s for the current player, -1 for the opponent's and 0 for empty spaces on the board
        """
        board_matrix = np.zeros(self.shape())
        next_player = game_state.next_player

        for r in range(self.board_width):
            for c in range(self.board_width):
                p = Point(row=r + 1, col=c + 1)
                go_string = game_state.board.get_go_string(p)
                if go_string is None:
                    continue
                if go_string.color == next_player:
                    board_matrix[0, r, c] = 1
                else:
                    board_matrix[0, r, c] = -1
        return board_matrix

    def encode_point(self, point: Point):
        """
        Transforms from Point coordinates col and row into the index of a contiguous vector
        This assume valid inputs and no checks are performed on the validity of the inputs."""
        return self.board_width * (point.row - 1) + (point.col - 1)

    def decode_point_index(self, index):
        """
        Assumes the points are stored in a vector and returns the Point for a given index.
        This assumes valid inputs and no checks are performed on the validity of the inputs."""
        row = index // self.board_width
        col = index % self.board_width
        return Point(row=row + 1, col=col + 1)

    def num_points(self):
        return self.board_width * self.board_height

    def shape(self):
        return self.num_planes, self.board_height, self.board_width


def create(board_size):
    return OnePlaneEncoder(board_size)
