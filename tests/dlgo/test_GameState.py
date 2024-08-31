"""
This file was initially generated using an AI language model (Claude 3.5 Sonnet),
as part of an educational project based on the book "Deep Learning and the Game of Go"
by Max Pumperla and Kevin Ferguson (Manning Publications, 2019).

The generated code has been reviewed, potentially modified, and adapted to fit the
project's requirements and to ensure correctness and adherence to the book's concepts.
"""

import pytest

from dlgo.board import Board
from dlgo.goboard_fast import GameState
from dlgo.gotypes import Player, Point
from dlgo.move import Move
from dlgo.visualizer import GameVisualizer
from misc.board_utils import create_board_from_ascii, debug_output


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
    assert next_state.board.get_go_string_color(Point(3, 3)) == Player.black
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


def test_is_over_after_resign(new_game):

    next_state = new_game.apply_move(Move.resign())
    assert next_state.is_over()


def test_is_valid_move_after_resign(new_game):

    move_resign = Move.resign()

    assert new_game.is_valid_move(move_resign)
    next_state = new_game.apply_move(move_resign)

    move_pass = Move.pass_turn()
    assert not next_state.is_valid_move(move_pass)


def test_is_valid_move_with_a_pass(new_game):

    next_state = new_game.apply_move(Move.resign())

    move_pass = Move.pass_turn()
    assert not next_state.is_valid_move(move_pass)


def test_is_over_after_two_passes(new_game):

    next_state = new_game.apply_move(Move.pass_turn())
    final_state = next_state.apply_move(Move.pass_turn())
    assert final_state.is_over()


def test_is_move_self_capture():

    ascii_board = """
      A B C D E
    1 . W . . .
    2 W . W . .
    3 . W . . .
    4 . . . . .
    5 . . . . .
    """

    board = create_board_from_ascii(ascii_board)

    game = GameState(board, Player.black, None, None)
    move = Move.play(Point(2, 2))
    assert game.is_move_self_capture(Player.black, move)

    move_pass = Move.pass_turn()
    assert not game.is_move_self_capture(Player.black, move_pass)


def test_is_move_self_capture_in_corner():

    board = create_board_from_ascii(
        """
        A B
      1 . W
      2 W .
    """
    )

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
      A B C D E F G
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
        print("Stone at (7, 4):", state3.board.get_go_string_color(Point(7, 4)))
        print("Stone at (6, 4):", state3.board.get_go_string_color(Point(6, 4)))
        print("Stone at (6, 5):", state3.board.get_go_string_color(Point(6, 5)))

    assert state3.board.get_go_string_color(Point(7, 4)) is Player.white, "White stone should still be at (7,4)"
    assert state3.board.get_go_string_color(Point(6, 4)) is None, "This should still be empty"
    assert state3.board.get_go_string_color(Point(6, 5)) == Player.black, "Black's move should be at (6,5)"

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


def test_does_move_violate_ko_with_non_play_move():
    board = Board(5, 5)

    game = GameState(board, Player.black, None, None)

    move_pass = Move.pass_turn()
    assert not game.does_move_violate_ko(Player.black, move_pass)


def test_ko_violation():
    debug = False
    output_dir = "ko_test_images"
    visualizer = GameVisualizer(cell_size=60, margin=30) if debug else None

    # Initial board setup
    ascii_board = """
      A B C D E F G
    1 . . . . . . .
    2 . . B W . . .
    3 . B W . W . .
    4 . . B W . . .
    5 . . . . . . .
    6 . . . . . . .
    7 . . . . . . .
    """

    board = create_board_from_ascii(ascii_board)
    game = GameState(board, Player.black, None, None)

    debug_output(debug, game, "Initial board state", output_dir, visualizer, 0)

    # Black captures white stone
    move1 = Move.play(Point(3, 4))
    state1 = game.apply_move(move1)

    debug_output(debug, state1, "After Black captures at (3, 4)", output_dir, visualizer, 1)

    assert state1.board.get_go_string_color(Point(3, 3)) is None, "White stone should be captured"
    assert state1.board.get_go_string_color(Point(3, 4)) == Player.black, "Black stone should be at (3,4)"

    # White attempts to recapture
    move2 = Move.play(Point(3, 3))

    # This move should violate the ko rule
    assert state1.does_move_violate_ko(Player.white, move2), "This move should violate the ko rule"

    # Attempt to apply the move anyway to see if it's prevented
    assert state1.is_valid_move(move2) is False

    # Verify that White can play elsewhere
    move3 = Move.play(Point(5, 5))
    assert state1.is_valid_move(move3), "White should be allowed to play elsewhere"

    state2 = state1.apply_move(move3)
    debug_output(debug, state2, "After White plays elsewhere at (5, 5)", output_dir, visualizer, 3)

    # Now Black can play elsewhere
    move4 = Move.play(Point(6, 6))
    state3 = state2.apply_move(move4)
    debug_output(debug, state3, "After Black plays elsewhere at (6, 6)", output_dir, visualizer, 4)

    # White should now be able to recapture
    move5 = Move.play(Point(3, 3))
    assert not state3.does_move_violate_ko(Player.white, move5), "White should now be allowed to recapture"

    state5 = state3.apply_move(move5)
    debug_output(debug, state5, "After White recaptures at (3, 2)", output_dir, visualizer, 5)

    assert state5.board.get_go_string_color(Point(3, 3)) == Player.white, "White stone should now be at (3,2)"
    assert state5.board.get_go_string_color(Point(3, 4)) is None, "Black stone should be captured"

    if debug:
        print("\nTest completed. Check the 'ko_test_images' directory for visual output.")


