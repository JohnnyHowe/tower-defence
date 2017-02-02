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
    message_height = 1
    game_grid = level_info['grid_size']
    scale = min(window_size[0] / game_grid[0], window_size[1] / (game_grid[1] + message_height))
    game_size = scale * game_grid[0], scale * game_grid[1]
    game_window = Surface(game_size)

    # Make message surface
    message_surf = Surface((game_size[0], math.ceil(scale)))

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
        scale = min(window_size[0] / playing_grid[0], window_size[1] / (playing_grid[1] + message_height))
        game_size = playing_grid[0] * scale, playing_grid[1] * scale
        game_window = Surface(game_size)
        offset = (window_size[0] - game_size[0]) / 2, math.ceil((window_size[1] - game_size[1] + scale) / 2)

        if new: window_size = new; window = display.set_mode(window_size, RESIZABLE)
        return offset, window, window_size, game_window, game_size, scale

    # Set background functions
    if type(level_info['background']) == tuple: show_background = show_background_colour; background = level_info['background']
    else: show_background = show_background_image; background = image.load(level_info['background'])

    # Path message
    red_value = 255
    last_red_change = -1

    # Set up loop (game)
    while True:

        # Must be at start
        offset, window, window_size, game_window, game_size, game_scale = resize(window_size, window, game_window, game_size)
        mouse_extras.update(game_scale, playing_grid, offset)
        message_surf = Surface((game_size[0], math.ceil(game_scale)))

        # Clear window(s)
        show_background(background)
        message_surf.fill((150, 150, 150))

        # Do important things
        dt = clock.tick() / 1000

        # Update towers
        tower_handler.tower_selection(game_window, game_scale, game_grid, tower_select_rows)

        # Update path
        enemy_handler.update_path(game_window, game_scale, game_grid, tower_handler.blocks, dt)

        # Show message

        if enemy_handler.path:
            gfunc.show_message('Build stage!', message_surf, size = game_scale * 0.7, pos = ('mid', 'top'))
            gfunc.show_message('Press enter to start the wave!', message_surf, size = game_scale * 0.5, pos = ('mid', 'low'), colour = (90, 90, 90))
        else:
            gfunc.show_message('It must be possible for the enemies to get through!', message_surf, colour = (red_value, 50, 0), boarder = 0.3)

            # Make the error message change colour for a cool animation
            red_value += last_red_change * dt * 500
            red_value = max(min(255, red_value), 150)
            if red_value >= 255 or red_value <= 150: last_red_change = -last_red_change

        # Must be at end
        window.fill((30, 30, 30))
        window.blit(game_window, offset)
        window.blit(message_surf, (offset[0], offset[1] - game_scale))

        display.update()

