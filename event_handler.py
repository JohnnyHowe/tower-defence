import pygame
from window import Window


class _EventHandler:
    events = []

    def update(self):
        self.events = pygame.event.get()
        self.event_loop()

    def event_loop(self):
        for event in self.events:
            if event.type == pygame.QUIT:
                quit()
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_ESCAPE:
                    quit()
            if event.type == pygame.VIDEORESIZE:
                Window.update_size((event.w, event.h))

    def get_event(self, event_type):
        event = self.get_events(event_type)
        return event[0] if event else None
            
    def get_events(self, event_type):
        """ Get a list of events with event_type. """
        return [event for event in self.events if event.type == event_type]


EventHandler = _EventHandler()