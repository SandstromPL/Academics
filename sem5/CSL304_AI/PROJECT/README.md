# Multi-Agent Warehouse Robot Simulator

## Project Information

**Course:** CSL304 - Artificial Intelligence  
**Institution:** Indian Institute of Technology (IIT) Bhilai  
**Semester:** 5 (2024-25)

### Group ID: 22
- **Paritosh Lahre** - 12341550
- **Agastya Nath** - 12340140
- **Y. Rahul Dev Reddy** - 12342390
- **Aarya Shadangule** - 12340020

---

## Project Overview

A sophisticated multi-agent warehouse automation system where autonomous robots coordinate to pick up and deliver packages efficiently. The simulator implements multiple AI search algorithms and conflict resolution strategies to handle complex scenarios with up to 25 robots operating simultaneously on large-scale warehouses (50×50 grids).

### Key Features
- **Multiple AI Search Algorithms:** A*, BFS, Minimax, CSP, Hill Climbing
- **Intelligent Conflict Resolution:** Game-theoretic decision making using Minimax
- **Dynamic Path Planning:** Real-time obstacle avoidance and replanning
- **Scalable Architecture:** Handles 25+ robots and 80+ packages simultaneously
- **Visual Feedback:** Real-time matplotlib visualization with statistics
- **Automated Parking:** Robots return to designated zones after task completion

---

## AI Concepts Used

### 1. Informed Search - A* Algorithm
- Primary pathfinding algorithm for all robot movements
- Uses Manhattan distance heuristic for optimal path calculation
- Ensures shortest collision-free paths in the warehouse grid

### 2. Uninformed Search - BFS (Breadth-First Search)
- Fallback algorithm when A* encounters complex obstacles
- Guarantees finding a path if one exists
- Used for systematic exploration of alternative routes

### 3. Adversarial Search - Minimax
- Game-theoretic conflict resolution between robots
- 2-step lookahead to predict and avoid collisions
- Evaluates multiple scenarios to make optimal decisions

### 4. Constraint Satisfaction Problem (CSP)
- Intelligent package-to-robot assignment
- Minimizes total Manhattan distance for efficient allocation
- Ensures balanced workload distribution among robots

### 5. Local Search - Hill Climbing
- Escapes deadlock situations through iterative improvement
- Finds detour paths when primary routes are blocked
- Handles dynamic environment changes adaptively

---

## Directory Structure

```
PROJECT/
├── src/                           # Source code directory
│   ├── __init__.py                # Package initializer
│   ├── warehouse.py               # Warehouse environment and grid management
│   ├── robot.py                   # Robot agent with AI decision-making
│   ├── simulator.py               # Simulation orchestration and control
│   ├── visualizer.py              # Matplotlib visualization engine
│   ├── informed_search.py         # A* algorithm implementation
│   ├── uninformed_search.py       # BFS, DFS, UCS algorithms
│   ├── adversarial_search.py      # Minimax conflict resolution
│   ├── csp.py                     # Constraint satisfaction solver
│   └── local_search.py            # Hill climbing for detours
│
├── main.py                        # Main entry point
├── requirements.txt               # Python dependencies
├── setup.sh                       # Quick setup script
│
├── README.md                      # This file
├── README_NEW.md                  # Detailed command reference
├── QUICKSTART.md                  # Quick start guide
├── AI_TECHNIQUES_EXPLAINED.md     # Detailed AI concepts documentation
├── ADVERSARIAL_INTEGRATION.md     # Minimax integration guide
└── PROJECT_STRUCTURE.md           # Architecture documentation
```

---

## Initial Setup

### Prerequisites
- Python 3.8 or higher
- pip (Python package manager)

### Installation Steps

**1. Clone or navigate to the project directory:**

```bash
cd /path/to/PROJECT
```

**2. Create a virtual environment (recommended):**

```bash
python3 -m venv venv
source venv/bin/activate  # On Linux/Mac
# OR
venv\Scripts\activate     # On Windows
```

**3. Install required dependencies:**

```bash
pip install -r requirements.txt
```

**Dependencies installed:**
- `numpy>=1.24.0` - Numerical computations
- `matplotlib>=3.7.0` - Visualization
- `colorama>=0.4.6` - Terminal colored output

**4. Verify installation:**

```bash
python3 -c "import numpy, matplotlib, colorama; print('All dependencies installed successfully!')"
```

---

## Sample Run - Moderate Test Case

### Running with Matplotlib and Minimax

Execute a moderate-scale simulation with visual feedback:

```bash
python3 main.py --width 25 --height 25 --robots 8 --packages 15 \
                --obstacles 60 --visualization matplotlib \
                --delay 0.1 --conflict-resolution minimax
```

