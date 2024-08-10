class Agent:
    """
    This is the interface for a Go playing Agent.
    """

    def __init__(self):
        pass

    def select_move(self, game_state):
        raise NotImplementedError()
