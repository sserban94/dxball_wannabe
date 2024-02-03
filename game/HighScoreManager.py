import json

from game.storage.Storage import HIGHSCORES_FILENAME


class HighScoreManager:
    def __init__(self, game):
        self.game = game
        self.high_score_json_data = []
        self.load_high_scores()

    def load_high_scores(self):
        self.high_score_json_data.extend(self.game.resource_manager.load_highscores_data(HIGHSCORES_FILENAME))

    def save_high_scores(self):
        self.high_score_json_data = self.game.resource_manager.write_highscores_data(HIGHSCORES_FILENAME,
                                                                                    self.high_score_json_data)

    def add_score(self, score):
        self.high_score_json_data.append(score)

    # def display(self):
    #     print("High Scores:")
    #     for i, score in enumerate(self.high_score_json_data, start=1):
    #         print(f"{i}. {score}")
