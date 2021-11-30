
class GameGrid:

    items: list
    size: tuple
    path = []
    grid_changed = True     # Flag set when board has changed and path is outdated

    def __init__(self, size: tuple):
        self.items = [None, ] * size[0] * size[1]
        self.size = size

    def get_at(self, position: tuple):
        if not self.is_on_grid(position): return None
        return self.items[self.get_index(position)]

    def set_at(self, position, obj):
        if self.items[self.get_index(position)] != obj:
            self.items[self.get_index(position)] = obj
            self.grid_changed = True

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
            self.grid_changed = True

    def get_path(self):
        if self.grid_changed:
            self.update_path()
            self.grid_changed = False
        return self.path


    def update_path(self):
        self.path = self.generate_path()
        
    def generate_path(self):
        candidates = [(-1, y, None) for y in range(self.size[1])]
        explored = []
        final_node = None

        def h(x): return abs(x[0] - self.size[0])

        while len(candidates) > 0:
            # Sort candidates by h
            candidates.sort(key=h)

            candidate = candidates.pop(0)
            explored.append(candidate[:2])

            # If candidate is a goal
            if candidate[0] >= self.size[0] - 1:
                final_node = candidate
                break

            # Else, add neighbours to candidates
            for dx, dy in [(-1, 0), (1, 0), (0, -1), (0, 1)]:
                neighbour_pos = (candidate[0] + dx, candidate[1] + dy)
                neighbour = neighbour_pos + (candidate,)

                # If neighbour is valid and unexplored
                if self.is_on_grid(neighbour_pos) and self.is_empty(neighbour_pos) and neighbour_pos not in explored:
                    candidates.append(neighbour)

        if final_node is None:
            return None

        # Construct path/backtrack
        path = [final_node[:2]]
        while final_node is not None:
            path.append(final_node[:2])
            final_node = final_node[2]

        return list(reversed(path))