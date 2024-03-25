from board import Board
from button import Button
from constants import MARGIN, cellSize
import pygame
import goal_states
import operators
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
        if not (isinstance(level, int) and 0 <= level <= 144):
            raise ValueError("level must be an integer between 1 and 143")
        if not (isinstance(score, int) and score >= 0):
            raise ValueError("score must be a non-negative integer")

        self.board = board
        self.level = level
        self.score = score

    def __str__(self):
        return f"Level={self.level}, Score={self.score}, \nBoard=\n{self.board}"

    def piecesCorrectlyPositioned(self):
        """ Return the number of pieces that are in the correct position """
        return sum(self.board.matrix[i][j] and goal_states.getGoalMatrix(self.level)[i][j] for i in range(9) for j in range(9))

    def isGoalState(self):
        """ Return True if the board is in the goal state """
        return self.piecesCorrectlyPositioned() == sum(goal_states.getGoalMatrix(self.level)[i][j] for i in range(9) for j in range(9))
    
    @staticmethod
    def getGoalMatrix(level):
        return goal_states.getGoalMatrix(level)
    
    def move(self, button):
        """ Board will shift shRow units in the row of the button + delta and shCol units in the column of the button + delta. """
        shRow, shCol, delta = button.getMove(self.level)
        match delta:
            case 0:
                newBoard = self.board.shiftRow(button.index, shRow).shiftColumn(button.index, shCol)
            case 1:
                symetric = 8 - button.index
                newBoard = self.board.shiftRow(symetric, shRow).shiftColumn(symetric, shCol)
            case 2:
                symetric = 8 - button.index
                newBoard = self.board.shiftRow(button.index, shRow).shiftColumn(button.index, shCol)
                newBoard = newBoard.shiftRow(symetric, -shRow).shiftColumn(symetric, -shCol)
            case 3:
                    #cima ou baixo
                    if (button.side % 2 == 0):
                        newBoard = self.board.shiftColumn(button.index, shCol)
                        
                        #exceção para regra do nivel 10 (estava a mexer uma linha sem botão)
                        if button.index != 1: 
                            newBoard = newBoard.shiftRow(button.index, shRow)
                    else:
                        newBoard = self.board.shiftRow(button.index, shRow).shiftColumn(button.index, shCol)
            case 4:
                symetric = 8 - button.index
                newBoard = self.board.shiftColumn(button.index, shCol).shiftRow(button.index, shRow)
                newBoard = newBoard.shiftColumn(symetric, shCol).shiftRow(symetric, shRow)
            case 5:
                next = (button.index + 1) % 9
                newBoard = self.board.shiftRow(button.index, shRow).shiftColumn(button.index, shCol)
                newBoard = newBoard.shiftRow(next, shRow).shiftColumn(next, shCol)
            case 6:
                prev = (button.index - 2) % 9
                newBoard = self.board.shiftRow(button.index, shRow).shiftColumn(button.index, shCol)
                newBoard = newBoard.shiftRow(prev, shRow).shiftColumn(prev, shCol)

        return GameState(newBoard, self.level, self.score + 1)
    
    @staticmethod
    def initializeRandomState(level, buttons):
        goalState = GameState(Board(goal_states.getGoalMatrix(level)), level, 0)
        # random moves
        randMoves = random.randint(50, 100)
        for _ in range(randMoves):
            button = random.choice(buttons)
            while (button.side, button.index) in operators.getOperation(level)["ignoreButtons"]:
                button = random.choice(buttons)

            newState = goalState.move(button)
            if newState.isGoalState():
                continue
            goalState = goalState.move(button)

        return GameState(goalState.board, level, 0)


class Game:

    def __init__(self, screen):
        self.screen = screen
        self.buttons = [Button(i,j) for j in range(9) for i in range(4)]
        self.state = GameState.initializeRandomState(12-1, self.buttons) #FIXME: Change to 0 after testing

    def checkButtons(self, x, y):
        for button in self.buttons:
            if (button.side, button.index) in operators.getOperation(self.state.level)["ignoreButtons"]:
                continue
            if button.isClicked(x, y):
                print(f"You clicked me! {button}")
                self.state = self.state.move(button)
                if self.state.isGoalState():
                    print("Goal state reached!")
                    if self.state.level == 143:
                        print("You won the game!")
                        return
                    self.state = GameState.initializeRandomState(self.state.level + 1, self.buttons)

    def draw(self):
        # Fill the screen with a color
        self.screen.fill((128, 128, 128))

        # Draw the game board
        goalMatrix = GameState.getGoalMatrix(self.state.level)
        self.state.board.draw(self.screen, goalMatrix)

        # Create a font object
        font = pygame.font.Font(None, 36)

        # Render the level and score
        levelText = font.render(f"Level: {self.state.level + 1}", True, (255, 255, 255))
        scoreText = font.render(f"Score: {self.state.score}", True, (255, 255, 255))

        # Draw the level and score on the right side of the board
        self.screen.blit(levelText, (2*MARGIN + 10*cellSize + 10, MARGIN))
        self.screen.blit(scoreText, (2*MARGIN + 10*cellSize + 10, MARGIN + 40))

        # Draw the buttons
        for button in self.buttons:
            if (button.side, button.index) in operators.getOperation(self.state.level)["ignoreButtons"]:
                continue
            button.draw(self.screen)


if __name__ == "__main__":

    """ 
    # TEST 1
    
    matrix = [[0, 0, 0, 0, 0, 0, 0, 0, 0],
             [0, 0, 0, 0, 0, 0, 0, 0, 0],
             [0, 0, 0, 0, 1, 0, 0, 0, 0],
             [0, 0, 0, 1, 1, 1, 0, 0, 0],
             [0, 0, 0, 1, 1, 1, 0, 0, 0],
             [0, 0, 0, 1, 0, 1, 0, 0, 0],
             [0, 0, 0, 0, 0, 0, 0, 0, 0],
             [0, 0, 0, 0, 0, 0, 0, 0, 0],
             [0, 0, 0, 0, 0, 0, 0, 0, 0]]
    
    board = Board(matrix)
    level = 1
    state = GameState(board, level, 0)
    button_side, button_index = 2, 4
    button = Button(button_side, button_index)

    print("BOARD:")
    print(state.board)
    print(f'Button: {button}')
    newState = state.move(button)
    print("NEW BOARD:")
    print(newState.board)

    # ITS WORKINNNNNNNNNNNNNNNNN
    
    # TEST 2
    buttons = [Button(i,j) for j in range(9) for i in range(4)]
    print(GameState.initializeRandomState(1, buttons))
    """

   

