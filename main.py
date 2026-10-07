import pygame
from game.game_engine import GameEngine


# Initialize pygame
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

            elif engine.game_over:
                if event.type == pygame.KEYDOWN:

                    if event.key == pygame.K_1:
                        engine.reset_game("Easy")

                    elif event.key == pygame.K_2:
                        engine.reset_game("Medium")

                    elif event.key == pygame.K_3:
                        engine.reset_game("Hard")

                    elif event.key == pygame.K_4:
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
    main()import pygame
from game.game_engine import GameEngine


# Initialize pygame
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

            elif engine.game_over:
                if event.type == pygame.KEYDOWN:

                    if event.key == pygame.K_1:
                        engine.reset_game("Easy")

                    elif event.key == pygame.K_2:
                        engine.reset_game("Medium")

                    elif event.key == pygame.K_3:
                        engine.reset_game("Hard")

                    elif event.key == pygame.K_4:
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