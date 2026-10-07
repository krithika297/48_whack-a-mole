import pygame
from game.game_engine import GameEngine


# Initialize pygame/Start application
pygame.init()

# Screen dimensions
WIDTH, HEIGHT = 500, 560
SCREEN = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("Whack-a-Mole - Pygame Version")

# Colors
GRASS_GREEN = (120, 170, 90)

# Clock
clock = pygame.time.Clock()
FPS = 60

# Game engine
engine = GameEngine(WIDTH, HEIGHT)


def main():
    running = True

    while running:
        SCREEN.fill(GRASS_GREEN)

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False

            # After game over, any key or mouse click exits the game.
            elif engine.game_over:
                if (
                    event.type == pygame.KEYDOWN
                    or event.type == pygame.MOUSEBUTTONDOWN
                ):
                    running = False

            else:
                engine.handle_event(event)

        engine.handle_input()
        engine.update()
        engine.render(SCREEN)

        pygame.display.flip()
        clock.tick(FPS)

    pygame.quit()


if __name__ == "__main__":
    main()