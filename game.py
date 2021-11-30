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
        self.board = GameGrid((20, 10))
        self.game_window = GameWindow(self.board.size)

    def update(self):
        EventHandler.update()

        # place towers
        keys_pressed = pygame.key.get_pressed()
        if keys_pressed[pygame.K_LSHIFT]:
            if pygame.mouse.get_pressed()[0]:
                self.try_place_tower(self.game_window.get_mouse_cell())
            elif pygame.mouse.get_pressed()[2]:
                self.board.clear_at(self.game_window.get_mouse_cell())
        else:
            for event in EventHandler.get_events(pygame.MOUSEBUTTONDOWN):
                if event.button == 1:
                    self.try_place_tower(self.game_window.get_mouse_cell())
                if event.button == 3:
                    self.board.clear_at(self.game_window.get_mouse_cell())
 
    def try_place_tower(self, cell):
        if self.board.is_empty(cell):
            self.board.set_at(cell, Wall(cell))

    def draw(self):
        self.game_window.draw_background()

        if pygame.mouse.get_focused():
            pygame.draw.rect(Window.surface, (0, 255, 0), self.game_window.get_cell_pixel_rect(self.game_window.get_mouse_cell()))

        for tower in self.board.get_all():
            image = tower.get_image(self.board)
            image = pygame.transform.scale(image, (int(self.game_window.get_cell_pixel_size()),) * 2)
            Window.surface.blit(image, self.game_window.get_cell_pixel_position(tower.position))

        # show path
        path = self.board.get_path()
        if path is not None:
            for i in range(len(path) - 1):
                pos1 = self.game_window.get_cell_pixel_position(path[i])
                pos2 = self.game_window.get_cell_pixel_position(path[i + 1])
                size = self.game_window.get_cell_pixel_size()
                pygame.draw.line(Window.surface, (255, 0, 0), (pos1[0] + size / 2, pos1[1] + size / 2), (pos2[0] + size / 2, pos2[1] + size / 2), 3)

        self.game_window.draw() 