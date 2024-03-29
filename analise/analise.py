import os
from time import time
from math import inf
import openpyxl
import pandas as pd
from matplotlib import pyplot as plt

from levels_analise import STATES

goal_state = [[0, 0, 0, 0, 0, 0, 0, 0, 0],   
    [0, 0, 0, 0, 0, 0, 0, 0, 0],
    [0, 0, 0, 0, 0, 0, 0, 0, 0],
    [0, 0, 0, 1, 1, 1, 0, 0, 0],
    [0, 0, 0, 1, 1, 1, 0, 0, 0],
    [0, 0, 0, 1, 1, 1, 0, 0, 0],
    [0, 0, 0, 0, 0, 0, 0, 0, 0],
    [0, 0, 0, 0, 0, 0, 0, 0, 0],
    [0, 0, 0, 0, 0, 0, 0, 0, 0]]

class TreeNode:

    def __init__ (self, state, parentNode=None, parentButton=None, distance=0):
        self.state = state
        self.parentNode = parentNode
        self.parentButton = parentButton
        self.distanceToGoal = 0
        self.distance = distance
    
    def __hash__(self):
        return hash((str(self.state.board), self.state.level))
    
    def __lt__(self, other):
        return self.distanceToGoal < other.distanceToGoal

    def isGoalState(self):
        return self.state.isGoalState()
    
    def getChildren(self, buttons):
        nodes = []
        for button in buttons:
            newState = self.state.move(button)
            if button.isValid(self.state.level) and newState != self.state:
                nodes.append(TreeNode(newState, self, button, distance=self.distance+1))
        return nodes
    
    def getButtonSequence(self):
        if self.parentNode == None:
            return []
        return self.parentNode.getButtonSequence() + [self.parentButton]
    
    def calculateDistanceToGoal(self, heuristic):
        self.distanceToGoal = heuristic(self.state)