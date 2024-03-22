#ifndef FACTORY_SIMULATOR_H
#define FACTORY_SIMULATOR_H
#include <string>

class FactorySimulator
{
public:
    FactorySimulator() = default;
    FactorySimulator(int machines, int jobs, const std::vector<std::vector<int>>& times): nums_machines(machines), nums_jobs(jobs), processingTimes(times) {};
    FactorySimulator(std::string fileName);
    int calculateMakespan(const std::vector<int>& jobSequence);

    void getAllNeighbor(std::vector<int>current_solution, std::vector<std::vector<int>>& neighbors);
    int iterativeimprovement(std::vector<int>current_solution);
    std::vector<int> generate_random_solution(int nums_jobs);

private:
    int nums_machines;
    int nums_jobs;
    std::vector<std::vector<int>> processingTimes; // Job processing times on each machine
};

#endif // FACTORY_SIMULATOR_H

