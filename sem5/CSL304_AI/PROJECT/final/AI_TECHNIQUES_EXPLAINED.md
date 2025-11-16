# AI Techniques Explained

## Detailed explanation of AI techniques used in the warehouse robot simulator

---

## 1. Uninformed Search Algorithms

### What are Uninformed Search Algorithms?
Uninformed (or "blind") search algorithms explore the search space without using problem-specific knowledge. They only distinguish goal states from non-goal states.

### Implemented Algorithms

#### 1.1 Breadth-First Search (BFS)
**How it works:**
- Explores all nodes at depth d before moving to depth d+1
- Uses a queue (FIFO) data structure
- Guarantees shortest path in unweighted graphs

**In our project:**
- Used as fallback when A* fails
- Finds any valid path from robot to package
- Guarantees finding a path if one exists

**Code location:** `src/uninformed_search.py` - `bfs()`

**Example use case:**
```python
path = bfs(robot.position, package.position, warehouse.get_neighbors)
```

#### 1.2 Depth-First Search (DFS)
**How it works:**
- Explores as deep as possible before backtracking
- Uses a stack (LIFO) data structure
- May not find shortest path

**In our project:**
- With depth limit to prevent infinite loops
- Memory-efficient exploration
- Good for checking reachability

**Code location:** `src/uninformed_search.py` - `dfs()`

#### 1.3 Uniform Cost Search (UCS)
**How it works:**
- Expands node with lowest path cost first
- Uses priority queue ordered by cost
- Guarantees optimal path

**In our project:**
- Can handle non-uniform movement costs
- Optimal when all moves have same cost
- Foundation for A*

**Code location:** `src/uninformed_search.py` - `ucs()`

---

## 2. Informed Search Algorithms

### What is Informed Search?
Informed (or "heuristic") search uses problem-specific knowledge to guide the search toward the goal more efficiently.

### 2.1 A* Algorithm
**How it works:**
- Combines actual cost g(n) and heuristic h(n)
- Evaluation function: f(n) = g(n) + h(n)
- Optimal if heuristic is admissible

**Mathematical formulation:**
```
f(n) = g(n) + h(n)
where:
  g(n) = cost from start to node n
  h(n) = estimated cost from n to goal
```

**In our project:**
- Primary pathfinding algorithm
- Uses Manhattan distance heuristic
- Finds optimal paths efficiently

**Code location:** `src/informed_search.py` - `a_star()`

**Why A* is optimal:**
- Manhattan distance is admissible (never overestimates)
- For grid with 4-directional movement
- h(n) ≤ actual distance for all n

### 2.2 Heuristics

#### Manhattan Distance (Primary)
```python
h(pos1, pos2) = |x1 - x2| + |y1 - y2|
```
- **Properties:** Admissible for 4-directional grids
- **Use case:** Standard warehouse navigation

#### Euclidean Distance
```python
h(pos1, pos2) = sqrt((x1-x2)² + (y1-y2)²)
```
- **Properties:** Admissible for continuous space
- **Use case:** When diagonal movement allowed

#### Chebyshev Distance
```python
h(pos1, pos2) = max(|x1-x2|, |y1-y2|)
```
- **Properties:** Admissible for 8-directional grids
- **Use case:** Diagonal movement with same cost

**Code location:** `src/informed_search.py` - heuristic functions

---

## 3. Local Search Algorithms

### What is Local Search?
Local search algorithms start from a current state and move to neighboring states, seeking to improve an objective function. They don't maintain search paths.

### 3.1 Hill Climbing
**How it works:**
1. Start at current position
2. Evaluate all neighbors
3. Move to neighbor closest to goal
4. Repeat until goal reached or stuck

**Characteristics:**
- Greedy approach
- Can get stuck in local optima
- Fast and memory-efficient

**In our project:**
- Used when robot is blocked
- Finds detours around congestion
- Escapes local traffic jams

**Code location:** `src/local_search.py` - `hill_climbing()`

**Example scenario:**
```
Robot blocked by other robots:
  [R1] [ ] [ ]
  [R2] [Me] [Goal]
  [R3] [ ] [ ]

Hill climbing finds: Move up, then right, then right
```

### 3.2 Simulated Annealing
**How it works:**
1. Start with high "temperature"
2. Accept worse moves with probability: e^(-ΔE/T)
3. Gradually cool down (reduce T)
4. Eventually converge to good solution

**Mathematical formulation:**
```
Accept move if:
  ΔE < 0  (improvement)
  OR
  random() < e^(-ΔE/T)  (worse move probabilistically)
  
T(t) = T₀ * cooling_rate^t
```

**In our project:**
- Optimizes paths avoiding congestion
- Escapes local optima
- Better than hill climbing for complex scenarios

