from board import Board
import pygame
import goal_states

import random


class GameState:
    """
    GameState contains the current state of the game. 
    It stores the board, the level and the score (number of movements in the current level).
    """

    def __init__(self, board, level, score):
        """ board is a Board object, level is an integer between 1 as 12 and score is an integer >= 0 """
        if not isinstance(board, Board):
            raise ValueError("board must be an instance of Board")
        if not (isinstance(level, int) and 1 <= level <= 12):
            raise ValueError("level must be an integer between 1 and 12")
        if not (isinstance(score, int) and score >= 0):
            raise ValueError("score must be a non-negative integer")

        self.board = board
        self.level = level
        self.score = score

    def isGoalState(self):
        """ Check if the current board's matrix is the same as the goal matrix for the current level """
        return self.board.matrix == goal_states.getGoalMatrix(self.level)


class Game:
    def __init__(self, screen):
        self.screen = screen
        self.state = GameState(Board([[0 for _ in range(9)] for _ in range(9)]), 1, 0)

    def update(self):
        pass

    def draw(self):
        # Draw everything
        self.state.board.draw(self.screen, goal_states.getGoalMatrix(self.state.level))

