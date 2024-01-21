import pygame
from pygame import QUIT, KEYDOWN

from game.states.GameState import GameState
# from game.states.MenuState import MenuState
from game.storage.Storage import FONT_VALUES, RED, GAME_OVER_POSITION, CONTINUE_POSITION, DELAY, INTERVAL, BLACK, WHITE


class GameOverState(GameState):
    def __init__(self, game):
        super().__init__(game)
        self.game_over_font = pygame.font.Font(FONT_VALUES['font_type'], FONT_VALUES['font_size'] * 2)
        self.game_over_text = self.game_over_font.render("GAME OVER", True, RED)
        self.game_over_rect = self.game_over_text.get_rect(center=GAME_OVER_POSITION)

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
                # added a delay because it was annoying to have a sudden change in the UI
                pygame.time.delay(500)
                # needed to clear the event because it was sending Enter to the next State
                pygame.event.clear()
                self.game.state = MenuState(self.game)

    def update(self):
        pass

    def render(self):
        self.game.screen.fill(BLACK)
        self.game.screen.blit(self.game_over_text, self.game_over_rect)
        self.game.screen.blit(self.continue_text, self.continue_rect)
        pygame.display.flip()
