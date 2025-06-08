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
    def __init__(self, board_size: tuple) -> None:
        """
        Initializes the encoder with the board size.
        :param board_size: An tuple representing the board dimensions.
        """
        self.board_width, self.board_height = board_size
        self.num_planes = 1

    def name(self) -> str:
        """
        Returns the name of the encoder.
        :return: A string representing the name of the encoder.
        """
        return "oneplane"

    def encode(self, game_state: GameState) -> np.ndarray:
        """
        Fill a matrix with 1s for the current player, -1 for the opponent's and 0 for empty spaces on the board
        :param game_state: The current state of the game.
        :return: A numpy array of shape (1,board_height, board_width) representing the board state.
        """
        board_matrix = np.zeros(self.shape())
        next_player = game_state.next_player

        # Iterate over all points on the board
        # and fill the matrix with 1s, -1s, or 0s
        # This could be done more efficiently with using the GoString objects.
        for row in range(self.board_width):
            for column in range(self.board_width):
                # Remember that the Point coordinates are 1-indexed
                # while the matrix is 0-indexed, so we add 1 to row and column
                p = Point(row=row + 1, col=column + 1)
                # Get the Go string at the point.
                # Remember the Go string is a contiguous group of stones of the same color.
                go_string = game_state.board.get_go_string(p)
                if go_string is None:
                    continue
                if go_string.color == next_player:
                    board_matrix[0, row, column] = 1
                else:
                    board_matrix[0, row, column] = -1
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

    def num_points(self) -> int:
        """
        Returns the total number of points on the board.
        :return: An int representing the total number of points on the board.
        """

        return self.board_width * self.board_height

    def shape(self) -> tuple:
        """
        Returns the shape of the encoded board.
        :return: A tuple representing the shape of the encoded board.
        """
        return self.num_planes, self.board_height, self.board_width


def create(board_size) -> OnePlaneEncoder:
    """
    Factory function to create an instance of OnePlaneEncoder.
    :param board_size: An int or tuple representing the board dimensions.
    :return: An instance of OnePlaneEncoder.
    """
    return OnePlaneEncoder(board_size)
