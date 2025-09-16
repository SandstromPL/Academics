board = [
    [0,1,0],
    [-1,0,0],
    [1,0,-1],
]

def get_lines(board):
    lines = []

    # rows
    lines.extend(board)

    # columns
    for col in range(3):
        column = [board[row][col] for row in range(3)]
        lines.append(column)

    # diagonals
    d1 = [board[i][i] for i in range(3)]
    d2 = [board[i][2-i] for i in range(3)]
    lines.append(d1)
    lines.append(d2)

    return lines

def calc_line_val(board):
    X1 = X2 = X3 = O1 = O2 = O3 = 0
    lines = get_lines(board)
    for line in lines:
        count_x = line.count(1)
        count_o = line.count(-1)
        if count_o == 0:
            if count_x == 1:
                X1 += 1
            elif count_x == 2:
                X2 += 1
            elif count_x == 3:
                X3 += 1

        if count_x == 0:
            if count_o == 1:
                O1 += 1
            elif count_o == 2:
                O2 += 1
            elif count_o == 3:
                O3 += 1   
        
    return X1, X2, X3, O1, O2, O3


def count_empty_spaces(board):
    count = 0
    for row in board:
        count += row.count(0)
    return count

def evaluate(board):
    X1, X2, X3, O1, O2, O3 = calc_line_val(board)
    e = (8*X3 + 3*X2 + X1) - (8*O3 + 3*O2 + O1)
    return e

def game_completed(board):
    X1, X2, X3, O1, O2, O3 = calc_line_val(board)
    if X3 > 0 or O3 > 0:
        return True
    if count_empty_spaces(board) > 0:
        return False
    else:
        return True

def get_possible_moves(board):
    moves = []
    for i in range(3):
        for j in range(3):
            if board[i][j] == 0:
                moves.append((i,j))
    return moves

def min_max(board, depth, alpha, beta, is_maximizing):
    if game_completed(board):
        return evaluate(board), None
    if is_maximizing:
        best_val = float('-inf')
        best_move = None
        for move in get_possible_moves(board):
            i, j = move
            board[i][j] = 1
            val, _ = min_max(board, depth+1, alpha, beta, False)
            board[i][j] = 0
            if val > best_val:
                best_val = val
                best_move = move
            if best_val > alpha:
                alpha = best_val 
            if beta <= alpha:
                break     
        return best_val, best_move
    else:
        best_val = float('inf')
        best_move = None
        for move in get_possible_moves(board):
            i, j = move
            board[i][j] = -1
            val, _ = min_max(board, depth+1, alpha, beta, True)
            board[i][j] = 0
            if val < best_val:
                best_val = val
                best_move = move
            if beta > best_val:
                beta = best_val  
            if beta <= alpha:
                break     
        return best_val, best_move

# Run minimax from current board (X's turn)
score, best_move_for_x = min_max(board, 0, float('-inf'), float('inf'), True)
print("Optimal move for X:", best_move_for_x)