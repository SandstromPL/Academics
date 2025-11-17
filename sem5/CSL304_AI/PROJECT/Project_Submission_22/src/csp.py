"""
Constraint Satisfaction Problem for Robot-Package Assignment
Assigns packages to robots optimally considering constraints
"""

from typing import List, Tuple, Dict, Set, Optional, Any
import itertools


class CSPVariable:
    """Represents a robot in the CSP"""
    def __init__(self, robot_id: int, position: Tuple[int, int]):
        self.robot_id = robot_id
        self.position = position
        self.domain = []  # List of package IDs this robot can be assigned
        self.assigned_package = None
    
    def __repr__(self):
        return f"Robot({self.robot_id}, pkg={self.assigned_package})"


class CSPConstraint:
    """Base class for constraints"""
    def is_satisfied(self, assignment: Dict[int, int]) -> bool:
        """Check if assignment satisfies this constraint"""
        raise NotImplementedError


class AllDifferentConstraint(CSPConstraint):
    """Ensures all robots get different packages"""
    def is_satisfied(self, assignment: Dict[int, int]) -> bool:
        values = [v for v in assignment.values() if v is not None]
        return len(values) == len(set(values))


class DistanceConstraint(CSPConstraint):
    """Ensures robot is reasonably close to assigned package"""
    def __init__(self, robot_positions: Dict[int, Tuple[int, int]], 
                 package_positions: Dict[int, Tuple[int, int]],
                 max_distance: int = 50):
        self.robot_positions = robot_positions
        self.package_positions = package_positions
        self.max_distance = max_distance
    
    def is_satisfied(self, assignment: Dict[int, int]) -> bool:
        for robot_id, package_id in assignment.items():
            if package_id is None:
                continue
            
            robot_pos = self.robot_positions[robot_id]
            package_pos = self.package_positions[package_id]
            
            distance = abs(robot_pos[0] - package_pos[0]) + abs(robot_pos[1] - package_pos[1])
            if distance > self.max_distance:
                return False
        
        return True


class WorkloadBalanceConstraint(CSPConstraint):
    """Ensures workload is balanced among robots"""
    def __init__(self, robot_positions: Dict[int, Tuple[int, int]],
                 package_positions: Dict[int, Tuple[int, int]],
                 max_imbalance: float = 2.0):
        self.robot_positions = robot_positions
        self.package_positions = package_positions
        self.max_imbalance = max_imbalance
    
    def get_workload(self, robot_id: int, package_id: int) -> float:
        """Calculate workload (distance) for robot to package"""
        robot_pos = self.robot_positions[robot_id]
        package_pos = self.package_positions[package_id]
        return abs(robot_pos[0] - package_pos[0]) + abs(robot_pos[1] - package_pos[1])
    
    def is_satisfied(self, assignment: Dict[int, int]) -> bool:
        if len(assignment) < 2:
            return True
        
        workloads = []
        for robot_id, package_id in assignment.items():
            if package_id is not None:
                workloads.append(self.get_workload(robot_id, package_id))
        
        if not workloads:
            return True
        
        max_workload = max(workloads)
        min_workload = min(workloads)
        
        if min_workload == 0:
            return max_workload <= self.max_imbalance * 10
        
        return max_workload / min_workload <= self.max_imbalance


class PackageAssignmentCSP:
    """CSP for assigning packages to robots"""
    
    def __init__(self, robots: List[CSPVariable], packages: List[Any],
                 constraints: List[CSPConstraint] = None):
        self.variables = {robot.robot_id: robot for robot in robots}
        self.packages = packages
        self.constraints = constraints or []
        self.assignment = {}  # robot_id -> package_id
    
    def add_constraint(self, constraint: CSPConstraint):
        """Add a constraint to the CSP"""
        self.constraints.append(constraint)
    
    def is_consistent(self, robot_id: int, package_id: int) -> bool:
        """Check if assigning package to robot is consistent with all constraints"""
        # Make temporary assignment
        temp_assignment = self.assignment.copy()
        temp_assignment[robot_id] = package_id
        
        # Check all constraints
        for constraint in self.constraints:
            if not constraint.is_satisfied(temp_assignment):
                return False
        
        return True
    
    def select_unassigned_variable(self) -> Optional[int]:
        """Select next robot to assign (MRV heuristic - Most Constrained Variable)"""
        unassigned = [rid for rid in self.variables.keys() if rid not in self.assignment]
        
        if not unassigned:
            return None
        
        # Choose robot with smallest domain (MRV)
        return min(unassigned, key=lambda rid: len(self.variables[rid].domain))
    
    def order_domain_values(self, robot_id: int) -> List[int]:
        """Order domain values (Least Constraining Value heuristic)"""
        robot = self.variables[robot_id]
        
        # Filter out already assigned packages
        assigned_packages = set(self.assignment.values())
        available = [pkg_id for pkg_id in robot.domain if pkg_id not in assigned_packages]
        
        # Sort by distance (closest first)
        def distance_to_package(pkg_id):
            pkg = next(p for p in self.packages if p.id == pkg_id)
            return abs(robot.position[0] - pkg.position[0]) + abs(robot.position[1] - pkg.position[1])
        
        return sorted(available, key=distance_to_package)
    
    def backtracking_search(self) -> Optional[Dict[int, int]]:
        """Solve CSP using backtracking with constraint propagation"""
        if len(self.assignment) == len(self.variables):
            return self.assignment
        
        # Select unassigned variable
        robot_id = self.select_unassigned_variable()
        if robot_id is None:
            return self.assignment
        
        # Try each value in ordered domain
        for package_id in self.order_domain_values(robot_id):
            if self.is_consistent(robot_id, package_id):
                # Make assignment
                self.assignment[robot_id] = package_id
                
                # Recurse
                result = self.backtracking_search()
                if result is not None:
                    return result
                
                # Backtrack
                del self.assignment[robot_id]
        
        return None
    
    def forward_checking(self, robot_id: int, package_id: int) -> bool:
        """
        Forward checking - check if assignment eliminates all options for future variables
        Returns True if assignment is valid
        """
        # Check if any unassigned robot would have empty domain
        for other_id, other_robot in self.variables.items():
            if other_id == robot_id or other_id in self.assignment:
                continue
            
            # Check if other robot still has valid options
            assigned_packages = set(self.assignment.values()) | {package_id}
            remaining = [p for p in other_robot.domain if p not in assigned_packages]
            
            if not remaining:
                return False
        
        return True
    
    def solve(self) -> Optional[Dict[int, int]]:
        """Solve the CSP and return assignment"""
        self.assignment = {}
        return self.backtracking_search()


