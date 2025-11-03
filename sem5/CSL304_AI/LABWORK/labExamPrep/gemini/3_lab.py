import random
import math

def calculate_conflicts(board):
    """
    Calculates the total number of attacking pairs (conflicts).
    We only need to check for diagonal attacks since the state representation
     already prevents row and column conflicts.
    """
    conflicts = 0
    n = len(board)
    for i in range(n):
        for j in range(i + 1, n):
            # Check for diagonal conflicts
            # abs(row1 - row2) == abs(col1 - col2)
            if abs(board[i] - board[j]) == abs(i - j):
                conflicts += 1
    return conflicts

def print_board(board):
    """Helper function to print the board."""
    n = len(board)
    print("Board State (Conflicts: {}): {}".format(calculate_conflicts(board), board))
    for i in range(n):
        row_str = ""
        for j in range(n):
            if board[j] == i + 1:
                row_str += " Q "
            else:
                row_str += " . "
        print(row_str)

def solve_8_queens_sa(initial_temp, cooling_rate, min_temp):
    """
    Solves the 8-Queens problem using Simulated Annealing.
    """
    
    # 1. Start with a random solution 
    # We use a permutation of [1..8] to ensure no row/col conflicts initially
    current_board = list(range(1, 9))
    random.shuffle(current_board)
    current_cost = calculate_conflicts(current_board)
    
    T = initial_temp
    
    # 5. Gradually reduce the temperature until it becomes very small 
    while T > min_temp:
        # Check if we found a solution
        if current_cost == 0:
            # Found a valid solution [cite: 24]
            return current_board
            
        # 2. Modify the state to create a new solution 
        # We will swap the row values of two random columns 
        new_board = list(current_board)
        i, j = random.sample(range(8), 2)
        new_board[i], new_board[j] = new_board[j], new_board[i]
        
        new_cost = calculate_conflicts(new_board)
        
        # Calculate the change in cost (energy)
        delta_E = new_cost - current_cost
        
        if delta_E < 0:
            # 3. If it is better, accept it 
            current_board = new_board
            current_cost = new_cost
        else:
            # 4. If it is worse, accept it with some probability 
            acceptance_probability = math.exp(-delta_E / T)
            if random.random() < acceptance_probability:
                current_board = new_board
                current_cost = new_cost
                
        # 5. Reduce the temperature 
        T *= cooling_rate
        
    # Return the best solution found if no perfect solution was reached
    return current_board

# --- Main execution ---
if __name__ == "__main__":
    
    # Algorithm parameters
    INITIAL_TEMPERATURE = 1000
    COOLING_RATE = 0.999
    MIN_TEMPERATURE = 1e-5
    
    print("Solving 8-Queens using Simulated Annealing...")
    
    solution = solve_8_queens_sa(INITIAL_TEMPERATURE, COOLING_RATE, MIN_TEMPERATURE)
    
    print("\n--- Final Solution Found ---")
    print_board(solution)
    
    if calculate_conflicts(solution) == 0:
        print("\nSuccessfully found a zero-conflict solution!")
    else:
        print("\nCould not find a perfect solution. This is the best state found.")
