"""
This file is based on code from the book "Deep Learning and the Game of Go"
by Max Pumperla and Kevin Ferguson (Manning Publications, 2019).
Original code repository: https://github.com/maxpumperla/deep_learning_and_the_game_of_go

The code may have been modified and adapted for educational purposes.
"""

from __future__ import annotations

import copy
from typing import FrozenSet, List, Optional, Tuple

from dlgo.gotypes import Player, Point


class Move:
    def __init__(self, point: Optional[Point] = None, is_pass: bool = False, is_resign: bool = False):
        assert (point is not None) ^ is_pass ^ is_resign
        self.point = point
        self.is_play = self.point is not None
        self.is_pass = is_pass
        self.is_resign = is_resign

    @classmethod
    def play(cls, point: Point) -> Move:
        return Move(point=point)

    @classmethod
    def pass_turn(cls) -> Move:
        return Move(is_pass=True)

    @classmethod
    def resign(cls) -> Move:
        return Move(is_resign=True)

    def __str__(self):
        if self.is_pass:
            return "pass"
        if self.is_resign:
            return "resign"
        return "(r %d, c %d)" % (self.point.row, self.point.col)

    def __hash__(self) -> int:
        return hash((self.point, self.is_pass, self.is_resign))

    def __eq__(self, other: object) -> bool:
        if not isinstance(other, Move):
            return NotImplemented
        return (self.point, self.is_pass, self.is_resign) == (other.point, other.is_pass, other.is_resign)
