
from typing_extensions import get_args


class GameGrid:

    items: list
    size: tuple

    def __init__(self, size: tuple):
        self.items = [None, ] * size[0] * size[1]
        self.size = size

    def get_at(self, position: tuple):
        if not self.is_on_grid(position): return None
        return self.items[self.get_index(position)]

    def set_at(self, position, obj):
        self.items[self.get_index(position)] = obj

    def is_empty(self, position):
        if not self.is_on_grid(position): return False
        return self.get_at(position) is None

    def get_index(self, position: tuple) -> int:
        return position[0] + position[1] * self.size[0]

    def is_on_grid(self, position: tuple) -> bool:
        return 0 <= position[0] < self.size[0] and 0 <= position[1] < self.size[1]

    def get_all(self):
        return [item for item in self.items if item is not None]

    def clear_at(self, position):
        self.set_at(position, None)
