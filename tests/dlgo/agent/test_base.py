import pytest

from dlgo.agent.base import Agent
from dlgo.goboard_slow import GameState
from dlgo.gotypes import Player


def test_agent_initialization():
    agent = Agent()
    assert isinstance(agent, Agent)


def test_select_move_not_implemented():
    agent = Agent()
    game_state = GameState.new_game(19)
    with pytest.raises(NotImplementedError):
        agent.select_move(game_state)


def test_subclass_must_implement_select_move():
    class ConcreteAgent(Agent):
        pass

    concrete_agent = ConcreteAgent()
    game_state = GameState.new_game(19)
    with pytest.raises(NotImplementedError):
        concrete_agent.select_move(game_state)


def test_proper_subclass_implementation():
    class ProperAgent(Agent):
        def select_move(self, game_state):
            return game_state.next_player

    proper_agent = ProperAgent()
    game_state = GameState.new_game(19)
    assert proper_agent.select_move(game_state) == Player.black


def test_select_move_receives_game_state():
    class CheckingAgent(Agent):
        def select_move(self, game_state):
            assert isinstance(game_state, GameState)
            return game_state.next_player

    checking_agent = CheckingAgent()
    game_state = GameState.new_game(19)
    checking_agent.select_move(game_state)


def test_agent_equality():
    agent1 = Agent()
    agent2 = Agent()
    assert agent1 != agent2  # Agents should not be considered equal by default
