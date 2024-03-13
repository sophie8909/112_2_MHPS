#include "FactorySimulator.h"
#include <iostream>
#include <fstream>
#include <string>
#include <vector>
#include <random>
#include <ctime>
#include <cmath>

using namespace std;

void initSimulator(FactorySimulator simulator, const string fileName)
{
    ifstream inFile(fileName);
    int numJobs, numMachines;
    if (!inFile)
    {
        cerr << "Unable to open input file: " << fileName << endl;
        return; // Exit if file not found
    }

    string str;
    inFile >> numJobs >> numMachines >> str;
    vector<vector<int>> processingTimes(numMachines, vector<int>(numJobs));
    for (int i = 0; i < numMachines; i++)
    {
        for (int j = 0; j < numJobs; j++)
        {
            inFile >> processingTimes[i][j];
        }
    }
    inFile.close();

    simulator = FactorySimulator(numMachines, processingTimes);
}

int main()
{
    FactorySimulator simulator;

    // variables
    string inputFile = "data/tai20_5_1.txt";
    int maxIter = 10000;
    int coolIter = 100;
    int temp = 500;
    double coolRate = 0.9;

    for (int iter = 0; iter < maxIter; ++iter)
    {
    }

    initSimulator(simulator, inputFile);
}