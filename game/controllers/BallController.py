import time

from game.storage.Storage import PLATE_HEIGHT, BALL_SPEED, GAME_WIDTH


class BallController:
    def __init__(self, ball, game, ball_speed):
        self.ball = ball
        self.game = game
        self.speed_x, self.speed_y = ball_speed, -ball_speed
        self.is_on_plate_flag = False

    def update(self):
        if (
                self.ball.rect.left < 0
                or
                self.ball.rect.right > GAME_WIDTH
        ):
            self.speed_x *= -1

        if self.ball.rect.top < 0:
            self.speed_y *= -1

        if self.ball.rect.bottom > self.ball.area.bottom - PLATE_HEIGHT and not self.is_on_plate_flag:
            return True

        self.ball.rect.move_ip(self.speed_x, self.speed_y)
        return False

    # def

    def is_on_plate(self, plate):
        # # this was just reversing the direction of the ball
        # if self.ball.rect.colliderect(plate.rect):
        #     if not self.is_on_plate_flag:
        #         self.speed_y *= -1
        #     self.is_on_plate_flag = True
        # else:
        #     self.is_on_plate_flag = False

        # # High acceleration
        #
        # if self.ball.rect.colliderect(plate.rect):
        #     collision_point = self.ball.rect.centerx - plate.rect.centerx
        #
        #     normalized_collision_point = collision_point / (plate.rect.width / 2)
        #
        #
        #     max_bounce_angle = 30
        #     self.speed_x = normalized_collision_point * max_bounce_angle
        #
        #
        #     if not self.is_on_plate_flag:
        #         self.speed_y *= -1
        #
        #     self.is_on_plate_flag = True
        # else:
        #     self.is_on_plate_flag = False

        if self.ball.rect.colliderect(plate.rect):
            # This calculates the horizontal distance between the center of the ball and plate
            # If it is positive => the ball hit the plate on the right side
            # Else => the ball hit the plate on the left side
            collision_point = self.ball.rect.centerx - plate.rect.centerx
            # Now I normalize the collision point, so it stays between -1 and 1
            # By dividing it with half of the plate's width it will stay inside this interval
            # From what I've read this should help with consistency if I change the paddle size
            normalized_collision_point = collision_point / (plate.rect.width / 2)

            # Here I'm limiting the max speed change of the ball after the collision
            # Basically after normalizing it (as well as before)
            # The collision point has the highest values near the edges/extremes
            max_speed_change = 10
            speed_change = normalized_collision_point * max_speed_change

            self.speed_x += speed_change
            # Here I also set some limits for the max speed as well as min speed for the ball
            # So I choose the minimum between the current speed and the default ball speed
            # After this I choose the max out of the previous min and the negative ball speed
            # Basically it never exceeds BALL SPEED, and it never goes below -BALL_SPEED
            self.speed_x = max(min(self.speed_x, BALL_SPEED), -BALL_SPEED)

            if not self.is_on_plate_flag:
                self.speed_y *= -1

            self.is_on_plate_flag = True
        else:
            self.is_on_plate_flag = False
