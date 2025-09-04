#include<bits/stdc++.h>
#include<chrono>
using namespace std;
using std::chrono::high_resolution_clock;
using std::chrono::duration;

//heuritstic func -> f = g + h 
// g -> depth of tree && h -> number of misplaces
int heuristic(vector<vector<int>>& currState,vector<vector<int>>& goalState){
    int h = 0;
    for(int i = 0; i < 3; i++){
        for(int j = 0; j < 3; j++){
            if(currState[i][j] != goalState[i][j]){
                h++;
            }
        }
    }
    return h;
}

pair<vector<vector<int>>,int> aStar(vector<vector<int>>& iniState,vector<vector<int>>& goalState){
    // required ds -> min-heap 
    // min-heap -> {g+h,h,g,currState}
    set<pair<pair<int,pair<int,int>>,vector<vector<int>>>> pq;
    int h = heuristic(iniState,goalState);
    pq.insert({{0+h,{h,0}},iniState});

    int dr[] = {-1,0,1,0};
    int dc[] = {0,1,0,-1};

    while(!pq.empty()){
        auto it = *(pq.begin());
        int f = it.first.first;
        int h = it.first.second.first;
        int g = it.first.second.second;
        auto currState = it.second;
        pq.erase(it);

        if(h == 0)
            return {currState,g};

        //let empty block be denoted as  -1
        for(int i = 0; i < 3; i++){
            for(int j = 0; j < 3; j++){
                if(currState[i][j] == 0){
                    for(int k = 0; k < 4; k++){
                        int nr = i + dr[k];
                        int nc = j + dc[k];

                        if( nr >= 0 && nr < 3 &&
                            nc >= 0 && nc < 3){
                                auto temp = currState;
                                temp[i][j] = currState[nr][nc];
                                temp[nr][nc] = 0;
                                int nh = heuristic(temp,goalState);
                                pq.insert({{g+1+nh,{nh,g+1}},temp});
                            }
                    }
                }
            }
        }
    }
    return {};
}



int main(){
    vector<vector<int>> iniState , goalState;
    iniState = {
    {6,4,7},
    {8,5,0},
    {3,2,1}
    };

    /* {
    {6,4,7},
    {8,5,0},
    {3,2,1}
    };

    {
    {7,8,6},
    {2,3,5},
    {1,4,0}
    };

    {
    {8,7,6},
    {2,4,5},
    {1,3,0}
    };
    
    */


    goalState = {
        {1,2,3},
        {4,5,6},
        {7,8,0}
    };


    auto start = high_resolution_clock::now();
    auto ans = aStar(iniState,goalState);
    auto stop = high_resolution_clock::now();
    auto block = ans.first;
    auto g = ans.second;
    for(int i = 0; i < 3; i++){
        for(auto it : block[i]){
            cout<<it<<" ";
        }
        cout<<endl;
    }

    cout<<endl<<"Depth : "<<g<<endl;
    std::chrono::duration<double, std::milli> duration = stop - start;
    cout << "Time taken: " << duration.count() / 1000<<" seconds"<<endl;
    return 0;
}
