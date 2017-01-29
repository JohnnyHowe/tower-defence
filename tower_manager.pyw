from pygame import *
import mouse_extras

# Import towers
# from towers import None


class Tower_Handler:

    def __init__(self):
        self.usable_towers = []
        self.towers = []


    def update_towers(self, window, window_scale, playing_grid, dt):

        # Update towers
        for tower in self.towers:

            tower.update(window, window_scale, playing_grid, dt)


    def tower_selection(self, window, window_scale, playing_grid):

        # Show towers in selection part
        for tower_i in range(len(self.usable_towers)):
            tower = self.usable_towers[tower_i]

            # Change index to pos
            y = int(tower_i / playing_grid[0])
            x = tower_i - y * playing_grid[0]

            # Scale pos
            x *= window_scale
            y *= window_scale

            # Show
            window.blit(tower.img, (x,y))

        print(mouse_extras.get_states())

