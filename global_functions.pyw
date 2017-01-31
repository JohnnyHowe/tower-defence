from pygame import *

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