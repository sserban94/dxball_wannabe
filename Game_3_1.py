import os
import random

import pygame
from pygame.locals import *

RESOLUTION = (1280, 720)
BLOCK_SIZE = 20  # Adjust this to change the block size
GAME_WIDTH = 1280
GAME_HEIGHT = 720
LEFT_MARGIN = 20
BLOCK_START_HEIGHT = 20
PLAY_OPTION_POSITION = (360, 200)
QUIT_OPTION_POSITION = (360, 300)
DELAY = 100
INTERVAL = 100
BACKGROUND_COLOR = (100, 100, 100)
WHITE = (255, 255, 255)
BLACK = (0, 0, 0)
GREY = (128, 128, 128)
FONT_VALUES = {'font_type': None,
               'font_size': 36}
GAME_TITLE = "DxBall cu buget redus"
BALL_FILENAME = 'silver_ball_32px.png'
PLATE_FILENAME = 'dxball_bar_120x24.png'


# Resource Manager Class
class ResourceManager:
    def __init__(self):
        self.main_dir = os.path.split(os.path.abspath(__file__))[0]
        self.data_dir = os.path.join(self.main_dir, 'data')

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
        try:
            sound = pygame.mixer.Sound(fullname)
        except pygame.error:
            print("cannot load sound: %s" % sound)
            raise SystemExit()
        return sound


# Game Object Classes
class Block(pygame.sprite.Sprite):
    def __init__(self, resource_manager, pos_x, pos_y):
        pygame.sprite.Sprite.__init__(self)
        self.image, self.rect = resource_manager.load_image(self.select_random_block_color(), -1)
        self.image = pygame.transform.scale(self.image, (30, 20))  # Scale the image to 40x40 pixels
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


class Plate(pygame.sprite.Sprite):
    def __init__(self, resource_manager):
        pygame.sprite.Sprite.__init__(self)
        self.image, self.rect = resource_manager.load_image('dxball_bar_120x24.png', -1)
        screen = pygame.display.get_surface()
        self.area = screen.get_rect()
        self.rect.left = 100
        self.rect.bottom = 540

    def move_left(self):
        if not self.rect.left - 20 < 0:
            newp_os = self.rect.move((-20, 0))
            self.rect = newp_os

    def move_right(self):
        if not self.rect.right + 20 > self.area.right:
            new_pos = self.rect.move((20, 0))
            self.rect = new_pos


class Ball(pygame.sprite.Sprite):
    def __init__(self, resource_manager):
        pygame.sprite.Sprite.__init__(self)
        self.image, self.rect = resource_manager.load_image('silver_ball_32px.png', -1)
        screen = pygame.display.get_surface()
        self.area = screen.get_rect()
        self.speed_x, self.speed_y = 12, -12
        self.rect.left = 100 + 60
        self.rect.bottom = self.area.bottom - 24
        self.is_on_plate_flag = False

    def update(self):
        # change horizontal speed for left and right borders
        # if self.rect.left + self.speed_x < 0 or self.rect.right + self.speed_y > self.area.right:
        #     self.speed_x *= -1
        if self.rect.left < 0 or self.rect.right > self.area.right:
            self.speed_x *= -1

        # change vertical speed for the top border
        # if self.rect.top + self.speed_y < 0:
        #     self.speed_y *= -1
        if self.rect.top < 0:
            self.speed_y *= -1

        # change vertical speed for the bottom border
        # if self.rect.bottom + self.speed_y > self.area.bottom - 24:
        #     if self.is_on_plate_flag:
        #         self.speed_y *= -1
        #         self.is_on_plate_flag = False
        #     else:
        #         print("Game Over")
        #         pygame.quit()
        # self.rect.move_ip(self.speed_x, self.speed_y)
        if self.rect.bottom > self.area.bottom - 24 and not self.is_on_plate_flag:
            print("Game Over")
            pygame.quit()

        self.rect.move_ip(self.speed_x, self.speed_y)

    def is_on_plate(self, plate):
        # if self.rect.colliderect(plate.rect):
        #     self.is_on_plate_flag = True
        # else:
        #     self.is_on_plate_flag = False
        if self.rect.colliderect(plate.rect):
            if not self.is_on_plate_flag:
                self.speed_y *= -1
            self.is_on_plate_flag = True
        else:
            self.is_on_plate_flag = False


