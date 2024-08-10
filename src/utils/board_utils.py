from dlgo.goboard_slow import Board
from dlgo.gotypes import Player, Point


def create_board_from_ascii(ascii_board):
    lines = [line.strip() for line in ascii_board.strip().split("\n") if line.strip()]

    if len(lines) < 2:
        raise ValueError("Invalid board: not enough lines")

    # Remove the column numbers line if it exists
    if all(c.isdigit() or c.isspace() for c in lines[0]):
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
    print("  " + " ".join(str(i) for i in range(1, board_size + 1)))
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
