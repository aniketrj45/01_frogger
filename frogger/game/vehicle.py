"""
Vehicle: a car/truck on a road lane. Moves continuously in pixel space
(not grid-snapped like the frog), wraps around when it exits the screen.
"""

import pygame


class Vehicle:
    def __init__(self, x, row, width, height, speed):
        self.x = float(x)
        self.row = row
        self.width = width
        self.height = height
        self.speed = speed

    def update(self, road_width_px):
        self.x += self.speed
        if self.speed > 0 and self.x > road_width_px:
            self.x = -self.width
        elif self.speed < 0 and self.x < -self.width:
            self.x = road_width_px

    def get_rect(self, cell_size, pad=4):
        return pygame.Rect(
            int(self.x),
            self.row * cell_size + pad,
            self.width,
            cell_size - 2 * pad,
        )
