import os

import pygame
from pygame.locals import *

from game.storage.Storage import DATA_FOLDER_NAME


# Resource Manager Class - this loads images and sounds
# TODO - Could use some refactoring - extract common code from load_image
class ResourceManager:
    def __init__(self):
        self.main_dir = os.path.split(os.path.abspath(__file__))[0]
        self.data_dir = os.path.join(self.main_dir, DATA_FOLDER_NAME)

    def load_image(self, name, color_key=None):
        fullname = os.path.join(self.data_dir, name)
        try:
            image = pygame.image.load(fullname)
        except pygame.error:
            print("cannot load image:", fullname)
            raise SystemExit()

        image = image.convert()
        if color_key is not None:
            if color_key == -1:
                color_key = image.get_at((0, 0))
            image.set_colorkey(color_key, RLEACCEL)
        return image, image.get_rect()

    def load_sound(self, name):
        class NoneSound:
            def play(self): pass

        if not pygame.mixer or not pygame.mixer.get_init():
            return NoneSound()
        fullname = os.path.join(self.data_dir, name)
        sound = None
        try:
            sound = pygame.mixer.Sound(fullname)
        except pygame.error:
            print(f"Sound not loaded: {sound}")
            raise SystemExit()
        return sound
