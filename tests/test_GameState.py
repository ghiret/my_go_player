import os

import pytest

from dlgo.goboard_slow import Board, GameState, Move
from dlgo.gotypes import Player, Point
from dlgo.visualizer import GameVisualizer
from utils.board_utils import create_board_from_ascii, print_board


def debug_output(debug, state, message, output_dir, visualizer, move_number):
    print(f"\n{message}")
    print_board(state.board)

    if debug and visualizer:
        os.makedirs(output_dir, exist_ok=True)
        visualizer.visualize_game_state(
            state,
            os.path.join(output_dir, f"{move_number:02d}_{message.replace(' ', '_').lower()}.png"),
        )


@pytest.fixture
def new_game():
    return GameState.new_game(19)


def test_new_game_initialization(new_game):
    assert isinstance(new_game.board, Board)
    assert new_game.next_player == Player.black
    assert new_game.previous_state is None
    assert new_game.last_move is None


def test_apply_move_play(new_game):
    move = Move.play(Point(3, 3))
    next_state = new_game.apply_move(move)
    assert next_state.board.get(Point(3, 3)) == Player.black
    assert next_state.next_player == Player.white
    assert next_state.previous_state == new_game
    assert next_state.last_move == move


def test_apply_move_pass(new_game):
    move = Move.pass_turn()
    next_state = new_game.apply_move(move)
    assert next_state.board == new_game.board
    assert next_state.next_player == Player.white
    assert next_state.previous_state == new_game
    assert next_state.last_move == move


def test_apply_move_resign(new_game):
    move = Move.resign()
    next_state = new_game.apply_move(move)
    assert next_state.board == new_game.board
    assert next_state.next_player == Player.white
    assert next_state.previous_state == new_game
    assert next_state.last_move == move


def test_is_over_new_game(new_game):
    assert not new_game.is_over()


def test_is_over_after_resign():
    game = GameState.new_game(19)
    next_state = game.apply_move(Move.resign())
    assert next_state.is_over()


def test_is_over_after_two_passes():
    game = GameState.new_game(19)
    next_state = game.apply_move(Move.pass_turn())
    final_state = next_state.apply_move(Move.pass_turn())
    assert final_state.is_over()


def test_is_move_self_capture():
    board = Board(5, 5)
    board.place_stone(Player.white, Point(1, 2))
    board.place_stone(Player.white, Point(2, 1))
    board.place_stone(Player.white, Point(2, 3))
    board.place_stone(Player.white, Point(3, 2))
    game = GameState(board, Player.black, None, None)
    move = Move.play(Point(2, 2))
    assert game.is_move_self_capture(Player.black, move)


def test_situation():
    board = Board(5, 5)
    game = GameState(board, Player.black, None, None)
    assert game.situation == (Player.black, board)


def test_snapback_not_ko():
    debug = False
    output_dir = "snapback_test_images"
    visualizer = GameVisualizer(cell_size=60, margin=30) if debug else None

    # Initial board setup for snapback
    ascii_board = """
      1 2 3 4 5 6 7
    1 . . . . . . .
    2 . . . . . . .
    3 . . . . . . .
    4 . . . . . . .
    5 . B W W W . .
    6 . B W B B W .
    7 . B B W . W .
    """

    board = create_board_from_ascii(ascii_board)
    game = GameState(board, Player.black, None, None)

    debug_output(debug, game, "Initial board state", output_dir, visualizer, 0)

    # Black captures one white stone
    move1 = Move.play(Point(7, 5))
    state1 = game.apply_move(move1)

    debug_output(debug, state1, "After Black captures at (7, 5)", output_dir, visualizer, 1)

    # White plays, creating a snapback situation
    move2 = Move.play(Point(7, 4))
    state2 = state1.apply_move(move2)

    debug_output(debug, state2, "After White plays at (7, 4)", output_dir, visualizer, 2)

    # Black captures the white group by playing at the 'mouth' of the snapback
    move3 = Move.play(Point(6, 5))
    state3 = state2.apply_move(move3)

    debug_output(debug, state3, "After Black plays at (6, 5)", output_dir, visualizer, 3)

    # Add these debug prints
    if debug:
        print("Stone at (7, 4):", state3.board.get(Point(7, 4)))
        print("Stone at (6, 4):", state3.board.get(Point(6, 4)))
        print("Stone at (6, 5):", state3.board.get(Point(6, 5)))

    assert state3.board.get(Point(7, 4)) is Player.white, "White stone should still be at (7,4)"
    assert state3.board.get(Point(6, 4)) is None, "This should still be empty"
    assert state3.board.get(Point(6, 5)) == Player.black, "Black's move should be at (6,5)"

    assert not state2.does_move_violate_ko(Player.black, move3), "Snapback should not violate ko rule"

    # Verify that White cannot immediately recapture
    move4 = Move.play(Point(7, 5))
    assert state3.is_valid_move(move4), "White should be allowed to play at (7,5)"
    state4 = state3.apply_move(move4)

    debug_output(debug, state4, "After White plays at (7, 5)", output_dir, visualizer, 4)

    # Black can now safely fill the eye
    move5 = Move.play(Point(6, 4))
    assert not state4.is_valid_move(move5), "Black should not be allowed to self-capture"

    if debug:
        print("\nTest completed. Check the 'snapback_test_images' directory for visual output.")
