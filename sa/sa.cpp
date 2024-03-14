#include "FactorySimulator.h"
#include <iostream>
#include <fstream>
#include <string>
#include <vector>
#include <random>
#include <ctime>
#include <cmath>

using namespace std;

void initSimulator(const string fileName, FactorySimulator &simulator, int &jobNum, int &machineNum)
{
    ifstream inFile(fileName);
    if (!inFile)
    {
        cerr << "Unable to open input file: " << fileName << endl;
        return; // Exit if file not found
    }

    string str;
    inFile >> jobNum >> machineNum >> str;
    vector<vector<int>> processingTimes(machineNum, vector<int>(jobNum));
    for (int i = 0; i < machineNum; i++)
    {
        for (int j = 0; j < jobNum; j++)
        {
            inFile >> processingTimes[i][j];
        }
    }
    inFile.close();

    simulator = FactorySimulator(machineNum, processingTimes);
}

vector<int> getNeighborhood(vector<int> curSol, const int jobNum)
{
    int a, b, tmp;
    vector<int> ret = curSol;
    a = rand() % jobNum;
    b = rand() % jobNum;
    while (a == b)
    {
        b = rand() % jobNum;
    }

    tmp = ret[a];
    ret[a] = ret[b];
    ret[b] = tmp;

    return ret;
}

vector<int> getInitSolution(int jobNum)
{
    vector<int> solution(jobNum);

    for (int i = 0; i < jobNum; ++i)
    {
        solution[i] = i;
    }

    for (int i = 0; i < 1000; ++i)
    {
        solution = getNeighborhood(solution, jobNum);
    }

    return solution;
}

void printVector(vector<int> vec)
{
    for (int i = 0; i < vec.size(); ++i)
    {
        cout << vec[i] << " ";
    }
    cout << endl;
}

int main()
{
    FactorySimulator simulator;

    // variables
    string inputFile = "data/tai20_5_1.txt";
    string outputFolder = "result/20_5/";
    int maxIter = 10000;
    int coolIter = 200;
    int temp = 500;
    int minTemp = 5;
    int jobNum;
    int machineNum;
    double coolRate = 0.9;

    initSimulator(inputFile, simulator, jobNum, machineNum);

    int sum = 0, average = 0;
    int minSpan = 2147483647;
    int maxSpan = 0;

    ofstream outFile;
    string outputFileName;

    for (int i = 0; i < 20; ++i)
    {
        int curTemp = temp;
        srand(time(NULL));

        vector<int> curSolution = getInitSolution(jobNum);
        int curMakespan = simulator.calculateMakespan(curSolution);

        outputFileName = outputFolder + to_string(temp) + "_0." + to_string((int)(coolRate * 100)) + "_" + to_string(i) + ".txt";
        outFile.open(outputFileName);
        if (!outFile.is_open())
        {
            cerr << "Unable to open input file: " << outputFileName << endl;
            return 0; // Exit if file not found
        }

        outFile << curMakespan << endl;

        for (int iter = 0; iter < maxIter; ++iter)
        {
            // generate a nrighborhood
            vector<int> neighborhood = getNeighborhood(curSolution, jobNum);
            int neighborhoodMakespan = simulator.calculateMakespan(neighborhood);

            // check if is better
            if (neighborhoodMakespan <= curMakespan)
            {
                curSolution = neighborhood;
                curMakespan = neighborhoodMakespan;
            }
            // else sa
            else
            {
                srand(time(NULL));
                double r = (double)rand() / RAND_MAX;
                double accept = exp((double)(curMakespan - neighborhoodMakespan) / curTemp);
                if (accept > r)
                {
                    curSolution = neighborhood;
                    curMakespan = neighborhoodMakespan;
                }
            }

            // cooling
            if (iter && iter % coolIter == 0)
            {
                curTemp *= coolRate;
                if (minTemp > curTemp)
                {
                    curTemp = minTemp;
                }
            }

            outFile << curMakespan << endl;
        }
        outFile.close();

        printVector(curSolution);
        sum += curMakespan;
        if (minSpan > curMakespan)
        {
            minSpan = curMakespan;
        }
        if (maxSpan < curMakespan)
        {
            maxSpan = curMakespan;
        }
    }

    average = sum / 20;

    outputFileName = outputFolder + to_string(temp) + "_0." + to_string((int)(coolRate * 100)) + "_all.txt";
    outFile.open(outputFileName);
    if (!outFile.is_open())
    {
        cerr << "Unable to open input file: " << outputFileName << endl;
        return 0; // Exit if file not found
    }

    outFile << minSpan << endl;
    outFile << maxSpan << endl;
    outFile << average << endl;

    outFile.close();
}