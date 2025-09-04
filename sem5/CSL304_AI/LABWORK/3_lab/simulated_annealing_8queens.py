import random
import math

def calculate_conflicts(state):
    """Calculate number of attacking queen pairs in the given state."""
    conflicts = 0
    n = len(state)
    
    for i in range(n):
        for j in range(i + 1, n):
            # Same row conflict
            if state[i] == state[j]:
                conflicts += 1
            # Diagonal conflict
            if abs(state[i] - state[j]) == abs(i - j):
                conflicts += 1
    
    return conflicts

def get_random_neighbor(state):
    """Generate a random neighbor by moving one queen to a different row."""
    new_state = state.copy()
    col = random.randint(0, len(state) - 1)
    new_row = random.randint(1, len(state))
    new_state[col] = new_row
    return new_state

def simulated_annealing(initial_state, max_iterations=10000, initial_temp=1000, cooling_rate=0.95):
    """
    Simulated Annealing algorithm for 8-Queens problem.
    
    Steps:
    1. Start with initial solution
    2. Generate neighbor solution
    3. Accept if better, or with probability if worse
    4. Gradually reduce temperature
    5. Return best solution found
    """
    current_state = initial_state.copy()
    current_cost = calculate_conflicts(current_state)
    
    best_state = current_state.copy()
    best_cost = current_cost
    
    temperature = initial_temp
    
    print(f"Starting state: {current_state}")
    print(f"Initial conflicts: {current_cost}")
    print("-" * 50)
    
    for iteration in range(max_iterations):
        # Generate neighbor
        new_state = get_random_neighbor(current_state)
        new_cost = calculate_conflicts(new_state)
        
        # Accept or reject the new state
        if new_cost < current_cost:
            # Better solution - accept
            current_state = new_state
            current_cost = new_cost
        else:
            # Worse solution - accept with probability
            delta = new_cost - current_cost
            probability = math.exp(-delta / temperature)
            
            if random.random() < probability:
                current_state = new_state
                current_cost = new_cost
        
        # Update best solution
        if current_cost < best_cost:
            best_state = current_state.copy()
            best_cost = current_cost
            print(f"Iteration {iteration}: New best solution with {best_cost} conflicts")
        
        # Cool down temperature
        temperature *= cooling_rate
        
        # Stop if perfect solution found
        if best_cost == 0:
            print(f"Perfect solution found at iteration {iteration}!")
            break
        
        # Progress update
        if iteration % 1000 == 0:
            print(f"Iteration {iteration}: Current cost={current_cost}, Best cost={best_cost}, Temp={temperature:.4f}")
    
    return best_state, best_cost

def print_board(state):
    """Print the chess board with queens."""
    n = len(state)
    print("\nFinal board:")
    for row in range(n, 0, -1):
        line = ""
        for col in range(n):
            if state[col] == row:
                line += "Q "
            else:
                line += ". "
        print(f"{row} {line}")
    print("  " + " ".join([str(i+1) for i in range(n)]))

# Main execution
if __name__ == "__main__":
    # Given initial state from problem statement
    initial_state = [2, 7, 4, 8, 1, 3, 6, 5]
    
    print("Simulated Annealing for 8-Queens Problem")
    print("=" * 50)
    
    # Solve using simulated annealing
    solution, final_conflicts = simulated_annealing(initial_state)
    
    print("\n" + "=" * 50)
    print("RESULT:")
    print(f"Final solution: {solution}")
    print(f"Final conflicts: {final_conflicts}")
    
    if final_conflicts == 0:
        print("✅ SUCCESS: Found valid 8-Queens solution!")
    else:
        print("⚠️ Near-optimal solution found")
    
    print_board(solution)
