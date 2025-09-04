#include <iostream>
#include <vector>
#include <algorithm>

using namespace std;

void findBridges(int u, int parent, vector<vector<int>>& adj, vector<bool>& visited, vector<int>& discovery, vector<int>& low, int& time, vector<pair<int, int>>& bridges) {
    visited[u] = true;
    discovery[u] = low[u] = ++time;

    for (int v : adj[u]) {
        if (!visited[v]) {
            findBridges(v, u, adj, visited, discovery, low, time, bridges);

            low[u] = min(low[u], low[v]);

            if (low[v] > discovery[u]) {
                bridges.push_back({u, v});
            }
        }
        else if (v != parent) {
            low[u] = min(low[u], discovery[v]);
        }
    }
}

void findAllBridges(int n, vector<vector<int>>& adj) {
    vector<bool> visited(n, false);
    vector<int> discovery(n, -1), low(n, -1);
    vector<pair<int, int>> bridges;
    int time = 0;

    for (int i = 0; i < n; ++i) {
        if (!visited[i]) {
            findBridges(i, -1, adj, visited, discovery, low, time, bridges);
        }
    }

    if (bridges.empty()) {
        cout << "none" << endl;
    } else {
        for (auto& bridge : bridges) {
            cout << bridge.first << " - " << bridge.second << endl;
        }
    }
}

int main() {
    int n, m;
    cout << "Enter number of vertices and edges: ";
    cin >> n >> m;
    
    vector<vector<int>> adj(n);
    
    cout << "Enter edges (u v):" << endl;
    for (int i = 0; i < m; ++i) {
        int u, v;
        cin >> u >> v;
        adj[u].push_back(v);
        adj[v].push_back(u);
    }

    cout << "Cut edges (bridges) in the graph:" << endl;
    findAllBridges(n, adj);

    return 0;
}
