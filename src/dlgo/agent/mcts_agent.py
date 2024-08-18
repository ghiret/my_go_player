import math
from typing import List

from dlgo.agent import base
from dlgo.agent.mcts_node import MCTSNode
from dlgo.goboard_slow import GameState
from dlgo.gotypes import Player


def uct_score(parent_rollouts, child_rollouts, win_pct, temperature):
    assert parent_rollouts > 0, f"parent_rollouts must be positive, got {parent_rollouts}"
    assert child_rollouts > 0, f"child_rollouts must be positive, got {child_rollouts}"
    assert 0 <= win_pct <= 1, f"win_pct must be between 0 and 1, got {win_pct}"
    assert temperature >= 0, f"temperature must be non-negative, got {temperature}"
    exploration = math.sqrt(math.log(parent_rollouts) / child_rollouts)
    return win_pct + temperature * exploration


class MCTSAgent(base.Agent):
    def __init__(self, num_rounds: int = 1000, temperature: float = 0.8):
        base.Agent.__init__(self)
        self.num_rounds = num_rounds
        self.temperature = temperature

    def pick_best_move(self, children: List[MCTSNode], next_player: Player):
        # Pick a move after having done num_rounds
        best_move = None
        best_pct = -1.0

        for child in children:
            child_pct = child.winning_frac(next_player)
            if child_pct > best_pct:
                best_pct = child_pct
                best_move = child.move
        return best_move

    def select_move(self, game_state: GameState):
        root = MCTSNode(game_state)

        # MCTS Search
        for i in range(self.num_rounds):
            node = root

            # Traverse the tree until a leaf is found
            while (not node.can_add_child()) and (not node.is_terminal()):
                node = self.select_child(node)

            # After a leaf has been found, add a new node.
            if node.can_add_child():
                node = node.add_random_child()

            winner = self.simulate_random_game(node.game_state)
            # Propagate the result upwards
            while node is not None:
                node.record_win(winner)
                node = node.parent  # type: ignore

        return self.pick_best_move(root.children, game_state.next_player)

    def select_child(self, node: MCTSNode):
        total_rollouts = sum(child.num_rollouts for child in node.children)

        best_score = -1

        best_child = None

        for child in node.children:
            score = uct_score(total_rollouts, child.num_rollouts, child.winning_frac(node.game_state.next_player), self.temperature)
            if score > best_score:
                best_score = score
                best_child = child
        return best_child

    def simulate_random_game(self, game_state):
        pass
