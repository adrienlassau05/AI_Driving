from datetime import datetime, timedelta
from config import RUN_TIME_HOURS, RUN_TIME_MINUTES, POPULATION_SIZE, NETWORK_VISUALISE, NODES_LAYER1, VISUALISE_EVERY
from env import Env
from brain import NeuralNetwork
import numpy as np
import matplotlib.pyplot as plt


running = True
current_time = datetime.now().time()
end_time = datetime.now() + timedelta(hours=RUN_TIME_HOURS) + timedelta(minutes=RUN_TIME_MINUTES)

env = Env(render=False, bounce=False, show_gates=False)

population_runs = 0  
networks, population_statistics = [], []
for network in range(POPULATION_SIZE):
    networks.append(NeuralNetwork(8, NODES_LAYER1, 2))
    
best_overall = [-10000, networks[0], 0]        #best reward, best network, run that it was added in
    
def mutate_matrix(matrix, deviation):   
    return matrix + np.random.normal(0, deviation, matrix.shape)

def inject_diversity(new_population):    
    for j in range(2):          #create random networks and strongly mutated networks
        new_population.append(NeuralNetwork(8, NODES_LAYER1, 2))
        child = new_population[j].clone()
        child = mutate(child, 0.3)
        new_population.append(child)
    return new_population
        

def mutate(network, deviation):
    network.w1 = mutate_matrix(network.w1, deviation)
    network.b1 = mutate_matrix(network.b1, deviation)
    network.w2 = mutate_matrix(network.w2, deviation)
    network.b2 = mutate_matrix(network.b2, deviation)
    return network


def repopulate_network(results, keep, stale=False):
    new_population = []
    strongest = results[:keep]
    for i in range(len(strongest)):
            new_population.append(strongest[i][1])
            
    if stale: 
        new_population = inject_diversity(new_population)
        num_clones = 3
        
    else:         
        num_clones = 4    
        
    for i in range(4):
        for j in range(num_clones):   
            child = new_population[i].clone()
            child = mutate(child, 0.1)
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
    stale = False
    for network in networks: 
        results.append((network.train(), network))
    results.sort(key=lambda x: x[0], reverse=True) 
    
    population_runs += 1

    if NETWORK_VISUALISE:
        if population_runs % VISUALISE_EVERY == 0:
            print(f'Best reward: {best_overall[0]}')
            best_overall[1].visualise()
            
    population_best, population_average, population_worst = get_statistics(results)
    population_statistics.append((population_best, population_average, population_worst))
    
    if population_best > best_overall[0]: 
        results[0][1].save('current_best_network')
        best_overall[0] = population_best
        best_overall[1] = results[0][1].clone()
        best_overall[2] = population_runs
    
    stale = population_runs - best_overall[2] >= 10
        
    networks = repopulate_network(results, 4, stale)



best_overall[1].visualise()  
x = np.arange(0, population_runs, 1)
plt.plot(x, population_statistics[0])
plt.plot(x, population_statistics[1])
plt.plot(x, population_statistics[2])
plt.legend('best reward', 'average reward', 'worst reward')
plt.show()        
    
    
