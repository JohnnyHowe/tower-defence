from pygame import *
import math
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


def text_button(window, window_size, window_offset, text, text_colour, rect, margin = 0.02, background_rect = None):
    base_font = font.SysFont(None, 100)

    # Text will be centered in the rect

    # Show button
    # Draw rect
    if background_rect:

        # Using this instead of draw.rect() so alpha values will work
        surf = Surface((rect[2:]))
        surf.fill(background_rect)

        # Add alpha
        if len(background_rect) == 4: surf.set_alpha(background_rect[3])
        window.blit(surf, rect[:2])


    mess_surf = base_font.render(text, 0, text_colour)
    mes_rect = mess_surf.get_rect()

    x_scale = rect[2] / mes_rect.width
    y_scale = rect[3] / mes_rect.height

    scale = min(x_scale, y_scale)

    new_font = font.SysFont(None, int(scale * 100))
    new_mes_surf = new_font.render(text, 0, text_colour)
    new_mes_rect = new_mes_surf.get_rect()

    if len(text_colour) == 4: new_mes_surf.set_alpha(text_colour[3])

    x = (rect[2] - new_mes_rect.width) / 2 + rect[0]
    y = (rect[3] - new_mes_rect.height) / 2 + rect[1]

    new_mes_rect_list = [x, y, new_mes_rect.width, new_mes_rect.height]
    window.blit(new_mes_surf, (x, y))


    # Is the button clicked?
    states = mouse_extras.get_states()

    mouse_pos = mouse.get_pos()
    mouse_rect = [mouse_pos[0] - window_offset[0], mouse_pos[1] - window_offset[1], 0, 0]

    if key.get_pressed()[K_F2]:
        draw.rect(window, (200, 200, 0), new_mes_rect_list, 2)
        draw.rect(window, (0, 0, 0), mouse_rect, 20)

    if touching(new_mes_rect_list, mouse_rect):
        if mouse_extras.get_states()[0] == -1:
            return True



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




