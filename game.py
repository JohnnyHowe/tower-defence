import pygame
from window import Window
from game_grid import GameGrid

TOWER_SELECTOR_HEIGHT = 2


class Game:

    board = None

    def __init__(self):
        self.board = GameGrid((10, 5))

    def update(self):
        self.event_loop()

    def draw(self):
        scale = self.get_cell_pixel_size()

        game_display_size = self.board.size[0] * scale, self.board.size[1] * scale
        game_display_position = (
            (Window.size[0] - game_display_size[0]) / 2,
            (Window.size[1] - game_display_size[1] - scale * TOWER_SELECTOR_HEIGHT) / 2
        )

        pygame.draw.rect(Window.surface, (255, 255, 255), game_display_position + game_display_size)

        selector_display_size = game_display_size[0], scale * TOWER_SELECTOR_HEIGHT
        selector_display_position = game_display_position[0], game_display_position[1] + game_display_size[1]
        pygame.draw.rect(Window.surface, (200, 200, 200), selector_display_position + selector_display_size)

        if pygame.mouse.get_focused():
            pygame.draw.rect(Window.surface, (0, 255, 0), self.get_cell_pixel_rect(self.get_pixel_cell_position(pygame.mouse.get_pos())))

        pygame.display.update()

    def event_loop(self):
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                quit()
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_ESCAPE:
                    quit()
            if event.type == pygame.VIDEORESIZE:
                Window.update_size((event.w, event.h))


    def get_cell_pixel_position(self, cell_position):
        scale = self.get_cell_pixel_size()
        game_display_size = self.board.size[0] * scale, self.board.size[1] * scale
        game_display_position = (
            (Window.size[0] - game_display_size[0]) / 2,
            (Window.size[1] - game_display_size[1] -
            scale * TOWER_SELECTOR_HEIGHT) / 2
        )
        return game_display_position[0] + cell_position[0] * scale, game_display_position[1] + cell_position[1] * scale


    def get_cell_pixel_size(self):
        return min(Window.size[0] / self.board.size[0], Window.size[1] / (self.board.size[1] + TOWER_SELECTOR_HEIGHT))


    def get_cell_pixel_rect(self, cell_position):
        return self.get_cell_pixel_position(cell_position) + (self.get_cell_pixel_size(),) * 2


    def get_pixel_cell_position(self, pixel_position):
        top_left = self.get_cell_pixel_position((0, 0))
        scale = self.get_cell_pixel_size()
        cell_position = (
            int((pixel_position[0] - top_left[0]) / scale),
            int((pixel_position[1] - top_left[1]) / scale)
        )
        if (cell_position[0] < 0 or cell_position[0] > self.board.size[0] - 1 or
            cell_position[1] < 0 or cell_position[1] > self.board.size[1] - 1 or
            pixel_position[0] < top_left[0] or
                pixel_position[1] < top_left[1]):
            return -1, -1
        return cell_position
