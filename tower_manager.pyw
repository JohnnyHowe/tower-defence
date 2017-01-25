from pygame import *
from towers import block, machine_gun


class Handler:
    def __init__(self, playing_grid, window_scale, window):
        self.playing_grid = playing_grid
        self.usable_towers = [block, machine_gun]
        self.placed_towers = []
        self.blocks = []
        self.window = window
        self.window_scale = window_scale


    def update(self, mouse_states, mouse_pos, phase, money, dt, dev):

        if phase == 0:
            self.selection_color(mouse_pos)
            self.show_menu()
            self.show_towers(dt, self.window, self.window_scale, dev)
            return self.tower_select(mouse_states, mouse_pos, money)
        elif phase == 1:
            self.show_towers(dt, self.window, self.window_scale, dev)
        elif phase == 2:
            self.show_towers(dt, self.window, self.window_scale, dev)

    def reset(self):
        for tower in self.placed_towers:
            tower.reset()

    def do_damage(self, enemies, window_scale, window):
        
        for tower in self.placed_towers:
            enemies = tower.do_damage(enemies, window_scale, window)

        return enemies

    # MENU
    def show_menu(self):
        for index in range(len(self.usable_towers)):
            y = index // self.playing_grid[0]
            x = index - y * self.playing_grid[0]
            self.window.blit(transform.scale(self.usable_towers[index].img, (self.window_scale, self.window_scale)), (x * self.window_scale, y + self.playing_grid[1] * self.window_scale))

    def show_towers(self, dt, window, window_scale, dev):
        for tower in self.placed_towers:
            tower.show(self.window, self.window_scale, dt, self.playing_grid, dev)
            
            if dev:
                draw.rect(window, (0, 255, 0), (tower.pos[0] * window_scale, tower.pos[1] * window_scale, window_scale, window_scale), 2)

    def manage_towers(self, enemies, dt, window, window_scale):
        for tower in self.placed_towers:
            wx, wy = self.playing_grid[0] * window_scale, self.playing_grid[1] * window_scale
            tower.update(enemies, dt, window, window_scale, wx, wy)

    def selection_color(self, mouse_pos):
        if self.held_tower:
            for tower in self.placed_towers:
                if tower.pos == mouse_pos:

                    if tower.id == 'block':
                        if self.held_tower.id == 'block':
                            self.draw_rect((255, 100, 100), mouse_pos)
                            return
                        else:
                            self.draw_rect((100, 255, 100), mouse_pos)
                            return

            if mouse_pos[1] < self.playing_grid[1]:        
                if self.held_tower.id == 'block':
                    self.draw_rect((100, 255, 100), mouse_pos)
                    return

            self.draw_rect((255, 100, 100), mouse_pos)
            return

        self.draw_rect((255,255,255), mouse_pos)


    def draw_rect(self, colour, mouse_pos):
        rect = Surface((self.window_scale, self.window_scale))
        rect.set_alpha(128)
        rect.fill(colour)
        self.window.blit(rect, (mouse_pos[0] * self.window_scale, mouse_pos[1] * self.window_scale))

    held_tower = None
    def tower_select(self, mouse_states, mouse_pos, money):

        if not self.held_tower:
                
            # Is the mouse over the tower selection section
            if mouse_pos[1] >= self.playing_grid[1]:

                # Is the mouse over a tower
                mouse_index = mouse_pos[0] + (mouse_pos[1] - self.playing_grid[1]) * self.playing_grid[0]

                if len(self.usable_towers) > mouse_index: tower = self.usable_towers[mouse_index]
                else: tower = None

                if tower:
                    # Display tower info
                    full_mouse_pos = mouse.get_pos()
                    k = key.get_pressed()

                    if k[K_LSHIFT]: self.show_tower_info(self.window, tower.tower_info, full_mouse_pos)
                    else: self.show_tower_info(self.window, '$' + str(tower.tower_cost) + ' (Press shift for more info)', full_mouse_pos)  

                    # Does the tower need to be picked up
                    if mouse_states[0] == -1:
                        self.held_tower = tower

            else:

                # Does a tower need to be picked up
                if mouse_states[2] == -1:

                    # Is the mouse over a tower, if so, destroy it
                    new_list = []
                    check_blocks = False
                    block_index = None
                    done = False

                    for placed_tower in self.placed_towers:
                        if placed_tower.pos == mouse_pos:
                            if placed_tower.id == 'block':
                                block_index = self.placed_towers.index(placed_tower)
                                check_blocks = True
                                new_list.append(placed_tower)
                            else:
                                done = True
                                money += placed_tower.refund_value
                        else:
                            new_list.append(placed_tower)
    
                    if done:
                        self.placed_towers = list(new_list)

                    elif check_blocks:
                        new_list = []
                        self.placed_towers.pop(block_index)

                        for block in self.blocks:
                            if not block.pos == mouse_pos:
                                new_list.append(block)
                            else:
                                money += block.refund_value
                        self.blocks = list(new_list)                                           


        else:

            # Show held tower
            img = self.held_tower.img
            img = transform.scale(img, (self.window_scale, self.window_scale))

            pos = list(mouse_pos)
            pos[0] *= self.window_scale; pos[1] *= self.window_scale
            self.window.blit(img, pos)

            # Does it need to be placed down
            if mouse_states[0] == -1:

                # Is there a tower in the way
                t = None
                for tower in self.placed_towers:

                    if tower.pos == mouse_pos:

                        t = tower.id
                        break

                okay = False
                if t == None:
                    if self.held_tower.id == 'block':
                        okay = True
                elif t == 'block':
                    if self.held_tower.id != 'block':
                        okay = True
                    

                if okay:

                    # Is it on the game screen
                    if mouse_pos[1] < self.playing_grid[1]:

                        # Can the user afford the tower
                        if money >= self.held_tower.tower_cost:

                            # Make the tower
                            tower = self.held_tower.Tower(mouse_pos)
                            self.placed_towers.append(tower)

                            money -= self.held_tower.tower_cost

                            if tower.id == 'block':
                                self.blocks.append(tower)

                            # Do we let go of the tower?
                            k = key.get_pressed()
                            if not k[K_LSHIFT]:
                                self.held_tower = None
                            
            elif mouse_states[2] == -1:
                self.held_tower = None

        return money


    def show_tower_info(self, window, text, pos):
        f = font.SysFont(0, 20)
        margin = 5
        border = 2

        message = f.render(text, 0, (255, 255, 255)) 
        rect = message.get_rect()

        # draw rectangles
        rect1 = Surface((rect.width + 2 * (margin + border), rect.height + 2 * (margin + border)))
        rect1.fill((255, 255, 255))
        rect1.set_alpha(128)
        window.blit(rect1, (pos[0], pos[1]))

        rect2 = Surface((rect.width + 2 * margin, rect.height + 2 * margin))
        rect2.fill((0, 0, 0))
        rect2.set_alpha(128)
        window.blit(rect2, (pos[0] + border, pos[1] + border))


        # draw text
        window.blit(message, (pos[0] + margin + border, pos[1] + margin + border))