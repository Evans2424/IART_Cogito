import pygame
from constants import MARGIN, cellSize

class Board:
    def __init__(self, matrix):
        self.matrix = matrix

    def shiftRow(self, row, num):
        """ Shift the row by num positions to the right. If num is negative, shift to the left. """
        new_matrix = self.matrix.copy()
        new_matrix[row] = new_matrix[row][-num:] + new_matrix[row][:-num]
        return Board(new_matrix)

    def shiftColumn(self, col, num):
        """ Shift the column by num positions down. If num is negative, shift up. """
        new_matrix = list(zip(*self.matrix))
        new_matrix[col] = new_matrix[col][-num:] + new_matrix[col][:-num]
        new_matrix = list(zip(*new_matrix))
        return Board(new_matrix)

    def __str__(self):
        return "\n".join(" ".join(str(cell) for cell in row) for row in self.matrix)
    
    def draw(self, screen, goalMatrix):
        for i in range(9):
            for j in range(9):
                borderColor = (255, 255, 255) if goalMatrix[i][j] else (0, 0, 0)  # If the cell is part of the goal state, draw its borders white otherwise black
                pygame.draw.rect(screen, borderColor, pygame.Rect(2*MARGIN + j*cellSize, 2*MARGIN + i*cellSize, cellSize, cellSize), 1)
                if self.matrix[i][j]:  # If there is a ball in this cell
                    ballColor = (255, 0, 0) # Red balls 
                    pygame.draw.circle(screen, ballColor, (2*MARGIN + j*cellSize + cellSize // 2, 2*MARGIN + i*cellSize + cellSize // 2), cellSize // 2 - 5)