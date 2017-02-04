from pygame import *
import math

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


def event_loop():
    for e in event.get():
        if e.type == QUIT:
            quit()
        if e.type == KEYDOWN:
            if e.key == K_ESCAPE:
                quit()

        if e.type == VIDEORESIZE:
            return e.w, e.h


def touching(rect1, rect2):

    if rect1[0] + rect1[2] >= rect2[0]:
        if rect1[0] <= rect2[0] + rect2[2]:
            if rect1[1] + rect1[3] >= rect2[1]:
                if rect1[1] <= rect2[1] + rect2[3]:

                    return True
    return False


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




