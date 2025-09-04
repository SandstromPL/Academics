#include <iostream>
#include <vector>
using namespace std;

class Graph {
private:
    int V;
    vector<vector<int>> adj;
    vector<bool> visited;

    void DFSVisit(int u) {
        visited[u] = true;
        cout << u << " ";

        for (int v : adj[u]) {
            if (!visited[v]) {
                cout << "Tree Edge: (" << u << ", " << v << ")\n";
                DFSVisit(v);
            } else {
                cout << "Back Edge: (" << u << ", " << v << ")\n";
            }
        }
    }

public:
    Graph(int V) : V(V), adj(V), visited(V, false) {}

    void addEdge(int u, int v) {
        adj[u].push_back(v);
    }

    void DFS(int start) {
        cout << "DFS Traversal:\n";
        DFSVisit(start);
        cout << endl;
    }
};

int main() {
    int V, E;
    cout << "Enter number of vertices: ";
    cin >> V;
    cout << "Enter number of edges: ";
    cin >> E;

    Graph g(V);

    cout << "Enter the edges (u v) format for directed graph:\n";
    for (int i = 0; i < E; ++i) {
        int u, v;
        cin >> u >> v;
        g.addEdge(u, v);
    }

    int start;
    cout << "Enter starting vertex: ";
    cin >> start;

    g.DFS(start);

    return 0;
}
