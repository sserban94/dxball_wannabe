import random

import pygame

from game.states.GameOverState import GameOverState
from game.storage.Storage import BALL_FILENAME, PLATE_HEIGHT, GAME_WIDTH, GAME_HEIGHT, PLATE_DISTANCE_FROM_BOTTOM


class Ball(pygame.sprite.Sprite):
    def __init__(self, game):
        pygame.sprite.Sprite.__init__(self)
        self.game = game
        # the image has size 32x32
        self.image, self.rect = game.resource_manager.load_image(BALL_FILENAME, -1)
        screen = pygame.display.get_surface()
        # screen.get_rect creates a new rect with the size of the image and the coordonates x 0 y 0
        self.area = screen.get_rect()
        # giving the rect - x position of 160
        # self.rect.left = 100 + 60
        self.rect.left = random.randint(0, GAME_WIDTH)
        # giving the rect - y position of
        self.rect.bottom = GAME_HEIGHT - PLATE_HEIGHT - PLATE_DISTANCE_FROM_BOTTOM
        print("test")
        # self.speed_x, self.speed_y = BALL_SPEED, -BALL_SPEED
        # self.is_on_plate_flag = False

    # def update(self):
    #     # change horizontal speed for left and right borders
    #     # if self.rect.left + self.speed_x < 0 or self.rect.right + self.speed_y > self.area.right:
    #     #     self.speed_x *= -1
    #     if self.rect.left < 0 or self.rect.right > self.area.right:
    #         self.speed_x *= -1
    #
    #     # change vertical speed for the top border
    #     # if self.rect.top + self.speed_y < 0:
    #     #     self.speed_y *= -1
    #     if self.rect.top < 0:
    #         self.speed_y *= -1
    #
    #     # change vertical speed for the bottom border
    #     # if self.rect.bottom + self.speed_y > self.area.bottom - 24:
    #     #     if self.is_on_plate_flag:
    #     #         self.speed_y *= -1
    #     #         self.is_on_plate_flag = False
    #     #     else:
    #     #         print("Game Over")
    #     #         pygame.quit()
    #     # self.rect.move_ip(self.speed_x, self.speed_y)
    #
    #     if self.rect.bottom > self.area.bottom - PLATE_HEIGHT and not self.is_on_plate_flag:
    #         self.game.state = GameOverState(self.game)
    #
    #         # pygame.quit()
    #
    #     self.rect.move_ip(self.speed_x, self.speed_y)
    #
    # def is_on_plate(self, plate):
    #     # if self.rect.colliderect(plate.rect):
    #     #     self.is_on_plate_flag = True
    #     # else:
    #     #     self.is_on_plate_flag = False
    #     if self.rect.colliderect(plate.rect):
    #         if not self.is_on_plate_flag:
    #             self.speed_y *= -1
    #         self.is_on_plate_flag = True
    #     else:
    #         self.is_on_plate_flag = False
