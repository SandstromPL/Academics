"""
Informed Search Algorithms
Implements A* with various heuristics for optimal pathfinding
"""

import heapq
from typing import List, Tuple, Set, Optional, Callable


class AStarNode:
    """Node for A* search"""
    def __init__(self, position: Tuple[int, int], parent=None, g: float = 0, h: float = 0):
        self.position = position
        self.parent = parent
        self.g = g  # Cost from start to this node
        self.h = h  # Heuristic estimate to goal
        self.f = g + h  # Total estimated cost
    
    def __lt__(self, other):
        return self.f < other.f
    
    def get_path(self) -> List[Tuple[int, int]]:
        """Reconstruct path from start to this node"""
        path = []
        current = self
        while current:
            path.append(current.position)
            current = current.parent
        return list(reversed(path))


def manhattan_distance(pos1: Tuple[int, int], pos2: Tuple[int, int]) -> float:
    """
    Manhattan distance heuristic (L1 norm)
    Admissible for grid with 4-directional movement
    """
    return abs(pos1[0] - pos2[0]) + abs(pos1[1] - pos2[1])


def euclidean_distance(pos1: Tuple[int, int], pos2: Tuple[int, int]) -> float:
    """
    Euclidean distance heuristic (L2 norm)
    Can be admissible depending on movement constraints
    """
    return ((pos1[0] - pos2[0])**2 + (pos1[1] - pos2[1])**2)**0.5


def chebyshev_distance(pos1: Tuple[int, int], pos2: Tuple[int, int]) -> float:
    """
    Chebyshev distance (L-infinity norm)
    Admissible for grid with 8-directional movement
    """
    return max(abs(pos1[0] - pos2[0]), abs(pos1[1] - pos2[1]))


def octile_distance(pos1: Tuple[int, int], pos2: Tuple[int, int]) -> float:
    """
    Octile distance - combines diagonal and straight movement
    Good for 8-directional grids
    """
    dx = abs(pos1[0] - pos2[0])
    dy = abs(pos1[1] - pos2[1])
    return (dx + dy) + (1.414 - 2) * min(dx, dy)


def a_star(start: Tuple[int, int], goal: Tuple[int, int],
           get_neighbors: Callable[[Tuple[int, int]], List[Tuple[int, int]]],
           heuristic: Callable[[Tuple[int, int], Tuple[int, int]], float] = manhattan_distance,
           cost_fn: Callable[[Tuple[int, int], Tuple[int, int]], float] = None) -> Optional[List[Tuple[int, int]]]:
    """
    A* Search Algorithm
    
    Args:
        start: Starting position
        goal: Goal position
        get_neighbors: Function that returns valid neighbors for a position
        heuristic: Heuristic function to estimate cost to goal
        cost_fn: Function to compute actual cost between positions (default: 1 per move)
    
    Returns:
        Optimal path from start to goal, or None if no path exists
    """
    if start == goal:
        return [start]
    
    # Default uniform cost
    if cost_fn is None:
        cost_fn = lambda p1, p2: 1
    
    # Priority queue: (f_score, node)
    open_set = [(0, AStarNode(start, g=0, h=heuristic(start, goal)))]
    closed_set: Set[Tuple[int, int]] = set()
    
    # Track best g score for each position
    g_scores = {start: 0}
    
    while open_set:
        _, current = heapq.heappop(open_set)
        
        # Skip if already processed
        if current.position in closed_set:
            continue
        
        # Mark as processed
        closed_set.add(current.position)
        
        # Check if we reached the goal
        if current.position == goal:
            return current.get_path()
        
        # Explore neighbors
        for neighbor_pos in get_neighbors(current.position):
            if neighbor_pos in closed_set:
                continue
            
            # Calculate tentative g score
            edge_cost = cost_fn(current.position, neighbor_pos)
            tentative_g = current.g + edge_cost
            
            # Only process if this is a better path
            if neighbor_pos not in g_scores or tentative_g < g_scores[neighbor_pos]:
                g_scores[neighbor_pos] = tentative_g
                h_score = heuristic(neighbor_pos, goal)
                neighbor_node = AStarNode(neighbor_pos, current, tentative_g, h_score)
                heapq.heappush(open_set, (neighbor_node.f, neighbor_node))
    
    # No path found
    return None


