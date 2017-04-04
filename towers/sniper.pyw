from pygame import *
img = image.load('images//towers//sniper_icon.png')
layer = 1

name = 'Sniper'
info = 'Slow but very high damage weapon'

class Tower:

    def __init__(self, pos):

        self.pos = pos
        self.cost = 50

        self.id = 'sniper'

        self.layer = layer


    def reset(self):
        pass

    def do_damage(self, enemies, *args):
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
