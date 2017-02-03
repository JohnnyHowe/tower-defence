from data import global_functions as gfunc
from pygame import *

class Enemy:

    def __init__(self, scale, speed, time_until_spawn):

        self.id = 'walker'

        self.speed = speed
        self.scale = scale

        # Negative distance will be treated as the time left until the enemy will spawn
        self.dist = -time_until_spawn

        # Load image
        self.image = image.load('images\\enemies\\walker.png')

    def update(self, window, window_scale, dt):
        self.move(dt)
        self.show(window, window_scale)

    # This will allow the init function to be called before the fight stage so all the images can be loaded in at the start
    def set(self, path):
        self.path = path

    # Enable the enemy to move
    def move(self, dt):
        self.dist += dt * self.speed

    # Change the distance integer to a position on the path
    def get_pos(self):
        return gfunc.get_pos_on_path(self.path, self.dist)

    # Show the enemy
    def show(self, window, window_scale):

        # Get blit pos and scale
        pos = self.get_pos()
        pos[0] *= window_scale
        pos[1] *= window_scale

        # Scale image to fit the correct amount of space
        img = transform.scale(self.image, (int(window_scale),) * 2)
        window.blit(img, pos)
