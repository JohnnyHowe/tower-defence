from pygame import *
import extra_mouse_functions, tower_manager, enemy_manager
import pickle

background = {
    'main': (200,200,200),
    'tower_selection': (100,100,100)
}

playing_grid = (20,10)
tower_selection_height = 2

window_scale = 30


w,h = playing_grid[0] * window_scale, (playing_grid[1] + tower_selection_height) * window_scale
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
    

    # Build phase
    med_font = font.SysFont(0, 30)

    while True:
        event_loop()
        mouse_extras.update()

        k = key.get_pressed()
        if k[K_RETURN]: break

        window.fill(background['main'])

        enemy_handler.update_path(window, window_scale, playing_grid, tower_handler.blocks)
        draw.rect(window, (background['tower_selection']), (0, playing_grid[1] * window_scale, w, h))

        mouse_extras.draw_on_grid(window)
        tower_handler.update(mouse_extras.get_state(), mouse_extras.pos, 0)

        dif = 2
        mes = med_font.render('Press enter to continue', 0, (0, 0, 0))
        mes2 = med_font.render('Press enter to continue', 0, (255, 255, 255))

        rect = mes.get_rect()
        window.blit(mes2, ((w - rect.width) / 2 - dif, 5 + dif))
        window.blit(mes, ((w - rect.width) / 2, 5))


        display.update()

    enemy_handler.set(level_info['enemies'])
    dt = clock.tick() / 1000
    tower_handler.held_tower = None
    
    # Fight!

    while True:

        event_loop()
        dt = clock.tick() / 1000

        window.fill(background['main'])
        
        tower_handler.update(mouse_extras.get_state(), mouse_extras.pos, 0)
        draw.rect(window, (background['tower_selection']), (0, playing_grid[1] * window_scale, w, h))

        enemy_handler.update(window, window_scale, dt)
        
        display.update()


def event_loop():
    for e in event.get():
        if e.type == QUIT:
            quit()
        if e.type == KEYDOWN:
            if e.key == K_ESCAPE:
                quit()



run(1)