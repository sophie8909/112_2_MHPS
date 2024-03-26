#include <iostream>
#include <fstream>
#include <vector>
#include <string>
#include <algorithm>
#include "FactorySimulator.h"
#include "TabuSearch.h"
#include <chrono>

void initializeSimulator(std::string fileName, FactorySimulator& simulator, int& numJobs, int& numMachines, std::vector<std::vector<int>>& processingTimes) {
    std::ifstream inFile("data/" + fileName);
    if (!inFile) {
        std::cerr << "Unable to open input file" << std::endl;
        return; // Exit if file not found
    }
    std::string str;
    inFile >> numJobs >> numMachines >> str;  
    processingTimes.resize(numMachines, std::vector<int>(numJobs));
    for (int i = 0; i < numMachines; i++) {
        for (int j = 0; j < numJobs; j++) {
            inFile >> processingTimes[i][j];

        }
    }
    inFile.close();

    simulator = FactorySimulator(numMachines, processingTimes);
}

int main() {
    

    std::vector<std::string> fileNames = { "tai50_5_1.txt","tai50_10_1.txt","tai50_20_1.txt"}; //, "tai20_10_1.txt", "tai20_20_1.txt", "tai50_5_1.txt", "tai50_10_1.txt", "tai50_20_1.txt", "tai100_5_1.txt", "tai100_10_1.txt", "tai100_20_1.txt"
    int numJobs;
    int numMachines;
    FactorySimulator simulator;
    std::vector<std::vector<int>> processingTimes; 

    
    for (auto fileName : fileNames) {
        for(int i=0 ;i<3;i++){          //number of execution
        auto start = std::chrono::high_resolution_clock::now();
        initializeSimulator(fileName, simulator, numJobs, numMachines,processingTimes);
        
        std::vector<int> jobSequence(numJobs);
        TabuSearch TS(&simulator); 
        TS.setProcessingTimes(processingTimes);
        TS.Setnumjobsize(numJobs);
        TS.setIterations(1000); //Iteration_number
        TS.setNeighborhoodSize(20); //neighborhood
        
/*        for (int i = 0; i < numJobs; i++) {
            jobSequence[i] = i;
        }*/
        TS.runTabuSearch();
        //TS.permutationTS(jobSequence);
/*        for (int i = 0; i < numJobs; i++) {
                std::cout << jobSequence[i] << " ";
            }*/
        
//        TS.exportMakespansHistoryToFile("D:/history.txt"); // makespan_log
        auto end = std::chrono::high_resolution_clock::now();
        std::chrono::duration<double> duration = end - start;
        std::cout << " Execution time: " << duration.count() << " seconds" ;
        
    }
    std::cout<<std::endl<<"-----------------";
    }
}