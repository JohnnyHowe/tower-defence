from pygame import *
import math, time
import mouse_extras

def slope(angle):

    while angle > 360: angle -= 360
    while angle < 0: angle += 360

    if angle > 270: c = 3; angle -= 270
    elif angle > 180: c = 2; angle -= 180
    elif angle > 90: c = 1; angle -= 90
    else: c = 0

    x = angle / 90
    y = 1 - x

    if c == 1: y, x = -x, y
    if c == 2: x = -x; y = -y
    if c == 3: y, x = x, -y

    return x, y


def get_rot(p1, p2):

    xc = p1[0] - p2[0]
    yc = p1[1] - p2[1]

    rads = math.atan2(-yc, xc)
    rads %= 2 * math.pi

    degs = math.degrees(rads) - 90
    return degs


def tuple_mult(tup, multiplier):
    tup = list(tup)
    for value_i in range(len(tup)):
        tup[value_i] *= multiplier
    return tuple(tup)


def event_loop():
    for e in event.get():
        if e.type == QUIT:
            quit()
        if e.type == KEYDOWN:
            if e.key == K_ESCAPE:
                quit()

        if e.type == VIDEORESIZE:
            return e.w, e.h

font.init()
base_font = font.SysFont(None, 100)
def text_button(window, window_size, window_offset, text, text_colour, max_rect, alignment = None):
    max_rect = list(max_rect)

    test_message = base_font.render(text, 0, (0,0,0))
    rect = test_message.get_rect()

    scale = min(max_rect[2] / rect.width, max_rect[3] / rect.height)
    size = 100 * scale

    new_font = font.SysFont(None, int(size))
    message = new_font.render(text, 0, text_colour)
    message_rect = message.get_rect()

    if alignment == 'center':
        max_rect[0] -= message_rect.width / 2
        max_rect[1] -= message_rect.height / 2


    mouse_pos = list(mouse.get_pos())
    mouse_pos[0] -= window_offset[0]
    mouse_pos[1] -= window_offset[1]

    mouse_pos[0] = int(mouse_pos[0])
    mouse_pos[1] = int(mouse_pos[1])

    mouse_rect = (mouse_pos[0], mouse_pos[1], 0, 0)


    window.blit(message, (max_rect[0], max_rect[1]))

    rect = (max_rect[0], max_rect[1], message_rect.width, message_rect.height)
    if key.get_pressed()[K_F2]:
        draw.rect(window, (200, 200, 50), rect, 2)
        draw.circle(window, (0,0,0), mouse_pos, 5)


    if mouse_extras.get_states()[0] == -1:
        if touching(rect, mouse_rect):
            return True





def touching(rect1, rect2):

    if rect1[0] + rect1[2] >= rect2[0]:
        if rect1[0] <= rect2[0] + rect2[2]:
            if rect1[1] + rect1[3] >= rect2[1]:
                if rect1[1] <= rect2[1] + rect2[3]:

                    return True
    return False

last_time = time.time()
def fps_counter():
    global last_time

    temp_time = time.time()
    time_since_last = temp_time - last_time

    fps = 1 / time_since_last
    last_time = temp_time

    return fps


def show_fps(window):

    rect = window.get_rect()

    window_scale = min(rect.width, rect.height) * 0.1

    f = font.SysFont(None, int(window_scale * 1))
    message = f.render(str(int(fps_counter())), 0, (200, 200, 0))

    dist = window_scale * 0.5
    window.blit(message, (dist, dist))


def get_pos_on_path(path, dist):

    if dist + 1 >= len(path):
        return False

    last_full = path[int(dist)]
    next_full = path[int(dist) + 1]

    xc = next_full[0] - last_full[0]
    yc = next_full[1] - last_full[1]

    pc = dist - int(dist)

    xd = xc * pc
    yd = yc * pc

    pos = list(last_full)

    pos[0] += xd
    pos[1] += yd

    return pos


font.init()
default_font = font.SysFont(None, 100) # Used to find the real font (to work out scale)
def show_message(text, window, colour = (70, 70, 70), size = None, pos = 'mid', boarder = 0.2):

    window_rect = window.get_rect()
    max_width = window_rect.width
    max_height = window_rect.height

    if not size:

        # Working out scale
        message = default_font.render(text, 0, (0, 0, 0))
        mes_rect = message.get_rect()
        mes_rect.height += boarder * 100
        mes_rect.width += boarder * 100

        scale = min(max_width / mes_rect.width, max_height / mes_rect.height)
        size = int(scale * 100)

    # Make message
    use_font = font.SysFont(None, int(size))
    message = use_font.render(text, 0, colour)

    # Center message
    rect = message.get_rect()

    if type(pos) == tuple or type(pos) == list:

        pos = list(pos)

        if pos[0] == 'mid': pos[0] = (max_width - rect.width) / 2
        elif pos[0] == 'right': pos[0] = max_width - rect.width - boarder * size / 2
        elif pos[0] == 'left': pos[0] = (max_height - rect.height) / 2

        if pos[1] == 'mid': pos[1] = (max_height - rect.height) / 2
        elif pos[1] == 'top': pos[1] = boarder * size / 2
        elif pos[1] == 'low': pos[1] = max_height - rect.height - boarder * size / 2

    elif pos == 'left': pos = boarder * size / 2, (max_height - rect.height) / 2
    elif pos == 'right': pos = max_width - rect.width - boarder * size / 2, (max_height - rect.height) / 2
    else: pos = (max_width - rect.width) / 2, (max_height - rect.height) / 2

    window.blit(message, pos)




