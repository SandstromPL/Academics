# Multi-Agent Warehouse Robot Simulator - Project Structure

## 📁 Directory Layout

```
PROJECT/
├── README.md                      # Project overview and features
├── QUICKSTART.md                  # Quick installation and usage guide
├── AI_TECHNIQUES_EXPLAINED.md     # Detailed AI algorithms documentation
├── main.py                        # Main entry point for simulation
├── setup.sh                       # Setup script for installation
├── requirements.txt               # Python dependencies
├── .gitignore                     # Git ignore file
│
└── src/                           # Source code modules
    ├── __init__.py                # Package initialization
    ├── warehouse.py               # Grid environment and package management
    ├── robot.py                   # Autonomous robot agent with AI
    ├── simulator.py               # Simulation orchestration
    ├── visualizer.py              # Matplotlib visualization
    ├── uninformed_search.py       # BFS, DFS, UCS, IDDFS algorithms
    ├── informed_search.py         # A* with multiple heuristics
    ├── local_search.py            # Hill Climbing, Simulated Annealing
    ├── adversarial_search.py      # Minimax, Alpha-Beta, Expectimax
    └── csp.py                     # Constraint Satisfaction for task allocation
```

## Core Modules

### warehouse.py
- **Purpose**: Manages warehouse grid environment
- **Key Classes**: `Warehouse`, `Package`, `CellType`
- **Features**: 
  - Grid management with obstacles, packages, drop zones
  - Parking zones for idle robots
  - Dynamic package tracking and removal

### robot.py
- **Purpose**: Autonomous robot agent with AI decision-making
- **Key Classes**: `Robot`, `RobotState`
- **Features**:
  - Multi-state FSM (idle, moving, picking, dropping, parking, blocked)
  - Package priority system (robots WITH packages > robots WITHOUT)
  - Oscillation detection and escape
  - Conflict resolution with priority-based yielding
  - Parking zone management

### simulator.py
- **Purpose**: Orchestrates multi-robot simulation
- **Key Classes**: `WarehouseSimulator`
- **Features**:
  - Multi-robot coordination
  - Package assignment using CSP
  - Statistics tracking
  - Step-by-step execution

### visualizer.py
- **Purpose**: Real-time visualization
- **Key Classes**: `WarehouseVisualizer`, `SimpleVisualizer`
- **Features**:
  - Matplotlib GUI with grid display
  - Real-time statistics panel (compact format)
  - Color-coded robots, packages, obstacles, drop zones, parking areas

## AI Technique Modules

### uninformed_search.py 
- **Algorithms**: BFS, DFS, UCS, IDDFS
- **Use Case**: Basic pathfinding, fallback for complex scenarios

### informed_search.py 
- **Algorithms**: A* with Manhattan, Euclidean, Chebyshev heuristics
- **Use Case**: Primary pathfinding with optimal paths

### local_search.py
- **Algorithms**: Hill Climbing, Simulated Annealing
- **Use Case**: Path optimization, local improvements

### adversarial_search.py 
- **Algorithms**: Minimax, Alpha-Beta Pruning, Expectimax
- **Use Case**: Conflict resolution, multi-agent decision making

### csp.py 
- **Algorithms**: Backtracking with MRV, LCV heuristics
- **Use Case**: Optimal package-to-robot task allocation


## Entry Points

### main.py
- Primary command-line interface
- Configurable parameters (grid size, robots, packages, obstacles)
- Example: `python main.py --width 30 --height 30 --robots 10 --packages 20`

## 🔧 Configuration Files

### requirements.txt
```
numpy>=1.24.0
matplotlib>=3.7.0
colorama>=0.4.6
```

### .gitignore
- Excludes: `venv/`, `__pycache__/`, `*.pyc`, `*.pyo`, `.DS_Store`

## ✨ Key Features Implemented

1. **Package Priority System**: Robots with packages get right-of-way
2. **Parking Zones**: Idle robots move to designated parking area (5x5 corner)
3. **Interior Parking Priority**: Robots fill parking from inside out
4. **Conflict-Free Parking**: Robots dynamically choose alternative spots
5. **Oscillation Detection**: Tracks position history, escapes loops
6. **Dynamic Obstacle Avoidance**: Real-time path replanning around other robots
7. **Drop Zone Congestion Handling**: Priority-based waiting for deliveries
8. **Compact Statistics Display**: Fits all robot data in visualization panel

## 📈 Performance Characteristics

- **Success Rate**: 100% delivery completion in all test cases
- **Scalability**: Tested up to 50x50 grids, 20 robots, 50 packages
- **Efficiency**: Typical completion in 80-150 steps for medium scenarios
- **Conflict Resolution**: Zero deadlocks with priority system

## 🎓 Academic Context

**Course**: CSL304 - Artificial Intelligence  
**Institution**: IIT Bhilai  
**Project Type**: Multi-Agent System with AI Techniques Integration  
**Semester**: 5 (2024-25)
