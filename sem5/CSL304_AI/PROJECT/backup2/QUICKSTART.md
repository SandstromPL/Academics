# Quick Start Guide

## Multi-Agent Warehouse Robot Simulator

### Installation

1. **Install Python Dependencies**
   ```bash
   pip install -r requirements.txt
   ```

2. **Verify Installation**
   ```bash
   python -c "import matplotlib; import numpy; print('✅ All dependencies installed')"
   ```

### Running the Simulator

#### Basic Usage

**Default simulation (matplotlib visualization):**
```bash
python main.py
```

**Custom configuration:**
```bash
python main.py --width 30 --height 30 --robots 5 --packages 10
```

#### Visualization Options

**Matplotlib (graphical):**
```bash
python main.py --visualization matplotlib
```

**Simple terminal display:**
```bash
python main.py --visualization simple
```

**No visualization (fastest):**
```bash
python main.py --visualization none --delay 0
```

#### Advanced Options

**Large warehouse:**
```bash
python main.py --width 40 --height 40 --robots 7 --packages 15 --obstacles 50
```

**Fast simulation:**
```bash
python main.py --delay 0.01
```

**Batch mode (run multiple simulations):**
```bash
python main.py --batch 10
```

### Running Demos

Interactive demo with preset configurations:
```bash
python demo.py
```

### Command-Line Arguments

```
--width N          Warehouse width (default: 20)
--height N         Warehouse height (default: 20)
--robots N         Number of robots (default: 3)
--packages N       Number of packages (default: 5)
--obstacles N      Number of obstacles (default: 30)
--drop-zones N     Number of drop zones (default: 2)
--max-steps N      Maximum simulation steps (default: 1000)
--visualization    Visualization mode: matplotlib, simple, none
--delay SECONDS    Delay between steps (default: 0.1)
--batch N          Run N simulations and show statistics
```

### Examples

**Small test scenario:**
```bash
python main.py --width 10 --height 10 --robots 2 --packages 3 --delay 0.2
```

**High-speed simulation:**
```bash
python main.py --visualization none --delay 0
```

**Performance testing:**
```bash
python main.py --batch 20 --visualization none
```

**Complex scenario:**
```bash
python main.py --width 50 --height 50 --robots 10 --packages 20 --obstacles 100
```

### AI Techniques Demonstrated

1. **Uninformed Search** - BFS, DFS, UCS for pathfinding
2. **Informed Search** - A* with Manhattan distance heuristic
3. **Local Search** - Hill climbing for congestion resolution
4. **Adversarial Search** - Minimax for conflict resolution
5. **Constraint Satisfaction** - CSP for package assignment
6. **Predicate Logic** - State representation (in code)

### Troubleshooting

**Issue: Matplotlib not displaying**
- Try: `python main.py --visualization simple`

**Issue: Simulation too slow**
- Try: `python main.py --delay 0.01`
- Or: `python main.py --visualization none`

**Issue: Import errors**
- Run: `pip install -r requirements.txt`

### Project Structure

```
PROJECT/
├── src/
│   ├── warehouse.py          # Warehouse environment
│   ├── robot.py               # Robot agent
│   ├── uninformed_search.py   # BFS, DFS, UCS
│   ├── informed_search.py     # A* algorithm
│   ├── local_search.py        # Hill climbing
│   ├── adversarial_search.py  # Minimax
│   ├── csp.py                 # Constraint satisfaction
│   ├── visualizer.py          # Visualization
│   └── simulator.py           # Main simulation
├── main.py                    # Entry point
├── demo.py                    # Demo scenarios
└── requirements.txt           # Dependencies
```

### Tips

- Start with small warehouse sizes to understand the system
- Use `--delay 0.2` or higher for better visualization
- Use `--batch` mode for performance analysis
- Press Ctrl+C to stop simulation at any time
- Matplotlib window must remain in focus for proper animation

### Support

For issues or questions, refer to the README.md or check the inline code documentation.