def weighted_a_star(start: Tuple[int, int], goal: Tuple[int, int],
                    get_neighbors: Callable[[Tuple[int, int]], List[Tuple[int, int]]],
                    weight: float = 1.5,
                    heuristic: Callable[[Tuple[int, int], Tuple[int, int]], float] = manhattan_distance,
                    cost_fn: Callable[[Tuple[int, int], Tuple[int, int]], float] = None) -> Optional[List[Tuple[int, int]]]:
    """
    Weighted A* - trades optimality for speed by inflating heuristic
    
    Args:
        start: Starting position
        goal: Goal position
        get_neighbors: Function that returns valid neighbors
        weight: Heuristic weight (>1 = faster but suboptimal, =1 = optimal A*)
        heuristic: Heuristic function
        cost_fn: Cost function
    
    Returns:
        Path from start to goal (may be suboptimal if weight > 1)
    """
    if start == goal:
        return [start]
    
    if cost_fn is None:
        cost_fn = lambda p1, p2: 1
    
    # Weighted heuristic
    weighted_heuristic = lambda p1, p2: weight * heuristic(p1, p2)
    
    open_set = [(0, AStarNode(start, g=0, h=weighted_heuristic(start, goal)))]
    closed_set: Set[Tuple[int, int]] = set()
    g_scores = {start: 0}
    
    while open_set:
        _, current = heapq.heappop(open_set)
        
        if current.position in closed_set:
            continue
        
        closed_set.add(current.position)
        
        if current.position == goal:
            return current.get_path()
        
        for neighbor_pos in get_neighbors(current.position):
            if neighbor_pos in closed_set:
                continue
            
            edge_cost = cost_fn(current.position, neighbor_pos)
            tentative_g = current.g + edge_cost
            
            if neighbor_pos not in g_scores or tentative_g < g_scores[neighbor_pos]:
                g_scores[neighbor_pos] = tentative_g
                h_score = weighted_heuristic(neighbor_pos, goal)
                neighbor_node = AStarNode(neighbor_pos, current, tentative_g, h_score)
                heapq.heappush(open_set, (neighbor_node.f, neighbor_node))
    
    return None


def greedy_best_first(start: Tuple[int, int], goal: Tuple[int, int],
                      get_neighbors: Callable[[Tuple[int, int]], List[Tuple[int, int]]],
                      heuristic: Callable[[Tuple[int, int], Tuple[int, int]], float] = manhattan_distance) -> Optional[List[Tuple[int, int]]]:
    """
    Greedy Best-First Search - only uses heuristic (ignores actual cost)
    Fast but not optimal
    
    Args:
        start: Starting position
        goal: Goal position
        get_neighbors: Function that returns valid neighbors
        heuristic: Heuristic function
    
    Returns:
        Path from start to goal (may be suboptimal)
    """
    if start == goal:
        return [start]
    
    # Priority queue based only on heuristic
    open_set = [(heuristic(start, goal), AStarNode(start, h=heuristic(start, goal)))]
    closed_set: Set[Tuple[int, int]] = set()
    
    while open_set:
        _, current = heapq.heappop(open_set)
        
        if current.position in closed_set:
            continue
        
        closed_set.add(current.position)
        
        if current.position == goal:
            return current.get_path()
        
        for neighbor_pos in get_neighbors(current.position):
            if neighbor_pos in closed_set:
                continue
            
            h_score = heuristic(neighbor_pos, goal)
            neighbor_node = AStarNode(neighbor_pos, current, h=h_score)
            heapq.heappush(open_set, (h_score, neighbor_node))
    
    return None


class InformedSearch:
    """Wrapper class for informed search algorithms"""
    
    HEURISTICS = {
        'manhattan': manhattan_distance,
        'euclidean': euclidean_distance,
        'chebyshev': chebyshev_distance,
        'octile': octile_distance
    }
    
    @staticmethod
    def search(start: Tuple[int, int], goal: Tuple[int, int],
               get_neighbors: Callable[[Tuple[int, int]], List[Tuple[int, int]]],
               algorithm: str = 'astar',
               heuristic: str = 'manhattan',
               weight: float = 1.0) -> Optional[List[Tuple[int, int]]]:
        """
        Perform informed search
        
        Args:
            start: Starting position
            goal: Goal position
            get_neighbors: Function that returns valid neighbors
            algorithm: Search algorithm ('astar', 'weighted_astar', 'greedy')
            heuristic: Heuristic name ('manhattan', 'euclidean', 'chebyshev', 'octile')
            weight: Weight for weighted A* (ignored for other algorithms)
        
        Returns:
            Path from start to goal, or None if no path exists
        """
        # Get heuristic function
        if isinstance(heuristic, str):
            heuristic_fn = InformedSearch.HEURISTICS.get(heuristic.lower(), manhattan_distance)
        else:
            heuristic_fn = heuristic
        
        algorithm = algorithm.lower()
        
        if algorithm == 'astar':
            return a_star(start, goal, get_neighbors, heuristic_fn)
        elif algorithm == 'weighted_astar':
            return weighted_a_star(start, goal, get_neighbors, weight, heuristic_fn)
        elif algorithm == 'greedy':
            return greedy_best_first(start, goal, get_neighbors, heuristic_fn)
        else:
            raise ValueError(f"Unknown algorithm: {algorithm}")
