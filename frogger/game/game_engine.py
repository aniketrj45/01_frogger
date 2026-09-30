"""
GameEngine: owns the frog and all vehicles, and runs one frame's worth
of game logic.
"""

import random

import pygame
from game.frog import Frog
from game.vehicle import Vehicle
from game.collisions import check_collision
from game.renderer import (
    GRID_COLS, GOAL_ROW, ROAD_ROWS, START_ROW, CELL_SIZE, WIDTH, HEIGHT,
)

LANE_SPEEDS = [1.5, -2, 2, -2.5, 1.5, -2]
STARTING_LIVES = 3
STARTING_SCORE = 0
ATTEMPT_SECONDS = 30
HIT_DELAY_FRAMES = 30


class GameEngine:
    def __init__(self):
        self.lives = STARTING_LIVES
        self.hit_timer = 0
        self.score = STARTING_SCORE
        self.won = False
        self.game_over = False
        self.attempt_started_at = pygame.time.get_ticks()
        self._build_entities()

    def _build_entities(self):
        start_col = GRID_COLS // 2
        self.frog = Frog(
            col=start_col, row=START_ROW,
            start_col=start_col, start_row=START_ROW,
            cols=GRID_COLS, start_row_limit=START_ROW,
        )
        frog_x_range = (start_col * CELL_SIZE, start_col * CELL_SIZE + CELL_SIZE)
        self.vehicles = []
        for i, row in enumerate(ROAD_ROWS):
            speed = LANE_SPEEDS[i % len(LANE_SPEEDS)]
            vehicle_width = 40 if i % 2 == 0 else 70
            spacing = 300
            count = 2
            for _attempt in range(20):
                phase = random.randint(0, spacing - 1)
                positions = []
                safe = True
                for n in range(count):
                    offset = phase + n * spacing
                    x = offset if speed > 0 else WIDTH - offset - vehicle_width
                    positions.append(x)
                    if not (x + vehicle_width <= frog_x_range[0] or x >= frog_x_range[1]):
                        safe = False
                if safe:
                    break
            for x in positions:
                self.vehicles.append(Vehicle(x=x, row=row, width=vehicle_width,
                                              height=CELL_SIZE - 8, speed=speed))

    def _start_attempt(self):
        self.frog.reset()
        self.hit_timer = 0
        self.attempt_started_at = pygame.time.get_ticks()

    def _remaining_seconds(self):
        elapsed_ms = pygame.time.get_ticks() - self.attempt_started_at
        remaining_ms = max(0, ATTEMPT_SECONDS * 1000 - elapsed_ms)
        return (remaining_ms + 999) // 1000

    def handle_keydown(self, key):
        if key == pygame.K_r:
            self.lives = STARTING_LIVES
            self.hit_timer = 0
            self.score = STARTING_SCORE
            self.won = False
            self.game_over = False
            self._build_entities()
            self.attempt_started_at = pygame.time.get_ticks()
            return

        if self.lives <= 0 or self.hit_timer > 0 or self.won or self.game_over:
            return

        if key == pygame.K_UP:
            self.frog.move(0, -1)
        elif key == pygame.K_DOWN:
            self.frog.move(0, 1)
        elif key == pygame.K_LEFT:
            self.frog.move(-1, 0)
        elif key == pygame.K_RIGHT:
            self.frog.move(1, 0)

    def update(self):
        if self.lives <= 0 or self.won or self.game_over:
            return

        for v in self.vehicles:
            v.update(road_width_px=WIDTH)

        if self.hit_timer > 0:
            self.hit_timer -= 1
            if self.hit_timer == 0:
                self._start_attempt()
            return

        # A real vehicle overlap ends the current attempt.
        if check_collision(self.frog, self.vehicles):
            self.lives -= 1
            self.hit_timer = HIT_DELAY_FRAMES
            return

        # Goal takes priority over timeout: reaching it before the timer expires wins.
        if self.frog.row == GOAL_ROW:
            self.score += 1
            self.won = True
            return

        # Calculate timeout from real elapsed time rather than frame count.
        if self._remaining_seconds() <= 0:
            self.lives -= 1
            if self.lives <= 0:
                self.game_over = True
                return
            self._start_attempt()

    def draw(self, surface, font):
        from game import renderer
        renderer.draw_scene(surface, self.frog, self.vehicles)
        renderer.draw_text(surface, font, f"Lives: {self.lives}", (10, 10))
        renderer.draw_text(surface, font, f"Score: {self.score}", (10, 34))
        if self.won:
            renderer.draw_banner(surface, font, "You Won!")
        elif self.game_over or self.lives <= 0:
            renderer.draw_banner(surface, font, "Game Over")
        elif self.hit_timer > 0:
            renderer.draw_banner(surface, font, "HIT!")
        else:
            renderer.draw_text(
                surface, font, f"Time: {self._remaining_seconds()}", (10, 58)
            )
        renderer.draw_text(surface, font, "Arrow keys to move. R to restart.", (10, HEIGHT - 24))
