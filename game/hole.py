import pygame


class Hole:
    def __init__(self, center_x, center_y):
        self.center_x = center_x
        self.center_y = center_y

        # Size of the actual mole.
        self.mole_radius = 32

        self.active = False
        self.timer = 0

    def pop_up(self, duration_frames):
        self.active = True
        self.timer = duration_frames

    def update(self):
        if self.active:
            self.timer -= 1

            if self.timer <= 0:
                self.active = False

    def whack(self):
        if self.active:
            self.active = False
            self.timer = 0
            return True

        return False