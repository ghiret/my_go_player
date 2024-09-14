from datetime import date

import pytest

from dlgo.gosgf.sgf import Sgf_game  # Assuming the class is in a file named sgf_game.py


def test_sgf_game_initialization():
    game = Sgf_game(19)
    assert game.get_size() == 19
    assert game.get_root() is not None
    assert game.get_charset() == "UTF-8"


def test_sgf_game_initialization_invalid_size():
    with pytest.raises(ValueError):
        Sgf_game(27)


def test_from_string():
    sgf_string = b"(;FF[4]GM[1]SZ[19]CA[UTF-8])"
    game = Sgf_game.from_string(sgf_string)
    assert game.get_size() == 19
    assert game.get_charset() == "UTF-8"


def test_serialise():
    game = Sgf_game(19)
    serialized = game.serialise()
    assert isinstance(serialized, bytes)
    assert b"FF[4]" in serialized
    assert b"GM[1]" in serialized
    assert b"SZ[19]" in serialized


def test_get_last_node():
    game = Sgf_game(19)
    last_node = game.get_last_node()
    assert last_node == game.get_root()

    new_node = game.extend_main_sequence()
    assert game.get_last_node() == new_node


def test_get_main_sequence():
    game = Sgf_game(19)
    game.extend_main_sequence()
    game.extend_main_sequence()
    main_sequence = game.get_main_sequence()
    assert len(main_sequence) == 3
    assert main_sequence[0] == game.get_root()
    assert main_sequence[-1] == game.get_last_node()


def test_get_komi():
    game = Sgf_game(19)
    assert game.get_komi() == 0.0
    game.get_root().set(b"KM", b"6.5")
    assert game.get_komi() == 6.5


def test_get_player_name():
    game = Sgf_game(19)
    assert game.get_player_name("b") is None
    assert game.get_player_name("w") is None
    game.get_root().set(b"PB", b"Black Player")
    game.get_root().set(b"PW", b"White Player")
    assert game.get_player_name("b") == "Black Player"
    assert game.get_player_name("w") == "White Player"


def test_get_winner():
    game = Sgf_game(19)
    assert game.get_winner() is None
    game.get_root().set(b"RE", b"B+Resign")
    assert game.get_winner() == "b"
    game.get_root().set(b"RE", b"W+3.5")
    assert game.get_winner() == "w"
    game.get_root().set(b"RE", b"Draw")
    assert game.get_winner() is None


def test_get_handicap_normal_cases():
    game = Sgf_game(19)  # Assuming 19x19 board

    # Test when HA is not set
    assert game.get_handicap() is None

    # Test with valid handicap values
    valid_handicaps = [2, 3, 4, 5, 6, 7, 8, 9]
    for handicap in valid_handicaps:
        game.root.set(b"HA", handicap)
        assert game.get_handicap() == handicap

    # Test with handicap 0 (should return None)
    game.root.set(b"HA", 0)
    assert game.get_handicap() is None


def test_get_handicap_edge_cases():
    game = Sgf_game(19)  # Assuming 19x19 board

    # Test with handicap 1 (should raise ValueError)
    game.root._set_raw_list(b"HA", [b"1"])
    with pytest.raises(ValueError):
        game.get_handicap()

    # Test with non-integer handicap
    game.root._set_raw_list(b"HA", [b"not a number"])
    with pytest.raises(ValueError):
        game.get_handicap()

    # Test with negative handicap
    game.root._set_raw_list(b"HA", [b"-3"])
    assert game.get_handicap() == -3  # The method doesn't explicitly check for negative values

    # Test with float handicap
    game.root._set_raw_list(b"HA", [b"2.5"])
    with pytest.raises(ValueError):
        game.get_handicap()

    # Test with very large handicap
    large_handicap = 1000000
    game.root._set_raw_list(b"HA", [str(large_handicap).encode()])
    assert game.get_handicap() == large_handicap
