import heapq

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

"""
Heuristic Evaluation Functions - Minimization!
"""
def correctPieces(state):
    """ This heuristic considers the number of pieces correctly positioned """
    return state.numberOfPieces() - state.piecesCorrectlyPositioned()

def manhattanDistancesFreeGS(state):
    """ This heuristic considers the sum of Manhattan Distances to the closest free goal position """
    currentMatrix = state.board.matrix
    goalMatrix = state.getGoalMatrix()
    dist = 0
    toSolve = [(i,j) for i in range(9) for j in range(9) if currentMatrix[i][j] and not goalMatrix[i][j]]
    free = [(i,j) for i in range(9) for j in range(9) if goalMatrix[i][j] and not currentMatrix[i][j]]

    for i,j in toSolve:
        dist += min([abs(i - x) + abs(j - y) for x,y in free])
        
    return dist

def manhattanDistancesAnyGS(state):
    """ This heuristic considers the sum of Manhattan Distances to the closest (any) goal position """
    currentMatrix = state.board.matrix
    goalMatrix = state.getGoalMatrix()
    dist = 0
    toSolve = [(i,j) for i in range(9) for j in range(9) if currentMatrix[i][j] and not goalMatrix[i][j]]
    goalPosition = [(i,j) for i in range(9) for j in range(9) if goalMatrix[i][j]]

    for i,j in toSolve:
        dist += min([abs(i - x) + abs(j - y) for x,y in goalPosition])
        
    return dist

def mixed(state):
    """ This heuristic considers the number of pieces correctly positioned and the sum of Manhattan Distances to the closest (any) goal position """
    return 3 * correctPieces(state) + manhattanDistancesAnyGS(state)

"""
Search Algorithms
"""
# Depth Limited Search
def dls(node, buttons, depth, visited=set()):
    if node.isGoalState():
        return node
    if depth == 0:
        return None
    for child in node.getChildren(buttons):
        if not child in visited:
            visited.add(child)
            result = dls(child, buttons, depth - 1, visited)
            if result:
                return result
    return None

# Iterative Deepening Search
def ids(node, buttons, maxDepth=8):
    for depth in range(1,maxDepth):
        result = dls(node, buttons, depth)
        if result:
            return result
    return None

# Breadth First Search
def bfs(root, buttons):
    queue = [root]
    visited = set()
    while queue:
        node = queue.pop(0)
        visited.add(node)
        if node.isGoalState():
            return node
        children = node.getChildren(buttons)
        for child in children:
            if not child in visited:
                queue.append(child)
    return None

# Greedy Search
def gs(root, buttons, heuristic):
    root.calculateDistanceToGoal(heuristic)
    queue = [(root.distanceToGoal, root)]
    heapq.heapify(queue)
    visited = set()
    while queue:
        _, node = heapq.heappop(queue)
        visited.add(node)
        if node.isGoalState():
            return node
        children = node.getChildren(buttons)
        for child in children:
            if child not in visited:
                child.calculateDistanceToGoal(heuristic)
                heapq.heappush(queue, (child.distanceToGoal, child))
    return None

# Weighted A* Search
def wa_star(root, buttons, heuristic, weight):
    root.calculateDistanceToGoal(heuristic)
    queue = [(weight * root.distanceToGoal, root)]
    heapq.heapify(queue)
    visited = set()
    while queue:
        _, node = heapq.heappop(queue)
        visited.add(node)
        if node.isGoalState():
            return node
        children = node.getChildren(buttons)
        for child in children:
            if child not in visited:
                child.calculateDistanceToGoal(heuristic)
                heapq.heappush(queue, (child.distance + weight * child.distanceToGoal, child))
    return None

# A* Search
def a_star(root, buttons, heuristic):
    return wa_star(root, buttons, heuristic, 1)