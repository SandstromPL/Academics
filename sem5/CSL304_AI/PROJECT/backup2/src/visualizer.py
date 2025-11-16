"""
Visualization Module
Displays warehouse simulation using Matplotlib
"""

import matplotlib.pyplot as plt
import matplotlib.patches as patches
from matplotlib.animation import FuncAnimation
import numpy as np
from typing import List, Tuple

from .warehouse import Warehouse, CellType
from .robot import Robot


class WarehouseVisualizer:
    """Visualize warehouse simulation using Matplotlib"""
    
    def __init__(self, warehouse: Warehouse, robots: List[Robot], cell_size: int = 30):
        self.warehouse = warehouse
        self.robots = robots
        self.cell_size = cell_size
        
        # Colors
        self.colors = {
            'empty': '#FFFFFF',
            'obstacle': '#2C3E50',
            'package': '#F39C12',
            'drop_zone': '#27AE60',
            'robot': ['#E74C3C', '#3498DB', '#9B59B6', '#E67E22', '#1ABC9C', 
                     '#D35400', '#C0392B', '#8E44AD', '#2980B9', '#16A085'],
            'path': '#BDC3C7',
            'grid_line': '#ECF0F1'
        }
        
        # Setup figure
        self.fig, (self.ax_main, self.ax_stats) = plt.subplots(1, 2, figsize=(16, 8),
                                                                gridspec_kw={'width_ratios': [3, 1]})
        self.fig.suptitle('Multi-Agent Warehouse Robot Simulator', fontsize=16, fontweight='bold')
        
        self._setup_main_axes()
        self._setup_stats_axes()
        
        # Animation state
        self.step_count = 0
        self.running = True
    
    def _setup_main_axes(self):
        """Setup main warehouse display"""
        self.ax_main.set_xlim(-0.5, self.warehouse.width - 0.5)
        self.ax_main.set_ylim(-0.5, self.warehouse.height - 0.5)
        self.ax_main.set_aspect('equal')
        self.ax_main.set_title('Warehouse Grid', fontsize=14, fontweight='bold')
        self.ax_main.set_xlabel('X')
        self.ax_main.set_ylabel('Y')
        self.ax_main.invert_yaxis()  # Invert Y-axis for matrix-like display
        
        # Grid lines
        for i in range(self.warehouse.width + 1):
            self.ax_main.axvline(i - 0.5, color=self.colors['grid_line'], linewidth=0.5)
        for i in range(self.warehouse.height + 1):
            self.ax_main.axhline(i - 0.5, color=self.colors['grid_line'], linewidth=0.5)
    
    def _setup_stats_axes(self):
        """Setup statistics display"""
        self.ax_stats.axis('off')
        self.stats_text = self.ax_stats.text(0.05, 0.98, '', transform=self.ax_stats.transAxes,
                                             fontsize=9, verticalalignment='top',
                                             fontfamily='monospace')
    
    def _draw_warehouse(self):
        """Draw warehouse grid with obstacles, packages, and drop zones"""
        self.ax_main.clear()
        self._setup_main_axes()
        
        # Draw obstacles
        for (x, y) in self.warehouse.obstacles:
            rect = patches.Rectangle((x - 0.4, y - 0.4), 0.8, 0.8,
                                     linewidth=1, edgecolor='black',
                                     facecolor=self.colors['obstacle'])
            self.ax_main.add_patch(rect)
        
        # Draw parking zones (light gray background)
        for (x, y) in self.warehouse.parking_zones:
            rect = patches.Rectangle((x - 0.48, y - 0.48), 0.96, 0.96,
                                     linewidth=1, edgecolor='gray',
                                     facecolor='lightgray', alpha=0.2)
            self.ax_main.add_patch(rect)
        
        # Draw drop zones
        for (x, y) in self.warehouse.drop_zones:
            rect = patches.Rectangle((x - 0.45, y - 0.45), 0.9, 0.9,
                                     linewidth=2, edgecolor=self.colors['drop_zone'],
                                     facecolor=self.colors['drop_zone'], alpha=0.3)
            self.ax_main.add_patch(rect)
            self.ax_main.text(x, y, 'D', ha='center', va='center',
                            fontsize=12, fontweight='bold', color='white')
        
        # Draw packages (not picked up and not delivered)
        for package in self.warehouse.packages:
            if not package.picked_up and not package.delivered and package.position is not None:
                x, y = package.position
                rect = patches.Rectangle((x - 0.35, y - 0.35), 0.7, 0.7,
                                         linewidth=2, edgecolor='black',
                                         facecolor=self.colors['package'])
                self.ax_main.add_patch(rect)
                self.ax_main.text(x, y, f'P{package.id}', ha='center', va='center',
                                fontsize=8, fontweight='bold')
    
    def _draw_robots(self):
        """Draw robots with their paths"""
        for i, robot in enumerate(self.robots):
            color = self.colors['robot'][i % len(self.colors['robot'])]
            x, y = robot.position
            
            # Draw robot path (if exists)
            if robot.path and len(robot.path) > 1:
                path_x = [p[0] for p in robot.path[robot.path_index:]]
                path_y = [p[1] for p in robot.path[robot.path_index:]]
                self.ax_main.plot(path_x, path_y, '--', color=color, alpha=0.3, linewidth=2)
            
            # Draw robot
            circle = patches.Circle((x, y), 0.35, linewidth=2, edgecolor='black',
                                   facecolor=color, zorder=10)
            self.ax_main.add_patch(circle)
            
            # Robot label
            label = f'R{robot.id}'
            if robot.carrying_package:
                label += f'\n(P{robot.carrying_package.id})'
            
            self.ax_main.text(x, y, label, ha='center', va='center',
                            fontsize=8, fontweight='bold', color='white', zorder=11)
    
    def _update_statistics(self):
        """Update statistics display"""
        warehouse_stats = self.warehouse.get_statistics()
        
        stats_str = f"""
╔════════════════════════════╗
║   SIMULATION STATISTICS    ║
╚════════════════════════════╝

⏱  Step: {self.step_count}

📦 PACKAGES:
   Total: {warehouse_stats['total_packages']} | Delivered: {warehouse_stats['delivered_packages']}
   In Transit: {warehouse_stats['picked_packages'] - warehouse_stats['delivered_packages']} | Remaining: {warehouse_stats['total_packages'] - warehouse_stats['picked_packages']}

🤖 ROBOTS:
"""
        
        for robot in self.robots:
            robot_stats = robot.get_statistics()
            state_abbrev = robot_stats['state'][:4]  # Abbreviate state
            stats_str += f"   R{robot.id}: {state_abbrev} | D:{robot_stats['packages_delivered']} Dist:{robot_stats['distance_traveled']} C:{robot_stats['conflicts_resolved']}\n"
        
        # AI Techniques Used
        all_algorithms = set()
        for robot in self.robots:
            all_algorithms.update(robot.search_algorithm_used)
        
        if all_algorithms:
            stats_str += f"\n🧠 AI: {', '.join(sorted(all_algorithms))}\n"
        
        stats_str += f"\n🎯 Progress: {warehouse_stats['delivered_packages']}/{warehouse_stats['total_packages']} "
        stats_str += f"({100 * warehouse_stats['delivered_packages'] / max(1, warehouse_stats['total_packages']):.1f}%)"
        
        self.stats_text.set_text(stats_str)
    
    def draw_frame(self):
        """Draw a single frame of the simulation"""
        self._draw_warehouse()
        self._draw_robots()
        self._update_statistics()
        plt.draw()
        plt.pause(0.01)
    
    def animate(self, frame):
        """Animation update function"""
        if not self.running:
            return
        
        self.step_count = frame
        self.draw_frame()
    
    def show(self, interactive: bool = False):
        """Show the visualization"""
        if interactive:
            plt.ion()
            self.draw_frame()
            plt.show(block=False)
        else:
            plt.show()
    
    def save_frame(self, filename: str):
        """Save current frame as image"""
        self.draw_frame()
        plt.savefig(filename, dpi=150, bbox_inches='tight')
    
    def close(self):
        """Close the visualization"""
        plt.close(self.fig)