### What This Does:
- Creates a **25×25 warehouse** (625 cells)
- Deploys **8 autonomous robots**
- Distributes **15 packages** to deliver
- Places **60 obstacles** randomly
- Shows **live matplotlib visualization** with animated robots
- Uses **Minimax algorithm** for intelligent conflict resolution
- Updates every **0.1 seconds** for smooth animation

### Expected Output:

**Console:**
```
================================================================================
               MULTI-AGENT WAREHOUSE ROBOT SIMULATOR
                    IIT Bhilai - CSL304 AI Project
================================================================================

Conflict Resolution: MINIMAX
================================================================================

Warehouse: 25x25
Robots: 8
Packages: 15
...
All packages delivered in 142 steps!
...
AI TECHNIQUES USED:
      • astar
      • minimax
================================================================================
```

---

## Command-Line Flags Reference

### Warehouse Configuration

| Flag | Type | Default | Description |
|------|------|---------|-------------|
| `--width` | Integer | 20 | Warehouse width in cells |
| `--height` | Integer | 20 | Warehouse height in cells |
| `--obstacles` | Integer | 30 | Number of obstacle cells |
| `--drop-zones` | Integer | 2 | Number of delivery zones |

**Example:**

```bash
python3 main.py --width 30 --height 30 --obstacles 50
```

---

### Simulation Parameters

| Flag | Type | Default | Description |
|------|------|---------|-------------|
| `--robots` | Integer | 3 | Number of autonomous robots |
| `--packages` | Integer | 5 | Number of packages to deliver |
| `--max-steps` | Integer | 1000 | Maximum simulation steps |

**Example:**

```bash
python3 main.py --robots 10 --packages 20
```

---

### Visualization Options

| Flag | Values | Default | Description |
|------|--------|---------|-------------|
| `--visualization` | matplotlib / simple / none | matplotlib | Visualization mode |
| `--delay` | Float | 0.1 | Delay between steps (seconds) |

**Examples:**

```bash
# Graphical (recommended for ≤35×35)
python3 main.py --visualization matplotlib --delay 0.1

# Terminal ASCII (fast, any size)
python3 main.py --visualization simple --delay 0.05

# No visualization (maximum speed)
python3 main.py --visualization none --delay 0
```

---

### AI Strategy

| Flag | Values | Default | Description |
|------|--------|---------|-------------|
| `--conflict-resolution` | minimax / priority | minimax | Conflict resolution strategy |

**Examples:**

```bash
# Minimax (intelligent)
python3 main.py --conflict-resolution minimax

# Priority-based (fast)
python3 main.py --conflict-resolution priority
```

---

### Batch Testing

```bash
# Run 10 simulations and show statistics
python3 main.py --batch 10 --visualization none
```

---

## Complete Command Examples

### 1. Small Test (Quick Demo)

```bash
python3 main.py --width 15 --height 15 --robots 3 --packages 5 \
                --visualization matplotlib --delay 0.15
```

### 2. Moderate Test (Recommended)

```bash
python3 main.py --width 25 --height 25 --robots 8 --packages 15 \
                --obstacles 60 --visualization matplotlib \
                --delay 0.1 --conflict-resolution minimax
```

### 3. Large Scale Test

```bash
python3 main.py --width 50 --height 50 --robots 25 --packages 80 \
                --obstacles 200 --visualization simple \
                --delay 0.01 --conflict-resolution minimax
```

### 4. Performance Benchmark

```bash
python3 main.py --width 30 --height 30 --robots 10 --packages 20 \
                --batch 5 --visualization none
```

---

## Tips

1. **Start Small:** Begin with 15×15 grids
2. **Optimal Size:** 25×25 to 35×35 for matplotlib
3. **Large Grids:** Use `--visualization simple` for 40×40+
4. **Smooth Animation:** Use `--delay 0.1` or higher
5. **Stop Anytime:** Press `Ctrl+C` to terminate

---

## Troubleshooting

| Issue | Solution |
|-------|----------|
| Matplotlib freezes | Reduce grid to ≤35×35 or use `--visualization simple` |
| Too slow | Reduce `--delay` or use `--visualization none` |
| Import errors | Run `pip install -r requirements.txt` |

---

## Performance Benchmarks

| Grid | Robots | Packages | Time | Success |
|------|--------|----------|------|---------|
| 20×20 | 5 | 10 | 8.5s | 100% |
| 25×25 | 8 | 15 | 15.2s | 100% |
| 35×35 | 12 | 25 | 31.5s | 100% |
| 50×50 | 25 | 80 | 5.6s | 100% |

---

## Additional Documentation

- **PROJECT_STRUCTURE.md** - For quick view of directory structure
- **QUICKSTART.md** - Minimal setup guide
- **AI_TECHNIQUES_EXPLAINED.md** - Detailed AI algorithms
- **ADVERSARIAL_INTEGRATION.md** - Minimax implementation

---
