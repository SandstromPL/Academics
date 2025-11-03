import heapq

# --- Define the Initial and Goal States from the PDF ---

# Initial State: [cite: 6, 7, 8, 9, 10]
# 1 2 3
# 4 _ 6
# 7 5 8
INITIAL_STATE = [[1, 2, 3], [4, 0, 6], [7, 5, 8]]  # 0 represents the blank space

# Goal State: [cite: 11, 12, 13, 14, 15]
# 1 2 3
# 4 5 6
# 7 8 _
GOAL_STATE = [[1, 2, 3], [4, 5, 6], [7, 8, 0]]

# --- Heuristic Functions ---

def calculate_misplaced_tiles(state, goal_tuple):
    """
    Heuristic 1: Counts the number of tiles not in their goal position.
    """
    misplaced = 0
    for r in range(3):
        for c in range(3):
            if state[r][c] != goal_tuple[r][c] and state[r][c] != 0:
                misplaced += 1
    return misplaced

def calculate_manhattan_distance(state, goal_positions):
    """
    Heuristic 2: Calculates the sum of Manhattan distances for all tiles.
    """
    distance = 0
    for r in range(3):
        for c in range(3):
            tile = state[r][c]
            if tile != 0:
                # Get the (row, col) where this tile *should* be
                goal_r, goal_c = goal_positions[tile]
                # Add the vertical and horizontal distance
                distance += abs(r - goal_r) + abs(c - goal_c)
    return distance

# --- Helper Functions ---

def get_blank_position(state):
    """Finds the (row, col) of the blank space (0)."""
    for r in range(3):
        for c in range(3):
            if state[r][c] == 0:
                return (r, c)
    return None

def get_neighbors(state_tuple):
    """Generates all valid neighboring states from the current state."""
    state = [list(row) for row in state_tuple] # Convert tuple back to list for mutation
    blank_r, blank_c = get_blank_position(state)
    neighbors = []
    
    # Possible moves for the blank: Up, Down, Left, Right [cite: 17, 18, 19, 20]
    for dr, dc in [(0, 1), (0, -1), (1, 0), (-1, 0)]:
        r, c = blank_r + dr, blank_c + dc
        
        # Check if the new position is within the 3x3 grid
        if 0 <= r < 3 and 0 <= c < 3:
            # Create a new state by swapping the blank and the tile
            new_state = [list(row) for row in state] # Deep copy
            new_state[blank_r][blank_c] = new_state[r][c]
            new_state[r][c] = 0
            
            # Convert back to tuple to be hashable
            neighbors.append(tuple(map(tuple, new_state)))
            
    return neighbors

def get_goal_positions(goal_tuple):
    """Pre-computes a map of {tile: (row, col)} for the goal state."""
    positions = {}
    for r in range(3):
        for c in range(3):
            positions[goal_tuple[r][c]] = (r, c)
    return positions

# --- A* Solver ---

def solve_puzzle(initial_state, goal_state, heuristic_func):
    """
    Solves the 8-puzzle using A* search.
    """
    # Convert states to immutable tuples for hashing
    start_tuple = tuple(map(tuple, initial_state))
    goal_tuple = tuple(map(tuple, goal_state))
    
    # Pre-calculate goal positions for Manhattan distance
    goal_positions = get_goal_positions(goal_tuple)

    # Priority queue stores: (f_cost, g_cost, state, path_list)
    # f_cost = g_cost + h_cost
    g_cost = 0
    if heuristic_func == calculate_manhattan_distance:
        h_cost = heuristic_func(start_tuple, goal_positions)
    else:
        h_cost = heuristic_func(start_tuple, goal_tuple)
        
    f_cost = g_cost + h_cost
    
    pq = [(f_cost, g_cost, start_tuple, [start_tuple])] # (priority, cost, state, path)
    visited = {start_tuple} # A set to store states we've already visited

    while pq:
        # Get the state with the lowest f_cost from the priority queue
        f, g, current_state, path = heapq.heappop(pq)
        
        # --- Goal Check ---
        if current_state == goal_tuple:
            return path # Solution found!

        # --- Explore Neighbors ---
        for neighbor in get_neighbors(current_state):
            if neighbor not in visited:
                visited.add(neighbor)
                
                # Calculate costs for the neighbor
                new_g = g + 1
                if heuristic_func == calculate_manhattan_distance:
                    new_h = heuristic_func(neighbor, goal_positions)
                else:
                    new_h = heuristic_func(neighbor, goal_tuple)
                new_f = new_g + new_h
                
                new_path = path + [neighbor]
                heapq.heappush(pq, (new_f, new_g, neighbor, new_path))

    return None # No solution found

# --- Utility to print the solution path ---

def print_solution(path):
    if path is None:
        print("No solution found.")
        return
        
    print(f"Solution found in {len(path) - 1} moves:\n")
    for i, state in enumerate(path):
        print(f"--- Step {i} ---")
        for row in state:
            print(" ".join(str(x) if x != 0 else '_' for x in row))
        print()

# --- Main execution ---
if __name__ == "__main__":
    print("Solving 8-Puzzle using Manhattan Distance (Best Heuristic)...")
    
    # We pass the function itself as an argument
    solution_path = solve_puzzle(INITIAL_STATE, GOAL_STATE, calculate_manhattan_distance)
    print_solution(solution_path)
    
    # Example of solving with the less efficient heuristic
    # print("\nSolving 8-Puzzle using Misplaced Tiles (Less Efficient)...")
    # solution_path_misplaced = solve_puzzle(INITIAL_STATE, GOAL_STATE, calculate_misplaced_tiles)
    # print_solution(solution_path_misplaced)
