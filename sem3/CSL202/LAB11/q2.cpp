#include <iostream>
#include <vector>
#include <algorithm>

using namespace std;

void findCutVertices(int u, int parent, vector<vector<int>>& adj, vector<bool>& visited, vector<int>& discovery, vector<int>& low, vector<bool>& isCutVertex, int& time) {
    visited[u] = true;
    discovery[u] = low[u] = ++time;
    int children = 0;

    for (int v : adj[u]) {
        if (!visited[v]) {
            children++;
            findCutVertices(v, u, adj, visited, discovery, low, isCutVertex, time);

            low[u] = min(low[u], low[v]);

            if (parent != -1 && low[v] >= discovery[u]) {
                isCutVertex[u] = true;
            }

            if (parent == -1 && children > 1) {
                isCutVertex[u] = true;
            }
        }
        else if (v != parent) {
            low[u] = min(low[u], discovery[v]);
        }
    }
}

void findAllCutVertices(int n, vector<vector<int>>& adj) {
    vector<bool> visited(n, false);
    vector<int> discovery(n, -1), low(n, -1);
    vector<bool> isCutVertex(n, false);
    int time = 0;

    for (int i = 0; i < n; ++i) {
        if (!visited[i]) {
            findCutVertices(i, -1, adj, visited, discovery, low, isCutVertex, time);
        }
    }

    bool hasCutVertex = false;
    for (int i = 0; i < n; ++i) {
        if (isCutVertex[i]) {
            cout << i << " ";
            hasCutVertex = true;
        }
    }

    if (!hasCutVertex) {
        cout << "none";
    }
    cout << endl;
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

    cout << "Cut vertices (articulation points) in the graph:" << endl;
    findAllCutVertices(n, adj);

    return 0;
}
