#include <iostream>
#include <fstream>
#include <string>
#include <vector>
#include <random>
#include <ctime>
#include <cmath>
#include "FactorySimulator.h"

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

    srand((unsigned)time(NULL));

    // variables
    std::vector<std::string> fileNames = {"tai20_5_1.txt", "tai20_10_1.txt", "tai20_20_1.txt", "tai50_5_1.txt", "tai50_10_1.txt", "tai50_20_1.txt", "tai100_5_1.txt", "tai100_10_1.txt", "tai100_20_1.txt"};
    for (auto fileName : fileNames)
    {
        string inputFile = "data/" + fileName;
        string outputFolder = "result/" + fileName;
        int maxIter = 10000;
        int coolIter = 165;
        int jobNum;
        int machineNum;
        double temp = 1000.0;
        double minTemp = 3.0;
        double coolRate = 0.9;

        initSimulator(inputFile, simulator, jobNum, machineNum);

        int sum = 0, average = 0;
        int minSpan = 2147483647;
        int maxSpan = 0;
        double totalTime = 0.0;

        ofstream outFile;
        string outputFileName;

        for (int i = 0; i < 20; ++i)
        {
            double START, END;
            START = clock();
            int curTemp = temp;

            vector<int> curSolution = getInitSolution(jobNum);
            int curMakespan = simulator.calculateMakespan(curSolution);
            int bestMakespan = curMakespan;

            outputFileName = outputFolder + to_string(i) + ".txt";
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

                if (neighborhoodMakespan < bestMakespan)
                {
                    bestMakespan = neighborhoodMakespan;
                }

                // check if is better
                if (neighborhoodMakespan <= curMakespan)
                {
                    curSolution = neighborhood;
                    curMakespan = neighborhoodMakespan;
                }
                // else sa
                else
                {
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

            END = clock();
            totalTime += (END - START);

            // printVector(curSolution);
            sum += bestMakespan;
            if (minSpan > bestMakespan)
            {
                minSpan = bestMakespan;
            }
            if (maxSpan < bestMakespan)
            {
                maxSpan = bestMakespan;
            }
        }

        cout << "average running time: " << totalTime / 20.0 / CLOCKS_PER_SEC << "s" << endl;

        average = sum / 20;

        outputFileName = outputFolder + "all.txt";
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

        cout << "avg: " << average << " min: " << minSpan << " max: " << maxSpan << endl;
    }
}