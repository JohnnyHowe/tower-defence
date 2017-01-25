from pygame import *

img = image.load('images//towers//block.png')
id = 'block'

tower_cost = 20
tower_info = 'Standard block, place towers on it and make enemies take a longer path'

class Tower:

    def __init__(self, pos):
        self.pos = pos
        self.img = img
        self.id = 'block'
        self.refund_value = 20
        self.img = image.load('images//towers//block.png')
        
    def show(self, window, window_scale, *args):
        window.blit(transform.scale(self.img, (window_scale, window_scale)), (self.pos[0] * window_scale, self.pos[1] * window_scale))

    def reset(self):
        pass

    def do_damage(self, enemies, *args):
        return enemies

    def update(self, *dont_care):
        pass