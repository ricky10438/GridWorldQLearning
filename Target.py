import pygame 

class Target(pygame.sprite.Sprite): 
    """A class to represent the target in the game.

    Attributes:
        image (Surface): The image representing the target.
        x_pos (int): The x-coordinate of the target's position.
        y_pos (int): The y-coordinate of the target's position.
        CELL_DIM (int): The dimension of each cell in the grid.
        rect (Rect): The rectangle defining the position and size of the image.
    """

    def __init__(self, x, y):
        """Initialises the target with a position and an image.

        Args:
            x (int): The x-coordinate of the target's position.
            y (int): The y-coordinate of the target's position.
        """
        super().__init__()
        self.image = pygame.image.load('images/ramen.png')
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
