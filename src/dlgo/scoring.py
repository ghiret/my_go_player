# Copied from https://github.com/maxpumperla/deep_learning_and_the_game_of_go/blob/master/code/dlgo/scoring.py
"""
This file is based on code from the book "Deep Learning and the Game of Go"
by Max Pumperla and Kevin Ferguson (Manning Publications, 2019).
Original code repository: https://github.com/maxpumperla/deep_learning_and_the_game_of_go

The code may have been modified and adapted for educational purposes.
"""
from __future__ import absolute_import

from collections import namedtuple

from dlgo.gotypes import Player, Point


class Territory:
    # A `territory_map` splits the board into stones, territory and neutral points (dame).
    def __init__(self, territory_map):
        self.num_black_territory = 0
        self.num_white_territory = 0
        self.num_black_stones = 0
        self.num_white_stones = 0
        self.num_dame = 0
        self.dame_points = []
        # Depending on the status of a point, we increment the respective counter.
        for point, status in territory_map.items():
            if status == Player.black:
                self.num_black_stones += 1
            elif status == Player.white:
                self.num_white_stones += 1
            elif status == "territory_b":
                self.num_black_territory += 1
            elif status == "territory_w":
                self.num_white_territory += 1
            elif status == "dame":
                self.num_dame += 1
                self.dame_points.append(point)


class GameResult(namedtuple("GameResult", "b w komi")):
    @property
    def winner(self):
        if self.b > self.w + self.komi:
            return Player.black
        return Player.white

    @property
    def winning_margin(self):
        w = self.w + self.komi
        return abs(self.b - w)

    def __str__(self):
        w = self.w + self.komi
        if self.b > w:
            return "B+%.1f" % (self.b - w,)
        return "W+%.1f" % (w - self.b,)


def evaluate_territory(board):
    """evaluate_territory:
    Map a board into territory and dame.

    Any points that are completely surrounded by a single color are
    counted as territory; it makes no attempt to identify even
    trivially dead groups.
    """

    status = {}
    for r in range(1, board.num_rows + 1):
        for c in range(1, board.num_cols + 1):
            p = Point(row=r, col=c)
            # Skip the point, if you already visited this as part of a different group.
            if p in status:
                continue
            stone = board.get_go_string_color(p)
            # If the point is a stone, add it as status.
            if stone is not None:
                status[p] = stone
            else:
                group, neighbors = _collect_region(p, board)
                # If a point is completely surrounded by black or white stones, count it as territory.
                if len(neighbors) == 1:
                    neighbor_stone = neighbors.pop()
                    stone_str = "b" if neighbor_stone == Player.black else "w"
                    fill_with = "territory_" + stone_str
                else:
                    # Otherwise the point has to be a neutral point, so we add it to dame.
                    fill_with = "dame"
                for pos in group:
                    status[pos] = fill_with
    return Territory(status)


def _collect_region(start_pos: Point, board, visited=None):
    """_collect_region:

    Find the contiguous section of a board containing a point. Also
    identify all the boundary points.
    """

    if visited is None:
        visited = {}
    if start_pos in visited:
        return [], set()
    all_points = [start_pos]
    all_borders = set()
    visited[start_pos] = True
    # This returns the color of the piece or None if no piece is placed here.
    here = board.get_go_string_color(start_pos)

    deltas = [(-1, 0), (1, 0), (0, -1), (0, 1)]
    for delta_r, delta_c in deltas:
        next_p = Point(row=start_pos.row + delta_r, col=start_pos.col + delta_c)
        if not board.is_on_grid(next_p):
            continue
        neighbor = board.get_go_string_color(next_p)
        # Check if the neighbor is the same color as the starting position
        if neighbor == here:
            points, borders = _collect_region(next_p, board, visited)
            all_points += points
            all_borders |= borders
        else:
            all_borders.add(neighbor)
    return all_points, all_borders


def compute_game_result(game_state):
    territory = evaluate_territory(game_state.board)
    return GameResult(
        territory.num_black_territory + territory.num_black_stones, territory.num_white_territory + territory.num_white_stones, komi=7.5
    )
