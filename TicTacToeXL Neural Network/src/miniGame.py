'''
Created on Jun 16, 2021

@author: Rand
'''

# Assigns names for integers to avoid magic numbers

PLAYER_X = 'X'
PLAYER_O = 'O'
EMPTY = ' '
PLAYER_X_VAL = -1
PLAYER_O_VAL = 1
EMPTY_VAL = 0
HORIZONTAL_SEPARATOR = '|'
GAME_STATE_X = -1
GAME_STATE_O = 1
GAME_STATE_DRAW = 0
GAME_STATE_NOT_ENDED = 2
ROW_METHOD=0
COL_METHOD=1
DIAG_METHOD=2

class miniGame:
    def __init__(self):
        self.resetBoard()
        
    # Resets board
        
    def resetBoard(self):
        self.board = [
            [0, 0, 0],
            [0, 0, 0],
            [0, 0, 0]
        ]        
        
    # Sets board for beginning of game
        
    def getGameResult(self):
        
        # Checks all possible wins for both "candidates" (X and O), returning who won, 
        # how they won, and where they won (example: [x victory, rows, row 2])
                
        # Rows
        
        for i in range(len(self.board)):
            candidate = self.board[i][0]
            start=i
            method=ROW_METHOD
            for j in range(len(self.board[i])):
                if candidate != self.board[i][j]:
                    candidate = 0
            if candidate != 0:
                return [candidate,start,method]

        # Columns
        
        for i in range(len(self.board)):
            candidate = self.board[0][i]
            start=i
            method=COL_METHOD
            for j in range(len(self.board[i])):
                if candidate != self.board[j][i]:
                    candidate = 0
            if candidate != 0:
                return [candidate,start,method]

        # First diagonal
        
        candidate = self.board[0][0]
        start=0
        method=DIAG_METHOD
        for i in range(len(self.board)):
            if candidate != self.board[i][i]:
                candidate = 0
        if candidate != 0:
            return [candidate,start,method]

        # Second diagonal
        
        candidate = self.board[0][2]
        start=2
        for i in range(len(self.board)):
            if candidate != self.board[i][len(self.board[i]) - i - 1]:
                candidate = 0
        if candidate != 0:
            return [candidate,start,method]
        for i in range(len(self.board)):
            for j in range(len(self.board[i])):
                if self.board[i][j] == EMPTY_VAL:
                    return [GAME_STATE_NOT_ENDED,-1,-1]
        return [GAME_STATE_DRAW,-1,-1]
    
    # Returns legal moves (squares that have not yet been chosen)
    
    def getAvailableMoves(self):
        availableMoves = []
        for i in range(len(self.board)):
            for j in range(len(self.board[i])):
                if (self.board[i][j]) == EMPTY_VAL:
                    availableMoves.append([i, j])
        return availableMoves
    
    # Makes move
    
    def move(self, position, player):
        availableMoves = self.getAvailableMoves()
        for i in range(len(availableMoves)):
            if position[0] == availableMoves[i][0] and position[1] == availableMoves[i][1]:
                self.board[position[0]][position[1]] = player
    
    # Gets square from board            
    
    def getSquare(self,i,j):
        return self.board[i][j]