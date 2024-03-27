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
            if event.key == pygame.K_a:
                game.giveHint()
            if event.key == pygame.K_LEFT:
                game.changeAlgorithm(-1)
            if event.key == pygame.K_RIGHT:
                game.changeAlgorithm(1)
            if event.key == pygame.K_UP:
                game.changeMaxDepth(1)
            if event.key == pygame.K_DOWN:
                game.changeMaxDepth(-1)
            if event.key == pygame.K_h:
                game.changeHeuristic()
            if event.key == pygame.K_p:
                game.changeHeuristicWeight(0.2)
            if event.key == pygame.K_l:
                game.changeHeuristicWeight(-0.2)

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