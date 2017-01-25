from pygame import *
import math
img = image.load('images//towers//machine_gun_icon.png')

tower_cost = 50
tower_info = 'Fires a continuous stream fast, low damagr bullets'

id = 'machine_gun'


def slope(angle):

    if angle < 0: angle += 360
    if angle > 360: angle -= 360

    c = 0
    if angle > 270: angle -= 270; c = 3
    elif angle > 180: angle -= 180; c = 2
    elif angle > 90: angle -= 90; c = 1

    x = angle / 90
    y = 1-x

    if c == 1:
        x, y = y, x
        y = -y

    elif c == 2:
        x = -x
        y = -y

    elif c == 3:
        x, y = y, x
        x = -x

    return x, y


bullet_img = image.load('images//enemies//bullet.png')
class Bullet:
    def __init__(self, pos, direction, speed):
        self.pos = list(pos)
        self.slope = slope(direction)
        self.angle = direction
        self.speed = -speed
        self.damage = 0.1
        
    def get_rect(self, window_scale):
        rect = bullet_img.get_rect()
        width_scale = rect.width / rect.height

        height = window_scale / 2
        width = width_scale * height

        img = transform.scale(bullet_img, (int(width), int(height)))
        img = transform.rotate(img, self.angle)

        rect = img.get_rect()
        return self.pos[0], self.pos[1], rect.width, rect.height 

    def update(self, dt):
        self.move(dt)

    def move(self, dt):
        self.pos[0] += dt * self.speed * self.slope[0]
        self.pos[1] += dt * self.speed * self.slope[1]

    def on_screen(self, wx, wy, window):

        draw.rect(window, (255, 255, 0), (0, 0, wx, wy), 4)
        if self.pos[0] + 100 > 0:
            if self.pos[0] - 100 < wx:
                if self.pos[1] + 100 > 0:
                    if self.pos[1] - 100 < wy:
                        return True
        return False

    def show(self, window, window_scale):

        rect = bullet_img.get_rect()

        width_scale = rect.width / rect.height

        height = window_scale / 2
        width = width_scale * height

        img = transform.scale(bullet_img, (int(width), int(height)))
        img = transform.rotate(img, self.angle)

        rect = img.get_rect()

        pos = self.pos[0] - rect.width / 2, self.pos[1] - rect.height / 2

        window.blit(img, pos)

        
class Tower:

    def __init__(self, pos):
        self.pos = pos
        self.img = img
        self.id = 'machine_gun'
        self.refund_value = 50
        self.base = image.load('images//towers//machine_gun_base.png')
        self.barrel = image.load('images//towers//machine_gun_barrel.png')
        self.angle = 45
        self.id = 'machine_gun'

    def update(self, enemies, dt, window, window_scale, wx, wy):
        self.aim(enemies, window_scale, window)
        self.shoot(dt, window_scale, enemies, window)
        self.update_bullets(dt, wx, wy, window)

        # print(len(self.bullets))

    def show_bullets(self, window, window_scale, dev):
        for bullet in self.bullets:
            bullet.show(window, window_scale)

            if dev:
                draw.rect(window, (0, 0, 255), bullet.get_rect(window_scale), 2)

    def update_bullets(self, dt, wx, wy, window):
        n = []
        for bullet in self.bullets:
            bullet.update(dt)
            if bullet.on_screen(wx, wy, window):
                n.append(bullet)
        self.bullets = n

    def reset(self):
        self.bullets = []

    bullets = []
    tick = 0
    def shoot(self, dt, window_scale, enemies, window):

        i = None
        for enemy in enemies:
            if enemy.pos:
                i = True
                break
        
        if i:
            if self.tick > 0.05:
                pos = int((self.pos[0] + 0.5) * window_scale), int((self.pos[1] + 0.5) * window_scale)
                self.bullets.append(Bullet(pos, self.angle, 5000)) 
                self.tick = 0

            self.tick += dt


    def do_damage(self, enemies, window_scale, window):
        
        bullets = []
        for bullet in self.bullets:
            b = bullet.get_rect(window_scale)

            for enemy in enemies:
                e = enemy.get_rect(window_scale)

                if b[0] + b[2] >= e[0]:
                    if b[0] <= e[0] + e[2]:
                        if b[1] + b[3] >= e[1]:
                            if b[1] <= e[1] + e[3]:

                                enemy.health = max(enemy.health - bullet.damage, 0)
                                break
            bullets.append(bullet)
        return enemies


    def aim(self, enemies, window_scale, window):
        pos = None

        # Where is the furtherist
        if len(enemies) > 0:
            pos = enemies[0].pos

       # Look in that direction

        if pos:

            rect = enemies[0].get_rect(window_scale)

            xd = pos[0] - self.pos[0]
            yd = pos[1] - self.pos[1]

            rad = math.atan2(-yd, xd)
            deg = math.degrees(rad)

            self.angle = deg - 90


    def show(self, window, window_scale, dt, game_grid, dev):
        window.blit(transform.scale(self.base, (window_scale, window_scale)), (self.pos[0] * window_scale, self.pos[1] * window_scale))

        top = transform.scale(self.barrel, (window_scale, window_scale))
        top = transform.rotate(top, self.angle)

        rect = top.get_rect()
        c = rect.width / 2, rect.height / 2

        wx, wy = game_grid[0] * window_scale, game_grid[1] * window_scale
        self.show_bullets(window, window_scale, dev)

        window.blit(top, ((self.pos[0] + 0.5) * window_scale - c[0], (self.pos[1] + 0.5) * window_scale - c[1]))
