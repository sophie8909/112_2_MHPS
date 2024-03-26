#ifndef TABU_SEARCH_H
#define TABU_SEARCH_H

#include <list>
#include <vector>
#include "FactorySimulator.h"
#include <string>

struct TabuItem{
    std::vector<int> order;
    int tabuTenure;

    TabuItem(const std::vector<int>& o, int tenure) : order(o), tabuTenure(tenure){}
};


class TabuSearch
{
public:
    bool isorderinTabu(const std::vector<int>& order);
    void setIterations(int iters);
    void setNeighborhoodSize(int size);
    void Setnumjobsize(int size);
    void swap(int jobIndex1,int jobIndex2,std::vector<int>& order);
    void permutationTS(std::vector<int>& tabuorder);
    void runTabuSearch();
    void updateTabuList();
    void exportMakespansHistoryToFile(const std::string& filePath) const;
    void setProcessingTimes(const std::vector<std::vector<int>>& times);
    TabuSearch(FactorySimulator* sim) : simulator(sim), iteration(10), neighborhood(5){
        maxTabuTenure = 5;
    };

private:
    std::list<TabuItem> tabuList;
    std::vector<int> makespansHistory; 
    std::vector<std::vector<int>> processingTimes;
    int maxTabuTenure;
    std::vector<int> joborder;
    int iteration; 
    int tabulist;
    int neighborhood;
    int changetenureflag;
    FactorySimulator* simulator;
};




#endif //TABU_SEARCH_H
