"""
This file is based on code from the book "Deep Learning and the Game of Go"
by Max Pumperla and Kevin Ferguson (Manning Publications, 2019).
Original code repository: https://github.com/maxpumperla/deep_learning_and_the_game_of_go

The code may have been modified and adapted for educational purposes.
"""

from __future__ import annotations

import copy
from typing import FrozenSet, List, Tuple

from dlgo.board import Board
from dlgo.gotypes import Player, Point
from dlgo.move import Move
from dlgo.scoring import compute_game_result


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
