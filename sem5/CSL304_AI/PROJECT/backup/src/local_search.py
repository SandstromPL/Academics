"""
Local Search Algorithms
Implements hill climbing and greedy improvement for congestion resolution
"""

import random
from typing import List, Tuple, Set, Optional, Callable


def evaluate_path_quality(path: List[Tuple[int, int]], 
                          robot_positions: dict,
                          goal: Tuple[int, int]) -> float:
    """
    Evaluate quality of a path considering congestion and length
    Lower score is better
    
    Args:
        path: Path to evaluate
        robot_positions: Current positions of other robots
        goal: Goal position
    
    Returns:
        Quality score (lower is better)
    """
    if not path:
        return float('inf')
    
    score = len(path)  # Base score is path length
    
    # Penalize congestion (proximity to other robots)
    congestion_penalty = 0
    for pos in path:
        for robot_pos in robot_positions.values():
            dist = abs(pos[0] - robot_pos[0]) + abs(pos[1] - robot_pos[1])
            if dist <= 2:  # Within 2 cells
                congestion_penalty += (3 - dist) * 2  # Closer = higher penalty
    
    # Penalize distance from goal at end
    if path:
        final_pos = path[-1]
        goal_distance = abs(final_pos[0] - goal[0]) + abs(final_pos[1] - goal[1])
        score += goal_distance * 3
    
    return score + congestion_penalty


def get_alternative_moves(current_pos: Tuple[int, int],
                          blocked_positions: Set[Tuple[int, int]],
                          get_neighbors: Callable[[Tuple[int, int]], List[Tuple[int, int]]]) -> List[Tuple[int, int]]:
    """
    Get alternative moves avoiding blocked positions
    
    Args:
        current_pos: Current position
        blocked_positions: Positions to avoid
        get_neighbors: Function to get valid neighbors
    
    Returns:
        List of alternative positions
    """
    neighbors = get_neighbors(current_pos)
    return [n for n in neighbors if n not in blocked_positions]


def hill_climbing(current_pos: Tuple[int, int],
                 goal: Tuple[int, int],
                 get_neighbors: Callable[[Tuple[int, int]], List[Tuple[int, int]]],
                 blocked_positions: Set[Tuple[int, int]] = None,
                 max_iterations: int = 50) -> Optional[List[Tuple[int, int]]]:
    """
    Hill Climbing for finding detour paths
    Iteratively moves to the neighbor closest to goal
    
    Args:
        current_pos: Starting position
        goal: Goal position
        get_neighbors: Function to get valid neighbors
        blocked_positions: Positions to avoid (e.g., other robots)
        max_iterations: Maximum steps to take
    
    Returns:
        Path from current to goal, or partial path if stuck
    """
    if blocked_positions is None:
        blocked_positions = set()
    
    path = [current_pos]
    visited = {current_pos}
    
    for _ in range(max_iterations):
        if path[-1] == goal:
            return path
        
        # Get unblocked neighbors
        neighbors = get_neighbors(path[-1])
        available = [n for n in neighbors if n not in blocked_positions and n not in visited]
        
        if not available:
            # Stuck - allow revisiting but penalize
            available = [n for n in neighbors if n not in blocked_positions]
            if not available:
                return path  # Completely stuck
        
        # Choose neighbor closest to goal (greedy)
        best_neighbor = min(available, 
                           key=lambda n: abs(n[0] - goal[0]) + abs(n[1] - goal[1]))
        
        path.append(best_neighbor)
        visited.add(best_neighbor)
    
    return path


def random_walk_escape(current_pos: Tuple[int, int],
                      get_neighbors: Callable[[Tuple[int, int]], List[Tuple[int, int]]],
                      blocked_positions: Set[Tuple[int, int]] = None,
                      steps: int = 5) -> List[Tuple[int, int]]:
    """
    Random walk to escape congestion
    Takes random valid moves to get away from crowded area
    
    Args:
        current_pos: Starting position
        get_neighbors: Function to get valid neighbors
        blocked_positions: Positions to avoid
        steps: Number of random steps
    
    Returns:
        Path of random walk
    """
    if blocked_positions is None:
        blocked_positions = set()
    
    path = [current_pos]
    
    for _ in range(steps):
        neighbors = get_neighbors(path[-1])
        available = [n for n in neighbors if n not in blocked_positions]
        
        if not available:
            break
        
        next_pos = random.choice(available)
        path.append(next_pos)
    
    return path


