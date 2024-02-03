import json
import os

import pygame
from pygame.locals import *

from game.HighScoreManager import HighScoreManager
# from game.HighScoreManager import HighScoreManager
from game.storage.Storage import DATA_FOLDER_NAME, PSEUDO_DB_FOLDER_NAME


# Resource Manager Class - this loads images and sounds
# TODO - Could use some refactoring - extract common code from load_image
class ResourceManager:
    def __init__(self):
        self.main_dir = os.path.split(os.path.abspath(__file__))[0]
        self.data_dir = os.path.join(self.main_dir, DATA_FOLDER_NAME)
        self.pseudo_db_dir = os.path.join(self.main_dir, PSEUDO_DB_FOLDER_NAME)

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

    def load_highscores_data(self, name):
        full_file_path = os.path.join(self.pseudo_db_dir, name)
        # TODO - check error
        try:
            with open(full_file_path, "r") as highscores_file:
                highscore_data = json.load(highscores_file)
                return highscore_data
        except FileNotFoundError:
            print("High score file not found")
            return []

    def write_highscores_data(self, name, new_data):
        full_file_path = os.path.join(self.pseudo_db_dir, name)
        # TODO - check error
        try:
            with open(full_file_path, "w") as highscores_file:
                json.dump(new_data, highscores_file)
        except FileNotFoundError:
            print("High score file not found")