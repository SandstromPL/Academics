import collections
import heapq

class State:
    def __init__(self, r1, r2, r3, parent=None, action=None, cost=0, h_score=0):
        self.r = (r1, r2, r3)
        self.parent = parent
        self.action = action
        self.cost = cost
        self.h_score = h_score
        
    def __eq__(self, other):
        return self.r == other.r
    
    def __hash__(self):
        return hash(self.r)
    
    def __lt__(self, other):
        # A* priority queue comparison
        return (self.cost + self.h_score) < (other.cost + other.h_score)

class Problem:
    def __init__(self, capacities, initial_state, target_state):
        self.capacities = capacities
        self.initial_state = State(*initial_state)
        self.target_state = State(*target_state)
        # Safety threshold is 20% of capacity.
        self.min_water = [c * 0.2 for c in capacities] 
    
    def is_goal(self, state):
        # Using a small tolerance for float comparison to avoid precision issues.
        for i in range(len(self.capacities)):
            if abs(state.r[i] - self.target_state.r[i]) > 0.001:
                return False
        return True

    def get_successors(self, state):
        successors = []
        
        # Possible valve operations (src -> dst)
        operations = [(0, 1), (1, 0), (0, 2), (2, 0), (1, 2), (2, 1)]
        
        for src_idx, dst_idx in operations:
            src_amount = state.r[src_idx]
            dst_amount = state.r[dst_idx]
            
            # Check if source has enough water to transfer above its safety threshold.
            if src_amount > self.min_water[src_idx]:
                available_to_transfer = src_amount - self.min_water[src_idx]
                space_in_dst = self.capacities[dst_idx] - dst_amount
                
                transfer_amount = min(available_to_transfer, space_in_dst)
                
                if transfer_amount > 0.001:  # Transfer must be more than a negligible amount
                    new_r = list(state.r)
                    new_r[src_idx] -= transfer_amount
                    new_r[dst_idx] += transfer_amount
                    
                    new_state = State(*new_r, parent=state, action=f"Open valve ({src_idx+1}->{dst_idx+1})", cost=state.cost + 1)
                    successors.append(new_state)
                    
        return successors

# --- Helper: round state only for visited checks ---
def round_state(r):
    return tuple(round(x, 2) for x in r)

def bfs(problem):
    initial_state = problem.initial_state
    if problem.is_goal(initial_state):
        return ([], 0)

    queue = collections.deque([initial_state])
    visited = {round_state(initial_state.r)}

    while queue:
        current_state = queue.popleft()
        
        for successor in problem.get_successors(current_state):
            rs = round_state(successor.r)
            if rs not in visited:
                if problem.is_goal(successor):
                    path = []
                    while successor.parent:
                        path.append(successor.action)
                        successor = successor.parent
                    return (path[::-1], len(path))
                
                visited.add(rs)
                queue.append(successor)
    
    return (None, 0)

def dfs(problem):
    initial_state = problem.initial_state
    if problem.is_goal(initial_state):
        return ([], 0)
        
    stack = [initial_state]
    visited = {round_state(initial_state.r)}

    while stack:
        current_state = stack.pop()
        
        for successor in problem.get_successors(current_state):
            rs = round_state(successor.r)
            if rs not in visited:
                if problem.is_goal(successor):
                    path = []
                    while successor.parent:
                        path.append(successor.action)
                        successor = successor.parent
                    return (path[::-1], len(path))
                
                visited.add(rs)
                stack.append(successor)
    
    return (None, 0)

def a_star_search(problem):
    def heuristic(state, problem):
        # Simple admissible heuristic: number of mismatched reservoirs
        h = 0
        for current_r, target_r in zip(state.r, problem.target_state.r):
            if abs(current_r - target_r) > 0.001:
                h += 1
        return h

    initial_state = problem.initial_state
    initial_state.h_score = heuristic(initial_state, problem)
    
    priority_queue = [initial_state]
    g_scores = {round_state(initial_state.r): 0}
    
    while priority_queue:
        current_state = heapq.heappop(priority_queue)
        
        if problem.is_goal(current_state):
            path = []
            while current_state.parent:
                path.append(current_state.action)
                current_state = current_state.parent
            return (path[::-1], len(path))

        for successor in problem.get_successors(current_state):
            rs = round_state(successor.r)
            tentative_g_score = g_scores[round_state(current_state.r)] + 1
            
            if rs not in g_scores or tentative_g_score < g_scores[rs]:
                g_scores[rs] = tentative_g_score
                successor.h_score = heuristic(successor, problem)
                heapq.heappush(priority_queue, successor)
                
    return (None, 0)

if __name__ == "__main__":
    capacities = (8.0, 5.0, 3.0)
    initial_water = (8.0, 0.0, 0.0)
    target_water = (5.4, 2.0, 0.6)
    
    reservoir_problem = Problem(capacities, initial_water, target_water)
    
    # BFS Solution
    bfs_path, bfs_ops = bfs(reservoir_problem)
    print("BFS Solution:")
    if bfs_path:
        for op in bfs_path:
            print(op)
        print(f"Number of valve operations = {bfs_ops}")
    else:
        print("No solution found.")
        
    print("-" * 20)
    
    # DFS Solution
    dfs_path, dfs_ops = dfs(reservoir_problem)
    print("DFS Solution:")
    if dfs_path:
        for op in dfs_path:
            print(op)
        print(f"Number of valve operations = {dfs_ops}")
    else:
        print("No solution found.")
        
    print("-" * 20)
    
    # A* Solution
    a_star_path, a_star_ops = a_star_search(reservoir_problem)
    print("A* Solution:")
    if a_star_path:
        for op in a_star_path:
            print(op)
        print(f"Number of valve operations = {a_star_ops}")
    else:
        print("No solution found.")
