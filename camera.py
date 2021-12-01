import pygame

from window import Window


class _Camera:
    def __init__(self):
        self.position = [0, 0]
        self.aspect_ratio = [1, 1]
        self.size = 10  # how many game units on min(screen size)

    # =========================================================================
    # Drawing
    # =========================================================================

    def draw_rect(self, color, game_rect):
        pygame.draw.rect(Window.surface, color, self.get_pixel_rect(game_rect))

    def draw_image(self, image, rect):
        pixel_size = self.get_pixel_size(rect[2:])
        pixel_position = self.get_pixel_position(rect[:2])
        Window.surface.blit(pygame.transform.scale(image, pixel_size), pixel_position)

    # =========================================================================
    # Math
    # =========================================================================

    def get_window_scale(self):
        aspect = self.aspect_ratio[0] / self.aspect_ratio[1]
        return min(Window.size[0], Window.size[1] * aspect)

    def get_pixels_per_unit(self):
        return self.get_window_scale() / self.size

    def get_pixel_position(self, game_position):
        return tuple(int(i) for i in self.get_perfect_pixel_position(game_position))

    def get_pixel_size(self, game_size):
        return tuple(int(i) for i in self.get_perfect_pixel_size(game_size))

    def get_pixel_rect(self, game_rect):
        return tuple(int(i) for i in self.get_perfect_pixel_rect(game_rect))

    def get_perfect_pixel_position(self, game_position):
        pixels_per_unit = self.get_pixels_per_unit()
        return (
            Window.size[0] / 2 + (game_position[0] - self.position[0]) * pixels_per_unit,
            Window.size[1] / 2 - (game_position[1] - self.position[1]) * pixels_per_unit,
        )

    def get_perfect_pixel_size(self, game_size):
        pixels_per_unit = self.get_pixels_per_unit()
        return game_size[0] * pixels_per_unit, game_size[1] * pixels_per_unit

    def get_perfect_pixel_rect(self, game_rect):
        return self.get_pixel_position(game_rect[:2]) + self.get_pixel_size(game_rect[2:])

    def get_world_position(self, pixel_position):
        pixels_per_unit = self.get_pixels_per_unit()
        return (
            (pixel_position[0] - Window.size[0] / 2) / pixels_per_unit + self.position[0],
            -(pixel_position[1] - Window.size[1] / 2) / pixels_per_unit + self.position[1]
        )


Camera = _Camera()