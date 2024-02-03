import math
import random
import time
from datetime import datetime

import pygame
from pygame import QUIT, KEYDOWN, K_LEFT, K_a, K_RIGHT, K_d

from game.controllers.BallController import BallController
from game.controllers.PlateController import PlateController
from game.elements.Ball import Ball
from game.elements.Block import Block
from game.elements.Plate import Plate
from game.states.GameOverState import GameOverState
from game.states.GameState import GameState
from game.states.GameWonState import GameWonState
from game.storage.Storage import BLOCK_WIDTH, BLOCK_HEIGHT, GAME_WIDTH, BLOCK_DISTANCE_FROM_LATERAL_WALL, \
    BLOCK_ENDING_DISTANCE_FROM_TOP, BLOCK_STARTING_DISTANCE_FROM_TOP, BLOCK_EMPTY_SPACE, DELAY, INTERVAL, \
    BACKGROUND_COLOR, PLAY_STATE_MUSIC_FILENAME, INITIAL_BALL_SPEED, BALL_SPEED, BALL_TOUCHING_PLATE_AUDIO_FILENAME, \
    DXBALL_OG_SOUNDS_FOLDER_NAME, BLOCK_DESTROYED_AUDIO_FILENAME


class PlayState(GameState):

    def __init__(self, game):
        super().__init__(game)
        self.active = None
        self.ball = None
        self.plate = None
        self.all_sprites = None
        self.blocks = None
        self.score = None
        self.font = None
        self.block_count = None
        self.start_time = None
        self.elapsed_time_already_checked = None
        self.ball_controller = None
        self.plate_controller = None
        self.music = self.game.resource_manager.load_sound(PLAY_STATE_MUSIC_FILENAME)

    def enter(self):
        self.active = True
        self.ball = Ball(self.game)
        self.plate = Plate(self.game)
        self.all_sprites = pygame.sprite.Group(self.ball, self.plate)
        self.blocks = None
        self.position_block()
        self.score = 0
        self.font = pygame.font.Font(None, 36)
        self.block_count = 0
        self.start_time = datetime.now()
        self.elapsed_time_already_checked = False
        self.ball_controller = BallController(self.ball, self.game, INITIAL_BALL_SPEED)
        self.plate_controller = PlateController(self.plate, self.game)
        self.music = self.game.resource_manager.load_music(PLAY_STATE_MUSIC_FILENAME)
        pygame.mixer.music.set_volume(0.5)
        pygame.mixer.music.play(-1)

    def exit(self):
        self.active = False
        pygame.mixer.music.stop()
        self.all_sprites.empty()


    def position_block(self):
        # resource_manager = self.game.resource_manager
        self.blocks = pygame.sprite.RenderPlain()
        block_width = BLOCK_WIDTH  # Here I can change the block size
        block_height = BLOCK_HEIGHT
        game_width = GAME_WIDTH
        left_margin = BLOCK_DISTANCE_FROM_LATERAL_WALL
        right_margin = BLOCK_DISTANCE_FROM_LATERAL_WALL
        block_start_height = BLOCK_ENDING_DISTANCE_FROM_TOP  # Here I can change the starting height of the blocks
        x = left_margin
        while x <= game_width - right_margin:
            y = BLOCK_STARTING_DISTANCE_FROM_TOP
            while y <= block_start_height:
                block = Block(self.game.resource_manager, x, y)
                # TODO - add multiple false here for less blocks
                to_be_or_not_to_be = [True, False]
                if random.choice(to_be_or_not_to_be):
                    self.blocks.add(block)
                y += block_height + BLOCK_EMPTY_SPACE
                # y += block_height + random.choice(BLOCK_EMPTY_SPACE_LIST)
            x += block_width + BLOCK_EMPTY_SPACE
            # x += block_width + random.choice(BLOCK_EMPTY_SPACE_LIST)
        # return blocks

    def handle_events(self):
        pygame.key.set_repeat(DELAY, INTERVAL)
        for event in pygame.event.get():
            if event.type == QUIT:
                self.game.high_score_manager.save_high_scores()
                pygame.quit()
            elif event.type == KEYDOWN:
                if event.key == K_LEFT or event.key == K_a:
                    self.plate_controller.move_left()
                elif event.key == K_RIGHT or event.key == K_d:
                    self.plate_controller.move_right()

    def update(self):
        # added logic here to wait before starting
        # TODO - add large counter text middle of screen
        if not self.elapsed_time_already_checked:
            if (datetime.now() - self.start_time).total_seconds() > 1:
                self.ball_controller.speed_x = BALL_SPEED
                self.ball_controller.speed_y = -BALL_SPEED
                self.elapsed_time_already_checked = True
        # TODO - I should move the logic outside the update method in controller - update should not return anything
        if self.ball_controller.update():
            # TODO - remove this block - only for win
            # save score and time
            latest_score = {
                "time": int((datetime.now() - self.start_time).total_seconds()),
                "blocks": self.score
            }
            self.game.high_score_manager.add_score(latest_score)
            self.game.state_manager.change_state("GameOver")
        if not self.active:
            return
        self.ball_controller.is_on_plate(self.plate)
        if self.ball_controller.is_on_plate_flag:
            self.music = self.game.resource_manager.load_sound(BALL_TOUCHING_PLATE_AUDIO_FILENAME, DXBALL_OG_SOUNDS_FOLDER_NAME)
            self.music.play()

        # this should get the no of sprites which collided
        collided_sprites = pygame.sprite.spritecollide(self.ball, self.blocks, True)
        if collided_sprites:
            self.music = self.game.resource_manager.load_sound(BLOCK_DESTROYED_AUDIO_FILENAME, DXBALL_OG_SOUNDS_FOLDER_NAME)
            self.music.play()
            self.ball_controller.speed_y *= -1
            self.score += len(collided_sprites)

        if len(self.blocks) == 0:
            # save score and time
            latest_score = {
                "time": (datetime.now() - self.start_time).total_seconds(),
                "blocks": self.score
            }
            self.game.high_score_manager.add_score(latest_score)
            self.game.state_manager.change_state("GameWon")

    def render(self):
        self.game.screen.fill(BACKGROUND_COLOR)
        self.all_sprites.draw(self.game.screen)
        self.blocks.draw(self.game.screen)
        score_text = self.font.render(f"Score: {self.score}", True, (255, 255, 255))
        self.game.screen.blit(score_text, (10, 10))
        elapsed_time_text = self.font.render(f"Time Elapsed: {int((datetime.now() - self.start_time).total_seconds())}", True,
                                      (255, 255, 255))
        self.game.screen.blit(elapsed_time_text, (10, 35))
        pygame.display.flip()
