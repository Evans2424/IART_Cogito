import csv
import time
from algorithms import bfs, ids, gs, a_star, wa_star, TreeNode
from button import Button
from game import GameState
from board import Board

# Initialize your states here
initial_board = [[0, 0, 0, 0, 0, 0, 0, 0, 0],    
    [0, 0, 0, 0, 0, 0, 0, 0, 0],
    [0, 0, 0, 0, 0, 0, 0, 0, 0],
    [0, 0, 1, 1, 1, 0, 0, 0, 0],
    [0, 0, 1, 0, 1, 1, 0, 0, 0],
    [0, 0, 0, 0, 1, 0, 1, 0, 0],
    [0, 0, 0, 0, 1, 0, 0, 0, 0],
    [0, 0, 0, 0, 0, 0, 0, 0, 0],
    [0, 0, 0, 0, 0, 0, 0, 0, 0]]

goal_state = [[0, 0, 0, 0, 0, 0, 0, 0, 0],   
    [0, 0, 0, 0, 0, 0, 0, 0, 0],
    [0, 0, 0, 0, 0, 0, 0, 0, 0],
    [0, 0, 0, 1, 1, 1, 0, 0, 0],
    [0, 0, 0, 1, 1, 1, 0, 0, 0],
    [0, 0, 0, 1, 1, 1, 0, 0, 0],
    [0, 0, 0, 0, 0, 0, 0, 0, 0],
    [0, 0, 0, 0, 0, 0, 0, 0, 0],
    [0, 0, 0, 0, 0, 0, 0, 0, 0]]  # replace with your actual state

algorithms = [bfs, ids, gs, a_star, wa_star]
results = []
buttons = [Button(i,j) for j in range(9) for i in range(4)]


for algorithm in algorithms:
    start_time = time.time()
    result = algorithm(initial_board, goal_state)
    end_time = time.time()

    # Check if the algorithm found the correct solution
    if result == goal_state:
        elapsed_time = end_time - start_time
        results.append([algorithm.__name__, elapsed_time])
    else:
        results.append([algorithm.__name__, "Failed"])

# Write the results to a CSV file
with open('algorithm_times.csv', 'w', newline='') as file:
    writer = csv.writer(file)
    writer.writerow(["Algorithm", "Time"])
    writer.writerows(results)