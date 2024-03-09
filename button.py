import pygame
import operators
from constants import MARGIN, cellSize

class Button:
    """
        0[i] - side[index]
    3 BOARD 1
        2 
    """
    def __init__(self, side, index):
        if not 0 <= side <= 3:
            raise ValueError("side must be in the range [0, 3]")
        if not 0 <= index <= 8:
            raise ValueError("index must be in the range [0, 8]")

        self.side = side
        self.index = index
        if side == 0:
            self.position = (MARGIN + (index+1)*cellSize, MARGIN)
        elif side == 1:
            self.position = (MARGIN + 10*cellSize, MARGIN + (index+1)*cellSize)
        elif side == 2:
            self.position = (MARGIN + (index+1)*cellSize, MARGIN + 10*cellSize)
        elif side == 3:
            self.position = (MARGIN, MARGIN + (index+1)*cellSize)

    def __str__(self):
        return f"Button({self.side}, {self.index})"

    def draw(self, screen):
        """ Draw the button on the screen - its round and filled with blue """
        buttonColor = (0, 0, 255)
        pygame.draw.circle(screen, buttonColor, self.position, cellSize // 2 - 5)

    def isClicked(self, x, y):
        """ Return True if the button is clicked """
        return self.position[0] - cellSize/2 <= x <= self.position[0] + cellSize/2 and self.position[1] - cellSize/2 <= y <= self.position[1] + cellSize/2

    def getMove(self, level):
        """ Return the shiftRow, shiftColumn and delta for the move associated with the button """
        op = operators.getOperation(level)
        if self.side == 0:
            return op["perpDir"], op["ownDir"], op["delta"]
        elif self.side == 1:
            return -op["ownDir"], op["perpDir"], op["delta"]
        elif self.side == 2:
            return op["perpDir"], -op["ownDir"], op["delta"]
        elif self.side == 3:
            return op["ownDir"], op["perpDir"], op["delta"]