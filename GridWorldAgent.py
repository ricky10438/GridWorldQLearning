from collections import defaultdict
import gymnasium as gym 
import numpy as np 

class GridWorldAgent: 
    """An agent for interacting with a grid world environment using Q-learning.

    Attributes:
        env (gym.Env): The environment in which the agent operates.
        q_values (defaultdict): A dictionary mapping state-action pairs to Q-values.
        lr (float): The learning rate for Q-value updates.
        discount_factor (float): The discount factor for future rewards.
        epsilon (float): The probability of choosing a random action for exploration.
        epsilon_decay (float): The rate at which epsilon decreases.
        final_epsilon (float): The minimum value of epsilon.
        training_error (list): A list to store the temporal difference errors.
    """

    def __init__(
            self, 
            env: gym.Env, 
            learning_rate: float, 
            initial_epsilon: float,
            epsilon_decay: float, 
            final_epsilon: float, 
            discount_factor: float = 1,
        ):
        """Initialises the GridWorldAgent with the given parameters.

        Args:
            env (gym.Env): The environment in which the agent operates.
            learning_rate (float): The learning rate for Q-value updates.
            initial_epsilon (float): The initial probability of choosing a random action.
            epsilon_decay (float): The rate at which epsilon decreases.
            final_epsilon (float): The minimum value of epsilon.
            discount_factor (float, optional): The discount factor for future rewards. Defaults to 1.
        """
        self.env = env 
        self.q_values = defaultdict(lambda: np.zeros(env.action_space.n))
        self.lr = learning_rate
        self.discount_factor = discount_factor 
        
        self.epsilon = initial_epsilon
        self.epsilon_decay = epsilon_decay
        self.final_epsilon = final_epsilon
        
        self.training_error = []
        
    def get_action(self, obs: dict) -> int:
        """Selects an action based on the current observation.

        With probability epsilon, a random action is chosen to explore the environment.
        Otherwise, the action with the highest Q-value is chosen.

        Args:
            obs (dict): The current observation from the environment.

        Returns:
            int: The action to be taken.
        """
        # Convert the obs dictionary to a tuple for compatibility with q_values lookup
        obs_tuple = (tuple(obs["agent"]), tuple(obs["target"]))
    
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
        """Updates the Q-values based on the agent's experience.

        Args:
            obs (dict): The current observation from the environment.
            action (int): The action taken by the agent.
            reward (float): The reward received after taking the action.
            terminated (bool): Whether the episode has ended.
            next_obs (dict): The next observation from the environment.
        """
        obs_tuple = (tuple(obs["agent"]), tuple(obs["target"]))
        next_obs_tuple = (tuple(next_obs["agent"]), tuple(next_obs["target"]))
        future_q_value = (not terminated) * np.max(self.q_values[next_obs_tuple])
        temporal_difference = (
            reward + self.discount_factor * future_q_value - self.q_values[obs_tuple][action]
        )

        self.q_values[obs_tuple][action] = (
            self.q_values[obs_tuple][action] + self.lr * temporal_difference
        )
        self.training_error.append(temporal_difference)

    def decay_epsilon(self):
        """Decays the epsilon value to reduce exploration over time."""
        self.epsilon = max(self.final_epsilon, self.epsilon - self.epsilon_decay)
        

        
        
        