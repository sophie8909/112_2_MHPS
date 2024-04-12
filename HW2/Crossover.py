from Factory import Factory, JobSequence, Job
import random
import copy
class CrossOver:
    def __init__(self, method):
        self.method = method
    
    def crossover(self, parent1: JobSequence, parent2: JobSequence):
        if self.method == "CX":
            return self.CX(parent1, parent2)
        elif self.method == "LOX_1":
            return self.LOX_1(parent1, parent2)
        elif self.method == "LOX_2":
            return self.LOX_2(parent1, parent2)


    # one-point linear order crossover
    def LOX_1(self, parent1: JobSequence, parent2: JobSequence):
        # one-point crossover, random select a point
        point = random.randint(0, parent1.num_of_jobs)
        child1 = parent1.sequence[:point]
        for job in parent2.sequence:
            in_child1 = False
            for j in child1:
                if job.id == j.id:
                    in_child1 = True
                    break
            if in_child1 == False:
                child1.append(job)

        child2 = parent2.sequence[:point]
        for job in parent1.sequence:
            in_child2 = False
            for j in child2:
                if job.id == j.id:
                    in_child2 = True
                    break
            if in_child2 == False:
                child2.append(job)
        # print(point)
        # parent1.print()
        # parent2.print()
        # JobSequence(child1).print()
        # JobSequence(child2).print()

        return JobSequence(child1), JobSequence(child2)
    
    # two-point linear order crossover
    def LOX_2(self, parent1: JobSequence, parent2: JobSequence):
        point_l = random.randint(0, parent1.num_of_jobs)
        point_r = random.randint(point_l, parent1.num_of_jobs)
        child1 = parent1.sequence[point_l:point_r]
        left_part = []
        for job in parent2.sequence:
            in_child1 = False
            for j in child1:
                if job.id == j.id:
                    in_child1 = True
                    break
            if in_child1 == False:
                if len(left_part) < point_l + 1:
                    left_part.append(job)
                else:
                    child1.append(job)
        child1 = left_part + child1

        child2 = parent2.sequence[point_l:point_r]
        left_part = []
        for job in parent1.sequence:
            in_child2 = False
            for j in child2:
                if job.id == j.id:
                    in_child2 = True
                    break
            if in_child2 == False:
                if len(left_part) < point_l + 1:
                    left_part.append(job)
                else:
                    child2.append(job)
        child2 = left_part + child2
        
        # print(point_l, point_r)
        # parent1.print()
        # parent2.print()
        # JobSequence(child1).print()
        # JobSequence(child2).print()

        return JobSequence(child1), JobSequence(child2)
    
    # cycle crossover
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
        child1.print()
        child2.print()
        return child1, child2