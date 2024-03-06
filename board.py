import pygame

class Board:
    def __init__(self):
        self.board = [[False for _ in range(9)] for _ in range(9)]  # False indicates no ball, True indicates a ball

    def draw(self, screen):
        # Fill the screen with a color
        screen.fill((0, 0, 128))  # Fill the screen with navy blue

        # Draw the game board
        MARGIN = 20
        cell_size = min((screen.get_width() - 2 * MARGIN) // 9, (screen.get_height() - 2 * MARGIN) // 9)
        for i in range(9):
            for j in range(9):
                pygame.draw.rect(screen, (255, 255, 255), pygame.Rect(MARGIN + j*cell_size, MARGIN + i*cell_size, cell_size, cell_size), 1)
                if self.board[i][j]:  # If there is a ball in this cell
                    pygame.draw.circle(screen, (255, 0, 0), (MARGIN + j*cell_size + cell_size // 2, MARGIN + i*cell_size + cell_size // 2), cell_size // 2 - 5)