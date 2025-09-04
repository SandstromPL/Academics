#include <iostream>
#include <vector>
#include <stack>
using namespace std;

class Graph {
private:
    int V;
    vector<vector<int>> adj;
    vector<bool> visited;
    stack<int> topoStack;

    void DFSVisit(int u) {
        visited[u] = true;

        for (int v : adj[u]) {
            if (!visited[v]) {
                DFSVisit(v);
            }
        }
        topoStack.push(u);
    }

public:
    Graph(int V) : V(V), adj(V), visited(V, false) {}

    void addEdge(int u, int v) {
        adj[u].push_back(v);
    }

    void topologicalSort() {
        for (int i = 0; i < V; ++i) {
            if (!visited[i]) {
                DFSVisit(i);
            }
        }

        cout << "Topological Order: ";
        while (!topoStack.empty()) {
            cout << topoStack.top() << " ";
            topoStack.pop();
        }
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

    g.topologicalSort();

    return 0;
}
