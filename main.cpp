#include <iostream>
#include <fstream>
#include <vector>
#include <string>
#include "FactorySimulator.h"

int main() {
    // FactorySimulator 
    // Read the data from the file
    std::ifstream inFile("data/tai20_5_1.txt");
    if (!inFile) {
        std::cerr << "Unable to open input file" << std::endl;
        return 1; // Exit if file not found
    }
    int numJobs;
    int numMachines;
    std::string str;
    inFile >> numJobs >> numMachines >> str;  
    std::vector<std::vector<int>> processingTimes(numMachines, std::vector<int>(numJobs));
    for (int i = 0; i < numMachines; i++) {
        for (int j = 0; j < numJobs; j++) {
            inFile >> processingTimes[i][j];
        }
    }
    inFile.close();

// for (int i = 0; i < numMachines; i++) {
//         for (int j = 0; j < numJobs; j++) {
//             std::cout << processingTimes[i][j] << " ";
//         }
//         std::cout << std::endl;
//     }

    // Initialize the simulator
    FactorySimulator simulator(numMachines, processingTimes);

    std::vector<int> jobSequence = {0, 1, 2, 3, 4, 5, 6, 7, 8, 9, 10, 
                                    11, 12, 13, 14, 15, 16, 17, 18, 19};
    std::cout << "Makespan: " << simulator.calculateMakespan(jobSequence) << std::endl;
    

    return 0;
}