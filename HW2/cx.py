from Factory import Factory, JobSequence, Job
import random
import copy
class CrossOver:
    def CX(self, parent1: JobSequence, parent2: JobSequence):
        # cycle crossover
        # select a random point
        changePoint = random.randint(0, parent1.num_of_jobs - 1)
        child1 = copy.deepcopy(parent1)
        child2 = copy.deepcopy(parent2)
        changed = []
        switch = True
        while switch:
            child1.sequence[changePoint], child2.sequence[changePoint] = child2.sequence[changePoint], child1.sequence[changePoint]
            changed.append(changePoint)
            nextNumber = child1.sequence[changePoint].id
            for i in range(parent1.num_of_jobs):
                if child1.sequence[i].id == nextNumber and i not in changed:
                    changePoint = i
                    break
                switch = False
        return child1, child2