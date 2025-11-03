#include<bits/stdc++.h>
using namespace std;

bool dfs(int node,vector<vector<int>>& adj,vector<bool>& vis,int count,int n,vector<int>& path){
    vis[node] = 1;
    path.push_back(node);

    if(count == n){
        return true;
    }

    for (auto nbr : adj[node]){
        if(!vis[nbr]){
            if(dfs(nbr,adj,vis,count+1,n,path))
                return true;
        }
    }

    vis[node] = false;
    path.pop_back(); // Backtrack
    return false;
}

int main(){

    // Using 0-based indexing for the graph
    // {{0,1},{1,2},{2,3},{3,4},{4,5},{5,0}} -> 6
    // {{0,1},{0,2},{0,3},{0,4},{1,2},{1,3},{1,4},{2,3},{2,4},{3,4}} -> 5
    /* 
        {{0,1},{1,2},{2,3},{3,4},{4,0},
        {5,0},{5,1},{5,2},{5,3},{5,4}}
        -> 6
    */

    /*  {{0,1},{1,2},{2,0},
        {3,4},{4,5},{5,3}, 
        {0,3},{1,4},{2,5}}
        -> 6
 */

    /*  {{0,1},{0,2},{0,3},{0,4},{0,5},{0,6},
        {1,2},{1,3},{1,4},{1,5},{1,6},
        {2,3},{2,4},{2,5},{2,6},
        {3,4},{3,5},{3,6},
        {4,5},{4,6},
        {5,6}}
        ->7
 */

    vector<vector<int>> edge = {{0,1},{0,2},{0,3},{0,4},{0,5},{0,6},
        {1,2},{1,3},{1,4},{1,5},{1,6},
        {2,3},{2,4},{2,5},{2,6},
        {3,4},{3,5},{3,6},
        {4,5},{4,6},
        {5,6}};
    int n = 7;
    vector<vector<int>> adj(n);
    vector<int> path;
    for(auto it : edge){
        int u = it[0];
        int v = it[1];
        adj[u].push_back(v);
        adj[v].push_back(u);
    }
    bool ans = false;
    for(int i = 0; i < n; i++){
        vector<bool> vis(n, false);
        if (dfs(i,adj,vis,1,n,path)){ // Start count at 1
            cout<<"Yes hamiltonian path exists with node : "<<i<<endl;
            for(auto it : path){
                cout<<it<<" -> ";
            }
            cout<<path[0]<<"... back to start"<<endl;
            path.clear();
                /* ans = true;
                break; */
            }
    }
    /* if(ans){
        cout<<"Yes hamiltonian path exists with node : "i<<<<endl;
        for(auto it : path){
            cout<<it<<" -> ";
        }
        cout<<path[0]<<"... back to start"<<endl;
    }
    else{
        cout<<"Hamiltonian path does not exist"<<endl;
    } */

    return 0;
}

/*
# Python equivalent of the C++ code

def dfs(node, adj, vis, count, n, path):
    vis[node] = True
    path.append(node)

    if count == n:
        # A Hamiltonian path is found
        return True

    for nbr in adj[node]:
        if not vis[nbr]:
            if dfs(nbr, adj, vis, count + 1, n, path):
                return True

    # Backtrack if no path is found from this node
    vis[node] = False
    path.pop()
    return False

def find_hamiltonian_path():
    # Using 0-based indexing for the graph
    # Example: A complete graph (K7) which always has a Hamiltonian path
    edges = [
        (0,1),(0,2),(0,3),(0,4),(0,5),(0,6),
        (1,2),(1,3),(1,4),(1,5),(1,6),
        (2,3),(2,4),(2,5),(2,6),
        (3,4),(3,5),(3,6),
        (4,5),(4,6),
        (5,6)
    ]
    n = 7

    adj = [[] for _ in range(n)]
    for u, v in edges:
        adj[u].append(v)
        adj[v].append(u)

    path = []
    
    # Try starting from each node to find a Hamiltonian path
    for i in range(n):
        vis = [False] * n
        path.clear()
        if dfs(i, adj, vis, 1, n, path):
            print(f"Yes, a Hamiltonian path exists starting from node: {i}")
            # To show it's a cycle, we can check if the last node connects to the first
            last_node = path[-1]
            start_node = path[0]
            is_cycle = start_node in adj[last_node]
            
            path_str = " -> ".join(map(str, path))
            if is_cycle:
                print(f"{path_str} -> {start_node} (Forms a Hamiltonian Cycle)")
            else:
                print(f"{path_str} (Is a Hamiltonian Path)")
            
            # If you want to find all possible paths, remove the break.
            # For just finding one, this is sufficient.
            return # Exit after finding the first path

    print("No Hamiltonian path exists in the graph.")

# To run the Python code
if __name__ == "__main__":
    find_hamiltonian_path()

*/