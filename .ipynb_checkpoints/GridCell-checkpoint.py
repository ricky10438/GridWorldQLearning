import pygame
from sys import exit
import numpy as np

class GridCell(pygame.sprite.Sprite):
    
    def __init__(self, x, y, special_coords):
        """Initialise grid cell with position and image.

        Args:
            x (int): The x-coordinate of the grid cell.
            y (int): The y-coordinate of the grid cell.
            special_coords (list of tuple): A list of coordinates to be rendered as red squares.
        """
        super().__init__()
    
        if np.array_equal(np.array([x, y]), special_coords):
            self.image = pygame.Surface((50, 50))  
            self.image.fill((255, 0, 0)) 
        else:
            # Load the regular floor image
            self.image = pygame.image.load('images/floor.png')
        
        self.x_pos = x
        self.y_pos = y
        # Set the rectangle for the image
        self.rect = self.image.get_rect(topleft=(x, y))
