from structures.board import Board
from structures.button import Button
from data.constants import MARGIN, cellSize, HEIGHT
import data.goal_states as goal_states
import data.operators as operators
from structures.algorithms import *
import pygame
import random
import time
from time import sleep


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
    
    def __eq__(self, other):
        return self.board == other.board and self.level == other.level

    def getGoalMatrix(self):
        return goal_states.getGoalMatrix(self.level)
    
    def numberOfPieces(self):
        """ Return the number of pieces in the board """
        return sum(self.board.matrix[i][j] for i in range(9) for j in range(9))
    
    def piecesCorrectlyPositioned(self):
        """ Return the number of pieces that are in the correct position """
        return sum(self.board.matrix[i][j] and self.getGoalMatrix()[i][j] for i in range(9) for j in range(9))

    def isGoalState(self):
        """ Return True if the board is in the goal state """
        return self.piecesCorrectlyPositioned() == self.numberOfPieces()
    
    def getMaxManhattanDistance(self):
        return goal_states.getMaxManhattanDistance(self.level)
    
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
        randMoves = random.randint(15, 20)
        for _ in range(randMoves):
            button = random.choice(buttons)
            while not button.isValid(level):
                button = random.choice(buttons)

            newState = goalState.move(button)
            while newState.isGoalState() or newState == goalState:
                button = random.choice(buttons)
                while not button.isValid(level):
                    button = random.choice(buttons)
                newState = goalState.move(button)
            goalState = goalState.move(button)

        return GameState(goalState.board, level, 0)

