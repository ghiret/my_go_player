"""
This file is based on code from the book "Deep Learning and the Game of Go"
by Max Pumperla and Kevin Ferguson (Manning Publications, 2019).
Original code repository: https://github.com/maxpumperla/deep_learning_and_the_game_of_go

The code may have been modified and adapted for educational purposes.
"""

from __future__ import annotations

import copy
from typing import FrozenSet, List, Optional, Tuple

import dlgo.zobrist as zobrist
from dlgo.gotypes import Player, Point
from dlgo.scoring import compute_game_result


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

    def __eq__(self, other: object) -> bool:
        if not isinstance(other, Move):
            return NotImplemented
        return (self.point, self.is_pass, self.is_resign) == (other.point, other.is_pass, other.is_resign)

    def __hash__(self) -> int:
        return hash((self.point, self.is_pass, self.is_resign))


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


class Board:
    def __init__(self, num_rows, num_cols):
        self.num_rows = num_rows
        self.num_cols = num_cols
        self._grid = {}
        self._hash = zobrist.EMPTY_BOARD

    def zobrist_hash(self):
        return self._hash

    def place_stone(self, player, point):
        """
        This function allows for self capture and it fails to recognise it.
        During normal game this will not be a problem because this will not be
        directly called, and GameState.apply_move checks for self-capture to reject the move
        """
        assert self.is_on_grid(point)
        assert self._grid.get(point) is None

        adjacent_same_color = []

        adjacent_opposite_color = []

        liberties = []

        for neighbor in point.neighbors():
            if not self.is_on_grid(neighbor):
                continue
            neighbor_string = self._grid.get(neighbor)

            if neighbor_string is None:
                liberties.append(neighbor)
            elif neighbor_string.color == player:
                if neighbor_string not in adjacent_same_color:
                    adjacent_same_color.append(neighbor_string)
            else:
                if neighbor_string not in adjacent_opposite_color:
                    adjacent_opposite_color.append(neighbor_string)

        new_string = GoString(player, [point], liberties)

        for same_color_string in adjacent_same_color:
            new_string = new_string.merged_with(same_color_string)
        for new_string_point in new_string.stones:
            self._grid[new_string_point] = new_string
        # Remove the None point and add the player color
        self._hash ^= zobrist.HASH_CODE[point, None]
        self._hash ^= zobrist.HASH_CODE[point, player]

        for other_color_string in adjacent_opposite_color:
            replacement = other_color_string.without_liberty(point)
            if replacement.num_liberties:
                self._replace_string(other_color_string.without_liberty(point))
            else:
                self._remove_string(other_color_string)

    def _replace_string(self, new_string: GoString):
        for point in new_string.stones:
            self._grid[point] = new_string

    def _remove_string(self, string):
        for point in string.stones:
            for neighbor in point.neighbors():
                neighbor_string = self._grid.get(neighbor)
                if neighbor_string is None:
                    continue
                if neighbor_string is not string:
                    self._replace_string(neighbor_string.with_liberty(point))
            self._grid.pop(point)
            # Remove the empty point and add the None point.
            self._hash ^= zobrist.HASH_CODE[point, string.color]
            self._hash ^= zobrist.HASH_CODE[point, None]

    def is_on_grid(self, point):
        return 1 <= point.row <= self.num_rows and 1 <= point.col <= self.num_cols

    def get_go_string_color(self, point):
        string = self._grid.get(point)
        if string is None:
            return None
        return string.color

    def get_go_string(self, point):
        string = self._grid.get(point)
        if string is None:
            return None
        return string

    def __eq__(self, other):
        return (
            isinstance(other, Board) and self.num_rows == other.num_rows and self.num_cols == other.num_cols and self._grid == other._grid
        )


class GameState:
    previous_states: FrozenSet[Tuple[Player, int]]  # Add type annotation

    def __init__(self, board: Board, next_player: Player, previous_gamestate: GameState, move: Move):
        self.board = board
        self.next_player = next_player
        self.previous_state = previous_gamestate

        if self.previous_state is None:
            self.previous_states = frozenset()
        else:
            self.previous_states = frozenset(
                previous_gamestate.previous_states
                # type: ignore[attr-defined]
                | {(previous_gamestate.next_player, previous_gamestate.board.zobrist_hash())}
            )
        self.last_move = move

    def apply_move(self, move: Move):
        if move.is_play:
            next_board = copy.deepcopy(self.board)
            next_board.place_stone(self.next_player, move.point)
        else:
            next_board = self.board
        return GameState(next_board, self.next_player.other, self, move)

    @classmethod
    def new_game(cls, board_size):
        if isinstance(board_size, int):
            board_size = (board_size, board_size)
        board = Board(*board_size)
        return GameState(board, Player.black, None, None)

    def is_move_self_capture(self, player: Player, move: Move):
        if not move.is_play:
            return False

        next_board = copy.deepcopy(self.board)
        next_board.place_stone(player, move.point)
        new_string = next_board.get_go_string(move.point)
        return new_string.num_liberties == 0

    @property
    def situation(self):
        return (self.next_player, self.board)

    def does_move_violate_ko(self, player: Player, move: Move):
        if not move.is_play:
            return False

        next_board = copy.deepcopy(self.board)
        next_board.place_stone(player, move.point)
        next_situation = (player.other, next_board.zobrist_hash())
        return next_situation in self.previous_states

    def is_valid_move(self, move: Move):
        if self.is_over():
            return False
        if move.is_pass or move.is_resign:
            return True

        return (
            self.board.get_go_string_color(move.point) is None
            and not self.does_move_violate_ko(self.next_player, move)
            and not self.is_move_self_capture(self.next_player, move)
        )

    def is_over(self):
        if self.last_move is None:
            return False
        if self.last_move.is_resign:
            return True

        if (second_last_move := self.previous_state.last_move) is None:
            return False
        return self.last_move.is_pass and second_last_move.is_pass

    def legal_moves(self) -> List[Move]:

        legal_moves = []
        for row in range(1, self.board.num_rows + 1):
            for col in range(1, self.board.num_cols + 1):
                point = Point(row, col)
                move = Move.play(point)
                if self.is_valid_move(move):
                    legal_moves.append(move)
        legal_moves.append(Move.pass_turn())
        legal_moves.append(Move.resign())
        return legal_moves

    def winner(self):
        if not self.is_over():
            return None
        if self.last_move.is_resign:
            return self.next_player
        game_result = compute_game_result(self)
        return game_result.winner
