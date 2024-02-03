import time

import pygame
from pygame import QUIT, KEYDOWN

from game.states.GameState import GameState
# from game.states.MenuState import MenuState
from game.storage.Storage import FONT_VALUES, RED, GAME_OVER_POSITION, CONTINUE_POSITION, DELAY, INTERVAL, BLACK, WHITE, \
    GAME_OVER_MUSIC_FILENAME, DXBALL_OG_SOUNDS_FOLDER_NAME


class GameOverState(GameState):
    def __init__(self, game):
        super().__init__(game)
        self.game_over_font = None
        self.game_over_text = None
        self.game_over_rect = None
        self.continue_font = None
        self.continue_text = None
        self.continue_rect = None

    def enter(self):
        self.music = self.game.resource_manager.load_sound(GAME_OVER_MUSIC_FILENAME, DXBALL_OG_SOUNDS_FOLDER_NAME)
        self.music.play()

        self.game_over_font = pygame.font.Font(FONT_VALUES['font_type'], FONT_VALUES['font_size'] * 2)
        self.game_over_text = self.game_over_font.render("GAME OVER", True, RED)
        self.game_over_rect = self.game_over_text.get_rect(center=GAME_OVER_POSITION)

        self.continue_font = pygame.font.Font(FONT_VALUES['font_type'], FONT_VALUES['font_size'])
        self.continue_text = self.continue_font.render("Press any key to continue", True, WHITE)
        self.continue_rect = self.continue_text.get_rect(center=CONTINUE_POSITION)

    def exit(self):
        self.music.stop()

    def handle_events(self):
        from game.states.MenuState import MenuState
        pygame.key.set_repeat()
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
