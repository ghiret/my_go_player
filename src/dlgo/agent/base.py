"""
This file is based on code from the book "Deep Learning and the Game of Go"
by Max Pumperla and Kevin Ferguson (Manning Publications, 2019).
Original code repository: https://github.com/maxpumperla/deep_learning_and_the_game_of_go

The code may have been modified and adapted for educational purposes.
"""


class Agent:
    """
    This is the interface for a Go playing Agent.
    """

    def __init__(self):
        pass

    def select_move(self, game_state):
        raise NotImplementedError()
