'''
Created on Jun 16, 2021

@author: Rand
'''
import miniGame
import numpy as np

# Assigns names for integers to avoid magic numbers

PLAYER_X = 'X'
PLAYER_O = 'O'
EMPTY = ' '
PLAYER_X_VAL = -1
PLAYER_O_VAL = 1
EMPTY_VAL = 0
HORIZONTAL_SEPARATOR = ' | '
VERTICAL_SEPARATOR = '-------------------------'
GAME_STATE_X = -1
GAME_STATE_O = 1
GAME_STATE_DRAW = 0
GAME_STATE_NOT_ENDED = 2
BASIC_LENGTH = 3
ROW_METHOD=0
COL_METHOD=1
DIAG_METHOD=2

class Game:
    def __init__(self):
        self.resetBoard()
        
        # Sets default "current square" (board that player is allowed to play)
        
        self.currentSquare=[1,1]
        
    # Sets board for beginning of game
    
    def resetBoard(self):
        self.board=np.empty((3,3),dtype=object)
        
        # Instantiates the nine by nine grid of minigames
        
        for i in range(BASIC_LENGTH):
            for k in range(BASIC_LENGTH):
                self.board[i][k]=miniGame.miniGame()
        self.playerToMove=PLAYER_X_VAL
        
    # Checks legal moves
        
    def getAvailableMoves(self):
        availableMoves=[]
        
        # Gets legal moves from current square
        
        miniAvailable = self.board[self.currentSquare[0]][self.currentSquare[1]].getAvailableMoves()
        if (miniAvailable==[]):
            
            # If the current square is full, legalizes all buttons on board

            for i in range(BASIC_LENGTH):
                for j in range(BASIC_LENGTH):
                    miniAvailable=self.board[i][j].getAvailableMoves()
                    for k in range(len(miniAvailable)):
                        availableMoves.append([i,j,miniAvailable[k][0],miniAvailable[k][1]])
        else:
                    
            # Change the two item lists to four item list compatible with full board
        
            for k in range(len(miniAvailable)):
                availableMoves.append([self.currentSquare[0],self.currentSquare[1],miniAvailable[k][0],miniAvailable[k][1]])       
        return availableMoves
    
    # Makes move for the player whilen checking legality
    
    def move(self, loc):
        
        # If move is legal, makes move on smaller board, changes current square, changes player,
        # and returns true.  Otherwise, returns false
        
        available=self.getAvailableMoves()
        if (available.__contains__(loc)):
            self.board[loc[0]][loc[1]].move([loc[2],loc[3]],self.playerToMove)
            self.currentSquare=[loc[2],loc[3]]
            if self.playerToMove == PLAYER_X_VAL:
                self.playerToMove = PLAYER_O_VAL
            else:
                self.playerToMove = PLAYER_X_VAL
            return True
        return False
    
    # Checks for all possible wins
    
    def getGameResult(self):
        
        # Gets board states from individual boards
        
        boardStates=np.empty((3,3),dtype=object)
        for i in range(BASIC_LENGTH):
            for j in range(BASIC_LENGTH):
                boardStates[i][j]=self.board[i][j].getGameResult()[0]
                
        # Checks all possible wins for both "candidates" (X and O), returning who won, 
        # how they won, and where they won (example: [x victory, rows, row 2])
        
        # Rows
        
        for i in range(len(boardStates)):
            candidate = boardStates[i][0]
            start=i
            method=ROW_METHOD
            for j in range(len(boardStates[i])):
                if candidate != boardStates[i][j]:
                    candidate = 0
            if candidate != 0 and candidate != 2:
                return [candidate,start,method]

        # Columns
        
        for i in range(len(boardStates)):
            candidate = boardStates[0][i]
            start=i
            method=COL_METHOD
            for j in range(len(boardStates[i])):
                if candidate != boardStates[j][i]:
                    candidate = 0
            if candidate != 0 and candidate !=2:
                return [candidate,start,method]

        # First diagonal
        
        candidate = boardStates[0][0]
        start=0
        method=DIAG_METHOD
        for i in range(len(boardStates)):
            if candidate != boardStates[i][i]:
                candidate = 0
        if candidate != 0 and candidate !=2:
            return [candidate,start,method]

        # Second diagonal
        
        candidate = boardStates[0][2]
        start=2
        for i in range(len(boardStates)):
            if candidate != boardStates[i][len(boardStates[i]) - i - 1]:
                candidate = 0
        if candidate != 0 and candidate !=2:
            return [candidate,start,method]
        for i in range(len(boardStates)):
            for j in range(len(boardStates[i])):
                if boardStates[i][j] == GAME_STATE_NOT_ENDED:
                    return [GAME_STATE_NOT_ENDED,-1,-1]
        return [GAME_STATE_DRAW,-1,-1]
    
    # Returns individual square from board 
    
    def getSquare(self,i,j,k,l):
        return self.board[i][j].getSquare(k,l)
    
    # Returns a mini board from the larger board
    
    def getBoard(self,i,j):
        return self.board[i][j].getGameResult()
    
    # Returns full game state
    
    def getBigBoard(self):
        bd=np.empty(83,dtype=object)
        for i in range(BASIC_LENGTH):
            for j in range(BASIC_LENGTH):
                for k in range(BASIC_LENGTH):
                    for l in range(BASIC_LENGTH):
                        bd[27*i+9*j+3*k+l]=self.getSquare(i, j, k, l)
                        
        # Adds "current square" to game state to assist in neural network analysis.
        # This idea was a huge break through and made the AI significantly better
                        
        bd[81]=self.currentSquare[0]
        bd[82]=self.currentSquare[1]
        return bd