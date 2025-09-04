#include <iostream>
#include <vector>
using namespace std;

vector<vector<int>> createAdjacencyList(const vector<pair<int, int>>& edges, int n) {
    vector<vector<int>> adjList(n + 1);
    for (const auto& edge : edges) {
        int u = edge.first;
        int v = edge.second;
        adjList[u].push_back(v);
        adjList[v].push_back(u);
    }
    return adjList;
}

vector<vector<int>> createAdjacencyMatrix(const vector<pair<int, int>>& edges, int n) {
    vector<vector<int>> adjMatrix(n + 1, vector<int>(n + 1, 0));
    for (const auto& edge : edges) {
        int u = edge.first;
        int v = edge.second;
        adjMatrix[u][v] = 1;
        adjMatrix[v][u] = 1;
    }
    return adjMatrix;
}

void printAdjacencyList(const vector<vector<int>>& adjList) {
    for (int i = 1; i < adjList.size(); ++i) {
        cout << i << ": ";
        for (int j : adjList[i]) {
            cout << j << " ";
        }
        cout << endl;
    }
}

void printAdjacencyMatrix(const vector<vector<int>>& adjMatrix) {
    for (int i = 1; i < adjMatrix.size(); ++i) {
        for (int j = 1; j < adjMatrix[i].size(); ++j) {
            cout << adjMatrix[i][j] << " ";
        }
        cout << endl;
    }
}

int main() {
    vector<pair<int, int>> edges = {{1, 2}, {2, 3}};

    int n = 3;

    vector<vector<int>> adjList = createAdjacencyList(edges, n);
    cout << "Adjacency List:\n";
    printAdjacencyList(adjList);

    vector<vector<int>> adjMatrix = createAdjacencyMatrix(edges, n);
    cout << "\nAdjacency Matrix:\n";
    printAdjacencyMatrix(adjMatrix);

    return 0;
}
