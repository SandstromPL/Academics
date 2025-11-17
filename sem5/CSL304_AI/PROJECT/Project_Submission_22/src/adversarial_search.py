"""
Adversarial Search for Conflict Resolution
Implements minimax-based decision making for robot conflicts
"""

from typing import List, Tuple, Optional, Callable
import random


class ConflictState:
    """Represents a conflict state between two robots"""
    def __init__(self, robot1_pos: Tuple[int, int], robot2_pos: Tuple[int, int],
                 robot1_goal: Tuple[int, int], robot2_goal: Tuple[int, int]):
        self.robot1_pos = robot1_pos
        self.robot2_pos = robot2_pos
        self.robot1_goal = robot1_goal
        self.robot2_goal = robot2_goal
    
    def __repr__(self):
        return f"Conflict(R1:{self.robot1_pos}, R2:{self.robot2_pos})"


def evaluate_conflict_state(state: ConflictState, robot_id: int) -> float:
    """
    Evaluate the state from perspective of given robot
    Higher score is better for this robot
    
    Args:
        state: Current conflict state
        robot_id: Which robot's perspective (1 or 2)
    
    Returns:
        Evaluation score
    """
    if robot_id == 1:
        my_pos = state.robot1_pos
        my_goal = state.robot1_goal
        opp_pos = state.robot2_pos
        opp_goal = state.robot2_goal
    else:
        my_pos = state.robot2_pos
        my_goal = state.robot2_goal
        opp_pos = state.robot1_pos
        opp_goal = state.robot1_goal
    
    # Distance to my goal (negative because closer is better)
    my_distance = -(abs(my_pos[0] - my_goal[0]) + abs(my_pos[1] - my_goal[1]))
    
    # Distance to opponent's goal (positive because farther for them is better for me)
    opp_distance = abs(opp_pos[0] - opp_goal[0]) + abs(opp_pos[1] - opp_goal[1])
    
    # Distance between robots (prefer not too close)
    robot_distance = abs(my_pos[0] - opp_pos[0]) + abs(my_pos[1] - opp_pos[1])
    proximity_penalty = -10 if robot_distance <= 1 else 0
    
    # Combine scores
    score = my_distance * 2 + opp_distance * 0.5 + proximity_penalty
    
    return score


def get_possible_moves(position: Tuple[int, int],
                      get_neighbors: Callable[[Tuple[int, int]], List[Tuple[int, int]]],
                      other_robot_pos: Tuple[int, int] = None) -> List[Tuple[int, int]]:
    """
    Get possible moves for a robot, excluding position of other robot
    
    Args:
        position: Current position
        get_neighbors: Function to get valid neighbors
        other_robot_pos: Position to avoid (other robot)
    
    Returns:
        List of valid moves
    """
    moves = get_neighbors(position)
    
    # Can also choose to stay in place
    moves.append(position)
    
    # Filter out other robot's position
    if other_robot_pos:
        moves = [m for m in moves if m != other_robot_pos]
    
    return moves


