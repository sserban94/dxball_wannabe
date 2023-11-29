import pygame

from game.storage.Storage import PLATE_FILENAME, GAME_WIDTH, PLATE_WIDTH, PLATE_DISTANCE_FROM_BOTTOM, GAME_HEIGHT, \
    PLATE_SPEED


class Plate(pygame.sprite.Sprite):
    def __init__(self, resource_manager):
        pygame.sprite.Sprite.__init__(self)
        self.image, self.rect = resource_manager.load_image(PLATE_FILENAME, -1)
        screen = pygame.display.get_surface()
        self.area = screen.get_rect()
        self.rect.left = GAME_WIDTH / 2 - PLATE_WIDTH / 2
        self.rect.bottom = GAME_HEIGHT - PLATE_DISTANCE_FROM_BOTTOM

    def move_left(self):
        if not self.rect.left - PLATE_SPEED < 0:
            newp_os = self.rect.move((-PLATE_SPEED, 0))
            self.rect = newp_os

    def move_right(self):
        if not self.rect.right + PLATE_SPEED > self.area.right:
            new_pos = self.rect.move((PLATE_SPEED, 0))
            self.rect = new_pos
