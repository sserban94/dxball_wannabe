import random

import pygame

from game.storage.Storage import BLOCK_SCALE_SIZE


class Block(pygame.sprite.Sprite):
    def __init__(self, resource_manager, pos_x, pos_y):
        pygame.sprite.Sprite.__init__(self)
        self.image, self.rect = resource_manager.load_image(self.select_random_block_color(), -1)
        self.image = pygame.transform.scale(self.image, BLOCK_SCALE_SIZE)  # Scale the image to 40x40 pixels
        self.rect = self.image.get_rect()  # Update the rectangle to match the new image size
        self.rect.topleft = pos_x, pos_y

    def select_random_block_color(self):
        file_list = ['dxball_block_0_255_255_10x10.png',
                     'dxball_block_10x10.png',
                     'dxball_block_255_0_0_10x10.png',
                     'dxball_block_255_255_0_10x10.png',
                     'dxball_block_blue_10x10.png',
                     'dxball_block_255_0_255_10x10.png']
        # return random file from the list
        return random.choice(file_list)