def minimax(state: ConflictState,
           depth: int,
           maximizing_robot: int,
           get_neighbors: Callable[[Tuple[int, int]], List[Tuple[int, int]]],
           alpha: float = float('-inf'),
           beta: float = float('inf')) -> Tuple[float, Optional[Tuple[int, int]]]:
    """
    Minimax algorithm with alpha-beta pruning for conflict resolution
    
    Args:
        state: Current conflict state
        depth: Search depth remaining
        maximizing_robot: Which robot is maximizing (1 or 2)
        get_neighbors: Function to get valid neighbors
        alpha: Alpha value for pruning
        beta: Beta value for pruning
    
    Returns:
        (best_score, best_move) tuple
    """
    # Base case: depth 0 or conflict resolved
    if depth == 0 or state.robot1_pos == state.robot1_goal or state.robot2_pos == state.robot2_goal:
        return evaluate_conflict_state(state, maximizing_robot), None
    
    if maximizing_robot == 1:
        # Robot 1 is maximizing
        max_eval = float('-inf')
        best_move = None
        
        # Get possible moves for robot 1
        moves = get_possible_moves(state.robot1_pos, get_neighbors, state.robot2_pos)
        
        for move in moves:
            # Create new state with robot 1 moved
            new_state = ConflictState(move, state.robot2_pos, 
                                     state.robot1_goal, state.robot2_goal)
            
            # Recursively evaluate (now robot 2's turn)
            eval_score, _ = minimax(new_state, depth - 1, 2, get_neighbors, alpha, beta)
            
            if eval_score > max_eval:
                max_eval = eval_score
                best_move = move
            
            # Alpha-beta pruning
            alpha = max(alpha, eval_score)
            if beta <= alpha:
                break
        
        return max_eval, best_move
    
    else:
        # Robot 2 is minimizing (from robot 1's perspective)
        min_eval = float('inf')
        best_move = None
        
        # Get possible moves for robot 2
        moves = get_possible_moves(state.robot2_pos, get_neighbors, state.robot1_pos)
        
        for move in moves:
            # Create new state with robot 2 moved
            new_state = ConflictState(state.robot1_pos, move,
                                     state.robot1_goal, state.robot2_goal)
            
            # Recursively evaluate (now robot 1's turn)
            eval_score, _ = minimax(new_state, depth - 1, 1, get_neighbors, alpha, beta)
            
            if eval_score < min_eval:
                min_eval = eval_score
                best_move = move
            
            # Alpha-beta pruning
            beta = min(beta, eval_score)
            if beta <= alpha:
                break
        
        return min_eval, best_move


def expectimax(state: ConflictState,
              depth: int,
              maximizing_robot: int,
              get_neighbors: Callable[[Tuple[int, int]], List[Tuple[int, int]]]) -> Tuple[float, Optional[Tuple[int, int]]]:
    """
    Expectimax algorithm - assumes opponent chooses randomly
    More realistic when robot behavior is unpredictable
    
    Args:
        state: Current conflict state
        depth: Search depth remaining
        maximizing_robot: Which robot is maximizing (1 or 2)
        get_neighbors: Function to get valid neighbors
    
    Returns:
        (expected_score, best_move) tuple
    """
    # Base case
    if depth == 0 or state.robot1_pos == state.robot1_goal or state.robot2_pos == state.robot2_goal:
        return evaluate_conflict_state(state, maximizing_robot), None
    
    if maximizing_robot == 1:
        # Robot 1 is maximizing
        max_eval = float('-inf')
        best_move = None
        
        moves = get_possible_moves(state.robot1_pos, get_neighbors, state.robot2_pos)
        
        for move in moves:
            new_state = ConflictState(move, state.robot2_pos,
                                     state.robot1_goal, state.robot2_goal)
            
            eval_score, _ = expectimax(new_state, depth - 1, 2, get_neighbors)
            
            if eval_score > max_eval:
                max_eval = eval_score
                best_move = move
        
        return max_eval, best_move
    
    else:
        # Robot 2 is a chance node (expected value)
        total_eval = 0
        moves = get_possible_moves(state.robot2_pos, get_neighbors, state.robot1_pos)
        
        if not moves:
            return evaluate_conflict_state(state, 1), None
        
        for move in moves:
            new_state = ConflictState(state.robot1_pos, move,
                                     state.robot1_goal, state.robot2_goal)
            
            eval_score, _ = expectimax(new_state, depth - 1, 1, get_neighbors)
            total_eval += eval_score
        
        # Average of all possible moves
        avg_eval = total_eval / len(moves)
        return avg_eval, None


