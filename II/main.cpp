#include <iostream>
#include <random>
#include <algorithm>
#include "FactorySimulator.h"
#include <fstream>
#include <string>

void initializeSimulator(std::string fileName, FactorySimulator& simulator, int& numJobs, int& numMachines) {
    std::ifstream inFile("data/" + fileName);
    if (!inFile) {
        std::cerr << "Unable to open input file" << std::endl;
        return;
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

    simulator = FactorySimulator(numMachines, numJobs, processingTimes);
}

int main() {
    std::vector<std::string> fileNames = {"tai20_5_1.txt", "tai20_10_1.txt", "tai20_20_1.txt", "tai50_5_1.txt", "tai50_10_1.txt", "tai50_20_1.txt", "tai100_5_1.txt", "tai100_10_1.txt", "tai100_20_1.txt"};

    int nums_jobs;
    int nums_machines;
    FactorySimulator simulator;

    for (auto fileName : fileNames) {
        initializeSimulator(fileName, simulator, nums_jobs, nums_machines);
        std::cout << "測資" << nums_jobs << " " << nums_machines << std::endl;
        std::vector<int> jobSequence(nums_jobs);


        std::cout << std::endl;




        std::vector<int>initsolution = simulator.generate_random_solution(nums_jobs); //對每個測資只生成一次初始解

        int result = simulator.iterativeimprovement(initsolution);
        std::cout << "makespan:" << result << std::endl;
        std::cout << std::endl;

    }

    return 0;
}
