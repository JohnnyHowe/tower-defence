from engine_math import Vector2


class GridPathFinder:
    last_board_id: str
    path: list
    greediness = 1  # multiplier on heurisitc function

    def __init__(self, board):
        self.board = board
        self.last_board_id = self.get_board_id()
        self.update_path()

    def get_board_id(self):
        """ Just a hash of the contents of the board """
        return hash(str(self.board.items)) + hash(str(self.board.base))

    def get_path(self):
        new_id = self.get_board_id()
        if self.last_board_id != new_id:
            self.update_path()
            self.last_board_id = new_id
        return self.path

    def update_path(self):
        self.path = self.generate_path()

    def generate_path(self):
        candidates = [(Vector2(-1, y), None) for y in range(self.board.size.y)]
        explored = set()
        final_node = None

        while len(candidates) > 0 and final_node is None:
            # Sort candidates by h

            candidate = candidates.pop(0)
            if tuple(candidate[0]) in explored:
                continue
            explored.add(tuple(candidate[0]))

            # If candidate is a goal
            if candidate[0].x >= self.board.size.x - 1:
                final_node = candidate
                break

            # Else, add neighbours to candidates
            for dx, dy in [(-1, 0), (1, 0), (0, -1), (0, 1)]:
                neighbour_pos = Vector2(candidate[0].x + dx, candidate[0].y + dy)
                neighbour = (neighbour_pos, candidate)

                # If neighbour is valid and unexplored
                if neighbour_pos not in explored and self.board.is_on_grid(neighbour_pos) and self.board.is_base_empty(neighbour_pos):
                    candidates.append(neighbour)

        if final_node is None:
            return None

        # Construct path/backtrack
        path = [Vector2(final_node[0].x + 1, final_node[0].y)]
        while final_node is not None:
            path.append(final_node[0])
            final_node = final_node[1]

        return list(reversed(path))


class GameGrid:

    items: list
    base: list
    size: tuple
    pathfinder: GridPathFinder

    def __init__(self, size: tuple):
        self.base = [None, ] * size.x * size.y
        self.items = [None, ] * size.x * size.y
        self.size = size
        self.pathfinder = GridPathFinder(self)

    def get_base_at(self, position: tuple):
        if not self.is_on_grid(position):
            return None
        return self.base[self.get_index(position)]

    def get_item_at(self, position: tuple):
        if not self.is_on_grid(position):
            return None
        return self.items[self.get_index(position)]

    def set_base_at(self, position, obj):
        if self.base[self.get_index(position)] != obj:
            self.base[self.get_index(position)] = obj

    def set_item_at(self, position, obj):
        if self.items[self.get_index(position)] != obj:
            self.items[self.get_index(position)] = obj

    def is_item_empty(self, position):
        if not self.is_on_grid(position):
            return False
        return self.get_item_at(position) is None

    def is_base_empty(self, position):
        if not self.is_on_grid(position):
            return False
        return self.get_base_at(position) is None

    def get_index(self, position: tuple) -> int:
        return int(position.x + position.y * self.size.x)

    def is_on_grid(self, position: Vector2) -> bool:
        return 0 <= position.x < self.size.x and 0 <= position.y < self.size.y

    def get_all_items(self):
        return [item for item in self.items if item is not None]

    def get_all_base(self):
        return [item for item in self.base if item is not None]

    def clear_at(self, position):
        if not self.is_item_empty(position):
            self.clear_item_at(position)
        else:
            self.clear_base_at(position)

    def clear_item_at(self, position):
        if self.items[self.get_index(position)] is not None:
            self.set_item_at(position, None)

    def clear_base_at(self, position):
        if self.base[self.get_index(position)] is not None:
            self.set_base_at(position, None)

    def get_path(self):
        return self.pathfinder.get_path()
