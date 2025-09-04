#include <iostream>
#include <vector>
using namespace std;

vector<vector<int>> transposeAdjList(const vector<vector<int>>& adjList) {
    int n = adjList.size();
    vector<vector<int>> transpose(n);

    for (int u = 0; u < n; ++u) {
        for (int v : adjList[u]) {
            transpose[v].push_back(u);
        }
    }
    return transpose;
}

vector<vector<int>> transposeAdjMatrix(const vector<vector<int>>& adjMatrix) {
    int n = adjMatrix.size();
    vector<vector<int>> transpose(n, vector<int>(n, 0));

    for (int u = 0; u < n; ++u) {
        for (int v = 0; v < n; ++v) {
            transpose[v][u] = adjMatrix[u][v];
        }
    }
    return transpose;
}

void printAdjList(const vector<vector<int>>& adjList) {
    for (int i = 0; i < adjList.size(); ++i) {
        cout << i << ": ";
        for (int v : adjList[i]) {
            cout << v << " ";
        }
        cout << endl;
    }
}

void printAdjMatrix(const vector<vector<int>>& adjMatrix) {
    for (int i = 0; i < adjMatrix.size(); ++i) {
        for (int j = 0; j < adjMatrix[i].size(); ++j) {
            cout << adjMatrix[i][j] << " ";
        }
        cout << endl;
    }
}

int main() {
    vector<vector<int>> adjList = {{1, 2},{2},{0},{2}};

    vector<vector<int>> adjMatrix = {{0, 1, 1, 0},{0, 0, 1, 0},{1, 0, 0, 0},{0, 0, 1, 0}};

    vector<vector<int>> transposedAdjList = transposeAdjList(adjList);
    cout << "Transpose (Adjacency List Representation):" << endl;
    printAdjList(transposedAdjList);

    vector<vector<int>> transposedAdjMatrix = transposeAdjMatrix(adjMatrix);
    cout << "\nTranspose (Adjacency Matrix Representation):" << endl;
    printAdjMatrix(transposedAdjMatrix);

    return 0;
}
