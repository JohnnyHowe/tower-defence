from pygame import *
import mouse_extras
import global_functions as gfunc
import math

# Import towers
from towers import block


class Tower_Handler:

    def __init__(self):
        self.usable_towers = [block]
        self.towers = []
        self.blocks = []


    def update_towers(self, window, window_scale, playing_grid, dt):

        for tower in self.towers:
            tower.update(window, window_scale, playing_grid, dt)

    
    held_tower = None
    def tower_selection(self, window, window_scale, playing_grid, tower_select_rows):

        def draw_rect(colour):
            pos = mouse_extras.get_pos()
            pos[0] *= window_scale
            pos[1] *= window_scale

            rect = Surface((window_scale, window_scale))
            rect.set_alpha(128)
            rect.fill(colour)
            window.blit(rect, pos)


        # Draw selecetion block
        selection_rect = (0, window_scale * playing_grid[1], math.ceil(window_scale * playing_grid[0]), math.ceil(tower_select_rows * window_scale))
        draw.rect(window, (150, 150, 150), selection_rect)

        # Show towers in selection part
        for tower_i in range(len(self.usable_towers)):
            tower = self.usable_towers[tower_i]

            # Change index to pos
            y = int(tower_i / playing_grid[0])
            x = tower_i - y * playing_grid[0]
            y += playing_grid[1]

            # Scale pos
            x *= window_scale
            y *= window_scale

            # Scale img
            img = transform.scale(tower.img, (int(window_scale), int(window_scale)))

            # Show
            window.blit(img, (x,y))

        # Delete tower
        if not self.held_tower:

            if mouse_extras.get_states()[2] == -1:

                mouse_pos = mouse_extras.get_pos()

                # What tower is the mouse over?
                for tower_index in range(len(self.towers)):
                    tower = self.towers[tower_index]

                    if tower.pos == mouse_pos:
                        self.towers.pop(tower_index)

                        if tower.id == 'block':
                            # Find block

                            for block_index in range(len(self.blocks)):

                                block = self.blocks[block_index]

                                if block.pos == mouse_pos:
                                    self.blocks.pop(block_index)

                                    break
                        break


        # Show placed towers
        for tower in self.towers:
            tower.show(window, window_scale)

        # Show held tower
        if self.held_tower:
            scaled_pos = mouse_extras.get_pos()
            img = transform.scale(self.held_tower.img, (int(window_scale), int(window_scale)))

            scaled_pos[0] *= window_scale
            scaled_pos[1] *= window_scale

            def show_tower():
                window.blit(img, scaled_pos)

            # Can the tower be placed?
            # Is it in the playing area

            # Does the held tower need to be let go?
            if mouse_extras.get_states()[2] == -1:
                self.held_tower = None
                return

            pos = mouse_extras.get_pos()
            if pos[1] < playing_grid[1]:

                # Check if a tower is in the way
                okay = True
                for tower in self.towers:
                    if tower.pos == pos:
                        okay = False

                if okay:
                    draw_rect((100, 255, 100))
                    show_tower()

                    # Does the held tower need to be placed?
                    if mouse_extras.get_states()[0] == -1:

                        # Place the tower
                        tower = self.held_tower.Tower(pos)
                        self.towers.append(tower)

                        # Is it a block
                        if tower.id == 'block':
                            self.blocks.append(tower)

                        # Should the tower still be held on to?
                        if not key.get_pressed()[K_LSHIFT]:
                            self.held_tower = None

                else:
                    draw_rect((255, 100, 100))
                    show_tower()

            else:
                draw_rect((255, 100, 100))
                show_tower()

        else:

            mouse_states = mouse_extras.get_states()
            if mouse_states[0] == -1:

                # Pick up tower
                pos = mouse_extras.get_pos()
                mouse_rect = [pos[0] * window_scale, pos[1] * window_scale, 0, 0]

                if gfunc.touching(mouse_rect, selection_rect):

                    pos = mouse_extras.get_pos()
                    pos[1] -= playing_grid[1]

                    index = pos[1] * playing_grid[0]
                    index += pos[0]

                    if index < len(self.usable_towers):
                        tower = self.usable_towers[index]
                        self.held_tower = tower