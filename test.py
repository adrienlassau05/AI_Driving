from datetime import datetime, timedelta
from config import RUN_TIME, POPULATION_SIZE
from env import Env
from brain import NeuralNetwork
import numpy as np
import matplotlib.pyplot as plt
import copy


running = True
current_time = datetime.now().time()
end_time = datetime.now() + timedelta(hours=RUN_TIME)

env = Env(render=False, bounce=False, show_gates=False)

population_runs, best_reward = 0, 0
networks, population_statistics = [], []
for network in range(POPULATION_SIZE):
    networks.append(NeuralNetwork(8, 6, 2))
    
def mutate_matrix(matrix):   
    return matrix + np.random.normal(0, 0.1, matrix.shape)
    
def repopulate_network(results, keep):
    strongest = results[:keep]
    new_population = []
    for i in range(len(strongest)):
        new_population.append(strongest[i][1])
    for i in range(4):
        for j in range(4):   
            child = copy.deepcopy(new_population[i])
            new_population.append(mutate_matrix(child))
    return new_population
    
    
def population_statistics(population):
    rewards = []
    population_average = 0
    for i in range(len(population)):
        rewards.append(population[i][0])
        population_average += population[i][0]
    population_average = population_average / len(population)
    return rewards[0], population_average, rewards[-1]
    
        
while datetime.now() < end_time:
    results = []
    for network in networks: 
        results.append((network.train(), network))
    results.sort(key=lambda x: x[0], reverse=True) 
    population_best, population_average, population_worst = population_statistics(results)
    population_statistics.append((population_best, population_average, population_worst))
    if population_best > best_reward: 
        results[0][1].save('current_best_network')
        best_reward = population_best
    networks = repopulate_network(results)


    
x = np.arange(1, len(population_statistics), 1)
plt.plot(x, population_statistics[0])
plt.plot(x, population_statistics[1])
plt.plot(x, population_statistics[2])
plt.legend()
plt.show()        
    
    
