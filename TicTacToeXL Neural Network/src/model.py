'''
Created on Jun 24, 2021

@author: Rand
'''
from tensorflow.keras.layers import Dense
from tensorflow.keras.models import Sequential
from tensorflow.keras.utils import to_categorical
import numpy as np


class TicTacToeModel:

    def __init__(self, neuronCount, layerCount, opt, initializer, epochs, batchSize):
        
        # Sets variables for model
        
        self.epochs = epochs
        self.batchSize = batchSize
        self.numberOfInputs = 83
        self.numberOfOutputs = 3
        self.model = Sequential()
        
        # Make layers
        
        self.model.add(Dense(self.numberOfInputs, activation='relu', input_shape=(self.numberOfInputs, )))
        for i in range(layerCount):
            self.model.add(Dense(neuronCount, activation='relu', kernel_initializer=initializer))
        self.model.add(Dense(self.numberOfOutputs, activation='softmax'))
        
        # Compile model
        
        self.model.compile(loss='categorical_crossentropy', optimizer=opt, metrics=['accuracy'])
        
    # Trains neural network with dataset
        
    def train(self, dataset):
        inp = []
        out = []
        
        # Separates game state (inp) from result (out)
        
        for data in dataset:
            inp.append(data[1])
            out.append(data[0])

        X = np.array(inp).reshape((-1, self.numberOfInputs))
        y = to_categorical(out, num_classes=3)
        
        # Train and test data split
        
        boundary = int(0.8 * len(X))
        X_train = X[:boundary]
        X_test = X[boundary:]
        y_train = y[:boundary]
        y_test = y[boundary:]
        
        # Trains neural network after preparing input data
        
        X_train=np.asarray(X_train).astype(np.int)
        y_train=np.asarray(y_train).astype(np.int)
        X_test=np.asarray(X_test).astype(np.int)
        y_test=np.asarray(y_test).astype(np.int)
        self.model.fit(X_train, y_train, validation_data=(X_test, y_test), epochs=self.epochs, batch_size=self.batchSize)

    # Plugs game state into neural network and returns probability of "index" victory

    def predict(self, data, index):
        data=np.asarray(data).astype(np.int)
        return self.model.predict(np.array(data).reshape(-1, self.numberOfInputs))[0][index]
if __name__ == '__main__':
    pass