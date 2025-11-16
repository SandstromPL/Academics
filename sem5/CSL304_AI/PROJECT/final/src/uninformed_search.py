"""
Uninformed Search Algorithms
Implements BFS, DFS, and UCS for pathfinding without heuristics
"""

from collections import deque
import heapq
from typing import List, Tuple, Set, Optional, Callable


class SearchNode:
    """Node for search algorithms"""
    def __init__(self, position: Tuple[int, int], parent=None, cost: float = 0):
        self.position = position
        self.parent = parent
        self.cost = cost
    
    def __lt__(self, other):
        return self.cost < other.cost
    
    def get_path(self) -> List[Tuple[int, int]]:
        """Reconstruct path from start to this node"""
        path = []
        current = self
        while current:
            path.append(current.position)
            current = current.parent
        return list(reversed(path))


def bfs(start: Tuple[int, int], goal: Tuple[int, int], 
        get_neighbors: Callable[[Tuple[int, int]], List[Tuple[int, int]]]) -> Optional[List[Tuple[int, int]]]:
    """
    Breadth-First Search
    
    Args:
        start: Starting position
        goal: Goal position
        get_neighbors: Function that returns valid neighbors for a position
    
    Returns:
        Path from start to goal, or None if no path exists
    """
    if start == goal:
        return [start]
    
    # Queue of nodes to explore
    queue = deque([SearchNode(start)])
    visited: Set[Tuple[int, int]] = {start}
    
    while queue:
        current = queue.popleft()
        
        # Get valid neighbors
        for neighbor_pos in get_neighbors(current.position):
            if neighbor_pos in visited:
                continue
            
            # Check if we reached the goal
            if neighbor_pos == goal:
                goal_node = SearchNode(neighbor_pos, current)
                return goal_node.get_path()
            
            # Add to queue
            visited.add(neighbor_pos)
            queue.append(SearchNode(neighbor_pos, current))
    
    # No path found
    return None


def dfs(start: Tuple[int, int], goal: Tuple[int, int],
        get_neighbors: Callable[[Tuple[int, int]], List[Tuple[int, int]]],
        max_depth: int = 1000) -> Optional[List[Tuple[int, int]]]:
    """
    Depth-First Search with depth limit
    
    Args:
        start: Starting position
        goal: Goal position
        get_neighbors: Function that returns valid neighbors for a position
        max_depth: Maximum search depth to prevent infinite loops
    
    Returns:
        Path from start to goal, or None if no path exists
    """
    if start == goal:
        return [start]
    
    # Stack of (node, depth) to explore
    stack = [(SearchNode(start), 0)]
    visited: Set[Tuple[int, int]] = {start}
    
    while stack:
        current, depth = stack.pop()
        
        if depth >= max_depth:
            continue
        
        # Get valid neighbors
        for neighbor_pos in get_neighbors(current.position):
            if neighbor_pos in visited:
                continue
            
            # Check if we reached the goal
            if neighbor_pos == goal:
                goal_node = SearchNode(neighbor_pos, current)
                return goal_node.get_path()
            
            # Add to stack
            visited.add(neighbor_pos)
            stack.append((SearchNode(neighbor_pos, current), depth + 1))
    
    # No path found
    return None


def ucs(start: Tuple[int, int], goal: Tuple[int, int],
        get_neighbors: Callable[[Tuple[int, int]], List[Tuple[int, int]]],
        cost_fn: Callable[[Tuple[int, int], Tuple[int, int]], float] = None) -> Optional[List[Tuple[int, int]]]:
    """
    Uniform Cost Search
    
    Args:
        start: Starting position
        goal: Goal position
        get_neighbors: Function that returns valid neighbors for a position
        cost_fn: Function to compute cost between two positions (default: uniform cost of 1)
    
    Returns:
        Path from start to goal with lowest cost, or None if no path exists
    """
    if start == goal:
        return [start]
    
    # Default uniform cost
    if cost_fn is None:
        cost_fn = lambda p1, p2: 1
    
    # Priority queue of (cost, node)
    pq = [(0, SearchNode(start, cost=0))]
    visited: Set[Tuple[int, int]] = set()
    # Track best cost to reach each position
    best_cost: dict = {start: 0}
    
    while pq:
        current_cost, current = heapq.heappop(pq)
        
        # Skip if already visited with better cost
        if current.position in visited:
            continue
        
        visited.add(current.position)
        
        # Check if we reached the goal
        if current.position == goal:
            return current.get_path()
        
        # Explore neighbors
        for neighbor_pos in get_neighbors(current.position):
            if neighbor_pos in visited:
                continue
            
            # Calculate cost to reach neighbor
            edge_cost = cost_fn(current.position, neighbor_pos)
            new_cost = current.cost + edge_cost
            
            # Only consider if this is a better path
            if neighbor_pos not in best_cost or new_cost < best_cost[neighbor_pos]:
                best_cost[neighbor_pos] = new_cost
                neighbor_node = SearchNode(neighbor_pos, current, new_cost)
                heapq.heappush(pq, (new_cost, neighbor_node))
    
    # No path found
    return None


def iterative_deepening_dfs(start: Tuple[int, int], goal: Tuple[int, int],
                            get_neighbors: Callable[[Tuple[int, int]], List[Tuple[int, int]]],
                            max_depth: int = 100) -> Optional[List[Tuple[int, int]]]:
    """
    Iterative Deepening Depth-First Search
    Combines benefits of BFS (completeness) and DFS (memory efficiency)
    
    Args:
        start: Starting position
        goal: Goal position
        get_neighbors: Function that returns valid neighbors for a position
        max_depth: Maximum depth to search
    
    Returns:
        Path from start to goal, or None if no path exists
    """
    def dfs_limited(node: SearchNode, depth: int, visited: Set[Tuple[int, int]]) -> Optional[SearchNode]:
        """DFS with depth limit"""
        if node.position == goal:
            return node
        
        if depth <= 0:
            return None
        
        visited.add(node.position)
        
        for neighbor_pos in get_neighbors(node.position):
            if neighbor_pos not in visited:
                result = dfs_limited(SearchNode(neighbor_pos, node), depth - 1, visited.copy())
                if result is not None:
                    return result
        
        return None
    
    # Try increasing depths
    for depth in range(max_depth):
        result = dfs_limited(SearchNode(start), depth, set())
        if result is not None:
            return result.get_path()
    
    return None


class UninformedSearch:
    """Wrapper class for uninformed search algorithms"""
    
    @staticmethod
    def search(start: Tuple[int, int], goal: Tuple[int, int],
               get_neighbors: Callable[[Tuple[int, int]], List[Tuple[int, int]]],
               algorithm: str = 'bfs') -> Optional[List[Tuple[int, int]]]:
        """
        Perform uninformed search
        
        Args:
            start: Starting position
            goal: Goal position
            get_neighbors: Function that returns valid neighbors
            algorithm: Search algorithm ('bfs', 'dfs', 'ucs', 'iddfs')
        
        Returns:
            Path from start to goal, or None if no path exists
        """
        algorithm = algorithm.lower()
        
        if algorithm == 'bfs':
            return bfs(start, goal, get_neighbors)
        elif algorithm == 'dfs':
            return dfs(start, goal, get_neighbors)
        elif algorithm == 'ucs':
            return ucs(start, goal, get_neighbors)
        elif algorithm == 'iddfs':
            return iterative_deepening_dfs(start, goal, get_neighbors)
        else:
            raise ValueError(f"Unknown algorithm: {algorithm}")
