import matplotlib.pyplot as plt
import networkx as nx
import time
from copy import deepcopy

# --- 1. Problem Definition (from Lab Assignment-5.pdf) ---

# Variables: 29 States [cite: 5, 27-57]
# (Sorting them for static order in plain backtracking)
variables = [
    "AP", "AR", "AS", "BR", "CG", "GA", "GJ", "HR", "HP", "JH", 
    "KA", "KL", "MP", "MH", "MN", "ML", "MZ", "NL", "OD", "PB", 
    "RJ", "SK", "TN", "TS", "TR", "UP", "UK", "WB", "JK"
]
variables.sort()

# Domain: 4 Colors [cite: 5]
colors = ['Red', 'Green', 'Blue', 'Yellow']

# Constraints: Adjacency List [cite: 58-86]
neighbors = {
    "AP": ["TS", "OD", "TN", "KA"],
    "AR": ["AS", "NL"],
    "AS": ["AR", "NL", "ML", "TR", "MZ", "MN", "WB"],
    "BR": ["UP", "JH", "WB"],
    "CG": ["UP", "JH", "OD", "MH", "MP", "TS"], # TS, MP added for symmetry
    "GA": ["MH", "KA"],
    "GJ": ["MH", "RJ", "MP"], # MP added for symmetry
    "HR": ["PB", "HP", "UK", "RJ", "UP"], # UP added for symmetry
    "HP": ["JK", "PB", "HR", "UK"],
    "JH": ["BR", "UP", "CG", "OD", "WB"],
    "KA": ["MH", "AP", "TS", "TN", "KL", "GA"],
    "KL": ["KA", "TN"],
    "MP": ["RJ", "UP", "CG", "MH", "GJ"],
    "MH": ["GJ", "MP", "CG", "TS", "KA", "GA"],
    "MN": ["AS", "MZ", "NL"],
    "ML": ["AS", "TR"],
    "MZ": ["AS", "MN", "TR"],
    "NL": ["AR", "AS", "MN"],
    "OD": ["WB", "JH", "CG", "AP", "TS"],
    "PB": ["JK", "HP", "HR", "RJ"],
    "RJ": ["PB", "HR", "MP", "GJ", "UP"],
    "SK": ["WB"],
    "TN": ["AP", "KA", "KL"],
    "TS": ["MH", "KA", "AP", "OD", "CG"], # CG added for symmetry
    "TR": ["AS", "ML", "MZ"],
    "UP": ["UK", "HR", "RJ", "MP", "CG", "JH", "BR"],
    "UK": ["HP", "HR", "UP"],
    "WB": ["BR", "JH", "OD", "AS", "SK"],
    "JK": ["HP", "PB"] # Added missing key
}

# --- 2. Utility Functions (Same as Demo) ---

# [cite: 128] Check if assignment is valid
def is_valid(assignment, var, value):
    # [cite: 129] for n in neighbors [var]:
    for n in neighbors[var]:
        # [cite: 130] if n in assignment and assignment[n] value:
        if n in assignment and assignment[n] == value:
            return False # [cite: 131]
    return True # [cite: 133]

# --- 3. Visualization Function (Adapted from Demo) ---

# [cite: 153] def visualize_coloring(solution, title, G, pos):
def visualize_coloring(solution, title, G, pos):
    """
    Uses networkx and matplotlib to draw the colored graph.
    G and pos are pre-computed for efficiency.
    """
    # [cite: 177] node_colors [solution.get(node, "white") for node in G.nodes()]
    node_colors = [solution.get(node, "white") for node in G.nodes()]
    
    # [cite: 178] plt.figure(figsize=(12, 12)) # Made larger for 29 nodes
    plt.figure(figsize=(12, 12))
    
    # [cite: 179] nx.draw(
    # [cite: 181] G, pos,
    # [cite: 182] with_labels True,
    # [cite: 183] node_color node_colors,
    # [cite: 184] node size = 3000, # Increased size
    # [cite: 185] font_size = 10,
    # [cite: 186] font_weight ="bold",
    # [cite: 187] edge_color="black"
    nx.draw(
        G, pos,
        with_labels=True,
        node_color=node_colors,
        node_size=3000,
        font_size=10,
        font_weight="bold",
        edge_color="black"
    )
    # [cite: 188] plt.title(title)
    plt.title(title, fontsize=16)
    # [cite: 189] plt.show()
    plt.show()

