import pygame
from enum import Enum


class MouseButton:
    LEFT = 0
    MIDDLE = 1
    RIGHT = 2


class _Mouse:

    buttons = []
    last_buttons = []

    position = [0, 0]
    last_position = [0, 0]

    def __init__(self):
        self.buttons = [0, 0, 0]
        self.last_buttons = [0, 0, 0]

    def update(self):
        self.last_buttons = self.buttons
        self.buttons = pygame.mouse.get_pressed()
        self.last_position = self.position
        self.position = pygame.mouse.get_pos()
    
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

    def get_position(self):
        return self.position

    def get_position_change(self):
        return (self.position[0] - self.last_position[0], self.position[1] - self.last_position[1])


Mouse = _Mouse()