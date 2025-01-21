from typing import Optional 
import numpy as np 
import gymnasium as gym 
import pygame 
from GridCell import GridCell
from Player import Player
from Target import Target

class GridWorldEnv(gym.Env): 
    """A grid world environment for reinforcement learning.

    Attributes:
        metadata (dict): Metadata for the environment, including render modes and FPS.
        size (int): The size of the square grid.
        GRID_WIDTH (int): The width of the grid.
        GRID_HEIGHT (int): The height of the grid.
        CELL_DIM (int): The dimension of each cell in the grid.
        WINDOW_WIDTH (int): The width of the window for rendering.
        WINDOW_HEIGHT (int): The height of the window for rendering.
        _agent_location (ndarray): The current location of the agent.
        _target_location (ndarray): The location of the target.
        grid_cells (Group): The group of grid cell sprites.
        player (GroupSingle): The player sprite.
        target (GroupSingle): The target sprite.
        observation_space (Dict): The observation space of the environment.
        action_space (Discrete): The action space of the environment.
        _action_to_direction (dict): Mapping of actions to direction vectors.
        render_mode (Optional[str]): The mode for rendering the environment.
        window (Optional[Surface]): The window surface for rendering.
        clock (Optional[Clock]): The clock for controlling the frame rate.
    """

    metadata = {"render_modes": ["human", "rgb_array"], "render_fps": 4}
    
    def __init__(self, render_mode=None, size: int = 5): 
        """Initialises the GridWorldEnv with the given parameters.

        Args:
            render_mode (Optional[str]): The mode for rendering the environment.
            size (int): The size of the square grid. Defaults to 5.
        """
        self.size = size
        self.GRID_WIDTH, self.GRID_HEIGHT = size, size
        self.CELL_DIM = 50
        self.WINDOW_WIDTH, self.WINDOW_HEIGHT = self.GRID_WIDTH * self.CELL_DIM, self.GRID_HEIGHT * self.CELL_DIM

        self._agent_location = np.array([0, 0], dtype=np.int32)
        self._target_location = np.array([size-1, size-1], dtype=np.int32)
                
        self.grid_cells = self.__init_grid()
        self.player = self.__init_player()
        self.target = self.__init_target()
        
        self.observation_space = gym.spaces.Dict(
            { 
                "agent": gym.spaces.Box(0, size - 1, shape=(2,)), 
                "target": gym.spaces.Box(0, size - 1, shape=(2,))
            }
        )
        
        self.action_space = gym.spaces.Discrete(4)
        self._action_to_direction = {
            0: np.array([1, 0]), 
            1: np.array([0, 1]), 
            2: np.array([-1, 0]), 
            3: np.array([0, -1])
        }
        
        assert render_mode is None or render_mode in self.metadata["render_modes"]
        self.render_mode = render_mode
        
        self.window = None
        self.clock = None
        
    def _get_obs(self): 
        """Returns the current observation of the environment.

        Returns:
            dict: A dictionary containing the agent and target locations.
        """
        return {
            "agent": self._agent_location, 
            "target": self._target_location 
        }
    
    def _get_info(self): 
        """Returns additional information about the environment.

        Returns:
            dict: A dictionary containing the distance between the agent and the target.
        """
        return {
            "distance": np.linalg.norm(
                self._agent_location - self._target_location, ord=1)
        }
    
    def __init_grid(self):
        """Creates and returns grid cells.

        Returns:
            Group: A group of grid cell sprites.
        """
        grid_cells = pygame.sprite.Group()
        for j in range(self.GRID_HEIGHT):
            y = j * self.CELL_DIM
            for i in range(self.GRID_WIDTH):
                x = i * self.CELL_DIM
                grid_cells.add(GridCell(x + 50, y + 50))
        return grid_cells
    
    def __init_player(self):
        """Creates and returns the player sprite.

        Returns:
            GroupSingle: A group containing the player sprite.
        """
        player = pygame.sprite.GroupSingle()
        x = (self._agent_location[0] + 1) * 50
        y = (self._agent_location[1] + 1) * 50
        player.add(Player(x, y))
        return player
    
    def __init_target(self):
        """Creates and returns the target sprite.

        Returns:
            GroupSingle: A group containing the target sprite.
        """
        target = pygame.sprite.GroupSingle()
        x = (self._target_location[0] + 1) * 50
        y = (self._target_location[1] + 1) * 50
        target.add(Target(x, y))
        return target
    
    def __update_player(self):
        """Updates the player position based on the agent location."""
        player_sprite = self.player.sprite
        player_sprite.rect.topleft = (
            (self._agent_location[0] + 1) * self.CELL_DIM,
            (self._agent_location[1] + 1) * self.CELL_DIM
        )
        
    def __update_target(self):
        """Updates the target position based on the target location."""
        target_sprite = self.target.sprite
        target_sprite.rect.topleft = (
            (self._target_location[0] + 1) * self.CELL_DIM,
            (self._target_location[1] + 1) * self.CELL_DIM
        )
        
    def reset(self, seed: Optional[int] = None, options: Optional[dict] = None): 
        """Resets the environment to an initial state.

        Args:
            seed (Optional[int]): The seed for random number generation.
            options (Optional[dict]): Additional options for resetting.

        Returns:
            tuple: A tuple containing the initial observation and info.
        """
        super().reset(seed=seed)
        
        self._agent_location = self.np_random.integers(0, self.size, size=2, dtype=int)
        self._target_location = self._agent_location 
        while np.array_equal(self._target_location, self._agent_location): 
            self._target_location = self.np_random.integers(
                0, self.size, size=2, dtype=int)   
            
        self.__update_player()
        self.__update_target()
            
        observation = self._get_obs()
        info = self._get_info()
        
        if self.render_mode == "human":
            self._render_frame()
        
        return observation, info
    
    def step(self, action):
        """Takes a step in the environment based on the given action.

        Args:
            action (int): The action to be taken.

        Returns:
            tuple: A tuple containing the observation, reward, termination status, truncation status, and info.
        """
        self.__step_direction(action)
        
        terminated = np.array_equal(self._agent_location, self._target_location)
        truncated = False 
        reward = 1 if terminated else 0 
        self.__update_player()
        observation = self._get_obs()
        info = self._get_info()
        
        if self.render_mode == "human":
            self._render_frame()
        
        return observation, reward, terminated, truncated, info
    
    def __step_direction(self, action):
        """Updates the agent's location based on the action.

        Args:
            action (int): The action to be taken.
        """
        direction = self._action_to_direction[action]
        self._agent_location = np.clip(
            self._agent_location + direction, 0, self.size - 1)
        
    def render(self): 
        """Renders the current state of the environment."""
        if self.render_mode == "rgb_array": 
            return self._render_frame()
        
    def _render_frame(self):
        """Renders a single frame of the environment."""
        if self.window is None and self.render_mode == "human":
            pygame.init()
            pygame.display.init()
            self.window = pygame.display.set_mode((self.WINDOW_WIDTH + 100, self.WINDOW_HEIGHT + 100))
        if self.clock is None and self.render_mode == "human": 
            self.clock = pygame.time.Clock()
            
        LIGHT_BLUE = (173, 216, 230)

        if self.render_mode == "human":
            self.window.fill(LIGHT_BLUE)
            # Draw grid 
            self.grid_cells.draw(self.window)
            self.player.draw(self.window)
            self.target.draw(self.window)
            pygame.display.update()
            self.clock.tick(self.metadata["render_fps"])
        else:  # rgb_array
            canvas = pygame.Surface((self.WINDOW_WIDTH + 100, self.WINDOW_HEIGHT + 100))
            canvas.fill(LIGHT_BLUE)
            self.grid_cells.draw(canvas)
            self.player.draw(canvas)
            self.target.draw(canvas)
            return np.transpose(
                np.array(pygame.surfarray.pixels3d(canvas)), axes=(1, 0, 2)
            )
            
    def close(self):
        """Closes the environment and releases resources."""
        if self.window is not None:
            pygame.display.quit()
            pygame.quit()
            
    
        
    
        
    
        
        
    
    
    
     
        