'''
-1: obstacle
None: empty
0: start
>1: dist from start
'''

def get_path(blocks, grid_size):

    grid = [[None for y in range(grid_size[1])] for x in range(grid_size[0])]

    candidates = []

    for block in blocks:
        grid[block.pos[0]][block.pos[1]] = -1

    for y in range(grid_size[1]):
        grid[0][y] = 0        

        if grid[1][y] == None:
            candidates.append((1, y, 1))

    directions = [(1, 0), (-1, 0), (0, 1), (0, -1)]

    print(candidates)

    while True:
        current = candidates.pop(0)
        #print(current[2])

        for opt in directions:
            new_pos = opt[0] + current[0], opt[1] + current[1]
            
            # is it in a valid spot?
            
            # is it on the grid
            if new_pos[0] >= 0 and new_pos[0] <= grid_size[0] - 1:
                if new_pos[1] >= 0 and new_pos[1] <= grid_size[1] - 1:
                    
                    # is the spot empty?
                    if grid[new_pos[0]][new_pos[1]] == None:
                        candidates.append(new_pos + (current[2] + 1,))
            
        grid[current[0]][current[1]] = current[2]

        if len(candidates) == 0:
            return False

        stop = False
        for y in range(grid_size[1]):
            if grid[grid_size[0] - 1][y]:
                stop = True
                break
        if stop: break

    for i in grid: print(i)

    # backtrack to find path

    # Find end pos with lowest value
    end_x = grid_size[0] - 1

    lowest = None
    pos = None
    
    for y in range(grid_size[1]):
        value = grid[end_x][y]

        if type(value) == int:

            if not type(lowest) == int:
                lowest = value
                pos = (end_x, y)

            elif value < lowest:
                lowest = value
                pos = (end_x, y)
    
    positions = [pos]
    moves = grid[pos[0]][pos[1]]

    for move in range(moves):
        last_pos = positions[len(positions) - 1]
        number = moves - move

        for opt in directions:
            new_pos = opt[0] + last_pos[0], opt[1] + last_pos[1]

            # Check new pos
            
            if new_pos[0] >= 0 and new_pos[0] <= grid_size[0] - 1:
                if new_pos[1] >= 0 and new_pos[1] <= grid_size[1] - 1:
            
                    if grid[new_pos[0]][new_pos[1]] == number - 1:
                        positions.append(new_pos)
                        break

    positions.reverse()
    print(positions)
    return positions
