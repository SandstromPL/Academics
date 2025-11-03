import math

# --- 1. Game State and Successor Function ---

def generate_successors(state):
    """
    Generates all possible successor states from the current state.
    """
    successors = []
    for i, heap_size in enumerate(state):
        # A player must remove at least one stone
        for stones_to_remove in range(1, heap_size + 1):
            # Create the new state tuple
            new_state_list = list(state)
            new_state_list[i] = heap_size - stones_to_remove
            successors.append(tuple(new_state_list))
    return successors

# --- 2. Alpha-Beta Pruning Implementation ---

def alpha_beta_pruning(state, is_max_player, alpha, beta, counters, verbose=False, depth=0):
    """
    Implements the Alpha-Beta pruning algorithm.
    Returns the utility value: +1 for MAX win, -1 for MIN win.
    """
    counters['explored'] += 1
    indent = "  " * depth

    # Check for terminal state
    if sum(state) == 0:
        # If it's MAX's turn and no stones are left, MIN made the last move and won.
        # If it's MIN's turn and no stones are left, MAX made the last move and won.
        return -1 if is_max_player else 1

    if is_max_player:
        best_value = -math.inf
        for next_state in generate_successors(state):
            # Recursively call for the minimizing player
            value = alpha_beta_pruning(next_state, False, alpha, beta, counters, verbose, depth + 1)
            best_value = max(best_value, value)
            alpha = max(alpha, best_value)
            
            # Pruning condition
            if alpha >= beta:
                if verbose:
                    print(f"{indent}[Pruned branch at {next_state} (alpha={alpha}, beta={beta})]")
                counters['pruned'] += 1
                break
        return best_value
    else: # Minimizing player
        best_value = math.inf
        for next_state in generate_successors(state):
            # Recursively call for the maximizing player
            value = alpha_beta_pruning(next_state, True, alpha, beta, counters, verbose, depth + 1)
            best_value = min(best_value, value)
            beta = min(beta, best_value)
            
            # Pruning condition
            if alpha >= beta:
                if verbose:
                    print(f"{indent}[Pruned branch at {next_state} (alpha={alpha}, beta={beta})]")
                counters['pruned'] += 1
                break
        return best_value

# --- 3. Plain Minimax (for Bonus Comparison) ---

def minimax(state, is_max_player, counters):
    """
    Implements the plain Minimax algorithm (no pruning) for comparison.
    """
    counters['explored'] += 1

    if sum(state) == 0:
        return -1 if is_max_player else 1

    if is_max_player:
        best_value = -math.inf
        for next_state in generate_successors(state):
            value = minimax(next_state, False, counters)
            best_value = max(best_value, value)
        return best_value
    else: # Minimizing player
        best_value = math.inf
        for next_state in generate_successors(state):
            value = minimax(next_state, True, counters)
            best_value = min(best_value, value)
        return best_value

# --- 4. Main Solver Function ---

def find_optimal_move(initial_state, use_pruning=True, verbose=False):
    """
    Finds and prints the best move for MAX from the initial state.
    """
    print(f"--- Running with { 'Alpha-Beta Pruning' if use_pruning else 'Plain Minimax' } ---")
    print(f"Initial State: {initial_state}")
    print(f"MAX explores {initial_state}")

    counters = {'explored': 0, 'pruned': 0}
    best_move = None
    best_value = -math.inf
    
    # Initial alpha and beta values
    alpha = -math.inf
    beta = math.inf

    # Loop through MAX's first set of moves
    for move in generate_successors(initial_state):
        if verbose:
            print(f"\nConsidering move: {initial_state} -> {move}")
        
        # Call the appropriate algorithm for MIN's turn
        if use_pruning:
            # It is now MIN's turn (is_max_player=False)
            value = alpha_beta_pruning(move, False, alpha, beta, counters, verbose, depth=1)
        else:
            value = minimax(move, False, counters)

        # The returned value is from MAX's perspective.
        if value > best_value:
            best_value = value
            best_move = move
        
        # Update alpha at the root
        if use_pruning:
            alpha = max(alpha, best_value)

    # Print the results
    outcome = "Winning position" if best_value == 1 else "Losing position"
    print("\n--- Results ---")
    print(f"Best Move for MAX: {initial_state} -> {best_move}")
    print(f"Outcome: {outcome}")
    print(f"Nodes Explored: {counters['explored']}")
    if use_pruning:
        print(f"Nodes Pruned: {counters['pruned']}")
    print("--------------------------------------\n")
    
    return counters['explored']

# --- 5. Program Execution ---

if __name__ == "__main__":
    # Define the initial state as required
    INITIAL_STATE = (3, 4, 5)

    # Run Alpha-Beta Pruning
    # Set verbose=True to see pruning in action (will be very long)
    ab_nodes = find_optimal_move(INITIAL_STATE, use_pruning=True, verbose=False)

    # Run plain Minimax for comparison
    mm_nodes = find_optimal_move(INITIAL_STATE, use_pruning=False, verbose=False)

    # Show efficiency improvement
    print("--- Bonus Comparison ---")
    print(f"Plain Minimax Explored: {mm_nodes} nodes")
    print(f"Alpha-Beta Explored:    {ab_nodes} nodes")
    print(f"Efficiency Improvement: Alpha-Beta explored {mm_nodes - ab_nodes} fewer nodes.")