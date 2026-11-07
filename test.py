from datetime import datetime, timedelta
from config import (RUN_TIME_HOURS, RUN_TIME_MINUTES, POPULATION_SIZE, NETWORK_VISUALISE_BEST, 
                    NETWORK_VISUALISE_EVERY, NODES_LAYER1, VISUALISE_EVERY, NUMBER_OF_SENSORS)
from env import Env
from brain import NeuralNetwork
import numpy as np
import matplotlib.pyplot as plt
import pygame as pg

pg.init()

def mutate_matrix(matrix, deviation):   
    return matrix + np.random.normal(0, deviation, matrix.shape)

def inject_diversity(new_population, number):    
    for j in range(number):          
        new_population.append(NeuralNetwork(NUMBER_OF_SENSORS+1, NODES_LAYER1, 2))
        child = new_population[j].clone()
        child = mutate(child, 0.3)
        new_population.append(child)
    return new_population
        

def mutate(network, deviation):
    network.w1 = mutate_matrix(network.w1, deviation)
    network.b1 = mutate_matrix(network.b1, deviation)
    network.w2 = mutate_matrix(network.w2, deviation)
    network.b2 = mutate_matrix(network.b2, deviation)
    network.score = None
    return network


def repopulate_network(results, keep, stale=False):
    new_population = []
    strongest = results[:keep]
    for i in range(len(strongest)):
            new_population.append(strongest[i][1])
    empty_population = POPULATION_SIZE - keep

    if stale: 
        new_population = inject_diversity(new_population, keep//2)
        empty_population -= keep    
    
    full = empty_population // keep
    rem = max(0, empty_population % keep) 
    num_clones = []
    for i in range(keep):
        num_clones.append(full + (1 if i < rem else 0))
    
    for i in range(keep):
        for j in range(num_clones[i]):   
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
 

end_time = datetime.now() + timedelta(hours=RUN_TIME_HOURS) + timedelta(minutes=RUN_TIME_MINUTES)

env = Env(render=False, bounce=False, show_gates=False)
population_runs = 0  
networks, population_statistics = [], []
for network in range(POPULATION_SIZE):
    networks.append(NeuralNetwork(NUMBER_OF_SENSORS+1, NODES_LAYER1, 2))
    
best_overall = [-10000, networks[0], 0]        #best reward, best network, run that it was added in 
 
 
while datetime.now() < end_time:
    results = []
    stale = False
    for network in networks: 
        results.append((network.run(env), network))
    results.sort(key=lambda x: x[0], reverse=True) 
    
    population_runs += 1
            
    population_best, population_average, population_worst = get_statistics(results)
    population_statistics.append((population_best, population_average, population_worst))
    
    if population_best > best_overall[0]: 
        results[0][1].save('current_best_network')
        best_overall[0] = population_best
        best_overall[1] = results[0][1].clone()
        best_overall[2] = population_runs
        
        if NETWORK_VISUALISE_BEST:
            print(f'Best reward: {best_overall[0]}')
            best_overall[1].visualise()
        
    if NETWORK_VISUALISE_EVERY:
            if population_runs % VISUALISE_EVERY == 0:
                print(f'Best reward: {best_overall[0]}')
                best_overall[1].visualise()
                
    stale = population_runs - best_overall[2] >= 10
    num_kept = round(POPULATION_SIZE * 0.2)  
    networks = repopulate_network(results, num_kept, stale)
    if stale == True:
        best_overall[2] = population_runs


best, avg, worst = zip(*population_statistics)
best_overall[1].visualise()  
plt.plot(best, label='best')
plt.plot(avg, label='average')
plt.plot(worst, label='worst')
plt.legend()
plt.show()        
    
pg.quit()