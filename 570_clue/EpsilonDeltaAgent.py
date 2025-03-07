import gym
import numpy as np
import pickle

from ClueEnv import ClueEnv
from collections import defaultdict

def default_q_values():
    return {}


class EpsilonDeltaAgent:
    def __init__(
            self,
            env: gym.Env,
            learning_rate: float,
            initial_epsilon: float,
            epsilon_decay: float,
            final_epsilon: float,
            discount_factor: float = 0.95,
    ):
        self.env = env


        self.q_values = defaultdict(default_q_values)

        self.lr = learning_rate
        self.discount_factor = discount_factor

        self.epsilon = initial_epsilon
        self.epsilon_decay = epsilon_decay
        self.final_epsilon = final_epsilon

        self.training_error = []

    def get_action(self, obs: np.ndarray) -> tuple[int, int, int, int]:
        """
        Returns the best action with probability (1 - epsilon),
        otherwise a random action with probability epsilon.
        """
        print("Obs: ")
        print(obs)
        obs_key = tuple(obs)  # Convert array to tuple for hashing

        if np.random.random() < self.epsilon:
            return self.env.action_space.sample()
        else:
            if self.q_values[obs_key]:  # Check if Q-values exist for this state
                return max(self.q_values[obs_key], key=self.q_values[obs_key].get)
            else:
                return self.env.action_space.sample()

    def update(
            self,
            obs: np.ndarray,
            action: tuple[int, int, int, int],
            reward: float,
            terminated: bool,
            next_obs: np.ndarray,
    ):
        """Updates the Q-value of an action."""
        obs_key = tuple(obs)  # Convert array to tuple for hashing
        next_obs_key = tuple(next_obs)

        if action not in self.q_values[obs_key]:
            self.q_values[obs_key][action] = 0.0  # Initialize if not present

        future_q_value = (not terminated) * max(self.q_values[next_obs_key].values(), default=0.0)
        temporal_difference = (
                reward + self.discount_factor * future_q_value - self.q_values[obs_key][action]
        )

        self.q_values[obs_key][action] += self.lr * temporal_difference
        self.training_error.append(temporal_difference)


    def decay_epsilon(self):
            self.epsilon = max(self.final_epsilon, self.epsilon - self.epsilon_decay)



# hyperparameters
learning_rate = 0.01
n_episodes = 100_000
start_epsilon = 1.0
epsilon_decay = start_epsilon / (n_episodes / 2)  # reduce the exploration over time
final_epsilon = 0.1

env = ClueEnv()
#env = gym.wrappers.RecordEpisodeStatistics(env, buffer_length=n_episodes)

agent = EpsilonDeltaAgent(
env=env,
    learning_rate=learning_rate,
    initial_epsilon=start_epsilon,
    epsilon_decay=epsilon_decay,
    final_epsilon=final_epsilon,
)

from tqdm import tqdm

current_obs = np.zeros(env.observation_space.shape)  # Initialize as a zero vector
print("First obs: ")
print(current_obs)

for episode in tqdm(range(n_episodes)):
    terminated = False
    if env.game_over:
        obs = env.reset()
        current_obs = obs  # Ensure obs is an array

    while not terminated:
        action = agent.get_action(current_obs)
        obs, reward, done, info = env.step(action)

        agent.update(current_obs, action, reward, done, obs)

        terminated = done
        current_obs = obs  # Update to new observation

    agent.decay_epsilon()

with open("trained_model.pkl", "wb") as f:
    pickle.dump(dict(agent.q_values), f)  # Convert defaultdict to dict

print("Training complete. Model saved as trained_model.pkl.")

agent.epsilon = 0.0





