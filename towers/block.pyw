from pygame import *
img = image.load('images//towers//block.png')

class Tower:

    def __init__(self, pos):
        self.pos = pos
        self.img = img