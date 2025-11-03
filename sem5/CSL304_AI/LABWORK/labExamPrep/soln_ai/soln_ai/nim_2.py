import math

# Check if game is over (no stones left)
def is_terminal(state):
    return all(pile == 0 for pile in state)

# Get all possible moves (pile index, stones to remove)
def get_moves(state):
    moves = []
    for i, pile in enumerate(state):
        for remove in range(1, pile + 1):
            moves.append((i, remove))
    return moves

# Apply move to state
def apply_move(state, move):
    pile, remove = move
    new_state = state[:]
    new_state[pile] -= remove
    return new_state

# Minimax with Alpha-Beta Pruning and debug output
def minimax(state, depth, alpha, beta, maximizing):
    if is_terminal(state):
        # If maximizing player’s turn, that means minimizing player took last stone (max lost)
        return (-1 if maximizing else 1), None

    if maximizing:
        max_eval = -math.inf
        best_move = None
        for move in get_moves(state):
            print("  " * depth + f"[AI considering move {move}] (alpha={alpha}, beta={beta})")
            eval, _ = minimax(apply_move(state, move), depth + 1, alpha, beta, False)
            if eval > max_eval:
                max_eval = eval
                best_move = move
            alpha = max(alpha, eval)
            if beta <= alpha:
                print("  " * depth + f"[Pruned after move {move}] (alpha={alpha}, beta={beta})")
                break
        return max_eval, best_move
    else:
        min_eval = math.inf
        best_move = None
        for move in get_moves(state):
            print("  " * depth + f"[Opponent considering move {move}] (alpha={alpha}, beta={beta})")
            eval, _ = minimax(apply_move(state, move), depth + 1, alpha, beta, True)
            if eval < min_eval:
                min_eval = eval
                best_move = move
            beta = min(beta, eval)
            if beta <= alpha:
                print("  " * depth + f"[Pruned after move {move}] (alpha={alpha}, beta={beta})")
                break
        return min_eval, best_move

# Play Nim against AI
def play_nim(initial_state):
    state = initial_state[:]
    human_turn = True

    print("Initial piles:", state)
    # Show AI's optimal move from the initial state
    _, initial_best_move = minimax(state, 0, -math.inf, math.inf, True)
    print(f"[Optimal first move for AI would be: remove {initial_best_move[1]} from pile {initial_best_move[0]}]")

    while not is_terminal(state):
        if human_turn:
            print("Your turn. Current piles:", state)
            pile = int(input("Choose pile index: "))
            remove = int(input("How many stones to remove: "))
            if 0 <= pile < len(state) and 1 <= remove <= state[pile]:
                state = apply_move(state, (pile, remove))
                human_turn = False
            else:
                print("Invalid move, try again.")
        else:
            print("AI's turn. Thinking...")
            _, move = minimax(state, 0, -math.inf, math.inf, True)
            state = apply_move(state, move)
            print(f"AI removes {move[1]} from pile {move[0]}")
            human_turn = True

    if human_turn:
        print("AI wins!")
    else:
        print("You win!")


if __name__ == "__main__":
    # Example game with 3 piles
    play_nim([3, 4, 5])
