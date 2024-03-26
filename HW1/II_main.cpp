#include <iostream>
#include <random>
#include <algorithm>
#include "FactorySimulator.h"
#include <fstream>
#include <string>
#include "time.h"
#include <chrono>
#include <windows.h>

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
    std::vector<std::string> fileNames = {"tai100_20_1.txt"};


    int nums_jobs;
    int nums_machines;
    FactorySimulator simulator;

    float time_record = 0;

    for (int i = 0; i < 20; i++){
        auto start = std::chrono::high_resolution_clock::now();

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
        auto end = std::chrono::high_resolution_clock::now();
        std::chrono::duration<double> elapsed_seconds = end - start;

        time_record += elapsed_seconds.count();
        Sleep(1000);
    }

    std::cout << "平均" << time_record/20 << "秒" << std::endl;

    return 0;
}
