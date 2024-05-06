import numpy as np
import random
import copy
import json
import time
import cv2
from Evaluate import Evaluate
PARAMETERS = {}

def nonDominatedSorting(populationSize, chromsObjRecord):
    pass

def CalculateCrowdingDistance(front, chromsObjRecord):
    pass

def selection(populationSize, front, chromsObjRecord, totalChromosome):
    pass

def initPopulation(populationSize):
    pass

def crossover(parent1, parent2, crossoverRate):
    pass

def mutation(original):
    pass


if __name__ == "__main__":
    with open("GA_config.json", "r") as f:
        PARAMETERS = json.load(f)