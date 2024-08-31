"""
This file is based on code from the book "Deep Learning and the Game of Go"
by Max Pumperla and Kevin Ferguson (Manning Publications, 2019).
Original code repository: https://github.com/maxpumperla/deep_learning_and_the_game_of_go

The code may have been modified and adapted for educational purposes.
"""

import time

from dlgo import agent, gotypes, utils
from dlgo.gamestate import GameState


def main():
    board_size = 9
    game = GameState.new_game(board_size)

    bots = {gotypes.Player.black: agent.random_bot.RandomBot(), gotypes.Player.white: agent.random_bot.RandomBot()}

    while not game.is_over():
        time.sleep(0.3)

        print(chr(27) + "[2J")
        utils.print_board(game.board)
        bot_move = bots[game.next_player].select_move(game)
        utils.print_move(game.next_player, bot_move)
        game = game.apply_move(bot_move)


if __name__ == "__main__":
    main()
