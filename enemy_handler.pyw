from pygame import *
import pickle
from enemy_things import *

class Enemy_Handler:
    def __init__(self):
        pass

    def get_path(self, blocks):
        path_finder.get_path(blocks, grid_size, start, end)

    # Enemies to be passed in like [('enemy_name', amount)]
    def set(self, enemies):
        self.enemies = []
        for enemy, amount in enemies:
            for num in range(amount):
                self.enemies.append(eval(enemy).Enemy())

    def update(self, window, dt):
        
        for enemy in self.enemies:
            enemy.update(window, dt)