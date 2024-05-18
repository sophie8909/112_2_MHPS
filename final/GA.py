import numpy as np
import random
import copy
import json
import time
import cv2
from Evaluate import Evaluate
PARAMETERS = {}
Eva = Evaluate(original_img = "test/photo.png")

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
        self.value = Eva(self.lineSet)

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

def nonDominatedSorting(allPopulation:list):
    front = []

    for i in allPopulation:
        for j in allPopulation:
            if i != j:
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
        front.append([])
        front[r] = nowRank
        for i in front[r]:
            for j in i.sp:
                j.np -= 1
        r += 1

    return front

def CalculateCrowdingDistance(front:list):
    frontLength = len(front)
    for i in front:
        i.crowdDis = 0.0
    front.sort(key = lambda StringArt: StringArt.value)
    front[0].crowdDis = front[frontLength - 1].crowdDis = 999999999999

    for i in range(1, frontLength - 1):
        # value dis
        front[i].crowdDis += float(front[i + 1].value - front[i - 1].value) / (front[frontLength - 1].value - front[0].value) # 如果 decode 還沒寫好，這裡的分母記得+1才可以跑，不然會是0
        # num dis
        maxNum = max([m.lineNum for m in front])
        minNum = min([m.lineNum for m in front])
        front[i].crowdDis += float(abs(front[i + 1].lineNum - front[i - 1].lineNum)) / (maxNum - minNum)

def selection(populationSize:int, front:list):
    N = 0
    nextPopulation = []
    while N < populationSize:
        for i in range(len(front)):
            N = N + len(front[i])
            if N > populationSize:
                CalculateCrowdingDistance(front[i])
                front[i].sort(key = lambda StringArt: StringArt.crowdDis)
                front[i].reverse()
                for j in front[i]:
                    if len(nextPopulation) == populationSize:
                        break                
                    nextPopulation.append(j)              
                break
            else:
                nextPopulation.extend(front[i])

    return nextPopulation

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

    crossNum = int(float(min(len(oneUnique), len(twoUnique))) * crossoverRate)

    oneCross = set()
    twoCross = set()
    for i in range(crossNum):
        oneCross.add(oneUnique.pop())
        twoCross.add(twoUnique.pop())

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

        start = time.time()
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
            
            curPopulation.extend(newPopulation)

            front = nonDominatedSorting(curPopulation)

            nextPopulation = selection(PARAMETERS["num_of_populations"], front)

            if iteration == 0:
                bestList = copy.deepcopy(nextPopulation)
            else:
                totalList = copy.deepcopy(nextPopulation) + copy.deepcopy(bestList)
                for i in totalList:
                    i.np = 0
                    i.sp = []
                    i.rank = -1 
                nowBestFront = nonDominatedSorting(totalList)
                bestList = selection(PARAMETERS["num_of_populations"], nowBestFront)
            
            curPopulation = nextPopulation

        end = time.time()

        print("experient time: ", end-start)
        bestList.sort(key = lambda StringArt: StringArt.lineNum)
        for i in bestList:
            print(i.lineNum, i.value)
                

if __name__ == "__main__":
    main()