from pygame import *
img = image.load('images//towers//block.png')
layer = 0

class Tower:

    def __init__(self, pos):

        self.layer = layer

        self.pos = pos
        self.cost = 5

        self.id = 'block'
        self.info = 'Base for other towers, can be used to make the enemies path longer'

        self.projectiles = []


    def reset(self):
        pass


    def do_damage(self, enemies, *args):
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

