#include <iostream>
#include <fstream>
#include <vector>
#include <string>
#include "FactorySimulator.h"

void initializeSimulator(std::string fileName, FactorySimulator& simulator, int& numJobs, int& numMachines) {
    std::ifstream inFile("data/" + fileName);
    if (!inFile) {
        std::cerr << "Unable to open input file" << std::endl;
        return; // Exit if file not found
    }
    std::string str;
    inFile >> numJobs >> numMachines >> str;  
    std::vector<std::vector<int>> processingTimes(numMachines, std::vector<int>(numJobs));
    for (int i = 0; i < numMachines; i++) {
        for (int j = 0; j < numJobs; j++) {
            inFile >> processingTimes[i][j];
        }
    }
    inFile.close();

    simulator = FactorySimulator(numMachines, processingTimes);
}

int main() {
    std::vector<std::string> fileNames = {"tai20_5_1.txt", "tai20_10_1.txt", "tai20_20_1.txt", "tai50_5_1.txt", "tai50_10_1.txt", "tai50_20_1.txt", "tai100_5_1.txt", "tai100_10_1.txt", "tai100_20_1.txt"};
    int numJobs;
    int numMachines;
    FactorySimulator simulator;
    
    for (auto fileName : fileNames) {
        initializeSimulator(fileName, simulator, numJobs, numMachines);

        std::vector<int> jobSequence(numJobs);
        

        for (int i = 0; i < numJobs; i++) {
            jobSequence[i] = i;
        }
        std::cout << "Makespan: " << simulator.calculateMakespan(jobSequence) << std::endl;

    }

    return 0;
}