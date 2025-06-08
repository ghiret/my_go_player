"""
This file is based on code from the book "Deep Learning and the Game of Go"
by Max Pumperla and Kevin Ferguson (Manning Publications, 2019).
Original code repository: https://github.com/maxpumperla/deep_learning_and_the_game_of_go

The code may have been modified and adapted for educational purposes.
"""

import argparse

import numpy as np

from dlgo import gamestate as goboard
from dlgo.agent import mcts_agent
from dlgo.encoders.base import get_encoder_by_name
from dlgo.utils import print_board, print_move


def generate_game(board_size: int, rounds: int, max_moves: int, temperature: float) -> tuple:
    """
    Generate a single game using MCTS.
    Args:
        board_size (int): Size of the Go board (e.g., 9, 13, 19).
        rounds (int): Number of MCTS rounds to simulate for each move.
        max_moves (int): Maximum number of moves in the game.
        temperature (float): Temperature parameter for MCTS exploration.
    Returns:
        tuple: A tuple containing two numpy arrays:
            - boards: Encoded board states.
            - moves: One-hot encoded moves corresponding to the board states.
    """
    if not isinstance(board_size, int):
        raise TypeError("Board size must be an integer.")
    if not isinstance(rounds, int) or not isinstance(max_moves, int):
        raise TypeError("Rounds and max_moves must be integers.")
    if not isinstance(temperature, float):
        raise TypeError("Temperature must be a float.")
    if board_size not in [5, 9, 13, 19]:
        raise ValueError("Board size must be one of 5, 9, 13, or 19.")
    if rounds <= 0:
        raise ValueError("Number of rounds must be a positive integer.")
    if temperature <= 0 or temperature > 1:
        raise ValueError("Temperature must be in the range (0, 1].")
    if max_moves <= 0:
        raise ValueError("Maximum moves must be a positive integer.")

    boards, moves = [], []

    encoder = get_encoder_by_name("oneplane", board_size)

    game = goboard.GameState.new_game(board_size)

    bot = mcts_agent.MCTSAgent(rounds, temperature)

    num_moves = 0

    while not game.is_over():
        print_board(game.board)
        move = bot.select_move(game)
        print(move)
        if move.is_play:
            boards.append(encoder.encode(game))

            move_one_hot = np.zeros(encoder.num_points())
            move_one_hot[encoder.encode_point(move.point)] = 1
            moves.append(move_one_hot)
        print_move(game.next_player, move)
        game = game.apply_move(move)

        num_moves += 1

        if num_moves > max_moves:
            break

    return np.array(boards), np.array(moves)


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("--board-size", "-b", type=int, default=9)
    parser.add_argument("--rounds", "-r", type=int, default=1000)
    parser.add_argument("--temperature", "-t", type=float, default=0.8)
    parser.add_argument("--max-moves", "-m", type=int, default=60, help="Max moves per game")
    parser.add_argument("--num-games", "-n", type=int, default=10)
    parser.add_argument("--board-out")
    parser.add_argument("--move-out")

    args = parser.parse_args()

    # X correspondes to the board states, Y to the moves
    # When we train a model X is the input and Y is the label to be predicted.
    xs = []
    ys = []

    for i in range(args.num_games):
        print(f"Generating game {i+1}/{args.num_games}...")
        x, y = generate_game(args.board_size, args.rounds, args.max_moves, args.temperature)
        xs.append(x)
        ys.append(y)

    x = np.concatenate(xs)
    y = np.concatenate(ys)

    np.save(args.board_out, x)
    np.save(args.move_out, y)


if __name__ == "__main__":
    print(f"Running a game generation sequence")
    main()