def test_empty_board_legal_moves():
    board = Board(5, 5)
    game = GameState(board, Player.black, None, None)
    legal_moves = game.legal_moves()

    assert len(legal_moves) == 27  # 5x5 board + pass + resign


def test_full_board_legal_moves():
    ascii_board = """
      A B C D E
    1 B W B W B
    2 W B W B W
    3 B W B W B
    4 W B W B W
    5 B W B W B
    """
    board = create_board_from_ascii(ascii_board)
    game = GameState(board, Player.black, None, None)
    legal_moves = game.legal_moves()

    assert len(legal_moves) == 2  # only pass and resign are legal


def test_some_legal_moves():
    ascii_board = """
      A B C D E
    1 . W . . .
    2 W . W . .
    3 . W . . .
    4 . . . . .
    5 . . . . .
    """
    board = create_board_from_ascii(ascii_board)
    game = GameState(board, Player.black, None, None)
    legal_moves = game.legal_moves()

    assert len(legal_moves) > 0  # more than just pass and resign
    assert Move.play(Point(1, 3)) in legal_moves
    assert Move.play(Point(2, 2)) not in legal_moves  # self-capture


def test_ko_rule():
    ascii_board = """
      A B C D E
    1 . B . . .
    2 B . B . .
    3 . B . . .
    4 . . . . .
    5 . . . . .
    """
    board = create_board_from_ascii(ascii_board)
    game_state = GameState(board, Player.white, None, None)

    # ko rule prevents this move
    assert Move.play(Point(2, 2)) not in game_state.legal_moves()


def test_edge_cases():
    ascii_board = """
      A B C
    1 B . B
    2 . . .
    3 B . B
    """
    board = create_board_from_ascii(ascii_board)
    game = GameState(board, Player.black, None, None)
    legal_moves = game.legal_moves()

    assert len(legal_moves) == 7  # 5 valid plays + pass + resign
    assert Move.play(Point(1, 2)) in legal_moves
    assert Move.play(Point(2, 1)) in legal_moves
    assert Move.play(Point(2, 2)) in legal_moves
    assert Move.play(Point(2, 3)) in legal_moves
    assert Move.play(Point(3, 2)) in legal_moves


def test_legal_moves_different_players():
    ascii_board = """
      A B C
    1 B . .
    2 . W .
    3 . . .
    """
    board = create_board_from_ascii(ascii_board)
    game_black = GameState(board, Player.black, None, None)
    game_white = GameState(board, Player.white, None, None)

    legal_moves_black = game_black.legal_moves()
    legal_moves_white = game_white.legal_moves()

    assert len(legal_moves_black) == len(legal_moves_white)
    assert Move.play(Point(1, 1)) not in legal_moves_black
    assert Move.play(Point(1, 1)) not in legal_moves_white
    assert Move.play(Point(2, 2)) not in legal_moves_black
    assert Move.play(Point(2, 2)) not in legal_moves_white


# Helper function to count specific move types


def count_move_types(moves):
    play_moves = sum(1 for move in moves if move.is_play)
    pass_moves = sum(1 for move in moves if move.is_pass)
    resign_moves = sum(1 for move in moves if move.is_resign)
    return play_moves, pass_moves, resign_moves


def test_move_types():
    board = Board(5, 5)
    game = GameState(board, Player.black, None, None)
    legal_moves = game.legal_moves()

    play_moves, pass_moves, resign_moves = count_move_types(legal_moves)
    assert play_moves == 25  # 5x5 board
    assert pass_moves == 1
    assert resign_moves == 1
