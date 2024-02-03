import pygame

from game.HighScoreManager import HighScoreManager
# from game.HighScoreManager import HighScoreManager
from game.ResourceManager import ResourceManager
from game.states.GameOverState import GameOverState
from game.states.GameStateManager import GameStateManager
from game.states.GameWonState import GameWonState
from game.states.HighScoreMenuState import HighScoreMenuState
from game.states.MenuState import MenuState
from game.states.PlayState import PlayState
from game.storage.Storage import RESOLUTION, GAME_TITLE, BALL_FILENAME, HIGHSCORES_FILENAME


class Game:
    def __init__(self):
        pygame.init()
        self.screen = pygame.display.set_mode(RESOLUTION)
        pygame.display.set_caption(GAME_TITLE)
        self.resource_manager = ResourceManager()
        pygame.mixer.init()
        # I will use the same resource manager for loading the icon as well
        self.game_icon = self.resource_manager.load_image(BALL_FILENAME, -1)
        # Because the resource_manager.load_image returns both the image and a rect I will use index 0
        # TODO - Could use some refactoring for efficiency -
        #  separate method in load_image cuz in this case I don't need a rect
        pygame.display.set_icon(self.game_icon[0])
        self.latest_score = {}
        self.clock = pygame.time.Clock()
        self.high_score_manager = HighScoreManager(self)
        # self.state = MenuState(self)
        # self.state = PlayState(self)
        self.state_manager = GameStateManager(self)
        self.state_manager.add_state("Menu", MenuState)
        self.state_manager.add_state("Play", PlayState)
        self.state_manager.add_state("GameOver", GameOverState)
        self.state_manager.add_state("GameWon", GameWonState)
        self.state_manager.add_state("HighScoreMenu", HighScoreMenuState)
        self.state_manager.change_state("Menu")



    def run(self):
        while True:
            self.clock.tick(60)
            self.state_manager.handle_events()
            self.state_manager.update()
            self.state_manager.render()
