from pygame import *
img = None #image.load('images//')

class Tower:

    def __init__(self, pos):

        self.pos = pos
        self.cost = 50

        self.id = 'name'
        self.info = 'description'


    def do_damage(self, enemies):
        # Do damage here
        return enemies


    def update(self, window, window_scale, playing_grid, dt):
        self.show(window, window_scale)


    def show(self, window, window_scale):

        # Scale image
        t_img = transform.scale(img, (int(window_scale), int(window_scale)))

        # Work out scaled pos
        pos = list(self.pos)
        pos[0] *= window_scale
        pos[1] *= window_scale

        # Show
        window.blit(t_img, pos)
