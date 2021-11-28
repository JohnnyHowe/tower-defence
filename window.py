import pygame


class _Window:
    """ Main window class. Everything that does any drawing or window related things must reference
    this somewhere down the chain.
    
    Contains the pygame surface used for displaying things. 
    
    Is singleton but because of python module gunk you don't need to use .get_instance, just Window. """
    def __init__(self):
        self.size = (500, 500)
        self.surface = pygame.display.set_mode(self.size, pygame.RESIZABLE)

    def update_size(self, new_size):
        self.size = new_size
        self.surface = pygame.display.set_mode(self.size, pygame.RESIZABLE)


Window = _Window()