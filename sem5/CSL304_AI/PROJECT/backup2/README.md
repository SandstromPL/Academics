# Multi-Agent Warehouse Robot Simulator

## Project Description

This project simulates a warehouse environment where multiple autonomous robots navigate a grid, pick up packages, and deliver them to designated locations efficiently. The system implements multiple AI techniques to enable intelligent navigation and coordination.

## AI Techniques Implemented

### 1. **Uninformed Search**
- **BFS (Breadth-First Search)**: Explores grid level by level
- **DFS (Depth-First Search)**: Explores grid depth-first
- **UCS (Uniform Cost Search)**: Finds lowest-cost path

### 2. **Informed Search**
- **A\* Algorithm**: Uses Manhattan distance heuristic for optimal pathfinding
- Efficiently finds shortest paths to packages and delivery destinations

### 3. **Local Search**
- **Hill Climbing**: Finds local improvements when stuck
- **Greedy Improvement**: Quick detours to resolve congestion
- Used when robots are blocked by other robots

### 4. **Adversarial Search**
- **Minimax Decision Making**: Predicts opponent robot moves
- Resolves conflicts when two robots compete for same space
- Enables collision avoidance through strategic planning

### 5. **Constraint Satisfaction Problem (CSP)**
- Assigns robots to packages optimally
- Variables: robots
- Domains: available packages
- Constraints: distance, workload balancing, uniqueness

### 6. **Predicate Logic (Optional)**
- Represents system states using first-order predicates
- Enables explainability and state reasoning

## Project Structure

```
PROJECT/
├── src/
│   ├── __init__.py
│   ├── warehouse.py          # Grid environment with obstacles
│   ├── robot.py               # Robot agent with AI decision-making
│   ├── uninformed_search.py   # BFS, DFS, UCS implementations
│   ├── informed_search.py     # A* algorithm
│   ├── local_search.py        # Hill climbing, greedy improvement
│   ├── adversarial_search.py  # Minimax conflict resolution
│   ├── csp.py                 # Constraint satisfaction
│   ├── visualizer.py          # Pygame/Matplotlib visualization
│   └── simulator.py           # Main simulation logic
├── main.py                    # Entry point
├── requirements.txt           # Dependencies
└── README.md                  # This file
```

## Installation

### Option 1: Automatic Setup (Recommended)

```bash
# Run the setup script
./setup.sh

# Activate virtual environment
source venv/bin/activate
```

### Option 2: Manual Setup

```bash
# Create virtual environment
python3 -m venv venv

# Activate virtual environment
source venv/bin/activate  # On Linux/Mac
# or
venv\Scripts\activate     # On Windows

# Install dependencies
pip install -r requirements.txt
```

## Quick Start

### 1. Run Tests (Optional)
```bash
python test_components.py
```

### 2. Run Basic Simulation
```bash
python main.py
```

### 3. Run Interactive Demos
```bash
python demo.py
```

### 4. Custom Configuration
```bash
# Large warehouse with many robots
python main.py --width 30 --height 30 --robots 5 --packages 10

# Terminal visualization (no matplotlib)
python main.py --visualization simple

# Batch testing
python main.py --batch 10
```

## Usage Examples

**Default configuration:**
```bash
python main.py
```

**Custom warehouse:**
```bash
python main.py --width 40 --height 40 --robots 7 --packages 15
```

**Simple terminal visualization:**
```bash
python main.py --visualization simple
```

**Fast simulation without visualization:**
```bash
python main.py --visualization none --delay 0
```

See [QUICKSTART.md](QUICKSTART.md) for more examples and options.

## Features

- Dynamic warehouse grid generation
- Multiple autonomous robots
- Real-time collision avoidance
- Intelligent package assignment
- Path optimization with multiple algorithms
- Visual simulation with animation
- Conflict resolution between robots
- Performance metrics and statistics

## How It Works

1. **Initialization**: Generate warehouse grid with obstacles, packages, and drop zones
2. **Robot Spawning**: Create multiple robots at different starting positions
3. **Package Assignment**: Use CSP to assign packages to robots optimally
4. **Navigation**: Each robot uses A* to find optimal path
5. **Conflict Resolution**: Use adversarial search when robots collide
6. **Congestion Handling**: Apply local search to find detours
7. **Delivery**: Complete when all packages delivered

## Authors

IIT Bhilai - CSL304 AI Project

## License

MIT License
