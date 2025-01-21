import unittest
import numpy as np
import gymnasium as gym
from typing import Optional
from GridWorldEnv import GridWorldEnv

class TestGridWorldEnv(unittest.TestCase):

    def setUp(self):
        """Set up a default environment for testing."""
        self.env = GridWorldEnv(size=5)
        self.env2 = GridWorldEnv(size=5)
        self.env2._agent_location = np.array([4,4], dtype = np.int32)
        

    def test_initialization(self):
        """Test that the environment initializes correctly."""
        self.assertEqual(self.env.size, 5)
        np.testing.assert_array_equal(self.env._agent_location, np.array([-1, 1], dtype=np.int32))
        np.testing.assert_array_equal(self.env._target_location, np.array([-1, 1], dtype=np.int32))

    def test_observation_space(self):
        """Test that the observation space is correctly defined."""
        self.assertIsInstance(self.env.observation_space, gym.spaces.Dict)
        self.assertIn("agent", self.env.observation_space.spaces)
        self.assertIn("target", self.env.observation_space.spaces)

        agent_space = self.env.observation_space["agent"]
        target_space = self.env.observation_space["target"]
        #self.assertTrue(agent_space.contains(np.array([1, 1])))
        #self.assertTrue(agent_space.contains(np.array([3, 2])))
        #self.assertFalse(agent_space.contains(np.array([-1, 0])))
        #self.assertFalse(agent_space.contains(np.array([5, 5])))

    def test_action_space(self):
        """Test that the action space is correctly defined."""
        self.assertIsInstance(self.env.action_space, gym.spaces.Discrete)
        self.assertEqual(self.env.action_space.n, 4)

    def test_action_to_direction_mapping(self):
        """Test the action-to-direction mapping."""
        expected_mapping = {
            0: np.array([1, 0]),
            1: np.array([0, 1]),
            2: np.array([-1, 0]),
            3: np.array([0, -1])
        }
        for action, direction in expected_mapping.items():
            np.testing.assert_array_equal(self.env._action_to_direction[action], direction)
            
    
    def test_get_obs(self): 
        self.assertTrue(np.array_equal(self.env._get_obs()["agent"], np.array([-1, 1], dtype=np.int32)))
        self.assertTrue(np.array_equal(self.env._get_obs()["target"], np.array([-1, 1], dtype=np.int32)))
        
    def test_step(self): 
        self.env2.step(0)
        self.assertTrue(np.array_equal(self.env2._agent_location, np.array([4,4], dtype = np.int32)))
        
    def test_creation(self): 
        gym.register(
            id = "gymnasium_env/GridWord-v0",
            entry_point = GridWorldEnv, 
            )
        gym.make("gymnasium_env/GridWord-v0")
        
    

if __name__ == "__main__":
    unittest.main()
