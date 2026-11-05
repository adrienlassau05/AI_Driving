import numpy as np
import pygame as pg
from env import Env
from sensors import observation_vector
from track import TRACK_BORDER, TRACK_BORDER_MASK
from config import FPS, NODES_LAYER1


class NeuralNetwork:
    
    def __init__(self, input_size, hidden_size, output_size, render=False):
        self.w1 = 2*np.random.uniform(-1, 1, (input_size, hidden_size))
        self.b1 = np.zeros((1, hidden_size))
        
        self.w2 = 2*np.random.uniform(-1, 1, (hidden_size, output_size))
        self.b2 = np.zeros((1, output_size))
        
        self.tested_populaton = 0
        self.env = Env(render=render, bounce=False, show_gates=True)
        
    
    def forward(self, X):        
        self.z1 = X @ self.w1 + self.b1 
        self.a1 = np.maximum(0, self.z1)
    
        self.z2 = self.a1 @ self.w2 + self.b2
        self.a2 = np.tanh(self.z2)
        
        return self.a2       
    
    def train(self):
        self.env.reset()
        reward = 0
        while not self.env.done:
            observations = observation_vector(self.env.car, TRACK_BORDER_MASK, TRACK_BORDER)
            outputs = self.forward(observations)
            action = outputs[0]
            reward = self.env.step(action)
        return reward
        
    def save(self, filename):
        np.savez(filename, W1=self.w1, b1=self.b1, W2=self.w2, b2=self.b2)
    
    def load(self, filename):
        data = np.load(filename)
        self.w1 = data['W1']
        self.b1 = data['b1']
        self.w2 = data['W2']
        self.b2 = data['b2']

    def clone(self):
        child = NeuralNetwork(8, NODES_LAYER1, 2)
        child.w1 = self.w1.copy()
        child.b1 = self.b1.copy()
        child.w2 = self.w2.copy()
        child.b2 = self.b2.copy()
        return child
    
    def visualise(self):
        self.env = Env(render=True, bounce=False, show_gates=True)
        self.env.reset()
        clock = pg.time.Clock()
        while not self.env.done:
            clock.tick(FPS)
            
            for event in pg.event.get():
                if event.type == pg.QUIT:
                    return
            
            observations = observation_vector(self.env.car, TRACK_BORDER_MASK, TRACK_BORDER)
            outputs = self.forward(observations)
            self.env.step(outputs[0])
            self.env.draw()
            
        pg.quit()