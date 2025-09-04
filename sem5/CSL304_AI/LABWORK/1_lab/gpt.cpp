#include <bits/stdc++.h>
#include <chrono>
using namespace std;
using hr = chrono::high_resolution_clock;

// helpers: serialize 2D -> string and back
string serialize2D(const vector<vector<int>>& b){
    string s; s.reserve(9);
    for(auto &r : b) for(int x : r) s.push_back(char('0' + x));
    return s;
}
vector<vector<int>> to2D(const string &s){
    vector<vector<int>> b(3, vector<int>(3));
    for(int i=0;i<9;i++) b[i/3][i%3] = s[i] - '0';
    return b;
}

// Manhattan heuristic on string-form states
int manhattan_string(const string &s, const string &goal){
    array<pair<int,int>,9> goalPos;
    for(int i=0;i<9;i++){
        int val = goal[i] - '0';
        goalPos[val] = {i/3, i%3};
    }
    int h = 0;
    for(int i=0;i<9;i++){
        int v = s[i] - '0';
        if(v == 0) continue;
        auto [gi, gj] = goalPos[v];
        int ri = i/3, rj = i%3;
        h += abs(ri - gi) + abs(rj - gj);
    }
    return h;
}

struct Node {
    int f, g, h;
    string s;
    // min-heap on f, tie-breaker prefer larger g (deeper)
    bool operator<(const Node& o) const {
        if(f != o.f) return f > o.f;
        return g < o.g;
    }
};

// A* returns pair<finalBoard2D, moves>
// If not found, returns empty vector (size 0)
pair<vector<vector<int>>, int> aStar_fast(vector<vector<int>>& iniState,
                                          vector<vector<int>>& goalState,
                                          long long maxExpansions = 20000000LL) {
    string start = serialize2D(iniState);
    string goal  = serialize2D(goalState);
    if(start == goal) return {goalState, 0};

    priority_queue<Node> open;
    unordered_map<string,int> gScore; // best g found so far
    unordered_set<string> closed;     // expanded set
    unordered_map<string,string> parent; // to reconstruct

    int h0 = manhattan_string(start, goal);
    open.push({h0, 0, h0, start});
    gScore[start] = 0;

    long long expansions = 0;
    int dr[4] = {-1,0,1,0}, dc[4] = {0,1,0,-1};

    while(!open.empty()){
        Node cur = open.top(); open.pop();

        // skip if we already expanded this state with better g
        if(closed.count(cur.s)) continue;

        // mark closed (we expand this now)
        closed.insert(cur.s);
        expansions++;

        // progress log (to stderr)
        if((expansions & 0x2710) == 0) { // every 10000 expansions
            cerr << "expanded=" << expansions
                 << "  open=" << open.size()
                 << "  closed=" << closed.size() << "\n";
        }

        // goal check
        if(cur.h == 0){
            // success: print expansions to stderr and return
            cerr << "Goal reached. total expansions=" << expansions << "\n";
            return { to2D(cur.s), cur.g };
        }

        if(expansions > maxExpansions){
            cerr << "Reached expansion limit (" << maxExpansions << "). Aborting.\n";
            break;
        }

        // find zero index
        int z = int(cur.s.find('0'));
        int zr = z/3, zc = z%3;
        for(int k=0;k<4;k++){
            int nr = zr + dr[k], nc = zc + dc[k];
            if(nr < 0 || nr >= 3 || nc < 0 || nc >= 3) continue;
            int ni = nr*3 + nc;

            string nb = cur.s;
            swap(nb[z], nb[ni]);

            int tentative_g = cur.g + 1;
            auto it = gScore.find(nb);
            if(it == gScore.end() || tentative_g < it->second){
                gScore[nb] = tentative_g;
                parent[nb] = cur.s;
                int nh = manhattan_string(nb, goal);
                open.push({tentative_g + nh, tentative_g, nh, nb});
            }
        }
    }

    // not found
    return { vector<vector<int>>(), -1 };
}

int main(){
    vector<vector<int>> iniState = {
        {8,7,6},
        {2,4,5},
        {1,3,0}
    };
    vector<vector<int>> goalState = {
        {1,2,3},
        {4,5,6},
        {7,8,0}
    };

    auto start = hr::now();
    auto ans = aStar_fast(iniState, goalState, 20000000LL); // set max expansions as needed
    auto stop  = hr::now();

    // Always check result before accessing
    if(ans.first.empty()){
        cout << "No solution found (searched limit or unsolvable).\n";
    } else {
        auto block = ans.first;
        int moves = ans.second;
        for(int i=0;i<3;i++){
            for(int j=0;j<3;j++) cout << block[i][j] << " ";
            cout << "\n";
        }
        cout << "\nMoves: " << moves << "\n";
    }

    chrono::duration<double> elapsed = stop - start;
    cout << "Wall time: " << elapsed.count() << " s\n";
    return 0;
}
