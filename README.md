# Cogito : One Player Solitaire Game

## Introduction
Cogito is a solitaire game played on a 9x9 grid. The objective is to correctly position all the red circles in the white squares according to the level's rules. The game is won when all the red circles are in their correct positions.

## Setup
The game was developed using python 3.10.11, but it should work with any python 3.x version. To install the required packages, run the following command:

```bash
pip install pygame
```

To initialize the game, run the following command:

```bash
python main.py
```

## How to play
When the previous command is ran the following screen will appear:

![Initial Game Screen](imgs/initial_game_screen.png)

This view displays the game board and its current state. The nine squares that need to be filled with red circles to win this level are marked in white.

You can shift rows and/or columns by clicking on the blue circles around the board. The effect of this action may differ based on the rules of the particular level, that the player should find out by himself. 

We have information about the current level, the number of moves made (score), and the current AI algorithm selected. The player can change the AI algorithm by using the "Left" and "Right" arrow keys.

When the AI finds a solution, it will press the buttons accordingly, and in the end show the elapsed time to find the solution. The player can then go to the next level, restart the level to try another algorithm, or quit the game. 

## Control List
- **Mouse Click on the blue circles** : Move the board.
<br>

- **S** : Solve the level using the selected AI algorithm.
- **A** : The AI highlights the next best calculated move. 
<br>

- **Left/Right Arrow Keys** : Change the AI algorithm.
- **Up/Down Arrow Keys** : Increase/Decrease Depth of the algorithm (when IDS is selected)
- **H** : Change the heuristic function (only for informed algorithms).
- **P** : Increase the Weight in Weighted A*.
- **L** : Decrease the Weigth in Weighted A*.



