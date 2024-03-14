#ifndef FACTORY_SIMULATOR_H
#define FACTORY_SIMULATOR_H

#include <vector>

class FactorySimulator
{
public:
    FactorySimulator() = default;
    FactorySimulator(int machines, const std::vector<std::vector<int>> &times)
        : numMachines(machines), processingTimes(times) {}
    int calculateMakespan(const std::vector<int> &jobSequence);

private:
    int numMachines;
    std::vector<std::vector<int>> processingTimes; // Job processing times on each machine
};

#endif // FACTORY_SIMULATOR_H
