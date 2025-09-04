#Tracks initialize
explored_nodes = 0
pruned_nodes = 0

def is_terminal(state):
    # Terminal when all heaps are empty
    return all(h == 0 for h in state)

def utility(state, maximizing):
    # At terminal: if it's MAX's turn, MIN made last move (MAX lost)
    return 1 if not maximizing else -1

def generate_successors(state):
    # Generate successors: remove 1..heap_size stones from each heap
    successors = []
    for i, heap in enumerate(state):
        for remove in range(1, heap + 1):
            new_state = list(state)
            new_state[i] -= remove
            successors.append(tuple(new_state))
    return successors

def alphabeta(state, alpha, beta, maximizing, depth=0):
    global explored_nodes, pruned_nodes
    indent = "  " * depth

    # If terminal, return utility
    if is_terminal(state):
        explored_nodes += 1
        return utility(state, maximizing), None

    best_move = None

    if maximizing:
        value = float('-inf')
        print(f"{indent}MAX explores {state}")
        for succ in generate_successors(state):
            print(f"{indent}  Considering move: {state} → {succ}")
            explored_nodes += 1
            succ_value, _ = alphabeta(succ, alpha, beta, False, depth + 1)
            if succ_value > value:
                value = succ_value
                best_move = succ
            alpha = max(alpha, value)
            if alpha >= beta:
                pruned_nodes += 1
                print(f"{indent}  [Pruned branch at {succ} because alpha >= beta]")
                break
        return value, best_move
    else:
        value = float('inf')
        print(f"{indent}MIN explores {state}")
        for succ in generate_successors(state):
            print(f"{indent}  Considering move: {state} → {succ}")
            explored_nodes += 1
            succ_value, _ = alphabeta(succ, alpha, beta, True, depth + 1)
            if succ_value < value:
                value = succ_value
                best_move = succ
            beta = min(beta, value)
            if alpha >= beta:
                pruned_nodes += 1
                print(f"{indent}  [Pruned branch at {succ} because alpha >= beta]")
                break
        return value, best_move

if __name__ == "__main__":
    initial_state = (1, 2, 3)
    #initial_state = (3, 4, 5)
    explored_nodes = 0
    pruned_nodes = 0
    print(f"Initial State: {initial_state}\n")
    best_value, best_move = alphabeta(initial_state, float('-inf'), float('inf'), True)
    print("\nBest Move for MAX:", initial_state, "→", best_move)
    print("Outcome:", "Winning position" if best_value == 1 else "Losing position")
    print("Nodes Explored:", explored_nodes)
    print("Nodes Pruned:", pruned_nodes)
