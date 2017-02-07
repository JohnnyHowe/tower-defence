from pygame import *
from enemy_things import path_finder
import global_functions as gfunc

# Import enemies
from enemy_things import walker

class Enemy_Handler:

    def __init__(self):
        self.enemies = []


    def update_enemies(self, window, window_scale, playing_grid, dt):

        temp = []
        for enemy in self.enemies:

            # Update
            enemy.update(window, window_scale, dt)

            # Is it still valid?
            pos = enemy.get_pos()

            if pos:
                if pos[0] < playing_grid[0] and not enemy.dead:
                    temp.append(enemy)
            else:
                temp.append(enemy)

        self.enemies = temp


    def set_enemy_path(self):

        # Update the path
        for enemy in self.enemies:
            enemy.path = self.path


    def load_enemies(self, enemies):

        # Store the objects
        self.enemies = []

        # Go over all the groups
        for enemy_group in enemies:

            # Work it out once and once only fo this group
            enemy_type = eval(enemy_group[0])

            scale = enemy_group[1]
            speed = enemy_group[2]

            # Make the specified amount
            for enemy_index in range(enemy_group[3]):

                time_until_spawn = enemy_group[4] + enemy_index * enemy_group[5]

                try:
                    # Make enemy string eg. 'walker' into the enemy object (MUST BE IMPORTED!)
                    obj = enemy_type.Enemy(scale, speed, time_until_spawn)
                    self.enemies.append(obj)

                except Exception as error:

                    print(error)
                    print('''
Cannot make the enemy into an object!
Check that the enemy file is imported into the 'enemy_manager.pyw' file''')


    blocks = []     # Keep track of the blocks on the grid to avoid updating the path when it doesn't need to
    path = None

    def update_path(self, window, window_scale, grid_size, blocks, dt):
        self.get_path(blocks, grid_size)

        if self.path:
            self.show_path(window, window_scale, dt)

    lines = None
    old_path = None

    def show_path(self, window, window_scale, dt):

        # Has the path changed?
        if self.path != self.old_path:

            # Update old path
            self.old_path = self.path

            # reset the lines

            # Partial reset
            if self.old_path and self.lines:

                for index in range(len(self.old_path)):
                    if self.old_path[index] != self.path[index]:
                        break

                lines = self.lines[:index - 1]

                for next_i in range(len(self.path) - len(lines)):
                    last = lines[len(lines) - 1]
                    lines.append(last + 1)

                self.lines = lines

            # Complete reset
            else:
                self.lines = []
                for dist in range(len(self.path) - 1):
                    self.lines.append(dist + 0.5)


        reset = False

        # Show the lines
        for dist_index in range(len(self.lines)):

            dist = self.lines[dist_index]
            self.lines[dist_index] += dt * 2

            # Work out positions
            front_dist = dist
            back_dist = dist - 0.5

            if front_dist > 0:

                pos = gfunc.get_pos_on_path(self.path, front_dist)
                back_pos = gfunc.get_pos_on_path(self.path, back_dist)

                # If everything is on the path
                if pos and back_pos:

                    pos = list(pos)
                    back_pos = list(back_pos)

                    # Center points
                    pos[0] += 0.5
                    pos[1] += 0.5

                    back_pos[0] += 0.5
                    back_pos[1] += 0.5

                    # Scale pos
                    pos[0] *= window_scale
                    pos[1] *= window_scale

                    back_pos[0] *= window_scale
                    back_pos[1] *= window_scale

                    # Show
                    draw.line(window, (255, 100, 30), pos, back_pos, max(1, int(window_scale * 0.15)))

                else:
                    reset = True

        if reset:

            for dist_index in range(len(self.lines)):
                self.lines[dist_index] -= 1


    def get_path(self, blocks, grid_size):

        if blocks != self.blocks or self.path == None:
            self.blocks = list(blocks)

            # Update path
            self.path = path_finder.get_path(blocks, grid_size)
