import pygame
from window import Window
from game_grid import GameGrid
from game_window import GameWindow
from event_handler import EventHandler
from clock import Clock

from wall import Wall
from machine_gun import MachineGun


class Game:
    board = None
    game_window = None
    path_visual_timer = 0

    selected_tower = None
    towers = [
        # (obj, class, requires base)
        (Wall((0, 0)), Wall, False),
        (MachineGun((0, 0)), MachineGun, True),
    ]

    def __init__(self):
        self.board = GameGrid((10, 5))
        self.game_window = GameWindow(self.board.size)

    def update(self):

        # is the player placing a tower?
        keys_pressed = pygame.key.get_pressed()
        if keys_pressed[pygame.K_LSHIFT]:
            if pygame.mouse.get_pressed()[0]:
                self.try_place_tower(self.game_window.get_mouse_cell())
            elif pygame.mouse.get_pressed()[2]:
                self.board.clear_at(self.game_window.get_mouse_cell())
        else:
            for event in EventHandler.get_events(pygame.MOUSEBUTTONDOWN):
                if event.button == 1:
                    self.try_place_tower(self.game_window.get_mouse_cell())
                if event.button == 3:
                    self.board.clear_at(self.game_window.get_mouse_cell())
    
        # did the player click a tower select button?
        for event in EventHandler.get_events(pygame.MOUSEBUTTONDOWN):
            mouse_cell = self.game_window.get_mouse_cell(check_in_bounds=False)
            if mouse_cell[1] == self.board.size[1]:
                index = mouse_cell[0]
                if index < len(self.towers):
                    self.selected_tower = index
 
    def try_place_tower(self, cell):
        if self.selected_tower is not None:
            if self.towers[self.selected_tower][2] and not self.board.is_base_empty(cell) and self.board.is_item_empty(cell):
                self.board.set_item_at(cell, self.towers[self.selected_tower][1](cell))

            if self.board.is_base_empty(cell) and not self.towers[self.selected_tower][2]:
                self.board.set_base_at(cell, self.towers[self.selected_tower][1](cell))

    def draw(self):
        self.game_window.draw_background()

        # tower selection
        for i in range(len(self.towers)):
            t_object, t_class, requires_base = self.towers[i]
            display_rect = self.game_window.get_cell_pixel_rect((i, self.board.size[1]))

            if self.selected_tower == i:
                pygame.draw.rect(Window.surface, (0, 255, 0), display_rect)

            image = t_object.get_image(self.board)
            image = pygame.transform.scale(image, (int(self.game_window.get_cell_pixel_size()),) * 2)
            Window.surface.blit(image, display_rect[:2])

        # highlighted cell
        if pygame.mouse.get_focused():
            pygame.draw.rect(Window.surface, (0, 255, 0), self.game_window.get_cell_pixel_rect(self.game_window.get_mouse_cell()))

        # placed towers
        for tower in self.board.get_all_base() + self.board.get_all_items():
            image = tower.get_image(self.board)
            image = pygame.transform.scale(image, (int(self.game_window.get_cell_pixel_size()),) * 2)
            Window.surface.blit(image, self.game_window.get_cell_pixel_position(tower.position))

        self.draw_path()

    def draw_path(self):
        path = self.board.get_path()
        if path is not None:
            self.path_visual_timer = (self.path_visual_timer + Clock.dt) % 1

            def draw_line(p1, p2):
                sp1 = self.game_window.get_cell_pixel_position((p1[0] + 0.5, p1[1] + 0.5))
                sp2 = self.game_window.get_cell_pixel_position((p2[0] + 0.5, p2[1] + 0.5)) 
                pygame.draw.line(Window.surface, (255, 165, 0), sp1, sp2, int(self.game_window.get_cell_pixel_size() / 8))

            for i in range(len(path) - 1):
                node1 = path[i]
                node2 = path[i + 1]

                dx = node2[0] - node1[0]
                dy = node2[1] - node1[1]

                t1 = self.path_visual_timer
                t2 = self.path_visual_timer + 0.5

                line_start = node1[0] + dx * t1, node1[1] + dy * t1 
                line_end = node1[0] + dx * (t2 % 1), node1[1] + dy * (t2 % 1) 

                if t2 < 1:
                    draw_line(line_start, line_end)
                else:
                    draw_line(node1, line_end)
                    draw_line(line_start, node2)


        self.game_window.draw() 