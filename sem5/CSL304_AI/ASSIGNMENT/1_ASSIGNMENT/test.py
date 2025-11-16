import heapq
import math

class TaxiRouter:
    def __init__(self):
        self.nodes = {}  # id -> (x, y)
        self.edges = {}  # (u, v) -> distance
        self.graph = {}  # adjacency list
        self.passengers = []  # [(pickup, dropoff), ...]
        self.speed = 40  # km/h
        self.wait_time = 30  # minutes
        self.time_per_km = 60 / 40  # 1.5 minutes per km

    def dijkstra_shortest_path(self, start, goal):
        """Find shortest path using Dijkstra's algorithm"""
        # Priority queue: (distance, current_node, path)
        pq = [(0, start, [start])]
        distances = {start: 0}
        visited = set()

        while pq:
            current_dist, current, path = heapq.heappop(pq)

            if current in visited:
                continue

            visited.add(current)

            # Found the goal!
            if current == goal:
                return path, current_dist

            # Explore neighbors
            if current in self.graph:
                for neighbor, edge_dist in self.graph[current]:
                    if neighbor not in visited:
                        new_dist = current_dist + edge_dist

                        if neighbor not in distances or new_dist < distances[neighbor]:
                            distances[neighbor] = new_dist
                            new_path = path + [neighbor]
                            heapq.heappush(pq, (new_dist, neighbor, new_path))

        return [], float('inf')  # No path found

    def check_congestion(self, edge, start_time, end_time, all_routes):
        """Check if edge would have 3+ taxis (congestion)"""
        u, v = edge
        count = 0

        for route_info in all_routes:
            for edge_data in route_info['edge_times']:
                route_u, route_v = edge_data['edge']
                route_start, route_end = edge_data['start'], edge_data['end']

                # Same edge (either direction)?
                if (route_u == u and route_v == v) or (route_u == v and route_v == u):
                    # Time intervals overlap?
                    if not (end_time <= route_start or start_time >= route_end):
                        count += 1

        return count >= 2  # True if would be 3rd taxi

    def plan_route(self, taxi_id, pickup, dropoff, existing_routes):
        """Plan route for one taxi considering traffic"""
        # Get shortest path using Dijkstra
        path, total_distance = self.dijkstra_shortest_path(pickup, dropoff)

        if not path:
            print(f"ERROR: No path from {pickup} to {dropoff}")
            return None

        current_time = 0
        edge_times = []
        waits = []

        # Go through each edge in the path
        for i in range(len(path) - 1):
            u, v = path[i], path[i + 1]
            distance = self.edges[(u, v)]
            travel_time = distance * self.time_per_km

            # When would we start/end on this edge?
            start_time = current_time
            end_time = current_time + travel_time

            # Check for congestion
            if self.check_congestion((u, v), start_time, end_time, existing_routes):
                # Must wait!
                waits.append({'at_node': u, 'to_edge': v, 'wait_minutes': self.wait_time})
                current_time += self.wait_time
                start_time = current_time
                end_time = current_time + travel_time

            # Record this edge usage
            edge_times.append({
                'edge': (u, v),
                'start': start_time,
                'end': end_time,
                'distance': distance
            })

            current_time = end_time

        return {
            'taxi_id': taxi_id,
            'pickup': pickup,
            'dropoff': dropoff,
            'path': path,
            'total_time': current_time,
            'edge_times': edge_times,
            'waits': waits
        }

    def solve(self):
        """Main solver - plan routes for all taxis"""
        all_routes = []

        # Process each taxi/passenger pair
        for i, (pickup, dropoff) in enumerate(self.passengers):
            taxi_id = i + 1
            route = self.plan_route(taxi_id, pickup, dropoff, all_routes)

            if route:
                all_routes.append(route)

        return all_routes

    def print_results(self, routes):
        """Print results in the required format"""
        total_time = 0
        max_time = 0

        print("\n--- Problem 1 Results ---")
        for route in routes:
            print(f"Taxi {route['taxi_id']}: Passenger {route['pickup']}->{route['dropoff']}")
            print(f"Route: {' -> '.join(map(str, route['path']))}")

            # Print any waits
            for wait in route['waits']:
                print(f"WAIT on edge ({wait['at_node']}->{wait['to_edge']}): {wait['wait_minutes']} minutes")

            print(f"Total time = {route['total_time']:.1f} minutes")
            print()

            total_time += route['total_time']
            max_time = max(max_time, route['total_time'])

        print(f"Overall Completion Time = {total_time:.1f} minutes")
        print(f"Makespan = {max_time:.1f} minutes")
        
# --- Main execution block for the sample input ---
if __name__ == "__main__":
    router = TaxiRouter()

    # Manually set up the sample data
    router.nodes = {1: (0, 0), 2: (30, 0), 3: (80, 0), 4: (30, 60),
                   5: (120, 0), 6: (30, 120), 7: (60, 120), 8: (110, 120)}

    edges_data = [(1,2,30), (2,3,50), (2,4,60), (3,5,40), (4,6,70),
                  (5,7,20), (6,7,30), (7,8,50), (3,6,90)]

    router.graph = {i: [] for i in range(1, 9)}
    router.edges = {}
    for u, v, d in edges_data:
        router.edges[(u, v)] = d
        router.edges[(v, u)] = d
        router.graph[u].append((v, d))
        router.graph[v].append((u, d))

    router.passengers = [(2, 7), (1, 8), (3, 4)]
    router.speed = 40
    router.wait_time = 30
    router.time_per_km = 1.5

    # Solve and print
    routes = router.solve()
    router.print_results(routes)