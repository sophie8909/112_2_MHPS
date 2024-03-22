#include <algorithm>
#include <vector>
#include "FactorySimulator.h"
#include <fstream>
#include <iostream>
#include <random>
#include <ctime>

FactorySimulator::FactorySimulator(std::string fileName) {
    int nums_jobs;
    int nums_machines;

    std::ifstream inFile("data/" + fileName);
    if (!inFile) {
        std::cerr << "Unable to open input file" << std::endl;
        return; // Exit if file not found
    }
    std::string str;
    inFile >> nums_machines >> nums_jobs >> str;
    std::vector<std::vector<int>> processingTimes(nums_machines, std::vector<int>(nums_jobs));

    for (int i = 0; i < nums_machines; i++) {
        for (int j = 0; j < nums_jobs; j++) {
            inFile >> processingTimes[i][j];
        }
    }
    inFile.close();

    nums_jobs = nums_jobs;
    nums_machines = nums_machines;
    processingTimes = processingTimes;
}

int FactorySimulator::calculateMakespan(const std::vector<int>& jobSequence)
{
    std::vector<int> machineEndTime(nums_machines, 0); // Tracks the end time for each machine
    std::vector<int> jobEndTime(nums_jobs, 0); // Tracks the end time for each job

    for (int jobId : jobSequence) { //1~20
        //std::cout << "jobId" << jobId << std::endl;
        int lastEndTime = 0;
        int startTime = 0;
        int endTime = 0;
        for (int machineId = 0; machineId < nums_machines; ++machineId) {
            // The start time for the current machine is the maximum of the end time of the last machine and the end time of the last job
            lastEndTime = endTime;

            startTime = std::max(lastEndTime, machineEndTime[machineId]);
            // The end time for the current machine is the start time plus the processing time
            endTime = startTime + processingTimes[machineId][jobId-1];
            // Update the end time for the current machine
            machineEndTime[machineId] = endTime;
        }

        jobEndTime[jobId-1] = endTime;
    }

    // The makespan is the end time of the last job in jobSequence
    int lastJobID = jobSequence[jobSequence.size() - 1];

    return jobEndTime[lastJobID-1];
}


int FactorySimulator::iterativeimprovement(std::vector<int> current_solution) {
    std::vector<int>final_solution = current_solution;

    int final_makespan = calculateMakespan(current_solution);

    std::vector<std::vector<int>>neighbors; //用來存所有neighbor

    bool improved = true;
    int neighbor_makespan;
    int g = 1;

    while (improved && g <= 10000) {
        getAllNeighbor(final_solution, neighbors);
        improved = false;
        for (std::vector<int>neigh : neighbors){
            neighbor_makespan = calculateMakespan(neigh);

            if (neighbor_makespan < final_makespan){
                improved = true;
                current_solution = neigh;
                final_solution = neigh;
                final_makespan = neighbor_makespan;
            }
        }
        g++;
    }

    std::cout << "停止代數" << g << std::endl;
    return final_makespan;
}


std::vector<int> FactorySimulator::generate_random_solution(int nums_jobs) {
    std::vector<int> solution(nums_jobs);

    std::srand(std::time(nullptr));
    bool used[nums_jobs+1] = {false};
    int randomNumber;

    for (int i = 0; i < nums_jobs; ++i){
        do {
            randomNumber = std::rand() % nums_jobs+1;
        } while (used[randomNumber]);

        solution[i] = randomNumber;
        used[randomNumber] = true;
    }



    return solution;
}

void FactorySimulator::getAllNeighbor(std::vector<int>current_solution, std::vector<std::vector<int>>& neighbors) { //得到目前解的所有neighbor
    neighbors.clear();
    std::vector<int>neighbor;

    for (int i = 0; i < nums_jobs; i++) {
        for (int j = i + 1; j < nums_jobs; j++) {
            neighbor = current_solution;

            std::swap(neighbor[i], neighbor[j]);

            neighbors.push_back(neighbor);
        }
    }
}


