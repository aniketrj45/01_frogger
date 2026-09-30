"""
Frog: the player-controlled character. Moves in discrete grid hops,
one cell per key press - not continuous pixel movement.
"""

import pygame


class Frog:
    def __init__(self, col, row, start_col, start_row, cols, start_row_limit):
        self.col = col
        self.row = row
        self.start_col = start_col
        self.start_row = start_row
        self.cols = cols
        self.start_row_limit = start_row_limit

    def move(self, dcol, drow):
        new_col = self.col + dcol
        new_row = self.row + drow
        if 0 <= new_col < self.cols:
            self.col = new_col
        if 0 <= new_row <= self.start_row_limit:
            self.row = new_row

    def reset(self):
        self.col = self.start_col
        self.row = self.start_row

    def get_rect(self, cell_size, pad=4):
        return pygame.Rect(
            self.col * cell_size + pad,
            self.row * cell_size + pad,
            cell_size - 2 * pad,
            cell_size - 2 * pad,
        )
