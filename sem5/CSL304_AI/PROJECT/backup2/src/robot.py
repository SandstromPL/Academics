"""
Robot Agent
Integrates all AI techniques for autonomous warehouse navigation
"""

from typing import List, Tuple, Optional, Set
from enum import Enum
import random

from .informed_search import InformedSearch, manhattan_distance
from .uninformed_search import UninformedSearch
from .local_search import LocalSearch
from .adversarial_search import AdversarialSearch
from .warehouse import Package


class RobotState(Enum):
    """Robot states"""
    IDLE = "idle"
    MOVING_TO_PACKAGE = "moving_to_package"
    PICKING_PACKAGE = "picking_package"
    MOVING_TO_DROPZONE = "moving_to_dropzone"
    DROPPING_PACKAGE = "dropping_package"
    BLOCKED = "blocked"
    RESOLVING_CONFLICT = "resolving_conflict"
    PARKING = "parking"  # Moving to parking zone to stay out of the way


class Robot:
    """Autonomous robot agent with AI decision-making"""
    
    def __init__(self, robot_id: int, position: Tuple[int, int], warehouse, all_robots=None):
        self.id = robot_id
        self.position = position
        self.warehouse = warehouse
        self.all_robots = all_robots if all_robots is not None else []
        self.state = RobotState.IDLE
        
        # Task tracking
        self.target_package: Optional[Package] = None
        self.carrying_package: Optional[Package] = None
        self.target_position: Optional[Tuple[int, int]] = None
        self.path: List[Tuple[int, int]] = []
        self.path_index = 0
        
        # Statistics
        self.packages_delivered = 0
        self.total_distance_traveled = 0
        self.conflicts_resolved = 0
        self.blocked_count = 0
        self.search_algorithm_used = []
        
        # Wait counter for deadlock detection
        self.wait_counter = 0
        self.max_wait_steps = 5  # Replan after waiting 5 steps
        
        # Position history for oscillation detection
        self.position_history = []
        self.max_history_length = 10
        self.stuck_threshold = 3  # If we visit same position 3 times in last 10 moves, we're stuck
        
        # Parking zone management
        self.parking_retry_count = 0
        self.max_parking_retries = 5  # Try 5 different spots before waiting
        self.parking_wait_counter = 0
        
        # Configuration
        self.preferred_search = 'astar'  # Default search algorithm
        self.conflict_detection_range = 3
        self.use_adversarial_search = True  # Use minimax for conflict resolution (vs priority-based)
        self.minimax_depth = 3  # Lookahead depth for adversarial search
        
        # Register with warehouse
        self.warehouse.add_robot(self.id, self.position)
    
    def assign_package(self, package: Package):
        """Assign a package to this robot"""
        self.target_package = package
        self.target_package.assigned_robot = self.id
        self.state = RobotState.MOVING_TO_PACKAGE
        self.target_position = package.position
        self._plan_path_to_target()
    
    def _plan_path_to_target(self):
        """Plan path to current target using A* with dynamic obstacle avoidance"""
        if not self.target_position:
            return
        
        # Create a custom neighbor function that considers other robots as obstacles
        def get_neighbors_avoiding_robots(pos):
            """Get neighbors while avoiding other robot positions and drop zone congestion"""
            neighbors = self.warehouse.get_neighbors(pos)
            
            # Filter out cells occupied by other robots (treat them as temporary obstacles)
            filtered = []
            for neighbor in neighbors:
                # Allow target position even if robot is there (for package pickup/delivery)
                if neighbor == self.target_position:
                    filtered.append(neighbor)
                    continue
                
                # Avoid drop zones unless we're carrying a package to deliver
                if self.warehouse.is_drop_zone(neighbor) and not self.carrying_package:
                    # Don't path through drop zones if not delivering
                    continue
                
                # Avoid other packages (not our target) to prevent blocking scenarios
                # Example: R2→P1 blocked by P2, R1→P2 blocked by P1 (mutual deadlock)
                if not self.carrying_package:  # Only check when moving to pick up
                    blocked_by_package = False
                    for pkg in self.warehouse.packages:
                        if not pkg.picked_up and pkg.position == neighbor and pkg != self.target_package:
                            # This neighbor has a package that's not our target - avoid it
                            blocked_by_package = True
                            break
                    if blocked_by_package:
                        continue
                
                # Check if any other robot is at this position
                occupied = False
                for robot_id, robot_pos in self.warehouse.robot_positions.items():
                    if robot_id != self.id and robot_pos == neighbor:
                        occupied = True
                        break
                
                if not occupied:
                    filtered.append(neighbor)
            
            return filtered
        
        # Try A* first with robot avoidance (informed search)
        path = InformedSearch.search(
            self.position,
            self.target_position,
            get_neighbors_avoiding_robots,  # Use custom neighbor function
            algorithm='astar',
            heuristic='manhattan'
        )
        
        if path:
            self.path = path
            self.path_index = 1  # Start at index 1 to skip current position
            self.search_algorithm_used.append('astar')
            return
        
        # If robot avoidance failed, try without it (maybe robots will move)
        path = InformedSearch.search(
            self.position,
            self.target_position,
            self.warehouse.get_neighbors,  # Use original neighbor function
            algorithm='astar',
            heuristic='manhattan'
        )
        
        if path:
            self.path = path
            self.path_index = 1
            self.search_algorithm_used.append('astar')
            return
        
        # Fallback to BFS (uninformed search)
        path = UninformedSearch.search(
            self.position,
            self.target_position,
            self.warehouse.get_neighbors,
            algorithm='bfs'
        )
        
        if path:
            self.path = path
            self.path_index = 1  # Start at index 1 to skip current position
            self.search_algorithm_used.append('bfs')
        else:
            self.state = RobotState.BLOCKED
            self.blocked_count += 1
    
    def _replan_with_local_search(self):
        """Replan path using local search when blocked"""
        # Get positions occupied by other robots
        blocked_positions = set()
        for robot_id, pos in self.warehouse.robot_positions.items():
            if robot_id != self.id:
                blocked_positions.add(pos)
        
        # Try local search
        detour_path = LocalSearch.find_detour(
            self.position,
            self.target_position,
            self.warehouse.get_neighbors,
            blocked_positions=blocked_positions,
            robot_positions=self.warehouse.robot_positions,
            algorithm='hill_climbing'
        )
        
        if detour_path:
            self.path = detour_path
            self.path_index = 1  # Start at index 1 to skip current position
            self.search_algorithm_used.append('local_search')
            return True
        
        return False
    
    def _detect_conflicts(self) -> List[int]:
        """Detect potential conflicts with nearby robots"""
        conflicts = []
        
        if self.path_index >= len(self.path):
            return conflicts
        
        my_next_pos = self.path[self.path_index]
        
        for robot_id, robot_pos in self.warehouse.robot_positions.items():
            if robot_id == self.id:
                continue
            
            # Check proximity
            distance = abs(self.position[0] - robot_pos[0]) + abs(self.position[1] - robot_pos[1])
            
            if distance <= self.conflict_detection_range:
                # Simple conflict check: other robot too close
                if distance <= 1 or my_next_pos == robot_pos:
                    conflicts.append(robot_id)
        
        return conflicts
    
    def _resolve_conflict_with_robot(self, other_robot_id: int, other_robot_pos: Tuple[int, int]):
        """Resolve conflict with another robot using adversarial search"""
        # Determine goals
        my_goal = self.target_position if self.target_position else self.position
        
        # Simplified opponent goal (assume they stay or move randomly)
        other_goal = other_robot_pos
        
        # Use minimax to decide best moves
        my_move, _ = AdversarialSearch.resolve_conflict(
            self.position,
            other_robot_pos,
            my_goal,
            other_goal,
            self.warehouse.get_neighbors,
            algorithm='minimax',
            depth=2
        )
        
        if my_move and my_move != self.position:
            # Update path with conflict-resolved move
            self.path = [self.position, my_move] + self.path[self.path_index + 1:]
            self.path_index = 0
            self.conflicts_resolved += 1
            self.search_algorithm_used.append('adversarial')
    
    def _is_stuck_in_loop(self) -> bool:
        """Detect if robot is oscillating between same positions"""
        if len(self.position_history) < self.stuck_threshold:
            return False
        
        # Count how many times current position appears in recent history
        recent_history = self.position_history[-self.max_history_length:]
        position_count = recent_history.count(self.position)
        
        # If we've been at this position too many times recently, we're stuck
        return position_count >= self.stuck_threshold
    
    def _get_robot_by_id(self, robot_id: int):
        """Get robot object by ID"""
        for robot in self.all_robots:
            if robot.id == robot_id:
                return robot
        return None
    
    def _record_position(self):
        """Record current position in history"""
        self.position_history.append(self.position)
        if len(self.position_history) > self.max_history_length:
            self.position_history.pop(0)
    
    def _resolve_conflict_adversarial(self, blocking_robot) -> Optional[Tuple[int, int]]:
        """
        Use adversarial search (minimax) to resolve conflict intelligently
        Returns recommended move position, or None if should stay
        """
        if not blocking_robot or not blocking_robot.target_position:
            return None
        
        # Create neighbor function for adversarial search
        def get_neighbors_func(pos):
            neighbors = self.warehouse.get_neighbors(pos)
            # Filter out obstacles
            return [n for n in neighbors if self.warehouse.is_free(n)]
        
        try:
            # Use minimax to find optimal moves for both robots
            move1, move2 = AdversarialSearch.resolve_conflict(
                self.position,
                blocking_robot.position,
                self.target_position,
                blocking_robot.target_position,
                get_neighbors_func,
                algorithm='minimax',
                depth=self.minimax_depth
            )
            
            self.conflicts_resolved += 1
            self.search_algorithm_used.append('minimax')
            return move1
            
        except Exception as e:
            # Fallback to priority-based if adversarial search fails
            return None
    
    def _should_use_adversarial_search(self, blocking_robot) -> bool:
        """Decide if adversarial search should be used for this conflict"""
        if not self.use_adversarial_search:
            return False
        
        # Use adversarial search for close conflicts with clear goals
        if not blocking_robot or not blocking_robot.target_position:
            return False
        
        # Check if conflict is close enough to matter
        distance = abs(self.position[0] - blocking_robot.position[0]) + \
                  abs(self.position[1] - blocking_robot.position[1])
        
        # Only use for nearby conflicts (within 3 cells)
        return distance <= 3
    
    def step(self) -> bool:
        """
        Execute one step of the robot's behavior
        Returns True if robot took an action, False if idle
        """
        # Check if stuck in loop BEFORE anything else
        if self._is_stuck_in_loop() and self.state != RobotState.IDLE:
            print(f"[Robot {self.id}] Detected oscillation! Breaking free...")
            self.wait_counter = 0
            self.position_history.clear()  # Clear history
            
            # Force an escape move - try ANY free neighbor, even if not ideal
            neighbors = self.warehouse.get_neighbors(self.position)
            random.shuffle(neighbors)
            
            # First try to find completely free cells (no robots nearby)
            for neighbor in neighbors:
                if self.warehouse.is_free(neighbor):
                    # Check if any robot is at this neighbor
                    occupied = any(rpos == neighbor for rid, rpos in self.warehouse.robot_positions.items() if rid != self.id)
                    if not occupied:
                        old_pos = self.position
                        if self.warehouse.update_robot_position(self.id, old_pos, neighbor):
                            self.position = neighbor
                            print(f"[Robot {self.id}] Escaped to {neighbor}")
                            # Clear path and force complete replan
                            self.path = []
                            self.path_index = 0
                            if self.target_position:
                                # Use BFS for escaping (more exploratory) - call function directly
                                from .uninformed_search import bfs
                                self.path = bfs(self.position, self.target_position, self.warehouse.get_neighbors)
                                if self.path:
                                    self.path_index = 1
                            self._record_position()
                            return True
            
            # If still can't escape, stay put but clear everything
            print(f"[Robot {self.id}] Cannot escape - clearing state")
            self.path = []
            self.path_index = 0
            self.state = RobotState.BLOCKED
            return False
        
        if self.state == RobotState.IDLE:
            # If idle, go to parking zone to stay out of the way
            if not self.warehouse.is_parking_zone(self.position):
                # Get all occupied positions to avoid assigning occupied parking spots
                occupied_positions = set(self.warehouse.robot_positions.values())
                parking_spot = self.warehouse.get_nearest_parking_spot(self.position, occupied_positions)
                
                if parking_spot:
                    self.target_position = parking_spot
                    self.state = RobotState.PARKING
                    self._plan_path_to_target()
                    print(f"[Robot {self.id}] Idle - heading to parking zone at {parking_spot}")
                    return False  # Will move on next step
            
            # Already in parking zone or no parking available, stay put
            return False
        
        if self.state == RobotState.PARKING:
            # Moving to parking zone
            if not self.path or self.path_index >= len(self.path):
                # Reached parking zone
                if self.warehouse.is_parking_zone(self.position):
                    self.state = RobotState.IDLE
                    self.target_position = None
                    # Reset parking counters on successful park
                    self.parking_retry_count = 0
                    self.parking_wait_counter = 0
                    print(f"[Robot {self.id}] Parked at {self.position}")
                    return True
                else:
                    # Not at parking yet, replan
                    occupied_positions = set(self.warehouse.robot_positions.values())
                    parking_spot = self.warehouse.get_nearest_parking_spot(self.position, occupied_positions)
                    if parking_spot:
                        self.target_position = parking_spot
                        self._plan_path_to_target()
                return False
            
            # Check if target parking spot is now occupied - if so, pick a different spot immediately
            if self.target_position:
                for robot_id, robot_pos in self.warehouse.robot_positions.items():
                    if robot_id != self.id and robot_pos == self.target_position:
                        # Target parking spot is taken! Choose a different one
                        self.parking_retry_count += 1
                        
                        # If tried too many times, wait a bit before retrying
                        if self.parking_retry_count >= self.max_parking_retries:
                            self.parking_wait_counter += 1
                            if self.parking_wait_counter >= 3:
                                # Reset counters and try again
                                print(f"[Robot {self.id}] Parking congested, waiting for spot to clear...")
                                self.parking_retry_count = 0
                                self.parking_wait_counter = 0
                            return False
                        
                        print(f"[Robot {self.id}] Parking spot {self.target_position} occupied by Robot {robot_id}, finding alternative...")
                        occupied_positions = set(self.warehouse.robot_positions.values())
                        new_parking_spot = self.warehouse.get_nearest_parking_spot(self.position, occupied_positions)
                        if new_parking_spot and new_parking_spot != self.target_position:
                            self.target_position = new_parking_spot
                            self._plan_path_to_target()
                            print(f"[Robot {self.id}] Redirecting to parking spot {new_parking_spot}")
                        else:
                            # No alternative spots available, wait
                            print(f"[Robot {self.id}] No parking spots available, waiting...")
                            self.parking_wait_counter += 1
                            if self.parking_wait_counter >= 5:
                                # Give up parking, just stay where we are
                                print(f"[Robot {self.id}] Parking zone full, staying at current position")
                                self.state = RobotState.IDLE
                                self.target_position = None
                                self.parking_retry_count = 0
                                self.parking_wait_counter = 0
                        break
        
        # Check if we have a path to follow
        if not self.path or self.path_index >= len(self.path):
            if self.state == RobotState.MOVING_TO_PACKAGE:
                # Reached package location
                self._pick_package()
                return True
            elif self.state == RobotState.MOVING_TO_DROPZONE:
                # Check if drop zone is accessible (not surrounded by other robots)
                if self.warehouse.is_drop_zone(self.position):
                    # Already at drop zone, deliver immediately
                    self._drop_package()
                    return True
                elif self.target_position and self.warehouse.is_drop_zone(self.target_position):
                    # Check if drop zone is blocked by multiple robots (trap scenario)
                    dropzone_neighbors = self.warehouse.get_neighbors(self.target_position)
                    blocked_count = 0
                    blocking_robots = []
                    
                    for neighbor in dropzone_neighbors:
                        for robot_id, robot_pos in self.warehouse.robot_positions.items():
                            if robot_id != self.id and robot_pos == neighbor:
                                blocked_count += 1
                                blocking_robots.append(robot_id)
                                break
                    
                    # If 2+ robots blocking drop zone, it's likely a trap - wait for higher priority to clear
                    if blocked_count >= 2:
                        has_priority = all(self.id < rid for rid in blocking_robots)
                        if not has_priority:
                            # Lower priority - wait briefly then replan
                            self.wait_counter += 1
                            if self.wait_counter >= 3:  # Short wait for drop zone congestion
                                print(f"[Robot {self.id}] Drop zone congested, replanning path...")
                                self.wait_counter = 0
                                # Clear current path and replan on next step
                                self.path = None
                                self.path_index = 0
                            return False
                    
                    # Try to reach drop zone
                    self._drop_package()
                    return True
                else:
                    return False
            else:
                return False
        
        # Try to move to next position in path
        next_pos = self.path[self.path_index]
        
        # Check if next position is occupied by another robot
        occupied_by_robot = False
        blocking_robot_id = None
        for robot_id, robot_pos in self.warehouse.robot_positions.items():
            if robot_id != self.id and robot_pos == next_pos:
                occupied_by_robot = True
                blocking_robot_id = robot_id
                break
        
        # If occupied by another robot, handle conflict
        if occupied_by_robot:
            self.wait_counter += 1
            
            # Get blocking robot's state to check if it's carrying a package
            blocking_robot = self._get_robot_by_id(blocking_robot_id)
            i_have_package = self.carrying_package is not None
            blocker_has_package = blocking_robot.carrying_package is not None if blocking_robot else False
            
            # TRY ADVERSARIAL SEARCH FIRST (if enabled and conditions met)
            if self._should_use_adversarial_search(blocking_robot):
                recommended_move = self._resolve_conflict_adversarial(blocking_robot)
                
                if recommended_move and recommended_move != self.position:
                    # Execute the minimax-recommended move
                    if self.warehouse.is_free(recommended_move):
                        # Check if position is occupied by another robot
                        occupied = False
                        for rid, rpos in self.warehouse.robot_positions.items():
                            if rid != self.id and rpos == recommended_move:
                                occupied = True
                                break
                        
                        if not occupied:
                            old_pos = self.position
                            if self.warehouse.update_robot_position(self.id, old_pos, recommended_move):
                                self.position = recommended_move
                                self.total_distance_traveled += 1
                                print(f"[Robot {self.id}] Minimax move to {recommended_move} (avoiding Robot {blocking_robot_id})")
                                self.wait_counter = 0
                                # Replan path from new position
                                self.path = []
                                self.path_index = 0
                                if self.target_position:
                                    self._plan_path_to_target()
                                return True
                elif recommended_move == self.position:
                    # Minimax recommends staying put
                    print(f"[Robot {self.id}] Minimax: Hold position (Robot {blocking_robot_id} will move)")
                    return False
            
            # FALLBACK TO PRIORITY-BASED SYSTEM if adversarial search not used/failed
            
            # PRIORITY RULE: Robot with package has HIGHER priority than robot without package
            # Also: Robots in PARKING state have LOWEST priority
            if i_have_package and not blocker_has_package:
                # I'm carrying a package, blocker is empty - I have priority
                # Tell blocker to move by waiting
                if self.wait_counter >= 1:
                    print(f"[Robot {self.id}] Carrying package, waiting for empty Robot {blocking_robot_id} to move...")
                    # If blocker doesn't move after shorter wait, replan around them
                    if self.wait_counter >= 3:
                        self.wait_counter = 0
                        self.path = []
                        self.path_index = 0
                        if self.target_position:
                            self._plan_path_to_target()
                return False
            elif not i_have_package and blocker_has_package:
                # I'm empty, blocker has package - they have priority, yield immediately!
                print(f"[Robot {self.id}] Yielding path to Robot {blocking_robot_id} (carrying package)")
                self.wait_counter = 0
                
                # SPECIAL: If I'm going to parking, just stay put and let them pass
                if self.state == RobotState.PARKING:
                    # Replan parking path after they pass
                    self.path = []
                    self.path_index = 0
                    return False
                
                # Try to move aside immediately
                neighbors = self.warehouse.get_neighbors(self.position)
                random.shuffle(neighbors)
                for neighbor in neighbors:
                    if neighbor != next_pos and self.warehouse.is_free(neighbor):
                        occupied = False
                        for rid, rpos in self.warehouse.robot_positions.items():
                            if rid != self.id and rpos == neighbor:
                                occupied = True
                                break
                        
                        if not occupied:
                            old_pos = self.position
                            if self.warehouse.update_robot_position(self.id, old_pos, neighbor):
                                self.position = neighbor
                                print(f"[Robot {self.id}] Moved aside to {neighbor} for package carrier")
                                # Replan from new position
                                self.path = []
                                self.path_index = 0
                                if self.target_position:
                                    self._plan_path_to_target()
                                return True
                
                # If can't move aside, just replan to find alternate route
                self.path = []
                self.path_index = 0
                if self.target_position:
                    self._plan_path_to_target()
                return False
            
            # If stuck for too long, force replanning regardless of priority
            if self.wait_counter >= 5:
                print(f"[Robot {self.id}] Stuck for {self.wait_counter} steps, finding alternate path...")
                self.wait_counter = 0
                self.path = []
                self.path_index = 0
                if self.target_position:
                    self._plan_path_to_target()
                
                # If still no path or same conflict, try moving to random adjacent cell
                if not self.path or len(self.path) <= 1:
                    neighbors = self.warehouse.get_neighbors(self.position)
                    random.shuffle(neighbors)
                    for neighbor in neighbors:
                        if self.warehouse.is_free(neighbor):
                            occupied = False
                            for rid, rpos in self.warehouse.robot_positions.items():
                                if rid != self.id and rpos == neighbor:
                                    occupied = True
                                    break
                            if not occupied:
                                old_pos = self.position
                                if self.warehouse.update_robot_position(self.id, old_pos, neighbor):
                                    self.position = neighbor
                                    print(f"[Robot {self.id}] Made exploratory move to {neighbor}")
                                    return True
                return False
            
            # If both have packages or both empty, use ID-based priority: Lower ID = Higher priority
            if self.id < blocking_robot_id:
                # I have priority - wait briefly
                if self.wait_counter >= 3:
                    # Higher priority but still blocked - try alternate route
                    self.wait_counter = 0
                    self.path = []
                    self.path_index = 0
                    if self.target_position:
                        self._plan_path_to_target()
                return False
            else:
                # I have lower priority - yield quickly
                if self.wait_counter >= 2:
                    self.wait_counter = 0
                    
                    # Try to move to an adjacent cell to let the other robot pass
                    neighbors = self.warehouse.get_neighbors(self.position)
                    random.shuffle(neighbors)  # Randomize to avoid patterns
                    for neighbor in neighbors:
                        if neighbor != next_pos and self.warehouse.is_free(neighbor):
                            occupied = False
                            for rid, rpos in self.warehouse.robot_positions.items():
                                if rid != self.id and rpos == neighbor:
                                    occupied = True
                                    break
                            
                            if not occupied:
                                old_pos = self.position
                                if self.warehouse.update_robot_position(self.id, old_pos, neighbor):
                                    self.position = neighbor
                                    print(f"[Robot {self.id}] Yielded to Robot {blocking_robot_id}")
                                    # Replan from new position
                                    self.path = []
                                    self.path_index = 0
                                    if self.target_position:
                                        self._plan_path_to_target()
                                    return True
                    
                    # If couldn't move aside, replan
                    self.path = []
                    self.path_index = 0
                    if self.target_position:
                        self._plan_path_to_target()
                    return False
                
                return False
        
        # Reset wait counter if not blocked
        self.wait_counter = 0
        
        # Check if position is free (or is our target)
        if self.warehouse.is_free(next_pos) or next_pos == self.target_position:
            # Move to next position
            old_pos = self.position
            success = self.warehouse.update_robot_position(self.id, old_pos, next_pos)
            
            if success:
                self.position = next_pos
                self.path_index += 1
                
                # Record position for loop detection
                self._record_position()
                
                # Update distance traveled
                self.total_distance_traveled += 1
                
                # Reset to normal state if was resolving conflict
                if self.state == RobotState.RESOLVING_CONFLICT:
                    if self.carrying_package:
                        self.state = RobotState.MOVING_TO_DROPZONE
                    else:
                        self.state = RobotState.MOVING_TO_PACKAGE
                
                return True
            else:
                # Position occupied, need to replan
                self.state = RobotState.BLOCKED
                self.blocked_count += 1
        
        # If blocked, try local search
        if self.state == RobotState.BLOCKED:
            if self._replan_with_local_search():
                # Successfully replanned
                if self.carrying_package:
                    self.state = RobotState.MOVING_TO_DROPZONE
                else:
                    self.state = RobotState.MOVING_TO_PACKAGE
            else:
                # Wait one turn
                pass
        
        return False
    
    def _pick_package(self):
        """Pick up the target package"""
        if self.target_package and not self.target_package.picked_up:
            self.carrying_package = self.target_package
            self.carrying_package.picked_up = True
            self.state = RobotState.PICKING_PACKAGE
            
            # Set target to nearest drop zone
            drop_zone = self.warehouse.get_nearest_drop_zone(self.position)
            if drop_zone:
                self.target_position = drop_zone
                self.state = RobotState.MOVING_TO_DROPZONE
                self._plan_path_to_target()
    
    def _drop_package(self):
        """Drop package at drop zone"""
        if self.carrying_package and self.warehouse.is_drop_zone(self.position):
            # Mark package as delivered and reset its state
            self.carrying_package.delivered = True
            self.carrying_package.picked_up = False
            self.carrying_package.assigned_robot = None
            
            # Remove the delivered package from the warehouse grid
            self.warehouse.remove_delivered_package(self.carrying_package)
            
            # Update robot statistics
            self.packages_delivered += 1
            
            # Clear robot state
            self.carrying_package = None
            self.target_package = None
            self.target_position = None
            self.path = []
            self.state = RobotState.IDLE
    
    def is_idle(self) -> bool:
        """Check if robot is idle"""
        return self.state == RobotState.IDLE
    
    def is_available(self) -> bool:
        """Check if robot is available for new assignment"""
        # Robot is available if it's idle or blocked (stuck) and not carrying a package
        return (self.state == RobotState.IDLE or self.state == RobotState.BLOCKED) and not self.carrying_package
    
    def get_statistics(self) -> dict:
        """Get robot statistics"""
        return {
            'id': self.id,
            'position': self.position,
            'state': self.state.value,
            'packages_delivered': self.packages_delivered,
            'distance_traveled': self.total_distance_traveled,
            'conflicts_resolved': self.conflicts_resolved,
            'blocked_count': self.blocked_count,
            'carrying_package': self.carrying_package.id if self.carrying_package else None,
            'target_package': self.target_package.id if self.target_package else None,
            'algorithms_used': list(set(self.search_algorithm_used))
        }
    
    def __repr__(self):
        return f"Robot({self.id}, pos={self.position}, state={self.state.value}, pkg={self.carrying_package.id if self.carrying_package else None})"
