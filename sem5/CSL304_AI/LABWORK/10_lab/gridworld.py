import numpy as np

class GridWorld:
    def __init__(self):
        self.grid_size = (5, 5)
        self.start_state = (0, 0)
        self.goal_state = (4, 4)
        self.obstacles = [(1, 1), (2, 2), (3, 1), (3, 3), (1, 3)]
        self.actions = {'UP': 0, 'DOWN': 1, 'LEFT': 2, 'RIGHT': 3}
        self.num_actions = len(self.actions)
        self.num_states = self.grid_size[0] * self.grid_size[1]

    def state_to_coords(self, state):
        return (state // self.grid_size[0], state % self.grid_size[1])

    def coords_to_state(self, coords):
        return coords[0] * self.grid_size[0] + coords[1]

    def is_valid_state(self, state):
        row, col = self.state_to_coords(state)
        return 0 <= row < self.grid_size[0] and 0 <= col < self.grid_size[1]

    def is_obstacle(self, state):
        return self.state_to_coords(state) in self.obstacles

    def is_goal(self, state):
        return self.state_to_coords(state) == self.goal_state

    def get_reward(self, state, next_state):
        if self.is_goal(next_state):
            return 100
        elif self.is_obstacle(next_state):
            return -10
        else:
            return -1

    def step(self, state, action):
        row, col = self.state_to_coords(state)
        
        if action == self.actions['UP']:
            next_row, next_col = row - 1, col
        elif action == self.actions['DOWN']:
            next_row, next_col = row + 1, col
        elif action == self.actions['LEFT']:
            next_row, next_col = row, col - 1
        elif action == self.actions['RIGHT']:
            next_row, next_col = row, col + 1
        else:
            raise ValueError("Invalid action")

        next_coords = (next_row, next_col)
        next_state = self.coords_to_state(next_coords)

        # Transition rules
        if not self.is_valid_state(next_state) or self.is_obstacle(next_state):
            # If action goes outside grid or hits an obstacle, agent stays in the same state
            next_state = state
            reward = self.get_reward(state, next_state) # Reward for hitting obstacle or boundary
        else:
            reward = self.get_reward(state, next_state)

        done = self.is_goal(next_state)
        return next_state, reward, done

    def reset(self):
        return self.coords_to_state(self.start_state)

    def render(self):
        grid = np.full(self.grid_size, '.', dtype=str)
        for obs in self.obstacles:
            grid[obs] = 'X'
        grid[self.start_state] = 'S'
        grid[self.goal_state] = 'G'

        for r in range(self.grid_size[0]):
            for c in range(self.grid_size[1]):
                print(grid[r, c], end=' ')
            print()
        print()

if __name__ == '__main__':
    env = GridWorld()
    env.render()

    current_state = env.reset()
    print(f"Initial state: {env.state_to_coords(current_state)}")

    # Test some steps
    # Move right
    next_state, reward, done = env.step(current_state, env.actions['RIGHT'])
    print(f"Action: RIGHT, Next state: {env.state_to_coords(next_state)}, Reward: {reward}, Done: {done}")
    current_state = next_state

    # Move down
    next_state, reward, done = env.step(current_state, env.actions['DOWN'])
    print(f"Action: DOWN, Next state: {env.state_to_coords(next_state)}, Reward: {reward}, Done: {done}")
    current_state = next_state

    # Try to move into an obstacle (1,1) from (0,1)
    current_state = env.coords_to_state((0,1))
    next_state, reward, done = env.step(current_state, env.actions['DOWN'])
    print(f"From (0,1) Action: DOWN (into obstacle), Next state: {env.state_to_coords(next_state)}, Reward: {reward}, Done: {done}")
    assert next_state == current_state # Should stay in the same state

    # Try to move out of bounds (from (0,0) UP)
    current_state = env.coords_to_state((0,0))
    next_state, reward, done = env.step(current_state, env.actions['UP'])
    print(f"From (0,0) Action: UP (out of bounds), Next state: {env.state_to_coords(next_state)}, Reward: {reward}, Done: {done}")
    assert next_state == current_state # Should stay in the same state

    # Reach goal
    current_state = env.coords_to_state((4,3))
    next_state, reward, done = env.step(current_state, env.actions['RIGHT'])
    print(f"From (4,3) Action: RIGHT (to goal), Next state: {env.state_to_coords(next_state)}, Reward: {reward}, Done: {done}")
    assert env.is_goal(next_state) and reward == 100 and done == True
