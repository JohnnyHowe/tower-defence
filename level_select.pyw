from pygame import *
import mouse_extras, pickle
import global_functions as gfunc


def run(window_size, old_window):

    offset = [0, window_size[1]]

    init()
    screen = display.set_mode(window_size, RESIZABLE)
    test_font = font.SysFont(None, 100)
    clock = time.Clock()

    def resize(window, window_size):
        new = gfunc.event_loop()

        if new:
            window = display.set_mode(new, RESIZABLE)
            scale = min(new)
            return window, new, scale
        else:
            return window, window_size, min(window_size)


    level_info = pickle.load(open('levels.dat', 'rb'))
    levels = len(level_info)

    #x_percent = levels / ()


    while True:

        screen, window_size, window_scale = resize(screen, window_size)
        window = Surface(window_size)
        window.fill((130, 130, 130))

        dt = clock.tick() / 1000
        offset[1] -= dt * offset[1] * 5
        offset[1] = max(0, offset[1])

        # So it does stop
        if offset[1] < 1:
            offset[1] = 0

        mouse_extras.update_buttons()
        mouse_extras.update_states()

        screen.blit(transform.scale(old_window, window_size), (0,0))

        draw.rect(window, (140, 140, 140), (offset[0], offset[1] + 0, window_size[0], window_size[1]))
        screen.blit(window, offset)

        display.update()
