import pygame
from engine.vector2 import Vector2


class _Window:
    """ Main window class. Everything that does any drawing or window related things must reference
    this somewhere down the chain.
    
    Contains the pygame surface used for displaying things. 
    
    Is singleton but because of python module gunk you don't need to use .get_instance, just Window. """
    size: Vector2
    surface: pygame.Surface

    def __init__(self):
        self.update_size(Vector2(500, 500))

    def update_size(self, new_size: Vector2) -> None:
        self.size = new_size
        self.surface = pygame.display.set_mode(self.size.get_rounded_tuple(), pygame.RESIZABLE)


Window = _Window()
