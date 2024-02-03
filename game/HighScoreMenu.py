# import json
#
# class HighScoreMenu:
#     def __init__(self, file_path):
#         self.file_path = file_path
#         self.high_scores = self.load_high_scores()
#
#     def load_high_scores(self):
#         try:
#             with open(self.file_path, 'r') as file:
#                 return json.load(file)
#         except FileNotFoundError:
#             return []
#
#     def save_high_scores(self):
#         with open(self.file_path, 'w') as file:
#             json.dump(self.high_scores, file)
#
#     def add_score(self, score):
#         self.high_scores.append(score)
#         self.high_scores.sort(reverse=True)
#         # Keep only the first ten high scores for now
#         self.high_scores = self.high_scores[:10]
#         self.save_high_scores()
#
#     def display(self):
#         print("High Scores:")
#         for i, score in enumerate(self.high_scores, start=1):
#             print(f"{i}. {score}")