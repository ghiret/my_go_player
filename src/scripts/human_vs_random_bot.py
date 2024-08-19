"""
This file is based on code from the book "Deep Learning and the Game of Go"
by Max Pumperla and Kevin Ferguson (Manning Publications, 2019).
Original code repository: https://github.com/maxpumperla/deep_learning_and_the_game_of_go

The code may have been modified and adapted for educational purposes.
"""

import time

from dlgo import agent
from dlgo import goboard_slow as goboard
from dlgo import gotypes, utils


def main():
    board_size = 9
    game = goboard.GameState.new_game(board_size)
    bot = agent.random_bot.RandomBot()

    while not game.is_over():
        time.sleep(0.3)

        print(chr(27) + "[2J")
        utils.print_board(game.board)
        if game.next_player == gotypes.Player.black:
            human_move = input("-- ")
            point = utils.point_from_coords(human_move.strip())
            move = goboard.Move.play(point)
        else:
            move = bot.select_move(game)
        utils.print_move(game.next_player, move)
        game = game.apply_move(move)


if __name__ == "__main__":
    main()
