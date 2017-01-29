from pygame import *
import pickle
import global_functions as gfunc

def run(level, window_size):

    # Set up
    window = display.set_mode(window_size, RESIZABLE)

    # Get level info
    level_info = pickle.load(open('levels.dat', 'rb'))[level]

    # Scale window correctly
    game_grid = level_info['grid_size']
    scale = min(window_size[0] / game_grid[0], window_size[1] / game_grid[1])
    game_size = scale * game_grid[0], scale * game_grid[1]
    game_window = Surface(game_size)

    # Make background functions (just for ease later)
    def show_background_image(background): game_window.blit(background, (0,0))
    def show_background_colour(background): game_window.fill(background)

    def resize(window_size, window, game_window, game_size):

        # Size and offset the game correctly
        new = gfunc.event_loop()
        scale = min(window_size[0] / game_grid[0], window_size[1] / game_grid[1])
        game_size = game_grid[0] * scale, game_grid[1] * scale
        game_window = Surface(game_size)
        offset = (window_size[0] - game_size[0]) / 2, (window_size[1] - game_size[1]) / 2

        if new: window_size = new; window = display.set_mode(window_size, RESIZABLE)
        return offset, window, window_size, game_window, game_size

    # Set background functions
    if type(level_info['background']) == tuple: show_background = show_background_colour; background = level_info['background']
    else: show_background = show_background_image; background = image.load(level_info['background'])

    # Set up loop (game)
    while True:

        # Must be at start
        offset, window, window_size, game_window, game_size = resize(window_size, window, game_window, game_size)

        show_background(background)

        # Must be at end
        window.fill((30, 30, 30))
        window.blit(game_window, offset)

        display.update()

