import pygame
from camera import Camera
from clock import Clock


class BadSquare:

    position = 0
    speed = 2
    path: list
    health = 1

    def __init__(self, path):
        self.position = 0
        self.path = path

    def draw(self):
        Camera.draw_rect((255, 0, 0), self.get_game_position() + (1, 1))

    def update(self):
        if pygame.key.get_pressed()[pygame.K_SPACE]:
            self.move()

    def get_game_position(self):
        t = self.position 
        if t >= len(self.path) - 1:
            return self.path[-1][0], self.path[-1][1] + 1
        p1 = self.path[int(t)]
        p2 = self.path[int(t) + 1]
        dp = p2[0] - p1[0], p2[1] - p1[1]
        mt = t % 1
        return p1[0] + dp[0] * mt, p1[1] + dp[1] * mt + 1

    def move(self):
        self.position += self.speed * Clock.dt
