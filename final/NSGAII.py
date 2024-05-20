import numpy as np
import random
import copy
import json
import time
import cv2
import matplotlib.pyplot as plt
from Evaluate import Evaluate
from Draw import StringArtDrawer
PARAMETERS = {}

class StringArt():    
    def __init__(self, init_set):
        
        # parameters for nsga-ii
        self.np = 0
        self.sp = []
        self.rank = -1
        self.crowdDis = 0.0

        if init_set != None:
            self.lineSet = init_set
            self.lineNum = len(self.lineSet)                  
        else:
            self.lineSet = set()
            self.lineNum = random.randint(PARAMETERS["init_line_min_num"], PARAMETERS["init_line_max_num"])
            for i in range(self.lineNum):
                while True:
                    a = random.randint(0, PARAMETERS["num_nails"] - 2)
                    b = random.randint(a + 1, PARAMETERS["num_nails"] - 1)
                    if((a, b) not in self.lineSet):
                        self.lineSet.add((a, b))
                        break
            
        self.evaluate()

    def evaluate(self):
        self.value = Eva(self.lineSet)

    def AddLine(self):
        while True:
            a = random.randint(0, PARAMETERS["num_nails"] - 2)
            b = random.randint(a + 1, PARAMETERS["num_nails"] - 1)
            if((a, b) not in self.lineSet):
                self.lineSet.add((a, b))
                break
        
    def ChangeLine(self, line):
        while True:
            if random.random() <= 0.5:
                ori_nail = line[0]
            else:
                ori_nail = line[1]

            new_nail = random.randint(0, PARAMETERS["num_nails"] - 1)
            if((ori_nail,new_nail) not in self.lineSet):
                self.lineSet.add((ori_nail,new_nail))
                break


    def mutation(self):
        decide = random.random()
        # add 10% lines
        if decide < 1.0 / 3.0:
            if self.lineNum * 1.1 > PARAMETERS["line_max_num"]:
                decide += 1.0 / 3.0
            else:
                addNumber = max(int(self.lineNum * 0.1), 1)
                for i in range(addNumber):
                    self.AddLine()
                self.lineNum += addNumber
        # remove 10% lines
        if decide < 2.0 / 3.0 and self.lineNum > 1:
            if self.lineNum * 0.9 < PARAMETERS["line_min_num"]:
                decide += 1.0 / 3.0
            else:
                deleteNumber = max(int(self.lineNum * 0.1), 1)
                for i in range(deleteNumber):
                    self.lineSet.remove(random.choice(list(self.lineSet)))
                self.lineNum -= deleteNumber
        #change 10% lines
        if decide >= 2.0 / 3.0:
            changeNumber = max(int(self.lineNum * 0.1), 1)
            for i in range(changeNumber):
                self.ChangeLine(random.choice(list(self.lineSet)))

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
        if front[frontLength - 1].value - front[0].value != 0:
            front[i].crowdDis += float(front[i + 1].value - front[i - 1].value) / (front[frontLength - 1].value - front[0].value) # 如果 decode 還沒寫好，這裡的分母記得+1才可以跑，不然會是0
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

def InitializePopulation(populationSize:int, initMethod:str, drawer: StringArtDrawer) -> list:

    if initMethod == "random":
        init_population = []
        for i in range(populationSize):
            newStringArt = StringArt(None)
            init_population.append(newStringArt)
        return init_population
    elif initMethod == "weights_nails":
        init_population = []
        for i in range(populationSize):
            # get nails
            nails = drawer.nails
            # get the value of each pixel 
            nail_value =  [nail[2] for nail in nails]
            weights = [max(255-x, 1) for x in nail_value]
            # calculate sum
            max_weight = sum(weights)
            # normalize weight of each nails
            normalized_weights = [weight / max_weight for weight in weights]
            # select the num of line 
            random_length = random.randint(PARAMETERS["init_line_min_num"], PARAMETERS["init_line_max_num"])
            # random choice n group of nail become line
            chromosome = set()
            for i in range(random_length):
                while True:
                    nail1, nail2 = random.choices(nails, weights=normalized_weights, k=2)
                    insert = (nails.index(nail1), nails.index(nail2))
                    if insert not in chromosome:
                        chromosome.add(insert)
                        break

            init_population.append(StringArt(chromosome))
        return init_population
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
    drawer = StringArtDrawer(original_img)
    


    for experientTimes in range(1):

        start = time.time()
        curPopulation = InitializePopulation(PARAMETERS["num_of_populations"], PARAMETERS["init_method"], drawer)
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

                child1.evaluate()
                child2.evaluate()
                newPopulation.append(child1)
                newPopulation.append(child2)
            
            for pop in newPopulation:
                if random.random() <= PARAMETERS["mutation_probability"]:
                    pop.mutation()
            
            curPopulation.extend(newPopulation)
            
            front = nonDominatedSorting(curPopulation)

            nextPopulation = selection(PARAMETERS["num_of_populations"], front)

            if iteration % 10 == 0:
                for i in front[0]:
                    
                    drawer.Decode(i.lineSet)
                    image = drawer.draw_image
                    cv2.putText(image, f"{iteration}\n{i.lineNum}\n{i.value}", 
                                org=(20, 80), fontFace=cv2.FONT_HERSHEY_SIMPLEX, 
                                fontScale=1, color=(0, 0, 255), thickness=2, lineType=cv2.LINE_AA)
                    cv2.imshow("show", image)
                    cv2.waitKey(1)            

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
                # if iteration % 10 == 0:
                #     xData = [x.lineNum for x in nowBestFront[0]]
                #     yData = [y.value for y in nowBestFront[0]]
                #     plt.scatter(xData, yData)
                #     plt.show()
            
            curPopulation = nextPopulation

        end = time.time()

        print("experient time: ", end-start)
        bestList.sort(key = lambda StringArt: StringArt.lineNum)
        for i in bestList:
            print(i.lineNum, i.value)
                

if __name__ == "__main__":
    with open("config.json", "r") as f:
        PARAMETERS = json.load(f)
    original_img = cv2.imread("test/star.png")
    original_img = cv2.cvtColor(original_img, cv2.COLOR_BGR2GRAY)
    global Eva
    Eva = Evaluate(original_img)
    main()