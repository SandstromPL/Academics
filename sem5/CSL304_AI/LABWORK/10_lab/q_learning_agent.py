import numpy as np
import random
import matplotlib.pyplot as plt
from gridworld import GridWorld

class QLearningAgent:
    def __init__(self, env: GridWorld, alpha=0.1, gamma=0.99, epsilon=0.1):
        self.env = env
        self.alpha = alpha  # Learning rate
        self.gamma = gamma  # Discount factor
        self.epsilon = epsilon  # Exploration-exploitation trade-off
        self.q_table = np.zeros((env.num_states, env.num_actions))

    def choose_action(self, state):
        if random.uniform(0, 1) < self.epsilon:
            return random.choice(range(self.env.num_actions))  # Explore
        else:
            return np.argmax(self.q_table[state, :])  # Exploit

    def update_q_table(self, state, action, reward, next_state):
        old_value = self.q_table[state, action]
        next_max = np.max(self.q_table[next_state, :])

        new_value = old_value + self.alpha * (reward + self.gamma * next_max - old_value)
        self.q_table[state, action] = new_value

    def train(self, num_episodes):
        rewards_per_episode = []

        for episode in range(num_episodes):
            state = self.env.reset()
            done = False
            total_reward = 0

            while not done:
                action = self.choose_action(state)
                next_state, reward, done = self.env.step(state, action)
                self.update_q_table(state, action, reward, next_state)

                state = next_state
                total_reward += reward
            rewards_per_episode.append(total_reward)
            
            if episode % 100 == 0:
                print(f"Episode {episode}: Total Reward = {total_reward}")

        print("Training finished.")
        return rewards_per_episode

    def get_optimal_policy(self):
        optimal_policy = np.argmax(self.q_table, axis=1)
        return optimal_policy

    def print_q_table(self):
        print("Q-Table:")
        print(self.q_table)

if __name__ == '__main__':
    env = GridWorld()
    agent = QLearningAgent(env, alpha=0.1, gamma=0.99, epsilon=0.1)

    num_episodes = 1000
    rewards = agent.train(num_episodes)

    print("\nFinal Q-Table:")
    agent.print_q_table()

    optimal_policy = agent.get_optimal_policy()
    print("\nOptimal Policy (action index for each state):")
    print(optimal_policy.reshape(env.grid_size))

    # Visualize the optimal policy (optional)
    policy_grid = np.full(env.grid_size, ' ', dtype=str)
    action_symbols = {0: '^', 1: 'v', 2: '<', 3: '>'} # UP, DOWN, LEFT, RIGHT

    for i in range(env.num_states):
        row, col = env.state_to_coords(i)
        if env.is_goal(i):
            policy_grid[row, col] = 'G'
        elif env.is_obstacle(i):
            policy_grid[row, col] = 'X'
        else:
            policy_grid[row, col] = action_symbols[optimal_policy[i]]
    
    policy_grid[env.start_state] = 'S'

    print("\nOptimal Policy Visualization:")
    for r in range(env.grid_size[0]):
        for c in range(env.grid_size[1]):
            print(policy_grid[r, c], end=' ')
        print()

    # Plot rewards per episode
    plt.plot(rewards)
    plt.xlabel("Episode")
    plt.ylabel("Total Reward")
    plt.title("Total Reward per Episode during Training")
    plt.grid(True)
    plt.show()
