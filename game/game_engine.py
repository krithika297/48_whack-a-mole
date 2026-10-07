import pygame
import random
from .hole import Hole


# Colors
DARK_BROWN = (60, 40, 20)
MOLE_BROWN = (140, 95, 55)
BLACK = (0, 0, 0)
WHITE = (255, 255, 255)


class GameEngine:
    def __init__(self, width, height, rows=3, cols=3):
        self.width = width
        self.height = height

        self.holes = []
        spacing_x = width // (cols + 1)
        spacing_y = (height - 80) // (rows + 1)

        for r in range(rows):
            for c in range(cols):
                cx = spacing_x * (c + 1)
                cy = 80 + spacing_y * (r + 1)
                self.holes.append(Hole(cx, cy))

        self.spawn_chance = 0.02
        self.mole_up_frames = 45

        self.round_seconds = 30
        self.time_left_frames = self.round_seconds * 60

        self.score = 0
        self.misses = 0

        self.font = pygame.font.SysFont("Arial", 28)
        self.game_over_font = pygame.font.SysFont("Arial", 48)
        self.final_score_font = pygame.font.SysFont("Arial", 36)
        self.instruction_font = pygame.font.SysFont("Arial", 24)

        self.game_over = False

    def handle_event(self, event):
        # When the game is over, ignore game clicks.
        if self.game_over:
            return

        if event.type == pygame.MOUSEBUTTONDOWN:
            self._handle_click(event.pos)

    def _handle_click(self, pos):
        hit_something = False

        for hole in self.holes:
            if not hole.active:
                continue

            dx = pos[0] - hole.center_x
            dy = pos[1] - hole.center_y

            if dx * dx + dy * dy <= hole.mole_radius * hole.mole_radius:
                if hole.whack():
                    self.score += 1
                    hit_something = True
                    break

        if not hit_something:
            self.misses += 1

    def handle_input(self):
        # Mouse events are handled in handle_event().
        pass

    def update(self):
        if self.game_over:
            return

        self.time_left_frames -= 1

        # End the game when the timer reaches zero.
        if self.time_left_frames <= 0:
            self.time_left_frames = 0
            self.game_over = True

            # Hide all active moles.
            for hole in self.holes:
                hole.active = False
                hole.timer = 0

            return

        for hole in self.holes:
            hole.update()

            if not hole.active and random.random() < self.spawn_chance:
                hole.pop_up(self.mole_up_frames)

    def render(self, screen):
        # Draw the normal game screen.
        for hole in self.holes:
            pygame.draw.circle(
                screen,
                DARK_BROWN,
                (hole.center_x, hole.center_y),
                40
            )

            if hole.active:
                pygame.draw.circle(
                    screen,
                    MOLE_BROWN,
                    (hole.center_x, hole.center_y),
                    hole.mole_radius
                )

        score_text = self.font.render(
            f"Score: {self.score}",
            True,
            BLACK
        )
        screen.blit(score_text, (10, 10))

        seconds_left = max(0, self.time_left_frames // 60)

        timer_text = self.font.render(
            f"Time: {seconds_left}s",
            True,
            BLACK
        )
        screen.blit(
            timer_text,
            (self.width - 140, 10)
        )

        # Show game-over screen after the timer reaches zero.
        if self.game_over:
            self._render_game_over(screen)

    def _render_game_over(self, screen):
        # Dark overlay over the game.
        overlay = pygame.Surface(
            (self.width, self.height),
            pygame.SRCALPHA
        )
        overlay.fill((0, 0, 0, 170))
        screen.blit(overlay, (0, 0))

        # Game Over text.
        game_over_text = self.game_over_font.render(
            "GAME OVER",
            True,
            WHITE
        )

        game_over_rect = game_over_text.get_rect(
            center=(self.width // 2, 180)
        )

        screen.blit(game_over_text, game_over_rect)

        # Final score.
        final_score_text = self.final_score_font.render(
            f"Final Score: {self.score}",
            True,
            WHITE
        )

        final_score_rect = final_score_text.get_rect(
            center=(self.width // 2, 250)
        )

        screen.blit(final_score_text, final_score_rect)

        # Instruction.
        instruction_text = self.instruction_font.render(
            "Press any key or click to exit",
            True,
            WHITE
        )

        instruction_rect = instruction_text.get_rect(
            center=(self.width // 2, 320)
        )

        screen.blit(instruction_text, instruction_rect)