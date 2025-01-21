import pygame 
from sys import exit 

class GridCell(pygame.sprite.Sprite): 
    """A class to represent a grid cell in a game.

    Attributes:
        image (Surface): The image representing the grid cell.
        x_pos (int): The x-coordinate of the grid cell.
        y_pos (int): The y-coordinate of the grid cell.
        rect (Rect): The rectangle defining the position and size of the image.
    """

    def __init__(self, x, y):
        """Initialises a grid cell with a position and an image.

        Args:
            x (int): The x-coordinate of the grid cell.
            y (int): The y-coordinate of the grid cell.
        """
        super().__init__()
        self.image = pygame.image.load('images/floor.png')
        self.x_pos = x
        self.y_pos = y
        # Set the rectangle for the image
        self.rect = self.image.get_rect(topleft=(x, y))
        
    
    
    
        
    
        
    
        
        
    
        