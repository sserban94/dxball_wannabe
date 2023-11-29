import random

import pygame
from pygame import QUIT, KEYDOWN, K_LEFT, K_a, K_RIGHT, K_d

from game.elements.Ball import Ball
from game.elements.Block import Block
from game.elements.Plate import Plate
from game.states.GameState import GameState
from game.storage.Storage import BLOCK_WIDTH, BLOCK_HEIGHT, GAME_WIDTH, BLOCK_DISTANCE_FROM_LATERAL_WALL, \
    BLOCK_ENDING_DISTANCE_FROM_TOP, BLOCK_STARTING_DISTANCE_FROM_TOP, BLOCK_EMPTY_SPACE, DELAY, INTERVAL, \
    BACKGROUND_COLOR


class PlayState(GameState):
    def __init__(self, game):
        super().__init__(game)
        self.ball = Ball(game)
        self.plate = Plate(game.resource_manager)
        self.all_sprites = pygame.sprite.Group(self.ball, self.plate)
        self.blocks = self.position_block(game.resource_manager)

    def position_block(self, resource_manager):
        blocks = pygame.sprite.RenderPlain()
        block_width = BLOCK_WIDTH  # Adjust this to change the block size
        block_height = BLOCK_HEIGHT
        game_width = GAME_WIDTH
        left_margin = BLOCK_DISTANCE_FROM_LATERAL_WALL
        right_margin = BLOCK_DISTANCE_FROM_LATERAL_WALL
        block_start_height = BLOCK_ENDING_DISTANCE_FROM_TOP  # Adjust this to change the starting height of the blocks
        x = left_margin
        while x <= game_width - right_margin:
            y = BLOCK_STARTING_DISTANCE_FROM_TOP
            while y <= block_start_height:
                block = Block(resource_manager, x, y)
                to_be_or_not_to_be = [True, False]
                if random.choice(to_be_or_not_to_be):
                    blocks.add(block)
                y += block_height + BLOCK_EMPTY_SPACE
                # y += block_height + random.choice(BLOCK_EMPTY_SPACE_LIST)
            x += block_width + BLOCK_EMPTY_SPACE
            # x += block_width + random.choice(BLOCK_EMPTY_SPACE_LIST)
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
        if pygame.sprite.spritecollide(self.ball, self.blocks, True):
            self.ball.speed_y *= -1

    def render(self):
        self.game.screen.fill(BACKGROUND_COLOR)
        self.all_sprites.draw(self.game.screen)
        self.blocks.draw(self.game.screen)
        pygame.display.flip()
