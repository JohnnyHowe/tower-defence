import enum
import pygame

from window import Window
from game_grid import GameGrid
from game_window import GameWindow
from event_handler import EventHandler
from clock import Clock
from camera import Camera

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
    ]

    def __init__(self):
        self.board = GameGrid((10, 5))
        self.game_window = GameWindow(self.board.size)
        self.game_state = GameState.SETUP

        Camera.size = max(self.board.size)
        Camera.aspect_ratio = (self.board.size[0], self.board.size[1] + 2)

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
    
        for event in EventHandler.get_events(pygame.MOUSEBUTTONDOWN):
            mouse_cell = self.game_window.get_mouse_cell(check_in_bounds=False)

            # did the player click a tower select button?
            if mouse_cell[1] == self.board.size[1]:
                index = mouse_cell[0]
                if index < len(self.towers):
                    self.selected_tower = index
            # did the player click the round start button?
            if self.game_state == self.game_state.SETUP:
                if -self.game_window.tower_selector_height <= mouse_cell[1] < 0:
                    self.game_state = GameState.IN_PLAY
 
    def try_place_tower(self, cell):
        if self.selected_tower is not None:
            if self.towers[self.selected_tower][2] and not self.board.is_base_empty(cell) and self.board.is_item_empty(cell):
                self.board.set_item_at(cell, self.towers[self.selected_tower][1](cell))

            if self.board.is_base_empty(cell) and not self.towers[self.selected_tower][2]:
                self.board.set_base_at(cell, self.towers[self.selected_tower][1](cell))

    def draw(self):
        # self.game_window.draw_background()

        game_board_top = round(self.board.size[1] / 2)
        game_board_bottom = game_board_top - self.board.size[1]

        # header
        Camera.draw_rect((-self.board.size[0] / 2, game_board_top + 1, self.board.size[0], 1), (150, 200, 150))
        # footer (tower selection)
        Camera.draw_rect((-self.board.size[0] / 2, game_board_bottom, self.board.size[0], 1), (150, 150, 200))
        # game board
        Camera.draw_rect((-self.board.size[0] / 2, game_board_top, self.board.size[0], game_board_top - game_board_bottom), (255, 255, 255))

        # # tower selection
        # for i in range(len(self.towers)):
        #     t_object, t_class, requires_base = self.towers[i]
        #     display_rect = self.game_window.get_cell_pixel_rect((i, self.board.size[1]))

        #     if self.selected_tower == i:
        #         pygame.draw.rect(Window.surface, (0, 255, 0), display_rect)

        #     image = t_object.get_image(self.board)
        #     image = pygame.transform.scale(image, (int(self.game_window.get_cell_pixel_size()),) * 2)
        #     Window.surface.blit(image, display_rect[:2])

        # highlighted cell
        if pygame.mouse.get_focused():
            # pygame.draw.rect(Window.surface, (0, 255, 0), self.game_window.get_cell_pixel_rect(self.game_window.get_mouse_cell()))
            mouse_pos = Camera.get_world_position(pygame.mouse.get_pos())
            cell_pos = (round(mouse_pos[0] - 0.5), round(mouse_pos[1] + 0.5))
            Camera.draw_rect(cell_pos + (1, 1), (255, 0, 0))

        return
        # placed towers
        for tower in self.board.get_all_base() + self.board.get_all_items():
            image = tower.get_image(self.board)
            image = pygame.transform.scale(image, (int(self.game_window.get_cell_pixel_size()),) * 2)
            Window.surface.blit(image, self.game_window.get_cell_pixel_position(tower.position))

        if self.game_state == GameState.SETUP:
            self.draw_path()

        self.draw_header_text()
        self.game_window.draw() 

    def draw_header_text(self):
        y = self.game_window.get_cell_pixel_position((0, -1))[1] + self.game_window.get_cell_pixel_size() / 2
        center_x = Window.size[0] / 2
        scale = self.game_window.get_cell_pixel_size()

        large_font = pygame.font.SysFont("", int(scale * 0.8))
        small_font = pygame.font.SysFont("", int(scale * 0.3))

        stage_surf = large_font.render(str(self.game_state), True, (0, 0, 0))
        stage_surf_rect = stage_surf.get_rect()
        change_stage_surf = small_font.render("Click here to start round", True, (0, 0, 0))
        change_stage_surf_rect = change_stage_surf.get_rect()

        Window.surface.blit(stage_surf, (center_x - stage_surf_rect.w / 2, y - stage_surf_rect.h / 2 - scale * 0.1))
        Window.surface.blit(change_stage_surf, (center_x - change_stage_surf_rect.w / 2, y - stage_surf_rect.h / 2 + scale * 0.5))

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
