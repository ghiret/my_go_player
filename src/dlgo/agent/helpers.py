"""
This file is based on code from the book "Deep Learning and the Game of Go"
by Max Pumperla and Kevin Ferguson (Manning Publications, 2019).
Original code repository: https://github.com/maxpumperla/deep_learning_and_the_game_of_go

The code may have been modified and adapted for educational purposes.
"""

from dlgo.board import Board
from dlgo.gotypes import Point


def is_point_an_eye(board: Board, point: Point, color):
    if board.get_go_string_color(point) is not None:
        return False

    for neighbor in point.neighbors():
        if board.is_on_grid(neighbor):
            neighbor_color = board.get_go_string_color(neighbor)
            if neighbor_color != color:
                return False

    friendly_corners = 0
    off_board_corners = 0

    for corner in point.corners():
        if board.is_on_grid(corner):
            corner_color = board.get_go_string_color(corner)
            if corner_color == color:
                friendly_corners += 1
        else:
            off_board_corners += 1
    if off_board_corners > 0:
        return off_board_corners + friendly_corners == 4
    return friendly_corners >= 3
