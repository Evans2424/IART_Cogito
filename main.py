from game import Game
from constants import WIDTH, HEIGHT, FPS
import pygame

# Initialize Pygame
pygame.init()

# Set up the display
screen = pygame.display.set_mode((WIDTH, HEIGHT))

# Initialize the game
game = Game(screen)

# Game loop
running = True
while running:
    # Event handling
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False

    # Update game state here
    game.update()

    # Draw everything
    game.draw()

    # Swap buffers
    pygame.display.flip()

    # Cap the frame rate
    pygame.time.Clock().tick(FPS)

# Quit Pygame
pygame.quit()