import pygame
from window import Window
from game_grid import GameGrid
from game_window import GameWindow


class Game:
    board = None
    game_window = None

    def __init__(self):
        self.board = GameGrid((10, 5))
        self.game_window = GameWindow(self.board.size)

    def update(self):
        self.event_loop()

    def draw(self):
        self.game_window.draw()

    def event_loop(self):
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                quit()
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_ESCAPE:
                    quit()
            if event.type == pygame.VIDEORESIZE:
                Window.update_size((event.w, event.h))

