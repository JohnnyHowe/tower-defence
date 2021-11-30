import pygame
from window import Window


class GameWindow:
    """ Specialized window specifically for the game scene.
    Unlike Window, this is not a singleton. """
    tower_selector_height = 1
    board_size = None

    def __init__(self, board_size):
        self.board_size = board_size

    def get_mouse_cell(self, check_in_bounds=True):
        return self.get_pixel_cell_position(pygame.mouse.get_pos(), check_in_bounds)

    def draw_background(self):
        scale = self.get_cell_pixel_size()

        game_display_size = self.board_size[0] * scale, self.board_size[1] * scale
        game_display_position = (
            (Window.size[0] - game_display_size[0]) / 2,
            (Window.size[1] - game_display_size[1] - scale * self.tower_selector_height) / 2
        )
        pygame.draw.rect(Window.surface, (255, 255, 255), game_display_position + game_display_size)

        selector_display_size = game_display_size[0], scale * self.tower_selector_height
        selector_display_position = game_display_position[0], game_display_position[1] + game_display_size[1]
        pygame.draw.rect(Window.surface, (200, 200, 200), selector_display_position + selector_display_size)

    def draw(self):
        pygame.display.update()

    def get_cell_pixel_position(self, cell_position):
        scale = self.get_cell_pixel_size()
        game_display_size = self.board_size[0] * scale, self.board_size[1] * scale
        game_display_position = (
            (Window.size[0] - game_display_size[0]) / 2,
            (Window.size[1] - game_display_size[1] -
            scale * self.tower_selector_height) / 2
        )
        return game_display_position[0] + cell_position[0] * scale, game_display_position[1] + cell_position[1] * scale

    def get_cell_pixel_size(self):
        return min(Window.size[0] / self.board_size[0], Window.size[1] / (self.board_size[1] + self.tower_selector_height))

    def get_cell_pixel_rect(self, cell_position):
        return self.get_cell_pixel_position(cell_position) + (self.get_cell_pixel_size(),) * 2

    def get_pixel_cell_position(self, pixel_position, check_in_bounds=True):
        top_left = self.get_cell_pixel_position((0, 0))
        scale = self.get_cell_pixel_size()
        cell_position = (
            int((pixel_position[0] - top_left[0]) / scale),
            int((pixel_position[1] - top_left[1]) / scale)
        )
        if (check_in_bounds and (
                cell_position[0] < 0 or cell_position[0] > self.board_size[0] - 1 or
                cell_position[1] < 0 or cell_position[1] > self.board_size[1] - 1 or
                pixel_position[0] < top_left[0] or
                pixel_position[1] < top_left[1])):
            return -1, -1
        return cell_position
