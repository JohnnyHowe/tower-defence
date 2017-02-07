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

    # Fancy hitbox things
    def show_dev_things():

        if key.get_pressed()[K_F2]:

            # Enemies
            for enemy in enemy_handler.enemies:
                rect = enemy.get_rect(game_scale)

                if rect:
                    draw.rect(game_window, (255, 100, 100), rect, 2)

            # Towers
            for tower in tower_handler.towers:
                draw.rect(game_window, (100, 255, 100), (tower.pos[0] * game_scale, tower.pos[1] * game_scale, game_scale, game_scale), 2)

                # Projectiles
                for obj in tower.projectiles:
                    draw.rect(game_window, (100, 100, 255), obj.get_rect(game_scale), 2)



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

    enemy_handler.load_enemies(level_info['enemies'])

    # Game loop (loop through the stages)
    while True:

        # Set up loop (game)
        while True:

            # Must be at start
            offset, window, window_size, game_window, game_size, game_scale = resize(window_size, window, game_window, game_size)
            mouse_extras.update(game_scale, playing_grid, offset)
            message_surf = Surface((game_size[0], math.ceil(game_scale)))

            # Does the game need to progress to the next stage?
            k = key.get_pressed()
            if k[K_RETURN] and enemy_handler.path: break

            # Does the game grid need to be cleared?
            if k[K_c]: tower_handler.clear_towers()

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


        enemy_handler.set_enemy_path()

        # Fight!
        while True:

            # Must be at start
            offset, window, window_size, game_window, game_size, game_scale = resize(window_size, window, game_window, game_size)
            mouse_extras.update(game_scale, playing_grid, offset)
            message_surf = Surface((game_size[0], math.ceil(game_scale)))

             # Clear/set up window(s)
            show_background(background)
            message_surf.fill((150, 150, 150))

            # Do we want to restart the game?
            if key.get_pressed()[K_r]:
                enemy_handler.load_enemies(level_info['enemies'])
                break

            tower_handler.draw_selection_block(game_window, game_scale, game_grid, tower_select_rows)

            # Do important things
            dt = clock.tick() / 1000

            # Update towers
            tower_handler.update_towers(game_window, game_scale, game_grid, dt)

            # Update enemies
            enemy_handler.update_enemies(game_window, game_scale, game_grid, dt)

            # Do the damage
            enemy_handler.enemies = tower_handler.do_damage(enemy_handler.enemies, game_scale)

            # Fancy
            show_dev_things()

            # Must be at end
            window.fill((30, 30, 30))
            window.blit(game_window, offset)
            window.blit(message_surf, (offset[0], offset[1] - game_scale))

            display.update()
