from pygame import *
import global_functions as gfunc
import random, math

img = image.load('images//towers//lightning.png')
lightning_img = image.load('images//towers//lightning_circle.png')

layer = 1

name = 'Lightning'
info = 'Zapps all enemies that are close enough.'

class Tower:

    def __init__(self, pos):

        self.pos = pos
        self.cost = 75

        self.id = 'lightning'
        self.layer = layer

        orbits = 5
        dif = 0.1
        start = 0.7
        self.circles = []
        for i in range(orbits):
            self.circles.append([random.randint(0, 360), random.choice([-1, 1]), round(dif * i, 3) + start])

    def reset(self):
        pass

    def do_damage(self, enemies, dt, *args):

        for enemy in enemies:
            pos = enemy.get_pos()

            if pos:
                dist = math.sqrt((pos[0] - self.pos[0]) ** 2 + (pos[1] - self.pos[1]) ** 2)

                if dist < 1.5:
                    enemy.health -= 0.002 * dt

        return enemies

    def show_external(self, window, window_scale, dt, *args):
        for circle in self.circles:

            circle[0] += random.randint(-90, 90) * dt * 50
            circle[0] = gfunc.fix_angle(circle[0])

            width = window_scale * 3 * circle[2]

            img = transform.scale(lightning_img, (int(width), int(width)))
            img = transform.rotate(img, int(circle[0]))

            rect = img.get_rect()
            center_pos = [self.pos[0] + 0.5, self.pos[1] + 0.5]
            center_pos[0] *= window_scale; center_pos[1] *= window_scale

            pos = center_pos[0] - rect.width / 2, center_pos[1] - rect.height / 2

            window.blit(img, pos)


    def update(self, window, window_scale, playing_grid, dt):
        self.show(window, window_scale, dt)


    def show(self, window, window_scale, dt):

        # Scale image
        t_img = transform.scale(img, (int(window_scale), int(window_scale)))

        # Work out scaled pos
        pos = list(self.pos)
        pos[0] *= window_scale
        pos[1] *= window_scale

        # Show
        window.blit(t_img, pos)
