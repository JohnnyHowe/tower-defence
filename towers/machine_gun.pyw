from pygame import *
import global_functions as gfunc

img = image.load('images\\towers\\machine_gun_icon.png')
layer = 1

bullet_img = image.load('images\\towers\\bullet.png')

class Bullet:

    def __init__(self, pos, slope, speed = 30):
        self.pos = list(pos)
        self.slope = slope
        self.angle = self.get_angle()
        self.speed = speed

        self.height = 0.3 # Multiplied by the window scale

    def update(self, window, window_scale, dt):
        self.move(dt)
        self.show(window, window_scale)


    def move(self, dt):
        self.pos[0] += dt * self.speed * self.slope[0]
        self.pos[1] += dt * self.speed * self.slope[1]


    def get_angle(self):
        p1 = self.pos
        p2 = self.pos[0] + self.slope[0], self.pos[1] + self.slope[1]
        return gfunc.get_rot(p1, p2)


    def get_rect(self, window_scale):
        img_rect = bullet_img.get_rect()
        scale = self.height * window_scale / min(img_rect.width, img_rect.height)

        width = img_rect.width * scale
        height = img_rect.height * scale

        img = transform.scale(bullet_img, (int(width), int(height)))
        img = transform.rotate(img, self.angle)

        rect_obj = img.get_rect()
        rect_list = [self.pos[0] * window_scale - rect_obj.width / 2, self.pos[1] * window_scale - rect_obj.height / 2, rect_obj.width, rect_obj.height]

        return rect_list


    def show(self, window, window_scale):
        img_rect = bullet_img.get_rect()
        scale = self.height * window_scale / min(img_rect.width, img_rect.height)

        width = img_rect.width * scale
        height = img_rect.height * scale

        img = transform.scale(bullet_img, (int(width), int(height)))
        img = transform.rotate(img, self.angle)

        rect = self.get_rect(window_scale)

        pos = rect[:2]
        window.blit(img, pos)


class Tower:

    def __init__(self, pos):

        self.layer = layer

        self.pos = pos
        self.cost = 50

        self.id = 'name'
        self.info = 'description'

        self.base_img = image.load('images\\towers\\machine_gun_base.png')
        self.barrel_img = image.load('images\\towers\\machine_gun_barrel.png')

        self.rot = None
        self.projectiles = []

    last_shot = 0
    def shoot(self, dt):

        self.last_shot += dt * 10

        if self.last_shot >= 1:
            self.last_shot -= 1

            if self.rot:

                pos = list(self.pos)
                pos[0] += 0.5
                pos[1] += 0.5

                self.projectiles.append(Bullet(pos, gfunc.slope(self.rot - 180)))


    def update_bullets(self, window, window_scale, dt):

        for bullet in self.projectiles:
            bullet.update(window, window_scale, dt)


    def do_damage(self, enemies):
        self.aim(enemies)
        # Do damage here

        return enemies


    def update(self, window, window_scale, playing_grid, dt):
        self.shoot(dt)
        self.update_bullets(window, window_scale, dt)
        self.show(window, window_scale)


    def aim(self, enemies):

        if len(enemies) > 0:

            # Aim at first
            enemy = enemies[0]
            self.rot = gfunc.get_rot(enemy.get_pos(), self.pos)

        else: self.rot = None


    def show(self, window, window_scale):

        # Scale images
        base = transform.scale(self.base_img, (int(window_scale), int(window_scale)))
        barrel = transform.scale(self.barrel_img, (int(window_scale), int(window_scale)))

        # Rotate barrel
        if self.rot: barrel = transform.rotate(barrel, self.rot)

        # Get correct position after rotation
        rect = barrel.get_rect()
        offset = (window_scale - rect.width) / 2, (window_scale - rect.height) / 2

        # Work out scaled pos
        pos = list(self.pos)
        pos[0] *= window_scale
        pos[1] *= window_scale

        # Show
        window.blit(base, pos)
        window.blit(barrel, (pos[0] + offset[0], pos[1] + offset[1]))