def assign_packages_to_robots(robot_positions: Dict[int, Tuple[int, int]],
                              packages: List[Any],
                              use_constraints: bool = True) -> Dict[int, Optional[int]]:
    """
    Assign packages to robots using CSP
    
    Args:
        robot_positions: Dictionary mapping robot_id to position
        packages: List of Package objects
        use_constraints: Whether to use constraints
    
    Returns:
        Dictionary mapping robot_id to package_id (or None if unassigned)
    """
    # Create variables (robots)
    variables = []
    for robot_id, position in robot_positions.items():
        var = CSPVariable(robot_id, position)
        # Domain is all available packages
        var.domain = [pkg.id for pkg in packages if not pkg.delivered and pkg.assigned_robot is None]
        variables.append(var)
    
    # Create package position mapping
    package_positions = {pkg.id: pkg.position for pkg in packages}
    
    # Create CSP
    csp = PackageAssignmentCSP(variables, packages)
    
    if use_constraints:
        # Add constraints
        csp.add_constraint(AllDifferentConstraint())
        csp.add_constraint(DistanceConstraint(robot_positions, package_positions, max_distance=100))
        csp.add_constraint(WorkloadBalanceConstraint(robot_positions, package_positions, max_imbalance=3.0))
    
    # Solve
    solution = csp.solve()
    
    # If no solution found with all constraints, try without workload balance
    if solution is None and use_constraints:
        csp = PackageAssignmentCSP(variables, packages)
        csp.add_constraint(AllDifferentConstraint())
        csp.add_constraint(DistanceConstraint(robot_positions, package_positions, max_distance=100))
        solution = csp.solve()
    
    # If still no solution, use greedy assignment
    if solution is None:
        solution = greedy_assignment(robot_positions, packages)
    
    return solution


def greedy_assignment(robot_positions: Dict[int, Tuple[int, int]],
                     packages: List[Any]) -> Dict[int, Optional[int]]:
    """
    Greedy package assignment - assign each robot to nearest unassigned package
    
    Args:
        robot_positions: Dictionary mapping robot_id to position
        packages: List of Package objects
    
    Returns:
        Dictionary mapping robot_id to package_id
    """
    assignment = {}
    available_packages = [pkg for pkg in packages if not pkg.delivered and pkg.assigned_robot is None]
    assigned_packages = set()
    
    # Sort robots by proximity to packages
    robot_list = list(robot_positions.items())
    
    for robot_id, robot_pos in robot_list:
        if not available_packages or len(assigned_packages) >= len(available_packages):
            assignment[robot_id] = None
            continue
        
        # Find nearest unassigned package
        nearest_package = None
        min_distance = float('inf')
        
        for pkg in available_packages:
            if pkg.id in assigned_packages:
                continue
            
            distance = abs(robot_pos[0] - pkg.position[0]) + abs(robot_pos[1] - pkg.position[1])
            if distance < min_distance:
                min_distance = distance
                nearest_package = pkg
        
        if nearest_package:
            assignment[robot_id] = nearest_package.id
            assigned_packages.add(nearest_package.id)
        else:
            assignment[robot_id] = None
    
    return assignment


class ConstraintSatisfaction:
    """Wrapper class for CSP operations"""
    
    @staticmethod
    def assign_packages(robot_positions: Dict[int, Tuple[int, int]],
                       packages: List[Any],
                       method: str = 'csp') -> Dict[int, Optional[int]]:
        """
        Assign packages to robots
        
        Args:
            robot_positions: Dictionary mapping robot_id to position
            packages: List of Package objects
            method: 'csp' or 'greedy'
        
        Returns:
            Dictionary mapping robot_id to package_id
        """
        if method == 'csp':
            return assign_packages_to_robots(robot_positions, packages, use_constraints=True)
        elif method == 'greedy':
            return greedy_assignment(robot_positions, packages)
        else:
            raise ValueError(f"Unknown method: {method}")
