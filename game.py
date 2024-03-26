from board import Board
from button import Button
from constants import MARGIN, cellSize
import pygame
import goal_states
import operators
import random
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
    
    def piecesCorrectlyPositioned(self):
        """ Return the number of pieces that are in the correct position """
        return sum(self.board.matrix[i][j] and self.getGoalMatrix()[i][j] for i in range(9) for j in range(9))

    def isGoalState(self):
        """ Return True if the board is in the goal state """
        return self.piecesCorrectlyPositioned() == sum(self.getGoalMatrix()[i][j] for i in range(9) for j in range(9))
    
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
        # randMoves = random.randint(50, 100)
        randMoves = 5
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


class TreeNode:

    def __init__ (self, state, parentNode=None, parentButton=None):
        self.state = state
        self.parentNode = parentNode
        self.parentButton = parentButton
    
    def __hash__(self):
        return hash((str(self.state.board), self.state.level))

    def isGoalState(self):
        return self.state.isGoalState()
    
    def getChildren(self, buttons):
        nodes = []
        for button in buttons:
            newState = self.state.move(button)
            if button.isValid(self.state.level) and newState != self.state:
                nodes.append(TreeNode(newState, self, button))
        return nodes
    
    def printPath(self):
        file = open("path.txt", "w")
        path = []
        node = self
        while node:
            path.append(node)
            node = node.parentNode

        path.reverse()
        file.write(f'{path[0].state}\n')
        for node in path[1:]:
            print(node.parentButton)
            file.write(f'{node.parentButton}\n')
            file.write(f'{node.state}\n')
        file.close()

    def getButtonSequence(self):
        if self.parentNode == None:
            return []
        return self.parentNode.getButtonSequence() + [self.parentButton]


def bfs(root, buttons):
    #open file output.txt to write
    file = open("output.txt", "w")
    queue = [root]
    visited = set()
    while queue:
        node = queue.pop(0)
        visited.add(node)
        file.write(f'{node.state}\n')
        if node.isGoalState():
            file.close()
            return node
        children = node.getChildren(buttons)
        for child in children:
            if not child in visited:
                child.parent = node
                queue.append(child)
    file.close()
    return None


class Game:

    def __init__(self, screen):
        self.screen = screen
        self.buttons = [Button(i,j) for j in range(9) for i in range(4)]
        self.state = GameState.initializeRandomState(0, self.buttons)

    def checkButtons(self, x, y):
        for button in self.buttons:
            if not button.isValid(self.state.level):
                continue
            if button.isClicked(x, y):
                print(f"You clicked me! {button}")
                self.state = self.state.move(button)

    def update(self):
        if self.state.isGoalState():
            print("Goal state reached!")
            sleep(1)
            if self.state.level == (len(operators.operations) * len(goal_states.goalMatrices) - 1):
                return True
            
            self.state = GameState.initializeRandomState(self.state.level + 1, self.buttons)
        return False
    
    def resolveLevel(self):
        initialNode = TreeNode(self.state)
        goalNode = bfs(initialNode, self.buttons)
        
        if goalNode:
            buttonSequence = goalNode.getButtonSequence()
            for button in buttonSequence:
                print(f"AI clicked me! {button}")
                self.state = self.state.move(button)
                button.highlight = True
                self.draw()
                pygame.display.flip()
                sleep(1)


    def giveHint(self):
        initialNode = TreeNode(self.state)
        goalNode = bfs(initialNode, self.buttons)

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

        # Render the level and score
        levelText = font.render(f"Level: {self.state.level + 1}", True, (255, 255, 255))
        scoreText = font.render(f"Score: {self.state.score}", True, (255, 255, 255))

        # Draw the level and score on the right side of the board
        self.screen.blit(levelText, (2*MARGIN + 10*cellSize + 10, MARGIN))
        self.screen.blit(scoreText, (2*MARGIN + 10*cellSize + 10, MARGIN + 40))

        # Draw the buttons
        for button in self.buttons:
            if not button.isValid(self.state.level):
                continue
            button.draw(self.screen)
        

if __name__ == "__main__":
    print("This is the game module")

    buttons = [Button(i,j) for j in range(9) for i in range(4)]
    initialState = GameState.initializeRandomState(0, buttons)
    initialNode = TreeNode(initialState)

    goalNode = bfs(initialNode, buttons)

    if goalNode:
        goalNode.printPath()
