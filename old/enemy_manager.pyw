from pygame import *
import pickle
from enemy_things import path_finder, walker

class Enemy_Handler:
    def __init__(self):
        pass

    blocks = []
    path = None

    def get_path(self, blocks, grid_size):
        # does it need to update
        if self.blocks != blocks or self.path == None:
            self.path = path_finder.get_path(blocks, grid_size)
            self.blocks = list(blocks)

    path_alpha = 0
    def show_path(self, window, game_scale):

        path = self.path
        if path:
            for index in range(len(path) - 1):
                pos1 = list(path[index][:2])
                pos2 = list(path[index + 1][:2])

                pos1[0] += 0.5; pos1[1] += 0.5
                pos2[0] += 0.5; pos2[1] += 0.5

                pos1[0] *= game_scale; pos1[1] *= game_scale
                pos2[0] *= game_scale; pos2[1] *= game_scale

                colour = (200, 100, 0)
                draw.line(window, colour, pos1, pos2, 3)
        else:
            return False
        return True


    def update_path(self, window, game_scale, grid_size, blocks):
        self.get_path(blocks, grid_size)
        return self.show_path(window, game_scale)

    # Enemies to be passed in like [('enemy_name', amount, time between each spawn, spawn time after start)]
    def set(self, enemies):
        self.enemies = []

        for enemy_index in range(len(enemies)):
            enemy, amount, time, start_time = enemies[enemy_index]

            for num in range(amount):
                enemy_obj = eval(enemy).Enemy(self.path)
                enemy_obj.spawn_time = num * time + start_time

                self.enemies.append(enemy_obj)

    def manage_health(self):
        
        new_list = []
        for enemy in self.enemies:
            if enemy.health > 0:
                new_list.append(enemy)
        self.enemies = new_list


    def update(self, window, game_scale, dt, playing_grid, dev):
        finished = False

        self.manage_health()

        new_list = []
        for enemy in self.enemies:

            enemy.update(dt, playing_grid, window, game_scale)

            if enemy.on_path(playing_grid):
                new_list.append(enemy)

        self.enemies = new_list

        return finished