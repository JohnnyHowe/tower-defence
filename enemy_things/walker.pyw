import math


class Enemy:

    def __init__(self, path):
        self.path = path
        self.path_length = len(path)
        self.dist = 0
        self.speed = 3
        self.id = 'walker'
        self.health = 10


    def update(self, dt):
        return self.move(dt)


    def move(self, dt):
        dist_to_travel = self.speed * dt
        new_dist = self.dist + dist_to_travel
        self.dist = new_dist
        
        if self.dist > self.path_length:
            return True


    def get_pos(self):
        
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
        angle = 0

        
        position = list(last_full)
        
        position[0] += x_change
        position[1] += y_change

        return position, angle