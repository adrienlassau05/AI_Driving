from datetime import datetime, timedelta
from config import RUN_TIME_HOURS, RUN_TIME_MINUTES, POPULATION_SIZE, NETWORK_VISUALISE
from env import Env
from brain import NeuralNetwork
import numpy as np
import matplotlib.pyplot as plt
import copy


running = True
current_time = datetime.now().time()
end_time = datetime.now() + timedelta(hours=RUN_TIME_HOURS) + timedelta(minutes=RUN_TIME_MINUTES)

env = Env(render=False, bounce=False, show_gates=False)

best_overall = None
population_runs, best_reward = 0, float('-inf')    
networks, population_statistics = [], []
for network in range(POPULATION_SIZE):
    networks.append(NeuralNetwork(8, 6, 2))
    
def mutate_matrix(matrix):   
    return matrix + np.random.normal(0, 0.1, matrix.shape)

def mutate(network):
    network.w1 = mutate_matrix(network.w1)
    network.b1 = mutate_matrix(network.b1)
    network.w2 = mutate_matrix(network.w2)
    network.b2 = mutate_matrix(network.b2)
    return network

def repopulate_network(results, keep):
    strongest = results[:keep]
    new_population = []
    for i in range(len(strongest)):
        new_population.append(strongest[i][1])
    for i in range(4):
        for j in range(4):   
            child = new_population[i].clone()
            child = mutate(child)
            new_population.append(child)
    return new_population
    
    
def get_statistics(population):
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
    best_reward, best_network = results[0]
    
    if NETWORK_VISUALISE:
        print(f'Best reward: {best_reward}')
        best_network.visualise()
    
    population_best, population_average, population_worst = get_statistics(results)
    population_statistics.append((population_best, population_average, population_worst))
    
    if population_best > best_reward: 
        results[0][1].save('current_best_network')
        best_reward = population_best
        best_overall = results[0][1].clone()
        
    networks = repopulate_network(results, 4)


best_overall.visualise()  
x1 = np.arange(0, len(population_statistics[0]), 1)
x2 = np.arange(0, len(population_statistics[1]), 1)
x3 = np.arange(0, len(population_statistics[2]), 1)
plt.plot(x1, population_statistics[0])
plt.plot(x2, population_statistics[1])
plt.plot(x3, population_statistics[2])
plt.legend('best reward', 'average reward', 'worst reward')
plt.show()        
    
    
