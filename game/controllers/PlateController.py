from game.storage.Storage import PLATE_SPEED


class PlateController:
    def __init__(self, plate, game):
        self.plate = plate
        self.game = game

    def move_left(self):
        if not self.plate.rect.left - PLATE_SPEED < 0:
            newp_os = self.plate.rect.move((-PLATE_SPEED, 0))
            self.plate.rect = newp_os

    def move_right(self):
        if not self.plate.rect.right + PLATE_SPEED > self.plate.area.right:
            new_pos = self.plate.rect.move((PLATE_SPEED, 0))
            self.plate.rect = new_pos
