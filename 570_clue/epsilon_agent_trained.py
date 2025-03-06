import gym
import pickle
from ClueEnv import ClueEnv  # Ensure this is accessible
from collections import defaultdict

class EpsilonDeltaAgent:
    def __init__(self, env: gym.Env):
        self.env = env
        self.q_values = defaultdict(dict)  # Initialize empty Q-table
        self.epsilon = 0.0  # No exploration during testing

    def load_q_values(self, filename: str):
        """Load trained Q-values from a pickle file."""
        with open(filename, "rb") as f:
            self.q_values = pickle.load(f)

    def get_action(self, obs):
        """Choose the best action based on learned Q-values."""
        if obs in self.q_values and self.q_values[obs]:
            return max(self.q_values[obs], key=self.q_values[obs].get)  # Greedy action
        else:
            return self.env.action_space.sample()  # If state unknown, take random action

# Initialize environment
env = ClueEnv()

# Load trained agent
agent = EpsilonDeltaAgent(env)
agent.load_q_values("trained_model.pkl")  # Load Q-values

# Test the trained model
obs, info = env.reset()
done = False
total_reward = 0
num_wins = 0

print("Testing trained agent...")

for _ in range(100):
    while not done:
        action = agent.get_action(obs)  # Pick best action
        # print(f"Agent takes action: {action}")

        obs, reward, done, info = env.step(action)
        total_reward += reward
    if env.won:
        num_wins += 1

print("Agent won: " + str(num_wins) +" times out of 100")

    #print(f"New observation: {obs}, Reward: {reward}, Done: {done}")

#print(f"Game over! Total reward: {total_reward}")
