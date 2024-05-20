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
        self.lineNum = len(self.lineSet)
        
    def ChangeLine(self, line):
        while True:
            if random.random() <= 0.5:
                ori_nail = line[0]
            else:
                ori_nail = line[1]

            new_nail = random.randint(0, PARAMETERS["num_nails"] - 1)
            if(ori_nail != new_nail and (ori_nail,new_nail) not in self.lineSet):
                self.lineSet.add((ori_nail,new_nail))
                break
        self.lineNum = len(self.lineSet)


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
        # remove 10% lines
        if decide < 2.0 / 3.0 and self.lineNum > 1:
            if self.lineNum * 0.9 < PARAMETERS["line_min_num"]:
                decide += 1.0 / 3.0
            else:
                deleteNumber = max(int(self.lineNum * 0.1), 1)
                for i in range(deleteNumber):
                    self.lineSet.remove(random.choice(list(self.lineSet)))
                self.lineNum = len(self.lineSet)
        #change 10% lines
        if decide >= 2.0 / 3.0:
            changeNumber = max(int(self.lineNum * 0.1), 1)
            for i in range(changeNumber):
                self.ChangeLine(random.choice(list(self.lineSet)))

def selection(populationSize:int, curPopulation:list) -> list:
    curPopulation.sort(key = lambda StringArt: StringArt.value)
    newPopulation = []
    seenSets = set()
    for pop in curPopulation:
        setTuple = tuple(sorted(pop.lineSet))
        if setTuple not in seenSets:
            newPopulation.append(pop)
            seenSets.add(setTuple)
    
    need = populationSize - len(newPopulation)

    for i in range(need):
        add = copy.deepcopy(random.choice(curPopulation))
        newPopulation.append(add)
    
    newPopulation = newPopulation[:populationSize]

    return newPopulation

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
            
            nextPopulation = selection(PARAMETERS["num_of_populations"], curPopulation)

            if iteration % 50 == 0:
                for j in range(PARAMETERS["num_of_populations"]):
                    i = 99-j
                    drawer.Decode(nextPopulation[i].lineSet)
                    image = drawer.draw_image
                    cv2.putText(image, f"{iteration}|{nextPopulation[i].lineNum}|{nextPopulation[i].value}", (20, 60), cv2.FONT_HERSHEY_SIMPLEX,  1, (0, 5, 255), 2, cv2.LINE_AA)
                    cv2.imshow("show", image)
                    cv2.waitKey(1)            

            if iteration == 0:
                bestList = copy.deepcopy(nextPopulation)
            else:
                totalList = copy.deepcopy(nextPopulation) + copy.deepcopy(bestList)
                totalList.sort(key = lambda StringArt: StringArt.value)
                bestList = totalList[:PARAMETERS["num_of_populations"]]
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
    original_img = cv2.imread("test/one_line.png")
    original_img = cv2.cvtColor(original_img, cv2.COLOR_BGR2GRAY)
    global Eva
    Eva = Evaluate(original_img)
    main()