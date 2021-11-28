import pygame
from window import Window
from game_grid import GameGrid
from game_window import GameWindow
from event_handler import EventHandler


class Game:
    board = None
    game_window = None

    def __init__(self):
        self.board = GameGrid((10, 5))
        self.game_window = GameWindow(self.board.size)

    def update(self):
        EventHandler.update()

        for event in EventHandler.get_events(pygame.MOUSEBUTTONDOWN):
            if event.button == 1:
                pass

    def draw(self):
        self.game_window.draw_background()
        if pygame.mouse.get_focused():
            pygame.draw.rect(Window.surface, (0, 255, 0), self.game_window.get_cell_pixel_rect(self.game_window.get_mouse_cell()))
        self.game_window.draw() 