class SimpleVisualizer:
    """Simple text-based visualization for terminal"""
    
    def __init__(self, warehouse: Warehouse, robots: List[Robot]):
        self.warehouse = warehouse
        self.robots = robots
        self.step_count = 0
    
    def draw(self):
        """Draw warehouse in terminal"""
        print("\n" + "=" * 80)
        print(f"STEP {self.step_count} - Warehouse Simulation")
        print("=" * 80)
        
        # Create display grid
        grid = [['.' for _ in range(self.warehouse.width)] for _ in range(self.warehouse.height)]
        
        # Add obstacles
        for (x, y) in self.warehouse.obstacles:
            grid[y][x] = '█'
        
        # Add drop zones
        for (x, y) in self.warehouse.drop_zones:
            grid[y][x] = 'D'
        
        # Add packages
        for pkg in self.warehouse.packages:
            if not pkg.picked_up and pkg.position is not None:
                x, y = pkg.position
                grid[y][x] = f'{pkg.id}'
        
        # Add robots
        for robot in self.robots:
            x, y = robot.position
            if robot.carrying_package:
                grid[y][x] = f'R{robot.id}({robot.carrying_package.id})'
            else:
                grid[y][x] = f'R{robot.id}'
        
        # Print grid
        for row in grid:
            print(' '.join(f'{cell:^4}' for cell in row))
        
        # Print statistics
        print("\n" + "-" * 80)
        stats = self.warehouse.get_statistics()
        print(f"Packages: {stats['delivered_packages']}/{stats['total_packages']} delivered")
        
        for robot in self.robots:
            print(f"Robot {robot.id}: {robot.state.value} - Distance: {robot.total_distance_traveled}")
        
        print("-" * 80)
        
        self.step_count += 1
    
    def show(self):
        """Display in terminal"""
        self.draw()


def create_visualizer(warehouse: Warehouse, robots: List[Robot], 
                     mode: str = 'matplotlib') -> WarehouseVisualizer:
    """
    Create appropriate visualizer
    
    Args:
        warehouse: Warehouse environment
        robots: List of robots
        mode: 'matplotlib' or 'simple'
    
    Returns:
        Visualizer instance
    """
    if mode == 'matplotlib':
        return WarehouseVisualizer(warehouse, robots)
    elif mode == 'simple':
        return SimpleVisualizer(warehouse, robots)
    else:
        raise ValueError(f"Unknown visualization mode: {mode}")
