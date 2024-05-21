import numpy as np
import random
import copy
import json
import time
import cv2
import matplotlib.pyplot as plt
from Evaluate import Evaluate
from Draw import StringArtDrawer
from threadTone import ThreadTone
PARAMETERS = {}

class StringArtParameter():    
    def __init__(self):
        
        # parameters for nsga-ii
        self.np = 0
        self.sp = []
        self.rank = -1
        self.crowdDis = 0.0

        
        self.pinNum = random.randint(PARAMETERS["pins_min_num"], PARAMETERS["pins_max_num"])
        self.lineNum = random.randint(PARAMETERS["line_min_num"], PARAMETERS["line_max_num"])
        self.lineWidth = random.randint(PARAMETERS["line_width_min"], PARAMETERS["line_width_max"])
            
        self.evaluate()
    
    def crossover(self, parent2):
        self.pinNum = (self.pinNum + parent2.pinNum) // 2
        self.lineNum = (self.lineNum + parent2.lineNum) // 2
        self.lineWidth = (self.lineWidth + parent2.lineWidth) // 2

    def evaluate(self):
        global allVisitedParameter, imgPath
        
        key = (self.pinNum, self.lineNum, self.lineWidth)
        if key in allVisitedParameter:
            self.value, self.image = allVisitedParameter[key]
        else:
            threadTone = ThreadTone(imgPath, self.pinNum, self.lineNum, self.lineWidth)
            self.image = copy.deepcopy(threadTone.imgResult)
            self.value = Eva(self.image)
            allVisitedParameter[key] = (self.value, self.image)

    def mutation(self):
        decide = random.random()
        # change lineNum
        if decide < 1.0 / 3.0:
            self.lineNum = random.randint(PARAMETERS["line_min_num"], PARAMETERS["line_max_num"])
        # change lineWidth
        elif decide < 2.0 / 3.0:
            self.lineWidth = random.randint(PARAMETERS["line_width_min"], PARAMETERS["line_width_max"])
        # change pinNum
        else:
            self.pinNum = random.randint(PARAMETERS["pins_min_num"], PARAMETERS["pins_max_num"])
            

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
    front.sort(key = lambda StringArtParameter: StringArtParameter.value)
    front[0].crowdDis = front[frontLength - 1].crowdDis = 999999999999

    for i in range(1, frontLength - 1):
        # value dis
        if front[frontLength - 1].value - front[0].value != 0:
            front[i].crowdDis += float(front[i + 1].value - front[i - 1].value) / (front[frontLength - 1].value - front[0].value)
        # num dis
        maxNum = max([m.lineNum for m in front])
        minNum = min([m.lineNum for m in front])
        if maxNum - minNum != 0:
            front[i].crowdDis += float(abs(front[i + 1].lineNum - front[i - 1].lineNum)) / (maxNum - minNum)

def selection(populationSize:int, front:list) -> list:
    N = 0
    nextPopulation = []
    while N < populationSize:
        for i in range(len(front)):
            N = N + len(front[i])
            if N > populationSize:
                CalculateCrowdingDistance(front[i])
                front[i].sort(key = lambda StringArtParameter: StringArtParameter.crowdDis)
                front[i].reverse()
                for j in front[i]:
                    if len(nextPopulation) == populationSize:
                        break                
                    nextPopulation.append(j)              
                break
            else:
                nextPopulation.extend(front[i])

    return nextPopulation

def InitializePopulation(populationSize:int) -> list:
    init_population = []
    for i in range(populationSize):
        newStringArtParameter = StringArtParameter()
        init_population.append(newStringArtParameter)
        print("complete init popuplation: ", i + 1)
    return init_population

def main():
    
    start = time.time()
    for experientTimes in range(1):
        curPopulation = InitializePopulation(PARAMETERS["num_of_populations"])
        bestList = []

        for iteration in range(PARAMETERS["iterations"]):
            print("in iteration: ", iteration + 1)

            for i in curPopulation:
                i.np = 0
                i.sp = []
                i.rank = -1            
            
            newPopulation = []

            while len(newPopulation) < PARAMETERS["num_of_populations"]:
                epsilon = random.random()
                [parent1, parent2] = random.sample(curPopulation, 2)
                child = copy.deepcopy(parent1)

                if epsilon <= PARAMETERS["crossover_probability"]: 
                    child.crossover(parent2)

                newPopulation.append(child)
            
            for pop in newPopulation:
                if random.random() <= PARAMETERS["mutation_probability"]:
                    pop.mutation()
                pop.evaluate()
            
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
                # if iteration % 1 == 0:
                #     xData = [x.lineNum for x in nowBestFront[0]]
                #     yData = [y.value for y in nowBestFront[0]]
                #     plt.scatter(xData, yData)
                #     plt.show()
            
            curPopulation = nextPopulation

        bestList.sort(key = lambda StringArtParameter: StringArtParameter.value)

        with open(f"experient_{experientTimes + 1}_result.txt", "w+") as f:
            for i in bestList:
                f.write(f"{i.pinNum} {i.lineNum} {i.lineWidth} {i.value}\n")            
    
    end = time.time()
    with open("experient_total_time.txt", "w+") as f:
        f.write(f"{end - start}")
                

if __name__ == "__main__":
    with open("config.json", "r") as f:
        PARAMETERS = json.load(f)
    global imgPath, Eva, allVisitedParameter
    imgPath = "test/Lenna.jpg"
    original_img = cv2.imread(imgPath)
    original_img = cv2.cvtColor(original_img, cv2.COLOR_BGR2GRAY)
    Eva = Evaluate(original_img)
    allVisitedParameter = {}
    main()