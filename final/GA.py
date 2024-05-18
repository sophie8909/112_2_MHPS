import numpy as np
import random
import copy
import json
import time
import cv2
from Evaluate import Evaluate
PARAMETERS = {}

class StringArt():
    def __init__(self):
        self.lineSet = set()
        self.lineNum = random.randint(2000, 5000)
        self.np = 0
        self.sp = []
        self.rank = -1
        self.crowdDis = 0.0

        for i in range(self.lineNum):
            while True:
                a = random.randint(1, 287)
                b = random.randint(a + 1, 288)
                if((a, b) not in self.lineSet):
                    self.lineSet.add((a, b))
                    break
        
        self.evaluate()

    def evaluate(self):
        self.value = Evaluate(self.lineSet)

    def mutation(self):
        decide = random.random()
        # add 10% lines
        if decide < 1.0 / 3.0:
            addNumber = int(self.lineNum * 0.1)
            for i in range(addNumber):
                while True:
                    a = random.randint(1, 287)
                    b = random.randint(a + 1, 288)
                    if((a, b) not in self.lineSet):
                        self.lineSet.add((a, b))
                        break
            self.lineNum += addNumber
        # remove 10% lines
        elif decide < 2.0 / 3.0:
            deleteNumber = int(self.lineNum * 0.1)
            for i in range(deleteNumber):
                self.lineSet.pop()
            self.lineNum -= deleteNumber
        #change 10% lines
        else:
            changeNumber = int(self.lineNum * 0.1)
            for i in range(changeNumber):
                self.lineSet.pop()
            for i in range(changeNumber):
                while True:
                    a = random.randint(1, 287)
                    b = random.randint(a + 1, 288)
                    if((a, b) not in self.lineSet):
                        self.lineSet.add((a, b))
                        break

def nonDominatedSorting(allPopulation):
    front = []

    for i in allPopulation:
        for j in allPopulation:
            if i.lineNum < j.lineNum and i.value < j.value:
                i.sp.append(j)
                j.np += 1
    
    r = 0
    while 1:
        nowRank = []
        for i in allPopulation:
            if i.np == 0 and i.rank == -1:
                nowRank.append(i)
                i.rank = r
        if len(nowRank) == 0:
            break
        front[r] = nowRank
        for i in front[r]:
            for j in i.sp:
                j.np -= 1
        r += 1

    return front

    

def CalculateCrowdingDistance(front, chromsObjRecord):
    pass

def selection(populationSize, front):
    pass

def initPopulation(populationSize:int, initMethod:str):
    if initMethod == "random":
        ret = []
        for i in range(populationSize):
            newStringArt = StringArt()
            ret.append(newStringArt)
        return ret
    else:
        pass

def crossover(parent1:StringArt, parent2:StringArt, crossoverRate:float):
    oneUnique = parent1.lineSet - parent2.lineSet
    twoUnique = parent2.lineSet - parent1.lineSet
    crossNum = int(float(min(len(oneUnique) + len(twoUnique))) * crossoverRate)

    oneCross = random.sample(parent1.lineSet, crossNum)
    twoCross = random.sample(parent2.lineSet, crossNum)

    for i in range(crossNum):
        oneToTwo = oneCross.pop()
        twoToOne = twoCross.pop()

        parent1.lineSet.remove(oneToTwo)
        parent2.lineSet.add(oneToTwo)

        parent1.lineSet.add(twoToOne)
        parent2.lineSet.remove(twoToOne)

def main():
    with open("GA_config.json", "r") as f:
        PARAMETERS = json.load(f)

    for experientTimes in range(1):

        curPopulation = initPopulation(PARAMETERS["num_of_populations"], PARAMETERS["init_method"])
        bestList = []

        for iteration in range(PARAMETERS["iterations"]):

            for i in curPopulation:
                i.np = 0
                i.sp = []
                i.rank = -1            
            
            newPopulation = []

            while len(newPopulation) < PARAMETERS["num_of_populations"]:
                epsilon = random.random()
                [parent1, parent2] = random.sample(curPopulation, 2)
                child1 = copy.deepcopy(parent1)
                child2 = copy.deepcopy(parent2)

                if epsilon <= PARAMETERS["crossover_probability"]:
                    crossover(child1, child2, PARAMETERS["crossover_rate"])
                else:
                    child1.mutation()
                    child2.mutation()

                child1.evaluate()
                child2.evaluate()
                newPopulation.append(child1)
                newPopulation.append(child2)
            
            curPopulation.append(newPopulation)

            front = nonDominatedSorting(curPopulation)

            nextPopulation = selection(PARAMETERS["num_of_populations"], front)

            if iteration == 0:
                bestList = copy.deepcopy(nextPopulation)
            else:
                totalList = copy.deepcopy(nextPopulation) + copy.deepcopy(bestList)
                nowBestFront = nonDominatedSorting(totalList)
                bestList = selection(PARAMETERS["num_of_populations"], nowBestFront)
                

if __name__ == "__main__":
    main()