# --- 4. Algorithm 1: Plain Backtracking (Same as Demo) ---

# [cite: 135] plain steps = 0
plain_steps = 0

# [cite: 136] def backtrack_plain(assignment):
def backtrack_plain(assignment):
    global plain_steps # [cite: 137]
    plain_steps += 1 # [cite: 138]
    
    # [cite: 139] if len(assignment) len(variables):
    if len(assignment) == len(variables):
        return assignment # [cite: 140]

    # [cite: 142] Pick first unassigned variable (no heuristic)
    var = None
    for v in variables:
        if v not in assignment:
            var = v
            break # [cite: 143]
    
    # [cite: 144] for value in colors: # try values in fixed order
    for value in colors:
        # [cite: 145] if is_valid(assignment, var, value):
        if is_valid(assignment, var, value):
            assignment[var] = value # [cite: 146]
            # [cite: 147] result backtrack_plain(assignment)
            result = backtrack_plain(assignment)
            if result:
                return result # [cite: 148]
            del assignment[var] # [cite: 149] #backtrack
            
    return None # [cite: 150]

# --- 5. Algorithm 2: Backtracking with MRV + LCV (Adapted from Demo) ---

# [cite: 285] heuristic steps = 0
heuristic_steps = 0
heuristic_log = [] # For storing MRV/LCV choices [cite: 19]

# [cite: 278] Minimum Remaining Values (MRV) heuristic
def select_mrv(assignment):
    # [cite: 279] unassigned [v for v in variables if v not in assignment]
    unassigned = [v for v in variables if v not in assignment]
    
    # [cite: 280] return min(unassigned, key lambda var: sum(is_valid(assignment, var, c) for c in colors))
    # This counts the number of *legal* values for each unassigned var
    return min(unassigned, 
               key=lambda var: sum(1 for c in colors if is_valid(assignment, var, c)))

# [cite: 281] Least Constraining Value (LCV) heuristic
def order_lcv(var, assignment):
    # This implementation is a standard LCV:
    # It counts, for each color, how many unassigned neighbors *could*
    # also take that color. We prefer the color that
    # conflicts with the *fewest* neighbor choices.
    color_conflicts = []
    for color in colors:
        if not is_valid(assignment, var, color):
            continue # Skip colors that are already illegal

        conflicts = 0
        for neighbor in neighbors[var]:
            if neighbor not in assignment:
                # Check if this color is *also* a legal move for the neighbor
                if is_valid(assignment, neighbor, color):
                    conflicts += 1
        color_conflicts.append((color, conflicts))
    
    # Sort by conflicts (ascending)
    color_conflicts.sort(key=lambda x: x[1])
    return [color for color, conflicts in color_conflicts]


# [cite: 287] def backtrack_heuristic(assignment):
def backtrack_heuristic(assignment):
    global heuristic_steps, heuristic_log # [cite: 288]
    heuristic_steps += 1 # [cite: 289]
    
    # [cite: 290] if len(assignment) len(variables):
    if len(assignment) == len(variables):
        return assignment # [cite: 292]

    # [cite: 293] var select_unassigned_var(assignment)
    var = select_mrv(assignment)
    
    # [cite: 19] Log the MRV choice
    heuristic_log.append(f"Step {heuristic_steps}: MRV selected = {var}")

    # [cite: 294] (logic for LCV)
    ordered_values = order_lcv(var, assignment)
    
    # [cite: 19] Log the LCV choice
    heuristic_log.append(f"  -> LCV order for {var}: {ordered_values}")

    # [cite: 298] for value in order_domain_values(var, assignment):
    for value in ordered_values:
        # [cite: 298] if is_valid(assignment, var, value):
        # We must re-check is_valid because LCV might return
        # a color that is valid for neighbors but not for us
        # (though our LCV implementation already filters this)
        if is_valid(assignment, var, value):
            assignment[var] = value # [cite: 298]
            
            # [cite: 299] result backtrack_heuristic(assignment)
            result = backtrack_heuristic(assignment)
            if result:
                return result # [cite: 300]
                
            del assignment[var] # [cite: 301] # backtrack
            
    return None # [cite: 302]

