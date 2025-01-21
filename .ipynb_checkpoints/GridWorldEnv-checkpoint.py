from typing import Optional 
import numpy as np 
import gymnasium as gym 
import pygame 
from GridCell import GridCell
from Player import Player

class GridWorldEnv(gym.Env): 
    metadata = {"render_modes": ["human", "rgb_array"], "render_fps": 4}
    
    def __init__(self, render_mode = None, size: int = 5): 
        self.size = size  # The size of the square grid
        self.GRID_WIDTH, self.GRID_HEIGHT = size, size
        self.CELL_DIM = 50
        self.WINDOW_WIDTH, self.WINDOW_HEIGHT = self.GRID_WIDTH * self.CELL_DIM, self.GRID_HEIGHT * self.CELL_DIM
        
        self.grid_cells = self.__init_grid()
        self.player = self.__init_player()
        
        self._agent_location = np.array([-1, 1], dtype = np.int32)
        self._target_location = np.array([-1, 1], dtype = np.int32)
        
        self.observation_space = gym.spaces.Dict(
            { 
                "agent" : gym.spaces.Box(0, size - 1, shape = (2,)), 
                "target" : gym.spaces.Box(0, size - 1, shape = (2,))
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
        return {
            "agent": self._agent_location, 
            "target": self._target_location 
            }
    
    
    def _get_info(self): 
        return {
            "distance": np.linalg.norm(
                self._agent_location - self._target_location, ord = 1)
            }
    
    def __init_grid(self):
        """Create and return grid cells."""
        special_cordinates = (self.target_location + 1) * 50
        grid_cells = pygame.sprite.Group()
        for j in range(self.GRID_HEIGHT):
            y = j * self.CELL_DIM
            for i in range(self.GRID_WIDTH):
                x = i * self.CELL_DIM
                grid_cells.add(GridCell(x + 50, y + 50, special_cordinates))
        return grid_cells
    
    def __init_player(self):
        """Create and return player sprite."""
        player = pygame.sprite.GroupSingle()
        x = (self._agent_location[0] + 1) * 50
        y = x = (self._agent_location[1] + 1) * 50
        player.add(Player(x, y))
        return player
    
    def reset(self, seed: Optional[int] = None, options: Optional[dict] = None): 
        super().reset(seed = seed)
        
        self._agent_location = self.np_randoms.integers(0, self.size, size = 2, dtype=int)
        self._target_location = self._agent_location 
        while np.array_equal(self._target_location, self._agent_location): 
            self._target_location = self.np_random.integers(
                0, self.size, size = 2, dtype = int)
            
        observation = self._get_obs()
        info = self._get_info()
        
        if self.render_mode == "human":
            self._render_frame()
        
        return observation, info
    
    def step(self, action):
        self.__step_direction(action)
        
        terminated = np.array_equal(self._agent_location, self._target_location)
        truncated = False 
        reward = 1 if terminated else 0 
        observation = self._get_obs()
        info = self._get_info()
        
        if self.render_mode == "human":
            self._render_frame()
        
        return observation, reward, terminated, truncated, info
    
    
    def __step_direction(self, action):
        direction = self._action_to_direction[action]
        self._agent_location = np.clip(
            self._agent_location + direction, 0, self.size - 1)
        
    def render(self): 
        if self.render_mode == "rgb_array": 
            return self._render_frame()
        
    def _render_frame(self):
        if self.window is None and self.render_mode == "human":
            pygame.init()
            pygame.display.init()
            self.window = pygame.display.set_mode((self.WINDOW_WIDTH + 100, self.WINDOW_HEIGHT + 100))
        if self.clock is None and self.render_mode == "human": 
            self.clock = pygame.time.Clock()
            
        LIGHT_BLUE = (173, 216, 230)
        self.window.fill(LIGHT_BLUE)
        
        # Draw grid 
        self.grid_cells.draw(self.window)
        self.player.draw(self.window)
        
        if self.render_mode == "human":
            self.grid_cells.update()
            self.player.update()
            pygame.display.update()
            self.clock.tick(self.metadata["render_fps"])
        else:  # rgb_array
            canvas = pygame.Surface((self.WINDOW_WIDTH + 100, self.WINDOW_HEIGHT + 100))
            canvas.fill(LIGHT_BLUE)
            self.grid_cells.draw(canvas)
            self.player.draw(canvas)
            return np.transpose(
                np.array(pygame.surfarray.pixels3d(canvas)), axes=(1, 0, 2)
            )
            
        
    
        
    
        
    
        
        
    
    
    
     
        