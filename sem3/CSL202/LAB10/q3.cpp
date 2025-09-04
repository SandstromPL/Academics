#include <iostream>
#include <vector>
using namespace std;

class Graph {
private:
    int V;
    vector<vector<int>> adj;
    vector<bool> visited;
    vector<bool> recStack;

    bool DFSVisit(int u) {
        visited[u] = true;
        recStack[u] = true;

        for (int v : adj[u]) {
            if (!visited[v]) {
                if (DFSVisit(v)) {
                    return true;
                }
            } else if (recStack[v]) {
                return true;
            }
        }

        recStack[u] = false;
        return false;
    }

public:
    Graph(int V) : V(V), adj(V), visited(V, false), recStack(V, false) {}

    void addEdge(int u, int v) {
        adj[u].push_back(v);
    }

    bool isDAG() {
        for (int i = 0; i < V; ++i) {
            if (!visited[i]) {
                if (DFSVisit(i)) {
                    return false;
                }
            }
        }
        return true;
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

    if (g.isDAG()) {
        cout << "The graph is a DAG.\n";
    } else {
        cout << "The graph is not a DAG (contains a cycle).\n";
    }

    return 0;
}
