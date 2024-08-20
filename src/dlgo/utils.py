# Copied from https://github.com/maxpumperla/deep_learning_and_the_game_of_go/blob/master/code/dlgo/utils.py
"""
This file is based on code from the book "Deep Learning and the Game of Go"
by Max Pumperla and Kevin Ferguson (Manning Publications, 2019).
Original code repository: https://github.com/maxpumperla/deep_learning_and_the_game_of_go

The code may have been modified and adapted for educational purposes.
"""
from dlgo import gotypes

COLS = "ABCDEFGHJKLMNOPQRST"
STONE_TO_CHAR = {
    None: " . ",
    gotypes.Player.black: " B ",
    gotypes.Player.white: " W ",
}


def print_move(player, move):
    if move.is_pass:
        move_str = "passes"
    elif move.is_resign:
        move_str = "resigns"
    else:
        move_str = "%s%d" % (COLS[move.point.col - 1], move.point.row)
    print("%s %s" % (player, move_str))


def print_board(board):
    for row in range(board.num_rows, 0, -1):
        bump = " " if row <= 9 else ""
        line = []
        for col in range(1, board.num_cols + 1):
            stone = board.get_go_string_color(gotypes.Point(row=row, col=col))
            line.append(STONE_TO_CHAR[stone])
        print("%s%d %s" % (bump, row, "".join(line)))
    print("    " + "  ".join(COLS[: board.num_cols]))


# end::print_utils[]


def point_from_coords(coords):
    col = COLS.index(coords[0]) + 1
    row = int(coords[1:])
    return gotypes.Point(row=row, col=col)
