from pygame import *
import pickle, math, mouse_extras, tower_manager, enemy_manager
import global_functions as gfunc

def run(level, window_size):

    # Set up
    window = display.set_mode(window_size, RESIZABLE)
    clock = time.Clock()

    # Get level info
    level_info = pickle.load(open('levels.dat', 'rb'))[level]

    # Scale window correctly
    game_grid = level_info['grid_size']
    scale = min(window_size[0] / game_grid[0], window_size[1] / game_grid[1])
    game_size = scale * game_grid[0], scale * game_grid[1]
    game_window = Surface(game_size)

    # Start up handlers
    tower_handler = tower_manager.Tower_Handler()
    enemy_handler = enemy_manager.Enemy_Handler()

    # Work out tower selection size
    num = len(tower_handler.usable_towers)
    rows = math.ceil(num / game_grid[0])
    playing_grid = list(game_grid)
    playing_grid[1] += rows
    tower_select_rows = rows

    # Make background functions (just for ease later)
    def show_background_image(background): game_window.blit(background, (0,0))
    def show_background_colour(background): game_window.fill(background)

    def resize(window_size, window, game_window, game_size):

        # Size and offset the game correctly
        new = gfunc.event_loop()
        scale = min(window_size[0] / playing_grid[0], window_size[1] / playing_grid[1])
        game_size = playing_grid[0] * scale, playing_grid[1] * scale
        game_window = Surface(game_size)
        offset = (window_size[0] - game_size[0]) / 2, (window_size[1] - game_size[1]) / 2

        if new: window_size = new; window = display.set_mode(window_size, RESIZABLE)
        return offset, window, window_size, game_window, game_size, scale

    # Set background functions
    if type(level_info['background']) == tuple: show_background = show_background_colour; background = level_info['background']
    else: show_background = show_background_image; background = image.load(level_info['background'])

    # Set up loop (game)
    while True:

        # Must be at start
        offset, window, window_size, game_window, game_size, game_scale = resize(window_size, window, game_window, game_size)
        mouse_extras.update(game_scale, playing_grid, offset)

        # Clear window
        show_background(background)

        # Do important things
        dt = clock.tick() / 1000

        # Update towers
        tower_handler.tower_selection(game_window, game_scale, game_grid, tower_select_rows)

        # Update path
        enemy_handler.update_path(game_window, game_scale, game_grid, tower_handler.blocks, dt)

        # Must be at end
        window.fill((30, 30, 30))
        window.blit(game_window, offset)

        display.update()

