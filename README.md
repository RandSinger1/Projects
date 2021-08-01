# Ultimate TicTacToe #
## Background ##
Since I knew I would have a lot of free time during the Summer of 2021, I wanted to learn python, get started with machine learning, and create my own project from scratch.  So, I taught a computer to play Ultimate TicTacToe against a human using Python, TensorFlow, Keras, and Tkinter.  Ultimate TicTacToe is a modified, significantly more complex version of regular TicTacToe that I've always played with my friends.
## Rules ##
The game begins with a 3 × 3 grid of tic-tac-toe boards, referred to as a local board, while the larger board is referred to as the global board.

![image](https://user-images.githubusercontent.com/74988565/127755486-9ebe13e8-8a66-4321-beda-e8bbea307df7.png)

The game starts with X playing in the middle local board. This move "sends" their opponent to its relative location. For example, if X played in the top right square of their local board, then O needs to play next in the top right local board of the global board. O can then play in any one of the nine available spots in that local board, each move sending X to a different local board.

![image](https://user-images.githubusercontent.com/74988565/127755590-49a73ca4-e658-4978-9d85-9141ee6b3bdd.png)

If a move is played so that it is to win a local board by the rules of normal tic-tac-toe, then the entire local board is marked as a victory for the player in the global board.

![image](https://user-images.githubusercontent.com/74988565/127755580-a33f6022-761b-412f-8c9f-cfbfb00f3c29.png)

A marked local board can still be played, however, its result will not change (This is different from how it is typically played, and makes the project more unique)

Game play ends when either a player wins the global board or there are no legal moves remaining, in which case the game is a draw.

![image](https://user-images.githubusercontent.com/74988565/127755586-93234d78-b475-4acd-873f-b4c9c4aec7a4.png)

## Download Instructions ##
Pull the src folder from the repository and make sure NumPy, TensorFlow, and Tkinter are installed.  Run the display script and the game will start

## Project Structure ##
miniGame.py: Class that handles the local boards
game.py: Class that handles the global boards, made up of a 3 x 3 grid of local boards
Simulate.py: Handles any computer simulation of gameplay, including iterating through simulations
model.py: Creates and trains the neural network through the data obtained from simulations
Optimizer.py: Creates many models based on different conditions, depending on user input, to determine the optimal conditions for training the AI
Display.py: Handles the user interface
Models: Folder that stores saved neural networks so that AI does not need tobe retrained
Optimizer Log: Folder that stores past trials, their accuracy, and their time cost

## Gameplay Sample ##

https://user-images.githubusercontent.com/74988565/127756072-4fedb7d0-2d66-4a3a-abbb-2d85cbcd3ff9.mp4

## Future Improvements ##
This was my first python project, my first TensorFlow project, my first Tkinter project, my first machine learning project, and my first github project so it has its flaws in following convention.  When I started the project, my understanding of how to use a repository was lacking, and so I just did one big upload at the end, there are too many global variables in the scripts, and the AI lacks accuracy due to low computing power and a lack of time.  However, understanding these mistakes will allowe me to be a better programmer in the future.  While the project may not be as polished or efficient as I might have hoped, it taught me a lot of new skills.  The computer may not have learned a lot about TicTacToe, but I know that I learned a lot about the computer



