#include <algorithm>
#include <vector>
#include "FactorySimulator.h"

FactorySimulator::FactorySimulator(std::string fileName) {
    int numJobs;
    int numMachines;

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

int FactorySimulator::calculateMakespan(const std::vector<int>& jobSequence)

    std::vector<int> machineEndTime(numMachines, 0); // Tracks the end time for each machine
    std::vector<int> jobEndTime(jobSequence.size(), 0); // Tracks the end time for each job

    for (int jobId : jobSequence) {
        int lastEndTime = 0;
        int startTime = 0;
        int endTime = 0;
        for (int machineId = 0; machineId < numMachines; ++machineId) {
            // The start time for the current machine is the maximum of the end time of the last machine and the end time of the last job
            lastEndTime = endTime;
            startTime = std::max(lastEndTime, machineEndTime[machineId]);
            // The end time for the current machine is the start time plus the processing time
            endTime = startTime + processingTimes[machineId][jobId];
            // Update the end time for the current machine
            machineEndTime[machineId] = endTime;
        }
        // Update the end time for the current job
        jobEndTime[jobId] = endTime;
    }

    // The makespan is the end time of the last job in jobSequence
    int lastJobID = jobSequence[jobSequence.size() - 1];
    return jobEndTime[lastJobID];
}

void JobSequence::getAllNeighborJobSequences(std::vector<jobSequence>& neighbors) {
    neighbours.clear();
    for (int i = 0; i < numJobs; i++) {
        for (int j = i + 1; j < numJobs; j++) {
            jobSequence neighbour = *this;
            std::swap(neighbour.jobSequence[i], neighbour.jobSequence[j]);
            neighbors.push_back(neighbour);
        }
    }
}