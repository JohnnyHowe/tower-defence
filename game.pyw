from pygame import *
import extra_mouse_functions, tower_manager, enemy_manager
import pickle

background = {
    'main': (200,200,200),
    'tower_selection': (185, 185, 185)
}

images = {
    'coin': image.load('images\\misc\\coin.png'),
    'pause': image.load('images\\misc\\pause.png'),
}

playing_grid = (10,5)
tower_selection_height = 2

p = 300
window_scale = int(p / playing_grid[1])

dev = 1

w,h = int(playing_grid[0] * window_scale), int((playing_grid[1] + tower_selection_height) * window_scale)
init()
window = display.set_mode((w,h))
display.set_caption('Tower Defense')
clock = time.Clock() 

# Initiate modules
mouse_extras = extra_mouse_functions.Mouse(window_scale)
tower_handler = tower_manager.Handler(playing_grid, window_scale, window)
enemy_handler = enemy_manager.Enemy_Handler()

def run(level_num):

    levels = pickle.load(open('levels.dat', 'rb'))
    level_info = levels[level_num]
    money = level_info['start_money']

    while True:
                
        # Build phase

        med_font = font.SysFont(0, 30)

        while True:
            event_loop()
            mouse_extras.update()

            k = key.get_pressed()

            window.fill(background['main'])

            # Tower selection greyout
            draw.rect(window, (background['tower_selection']), (0, playing_grid[1] * window_scale, w, h))

            mouse_extras.draw_on_grid(window)

            dif = 2
            if enemy_handler.update_path(window, window_scale, playing_grid, tower_handler.blocks):

                # Continue message
                mes = med_font.render('Press enter to continue', 0, (0, 0, 0))
                mes2 = med_font.render('Press enter to continue', 0, (255, 255, 255))
                rect = mes.get_rect()

                money = tower_handler.update(mouse_extras.get_state(), mouse_extras.pos, 0, money, None, dev)
                window.blit(mes2, ((w - rect.width) / 2 - dif, 5 + dif))
                window.blit(mes, ((w - rect.width) / 2, 5))
                if k[K_RETURN]: break

            else:

                # Can't continue message
                mes = med_font.render('Clear path to continue', 0, (0, 0, 0))
                mes2 = med_font.render('Clear path to continue', 0, (255, 255, 255))
                rect = mes.get_rect()

                money = tower_handler.update(mouse_extras.get_state(), mouse_extras.pos, 0, money, None, dev)
                window.blit(mes2, ((w - rect.width) / 2 - dif, 5 + dif))
                window.blit(mes, ((w - rect.width) / 2, 5))
 

            # Show coins
            coin_size = 30
            show_image(images['coin'], (10, 10, coin_size, coin_size))
            money_message = med_font.render(str(money), 0, (240, 200, 50))
            money_message2 = med_font.render(str(money), 0, (0, 0, 0))

            rect = money_message.get_rect()
            window.blit(money_message2, (coin_size + 22, 12 + (coin_size - rect.height) / 2))
            window.blit(money_message, (coin_size + 20, 10 + (coin_size - rect.height) / 2))

            display.update()

        enemy_handler.set(level_info['enemies'])
        dt = clock.tick() / 1000
        tower_handler.held_tower = None
        
        # Fight!
        while True:

            event_loop()
            dt = clock.tick() / 1000

            window.fill(background['main'])
            
            tower_handler.update(mouse_extras.get_state(), mouse_extras.pos, 1, None, dt, dev)
            tower_handler.manage_towers(enemy_handler.enemies, dt, window, window_scale)
            draw.rect(window, (background['tower_selection']), (0, playing_grid[1] * window_scale, w, h))
            
            if enemy_handler.update(window, window_scale, dt, playing_grid, dev): break
            enemy_handler.enemies = tower_handler.do_damage(enemy_handler.enemies, window_scale, window)

            display.update()

        # Death screen
        tower_handler.reset()
        while True:

            event_loop()
            dt = clock.tick() / 1000
            mouse_extras.update()

            window.fill(background['main'])
            
            tower_handler.update(mouse_extras.get_state(), mouse_extras.pos, 2, None, None, dev)

            draw.rect(window, (background['tower_selection']), (0, playing_grid[1] * window_scale, w, h))
            enemy_handler.update(window, window_scale, dt, playing_grid, dev)

            # Show death window
            if death_window(window, playing_grid, window_scale, mouse_extras.get_state()) == 0:
                break
            
            display.update()


def event_loop():
    global dev

    for e in event.get():
        if e.type == QUIT:
            quit()
        if dev:
            if e.type == KEYDOWN:
                if e.key == K_ESCAPE:
                    quit()
        if e.type == KEYDOWN:
            if e.key == K_F2:
                dev = abs(dev - 1)

def show_image(img, rect):
    img = transform.scale(img, rect[2:])
    window.blit(img, rect[:2])

def button(window, mouse_state, pos, size, text, colour, background_colour, background_colour2):
    f = font.SysFont(0, size)
    mouse_pos = mouse.get_pos()
    mouse_button = mouse.get_pressed()
    message = f.render(text, 0, colour)

    rect = message.get_rect()
    
    if mouse_pos[0] > pos[0]:
        if mouse_pos[0] < pos[0] + rect.width:
            if mouse_pos[1] > pos[1]:
                if mouse_pos[1] < pos[1] + rect.height:

                    if mouse_state[0] == -1:
                        draw.rect(window, background_colour, pos + (rect.width, rect.height))
                        window.blit(message, pos)
                        return True
    
                    elif mouse_button[0]:
                        draw.rect(window, background_colour2, pos + (rect.width, rect.height))
                        window.blit(message, pos)
                        return False
    window.blit(message, pos)
    
 

head = font.SysFont(0, window_scale)
def death_window(window, game_grid, game_scale, mouse_state):
    window_size = list(game_grid)
    window_size[0] *= game_scale; window_size[1] *= game_scale

    # Show pause background
    scale = 5
    img = images['pause']
    rect = img.get_rect()
    y_scale = rect.height / rect.width
    this_size = (game_scale * scale, int(game_scale * scale * y_scale))
    img = transform.scale(img, this_size)
    rect = img.get_rect()
    win_rect = rect

    x = (window_size[0] - rect.width) / 2
    y = (window_size[1] - rect.height) / 2

    window.blit(img, (x,y)) 

    text_colour = (50, 50, 50)

    # Make and show centered message
    message = head.render('You Failed!', 0, text_colour)
    rect = message.get_rect()
    mess_x = x + this_size[0] / 2 - rect.width / 2
    window.blit(message, (mess_x, y + 20))

    button_size = game_scale / 2
    button_y = y + win_rect.height - button_size - game_scale / 2.5
    if button(window, mouse_state, (game_scale + x, button_y), int(button_size), 'restart', text_colour, (127, 127, 127), (120, 120, 120)):
        return 0

run(1)