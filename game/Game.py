import pygame

from game.ResourceManager import ResourceManager
from game.states.MenuState import MenuState
from game.storage.Storage import RESOLUTION, GAME_TITLE, BALL_FILENAME


class Game:
    def __init__(self):
        pygame.init()
        self.screen = pygame.display.set_mode(RESOLUTION)
        pygame.display.set_caption(GAME_TITLE)
        self.resource_manager = ResourceManager()
        pygame.mixer.init()
        # I will use the same resource manager for loading the icon as well
        self.game_icon = self.resource_manager.load_image(BALL_FILENAME, -1)
        # self.game_icon = pygame.image.load(r"data\silver_ball_32px.png")
        # Because the resource_manager.load_image returns both the image and a rect I will use index 0
        # TODO - Could use some refactoring for efficiency -
        #  separate method in load_image cuz in this case I don't need a rect
        pygame.display.set_icon(self.game_icon[0])
        self.state = MenuState(self)
        # self.state = PlayState(self)
        self.clock = pygame.time.Clock()

    def run(self):
        while True:
            self.clock.tick(20)
            self.state.handle_events()
            self.state.update()
            self.state.render()
