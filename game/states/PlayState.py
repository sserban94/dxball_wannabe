import random

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
    BACKGROUND_COLOR, PLAY_STATE_MUSIC_FILENAME


class PlayState(GameState):
    def __init__(self, game):
        super().__init__(game)
        self.ball = Ball(self.game)
        self.ball_controller = BallController(self.ball, self.game)
        self.plate = Plate(self.game)
        self.plate_controller = PlateController(self.plate, self.game)
        self.all_sprites = pygame.sprite.Group(self.ball, self.plate)
        self.blocks = None
        self.position_block()
        self.score = 0
        self.font = pygame.font.Font(None, 36)
        self.block_count = 0
        self.music = self.game.resource_manager.load_sound(PLAY_STATE_MUSIC_FILENAME)
        self.music.play(-1)

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
                pygame.quit()
            elif event.type == KEYDOWN:
                if event.key == K_LEFT or event.key == K_a:
                    self.plate.move_left()
                elif event.key == K_RIGHT or event.key == K_d:
                    self.plate.move_right()

    def update(self):
        if self.ball_controller.update():
            self.music.stop()
            self.game.state = GameOverState(self.game)
        self.ball_controller.is_on_plate(self.plate)

        # this should get the no of sprites which collided
        collided_sprites = pygame.sprite.spritecollide(self.ball, self.blocks, True)
        if collided_sprites:
            self.ball_controller.speed_y *= -1
            self.score += len(collided_sprites)

        if len(self.blocks) == 0:
            self.game.state = GameWonState(self.game)

    def render(self):
        self.game.screen.fill(BACKGROUND_COLOR)
        self.all_sprites.draw(self.game.screen)
        self.blocks.draw(self.game.screen)
        score_text = self.font.render(f"Score: {self.score}", True, (255, 255, 255))
        self.game.screen.blit(score_text, (10, 10))
        pygame.display.flip()
