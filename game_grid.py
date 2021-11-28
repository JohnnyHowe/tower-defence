
class GameGrid:

    items = list
    size: tuple

    def __init__(self, size: tuple):
        self.items = [None,] * size[0] * size[1]
        self.size = size

    def get_at(self, position: tuple):
        if not self.is_on_grid(position):
            raise Exception("Cannot get item at position {}".format(position)) 
        return self.items[self.get_index(position)]

    def get_index(self, position: tuple) -> bool:
        return position[0] + position[1] * self.size[0]

    def is_on_grid(self, position: tuple) -> bool:
        return 0 <= position[0] < self.size[0] and 0 <= position[1] < self.size[1]
