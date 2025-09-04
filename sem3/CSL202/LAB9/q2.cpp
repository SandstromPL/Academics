#include <iostream>
#include <vector>
#include <queue>
using namespace std;

vector<int> bfs(const vector<vector<int>>& adjList, int start) {
    int n = adjList.size();
    vector<bool> visited(n, false);
    vector<int> parent(n, -1);
    queue<int> q;

    visited[start] = true;
    q.push(start);

    while (!q.empty()) {
        int u = q.front();
        q.pop();

        for (int v : adjList[u]) {
            if (!visited[v]) {
                visited[v] = true;
                parent[v] = u;
                q.push(v);
            }
        }
    }
    return parent;
}

void printBFSTree(const vector<int>& parent) {
    cout << "BFS Tree (Parent relationships):\n";
    for (int i = 1; i < parent.size(); ++i) {
        if (parent[i] != -1) {
            cout << "Parent of node " << i << " is node " << parent[i] << endl;
        }
    }
}

int main() {
    vector<vector<int>> adjList = {{},{2, 3},{1, 4},{1, 5},{2},{3}};

    int startNode = 1; 

    vector<int> bfsTree = bfs(adjList, startNode);

    printBFSTree(bfsTree);

    return 0;
}
