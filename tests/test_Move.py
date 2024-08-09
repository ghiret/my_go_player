from dlgo.goboard_slow import Move


def test_move_play():
    point = (3, 3)
    move = Move.play(point)
    assert move.point == point
    assert move.is_play
    assert not move.is_pass
    assert not move.is_resign


def test_move_pass():
    move = Move.pass_turn()
    assert move.point is None
    assert not move.is_play
    assert move.is_pass
    assert not move.is_resign


def test_move_resign():
    move = Move.resign()
    assert move.point is None
    assert not move.is_play
    assert not move.is_pass
    assert move.is_resign


def test_move_init_play():
    point = (4, 4)
    move = Move(point=point)
    assert move.point == point
    assert move.is_play
    assert not move.is_pass
    assert not move.is_resign


def test_move_init_pass():
    move = Move(is_pass=True)
    assert move.point is None
    assert not move.is_play
    assert move.is_pass
    assert not move.is_resign


def test_move_init_resign():
    move = Move(is_resign=True)
    assert move.point is None
    assert not move.is_play
    assert not move.is_pass
    assert move.is_resign