def resolve_two_robot_conflict(robot1_pos: Tuple[int, int],
                               robot2_pos: Tuple[int, int],
                               robot1_goal: Tuple[int, int],
                               robot2_goal: Tuple[int, int],
                               get_neighbors: Callable[[Tuple[int, int]], List[Tuple[int, int]]],
                               algorithm: str = 'minimax',
                               depth: int = 3) -> Tuple[Tuple[int, int], Tuple[int, int]]:
    """
    Resolve conflict between two robots using game theory
    
    Args:
        robot1_pos: Position of first robot
        robot2_pos: Position of second robot
        robot1_goal: Goal of first robot
        robot2_goal: Goal of second robot
        get_neighbors: Function to get valid neighbors
        algorithm: 'minimax' or 'expectimax'
        depth: Search depth
    
    Returns:
        (best_move_robot1, best_move_robot2) tuple
    """
    state = ConflictState(robot1_pos, robot2_pos, robot1_goal, robot2_goal)
    
    if algorithm == 'minimax':
        # Get best move for robot 1
        _, move1 = minimax(state, depth, 1, get_neighbors)
        
        # Get best move for robot 2 (from its perspective)
        state2 = ConflictState(robot2_pos, robot1_pos, robot2_goal, robot1_goal)
        _, move2 = minimax(state2, depth, 1, get_neighbors)
        
        return move1 if move1 else robot1_pos, move2 if move2 else robot2_pos
    
    elif algorithm == 'expectimax':
        # Get best move for robot 1
        _, move1 = expectimax(state, depth, 1, get_neighbors)
        
        # Get best move for robot 2
        state2 = ConflictState(robot2_pos, robot1_pos, robot2_goal, robot1_goal)
        _, move2 = expectimax(state2, depth, 1, get_neighbors)
        
        return move1 if move1 else robot1_pos, move2 if move2 else robot2_pos
    
    else:
        raise ValueError(f"Unknown algorithm: {algorithm}")


def detect_conflict(robot1_pos: Tuple[int, int],
                   robot2_pos: Tuple[int, int],
                   robot1_next: Tuple[int, int],
                   robot2_next: Tuple[int, int]) -> bool:
    """
    Detect if two robots are in conflict
    
    Conflict types:
    1. Both want same position
    2. Swapping positions (passing through each other)
    3. Too close (adjacent and moving closer)
    
    Args:
        robot1_pos: Current position of robot 1
        robot2_pos: Current position of robot 2
        robot1_next: Next position robot 1 wants
        robot2_next: Next position robot 2 wants
    
    Returns:
        True if conflict detected
    """
    # Same target position
    if robot1_next == robot2_next:
        return True
    
    # Swapping positions
    if robot1_next == robot2_pos and robot2_next == robot1_pos:
        return True
    
    # Moving too close
    current_dist = abs(robot1_pos[0] - robot2_pos[0]) + abs(robot1_pos[1] - robot2_pos[1])
    next_dist = abs(robot1_next[0] - robot2_next[0]) + abs(robot1_next[1] - robot2_next[1])
    
    if current_dist <= 2 and next_dist <= 1:
        return True
    
    return False


class AdversarialSearch:
    """Wrapper class for adversarial search algorithms"""
    
    @staticmethod
    def resolve_conflict(robot1_pos: Tuple[int, int],
                        robot2_pos: Tuple[int, int],
                        robot1_goal: Tuple[int, int],
                        robot2_goal: Tuple[int, int],
                        get_neighbors: Callable[[Tuple[int, int]], List[Tuple[int, int]]],
                        algorithm: str = 'minimax',
                        depth: int = 3) -> Tuple[Tuple[int, int], Tuple[int, int]]:
        """
        Resolve conflict between two robots
        
        Args:
            robot1_pos: Position of first robot
            robot2_pos: Position of second robot
            robot1_goal: Goal of first robot
            robot2_goal: Goal of second robot
            get_neighbors: Function to get valid neighbors
            algorithm: 'minimax' or 'expectimax'
            depth: Search depth
        
        Returns:
            (move_for_robot1, move_for_robot2)
        """
        return resolve_two_robot_conflict(robot1_pos, robot2_pos,
                                         robot1_goal, robot2_goal,
                                         get_neighbors, algorithm, depth)
    
    @staticmethod
    def is_conflict(robot1_pos: Tuple[int, int],
                   robot2_pos: Tuple[int, int],
                   robot1_next: Tuple[int, int],
                   robot2_next: Tuple[int, int]) -> bool:
        """Check if two robots are in conflict"""
        return detect_conflict(robot1_pos, robot2_pos, robot1_next, robot2_next)
