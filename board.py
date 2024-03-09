import pygame

class Board:
    def __init__(self, matrix):
        self.matrix = matrix

    def draw(self, screen, goalMatrix):
        # Fill the screen with a color
        screen.fill((128, 128, 128))

        # Draw the game board
        MARGIN = 20
        cell_size = min((screen.get_width() - 2 * MARGIN) // 9, (screen.get_height() - 2 * MARGIN) // 9)
        for i in range(9):
            for j in range(9):
                color = (255, 255, 255) if goalMatrix[i][j] else (0, 0, 0)
                pygame.draw.rect(screen, color, pygame.Rect(MARGIN + j*cell_size, MARGIN + i*cell_size, cell_size, cell_size), 1)
                if self.matrix[i][j]:  # If there is a ball in this cell
                    pygame.draw.circle(screen, (255, 0, 0), (MARGIN + j*cell_size + cell_size // 2, MARGIN + i*cell_size + cell_size // 2), cell_size // 2 - 5)

    def shiftRow(self, row, num):
        """ Shift the row by num positions to the right. If num is negative, shift to the left. """
        self.matrix[row] = self.matrix[row][-num:] + self.matrix[row][:-num]

    def shiftColumn(self, col, num):
        """ Shift the column by num positions down. If num is negative, shift up. """
        self.matrix = list(zip
        (*self.matrix))
        self.shiftRow(col, num)
        self.matrix = list(zip(*self.matrix))

    def __str__(self):
        return "\n".join(" ".join(str(cell) for cell in row) for row in self.matrix)
    
