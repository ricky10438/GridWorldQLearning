import pygame 
from sys import exit

class Player(pygame.sprite.Sprite): 
    
    def __init__(self, x, y):
        """Initialise player with position and image."""
        super().__init__()
        self.image = pygame.image.load('images/naruto_head.png')
        self.x_pos = x
        self.y_pos = y
        self.CELL_DIM = 50
        self.reward = 0
        # Set the position and rect
        # Get the original width and height
        original_width, original_height = self.image.get_size()
        # Calculate the new dimensions maintaining aspect ratio
        scale_factor = 0.095
        new_width = int(original_width * scale_factor)
        new_height = int(original_height * scale_factor)
        
        # Scale the image
        self.image = pygame.transform.scale(self.image, (new_width, new_height))
        self.rect = self.image.get_rect(topleft=(self.x_pos, self.y_pos))