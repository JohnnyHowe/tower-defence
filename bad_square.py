import pygame
from camera import Camera
from clock import Clock

from engine_math import Vector2, Rect


class BadSquare:

    position = 0
    speed = 2
    path: list
    health = 1

    def __init__(self, path):
        self.position = 0
        self.path = path

    def draw(self):
        game_position = self.get_game_position() 
        Camera.draw_rect((255, 0, 0), Rect(game_position.x, game_position.y, 1, 1))

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
