import pytest
import math
from dlgo.agent.mcts_agent import uct_score, MCTSAgent 

def test_uct_score_typical_case():
    result = uct_score(parent_rollouts=100, child_rollouts=10, win_pct=0.6, temperature=1.0)
    expected = 0.6 + 1.0 * math.sqrt(math.log(100) / 10)
    assert math.isclose(result, expected, rel_tol=1e-9)

def test_uct_score_zero_temperature():
    result = uct_score(parent_rollouts=100, child_rollouts=10, win_pct=0.5, temperature=0.0)
    assert result == 0.5

def test_uct_score_high_temperature():
    result = uct_score(parent_rollouts=100, child_rollouts=10, win_pct=0.5, temperature=2.0)
    expected = 0.5 + 2.0 * math.sqrt(math.log(100) / 10)
    assert math.isclose(result, expected, rel_tol=1e-9)

def test_uct_score_equal_rollouts():
    result = uct_score(parent_rollouts=100, child_rollouts=100, win_pct=0.7, temperature=1.0)
    expected = 0.7 + 1.0 * math.sqrt(math.log(100) / 100)
    assert math.isclose(result, expected, rel_tol=1e-9)

def test_uct_score_large_numbers():
    result = uct_score(parent_rollouts=1000000, child_rollouts=100000, win_pct=0.9, temperature=0.5)
    expected = 0.9 + 0.5 * math.sqrt(math.log(1000000) / 100000)
    assert math.isclose(result, expected, rel_tol=1e-9)

def test_uct_score_win_pct_bounds():
    assert 0 <= uct_score(parent_rollouts=100, child_rollouts=10, win_pct=0.0, temperature=1.0) <= 1
    assert uct_score(parent_rollouts=100, child_rollouts=10, win_pct=1.0, temperature=1.0) > 1

def test_uct_score_error_child_rollouts_zero():
    with pytest.raises(AssertionError, match="child_rollouts must be positive, got 0"):
        uct_score(parent_rollouts=100, child_rollouts=0, win_pct=0.5, temperature=1.0)

def test_uct_score_error_parent_rollouts_zero():
    with pytest.raises(AssertionError, match="parent_rollouts must be positive, got 0"):
        uct_score(parent_rollouts=0, child_rollouts=10, win_pct=0.5, temperature=1.0)

def test_uct_score_error_negative_rollouts():
    with pytest.raises(AssertionError, match="parent_rollouts must be positive, got -1"):
        uct_score(parent_rollouts=-1, child_rollouts=10, win_pct=0.5, temperature=1.0)
    with pytest.raises(AssertionError, match="child_rollouts must be positive, got -1"):
        uct_score(parent_rollouts=100, child_rollouts=-1, win_pct=0.5, temperature=1.0)

def test_uct_score_error_invalid_win_pct():
    with pytest.raises(AssertionError, match="win_pct must be between 0 and 1, got -0.1"):
        uct_score(parent_rollouts=100, child_rollouts=10, win_pct=-0.1, temperature=1.0)
    with pytest.raises(AssertionError, match="win_pct must be between 0 and 1, got 1.1"):
        uct_score(parent_rollouts=100, child_rollouts=10, win_pct=1.1, temperature=1.0)

def test_uct_score_error_negative_temperature():
    with pytest.raises(AssertionError, match="temperature must be non-negative, got -1.0"):
        uct_score(parent_rollouts=100, child_rollouts=10, win_pct=0.5, temperature=-1.0)