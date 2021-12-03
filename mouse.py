import pygame
from enum import Enum
from engine_math import Vector2
from window import Window


class MouseButton:
    LEFT = 0
    MIDDLE = 1
    RIGHT = 2


class _Mouse:

    buttons = []
    last_buttons = []

    position: Vector2
    last_position: Vector2 

    def __init__(self):
        self.buttons = [0, 0, 0]
        self.last_buttons = [0, 0, 0]
        self.position = Vector2(0, 0)
        self.last_position = Vector2(0, 0)

    def update(self):
        self.last_buttons = self.buttons
        self.buttons = pygame.mouse.get_pressed()

        self.last_position = self.position.get_copy()
        mouse_pos_tuple = pygame.mouse.get_pos()
        self.position.x = mouse_pos_tuple[0]
        self.position.y = mouse_pos_tuple[1]
    
    @staticmethod
    def is_focused():
        return pygame.mouse.get_focused()

    # =========================================================================
    # buttons
    # =========================================================================

    def get_pressed(self, button):
        return self.buttons[button]

    def get_button_change(self, button):
        return self.last_buttons[button] - self.buttons[button]

    def get_mouse_up(self, button):
        return self.get_button_change(button) == -1

    def get_mouse_down(self, button):
        return self.get_button_change(button) == 1

    # =========================================================================
    # position
    # =========================================================================

    def get_position(self) -> Vector2:
        return self.position

    def get_position_change(self) -> Vector2:
        return self.position - self.last_position


Mouse = _Mouse()