# --- 6. Algorithm 3: Backtracking with MRV + LCV + AC-3 ---
# (This part is new, as required by Lab Assignment 5, 
# but follows the same backtracking structure)

ac3_steps = 0
ac3_log = [] # For storing MRV/LCV choices [cite: 19]

def backtrack_ac3(assignment, domains):
    global ac3_steps, ac3_log
    ac3_steps += 1
    
    if len(assignment) == len(variables):
        return assignment

    # MRV: Select var with smallest domain
    unassigned = [v for v in variables if v not in assignment]
    var = min(unassigned, key=lambda v: len(domains[v]))
    
    # [cite: 19] Log the MRV choice
    ac3_log.append(f"Step {ac3_steps}: MRV selected = {var} (Domain size: {len(domains[var])})")

    # LCV: Order values by fewest conflicts with neighbor *domains*
    ordered_values = sorted(domains[var], 
                            key=lambda val: sum(1 for n in neighbors[var] 
                                                if n not in assignment and val in domains[n]))
    
    # [cite: 19] Log the LCV choice
    ac3_log.append(f"  -> LCV order for {var}: {ordered_values}")

    for value in ordered_values:
        assignment[var] = value
        
        # We need to copy domains to restore on failure
        domains_copy = deepcopy(domains)
        
        # Set the domain for the current var to just the chosen color
        domains[var] = {value}

        # Run AC-3 to propagate constraints (MAC)
        # We start the queue with all neighbors of our *current* var
        queue = [(neighbor, var) for neighbor in neighbors[var] if neighbor not in assignment]
        
        if ac3(domains, queue):
            result = backtrack_ac3(assignment, domains)
            if result:
                return result

        # Failure: backtrack
        del assignment[var]
        domains = domains_copy # Restore domains
            
    return None

def ac3(domains, queue):
    """
    AC-3 algorithm to enforce arc consistency.
    'queue' is an initial set of arcs (xi, xj) to check.
    """
    while queue:
        (xi, xj) = queue.pop(0)
        
        if revise(domains, xi, xj):
            if not domains[xi]: # Domain is empty
                return False # Failure
            
            # If we revised xi, we must re-check all neighbors of xi
            for xk in neighbors[xi]:
                if xk != xj:
                    queue.append((xk, xi))
    return True

def revise(domains, xi, xj):
    """Helper for AC-3. Returns true if domains[xi] was revised."""
    revised = False
    colors_to_remove = set()
    
    for color_x in domains[xi]:
        # Check if there's any color_y in xj's domain that supports color_x
        supported = False
        for color_y in domains[xj]:
            if color_x != color_y:
                supported = True
                break
        
        if not supported:
            colors_to_remove.add(color_x)
            revised = True
    
    domains[xi] -= colors_to_remove
    return revised


# --- 7. Main Execution Block (Similar to Demo) ---

