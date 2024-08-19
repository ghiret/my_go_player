# Copied from https://github.com/maxpumperla/deep_learning_and_the_game_of_go/blob/master/code/generate_zobrist.py
"""
This file is based on code from the book "Deep Learning and the Game of Go"
by Max Pumperla and Kevin Ferguson (Manning Publications, 2019).
Original code repository: https://github.com/maxpumperla/deep_learning_and_the_game_of_go

The code may have been modified and adapted for educational purposes.
"""
import random

from dlgo.gotypes import Player, Point


def to_python(player_state):
    if player_state is None:
        return "None"
    if player_state == Player.black:
        return Player.black
    return Player.white


MAX63 = 0x7FFFFFFFFFFFFFFF

table = {}
empty_board = 0
for row in range(1, 20):
    for col in range(1, 20):
        for state in (None, Player.black, Player.white):
            code = random.randint(0, MAX63)
            table[Point(row, col), state] = code

print("from .gotypes import Player, Point")
print("")
print("__all__ = ['HASH_CODE', 'EMPTY_BOARD']")
print("")
print("HASH_CODE = {")
for (pt, state), hash_code in table.items():
    print("    (%r, %s): %r," % (pt, to_python(state), hash_code))
print("}")
print("")
print("EMPTY_BOARD = %d" % random.randint(empty_board, MAX63))
# end::generate_zobrist[]
