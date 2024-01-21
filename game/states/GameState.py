# Abstract class for the game states
from abc import ABC, abstractmethod

from game.storage.Storage import PLAY_STATE_MUSIC_FILENAME


class GameState(ABC):
    def __init__(self, game):
        self.game = game

    @abstractmethod
    def handle_events(self):
        raise NotImplementedError

    @abstractmethod
    def update(self):
        raise NotImplementedError

    @abstractmethod
    def render(self):
        raise NotImplementedError
