from pygame import *

class Mouse:

    def __init__(self, window_scale):
        self.window_scale = window_scale
        self.update()

    def draw_on_grid(self, window):
        pos = (self.pos[0] * self.window_scale, self.pos[1] * self.window_scale)

        rect = Surface((self.window_scale, self.window_scale))
        rect.set_alpha(70)
        rect.fill((255,255,255))
        window.blit(rect, pos)


    old_button_state = []
    event_state = []

    #ONLY ONCE EVERY LOOP!!!
    def update(self):

        #Position
        pos = mouse.get_pos()
        self.pos = pos[0] // self.window_scale, pos[1] // self.window_scale


        #States
        current_state = mouse.get_pressed()

        if self.old_button_state == []:
            self.old_button_state = current_state
            self.event_state = current_state

        else:
            new_event_states = []

            for index in range(len(current_state)):
                new_event_states.append((current_state[index] - self.old_button_state[index]))

            self.event_state = new_event_states
            self.old_button_state = current_state

    def get_state(self):
        return tuple(self.event_state)

