from board import Board
from button import Button
from constants import MARGIN, cellSize
import pygame
import goal_states


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

    def piecesCorrectlyPositioned(self):
        """ Return the number of pieces that are in the correct position """
        return sum(self.board.matrix[i][j] and goal_states.getGoalMatrix(self.level)[i][j] for i in range(9) for j in range(9))

    def isGoalState(self):
        """ Return True if the board is in the goal state """
        return self.piecesCorrectlyPositioned() == 9
    
    @staticmethod
    def getGoalMatrix(level):
        return goal_states.getGoalMatrix(level)


class Game:

    def __init__(self, screen):
        self.screen = screen
        self.state = GameState(Board([[0 for _ in range(9)] for _ in range(9)]), 1, 0)
        self.buttons = [Button(i,j) for j in range(9) for i in range(4)]

    def update(self):
        for event in pygame.event.get():
            if event.type == pygame.MOUSEBUTTONDOWN:
                x, y = pygame.mouse.get_pos()
                for button in self.buttons:
                    if button.isClicked(x, y):
                        # Board will shift shRow units in the row of teh button + delta and shCol units in the column of the button + delta.
                        shRow, shCol, delta = button.getMove(self.state.level)
                        newBoard = self.state.board.shiftRow(button.index + delta, shRow).shiftColumn(button.index + delta, shCol)
                        self.state = GameState(newBoard, self.state.level, self.state.score + 1)

    def draw(self):
        # Fill the screen with a color
        self.screen.fill((128, 128, 128))

        # Draw the game board
        goalMatrix = GameState.getGoalMatrix(self.state.level)
        self.state.board.draw(self.screen, goalMatrix)

        # Create a font object
        font = pygame.font.Font(None, 36)

        # Render the level and score
        levelText = font.render(f"Level: {self.state.level}", True, (255, 255, 255))
        scoreText = font.render(f"Score: {self.state.score}", True, (255, 255, 255))

        # Draw the level and score on the right side of the board
        self.screen.blit(levelText, (2*MARGIN + 10*cellSize + 10, MARGIN))
        self.screen.blit(scoreText, (2*MARGIN + 10*cellSize + 10, MARGIN + 40))

        for button in self.buttons:
            button.draw(self.screen)


if __name__ == "__main__":
    matrix = [[0, 0, 0, 0, 0, 0, 0, 0, 0],
             [0, 0, 0, 0, 0, 0, 0, 0, 0],
             [0, 0, 0, 0, 0, 0, 0, 0, 0],
             [0, 0, 0, 1, 1, 1, 0, 0, 0],
             [0, 0, 0, 1, 1, 1, 0, 0, 0],
             [0, 0, 0, 1, 1, 1, 0, 0, 0],
             [0, 0, 0, 0, 0, 0, 0, 0, 0],
             [0, 0, 0, 0, 0, 0, 0, 0, 0],
             [0, 0, 0, 0, 0, 0, 0, 0, 0]]
    
    state = GameState(Board(matrix), 1, 0)
    print(state.piecesCorrectlyPositioned())
    print(state.isGoalState())

    button_side, button_index = 2, 4
    shRow, shCol, delta = Button(button_side, button_index).getMove(1)
    print(shRow, shCol, delta)
    newBoard = state.board.shiftRow(button_index + delta, shRow).shiftColumn(button_index + delta, shCol)
    print("NEW BOARD:")
    print(newBoard)

    # ITS WORKINNNNNNNNNNNNNNNNN

