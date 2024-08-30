"""
This file is based on code from the book "Deep Learning and the Game of Go"
by Max Pumperla and Kevin Ferguson (Manning Publications, 2019).
Original code repository: https://github.com/maxpumperla/deep_learning_and_the_game_of_go

The code may have been modified and adapted for educational purposes.
"""

from __future__ import annotations

import copy

from dlgo.gotypes import Player, Point


class GoString:
    def __init__(self, color, stones, liberties):
        self.color = color
        self.stones = frozenset(stones)
        self.liberties = frozenset(liberties)

    def without_liberty(self, point: Point):
        if point not in self.liberties:
            raise ValueError(f"Point {point} is not a liberty of this string")
        new_liberties = self.liberties - set([point])

        return GoString(self.color, self.stones, new_liberties)

    def with_liberty(self, point: Point):
        new_liberties = self.liberties | set([point])
        return GoString(self.color, self.stones, new_liberties)

    def merged_with(self, go_string: GoString) -> GoString:
        if self.color != go_string.color:
            raise ValueError("Can only merge strings of the same color")
        combined_stones = self.stones | go_string.stones
        return GoString(
            self.color,
            set(combined_stones),
            set((self.liberties | go_string.liberties) - combined_stones),
        )

    @property
    def num_liberties(self) -> int:
        return len(self.liberties)

    def __eq__(self, other: object) -> bool:
        if not isinstance(other, GoString):
            return NotImplemented
        return self.color == other.color and self.stones == other.stones and self.liberties == other.liberties

    def __hash__(self) -> int:
        return hash((self.color, self.stones, self.liberties))
    

    def __deepcopy__(self, memodict={}):
        return GoString(self.color, self.stones, copy.deepcopy(self.liberties))