class Game:

    def __init__(self, screen):
        self.screen = screen
        self.buttons = [Button(i,j) for j in range(9) for i in range(4)]
        self.state = GameState.initializeRandomState(0, self.buttons)
        self.elapsed_time = 0
        
        self.algorithms = [bfs, ids, gs, a_star, wa_star]
        self.selectedAlgorithm = 0
        
        self.heuristics = [correctPieces, manhattanDistancesFreeGS, manhattanDistancesAnyGS, mixed]
        self.heuristicIndex = 0
        
        self.maxDepth = 5

        self.heuristicWeight = 1.0
        
        self.thinking = False

    def changeAlgorithm(self, delta):
        self.selectedAlgorithm = (self.selectedAlgorithm + delta) % len(self.algorithms)

    def changeMaxDepth(self, delta):
        self.maxDepth = max(1, self.maxDepth + delta)
        self.maxDepth = min(10, self.maxDepth)
    
    def changeHeuristic(self):
        self.heuristicIndex = (self.heuristicIndex + 1) % len(self.heuristics)

    def changeHeuristicWeight(self, delta):
        self.heuristicWeight = round(max(1.0, self.heuristicWeight + delta), 1)
        self.heuristicWeight = round(min(10.0, self.heuristicWeight), 1)

    def checkButtons(self, x, y):
        for button in self.buttons:
            if not button.isValid(self.state.level):
                continue
            if button.isClicked(x, y):
                print(f"You clicked me! {button}")
                self.state = self.state.move(button)

    def update(self):
        if self.state.isGoalState():
            print("Goal state reached! Press Enter to continue.")

            self.draw()
            pygame.display.flip()

            while True:
                for event in pygame.event.get():
                    if event.type == pygame.KEYDOWN:
                        if event.key == pygame.K_RETURN:
                            if self.state.level == (len(operators.operations) * len(goal_states.goalMatrices) - 1):
                                return True, True
                            self.state = GameState.initializeRandomState(self.state.level + 1, self.buttons)
                            self.elapsed_time = 0
                            return False, False
                        elif event.key == pygame.K_ESCAPE:
                            return True, False
                        elif event.key == pygame.K_r:  # Check if the 'R' key was pressed
                            self.state = GameState.initializeRandomState(self.state.level, self.buttons)  # Restart the current level
                            self.elapsed_time = 0
                            return False, False
        return False, False

    def callAlgorithm(self, testing=False):
        if not testing:
            print("AI is thinking...")
        self.thinking = True
        self.draw()
        pygame.display.flip()

        
        start_time = time.time()  # Record the start time

        algorithm = self.algorithms[self.selectedAlgorithm]
        match algorithm.__name__:
            case "bfs":
                goalNode = algorithm(TreeNode(self.state), self.buttons)
            case "ids":
                goalNode = algorithm(TreeNode(self.state), self.buttons, self.maxDepth)
            case "gs":
                goalNode = algorithm(TreeNode(self.state), self.buttons, self.heuristics[self.heuristicIndex])
            case "a_star":
                goalNode = algorithm(TreeNode(self.state), self.buttons, self.heuristics[self.heuristicIndex])
            case "wa_star":
                goalNode = algorithm(TreeNode(self.state), self.buttons, self.heuristics[self.heuristicIndex], self.heuristicWeight)
            case _:
                raise ValueError("Algorithm not implemented")
            
        end_time = time.time()  # Record the end time
        self.thinking = False
        self.elapsed_time = end_time - start_time
        if not testing:
            print(f"It took the AI {self.elapsed_time:.2f} seconds to find the best move(s)!\n")
        return goalNode

    def resolveLevel(self, testing=False):
        goalNode = self.callAlgorithm(testing)
        
        if goalNode:
            buttonSequence = goalNode.getButtonSequence()
            for button in buttonSequence:
                if not testing:
                    print(f"AI clicked me! {button}")
                self.state = self.state.move(button)
                button.highlight = True
                self.draw()
                pygame.display.flip()
                sleep(1)
      

    def giveHint(self):
        goalNode = self.callAlgorithm(False)

        if goalNode:
            buttonSequence = goalNode.getButtonSequence()
            button = buttonSequence[0]
            print(f"AI suggested me! {button}")
            button.highlight = True
            self.draw()
            pygame.display.flip()
            sleep(2)

    def draw(self):
        # Fill the screen with a color
        self.screen.fill((128, 128, 128))

        # Draw the game board
        goalMatrix = self.state.getGoalMatrix()
        self.state.board.draw(self.screen, goalMatrix)

        # Create a font object
        font = pygame.font.Font(None, 36)
        fontDescription = pygame.font.Font(None, 22)
        smallerFont = pygame.font.Font(None, 20)

        # Render the level and score
        levelText = font.render(f"Level: {self.state.level + 1}", True, (255, 255, 255))
        scoreText = font.render(f"Score: {self.state.score}", True, (255, 255, 255))
        
        algorithmText = font.render(f"Algorithm: {self.algorithms[self.selectedAlgorithm].__name__.upper()}", True, (255, 255, 255))
        depthText = font.render(f"Max Depth: {self.maxDepth}", True, (255, 255, 255))
        heuristicText = font.render(f"Heuristic: {self.heuristicIndex+1}", True, (255, 255, 255))
        heuristicWeightText = font.render(f"Weight: {self.heuristicWeight}", True, (255, 255, 255))
        
        enterText = smallerFont.render("Goal state reached! Press Enter to continue!", True, (0, 0, 0))
        restartText = smallerFont.render("Press R to restart the level", True, (0, 0, 0))
        escText = smallerFont.render("Press ESC to leave the game", True, (0, 0, 0))
        time_text = smallerFont.render(f"Elapsed time: {self.elapsed_time:.2f} seconds", True, (255, 255, 255))
        
        thinkingText = font.render("Thinking...", True, (255, 255, 255))

        # Draw the level and score on the right side of the board
        self.screen.blit(levelText, (2*MARGIN + 10*cellSize + 10, MARGIN))
        self.screen.blit(scoreText, (2*MARGIN + 10*cellSize + 10, MARGIN + 40))

        #Algorithm information
        self.screen.blit(algorithmText, (2*MARGIN + 10*cellSize + 10, MARGIN + 120))
        if self.selectedAlgorithm == 1:
            self.screen.blit(depthText, (2*MARGIN + 10*cellSize + 10, MARGIN + 160))
        if self.selectedAlgorithm >= 2:
            self.screen.blit(heuristicText, (2*MARGIN + 10*cellSize + 10, MARGIN + 160))
        if self.selectedAlgorithm == 4:
            self.screen.blit(heuristicWeightText, (2*MARGIN + 10*cellSize + 10, MARGIN + 200))

        if self.selectedAlgorithm >= 2:
            words = self.heuristics[self.heuristicIndex].__doc__.split()
            lines = [words[i:i+5] for i in range(0, len(words), 5)]
            for i, line in enumerate(lines):
                line = " ".join(line)
                text = fontDescription.render(line, True, (0, 0, 0))
                self.screen.blit(text, (2*MARGIN + 10*cellSize + 10, MARGIN + 240 + i*20))

        # Draw the goal state message
        if self.state.isGoalState():
            self.screen.blit(enterText, (2*MARGIN + 10*cellSize + 10, MARGIN + 320))
            self.screen.blit(restartText, (2*MARGIN + 10*cellSize + 10, MARGIN + 340))
            self.screen.blit(escText, (2*MARGIN + 10*cellSize + 10, MARGIN + 360))
            if self.elapsed_time > 0:
                self.screen.blit(time_text, (2*MARGIN + 10*cellSize + 10, MARGIN + 390))

        # Draw the thinking message
        if self.thinking:
            self.screen.blit(thinkingText, (2*MARGIN + 10*cellSize + 10, HEIGHT - 2*MARGIN))

        # Draw the buttons
        for button in self.buttons:
            if not button.isValid(self.state.level):
                continue
            button.draw(self.screen)
        

if __name__ == "__main__":
    print("This is the game module")