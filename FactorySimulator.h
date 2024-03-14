#ifndef FACTORY_SIMULATOR_H
#define FACTORY_SIMULATOR_H


class FactorySimulator
{
public:
    FactorySimulator() = default;
    FactorySimulator(int machines, const std::vector<std::vector<int>>& times) 
        : numMachines(machines), processingTimes(times) {}
    FactorySimulator(std::string fileName);
    int calculateMakespan(const std::vector<int>& jobSequence);

private:
    int numMachines;
    std::vector<std::vector<int>> processingTimes; // Job processing times on each machine
};

class JobSequence
{
public:
    JobSequence() = default;
    JobSequence(int jobs) : numJobs(jobs) {
        jobSequence.resize(numJobs);
        for (int i = 0; i < numJobs; i++) {
            jobSequence[i] = i;
        }
    }
    int getNumJobs() const { return numJobs; }
    std::vector<int> getJobSequence() const { return jobSequence; }
    void setJobSequence(const std::vector<int>& sequence) { jobSequence = sequence; }
    void getAllNeighborJobSequences(std::vector<jobSequence>& neighbors);
private:
    int numJobs;
    std::vector<int> jobSequence;
};
}

#endif // FACTORY_SIMULATOR_H
