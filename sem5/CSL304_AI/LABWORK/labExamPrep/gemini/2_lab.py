class Graph:
    def __init__(self, vertices):
        self.V = vertices  # Number of vertices
        self.graph = [[0] * vertices for _ in range(vertices)]
        self.path = []

    def add_edge(self, u, v):
        """Adds an undirected edge between two vertices."""
        self.graph[u][v] = 1
        self.graph[v][u] = 1

    def print_solution(self):
        """Prints the found Hamiltonian cycle."""
        print("✅ Hamiltonian Cycle found:")
        cycle_str = " -> ".join(map(str, self.path))
        print(f"{cycle_str} -> {self.path[0]}")

    def is_safe(self, v, pos):
        """
        Checks if vertex 'v' can be added at position 'pos' in the 
        Hamiltonian path.
        """
        
        # 1. Check if 'v' is adjacent to the previous vertex in the path.
        #    self.path[pos - 1] is the last vertex added.
        if self.graph[self.path[pos - 1]][v] == 0:
            return False
            
        # 2. Check if 'v' has already been included in the path.
        if v in self.path:
            return False
            
        return True

    def find_cycle_util(self, pos):
        """
        The recursive utility function to find the Hamiltonian cycle 
        using backtracking. 'pos' is the current position in the path.
        """
        
        # Base Case: If all vertices are included in the path
        if pos == self.V:
            # Check if the last vertex is connected to the first vertex
            if self.graph[self.path[pos - 1]][self.path[0]] == 1:
                return True
            else:
                return False

        # Try different vertices as the next one in the path
        # We start from 1 because vertex 0 is always the start
        for v in range(1, self.V):
            if self.is_safe(v, pos):
                self.path.append(v)
                
                # Recur to find the rest of the path
                if self.find_cycle_util(pos + 1):
                    return True
                    
                # If adding 'v' didn't lead to a solution, backtrack
                self.path.pop()
        
        return False

    def find_hamiltonian_cycle(self):
        """
        The main function to find and print the Hamiltonian cycle.
        """
        # Start the path with the first vertex (0)
        self.path = [0]
        
        if not self.find_cycle_util(1):
            print("❌ No Hamiltonian Cycle exists for this graph.")
            return False
            
        self.print_solution()
        return True

# --- Main execution ---

print("--- Example 1: Square Graph (Cycle Exists) ---")
# This is the square graph from the document [cite: 10]
# Vertices {0, 1, 2, 3}
g1 = Graph(4)
g1.add_edge(0, 1) # Corresponds to (1,2) in text
g1.add_edge(1, 2) # Corresponds to (2,3) in text
g1.add_edge(2, 3) # Corresponds to (3,4) in text
g1.add_edge(3, 0) # Corresponds to (4,1) in text

g1.find_hamiltonian_cycle()


print("\n--- Example 2: Star Graph (No Cycle) ---")
# This is the star graph from the document 
# 5 vertices: 0 is the center, {1, 2, 3, 4} are leaves
g2 = Graph(5)
g2.add_edge(0, 1)
g2.add_edge(0, 2)
g2.add_edge(0, 3)
g2.add_edge(0, 4)

g2.find_hamiltonian_cycle()
