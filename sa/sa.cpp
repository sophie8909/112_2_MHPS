#include "FactorySimulator.h"
#include <iostream>
#include <fstream>
#include <string>
#include <vector>
#include <random>
#include <ctime>
#include <cmath>

using namespace std;

void initSimulator(FactorySimulator simulator, const string fileName, int *jobNum, int *machineNum)
{
    ifstream inFile(fileName);
    if (!inFile)
    {
        cerr << "Unable to open input file: " << fileName << endl;
        return; // Exit if file not found
    }

    string str;
    inFile >> *jobNum >> *machineNum >> str;
    vector<vector<int>> processingTimes(*machineNum, vector<int>(*jobNum));
    for (int i = 0; i < *machineNum; i++)
    {
        for (int j = 0; j < *jobNum; j++)
        {
            inFile >> processingTimes[i][j];
        }
    }
    inFile.close();

    simulator = FactorySimulator(*machineNum, processingTimes);
}

vector<int> getInitSolution(int jobNum)
{
    vector<int> solution;

    for (int i = 0; i < jobNum; ++i)
    {
        solution.push_back(i);
    }

    for (int i = 0; i < 1000; ++i)
    {
        int a, b, tmp;
        a = rand() % jobNum;
        b = rand() % jobNum;
        while (a == b)
        {
            b = rand() % jobNum;
        }

        tmp = solution[a];
        solution[a] = solution[b];
        solution[b] = tmp;
    }

    return solution;
}

int main()
{
    FactorySimulator simulator;

    // variables
    string inputFile = "data/tai20_5_1.txt";
    string outputFile = "result/20_5/";
    int maxIter = 10000;
    int coolIter = 100;
    int temp = 500;
    int jobNum;
    int machineNum;
    double coolRate = 0.9;

    initSimulator(simulator, inputFile, &jobNum, &machineNum);

    int sum = 0;
    int minSpan = 2147483647;
    int maxSpan = 0;

    for (int i = 0; i < 20; ++i)
    {
        srand((unsigned)time(NULL));

        vector<int> solution = getInitSolution(jobNum);
        int makespan = simulator.calculateMakespan(solution);

        ofstream outFile(outputFile + to_string(i) + ".txt");

        for (int iter = 0; iter < maxIter; ++iter)
        {
        }
    }
}