import cv2
import numpy as np
from Draw import StringArtDrawer 
import GA
from Evaluate import Evaluate 

def generateInitPopulation(drawer):
    nails = drawer.nails
    sortedNails = sorted(nails, key=lambda x: x[2])
    print(sortedNails)
    print(drawer.nails)

def initPopulation(populationSize, drawer):
    population = []
    for i in range(populationSize):
        chromosome = generateInitPopulation(drawer)
        population.append(chromosome)
    return population

if __name__ == "__main__":
    # Load photo
    photo = cv2.imread("test/photo.png")
    print(1)
    # Convert to grayscale
    gray = cv2.cvtColor(photo, cv2.COLOR_BGR2GRAY)
    # Save the grayscale photo
    cv2.imwrite("test/gray.png", gray)
    print(2)


    drawer = StringArtDrawer(gray)
    drawer.initialize_nails()
    
    # GA for generating the string art

    # Draw the string art result

    # Show the result
    
    # Save the result

   