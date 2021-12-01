import enum
import pygame

from window import Window
from game_grid import GameGrid
from event_handler import EventHandler
from clock import Clock
from camera import Camera
from mouse import Mouse, MouseButton

from wall import Wall
from machine_gun import MachineGun


class GameState(enum.Enum):
    SETUP = 1
    IN_PLAY = 2


class Game:
    board = None
    game_window = None
    path_visual_timer = 0
    game_state: GameState

    selected_tower = None
    towers = [
        # (obj, class, requires base)
        (Wall((0, 0)), Wall, False),
        (MachineGun((0, 0)), MachineGun, True),
        (Wall((0, 0)), Wall, False),
        (MachineGun((0, 0)), MachineGun, True),
    ]

    def __init__(self):
        self.board = GameGrid((10, 6))
        self.game_state = GameState.SETUP

        Camera.size = max(self.board.size)
        Camera.aspect_ratio = (self.board.size[0], self.board.size[1] + 2)
        Camera.position[1] = -((self.board.size[1] + 2) % 2) / 2

    def update(self):
        # is the player placing a tower?
        keys_pressed = pygame.key.get_pressed()
        mouse_pos = Camera.get_world_position(Mouse.get_position())
        mouse_cell = (round(mouse_pos[0] - 0.5), round(mouse_pos[1] + 0.5))

        if keys_pressed[pygame.K_LSHIFT]:
            if Mouse.get_pressed(MouseButton.LEFT):
                self.try_place_tower(mouse_cell)
            elif Mouse.get_pressed(MouseButton.RIGHT):
                self.board.clear_at(mouse_cell)
        else:
            if Mouse.get_mouse_down(MouseButton.LEFT):
                self.try_place_tower(mouse_cell)
            if Mouse.get_mouse_down(MouseButton.RIGHT):
                self.board.clear_at(mouse_cell)
    
    def try_place_tower(self, cell):
        if self.selected_tower is not None:
            if self.towers[self.selected_tower][2] and not self.board.is_base_empty(cell) and self.board.is_item_empty(cell):
                self.board.set_item_at(cell, self.towers[self.selected_tower][1](cell))
            if self.board.is_base_empty(cell) and not self.towers[self.selected_tower][2]:
                self.board.set_base_at(cell, self.towers[self.selected_tower][1](cell))

    def draw(self):
        self.draw_board()
        self.draw_ui()

    def draw_ui(self):
        """ Draw AND handle ui events. 
        Ideally this would be a completely different system but hey, here we are. """
        ui_scale = Camera.get_window_scale() * 0.1

        # header
        header_rect = (0, 0, Window.size[0], ui_scale)
        pygame.draw.rect(Window.surface, (150, 200, 150), header_rect)

        # footer (tower selection)
        footer_rect = (0, Window.size[1] - ui_scale, Window.size[0], ui_scale)
        pygame.draw.rect(Window.surface, (150, 200, 150), footer_rect)

        for i in range(len(self.towers)):
            t_object, t_class, requires_base = self.towers[i]

            tower_rect = (int(i * ui_scale), int(footer_rect[1]), int(ui_scale), int(ui_scale))

            if self.selected_tower == i:
                pygame.draw.rect(Window.surface, (0, 255, 0), tower_rect)
            image = t_object.get_image(self.board)
            Window.surface.blit(pygame.transform.scale(image, tower_rect[2:]), tower_rect[:2])

    def draw_board(self):
        """ Draw the main game board and all its bits. """
        game_board_top = round(self.board.size[1] / 2)
        game_board_left = -self.board.size[0] / 2
        game_board_bottom = game_board_top - self.board.size[1]

        # game board
        Camera.draw_rect((255, 255, 255), (game_board_left, game_board_top, self.board.size[0], game_board_top - game_board_bottom))

        # highlighted cell
        if Mouse.is_focused():
            mouse_pos = Camera.get_world_position(Mouse.get_position())
            cell_pos = (round(mouse_pos[0] - 0.5), round(mouse_pos[1] + 0.5))
            Camera.draw_rect((255, 0, 0), cell_pos + (1, 1))

        # placed towers
        for tower in self.board.get_all_base() + self.board.get_all_items():
            Camera.draw_image(tower.get_image(self.board), tower.position)

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
