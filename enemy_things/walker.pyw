from pygame import *
import math

class Enemy:

    def __init__(self, path):
        self.path = path
        self.path_length = len(path)
        self.dist = 0
        self.speed = 3
        self.id = 'walker'
        self.health = 10
        self.max_health = 10
        self.tick = 0
        self.pos = None
        self.img = image.load('images\\enemies\\walker.png')

    def update(self, dt, playing_grid, window, window_scale):
        self.tick += dt
        self.move(dt, playing_grid)
        self.show(window, window_scale)

    def show(self, window, window_scale):
        pos, angle = self.get_info()
        center_pos = list(pos)

        try:            
            center_pos[0] += 0.5; center_pos[1] += 0.5
            center_pos[0] *= window_scale; center_pos[1] *= window_scale

            img = transform.scale(self.img, (window_scale, window_scale))
            img = transform.rotate(img, angle)

            rect = img.get_rect()
            pos = center_pos[0] - rect.width / 2, center_pos[1] - rect.height / 2

            window.blit(img, pos)

        except Exception as error:
            print('WARNGIN DOOD, ERROR SHOWING WALKER')
            print(error)


    def move(self, dt, playing_grid):
        dist_to_travel = self.speed * dt
        new_dist = self.dist + dist_to_travel
        self.dist = new_dist

    def on_path(self, playing_grid):
        
        # Is it past the destination
        try:
            value = self.get_info()[0][0]
        except:
            value = 0

        if value > playing_grid[0]:
            return False
        return False

    def get_rect(self, window_scale):
        pos, angle = self.get_info()

        width = window_scale / 16 * 14

        return pos[0] * window_scale, pos[1] * window_scale, width, width

    def get_info(self):
        
        # where was the last full position?
        last_full = self.path[int(self.dist)][:2]

        # where to go to get to next pos
        next_full = self.path[int(self.dist) + 1][:2]
        x_change = next_full[0] - last_full[0]
        y_change = next_full[1] - last_full[1]

        # go part of the way
        dist_to_go = self.dist - int(self.dist)

        x_change *= dist_to_go
        y_change *= dist_to_go

        # get direction
        next2 = self.path[int(self.dist) + 2][:2]

        if x_change > 0: angle = 0
        elif x_change < 0: angle = 180
        elif y_change > 0: angle = 90
        elif y_change < 0: angle = 270
        else: angle = 0

        # Sin because the curve it creates (on a graph) is what I need for the swaying of the image to make it look like walking. cos would also work
        angle += math.sin(self.tick * 10) * 10
       
        position = list(last_full)
        
        position[0] += x_change
        position[1] += y_change

        self.pos = position

        return position, angle