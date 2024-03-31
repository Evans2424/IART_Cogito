from structures.game import Game, GameState
from structures.board import Board
from data.test_states import STATES
from data.constants import WIDTH, HEIGHT, FPS
from math import inf
from numpy import arange
import pygame

def testGame(game : Game, best_time, best_moves):
    game.resolveLevel(testing=True)

    print("\n")
    print(f"Algorithm: {game.algorithms[game.selectedAlgorithm].__name__}")
    print(f"Took {game.elapsed_time:.2f} and {game.state.score} moves to solve test board number: {test_num+1}.")

    if game.selectedAlgorithm == 1:
        print(f"Using depth: {game.maxDepth}")
    elif 2 <= game.selectedAlgorithm <= 4:
        print(f"Using Heuristic: {game.heuristicIndex+1}")
        if game.selectedAlgorithm == 4:
            print(f"Using weight: {game.heuristicWeight}")

    if game.elapsed_time < best_time[2]:
        if game.selectedAlgorithm >= 2:
            best_time = (game.algorithms[game.selectedAlgorithm].__name__, game.heuristicIndex, game.elapsed_time)
        else:
            best_time = (game.algorithms[game.selectedAlgorithm].__name__, -1, game.elapsed_time)
    
    if game.state.score < best_moves[2]:
        if game.selectedAlgorithm >= 2:
            best_moves = (game.algorithms[game.selectedAlgorithm].__name__, game.heuristicIndex, game.state.score)
        else:
            best_moves = (game.algorithms[game.selectedAlgorithm].__name__, -1, game.state.score)

    return best_time, best_moves

def printBest(best_time, best_moves):
    print("\n")
    if best_time[1] == -1:
        print(f"Best time: {best_time[0]} with {best_time[2]:.2f} seconds.")
    else:
        print(f"Best time: {best_time[0]}, using heuristic number {best_time[1]} with {best_time[2]:.2f} seconds.")

    if best_moves[1] == -1:
        print(f"Best moves: {best_moves[0]} with {best_moves[2]:.2f} moves.")
    else:
        print(f"Best moves: {best_moves[0]}, using heuristic number {best_moves[1]} with {best_moves[2]:.2f} moves.")

if __name__ == "__main__":
    uninformed_limit = 1
    pygame.init()
    screen = pygame.display.set_mode((WIDTH, HEIGHT))
    game = Game(screen)

    for test_num, test_state in enumerate(STATES):
        best_time = ("", -1, inf)
        best_moves = ("", -1, inf)
        
        if test_num < uninformed_limit:
            """
            #uninformed search
            for algorithm in range(2):
                game.state = GameState(Board(test_state), 0, 0)
                game.selectedAlgorithm = algorithm
                game.maxDepth = 10

                best_time, best_moves = testGame(game, best_time, best_moves)
            """


        #informed search
        for algorithm in range(2, 4):
            # for heuristic in range (len(game.heuristics)): # the correct loop
            for heuristic in range (len(game.heuristics)-1, len(game.heuristics)): #to test the new heuristic 
                if (algorithm, heuristic) in [(2,1)]:
                    continue
                game.state = GameState(Board(test_state), 0, 0)
                game.selectedAlgorithm = algorithm
                
                game.heuristicIndex = heuristic

                best_time, best_moves = testGame(game, best_time, best_moves)

        # for heuristic in range (len(game.heuristics)): # the correct loop
        for heuristic in range (len(game.heuristics)-1, len(game.heuristics)): #to test the new heuristic 
            for weight in arange(1.2, 2.2, 0.2):
                game.state = GameState(Board(test_state), 0, 0)
                game.selectedAlgorithm = 4
                game.heuristicIndex = heuristic
                game.heuristicWeight = round(weight,1)

                best_time, best_moves = testGame(game, best_time, best_moves)

        printBest(best_time, best_moves)
        
        
    pygame.quit()
