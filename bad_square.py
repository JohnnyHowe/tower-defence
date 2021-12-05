import pygame
from camera import Camera
from clock import Clock

from engine_math import Vector2, Rect


class BadSquare:

    position = 0
    speed = 2
    path: list
    health: float
    max_health = 100

    def __init__(self, path):
        self.position = 0
        self.path = path
        self.health = self.max_health

    def draw(self):
        Camera.draw_rect((255, 0, 0), self.get_rect())
        self.draw_health()

    def draw_health(self):
        width = 1
        height = 0.1
        game_position = self.get_game_position() + Vector2(0, 1)
        Camera.draw_rect((255, 0, 0), Rect(game_position.x, game_position.y, width, height))
        green_width = width * self.health / self.max_health
        Camera.draw_rect((0, 255, 0), Rect(game_position.x + (width - green_width) / 2, game_position.y, green_width, height))

    def update(self):
        self.move()

    def get_game_position(self) -> Vector2:
        t = self.position 
        if t >= len(self.path) - 1:
            return Vector2(self.path[-1].x + 0.5, self.path[-1].y + 0.5)
        p1 = self.path[int(t)]
        p2 = self.path[int(t) + 1]
        dp = p2 - p1
        mt = t % 1
        return Vector2(p1.x + dp.x * mt + 0.5, p1.y + dp.y * mt + 0.5)

    def move(self):
        self.position += self.speed * Clock.dt
        
    def get_rect(self):
        game_position = self.get_game_position() 
        return Rect(game_position.x, game_position.y, 1, 1)
