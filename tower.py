import abc
import pygame
from engine_math import Vector2, Rect


class Tower(abc.ABC):

    position: Vector2

    def __init__(self, position: Vector2, projectile_list: list) -> None:
        self.position = position
        self.projectile_list = projectile_list
        self.__init_subclass__()

    @abc.abstractmethod
    def draw_icon(self, rect: Rect, surface: pygame.Surface) -> None:
        """ Draw an icon of the tower on the surface, taking up the space defined by rect.
        Do not go through the camera for this. This is a UI thing. """

    @abc.abstractmethod
    def draw(self) -> None:
        pass
    
    def update(self, first_enemy):
        pass
