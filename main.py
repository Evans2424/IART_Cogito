from game import Game, GameState
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
        if event.type == pygame.MOUSEBUTTONDOWN:
            x, y = pygame.mouse.get_pos()
            game.checkButtons(x, y)
        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_s:
                game.resolveLevel()
            if event.key == pygame.K_h:
                game.giveHint()

    # Draw everything
    game.draw()
    # Swap buffers
    pygame.display.flip()

    # Update the game
    won = game.update()
    if won:
        # End the game
        print("You won the game!")
        running = False

    # Cap the frame rate
    pygame.time.Clock().tick(FPS)

# Quit Pygame
pygame.quit()