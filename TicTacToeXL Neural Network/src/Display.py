'''
Created on Jun 18, 2021

@author: Rand
'''
import tkinter as tk
import tkinter.font as tkFont
import numpy as np
import copy
import tensorflow as tf
import game
from tkinter.constants import BOTH

# Colors for Display

GREY="#8a8c84"
GREEN="#05ff1a"
RED="#ff0000"
BLUE="#0008ff"
BLACK="#000000"

# Assigns names for integers to avoid magic numbers

BASIC_LENGTH=3
GAME_STATE_X = -1
GAME_STATE_O = 1
GAME_STATE_DRAW = 0
GAME_STATE_NOT_ENDED = 2
ROW_METHOD=0
COL_METHOD=1
DIAG_METHOD=2
ONE_PLAYER=0
TWO_PLAYER=1
PLAYER_X_VAL = -1
PLAYER_O_VAL = 1

class Display:
    def __init__(self):
        
        # Create main window
        
        self.window=tk.Tk()
        self.window.geometry("900x900")
        self.window.resizable(width=False, height=False)
        self.window.title("Large TicTacToe!")
        
        # Instantiate Game and other associated variables
        
        self.theGame=game.Game()
        self.completedBoards=[]
        self.greyLocs=[]
        
        # Create user interface
        
        self.createCanvas()
        self.createButtons()
        
    # Creates screen that offers either a one or two player game mode
        
    def createStartScreen(self):
        fontStyle = tkFont.Font(family="Lucida Grande", size=110)
        self.onePlayer=tk.Button(self.window, bg=RED,
                            height=2,width=11, command=lambda numPlayers=ONE_PLAYER:
                            self.playerCountSelected(numPlayers),
                            text="One Player", fg=BLACK, font=fontStyle)
        self.onePlayer.place(x=0, y=0)
        self.twoPlayer=tk.Button(self.window, bg=BLUE,
                            height=2,width=11, command=lambda numPlayers=TWO_PLAYER:
                            self.playerCountSelected(numPlayers),
                            text="Two Player", fg=BLACK, font=fontStyle)
        self.twoPlayer.place(x=0, y=450)
        self.window.mainloop()
    
    # Reacts to one/two player selection accordingly
    
    def playerCountSelected(self, numPlayers):
        self.players=numPlayers
        self.onePlayer.destroy()
        self.twoPlayer.destroy()
        if (numPlayers is ONE_PLAYER):
            self.model=tf.keras.models.load_model(
                 "Models/model1", custom_objects=None, compile=True, options=None)
        self.makeNeuralNetworkMove()
        
    # Creates canvas for lines on Tic-Tac-Toe board
        
    def createCanvas(self):
        self.canvas=tk.Canvas(self.window)
        for i in range(BASIC_LENGTH):
            
            # Lines that separate the nine boards
            
            self.canvas.create_line(i*300,0,i*300,900,width=3)
            self.canvas.create_line(0,i*300,900,i*300,width=3)
            for j in range(BASIC_LENGTH):
                
                # Lines that separate the squares within the boards
                
                self.canvas.create_line(i*300+j*100,0,i*300+j*100,900,dash=(5,5))
                self.canvas.create_line(0,i*300+j*100,900,i*300+j*100,dash=(5,5))
        # Outside lines of main board        
        
        self.canvas.create_line(0,900,900,900,width=3)
        self.canvas.create_line(900,0,900,900,width=3)
        self.canvas.pack(fill=BOTH, expand=True)
        
    # Creates buttons for display so that user can select squares
        
    def createButtons(self):
        
        # Creates buttons
        
        pixelVirtual = tk.PhotoImage(width=1, height=1)
        self.buttons=np.empty((3,3,3,3),dtype=object)
        for i in range(BASIC_LENGTH):
            for j in range(BASIC_LENGTH):
                for k in range(BASIC_LENGTH):
                    for l in range(BASIC_LENGTH):
                        self.buttons[i][j][k][l]=tk.Button(self.window, 
                            image=pixelVirtual, bg=GREY,
                            height=80,width=80, command=lambda i=i, j=j, k=k, l=l: 
                            self.buttonClicked([i,j,k,l],self.buttons[i][j][k][l]))
                        self.buttons[i][j][k][l].place(x=j*300+l*100+8, y=i*300+k*100+8)
                        
        # Indicates available moves to the user
                        
        self.greenify(self.theGame.getAvailableMoves())
        
        # Launches the start screen after buttons are created so that the 
        # user can't play the game until either one or two player option
        # is selected
        
        self.createStartScreen() 
        
    # Responds to a square being clicked on the board
        
    def buttonClicked(self, loc, button):
        
        # Attempts to make the move while checking whether or not move actually occurred
        
        if (self.theGame.move(loc)):
            
            # Assuming valid move was selected, button that was pressed is destroyed to make way for 
            # X or O after the view is updated
            
            button.destroy()        
            available=self.theGame.getAvailableMoves()
            self.greenify(available)
            self.showGame()
                
            # Checks win
            
            bigBoardState=self.theGame.getGameResult()
            if (bigBoardState[0]!=2):
                self.gameOver(bigBoardState)
            else:
                
                # If the user is playing against the neural network, there is a 2 second delay, and then the 
                # neural network is called
                
                if (self.players is ONE_PLAYER):
                    self.window.after(2000, self.makeNeuralNetworkMove)
                
    # Indicates to user which squares can be picked
                
    def greenify(self,available):
        for i in range(BASIC_LENGTH):
            for j in range(BASIC_LENGTH):
                for k in range(BASIC_LENGTH):
                    for l in range(BASIC_LENGTH):
                        button=self.buttons[i][j][k][l]
                        
                        # Checks that button has not been destroyed
                        
                        if (button.winfo_exists()):
                            
                            # Available buttons turn green while unavailable squares turn grey
                            
                            if (available.__contains__([i,j,k,l])):
                                    button.configure(bg=GREEN)
                            else:
                                button.configure(bg=GREY)
                                
    # Plays for neural network
    
    def makeNeuralNetworkMove(self):
        availableMoves = self.theGame.getAvailableMoves()
        
        # Gives basis values for max algorithm
        
        maxValue = 0
        bestMove = availableMoves[0]
        for availableMove in availableMoves:
            
            # Get a copy of a board and prepare it for the neural network
            
            boardCopy = copy.deepcopy(self.theGame.getBigBoard())
            boardCopy[availableMove[0]*27+availableMove[1]*9+availableMove[2]*3+availableMove[3]] = PLAYER_X_VAL
            boardCopy = np.asarray(boardCopy).astype(np.int)
            value = self.model.predict(np.array(boardCopy).reshape(-1, 83))[0][0]
            
            # Check value for new maximum
            
            if value > maxValue:
                maxValue = value
                bestMove = availableMove
                
        # Make best move
                
        selectedMove = bestMove
        self.theGame.move(selectedMove)
        self.buttons[selectedMove[0]][selectedMove[1]][selectedMove[2]][selectedMove[3]].destroy()
        available=self.theGame.getAvailableMoves()
        self.greenify(available)
        self.showGame()
        
        # Check for win
        
        bigBoardState=self.theGame.getGameResult()
        if (bigBoardState!=2):
            self.gameOver(bigBoardState)
        
        
    # Displays the game
        
    def showGame(self):
        fontStyle = tkFont.Font(family="Lucida Grande", size=50)
        labels=np.empty((3,3,3,3),dtype=object)
        for i in range(BASIC_LENGTH):
            for j in range(BASIC_LENGTH):
                self.showGameState(i,j)
                for k in range(BASIC_LENGTH):
                    for l in range(BASIC_LENGTH):
                        square=self.theGame.getSquare(i, j, k, l)
                        
                        # Shows either a red X, a blue O, or nothing
                        
                        if (square!=0):
                            letter="O"
                            clr=BLUE
                            if (square==-1):
                                letter="X"
                                clr=RED
                            if (self.greyLocs.__contains__([i,j,k,l])):
                                clr=GREY
                            labels[i][j][k][l]=tk.Label(self.window,text=letter, font=fontStyle, fg=clr)
                            labels[i][j][k][l].place(x=j*300+l*100+20, y=i*300+k*100+10)
    
    # Indicates that a board is captured
    
    def showGameState(self,row,col):
        state= self.theGame.getBoard(row, col)
        
        # Makes sure that the board was captured by a player and that the board has not already been changed
        
        if (state[0]!=GAME_STATE_NOT_ENDED and not self.completedBoards.__contains__([row,col])):
            
            #Sets winning color and draws around board in that color
            
            clr=RED
            if (state[0]==GAME_STATE_DRAW):
                clr=GREY
            elif (state[0]==GAME_STATE_O):
                clr=BLUE
            self.canvas.create_line(col*300+5, row*300+5, col*300+5, row*300+295,fill=clr, width=3)
            self.canvas.create_line(col*300+295, row*300+5, col*300+5, row*300+5,fill=clr, width=3)
            self.canvas.create_line(col*300+295, row*300+295, col*300+5, row*300+295,fill=clr, width=3)
            self.canvas.create_line(col*300+295, row*300+295, col*300+295, row*300+5,fill=clr, width=3)
            
            # Shows "Winning Line based on how board was won
            
            if (state[2]==ROW_METHOD):
                self.canvas.create_line(col*300, row*300+state[1]*100+50, (col+1)*300, row*300+state[1]*100+50,fill=clr, width=5)
                for i in range(BASIC_LENGTH):
                    for j in range(BASIC_LENGTH):
                        if (i!=state[1]):
                            self.greyLocs.append([row,col,i,j])
            if (state[2]==COL_METHOD):
                self.canvas.create_line(col*300+state[1]*100+50, row*300, col*300+state[1]*100+50, (row+1)*300,fill=clr, width=5)
                for i in range(BASIC_LENGTH):
                    for j in range(BASIC_LENGTH):
                        if (j!=state[1]):
                            self.greyLocs.append([row,col,i,j])
            if (state[2]==DIAG_METHOD):
                if (state[1]==0):
                    self.canvas.create_line(col*300, row*300, (col+1)*300, (row+1)*300,fill=clr, width=5)
                    for i in range(BASIC_LENGTH):
                        for j in range(BASIC_LENGTH):
                            if (j!=i):
                                self.greyLocs.append([row,col,i,j])
                else:
                    self.canvas.create_line(col*300, (row+1)*300, (col+1)*300, row*300,fill=clr, width=5)
                    for i in range(BASIC_LENGTH):
                        for j in range(BASIC_LENGTH):
                            if (j!=2-i):
                                self.greyLocs.append([row,col,i,j])
                
            # Records that board has been taken care of
            
            self.completedBoards.append([row,col])
            self.canvas.place()
            
    # Shows game-over screen
            
    def gameOver(self,state):
        
        # Checks if game was won
         
        if (state[0]!=GAME_STATE_NOT_ENDED):
            
            # Create appropriate text for how game ended
            
            fontStyle = tkFont.Font(family="Lucida Grande", size=100)
            clr=RED
            txt="X VICTORY!"
            if (state[0]==GAME_STATE_DRAW):
                clr=GREY
                txt="ITS A TIE!"
            elif (state[0]==GAME_STATE_O):
                clr=BLUE
                txt="O VICTORY!"
                        
            # Shows "Winning Line based on how board was won
            
            self.canvas.create_line(0,0,900,0,fill=clr, width=8)
            self.canvas.create_line(0,0,0,900, fill=clr, width=8)
            self.canvas.create_line(900,900,0,900,fill=clr, width=8)
            self.canvas.create_line(900,900,900,0,fill=clr, width=8)
            if (state[2]==ROW_METHOD):
                self.canvas.create_line(0, state[1]*300+150, 900, state[1]*300+150,fill=clr, width=5)
            if (state[2]==COL_METHOD):
                self.canvas.create_line(state[1]*300+150,0, state[1]*300+150,900, fill=clr, width=5)
            if (state[2]==DIAG_METHOD):
                if (state[1]==0):
                    self.canvas.create_line(0,0, 900,900,fill=clr, width=5)
                else:
                    self.canvas.create_line(900,0,0,900,fill=clr, width=5)
            label=tk.Label(self.window,text=txt, font=fontStyle, fg=clr)
            label.place(x=10,y=450)
            
            #Destroys buttons
            
            for i in range(BASIC_LENGTH):
                for j in range(BASIC_LENGTH):
                    for k in range(BASIC_LENGTH):
                        for l in range(BASIC_LENGTH):
                            self.buttons[i][j][k][l].destroy()
            self.canvas.place()
            
if __name__ == '__main__':
    disp=Display()