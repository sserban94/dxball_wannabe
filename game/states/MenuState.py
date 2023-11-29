import pygame
from pygame import KEYDOWN, K_UP, K_DOWN, K_RETURN, QUIT

from game.storage.Storage import BLACK
from game.states.PlayState import PlayState
from game.states.GameState import GameState
from game.storage.Storage import FONT_VALUES, WHITE, PLAY_OPTION_POSITION, QUIT_OPTION_POSITION, GREY


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
        self.game.screen.fill(BLACK)
        play_color = WHITE if self.selected_option == 0 else GREY
        quit_color = WHITE if self.selected_option == 1 else GREY
        play_text = self.font.render("Play", True, play_color)
        quit_text = self.font.render("Quit", True, quit_color)
        self.game.screen.blit(play_text, self.play_rect)
        self.game.screen.blit(quit_text, self.quit_rect)
        pygame.display.flip()
