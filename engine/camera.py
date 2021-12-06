import pygame
import math
from engine.vector2 import Vector2
from engine.rect import Rect

from engine.window import Window


class _Camera:
    def __init__(self) -> None:
        self.position = Vector2(0, 0)
        self.aspect_ratio = Vector2(1, 1)
        self.size = 10  # how many game units on min(screen size)

    # =========================================================================
    # Drawing
    # =========================================================================

    def draw_rect(self, color: tuple, game_rect: Rect, outline_width=None) -> None:
        """ Draw a solid rectangle in game space at game_rect. """
        if outline_width is None:
            pygame.draw.rect(Window.surface, color, self.get_pixel_rect(game_rect).get_pygame_tuple())
        else:
            pygame.draw.rect(Window.surface, color, self.get_pixel_rect(game_rect).get_pygame_tuple(), outline_width * self.get_pixels_per_unit())

    def draw_image(self, image: pygame.Surface, rect: Rect, rotation=0) -> None:
        """ Draw the image in game space at rect.
        Rotation is applied after scaling, so that the width and height specified will not be the
        final width and height on the world x and y axes. """
        pixel_size = self.get_pixel_size(rect.get_size())
        center_position = self.get_pixel_position(rect.get_center())

        scaled_image = pygame.transform.scale(image, pixel_size.get_rounded_tuple())
        rotated_image = pygame.transform.rotate(scaled_image, rotation * 180 / math.pi)

        rotated_rect = rotated_image.get_rect()
        top_left = center_position.x - rotated_rect.w / 2, center_position.y - rotated_rect.h / 2

        Window.surface.blit(rotated_image, top_left)

    def draw_line(self, color: tuple, p1: Vector2, p2: Vector2, width=0.1) -> None:
        pygame.draw.line(Window.surface, color, self.get_pixel_position(p1).get_rounded_tuple(), self.get_pixel_position(p2).get_rounded_tuple(), int(self.get_pixels_per_unit() * width))

    def draw_circle(self, color: tuple, position: Vector2, radius: float) -> None:
        pygame.draw.circle(Window.surface, color, tuple(self.get_pixel_position(position)), self.get_pixels_per_unit() * radius)

    # =========================================================================
    # Math
    # =========================================================================

    def get_window_scale(self) -> float:
        aspect = self.aspect_ratio.x / self.aspect_ratio.y
        return min(Window.size.x, Window.size.y * aspect)

    def get_pixels_per_unit(self) -> float:
        return self.get_window_scale() / self.size

    def get_pixel_position(self, game_position: Vector2) -> Vector2:
        pixels_per_unit = self.get_pixels_per_unit()
        return Vector2(
            Window.size.x / 2 + (game_position.x - self.position.x) * pixels_per_unit,
            Window.size.y / 2 - (game_position.y - self.position.y) * pixels_per_unit,
        )

    def get_pixel_size(self, game_size: Vector2) -> Vector2:
        pixels_per_unit = self.get_pixels_per_unit()
        return Vector2(game_size.x * pixels_per_unit, game_size.y * pixels_per_unit)

    def get_pixel_rect(self, game_rect: Rect) -> Rect:
        center_position = self.get_pixel_position(game_rect.get_center())
        size = self.get_pixel_size(game_rect.get_size())
        return Rect(center_position.x, center_position.y - size.y, size.x, size.y)

    def get_world_position(self, pixel_position: Vector2) -> Vector2:
        pixels_per_unit = self.get_pixels_per_unit()
        return Vector2(
            (pixel_position.x - Window.size.x / 2) / pixels_per_unit + self.position.x,
            -(pixel_position.y - Window.size.y / 2) / pixels_per_unit + self.position.y
        )


Camera = _Camera()
