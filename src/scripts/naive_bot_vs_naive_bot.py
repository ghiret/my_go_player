import time

from dlgo import agent
from dlgo import goboard_slow as goboard
from dlgo import gotypes, utils


def main():
    board_size = 9
    game = goboard.Gamestate.new_game(board_size)

    bots = {gotypes.Player.black: agent.naive.RandomBot(), gotypes.Player.white: agent.naive.RandomBot()}

    while not game.is_over():
        time.sleep(0.3)

        print(chr(27) + "[2J")
        utils.print_board(game.board)
        bot_move = bots[game.next_player].select_move(game)
        utils.print_move(game.next_player, bot_move)
        game = game.apply_move(bot_move)


if __name__ == "__main__":
    main()
