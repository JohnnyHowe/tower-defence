from pygame import *


def update_states():

    try:

        global states, old_state
        new_state = mouse.get_pressed()

        for state_i in range(len(states)):
            states[state_i] = new_state[state_i] - old_state[state_i]

        old_state = new_state

    except:

        states = [0,0,0]
        old_state = [0,0,0]

        global states, old_state


def update(window_scale):
    update_states()


def get_states():
    global states
    return states

