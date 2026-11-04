from datetime import datetime, timedelta
from config import RUN_TIME, POPULATION_SIZE
from env import Env
from brain import NeuralNetwork
import random


running = True
current_time = datetime.now().time()
end_time = datetime.now() + timedelta(hours=RUN_TIME)

env = Env(render=False, bounce=False, show_gates=False)

population_runs = 0
networks = []
for network in range(POPULATION_SIZE):
    networks.append(NeuralNetwork(8, 6, 2))
    
def mutate_matrix(matrix):   
    for i in range(matrix.shape[0]):
        for j in range(matrix.shape[1]):
            matrix[i, j] += random.gauss(-0.1, 0.1)
    return matrix
    
def mutate(network):
    network.w1 = mutate_matrix(network.w1)
    network.b1 = mutate_matrix(network.b1)
    network.w2 = mutate_matrix(network.w2)
    network.b2 = mutate_matrix(network.b2)
    return network
    
def repopulate_network(results, keep):
    strongest = results[:keep]
    new_population = 0
    for i in range(strongest):
        new_population.append(strongest[i][1])
    for i in range(4):
        for j in range(4):   
            new_population.append(mutate(new_population[i]))
    return new_population
    

while datetime.now() < end_time:                           
    results = []
    for network in networks: 
        results.append(network.train(), network)
    results.sort(key=lambda x: x[0], reverse=True) 
    networks = repopulate_network(results)
    
    
        
    
    
