#include <algorithm>
#include <vector>
#include "FactorySimulator.h"

int FactorySimulator::calculateMakespan(const std::vector<int> &jobSequence)
{
    std::vector<int> machineEndTime(numMachines, 0);    // Tracks the end time for each machine
    std::vector<int> jobEndTime(jobSequence.size(), 0); // Tracks the end time for each job

    for (int jobId : jobSequence)
    {
        int lastEndTime = 0;
        int startTime = 0;
        int endTime = 0;
        for (int machineId = 0; machineId < numMachines; ++machineId)
        {
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

    // The makespan is the end time of the last job
    return jobEndTime[jobSequence[jobSequence.size() - 1]];
}