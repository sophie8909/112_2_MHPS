#include "TabuSearch.h"
#include "FactorySimulator.h"
#include <algorithm>
#include <cmath>
#include <fstream>
#include <random>
#include <chrono>
#include <iostream>
#include <climits>
FactorySimulator simulator;


bool TabuSearch::isorderinTabu(const std::vector<int>& order){
    for (const auto& item: tabuList){
        if(item.order == order){
            return true;
        }
    }
    return false;
}

void TabuSearch::updateTabuList(){
    for(auto it = tabuList.begin(); it != tabuList.end();){
        --(it->tabuTenure);
        if(it->tabuTenure == 0){
            it = tabuList.erase(it);
        }else{
            ++it;
        }
    }
}
void TabuSearch::setIterations(int iters){
    iteration = iters;
}
void TabuSearch::setNeighborhoodSize(int size){
    neighborhood = size ;
}
void TabuSearch::runTabuSearch(){
    std::vector<int> currentOrder = joborder;
    int GlobalbestMakespan = INT_MAX;
      
    std::vector<int> bestOrder = joborder;
    for( int i = 0; i < iteration ; ++i){
        int LocalbestMakespan = INT_MAX;  
        for(int j = 0; j < neighborhood ; ++j){
            bool tabu;
            do{
                tabu = false;
                permutationTS(currentOrder);

                if(isorderinTabu(currentOrder)){
                    tabu = true;
                }else{
                    int currentMakespan =  simulator->calculateMakespan(currentOrder);
                    //std::cout <<currentMakespan<<std::endl; //"-->CURRENTMakespan_Tabu:"
                    
                    if(currentMakespan < LocalbestMakespan){
                        LocalbestMakespan = currentMakespan;
                        bestOrder = currentOrder;
                    }              
                }
            }while (tabu);
            tabuList.push_back(TabuItem(currentOrder,maxTabuTenure));
            updateTabuList();
        }
        currentOrder = bestOrder;
        
        makespansHistory.push_back(LocalbestMakespan); 
        if(LocalbestMakespan < GlobalbestMakespan){
            GlobalbestMakespan = LocalbestMakespan;
            changetenureflag = 0;
        }else{
            changetenureflag +=1;
        }
        if(changetenureflag >= 50){
            maxTabuTenure = 10;
        }else{
            maxTabuTenure = 5;
        }

    }
/*    for (int x = 0; x < 20; x++) {
       std::cout << bestOrder[x] << " ";
    }*/
    std::cout <<std::endl<< "BestMakespan_Tabu:"<<GlobalbestMakespan<<std::endl;
   
}
void TabuSearch::permutationTS(std::vector<int>& tabuorder){
    unsigned seed = std :: chrono::system_clock::now().time_since_epoch().count();
    std::default_random_engine generator(seed);
    std::uniform_int_distribution<int> distribution(0, joborder.size() - 1);

    int jobIndex1 = distribution(generator);
    int jobIndex2 = distribution(generator);
    while(jobIndex1 == jobIndex2  ){
        
        jobIndex2 = distribution(generator);
    }
    while(jobIndex1 < jobIndex2 || processingTimes[0][tabuorder[jobIndex1]] >= processingTimes[0][tabuorder[jobIndex2]]){
        if(processingTimes[0][tabuorder[jobIndex1]] >= processingTimes[0][tabuorder[jobIndex2]])
            break;
        jobIndex1 = distribution(generator);
        jobIndex2 = distribution(generator);
    }
    

    swap(jobIndex1, jobIndex2, tabuorder);
}

void TabuSearch::swap(int jobIndex1, int jobIndex2,std::vector<int>& order){
    std::swap(order[jobIndex1], order[jobIndex2]);
}

void TabuSearch::Setnumjobsize(int size){
    joborder.resize(size);
    for (int i = 0; i < size; ++i) {
        joborder[i] = i;
    }
    unsigned seed = std::chrono::system_clock::now().time_since_epoch().count();
    std::default_random_engine engine(seed);

    std::shuffle(joborder.begin(),joborder.end(),engine);
}
void TabuSearch::exportMakespansHistoryToFile(const std::string& filePath) const {
    std::ofstream outFile(filePath);

    if (outFile.is_open()) {
        for (const auto& makespan : makespansHistory) {
            outFile << makespan << "\n"; // 每个makespan后换行
        }
        outFile.close();
    } else {
        std::cerr << "Unable to open file: " << filePath << std::endl;
    }
}
void TabuSearch::setProcessingTimes(const std::vector<std::vector<int>>& times) {
    processingTimes = times;
}
