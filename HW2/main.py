import numpy as np
import random
import copy
import json
import time
from Factory import Factory, JobSequence, Job
from Mutation import Mutation
from Crossover import CrossOver
BEST_MAKESPAN = 2147483647
# BEST_SEQUENCE = []
PARAMETERS = {}    

def GetNeighbors(current: JobSequence, num_of_neighbors):
    neighbors = []
    for i in range(num_of_neighbors):
        neighbor = copy.deepcopy(current)  # Create a deep copy of the current sequence
        i = random.randint(0, current.num_of_jobs - 1)
        j = random.randint(0, current.num_of_jobs - 1)
        neighbor.sequence[i], neighbor.sequence[j] = current.sequence[j], current.sequence[i]
        neighbors.append(neighbor)
    return neighbors

def GetNeighbor(current: JobSequence):
    neighbor = copy.deepcopy(current)
    
    i = random.randint(0, current.num_of_jobs - 1)
    j = random.randint(0, current.num_of_jobs - 1)
    neighbor.sequence[i], neighbor.sequence[j] = current.sequence[j], current.sequence[i]
        
    return neighbor

# IterativeImprovement
def LocalSearch(s, local_search_generation_size, local_search_neighbors_size, mode):
    Evaluate(s)
    neighbors = GetNeighbors(s, local_search_neighbors_size)
    improved = True
    generation = 0
    while improved and generation < local_search_generation_size:
        improved = False
        for neighbor in neighbors:
            Evaluate(neighbor)
            if neighbor.fitness < s.fitness:
                if mode == "Lamarckian":
                    s = neighbor
                elif mode == "Baldwinian":
                    s.fitness = neighbor.fitness
                else:
                    print("Invalid mode in LocalSearch")
                improved = True
                break
        generation += 1
        neighbors = GetNeighbors(s, local_search_neighbors_size)


def Evaluate(jobSequence):
    global BEST_MAKESPAN
    # global BEST_SEQUENCE
    jobSequence.fitness = factory.calculateMakespan(jobSequence) 
    if jobSequence.fitness < BEST_MAKESPAN:
        BEST_MAKESPAN = jobSequence.fitness
        # BEST_SEQUENCE = []
        # for job in jobSequence.sequence:
        #     BEST_SEQUENCE.append(job.id)
    return jobSequence.fitness

def SelectParents(populations: list[JobSequence], k: int):
    # random select
    return random.sample(populations, k)


def EnvironmentSelection(populations, new_populations):
    # select the best 50% of the populations
    all_populations = populations + new_populations
    all_populations.sort(key=lambda x: x.fitness)
    return all_populations[:len(populations)]

def SelectLearner(populations: list[JobSequence]):
    # random select
    return random.choice(populations)

def InitPopulation(allJobs, init_population_size: int):
    ret = []
    for job in allJobs:
        job.calculateMinimalTime()
    init = sorted(allJobs, key = lambda x: x.minimalTime)
    initJobSequence = JobSequence(init)
    ret.append(initJobSequence)
    ret.extend(GetNeighbors(initJobSequence, init_population_size-1))
    return ret

def MA(allJobs, num_of_populations, iteration, probability_crossover, num_learner):
    populations = InitPopulation(allJobs, num_of_populations)

    for population in populations:
        Evaluate(population)
        
    for t in range(iteration):
        new_populations = []
        for population in populations:
            parent1, parent2 = SelectParents(populations, 2)
            child1, child2 = parent1, parent2
            if random.random() < probability_crossover:
                x = CrossOver(PARAMETERS["crossover_method"])
                child1, child2 = x.crossover(parent1, parent2)
            else:
                m = Mutation(PARAMETERS["mutation_method"])
                child1 = m.mutate(child1)
                child2 = m.mutate(child2)
            Evaluate(child1)
            Evaluate(child2)
            new_populations.append(child1)
            new_populations.append(child2)
            
        populations = EnvironmentSelection(populations, new_populations)

        for i in range(num_learner):
            s = SelectLearner(populations)
            LocalSearch(s, PARAMETERS["local_search_generation_size"], PARAMETERS["local_search_neighbors_size"], PARAMETERS["local_search_mode"])
            

if __name__ == "__main__":
    dataName = ["20_5_1", "20_10_1", "20_20_1", "50_5_1", "50_10_1", "50_20_1", "100_5_1", "100_10_1", "100_20_1"]
    
    # read parameters from json file
    PARAMETERS = {}
    with open("parameters.json", "r") as f:
        PARAMETERS = json.load(f)
    
    
    for i in range(9):
        of = open("TA0"+str(i)+"1_record.txt", "w+")
        sum = 0.0
        time_sum = 0.0
        total_best = 2147483647
        total_wrost = -1
        result = []
        for tries in range(20):
            BEST_MAKESPAN = 2147483647
            # BEST_SEQUENCE = []
            with open("data/tai"+dataName[i]+".txt", "r") as f:
                allJobs = []
                lines = f.readlines()
                lines = lines[1:]
                for j in range(len(lines)):
                    numbers = list(map(int, lines[j].split()))
                    
                    if j == 0:
                        for k in range(len(numbers)):
                            allJobs.append(Job(k))
                    
                    for k in range(len(numbers)):
                        allJobs[k].add(numbers[k])
                factory = Factory(len(allJobs[0].processingTime))
                
                start_time = time.time()
                # n: number of populations
                MA(allJobs, PARAMETERS["num_of_populations"], PARAMETERS["MA_iterations"], PARAMETERS["probability_crossover"], PARAMETERS["num_learner"])

                end_time = time.time()

                time_sum += end_time - start_time

                result.append(BEST_MAKESPAN)
                sum += float(BEST_MAKESPAN)
                if BEST_MAKESPAN < total_best:
                    total_best = BEST_MAKESPAN
                if total_wrost < BEST_MAKESPAN:
                    total_wrost = BEST_MAKESPAN

                of.write(str(BEST_MAKESPAN) + "\n")
                print("TA0"+str(i)+"1_"+str(tries), BEST_MAKESPAN)
        of.close()
        average = sum / 20.0
        sd = 0
        for j in range(20):
            sd += (float(result[j]) - average) ** 2
        sd /= 20.0
        sd = sd ** 0.5
        with open("TA0"+str(i)+"1_conclusion.txt", "w+") as of:
            of.write(f"best: {total_best}\n")
            of.write(f"wrost: {total_wrost}\n")
            of.write(f"average: {average}\n")
            of.write(f"deviation: {sd}\n")
            of.write(f"average rum time: {time_sum / 20.0}")