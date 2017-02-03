from pygame import *
import global_functions as gfunc
import math

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
    def get_pos(self, dist = None):
        if not dist: return gfunc.get_pos_on_path(self.path, self.dist)
        else: return gfunc.get_pos_on_path(self.path, dist)

    # Show the enemy
    def show(self, window, window_scale):

        # Get blit pos and scale
        current_pos = self.get_pos()
        pos = list(current_pos)
        pos[0] *= window_scale
        pos[1] *= window_scale

        # Scale image to fit the correct amount of space
        img = transform.scale(self.image, (int(window_scale),) * 2)
        old_rect = img.get_rect()

        # Add the rotation
        next_dist = self.dist + 0.7
        next_pos = self.get_pos(dist = next_dist)

        xc = current_pos[0] - next_pos[0]
        yc = current_pos[1] - next_pos[1]

        rads = math.atan2(-yc, xc)
        rads %= 2 * math.pi

        img = transform.rotate(img, math.degrees(rads))

        # Add the sway
        rot = math.sin(self.dist * 4) * 5 # Sin because the curve resembles the wanted swaying motion
        img = transform.rotate(img, rot)

        rect = img.get_rect()
        change = (rect.width - old_rect.width) / 2, (rect.height - old_rect.height) / 2

        pos[0] -= change[0]
        pos[1] -= change[1]

        # Show
        window.blit(img, pos)
