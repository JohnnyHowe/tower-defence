
class Enemy:

    def __init__(self, path):
        self.path = path
        self.speed = 5
        self.x, self.y = path[0]

    last_pos_index = 0
    def move(self):

        # get to next spot
        next_pos_index = self.last_pos_index + 1
        next_pos = self.path[next_pos_index]