# [cite: 191] if __name__ == "__main__":
if __name__ == "__main__":
    
    # --- Setup Graph for Visualization ---
    # We do this once, as it's the same for all solutions
    # [cite: 154] G = nx.Graph()
    G = nx.Graph()
    # [cite: 160] for var in variables: G.add_node (var)
    for var in variables:
        G.add_node(var)
    # [cite: 162] for var, neighs in neighbors.items():
    for var, neighs in neighbors.items():
        for n in neighs:
            G.add_edge(var, n) # [cite: 164]
            
    # [cite: 166] Create a layout. We use kamada_kawai_layout
    # as a 29-node manual layout is impractical.
    print("Calculating graph layout...")
    pos = nx.kamada_kawai_layout(G)
    print("Layout calculated. Starting solvers...\n")

    # --- 1. Plain Backtracking ---
    print("--- 1. Solving with Plain Backtracking ---")
    start_time = time.time()
    # [cite: 195] plain solution backtrack_plain({})
    plain_solution = backtrack_plain({})
    time_plain = time.time() - start_time
    
    # [cite: 196] print("Plain Backtracking Solution:", plain_solution)
    print("Plain Backtracking Solution:", plain_solution)
    # [cite: 197] print("Plain Backtracking Steps:", plain_steps)
    print(f"Plain Backtracking Steps: {plain_steps}")
    print(f"Time Taken: {time_plain:.4f} seconds\n")
    # [cite: 198] visualize_coloring(plain_solution, f"Plain Backtracking ( plain_steps steps)")
    visualize_coloring(
        plain_solution, 
        f"Plain Backtracking ({plain_steps} steps)",
        G, pos
    )

    # --- 2. Backtracking with MRV + LCV ---
    print("--- 2. Solving with Backtracking + MRV + LCV ---")
    start_time = time.time()
    # [cite: 306] heuristic_solution = backtrack_heuristic({})
    heuristic_solution = backtrack_heuristic({})
    time_heuristic = time.time() - start_time
    
    # [cite: 308] print("Backtracking with MRV + LCV Solution:", heuristic_solution)
    print("Backtracking with MRV + LCV Solution:", heuristic_solution)
    # [cite: 308] print("Backtracking with MRV + LCV Steps:", heuristic_steps)
    print(f"Backtracking with MRV + LCV Steps: {heuristic_steps}")
    print(f"Time Taken: {time_heuristic:.4f} seconds\n")
    
    # [cite: 89] Print the MRV/LCV log
    print("--- MRV/LCV Log (Heuristic) [First 20 lines] ---")
    for line in heuristic_log[:20]:
        print(line)
    print("... (log truncated) ...\n")
    
    # [cite: 309] visualize_coloring(heuristic_solution, f"MRV + LCV Heuristic ( heuristic_steps) steps)")
    visualize_coloring(
        heuristic_solution, 
        f"MRV + LCV Heuristic ({heuristic_steps} steps)",
        G, pos
    )

    # --- 3. Backtracking with MRV + LCV + AC-3 ---
    print("--- 3. Solving with Backtracking + MRV + LCV + AC-3 ---")
    # Initialize domains for all variables
    initial_domains = {var: set(colors) for var in variables}
    start_time = time.time()
    
    ac3_solution = backtrack_ac3({}, initial_domains)
    time_ac3 = time.time() - start_time
    
    print("Backtracking + AC-3 Solution:", ac3_solution)
    print(f"Backtracking + AC-3 Steps: {ac3_steps}")
    print(f"Time Taken: {time_ac3:.4f} seconds\n")

    # [cite: 89] Print the MRV/LCV log
    print("--- MRV/LCV Log (AC-3) [First 20 lines] ---")
    for line in ac3_log[:20]:
        print(line)
    print("... (log truncated) ...\n")

    visualize_coloring(
        ac3_solution, 
        f"MRV + LCV + AC-3 ({ac3_steps} steps)",
        G, pos
    )

    # --- 4. Final Comparison Table [cite: 90] ---
    print("--- 📊 Final Comparison ---")
    print(f"{'Algorithm':<35} | {'Steps Explored':<15} | {'Time (seconds)':<15}")
    print("-" * 68)
    print(f"{'1. Plain Backtracking':<35} | {plain_steps:<15} | {time_plain:<15.4f}")
    print(f"{'2. Backtracking + MRV/LCV':<35} | {heuristic_steps:<15} | {time_heuristic:<15.4f}")
    print(f"{'3. Backtracking + MRV/LCV + AC-3':<35} | {ac3_steps:<15} | {time_ac3:<15.4f}")