def greedy_detour(current_pos: Tuple[int, int],
                 goal: Tuple[int, int],
                 get_neighbors: Callable[[Tuple[int, int]], List[Tuple[int, int]]],
                 blocked_positions: Set[Tuple[int, int]] = None,
                 intermediate_targets: List[Tuple[int, int]] = None) -> Optional[List[Tuple[int, int]]]:
    """
    Greedy improvement strategy for finding detours
    Tries to navigate around obstacles by setting intermediate waypoints
    
    Args:
        current_pos: Starting position
        goal: Goal position
        get_neighbors: Function to get valid neighbors
        blocked_positions: Positions to avoid
        intermediate_targets: Optional waypoints to visit first
    
    Returns:
        Detour path from current to goal
    """
    if blocked_positions is None:
        blocked_positions = set()
    
    path = [current_pos]
    targets = intermediate_targets[:] if intermediate_targets else []
    targets.append(goal)
    
    max_steps_per_target = 100
    
    for target in targets:
        steps = 0
        while path[-1] != target and steps < max_steps_per_target:
            neighbors = get_neighbors(path[-1])
            
            # Filter out blocked and recently visited positions
            recent_positions = set(path[-5:]) if len(path) > 5 else set(path)
            available = [n for n in neighbors 
                        if n not in blocked_positions and n not in recent_positions]
            
            if not available:
                # Allow backtracking if stuck
                available = [n for n in neighbors if n not in blocked_positions]
                if not available:
                    return None  # Completely blocked
            
            # Choose neighbor that reduces distance to current target
            best = min(available,
                      key=lambda n: abs(n[0] - target[0]) + abs(n[1] - target[1]))
            
            path.append(best)
            steps += 1
        
        if path[-1] != target:
            return None  # Couldn't reach this target
    
    return path


def simulated_annealing_path(start: Tuple[int, int],
                             goal: Tuple[int, int],
                             get_neighbors: Callable[[Tuple[int, int]], List[Tuple[int, int]]],
                             robot_positions: dict,
                             initial_temp: float = 100.0,
                             cooling_rate: float = 0.95,
                             iterations: int = 100) -> Optional[List[Tuple[int, int]]]:
    """
    Simulated annealing for finding good paths avoiding congestion
    
    Args:
        start: Starting position
        goal: Goal position
        get_neighbors: Function to get valid neighbors
        robot_positions: Current positions of other robots
        initial_temp: Initial temperature
        cooling_rate: Temperature reduction factor
        iterations: Number of iterations
    
    Returns:
        Path from start to goal
    """
    # Start with hill climbing solution
    current_path = hill_climbing(start, goal, get_neighbors, set(robot_positions.values()))
    if not current_path:
        return None
    
    current_score = evaluate_path_quality(current_path, robot_positions, goal)
    best_path = current_path[:]
    best_score = current_score
    
    temp = initial_temp
    
    for _ in range(iterations):
        # Generate neighbor solution by modifying a random segment
        if len(current_path) < 3:
            break
        
        # Pick a random point in the path to modify
        idx = random.randint(1, len(current_path) - 2)
        
        # Try alternative move from that point
        neighbors = get_neighbors(current_path[idx - 1])
        available = [n for n in neighbors if n != current_path[idx]]
        
        if not available:
            continue
        
        # Create new path with modified segment
        new_pos = random.choice(available)
        new_path = current_path[:idx] + [new_pos]
        
        # Try to complete path to goal with hill climbing
        completion = hill_climbing(new_pos, goal, get_neighbors)
        if completion and len(completion) > 1:
            new_path.extend(completion[1:])
        else:
            continue
        
        # Evaluate new path
        new_score = evaluate_path_quality(new_path, robot_positions, goal)
        
        # Accept or reject based on score and temperature
        delta = new_score - current_score
        if delta < 0 or random.random() < min(1.0, temp / 100.0 * (1.0 / (1.0 + abs(delta)))):
            current_path = new_path
            current_score = new_score
            
            if current_score < best_score:
                best_path = current_path[:]
                best_score = current_score
        
        # Cool down
        temp *= cooling_rate
    
    return best_path


class LocalSearch:
    """Wrapper class for local search algorithms"""
    
    @staticmethod
    def find_detour(current_pos: Tuple[int, int],
                   goal: Tuple[int, int],
                   get_neighbors: Callable[[Tuple[int, int]], List[Tuple[int, int]]],
                   blocked_positions: Set[Tuple[int, int]] = None,
                   robot_positions: dict = None,
                   algorithm: str = 'hill_climbing') -> Optional[List[Tuple[int, int]]]:
        """
        Find detour path using local search
        
        Args:
            current_pos: Starting position
            goal: Goal position
            get_neighbors: Function to get valid neighbors
            blocked_positions: Positions to avoid
            robot_positions: Current positions of all robots (for SA)
            algorithm: Local search algorithm ('hill_climbing', 'greedy', 'random_walk', 'simulated_annealing')
        
        Returns:
            Detour path from current to goal
        """
        algorithm = algorithm.lower()
        
        if algorithm == 'hill_climbing':
            return hill_climbing(current_pos, goal, get_neighbors, blocked_positions)
        elif algorithm == 'greedy':
            return greedy_detour(current_pos, goal, get_neighbors, blocked_positions)
        elif algorithm == 'random_walk':
            # Random walk then hill climb
            escape_path = random_walk_escape(current_pos, get_neighbors, blocked_positions)
            if escape_path:
                completion = hill_climbing(escape_path[-1], goal, get_neighbors, blocked_positions)
                if completion:
                    return escape_path + completion[1:]
            return None
        elif algorithm == 'simulated_annealing':
            if robot_positions is None:
                robot_positions = {}
            return simulated_annealing_path(current_pos, goal, get_neighbors, robot_positions)
        else:
            raise ValueError(f"Unknown algorithm: {algorithm}")
