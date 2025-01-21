from collections import defaultdict
import gymnasium as gym 
import numpy as np 

class GymWorldAgent: 
    def __init__(
            self, 
            env: gym.Env, 
            learning_rate: float, 
            initial_epsilon: float,
            epsilon_decay: float, 
            final_epsilon: float, 
            discount_factor: float = 1,
        ):
        
        self.env = env 
        self.q_values = defaultdict(lambda: np.zeros(env.action_space.n))
        self.lr = learning_rate
        self.discount_factor = discount_factor 
        
        self.epsilon = initial_epsilon
        self.epsilon_decay = epsilon_decay
        self.final_epsilon = final_epsilon
        
        self.training_error = []
        
    def get_action(self, obs: dict) -> int:
        """
        Returns the best action with probability (1 - epsilon)
        otherwise a random action with probability epsilon to ensure exploration.
        """
        # Convert the obs dictionary to a tuple for compatibility with q_values lookup
        obs_tuple = (obs["agent"], obs["target"])
    
        # With probability epsilon, return a random action to explore the environment
        if np.random.random() < self.epsilon:
            return self.env.action_space.sample()
        # With probability (1 - epsilon), act greedily (exploit)
        else:
            return int(np.argmax(self.q_values[obs_tuple]))
        
    def update(
        self,
        obs: dict,
        action: int,
        reward: float,
        terminated: bool,
        next_obs: dict,
    ):
        obs_tuple = (obs["agent"], obs["target"])
        next_obs_tuple = (next_obs["agent"], next_obs["target"])
        future_q_value = (not terminated) * np.max(self.q_values[next_obs_tuple])
        temporal_difference = (
            reward + self.discount_factor * future_q_value - self.q_values[obs_tuple][action]
        )

        self.q_values[obs_tuple][action] = (
            self.q_values[obs_tuple][action] + self.lr * temporal_difference
        )
        self.training_error.append(temporal_difference)

    def decay_epsilon(self):
        self.epsilon = max(self.final_epsilon, self.epsilon - self.epsilon_decay)

        
        
        