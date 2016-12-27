from pygame import *
from towers import block


class Handler:
    def __init__(self, playing_grid, window_scale, window):
        self.playing_grid = playing_grid
        self.usable_towers = [block]
        self.placed_towers = []
        self.window = window
        self.window_scale = window_scale


    def update(self, mouse_states, mouse_pos):
        self.selection_color(mouse_pos)
        self.show_menu()
        self.manage_towers()
        self.tower_select(mouse_states, mouse_pos)


    # MENU
    def show_menu(self):
        for index in range(len(self.usable_towers)):
            y = index // self.playing_grid[0]
            x = index - y * self.playing_grid[0]
            self.window.blit(transform.scale(self.usable_towers[index].img, (self.window_scale, self.window_scale)), (x, y + self.playing_grid[1] * self.window_scale))


    def manage_towers(self):
        for tower in self.placed_towers:
            self.window.blit(transform.scale(tower.img, (self.window_scale, self.window_scale)), (tower.pos[0] * self.window_scale, tower.pos[1] * self.window_scale))

    def selection_color(self, mouse_pos):
        if self.held_tower:
            for tower in self.placed_towers:
                if tower.pos == mouse_pos:
                    # draw red Rect
                    rect = Surface((self.window_scale, self.window_scale))
                    rect.set_alpha(128)
                    rect.fill((255, 100, 100))
                    self.window.blit(rect, (mouse_pos[0] * self.window_scale, mouse_pos[1] * self.window_scale))
                    return
            if mouse_pos[1] < self.playing_grid[1]:
                rect = Surface((self.window_scale, self.window_scale))
                rect.set_alpha(128)
                rect.fill((100, 255, 100))
                self.window.blit(rect, (mouse_pos[0] * self.window_scale, mouse_pos[1] * self.window_scale))
            else:
                rect = Surface((self.window_scale, self.window_scale))
                rect.set_alpha(128)
                rect.fill((255, 100, 100))
                self.window.blit(rect, (mouse_pos[0] * self.window_scale, mouse_pos[1] * self.window_scale))


    held_tower = None
    def tower_select(self, mouse_states, mouse_pos):
        if self.held_tower == None:

            #Is mouse in valid spot
            if mouse_states[0] == -1:
                # Position from start of tower selection menu
                r_pos = mouse_pos[0], mouse_pos[1] - self.playing_grid[1]
                if r_pos[1] >= 0:

                    #Is a tower in selected slot
                    full_rows = len(self.usable_towers) // self.playing_grid[0]
                    columns = len(self.usable_towers) - full_rows * self.playing_grid[0]

                    if r_pos[1] < full_rows or (r_pos[0] < columns and r_pos[1] < full_rows + 1):
                        mouse_pos_index = r_pos[0] + r_pos[1] * self.playing_grid[1]
                        self.held_tower = self.usable_towers[mouse_pos_index]
        else:

            if mouse_states[0] == -1 and mouse_pos[1] < self.playing_grid[1]:
                okay = True
                for tower in self.placed_towers:
                    if tower.pos == mouse_pos:
                        okay = False
                        break
                if okay:
                    self.placed_towers.append(self.held_tower.Tower(mouse_pos))
                    self.window.blit(transform.scale(self.held_tower.img, (self.window_scale, self.window_scale)), (mouse_pos[0] * self.window_scale, mouse_pos[1] * self.window_scale))
                    self.held_tower = None
            else:
                self.window.blit(transform.scale(self.held_tower.img, (self.window_scale, self.window_scale)), (mouse_pos[0] * self.window_scale, mouse_pos[1] * self.window_scale))