**Code location:** `src/local_search.py` - `simulated_annealing_path()`

---

## 4. Adversarial Search (Game Theory)

### What is Adversarial Search?
Adversarial search handles situations where multiple agents have conflicting goals. It models the problem as a game.

### 4.1 Minimax Algorithm
**How it works:**
1. Model as two-player zero-sum game
2. Maximizing player chooses move that maximizes minimum payoff
3. Minimizing player chooses move that minimizes maximum loss
4. Search game tree to depth limit

**Mathematical formulation:**
```
minimax(state, depth, maximizing) =
  if depth = 0 or terminal:
    return evaluate(state)
  if maximizing:
    return max(minimax(successor, depth-1, false))
  else:
    return min(minimax(successor, depth-1, true))
```

**Alpha-Beta Pruning:**
```
Prune branch if:
  β ≤ α
where:
  α = best value for maximizer
  β = best value for minimizer
```

**In our project:**
- Resolves robot-robot conflicts
- Each robot predicts opponent's move
- Finds Nash equilibrium move
- Prevents collisions and deadlocks

**Code location:** `src/adversarial_search.py` - `minimax()`

**Example conflict:**
```
R1 wants: (5,5) → (5,6)
R2 wants: (5,6) → (5,5)

Minimax solution:
R1: stay at (5,5) or move to (4,5)
R2: stay at (5,6) or move to (5,7)
```

### 4.2 Expectimax
**How it works:**
- Like minimax, but models uncertain opponents
- Opponent nodes are "chance nodes"
- Takes expected value instead of min

**In our project:**
- Used when robot behavior unpredictable
- More realistic than minimax
- Handles randomness in opponent moves

**Code location:** `src/adversarial_search.py` - `expectimax()`

---

## 5. Constraint Satisfaction Problems (CSP)

### What is a CSP?
A CSP consists of:
- **Variables:** Things to assign values to
- **Domains:** Possible values for each variable
- **Constraints:** Rules that must be satisfied

### Our CSP Formulation

**Variables:** Robots (R₁, R₂, ..., Rₙ)

**Domains:** Available packages (P₁, P₂, ..., Pₘ)

**Constraints:**
1. **AllDifferent:** Each robot gets unique package
   ```
   ∀i,j: i≠j → assignment[Rᵢ] ≠ assignment[Rⱼ]
   ```

2. **Distance:** Robot-package distance ≤ threshold
   ```
   ∀R,P: |R.pos - P.pos| ≤ max_distance
   ```

3. **WorkloadBalance:** Fair distribution
   ```
   max_load / min_load ≤ balance_factor
   ```

### 5.1 Backtracking Search
**How it works:**
1. Select unassigned variable (robot)
2. Try each value in domain (package)
3. If consistent, assign and recurse
4. If fail, backtrack and try next value

**Pseudocode:**
```
function backtrack(assignment):
  if assignment complete:
    return assignment
  
  robot = select_unassigned_variable()
  for package in order_domain_values(robot):
    if consistent(robot, package):
      assignment[robot] = package
      result = backtrack(assignment)
      if result ≠ failure:
        return result
      remove assignment[robot]
  
  return failure
```

**Code location:** `src/csp.py` - `backtracking_search()`

### 5.2 CSP Heuristics

#### MRV (Minimum Remaining Values)
- Select variable with fewest legal values
- "Most constrained variable"
- Fails fast if no solution

#### LCV (Least Constraining Value)
- Choose value that rules out fewest options for neighbors
- Leaves maximum flexibility

**In our project:**
- MRV: Choose robot with smallest package domain
- LCV: Assign closest package first

**Code location:** `src/csp.py` - `select_unassigned_variable()`, `order_domain_values()`

---

## 6. Integration: How Techniques Work Together

### Simulation Flow

```
1. START
   ↓
2. CSP assigns packages to idle robots
   - Variables: idle robots
   - Domains: unassigned packages
   - Constraints: distance, balance, uniqueness
   ↓
3. Each robot plans path with A*
   - Uses Manhattan distance heuristic
   - Finds optimal path to assigned package
   ↓
4. Robots execute moves
   ↓
5. Conflict detection
   - Check if robots will collide
   ↓
6. IF CONFLICT → Minimax resolution
   - Model as two-player game
   - Find Nash equilibrium moves
   - Avoid collision
   ↓
7. IF BLOCKED → Local search detour
   - Hill climbing finds alternative path
   - Simulated annealing optimizes
   ↓
8. Package pickup/delivery
   ↓
9. IF NOT ALL DELIVERED → Go to step 2
   ↓
10. END
```

### Why This Combination Works

**A* for efficiency:** 
- Optimal paths in clear areas
- Fast with good heuristic

