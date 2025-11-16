"""
Warehouse Grid Environment
Manages the warehouse layout, obstacles, packages, and drop zones
"""

import random
from typing import List, Tuple, Set, Optional
from enum import Enum


class CellType(Enum):
    """Types of cells in the warehouse grid"""
    EMPTY = 0
    OBSTACLE = 1
    PACKAGE = 2
    DROP_ZONE = 3
    ROBOT = 4


class Package:
    """Represents a package in the warehouse"""
    def __init__(self, package_id: int, position: Tuple[int, int]):
        self.id = package_id
        self.position = position
        self.picked_up = False
        self.delivered = False
        self.assigned_robot = None
    
    def __repr__(self):
        return f"Package({self.id}, pos={self.position}, picked={self.picked_up}, delivered={self.delivered})"


class Warehouse:
    """Warehouse grid environment with obstacles, packages, and drop zones"""
    
    def __init__(self, width: int = 20, height: int = 20, 
                 num_obstacles: int = 30, num_packages: int = 5, num_drop_zones: int = 2):
        """
        Initialize warehouse grid
        
        Args:
            width: Grid width
            height: Grid height
            num_obstacles: Number of obstacles to place
            num_packages: Number of packages to place
            num_drop_zones: Number of drop zones to place
        """
        self.width = width
        self.height = height
        self.grid = [[CellType.EMPTY for _ in range(width)] for _ in range(height)]
        
        # Track positions
        self.obstacles: Set[Tuple[int, int]] = set()
        self.packages: List[Package] = []
        self.drop_zones: Set[Tuple[int, int]] = set()
        self.parking_zones: Set[Tuple[int, int]] = set()  # Where idle robots wait
        self.robot_positions: dict = {}  # robot_id -> position
        
        # Generate environment - parking zones first so other things avoid them
        self._place_parking_zones()  # Create parking area for idle robots FIRST
        self._place_obstacles(num_obstacles)
        self._place_drop_zones(num_drop_zones)
        self._place_packages(num_packages)
    
    def _place_obstacles(self, num_obstacles: int):
        """Place obstacles randomly on the grid (avoiding parking zones)"""
        placed = 0
        while placed < num_obstacles:
            x = random.randint(0, self.width - 1)
            y = random.randint(0, self.height - 1)
            
            # Don't place obstacles in parking area - keep it clear!
            if self.grid[y][x] == CellType.EMPTY and (x, y) not in self.parking_zones:
                self.grid[y][x] = CellType.OBSTACLE
                self.obstacles.add((x, y))
                placed += 1
    
    def _place_drop_zones(self, num_drop_zones: int):
        """Place drop zones on the grid (avoiding parking zones)"""
        placed = 0
        while placed < num_drop_zones:
            x = random.randint(0, self.width - 1)
            y = random.randint(0, self.height - 1)
            
            # Avoid parking zones for drop zones!
            if self.grid[y][x] == CellType.EMPTY and (x, y) not in self.parking_zones:
                self.grid[y][x] = CellType.DROP_ZONE
                self.drop_zones.add((x, y))
                placed += 1
    
    def _place_parking_zones(self):
        """Create parking zones in bottom-right corner for idle robots"""
        # Reserve a 5x5 area in the bottom-right corner as parking zone
        parking_size = min(5, self.width // 4, self.height // 4)  # Scale with warehouse size
        
        start_x = self.width - parking_size
        start_y = self.height - parking_size
        
        for x in range(start_x, self.width):
            for y in range(start_y, self.height):
                # Only mark as parking if it's currently empty
                if self.grid[y][x] == CellType.EMPTY:
                    self.parking_zones.add((x, y))
                    # Don't change grid type - keep as EMPTY so robots can move there
        
        print(f"[Warehouse] Created parking zone: {len(self.parking_zones)} spots in corner ({start_x}-{self.width-1}, {start_y}-{self.height-1})")
    
    def _place_packages(self, num_packages: int):
        """Place packages on the grid (avoiding parking zones)"""
        placed = 0
        while placed < num_packages:
            x = random.randint(0, self.width - 1)
            y = random.randint(0, self.height - 1)
            
            # Avoid parking zones for packages!
            if self.grid[y][x] == CellType.EMPTY and (x, y) not in self.parking_zones:
                package = Package(placed, (x, y))
                self.packages.append(package)
                self.grid[y][x] = CellType.PACKAGE
                placed += 1
    
    def get_free_position(self) -> Optional[Tuple[int, int]]:
        """Find a free position for robot spawning"""
        attempts = 0
        max_attempts = 100
        
        while attempts < max_attempts:
            x = random.randint(0, self.width - 1)
            y = random.randint(0, self.height - 1)
            
            if self.is_free((x, y)):
                return (x, y)
            attempts += 1
        
        return None
    
    def is_free(self, position: Tuple[int, int]) -> bool:
        """Check if a position is free (no obstacle, robot, or package)"""
        x, y = position
        if not (0 <= x < self.width and 0 <= y < self.height):
            return False
        
        if position in self.obstacles:
            return False
        
        if position in self.robot_positions.values():
            return False
        
        # Check if package is still at this position (not picked up and not delivered)
        for pkg in self.packages:
            if pkg.position == position and not pkg.picked_up and not pkg.delivered:
                return False
        
        return True
    
    def is_valid_position(self, position: Tuple[int, int]) -> bool:
        """Check if position is within grid bounds"""
        x, y = position
        return 0 <= x < self.width and 0 <= y < self.height
    
    def is_obstacle(self, position: Tuple[int, int]) -> bool:
        """Check if position contains an obstacle"""
        return position in self.obstacles
    
    def is_drop_zone(self, position: Tuple[int, int]) -> bool:
        """Check if position is a drop zone"""
        return position in self.drop_zones
    
    def get_package_at(self, position: Tuple[int, int]) -> Optional[Package]:
        """Get package at given position if it exists and not picked up and not delivered"""
        for pkg in self.packages:
            if pkg.position == position and not pkg.picked_up and not pkg.delivered:
                return pkg
        return None
    
    def get_undelivered_packages(self) -> List[Package]:
        """Get list of packages that haven't been delivered yet"""
        return [pkg for pkg in self.packages if not pkg.delivered]
    
    def get_unassigned_packages(self) -> List[Package]:
        """Get list of packages not yet assigned to any robot and not picked up"""
        return [pkg for pkg in self.packages if not pkg.delivered and not pkg.picked_up and pkg.assigned_robot is None]
    
    def remove_delivered_package(self, package: Package):
        """Remove a delivered package from the grid to free up space"""
        if package.delivered:
            # Store original position before clearing
            original_pos = package.position
            x, y = original_pos
            
            # Clear the package from the grid cell (its SOURCE location)
            if 0 <= y < self.height and 0 <= x < self.width:
                if self.grid[y][x] == CellType.PACKAGE:
                    self.grid[y][x] = CellType.EMPTY
                    print(f"[Warehouse] Cleared Package {package.id} source at {original_pos}")
            
            # Mark package position as None to indicate it's been fully removed
            package.position = None
    
    def get_neighbors(self, position: Tuple[int, int]) -> List[Tuple[int, int]]:
        """Get valid neighboring positions (up, down, left, right)"""
        x, y = position
        neighbors = []
        
        # 4-directional movement
        directions = [(0, 1), (0, -1), (1, 0), (-1, 0)]
        
        for dx, dy in directions:
            new_pos = (x + dx, y + dy)
            if self.is_valid_position(new_pos) and not self.is_obstacle(new_pos):
                neighbors.append(new_pos)
        
        return neighbors
    
    def update_robot_position(self, robot_id: int, old_pos: Tuple[int, int], 
                             new_pos: Tuple[int, int]) -> bool:
        """
        Update robot position in the warehouse
        
        Returns:
            True if move successful, False if position occupied
        """
        # Check if new position is occupied by another robot
        for rid, pos in self.robot_positions.items():
            if rid != robot_id and pos == new_pos:
                return False
        
        self.robot_positions[robot_id] = new_pos
        return True
    
    def add_robot(self, robot_id: int, position: Tuple[int, int]):
        """Add a robot to the warehouse"""
        self.robot_positions[robot_id] = position
    
    def remove_robot(self, robot_id: int):
        """Remove a robot from the warehouse"""
        if robot_id in self.robot_positions:
            del self.robot_positions[robot_id]
    
    def get_nearest_drop_zone(self, position: Tuple[int, int]) -> Tuple[int, int]:
        """Find nearest drop zone from given position"""
        if not self.drop_zones:
            return None
        
        min_dist = float('inf')
        nearest = None
        
        for drop_zone in self.drop_zones:
            dist = abs(position[0] - drop_zone[0]) + abs(position[1] - drop_zone[1])
            if dist < min_dist:
                min_dist = dist
                nearest = drop_zone
        
        return nearest
    
    def get_nearest_parking_spot(self, position: Tuple[int, int], occupied_positions: Set[Tuple[int, int]]) -> Optional[Tuple[int, int]]:
        """Find best available parking spot - prioritize interior (furthest corner) first"""
        if not self.parking_zones:
            return None
        
        # Get available spots
        available_spots = [spot for spot in self.parking_zones if spot not in occupied_positions]
        
        if not available_spots:
            return None
        
        # Prioritize spots in the INTERIOR (furthest from parking entrance)
        # For bottom-right parking zone, interior means max x AND max y
        # Sort by: 1) Interior priority (sum of x+y, higher is better), 2) Distance from robot (lower is better)
        def parking_priority(spot):
            interior_score = spot[0] + spot[1]  # Higher = more interior (bottom-right corner)
            distance = abs(position[0] - spot[0]) + abs(position[1] - spot[1])
            # Prioritize interior heavily, then distance
            return (-interior_score, distance)  # Negative interior_score to maximize it
        
        best_spot = min(available_spots, key=parking_priority)
        return best_spot
    
    def is_parking_zone(self, position: Tuple[int, int]) -> bool:
        """Check if position is in parking zone"""
        return position in self.parking_zones
    
    def all_packages_delivered(self) -> bool:
        """Check if all packages have been delivered"""
        return all(pkg.delivered for pkg in self.packages)
    
    def get_statistics(self) -> dict:
        """Get warehouse statistics"""
        return {
            'total_packages': len(self.packages),
            'delivered_packages': sum(1 for pkg in self.packages if pkg.delivered),
            'picked_packages': sum(1 for pkg in self.packages if pkg.picked_up),
            'active_robots': len(self.robot_positions),
            'obstacles': len(self.obstacles),
            'drop_zones': len(self.drop_zones)
        }
    
    def __repr__(self):
        """String representation of warehouse"""
        stats = self.get_statistics()
        return (f"Warehouse({self.width}x{self.height}, "
                f"packages={stats['delivered_packages']}/{stats['total_packages']}, "
                f"robots={stats['active_robots']})")