class GameState:
    def __init__(self, game):
        self.game = game

    def handle_events(self):
        raise NotImplementedError

    def update(self):
        raise NotImplementedError

    def render(self):
        raise NotImplementedError


# Play State
class PlayState(GameState):
    def __init__(self, game):
        super().__init__(game)
        self.ball = Ball(game.resource_manager)
        self.plate = Plate(game.resource_manager)
        self.all_sprites = pygame.sprite.Group(self.ball, self.plate)
        self.blocks = self.position_block(game.resource_manager)

    def position_block(self, resource_manager):
        blocks = pygame.sprite.RenderPlain()
        block_size = BLOCK_SIZE  # Adjust this to change the block size
        game_width = GAME_WIDTH
        game_height = GAME_HEIGHT
        left_margin = LEFT_MARGIN
        block_start_height = BLOCK_START_HEIGHT  # Adjust this to change the starting height of the blocks
        x = left_margin
        while x <= game_width:
            y = block_start_height
            while y <= game_height:
                block = Block(resource_manager, x, y)
                blocks.add(block)
                y += block_size
            x += block_size
        return blocks

    def handle_events(self):
        pygame.key.set_repeat(DELAY, INTERVAL)
        for event in pygame.event.get():
            if event.type == QUIT:
                pygame.quit()
            elif event.type == KEYDOWN:
                if event.key == K_LEFT or event.key == K_a:
                    self.plate.move_left()
                elif event.key == K_RIGHT or event.key == K_d:
                    self.plate.move_right()

    def update(self):
        self.ball.update()
        self.ball.is_on_plate(self.plate)
        pygame.sprite.spritecollide(self.ball, self.blocks, True)

    def render(self):
        self.game.screen.fill(BACKGROUND_COLOR)
        self.all_sprites.draw(self.game.screen)
        self.blocks.draw(self.game.screen)
        pygame.display.flip()


class MenuState(GameState):
    def __init__(self, game):
        super().__init__(game)
        self.font = pygame.font.Font(FONT_VALUES['font_type'], FONT_VALUES['font_size'])
        self.play_text = self.font.render("Play", True, WHITE)
        self.quit_text = self.font.render("Quit", True, WHITE)
        self.play_rect = self.play_text.get_rect(center=PLAY_OPTION_POSITION)
        self.quit_rect = self.quit_text.get_rect(center=QUIT_OPTION_POSITION)
        self.selected_option = 0

    def handle_events(self):
        for event in pygame.event.get():
            if event.type == QUIT:
                pygame.quit()
            elif event.type == KEYDOWN:
                if event.key == K_UP:
                    # using max so the user can't go lower than 0 here
                    self.selected_option = max(0, self.selected_option - 1)
                elif event.key == K_DOWN:
                    # using min so the user can't go higher than 1 here
                    self.selected_option = min(1, self.selected_option + 1)
                    # K_RETURN apparently is the enter key
                elif event.key == K_RETURN:
                    if self.selected_option == 0:
                        self.game.state = PlayState(self.game)
                    else:
                        pygame.quit()

    def update(self):
        pass

    def render(self):
        self.game.screen.fill((0, 0, 0))
        play_color = WHITE if self.selected_option == 0 else GREY
        quit_color = WHITE if self.selected_option == 1 else GREY
        play_text = self.font.render("Play", True, play_color)
        quit_text = self.font.render("Quit", True, quit_color)
        self.game.screen.blit(play_text, self.play_rect)
        self.game.screen.blit(quit_text, self.quit_rect)
        pygame.display.flip()


# Game Class
class Game:
    def __init__(self):
        pygame.init()
        self.screen = pygame.display.set_mode(RESOLUTION)
        pygame.display.set_caption(GAME_TITLE)
        self.resource_manager = ResourceManager()
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


# Entry Point
if __name__ == '__main__':
    game = Game()
    game.run()
