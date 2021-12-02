from clock import Clock
from camera import Camera

from game_grid import GameGrid

from wall import Wall
from machine_gun import MachineGun


class TowerController:
    board = None
    
    # a list of possible towers to be on the board.
    # in form [(obj, class, requires base), ]
    towers = [
        (Wall((0, 0), []), Wall, False),
        (MachineGun((0, 0), []), MachineGun, True),
    ]

    # list of current projectiles
    projectiles: list

    def __init__(self, board_size):
        self.board = GameGrid(board_size)
        self.projectiles = []

    def try_place_tower(self, cell, tower_index):
        tower_object, tower_class, requires_base = self.towers[tower_index]
        if self.towers[tower_index][2] and not self.board.is_base_empty(cell) and self.board.is_item_empty(cell):
            self.board.set_item_at(cell, tower_class(cell, self.projectiles))
        if self.board.is_base_empty(cell) and not self.towers[tower_index][2]:
            self.board.set_base_at(cell, tower_class(cell, self.projectiles))

    def draw(self):
        self.draw_board()
        self.draw_projectiles()

    def draw_board(self):
        """ Draw the main game board and all its bits. """
        game_board_top = self.board.size[1]
        game_board_left = 0
        game_board_bottom = game_board_top - self.board.size[1]

        # game board
        Camera.draw_rect((255, 255, 255), (game_board_left, game_board_top, self.board.size[0], game_board_top - game_board_bottom))

        # placed towers
        for tower in self.board.get_all_base() + self.board.get_all_items():
            # Camera.draw_image(tower.get_image(), (tower.position[0], tower.position[1] + 1) + (1, 1))
            tower.draw()

    def draw_projectiles(self):
        for projectile in self.projectiles:
            projectile.draw()

    def update(self, first_enemy):
        for tower in self.board.get_all_items() + self.board.get_all_base():
            tower.update(first_enemy)
        self.update_projectiles()

    def update_projectiles(self):
        for projectile in self.projectiles:
            projectile.update()

