import time

import pygame
from pygame import KEYDOWN, QUIT

from game.HighScoreManager import HighScoreManager
from game.states.GameState import GameState
from game.states.HighScoreMenuState import HighScoreMenuState
from game.storage.Storage import FONT_VALUES, CONTINUE_POSITION, GAME_WON_POSITION, RED, WHITE, BLACK, DELAY, INTERVAL, \
    GAME_WON_STATE_MUSIC_FILENAME


class GameWonState(GameState):
    def __init__(self, game):
        super().__init__(game)
        self.continue_rect = None
        self.continue_text = None
        self.continue_font = None
        self.game_over_rect = None
        self.game_over_text = None
        self.game_over_font = None
        self.music = None

    def enter(self):
        self.music = self.game.resource_manager.load_sound(GAME_WON_STATE_MUSIC_FILENAME)
        self.music.play()

        self.game_over_font = pygame.font.Font(FONT_VALUES['font_type'], FONT_VALUES['font_size'] * 2)
        self.game_over_text = self.game_over_font.render("CONGRATULATIONS YOU HAVE NO LIFE", True, RED)
        self.game_over_rect = self.game_over_text.get_rect(center=GAME_WON_POSITION)

        self.continue_font = pygame.font.Font(FONT_VALUES['font_type'], FONT_VALUES['font_size'])
        self.continue_text = self.continue_font.render("Press any key to continue", True, WHITE)
        self.continue_rect = self.continue_text.get_rect(center=CONTINUE_POSITION)

    def exit(self):
        self.music.stop()

    def handle_events(self):
        # TODO - add score to db
        from game.states.MenuState import MenuState
        pygame.key.set_repeat(DELAY, INTERVAL)
        for event in pygame.event.get():
            if event.type == QUIT:
                self.game.high_score_manager.save_high_scores()
                pygame.quit()
            elif event.type == KEYDOWN:
                # added a delay because it was annoying to have a sudden change in the UI
                # pygame.time.delay(500)
                time.sleep(0.2)
                # needed to clear the event because it was sending Enter to the next State
                pygame.event.clear()
                self.game.state_manager.change_state("Menu")

    def update(self):
        pass

    def render(self):
        self.game.screen.fill(BLACK)
        self.game.screen.blit(self.game_over_text, self.game_over_rect)
        self.game.screen.blit(self.continue_text, self.continue_rect)
        pygame.display.flip()