'''
Created on Jun 20, 2021

@author: Rand
'''
from tensorflow.keras import optimizers
from tensorflow.keras import models
import random
import copy
import game
import model

# Assigns names for integers to avoid magic numbers

GAME_STATE_X = -1
GAME_STATE_O = 1
GAME_STATE_DRAW = 0
GAME_STATE_NOT_ENDED = 2
PLAYER_X_VAL = -1
PLAYER_O_VAL = 1

class Simulation:
    def __init__(self):
        self.trainingHistory=[]
        
    # Simulate random game
        
    def simulate(self, game):
        boardHistory=[]
        
        # Plays through random game while appending game state to training history
        
        while (game.getGameResult()[0] == GAME_STATE_NOT_ENDED):
            available=game.getAvailableMoves()
            move=available[random.randrange(0, len(available))]
            game.move(move)
            boardHistory.append(game.getBigBoard())
            
        # Get the history and build the training set
        
        result=game.getGameResult()[0]
        for boardState in boardHistory:
            self.trainingHistory.append((result, copy.deepcopy(boardState)))
        return result
    
    # Simulates multiple random games
    
    def simulateManyGames(self, numberOfGames):
        for i in range(numberOfGames):
            self.simulate(game.Game())
        return self.trainingHistory
    
    # Simulates a NeuralNetwork game
    
    def simulateNeuralNetwork(self, nnPlayer, game, model):
        playerToMove = PLAYER_X_VAL
        while (game.getGameResult()[0] == GAME_STATE_NOT_ENDED):
            availableMoves = game.getAvailableMoves()
            
            # Checks if move should be random or based on neural network
            
            if playerToMove == nnPlayer:
                
                # Looks for best move
                
                maxValue = 0
                bestMove = availableMoves[0]
                for availableMove in availableMoves:
                    
                    # Get a copy of a board and prepares it for neural network
                                        
                    boardCopy = copy.deepcopy(game.getBigBoard())
                    boardCopy[availableMove[0]*27+availableMove[1]*9+availableMove[2]*3+availableMove[3]] = nnPlayer
                    if nnPlayer == PLAYER_X_VAL:
                        value = model.predict(boardCopy, 0)
                    else:
                        value = model.predict(boardCopy, 2)
                    if value > maxValue:
                        maxValue = value
                        bestMove = availableMove
                selectedMove = bestMove
            else:
                
                # Random Move
                
                selectedMove = availableMoves[random.randrange(0, len(availableMoves))]
            game.move(selectedMove)
            
            # Switches player
            
            if playerToMove == PLAYER_X_VAL:
                playerToMove = PLAYER_O_VAL
            else:
                playerToMove = PLAYER_X_VAL
        return game.getGameResult()
    
    # Simulates many neural network games
    
    def simulateManyNeuralNetworkGames(self, nnPlayer, numberOfGames, model):
        nnPlayerWins = 0
        randomPlayerWins = 0
        draws = 0
        print ("NN player")
        print (nnPlayer)
        for i in range(numberOfGames):
            
            # Gets result from individual game and changes broader results accordingly
            
            result=self.simulateNeuralNetwork(nnPlayer, game.Game(), model)
            if result[0] == nnPlayer:
                nnPlayerWins = nnPlayerWins + 1
            elif result[0] == GAME_STATE_DRAW:
                draws = draws + 1
            else: randomPlayerWins = randomPlayerWins + 1
            totalWins = nnPlayerWins + randomPlayerWins + draws
            print ('X Wins: ' + str(int(nnPlayerWins * 100/totalWins)) + '%')
            print('O Wins: ' + str(int(randomPlayerWins * 100 / totalWins)) + '%')
            print('Draws: ' + str(int(draws * 100 / totalWins)) + '%')
            
        # returns overall accuracy of neural network
            
        return (nnPlayerWins-randomPlayerWins)/totalWins
if __name__ == '__main__':
    sim=Simulation()
    
    # Sets variables based on optimizer results
    
    learningRate=10**(-10.5)
    opt=optimizers.Adam(learning_rate=learningRate)
    batchSize=800
    epochs=10
    neuronCount=128
    layerCount=8
    initializer="random_normal"
    
    # Trains neural network
    
    trainingHistory=sim.simulateManyGames(100000)
    ticTacToeModel = model.TicTacToeModel(neuronCount, layerCount, opt, initializer, epochs, batchSize)
    ticTacToeModel.train(trainingHistory)
    
    # Saves model so neural network doesn't need to be trained every time
    
    models.save_model(
        ticTacToeModel.model, "Models/model1", overwrite=True, include_optimizer=True, save_format=None,
        signatures=None, options=None, save_traces=True
    )