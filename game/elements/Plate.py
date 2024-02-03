import pygame

from game.storage.Storage import PLATE_FILENAME, GAME_WIDTH, PLATE_WIDTH, PLATE_DISTANCE_FROM_BOTTOM, GAME_HEIGHT, \
    PLATE_SPEED


class Plate(pygame.sprite.Sprite):
    def __init__(self, game):
        pygame.sprite.Sprite.__init__(self)
        self.image, self.rect = game.resource_manager.load_image(PLATE_FILENAME, -1)
        screen = pygame.display.get_surface()
        self.area = screen.get_rect()
        self.rect.left = GAME_WIDTH / 2 - PLATE_WIDTH / 2
        self.rect.bottom = GAME_HEIGHT - PLATE_DISTANCE_FROM_BOTTOM
