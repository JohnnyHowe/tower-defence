
class GridPathFinder:
    last_board_id: str
    path: list
    greediness = 2  # multiplier on heurisitc function

    def __init__(self, board):
        self.board = board
        self.last_board_id = self.get_board_id()
        self.update_path()

    def get_board_id(self):
        """ Just a hash of the contents of the board """
        return hash(str(self.board.items))

    def get_path(self):
        new_id = self.get_board_id()
        if self.last_board_id != new_id:
            self.update_path()
            self.last_board_id = new_id
        return self.path

    def update_path(self):
        self.path = self.generate_path()

    def generate_path(self):
        candidates = [(-1, y, None, 0) for y in range(self.board.size[1])]
        explored = []
        final_node = None

        def h(x): return abs(x[0] - self.board.size[0])
        def c(x): return x[3]
        def f(x): return c(x) + h(x) * self.greediness

        while len(candidates) > 0 and final_node is None:
            # Sort candidates by h
            candidates.sort(key=f)

            candidate = candidates.pop(0)
            explored.append(candidate[:2])

            # If candidate is a goal
            if candidate[0] >= self.board.size[0] - 1:
                final_node = candidate
                break

            # Else, add neighbours to candidates
            for dx, dy in [(-1, 0), (1, 0), (0, -1), (0, 1)]:
                neighbour_pos = (candidate[0] + dx, candidate[1] + dy)
                neighbour = neighbour_pos + (candidate, candidate[3] + 1)

                # If neighbour is valid and unexplored
                if self.board.is_on_grid(neighbour_pos) and self.board.is_empty(neighbour_pos) and neighbour_pos not in explored:
                    candidates.append(neighbour)

        if final_node is None:
            return None

        # Construct path/backtrack
        path = [final_node[:2]]
        while final_node is not None:
            path.append(final_node[:2])
            final_node = final_node[2]

        return list(reversed(path)) 


class GameGrid:

    items: list
    size: tuple
    pathfinder: GridPathFinder

    def __init__(self, size: tuple):
        self.items = [None, ] * size[0] * size[1]
        self.size = size
        self.pathfinder = GridPathFinder(self)

    def get_at(self, position: tuple):
        if not self.is_on_grid(position): return None
        return self.items[self.get_index(position)]

    def set_at(self, position, obj):
        if self.items[self.get_index(position)] != obj:
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
        if self.items[self.get_index(position)] is not None:
            self.set_at(position, None)

    def get_path(self):
        return self.pathfinder.get_path()
