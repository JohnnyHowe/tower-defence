import pygame
from window import Window
from game_grid import GameGrid
from game_window import GameWindow
from event_handler import EventHandler

from wall import Wall


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
                cell = self.game_window.get_mouse_cell()
                if self.board.is_empty(cell):
                    self.board.set_at(cell, Wall(cell))
            if event.button == 3:
                cell = self.game_window.get_mouse_cell()
                self.board.clear_at(cell)

    def draw(self):
        self.game_window.draw_background()

        if pygame.mouse.get_focused():
            pygame.draw.rect(Window.surface, (0, 255, 0), self.game_window.get_cell_pixel_rect(self.game_window.get_mouse_cell()))

        for tower in self.board.get_all():
            # pygame.draw.rect(Window.surface, (0, 0, 255), self.game_window.get_cell_pixel_position(tower.position) + (0.8 * self.game_window.get_cell_pixel_size(),) * 2)
            image = tower.get_image()
            image = pygame.transform.scale(image, (int(self.game_window.get_cell_pixel_size()),) * 2)
            Window.surface.blit(image, self.game_window.get_cell_pixel_position(tower.position))

        self.game_window.draw() 