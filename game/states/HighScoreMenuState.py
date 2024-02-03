import pygame
from pygame import KEYDOWN, QUIT

from game.HighScoreManager import HighScoreManager
from game.states.GameState import GameState
from game.storage.Storage import FONT_VALUES, CONTINUE_POSITION, RED, WHITE, BLACK, DELAY, INTERVAL, GAME_WIDTH


class HighScoreMenuState(GameState):
    def __init__(self, game):
        super().__init__(game)
        self.high_score_menu = HighScoreManager(game)
        self.title_font = pygame.font.Font(FONT_VALUES['font_type'], FONT_VALUES['font_size'] * 2)
        self.title_text = self.title_font.render("High Scores", True, RED)
        self.title_rect = self.title_text.get_rect(center=(GAME_WIDTH // 2, 50))

        self.score_font = pygame.font.Font(FONT_VALUES['font_type'], FONT_VALUES['font_size'])
        self.score_texts = [self.score_font.render(f"{i + 1}. {score}", True, WHITE) for i, score in
                            enumerate(
                                sorted(self.high_score_menu.high_score_json_data,
                                       key=lambda x: (-x['blocks'], x['time'])
                                       )

                            )]
        self.score_rects = [text.get_rect(center=(GAME_WIDTH // 2, 100 + i * 30)) for i, text in
                            enumerate(self.score_texts)]

        self.continue_font = pygame.font.Font(FONT_VALUES['font_type'], FONT_VALUES['font_size'])
        self.continue_text = self.continue_font.render("Press any key to continue", True, WHITE)
        self.continue_rect = self.continue_text.get_rect(center=CONTINUE_POSITION)

    def handle_events(self):
        from game.states.MenuState import MenuState
        pygame.key.set_repeat(DELAY, INTERVAL)
        for event in pygame.event.get():
            if event.type == QUIT:
                pygame.quit()
            elif event.type == KEYDOWN:
                pygame.time.delay(500)
                pygame.event.clear()
                return

    def update(self):
        pass

    def render(self):
        self.game.screen.fill(BLACK)
        self.game.screen.blit(self.title_text, self.title_rect)
        for text, rect in zip(self.score_texts, self.score_rects):
            self.game.screen.blit(text, rect)
        self.game.screen.blit(self.continue_text, self.continue_rect)
        pygame.display.flip()
