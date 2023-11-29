# Abstract class for the game states
class GameState:
    def __init__(self, game):
        self.game = game

    def handle_events(self):
        raise NotImplementedError

    def update(self):
        raise NotImplementedError

    def render(self):
        raise NotImplementedError
