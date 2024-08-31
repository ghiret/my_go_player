"""
This file is based on code from the book "Deep Learning and the Game of Go"
by Max Pumperla and Kevin Ferguson (Manning Publications, 2019).
Original code repository: https://github.com/maxpumperla/deep_learning_and_the_game_of_go

The code may have been modified and adapted for educational purposes.
"""

import random
from typing import TYPE_CHECKING, List, Optional

from dlgo.gamestate import GameState
from dlgo.move import Move
from dlgo.gotypes import Player


class MCTSNode(object):
    def __init__(self, game_state: GameState, parent: Optional["MCTSNode"] = None, move: Optional[Move] = None):
        self.game_state = game_state
        self.parent = parent
        self.move = move

        self.win_counts = {Player.black: 0, Player.white: 0}
        # Roll-outs counter, should amount to all the win_counts.
        self.num_rollouts = 0
        self.children: List["MCTSNode"] = []
        self.unvisited_moves = game_state.legal_moves()

    def add_random_child(self) -> "MCTSNode":
        index = random.randint(0, len(self.unvisited_moves) - 1)
        new_move = self.unvisited_moves.pop(index)
        new_game_state = self.game_state.apply_move(new_move)
        new_node = MCTSNode(new_game_state, self, new_move)
        self.children.append(new_node)
        return new_node

    def record_win(self, winner):
        self.win_counts[winner] += 1
        self.num_rollouts += 1

    def can_add_child(self):
        return len(self.unvisited_moves) > 0

    def is_terminal(self):
        return self.game_state.is_over()

    def winning_frac(self, player):
        return float(self.win_counts[player]) / float(self.num_rollouts)
