'''
Created on Jun 30, 2021

@author: Rand
'''
from tensorflow.keras import optimizers
import time
import model
import Simulate
class Optimizer:
    def __init__(self):
        
        # Independent variables
        
        self.learningRate=10**(-10.5)
        self.opt=optimizers.Adam(learning_rate=self.learningRate)
        self.batchSize=800
        self.epochs=10
        self.neuronCount=128
        self.layerCount=8
        self.initializer="random_normal"
        
        # Gathers training history
        
        self.simulator=Simulate.Simulation()
        self.trainingHistory=self.simulator.simulateManyGames(10000)
        self.askTest()
        
    # Asks user to select an independent variable
        
    def askTest(self):
        test=input("What element will be tested?")
        if (test=="Learning Rate"):
            self.testLearningRate()
            print("Testing ", test)
        elif (test=="Optimizer"):
            self.testOptimizer()
            print("Testing ", test)
        elif (test=="Batch Size"):
            self.testBatchSize()
            print("Testing ", test)
        elif (test=="NeuronCount"):
            self.testNeuronCount()
            print("Testing ", test)
        elif (test=="LayerCount"):
            self.testLayerCount()
            print("Testing ", test)
        elif (test=="Initializer"):
            self.testInitializer()
            print("Testing ", test)
        elif (test=="Epochs"):
            self.testEpochs()
            
            
    # Testing plans for all possible dependent variables printed to 
    # files with records of success for future use
            
            
    def testLearningRate(self):
        with open('Optimizer Log/LearningRateTest3', 'w') as f:
            for i in range(0,10):
                self.learningRate=10**(i*.4-11)
                self.opt=optimizers.Adam(learning_rate=self.learningRate)
                result=self.test()
                print("A learning rate of 10^(-",i*.4-11,") yielded a time of", result[0], "and an accuracy of ", result[1],file=f)
    def testOptimizer(self):
        with open('Optimizer Log/OptimizerTest1', 'w') as f:
            self.opt=optimizers.Adam(learning_rate=self.learningRate)
            result=self.test()
            print("Adam optimizer yielded a time of ", result[0], "and an accuracy of ", result[1], file=f)
            self.opt=optimizers.SGD(learning_rate=self.learningRate)
            result=self.test()
            print("SGD optimizer yielded a time of ", result[0], "and an accuracy of ", result[1], file=f)
            self.opt=optimizers.RMSprop(learning_rate=self.learningRate)
            result=self.test()
            print("RMSProp optimizer yielded a time of ", result[0], "and an accuracy of ", result[1], file=f)
            self.opt=optimizers.Adamax(learning_rate=self.learningRate)
            result=self.test()
            print("Adamax optimizer yielded a time of ", result[0], " =and an accuracy of ", result[1], file=f)
            self.opt=optimizers.Adagrad(learning_rate=self.learningRate)
            result=self.test()
            print("Adagrad optimizer yielded a time of ", result[0], "and an accuracy of ", result[1], file=f)
    def testBatchSize(self):
        with open('Optimizer Log/BatchSizeTest4', 'w') as f:    
            for i in range(200,2000,100):
                self.batchSize=i
                result=self.test()
                print("A batchsize of",self.batchSize, "yielded a time of", result[0], "and an accuracy of ", result[1], file=f)
    def testEpochs(self):
        with open('Optimizer Log/EpochTest1', 'w') as f:
            for i in range(10, 200, 20):
                self.epochs=i
                result=self.test()
                print(self.epochs, "epochs yielded a time of", result[0], "and an accuracy of ", result[1], file=f)
    def testNeuronCount(self):
        with open('Optimizer Log/NeuronTest2', 'w') as f:
            for i in range(1,10):
                self.neuronCount=2**(i/2)
                result=self.test()
                print("A neuron count of",self.neuronCount, "yielded a time of", result[0], "and an accuracy of ", result[1], file=f)
    def testLayerCount(self):
        with open('Optimizer Log/LayerTest2', 'w') as f:
            for i in range(8,12):
                self.layerCount=i
                result=self.test()
                print("A layer count of",self.layerCount, "yielded a time of", result[0], "and an accuracy of ", result[1], file=f)
    def testInitializer(self):
        initializers=["random_uniform", "random_normal","glorot_uniform", "TruncatedNormal", 
                      "glorot_normal","zeros","ones","orthogonal","identity"]
        with open('Optimizer Log/InitializerTest1', 'w') as f:
            for i in initializers:
                self.initializer=i
                result=self.test()
                print("Initializer",self.initializer, "yielded a time of", result[0], "and an accuracy of ", result[1], file=f)
    def test(self):
        t1=time.time()
        m=model.TicTacToeModel(self.neuronCount,self.layerCount,
                             self.opt,self.initializer,self.epochs,self.batchSize)
        m.train(self.trainingHistory)
        t2=time.time()
        return [t2-t1,self.simulator.simulateManyNeuralNetworkGames(-1, 500, m)]
if __name__ == '__main__':
    o=Optimizer()
            
            
        