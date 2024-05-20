import cv2
import numpy as np
from Draw import StringArtDrawer 
import final.NSGAII as NSGAII
from Evaluate import Evaluate 

import random
def generateInitPopulation(drawer):
    nails = drawer.nails
    weights = [nail[2] for nail in nails]
    max_weight = sum(weights)
    normalized_weights = [weight / max_weight for weight in weights]
    random_length = random.randint(2000, 5000)
    chromosome = []
    for i in range(random_length):
        a, b = random.choices(nails, weights=normalized_weights, k=2)
        chromosome.append([a[0], a[1], b[0], b[1]])
    return chromosome


def initPopulation(populationSize, drawer):
    population = []
    for i in range(populationSize):
        chromosome = generateInitPopulation(drawer)
        population.append(chromosome)
    return population

if __name__ == "__main__":
    # Load photo
    photo = cv2.imread("test/hw3.jpg")
    # Convert to grayscale
    gray = cv2.cvtColor(photo, cv2.COLOR_BGR2GRAY)
    # Save the grayscale photo
    cv2.imwrite("test/gray.png", gray)


    drawer = StringArtDrawer(gray)
    
    # cv2.imshow("circle", drawer.image)
    # cv2.waitKey(0)

    drawer.initialize_nails()
    pop = initPopulation(1, drawer)
    
    with open("record.txt", "w") as f:
        f.write(str(pop))

    # GA for generating the string art

    # Draw the string art result

    # Show the result
    
    # Save the result

   