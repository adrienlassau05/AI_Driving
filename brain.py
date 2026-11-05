import numpy as np
from env import Env
from sensors import observation_vector
from track import TRACK_BORDER, TRACK_BORDER_MASK

class NeuralNetwork:
    
    def __init__(self, input_size, hidden_size, output_size):
        self.w1 = np.random.rand(input_size, hidden_size)
        self.b1 = np.zeros((1, hidden_size))
        
        self.w2 = np.random.rand(hidden_size, output_size)
        self.b2 = np.zeros((1, output_size))
        
        self.tested_populaton = 0
        self.env = Env()
    
    def forward(self, X):
        self.z1 = self.w1 @ X + self.b1 
        self.a1 = np.maximum(0, self.z1)
    
        self.z2 = self.w2 @ self.a1 + self.b2
        self.a2 = np.tanh(self.z2)
        return self.a2       
    
    def train(self):
        self.env.reset()
        reward = 0
        while not self.env.done:
            observations = observation_vector(self.env.car, TRACK_BORDER_MASK, TRACK_BORDER)
            outputs = self.forward(observations)
            action = outputs.tolist()
            reward += self.env.step(action)
        return reward
        
    def save(self, filename):
        np.savez(filename, W1=self.w1, b1=self.b1, W2=self.w2, b2=self.b2)
    
    def load(self, filename):
        data = np.load(filename)
        self.w1 = data['W1']
        self.b1 = data['b1']
        self.w2 = data['W2']
        self.b2 = data['b2']

        