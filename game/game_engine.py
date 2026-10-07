import pygame
import random
from .hole import Hole


# Colors
DARK_BROWN = (60, 40, 20)
MOLE_BROWN = (140, 95, 55)
BLACK = (0, 0, 0)
WHITE = (255, 255, 255)
GRAY = (180, 180, 180)


class GameEngine:
    def __init__(self, width, height, rows=3, cols=3):
        self.width = width
        self.height = height

        self.rows = rows
        self.cols = cols

        self.holes = []
        spacing_x = width // (cols + 1)
        spacing_y = (height - 80) // (rows + 1)

        for r in range(rows):
            for c in range(cols):
                cx = spacing_x * (c + 1)
                cy = 80 + spacing_y * (r + 1)
                self.holes.append(Hole(cx, cy))

        # Default difficulty
        self.difficulty = "Medium"

        self.round_seconds = 30

        self.score = 0
        self.misses = 0
        self.game_over = False

        self.font = pygame.font.SysFont("Arial", 28)
        self.game_over_font = pygame.font.SysFont("Arial", 48)
        self.final_score_font = pygame.font.SysFont("Arial", 36)
        self.menu_font = pygame.font.SysFont("Arial", 26)
        self.small_font = pygame.font.SysFont("Arial", 22)

        self._set_difficulty("Medium")
        self._reset_timer()

    def _set_difficulty(self, difficulty):
        self.difficulty = difficulty

        if difficulty == "Easy":
            self.spawn_chance = 0.012
            self.mole_up_frames = 70

        elif difficulty == "Medium":
            self.spawn_chance = 0.02
            self.mole_up_frames = 45

        elif difficulty == "Hard":
            self.spawn_chance = 0.035
            self.mole_up_frames = 30

    def _reset_timer(self):
        self.time_left_frames = self.round_seconds * 60

    def reset_game(self, difficulty):
        # Apply selected difficulty.
        self._set_difficulty(difficulty)

        # Reset score and misses.
        self.score = 0
        self.misses = 0

        # Reset timer.
        self._reset_timer()

        # Start the game again.
        self.game_over = False

        # Hide all existing moles.
        for hole in self.holes:
            hole.active = False
            hole.timer = 0

    def handle_event(self, event):
        # Game-over input is handled separately by main.py.
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

            # Check if click is inside the mole.
            if dx * dx + dy * dy <= hole.mole_radius * hole.mole_radius:
                if hole.whack():
                    self.score += 1
                    hit_something = True
                    break

        if not hit_something:
            self.misses += 1

    def handle_input(self):
        pass

    def update(self):
        if self.game_over:
            return

        self.time_left_frames -= 1

        if self.time_left_frames <= 0:
            self.time_left_frames = 0
            self.game_over = True

            # Hide all moles.
            for hole in self.holes:
                hole.active = False
                hole.timer = 0

            return

        for hole in self.holes:
            hole.update()

            if not hole.active and random.random() < self.spawn_chance:
                hole.pop_up(self.mole_up_frames)

    def render(self, screen):
        # Draw holes and moles.
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

        # Score.
        score_text = self.font.render(
            f"Score: {self.score}",
            True,
            BLACK
        )
        screen.blit(score_text, (10, 10))

        # Timer.
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

        # Difficulty.
        difficulty_text = self.small_font.render(
            f"Difficulty: {self.difficulty}",
            True,
            BLACK
        )
        screen.blit(
            difficulty_text,
            (10, 45)
        )

        # Game-over/replay menu.
        if self.game_over:
            self._render_game_over(screen)

    def _render_game_over(self, screen):
        # Dark transparent overlay.
        overlay = pygame.Surface(
            (self.width, self.height),
            pygame.SRCALPHA
        )
        overlay.fill((0, 0, 0, 180))
        screen.blit(overlay, (0, 0))

        # GAME OVER.
        game_over_text = self.game_over_font.render(
            "GAME OVER",
            True,
            WHITE
        )

        game_over_rect = game_over_text.get_rect(
            center=(self.width // 2, 120)
        )

        screen.blit(game_over_text, game_over_rect)

        # Final score.
        final_score_text = self.final_score_font.render(
            f"Final Score: {self.score}",
            True,
            WHITE
        )

        final_score_rect = final_score_text.get_rect(
            center=(self.width // 2, 180)
        )

        screen.blit(final_score_text, final_score_rect)

        # Replay instructions.
        menu_title = self.menu_font.render(
            "Choose Difficulty",
            True,
            WHITE
        )

        menu_title_rect = menu_title.get_rect(
            center=(self.width // 2, 240)
        )

        screen.blit(menu_title, menu_title_rect)

        # Difficulty options.
        easy_text = self.menu_font.render(
            "1 - Easy",
            True,
            WHITE
        )

        medium_text = self.menu_font.render(
            "2 - Medium",
            True,
            WHITE
        )

        hard_text = self.menu_font.render(
            "3 - Hard",
            True,
            WHITE
        )

        exit_text = self.menu_font.render(
            "4 - Exit",
            True,
            WHITE
        )

        easy_rect = easy_text.get_rect(
            center=(self.width // 2, 290)
        )

        medium_rect = medium_text.get_rect(
            center=(self.width // 2, 330)
        )

        hard_rect = hard_text.get_rect(
            center=(self.width // 2, 370)
        )

        exit_rect = exit_text.get_rect(
            center=(self.width // 2, 410)
        )

        screen.blit(easy_text, easy_rect)
        screen.blit(medium_text, medium_rect)
        screen.blit(hard_text, hard_rect)
        screen.blit(exit_text, exit_rect)

        instruction_text = self.small_font.render(
            "Press 1, 2, 3 or 4",
            True,
            GRAY
        )

        instruction_rect = instruction_text.get_rect(
            center=(self.width // 2, 460)
        )

        screen.blit(instruction_text, instruction_rect)