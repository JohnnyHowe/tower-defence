from pygame import *
import extra_mouse_functions, tower_manager


background = {
    'main': (200,200,200),
    'tower_selection': (100,100,100)
}

playing_grid = (15,7)
tower_selection_height = 2

window_scale = 50


w,h = playing_grid[0] * window_scale, (playing_grid[1] + tower_selection_height) * window_scale
window = display.set_mode((w,h))
display.set_caption('Tower Defense')
clock = time.Clock()


#Initiate modules
mouse_extras = extra_mouse_functions.Mouse(window_scale)
tower_handler = tower_manager.Handler(playing_grid, window_scale, window)

def run():


    while True:
        event_loop()
        mouse_extras.update()


        window.fill(background['main'])
        draw.rect(window, (background['tower_selection']), (0, playing_grid[1] * window_scale, w, h))

        mouse_extras.draw_on_grid(window)
        tower_handler.update(mouse_extras.get_state(), mouse_extras.pos)

        clock.tick(20)
        display.update()


def event_loop():
    for e in event.get():
        if e.type == QUIT:
            quit()



run()