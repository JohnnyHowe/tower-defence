import enum
import pygame

from window import Window
from event_handler import EventHandler
from clock import Clock
from camera import Camera
from mouse import Mouse, MouseButton

from enemy_controller import EnemyController
from tower_controller import TowerController
from wall import Wall
from machine_gun import MachineGun

from engine_math import Vector2, Rect

class GameState(enum.Enum):
    SETUP = 1
    IN_PLAY = 2
    LOST = 3


class Game:
    game_window = None
    path_visual_timer = 0
    game_state: GameState
    enemy_controller: EnemyController
    tower_controller: TowerController

    selected_tower = None 


    def __init__(self):
        self.game_state = GameState.SETUP
        self.board_size = Vector2(10, 5)
        self.enemy_controller = EnemyController()
        self.tower_controller = TowerController(self.board_size)

        Camera.size = max(self.board_size) + 1
        Camera.aspect_ratio = Vector2(self.board_size.x, self.board_size.y + 2)
        Camera.position = Vector2(self.board_size.x / 2, self.board_size.y / 2)

    def start_round(self):
        self.game_state = GameState.IN_PLAY
        self.enemy_controller.start_round(self.tower_controller.board.get_path())

    def update(self):
        self.path_visual_timer = (self.path_visual_timer + Clock.dt) % 1
        self.enemy_controller.update()

        if self.game_state == GameState.IN_PLAY:
            first_enemy = self.enemy_controller.get_first_enemy()
            if first_enemy:
                self.tower_controller.update(first_enemy)

            if self.enemy_controller.has_enemy_finished():
                self.game_state = GameState.LOST

        self.tower_controller.update_projectiles()

        # is the player placing a tower?
        keys_pressed = pygame.key.get_pressed()
        mouse_pos = Camera.get_world_position(Mouse.get_position())
        mouse_cell = round(mouse_pos - Vector2(0.5, 0.5))

        if keys_pressed[pygame.K_LSHIFT]:
            if Mouse.get_pressed(MouseButton.LEFT) and self.selected_tower is not None:
                self.tower_controller.try_place_tower(mouse_cell, self.selected_tower)
            elif Mouse.get_pressed(MouseButton.RIGHT):
                self.tower_controller.board.clear_at(mouse_cell)
        else:
            if Mouse.get_mouse_down(MouseButton.LEFT) and self.selected_tower is not None:
                self.tower_controller.try_place_tower(mouse_cell, self.selected_tower)
            if Mouse.get_mouse_down(MouseButton.RIGHT):
                self.tower_controller.board.clear_at(mouse_cell)
    
    def draw(self):
        self.tower_controller.draw()
        self.draw_path()
        self.enemy_controller.draw()

        # highlighted cell
        if Mouse.is_focused():
            mouse_pos = Camera.get_world_position(Mouse.get_position())
            cell_pos = round(mouse_pos - Vector2(0.5, 0.5))
            cell_center = cell_pos + Vector2(0.5, 0.5)
            Camera.draw_rect((255, 0, 0), Rect(cell_center.x, cell_center.y, 1, 1))

        self.draw_ui()

    def draw_ui(self):
        """ Draw AND handle ui events. 
        Ideally this would be a completely different system but hey, here we are. """

        def draw_text(text, color, font_size, center_position):
            font = pygame.font.SysFont("", int(font_size))
            surface = font.render(text, True, color)
            rect = surface.get_rect()
            Window.surface.blit(surface, (center_position.x - rect.w / 2, center_position.y - rect.h / 2))

        ui_scale = Camera.get_window_scale() * 0.1

        # header
        header_rect = Rect(Window.size.x / 2, ui_scale / 2, Window.size.x, ui_scale)
        pygame.draw.rect(Window.surface, (150, 200, 150), header_rect.get_pygame_tuple(flip_y=True))

        draw_text(str(self.game_state), (0, 0, 0), ui_scale, Vector2(Window.size.x / 2, ui_scale * 0.4))

        if self.game_state == GameState.SETUP:
            if Mouse.get_pressed(MouseButton.LEFT) and header_rect.contains(Mouse.get_position()):
                self.start_round()
            draw_text("Click here to start round", (0, 0, 0), ui_scale * 0.3, Vector2(Window.size.x / 2, ui_scale * 0.8))

        # footer (tower selection)
        footer_rect = Rect(Window.size.x / 2, Window.size.y - ui_scale / 2, Window.size.x, ui_scale)
        pygame.draw.rect(Window.surface, (150, 200, 150), footer_rect.get_pygame_tuple(flip_y=True))

        for i in range(len(self.tower_controller.towers)):
            t_object, _, _ = self.tower_controller.towers[i]
            tower_rect = Rect((i + 0.5) * ui_scale, footer_rect.y, ui_scale, ui_scale)
            if Mouse.get_pressed(MouseButton.LEFT) and tower_rect.contains(Mouse.get_position()):
                self.selected_tower = i
            if self.selected_tower == i:
                pygame.draw.rect(Window.surface, (0, 255, 0), tower_rect.get_pygame_tuple(flip_y=True))
            t_object.draw_icon(tower_rect, Window.surface)

    def draw_path(self):
        path = self.tower_controller.board.get_path()
        if path is not None:

            def draw_line(p1, p2):
                Camera.draw_line((255, 165, 0), p1 + Vector2(0.5, 0.5), p2 + Vector2(0.5, 0.5))

            for i in range(len(path) - 1):
                node1 = path[i]
                node2 = path[i + 1]

                dp = node2 - node1
                dx, dy = dp.x, dp.y

                t1 = self.path_visual_timer
                t2 = self.path_visual_timer + 0.5

                line_start = Vector2(node1.x + dx * t1, node1.y + dy * t1)
                line_end = Vector2(node1.x + dx * (t2 % 1), node1.y + dy * (t2 % 1))

                if t2 < 1:
                    draw_line(line_start, line_end)
                else:
                    draw_line(node1, line_end)
                    draw_line(line_start, node2)
