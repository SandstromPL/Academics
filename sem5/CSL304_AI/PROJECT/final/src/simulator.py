"""
Warehouse Robot Simulator
Main simulation logic that orchestrates all components
"""

import time
from typing import List, Optional
import sys

from .warehouse import Warehouse
from .robot import Robot, RobotState
from .csp import ConstraintSatisfaction
from .visualizer import create_visualizer


class Simulator:
    """Main warehouse robot simulator"""
    
    def __init__(self, width: int = 20, height: int = 20,
                 num_robots: int = 3, num_packages: int = 5,
                 num_obstacles: int = 30, num_drop_zones: int = 2,
                 max_steps: int = 1000, visualization: str = 'matplotlib',
                 use_adversarial_search: bool = True):
        """
        Initialize simulator
        
        Args:
            width: Warehouse width
            height: Warehouse height
            num_robots: Number of robots
            num_packages: Number of packages
            num_obstacles: Number of obstacles
            num_drop_zones: Number of drop zones
            max_steps: Maximum simulation steps
            visualization: Visualization mode ('matplotlib', 'simple', 'none')
            use_adversarial_search: Use minimax for conflict resolution vs priority-based
        """
        # Create warehouse
        self.warehouse = Warehouse(width, height, num_obstacles, num_packages, num_drop_zones)
        
        # Create robots
        self.robots: List[Robot] = []
        for i in range(num_robots):
            position = self.warehouse.get_free_position()
            if position:
                robot = Robot(i, position, self.warehouse)
                robot.use_adversarial_search = use_adversarial_search
                self.robots.append(robot)
        
        # Set all_robots reference for each robot (for package priority checking)
        for robot in self.robots:
            robot.all_robots = self.robots
        
        # Simulation parameters
        self.max_steps = max_steps
        self.current_step = 0
        self.running = False
        self.visualization_mode = visualization
        
        # Create visualizer
        if visualization != 'none':
            self.visualizer = create_visualizer(self.warehouse, self.robots, visualization)
        else:
            self.visualizer = None
        
        # Statistics
        self.total_time = 0
        self.assignment_method = 'csp'
    
    def _assign_packages_to_robots(self):
        """Assign packages to available robots using CSP"""
        # During cleanup phase, don't assign new packages - let robots park
        if hasattr(self, 'completion_step'):
            return
        
        # Get available robots (idle and not carrying)
        available_robots = {r.id: r.position for r in self.robots if r.is_available()}
        
        if not available_robots:
            return
        
        # Get unassigned packages
        unassigned_packages = self.warehouse.get_unassigned_packages()
        
        if not unassigned_packages:
            return
        
        # Use CSP to assign packages
        assignment = ConstraintSatisfaction.assign_packages(
            available_robots,
            unassigned_packages,
            method=self.assignment_method
        )
        
        # Assign packages to robots
        for robot_id, package_id in assignment.items():
            if package_id is not None:
                robot = next(r for r in self.robots if r.id == robot_id)
                package = next(p for p in unassigned_packages if p.id == package_id)
                robot.assign_package(package)
                print(f"[CSP] Assigned Package {package_id} to Robot {robot_id}")
    
    def step(self) -> bool:
        """
        Execute one simulation step
        
        Returns:
            True if simulation should continue, False if complete
        """
        # Assign packages to idle robots (only if packages not all delivered)
        if not self.warehouse.all_packages_delivered():
            self._assign_packages_to_robots()
        
        # Update each robot
        for robot in self.robots:
            robot.step()
        
        # Increment step counter AFTER robot movement
        self.current_step += 1
        
        # Check if all packages delivered (after movement and increment)
        if self.warehouse.all_packages_delivered():
            # Check if we already recorded completion step
            if not hasattr(self, 'completion_step'):
                self.completion_step = self.current_step
                print(f"\nAll packages delivered in {self.completion_step} steps!")
                print(f"Sending all robots to parking zone...")
            
            # Check if all robots are parked (in parking zone or idle)
            all_parked = all(
                robot.state == RobotState.IDLE or 
                (robot.state == RobotState.PARKING and self.warehouse.is_parking_zone(robot.position))
                for robot in self.robots
            )
            
            if all_parked:
                print(f"All robots parked! Cleanup completed in {self.current_step - self.completion_step} additional steps.")
                return False
            
            # Continue running to let robots park (but don't count towards delivery time)
            # Set a safety limit for parking
            if self.current_step - self.completion_step > 50:
                print(f"Parking timeout - some robots couldn't reach parking zone")
                return False
        
        # Check max steps
        if self.current_step >= self.max_steps:
            print(f"\nMaximum steps ({self.max_steps}) reached!")
            return False
        
        # Update visualization
        if self.visualizer:
            if self.visualization_mode == 'matplotlib':
                self.visualizer.step_count = self.current_step
                self.visualizer.draw_frame()
            elif self.visualization_mode == 'simple':
                if self.current_step % 10 == 0:  # Update every 10 steps for terminal
                    self.visualizer.step_count = self.current_step
                    self.visualizer.draw()
        
        return True
    
    def run(self, step_delay: float = 0.1, interactive: bool = False):
        """
        Run the simulation
        
        Args:
            step_delay: Delay between steps in seconds
            interactive: Whether to run in interactive mode
        """
        print("\n" + "=" * 80)
        print("MULTI-AGENT WAREHOUSE ROBOT SIMULATOR")
        print("=" * 80)
        print(f"Warehouse: {self.warehouse.width}x{self.warehouse.height}")
        print(f"Robots: {len(self.robots)}")
        print(f"Packages: {len(self.warehouse.packages)}")
        print(f"Obstacles: {len(self.warehouse.obstacles)}")
        print(f"Drop Zones: {len(self.warehouse.drop_zones)}")
        print("=" * 80 + "\n")
        
        # Show initial state
        if self.visualizer:
            if self.visualization_mode == 'matplotlib':
                self.visualizer.show(interactive=True)
        
        self.running = True
        start_time = time.time()
        
        try:
            while self.running:
                if not self.step():
                    break
                
                if step_delay > 0:
                    time.sleep(step_delay)
        
        except KeyboardInterrupt:
            print("\n\nSimulation interrupted by user")
        
        finally:
            self.running = False
            self.total_time = time.time() - start_time
            self._print_final_statistics()
            
            if self.visualizer and self.visualization_mode == 'matplotlib':
                input("\nPress Enter to close visualization...")
                self.visualizer.close()
    
    def run_batch(self, num_runs: int = 10) -> dict:
        """
        Run multiple simulations and collect statistics
        
        Args:
            num_runs: Number of simulation runs
        
        Returns:
            Dictionary of aggregate statistics
        """
        results = {
            'completed': 0,
            'total_steps': [],
            'total_distances': [],
            'packages_delivered': []
        }
        
        for run in range(num_runs):
            print(f"\n--- Run {run + 1}/{num_runs} ---")
            
            # Reset simulation
            self.__init__(
                self.warehouse.width, self.warehouse.height,
                len(self.robots), len(self.warehouse.packages),
                len(self.warehouse.obstacles), len(self.warehouse.drop_zones),
                self.max_steps, visualization='none'
            )
            
            # Run simulation
            while self.step() and self.current_step < self.max_steps:
                pass
            
            # Collect statistics
            if self.warehouse.all_packages_delivered():
                results['completed'] += 1
            
            results['total_steps'].append(self.current_step)
            results['total_distances'].append(sum(r.total_distance_traveled for r in self.robots))
            results['packages_delivered'].append(
                sum(1 for p in self.warehouse.packages if p.delivered)
            )
        
        return results
    
    def _print_final_statistics(self):
        """Print final simulation statistics"""
        print("\n" + "=" * 80)
        print("FINAL STATISTICS")
        print("=" * 80)
        
        warehouse_stats = self.warehouse.get_statistics()
        
        print(f"\nSimulation Time: {self.total_time:.2f} seconds")
        
        # Show delivery steps vs total steps if cleanup phase occurred
        if hasattr(self, 'completion_step'):
            print(f"Delivery Steps: {self.completion_step} (packages delivered)")
            parking_steps = self.current_step - self.completion_step
            print(f"Parking Steps: {parking_steps} (robots returning to base)")
            print(f"Total Steps: {self.current_step}")
        else:
            print(f"Total Steps: {self.current_step}")
        print(f"\nPACKAGE STATISTICS:")
        print(f"   • Total Packages: {warehouse_stats['total_packages']}")
        print(f"   • Delivered: {warehouse_stats['delivered_packages']}")
        print(f"   • Success Rate: {100 * warehouse_stats['delivered_packages'] / warehouse_stats['total_packages']:.1f}%")
        
        print(f"\nROBOT STATISTICS:")
        total_distance = 0
        total_conflicts = 0
        total_blocked = 0
        
        for robot in self.robots:
            stats = robot.get_statistics()
            total_distance += stats['distance_traveled']
            total_conflicts += stats['conflicts_resolved']
            total_blocked += stats['blocked_count']
            
            print(f"\n   Robot {robot.id}:")
            print(f"      • Packages Delivered: {stats['packages_delivered']}")
            print(f"      • Distance Traveled: {stats['distance_traveled']}")
            print(f"      • Conflicts Resolved: {stats['conflicts_resolved']}")
            print(f"      • Times Blocked: {stats['blocked_count']}")
            print(f"      • Final State: {stats['state']}")
        
        print(f"\n   TOTALS:")
        print(f"      • Total Distance: {total_distance}")
        print(f"      • Total Conflicts: {total_conflicts}")
        print(f"      • Total Blocks: {total_blocked}")
        print(f"      • Avg Distance/Robot: {total_distance / len(self.robots):.1f}")
        
        # AI Techniques Summary
        all_techniques = set()
        for robot in self.robots:
            all_techniques.update(robot.search_algorithm_used)
        
        print(f"\nAI TECHNIQUES USED:")
        for technique in sorted(all_techniques):
            print(f"      • {technique}")
        
        print("\n" + "=" * 80)
    
    def get_statistics(self) -> dict:
        """Get current simulation statistics"""
        return {
            'step': self.current_step,
            'time': self.total_time,
            'warehouse': self.warehouse.get_statistics(),
            'robots': [r.get_statistics() for r in self.robots]
        }


def run_simulation(width: int = 20, height: int = 20,
                  num_robots: int = 3, num_packages: int = 5,
                  visualization: str = 'matplotlib',
                  step_delay: float = 0.1):
    """
    Convenience function to run a simulation
    
    Args:
        width: Warehouse width
        height: Warehouse height
        num_robots: Number of robots
        num_packages: Number of packages
        visualization: Visualization mode
        step_delay: Delay between steps
    """
    sim = Simulator(width, height, num_robots, num_packages,
                   visualization=visualization)
    sim.run(step_delay=step_delay, interactive=True)
    return sim
