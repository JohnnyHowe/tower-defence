from pygame import *
import pickle
from enemy_things import path_finder, walker

class Enemy_Handler:
    def __init__(self):
        
        self.images = {
            'walker': image.load('images\\enemies\\walker.png')
        }

    blocks = []
    path = None


    def get_path(self, blocks, grid_size):
        # does it need to update
        if self.blocks != blocks or self.path == None:
            self.path = path_finder.get_path(blocks, grid_size)
            self.blocks = list(blocks)


    def show_path(self, window, game_scale):
        path = self.path
        for index in range(len(path) - 1):
            pos1 = list(path[index][:2])
            pos2 = list(path[index + 1][:2])

            pos1[0] += 0.5; pos1[1] += 0.5
            pos2[0] += 0.5; pos2[1] += 0.5

            pos1[0] *= game_scale; pos1[1] *= game_scale
            pos2[0] *= game_scale; pos2[1] *= game_scale

            colour = (200, 100, 0)
            draw.line(window, colour, pos1, pos2, 3)


    def update_path(self, window, game_scale, grid_size, blocks):
        self.get_path(blocks, grid_size)
        self.show_path(window, game_scale)

    # Enemies to be passed in like [('enemy_name', amount)]
    def set(self, enemies):
        self.enemies = []
        for enemy, amount in enemies:
            for num in range(amount):
                self.enemies.append(eval(enemy).Enemy(self.path))


    def update(self, window, game_scale, dt):
        finished = False
        
        for enemy in self.enemies:
            if enemy.update(dt):
                finished = True

            # show
            pos, angle = enemy.get_pos()
            new_pos = list(pos)
            new_pos[0] *= game_scale
            new_pos[1] *= game_scale

            img = self.images[enemy.id]
            img = transform.scale(img, (game_scale, game_scale))
            img = transform.rotate(img, angle)

            window.blit(img, new_pos)

        return finished