**BFS/DFS for robustness:**
- Fallback when A* fails
- Guaranteed to find solution

**Local search for adaptability:**
- Handles dynamic obstacles (other robots)
- Quick detours when blocked

**Minimax for coordination:**
- Explicit conflict modeling
- Optimal two-agent decisions

**CSP for optimality:**
- Global task allocation
- Balanced workload
- Avoids suboptimal greedy assignment

---

## 7. Performance Analysis

### Time Complexity

| Algorithm | Time Complexity | Space Complexity |
|-----------|----------------|------------------|
| BFS | O(b^d) | O(b^d) |
| DFS | O(b^d) | O(bd) |
| UCS | O(b^d) | O(b^d) |
| A* | O(b^d) | O(b^d) |
| Hill Climbing | O(n) | O(1) |
| Simulated Annealing | O(n*m) | O(n) |
| Minimax | O(b^m) | O(bm) |
| CSP Backtracking | O(d^n) | O(n) |

Where:
- b = branching factor (~4 for grid)
- d = solution depth
- n = number of variables
- m = search depth limit
- n*m = iterations * path length

### When Each Algorithm is Used

**A*** (90% of pathfinding):
- Clear path exists
- No immediate obstacles
- Primary navigation

**BFS/DFS** (5% of pathfinding):
- A* fails (rare)
- Fallback mechanism
- Sanity check

**Local Search** (30% of moves):
- Path blocked by other robots
- Need quick detour
- Congested areas

**Minimax** (10% of steps):
- Robot collision imminent
- Direct path conflict
- Coordinated resolution

**CSP** (At each idle cycle):
- New packages available
- Robots become idle
- Optimal assignment needed

---

## 8. Real-World Applications

### Warehouse Automation
- **Amazon Robotics:** Similar multi-robot coordination
- **Alibaba Smart Warehouse:** Path planning and conflict resolution
- **JD.com Logistics:** CSP for task allocation

### Other Applications
1. **Traffic Management:** Cars as agents, roads as grid
2. **Drone Delivery:** 3D pathfinding with conflicts
3. **Factory Automation:** Assembly line robots
4. **Multi-robot Exploration:** Search and rescue
5. **Game AI:** Strategy games, unit coordination

---

## 9. Extension Ideas

### Advanced Features You Can Add

1. **Dynamic Obstacles:**
   - Moving obstacles
   - Uncertain environment
   - Requires replanning

2. **Communication:**
   - Explicit robot-robot messages
   - Shared knowledge
   - Coordinated plans

3. **Learning:**
   - Q-learning for path preferences
   - Learn congestion patterns
   - Adaptive heuristics

4. **Multi-objective:**
   - Minimize time AND energy
   - Pareto optimization
   - Trade-offs

5. **Hierarchical Planning:**
   - High-level: task allocation
   - Low-level: path execution
   - Two-level optimization

---

## 10. Key Takeaways

### Why These Algorithms?

**Uninformed Search:**
- ✅ Complete (finds solution if exists)
- ✅ Simple to implement
- ❌ Inefficient for large spaces

**Informed Search:**
- ✅ Optimal with good heuristic
- ✅ Much faster than uninformed
- ❌ Needs domain knowledge

**Local Search:**
- ✅ Memory efficient
- ✅ Fast for local repairs
- ❌ Can get stuck

**Adversarial:**
- ✅ Handles conflicts explicitly
- ✅ Game-theoretic optimal
- ❌ Expensive for deep search

**CSP:**
- ✅ Global optimization
- ✅ Constraint reasoning
- ❌ Exponential worst case

### Best Practices

1. **Use A* first:** Most efficient for clear paths
2. **Have fallbacks:** BFS when A* fails
3. **Local repair:** Quick fixes for blocking
4. **Explicit coordination:** Minimax for conflicts
5. **Global planning:** CSP for assignments

---

## 11. Further Reading

### Books
- "Artificial Intelligence: A Modern Approach" - Russell & Norvig
- "Planning Algorithms" - Steven LaValle
- "Multi-Agent Systems" - Gerhard Weiss

### Papers
- "A* Search Algorithm" - Hart, Nilsson, Raphael (1968)
- "Cooperative Pathfinding" - Silver (2005)
- "Multi-Robot Path Planning" - Lavalle & Hutchinson (1998)

### Online Resources
- [Stanford CS221: AI](https://stanford-cs221.github.io/)
- [Berkeley CS188: AI](https://inst.eecs.berkeley.edu/~cs188/)
- [Path Planning Algorithms](https://www.redblobgames.com/pathfinding/)

---

**Document**: AI Techniques Explained  
**Project**: Multi-Agent Warehouse Robot Simulator  
**Course**: CSL304 - Artificial Intelligence  
**Institution**: IIT Bhilai
