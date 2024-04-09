import numpy as np
import random
import copy
import json
BEST_MAKESPAN = 2147483647
BEST_SEQUENCE = []
PARAMETERS = {}
class Job:
    def __init__(self, id):
        self.id = id
        self.processingTime = []
        self.minimalTime = -1
    def add(self, time):
        self.processingTime.append(time)
    def calculateMinimalTime(self):
        if self.minimalTime == -1:
            self.minimalTime = sum(self.processingTime)
        return self.minimalTime
class JobSequence:
    def __init__(self, jobs: list[Job]):
        self.sequence = jobs
        self.num_of_jobs = len(self.sequence)
        self.fitness = -1
        

        
class Factory:
    def __init__(self, num_of_machines: int):
        self.num_of_machines = num_of_machines
    
    def calculateMakespan(self, jobSequence: JobSequence):
        machine_end_time = [0] * factory.num_of_machines
        job_end_time = [0] * jobSequence.num_of_jobs
        for job in jobSequence.sequence:
            last_end_time = 0
            start_time = 0
            end_time = 0
            for machine in range(factory.num_of_machines):
                last_end_time = end_time
                start_time = max(machine_end_time[machine], last_end_time)
                end_time = start_time + job.processingTime[machine]
                machine_end_time[machine] = end_time
            job_end_time[job.id] = end_time
        return job_end_time[jobSequence.sequence[-1].id]

class CrossOver:
    def __init__(self, method):
        self.method = method
    
    def crossover(self, parent1: JobSequence, parent2: JobSequence):
        if self.method == "CX":
            return self.CX(parent1, parent2)
        elif self.method == "LOX":
            return self.LOX(parent1, parent2)

    def CX(self, parent1: JobSequence, parent2: JobSequence):
        # cycle crossover
        # select a random point
        point = random.randint(0, parent1.num_of_jobs)
        child1 = [-1] * parent1.num_of_jobs
        child2 = [-1] * parent1.num_of_jobs
        cycle = 0
        while -1 in child1:
            if cycle % 2 == 0:
                child1[point] = parent1.sequence[point]
                child2[point] = parent2.sequence[point]
            else:
                child1[point] = parent2.sequence[point]
                child2[point] = parent1.sequence[point]
            point = parent1.sequence.index(parent2.sequence[point])
            cycle += 1
        return JobSequence(child1), JobSequence(child2)


    def LOX(self, parent1: JobSequence, parent2: JobSequence):
        # one-point crossover, random select a point
        point = random.randint(0, parent1.num_of_jobs)
        child1 = parent1.sequence[:point]
        for job in parent2.sequence:
            if job not in child1:
                child1.append(job)

        child2 = parent2.sequence[:point]
        for job in parent1.sequence:
            if job not in child2:
                child2.append(job)
        
        return JobSequence(child1), JobSequence(child2)

def GetNeighbors(current: JobSequence, num_of_neighbors):
    neighbors = []
    for i in range(num_of_neighbors):
        neighbor = current
        i = random.randint(0, current.num_of_jobs - 1)
        j = random.randint(0, current.num_of_jobs - 1)
        neighbor.sequence[i], neighbor.sequence[j] = current.sequence[j], current.sequence[i]
        neighbors.append(neighbor)
    return neighbors

def GetNeighbor(current: JobSequence):
    neighbor = current
    
    i = random.randint(0, current.num_of_jobs - 1)
    j = random.randint(0, current.num_of_jobs - 1)
    neighbor.sequence[i], neighbor.sequence[j] = current.sequence[j], current.sequence[i]
        
    return neighbor

class Mutation:
    def __init__(self, method):
        self.method = method
    
    def mutate(self, jobSequence: JobSequence):
        if self.method == "cut_insert":
            return self.cut_insert(jobSequence)
        elif self.method == "reverse":
            return self.reverse(jobSequence)
        elif self.method == "mixed":
            return self.mixed(jobSequence)
    
    def cut_insert(self, jobSequence: JobSequence):
        # cut and insert
        k = random.randint(0, jobSequence.num_of_jobs)
        return JobSequence(jobSequence.sequence[k:] + jobSequence.sequence[:k])
    
    def reverse(self, jobSequence: JobSequence):
        # reverse the sequence
        jobSequence.sequence.reverse()
        return jobSequence

    def mixed(self, jobSequence: JobSequence):
        #If random_value is less than 0.5, execute plan one; otherwise, execute plan two
        random_value = random.random()
        if random_value < 0.5:
            # cut and insert
            k = random.randint(0, jobSequence.num_of_jobs)
            jobSequence = JobSequence(jobSequence.sequence[k:] + jobSequence.sequence[:k])
        else:
            # reverse the sequence
            jobSequence.sequence.reverse()
        return jobSequence

# IterativeImprovement
def LocalSearch(s, local_search_generation_size, local_search_neighbors_size):
    Evaluate(s)
    neighbors = GetNeighbors(s, local_search_neighbors_size)
    improved = True
    generation = 0
    while improved and generation < local_search_generation_size:
        improved = False
        for neighbor in neighbors:
            Evaluate(neighbor)
            if neighbor.fitness < s.fitness:
                s = neighbor
                improved = True
                break
        generation += 1
        neighbors = GetNeighbor(s)


def Evaluate(jobSequence):
    global BEST_MAKESPAN
    global BEST_SEQUENCE
    jobSequence.fitness = factory.calculateMakespan(jobSequence) 
    if jobSequence.fitness < BEST_MAKESPAN:
        BEST_MAKESPAN = jobSequence.fitness
        BEST_SEQUENCE = []
        for job in jobSequence.sequence:
            BEST_SEQUENCE.append(job.id)
    return jobSequence.fitness

def SelectParent(populations: list[JobSequence]):
    # random select
    return random.choice(populations)

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
            parent1 = SelectParent(populations)
            parent2 = SelectParent(populations)
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
            LocalSearch(s, PARAMETERS["local_search_generation_size"], PARAMETERS["local_search_neighbors_size"])
            

if __name__ == "__main__":
    dataName = ["20_5_1", "20_10_1", "20_20_1", "50_5_1", "50_10_1", "50_20_1", "100_5_1", "100_10_1", "100_20_1"]
    # read parameters from json file
    PARAMETERS = {}
    with open("parameters.json", "r") as f:
        PARAMETERS = json.load(f)
    

    for i in range(9):
        BEST_MAKESPAN = 2147483647
        BEST_SEQUENCE = []
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
            # for job in allJobs:
            #     print(job.id)
            factory = Factory(len(allJobs[0].processingTime))
            
            # n: number of populations
            MA(allJobs, PARAMETERS["num_of_populations"], PARAMETERS["MA_iterations"], PARAMETERS["probability_crossover"], PARAMETERS["num_learner"])

            with open("TA0"+str(i)+"1.txt", "w+") as of:
                for job in BEST_SEQUENCE:
                    of.write(str(job) + " ")
            print("TA0"+str(i)+"1.txt: ", BEST_MAKESPAN)