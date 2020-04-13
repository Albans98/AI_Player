# AI Player

*Building an AI "Gomoku" player*

✒️ Note : our team was ranked 7/100 during school competition @ESILV.

- [📍 Introduction](#-introduction)
- [👩‍💻 Just tell me what to do](#-Just-tell-me-what-to-do)
- [📝 Some explanations](#-Some-explanations)
- [🎓 Developers](#-Developers)

## 📍 Introduction

Gomoku is a **turn-based two-player board game** (player 1 with black pawns, player 2 with white pawns). The black player plays first. Each player has 60 pieces. The size of the board is **15x15 cells**. The rows are numbered from **'A' to 'O'** and the columns are numbered from **'1' to '15'**. A player can place a pawn on any free space. The first player to **align 5 consecutive pieces** (horizontally, vertically or diagonally) wins. Otherwise, the game is a draw if there are no more pawns. In the game of Gomoku (as for tic-tac-toe), the first player has more chances to win. Then we used the **long-pro variant :**
• player 1 (black) places a pawn in the center of the board (H8)
• player 2 (white) can place a pawn anywhere
• then player 1 can place a pawn anywhere except in a square of size 7x7 from the center H8.
• Then the game is going normally


## 👩‍💻 Just tell me what to do

In order to play this game, you can download the `AI_Project.py` file and launch it using the command line `python AI_Project.py`.

Then, follow the instructions displayed on the shell. (French version)

## 📝 Some explanations

In order to build our AI, we focused on implementing the **MinMax algorithm** based on 4 functions :
  - Actions
  - Result
  - Utility
  - Terminal Test

To improve performance, we needed to reduce the number of nodes since a grid of 15x15 is really large. We used an improved version of MinMax algorithm by using a method called "Alpha-Beta pruning".

We also used a maximum **depth** in our *searching tree* to limit the time we have to wait during each move to **0-5 seconds** approximately.

*And what about our heuristic ?*

We decided to implement a *best score* heuristic which is giving a specific score to each cell of the grid. It means that each cell will be assigned a value based on the **probabaility to win the game** if we play on this cell. Then, we return only the 5 cells with the highest score to reduce our AI complexity.

## 🎓 Developers

Students @ESILV - Paris.
* Alban STEFF
* Soumaya SABRY
* Fanny ZHONG
* Alexandre SALOU

Project of 2019
