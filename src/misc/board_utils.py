"""
This file was initially generated using an AI language model (Claude 3.5 Sonnet),
as part of an educational project based on the book "Deep Learning and the Game of Go"
by Max Pumperla and Kevin Ferguson (Manning Publications, 2019).

The generated code has been reviewed, potentially modified, and adapted to fit the
project's requirements and to ensure correctness and adherence to the book's concepts.
"""

import os

from dlgo.goboard_slow import Board
from dlgo.gotypes import Player, Point


def create_board_from_ascii(ascii_board):
    lines = [line.strip() for line in ascii_board.strip().split("\n") if line.strip()]

    if len(lines) < 2:
        raise ValueError("Invalid board: not enough lines")

    # Remove the column letters line if it exists
    if all(c.isalpha() or c.isspace() for c in lines[0]):
        lines = lines[1:]

    # Determine board size
    board_size = len(lines)

    board = Board(board_size, board_size)

    for row, line in enumerate(lines, start=1):
        # Split the line and remove the row number
        stones = line.split()[1:]

        if len(stones) != board_size:
            raise ValueError(f"Invalid board: inconsistent row length in row {row}")

        for col, stone in enumerate(stones, start=1):
            if stone == "B":
                board.place_stone(Player.black, Point(row, col))
            elif stone == "W":
                board.place_stone(Player.white, Point(row, col))
            elif stone != ".":
                raise ValueError(f"Invalid character '{stone}' at position ({row}, {col})")

    return board


def print_board(board):
    board_size = board.num_rows  # Assuming square board
    # Generate column labels (A-H, J-Z)
    column_labels = [chr(i) for i in range(ord("A"), ord("A") + board_size) if chr(i) != "I"]

    print("  " + " ".join(column_labels[:board_size]))
    for row in range(1, board_size + 1):
        line = f"{row} "
        for col in range(1, board_size + 1):
            point = Point(row, col)
            if board.get(point) == Player.black:
                line += "B "
            elif board.get(point) == Player.white:
                line += "W "
            else:
                line += ". "
        print(line.rstrip())  # Remove trailing whitespace


def debug_output(debug, state, message, output_dir, visualizer, move_number):
    print(f"\n{message}")
    print_board(state.board)

    if debug and visualizer:
        os.makedirs(output_dir, exist_ok=True)
        visualizer.visualize_game_state(
            state,
            os.path.join(output_dir, f"{move_number:02d}_{message.replace(' ', '_').lower()}.png"),
        )
