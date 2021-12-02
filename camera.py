import pygame
import math

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

    def draw_image(self, image, rect, rotation=0):
        pixel_size = list(self.get_pixel_size(rect[2:]))
        center_position = self.get_pixel_position((rect[0] + rect[2] / 2, rect[1] + rect[3] / 2))
        scaled_image = pygame.transform.scale(image, pixel_size)
        rotated_image = pygame.transform.rotate(scaled_image, rotation * 180 / math.pi)
        rotated_rect = rotated_image.get_rect()
        top_left = center_position[0] - rotated_rect.w / 2, center_position[1] - rotated_rect.h / 2
        Window.surface.blit(rotated_image, top_left)

    def draw_line(self, color, p1, p2, width=0.1):
        cp1 = (p1[0] + 0.5, p1[1] + 0.5)
        cp2 = (p2[0] + 0.5, p2[1] + 0.5)
        pygame.draw.line(Window.surface, color, self.get_pixel_position(cp1), self.get_pixel_position(cp2), int(self.get_pixels_per_unit() * width))

    def draw_circle(self, color, position, radius):
        pygame.draw.circle(Window.surface, color, self.get_pixel_position(position), self.get_pixels_per_unit() * radius)

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