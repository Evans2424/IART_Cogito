from board import Board
import pygame

import random

class Game:
    def __init__(self, screen):
        self.screen = screen
        self.board = Board()
        self.ball_count = 0  # Add a counter for the number of balls

    def update(self):
        # Randomly place a ball in an empty cell, but only if there are less than 9 balls
        if self.ball_count < 9:
            empty_cells = [(i, j) for i in range(9) for j in range(9) if not self.board.board[i][j]]
            if empty_cells:
                i, j = random.choice(empty_cells)
                self.board.board[i][j] = True
                self.ball_count += 1  # Increment the ball count

    def draw(self):
        # Draw everything
        self.board.draw(self.screen)