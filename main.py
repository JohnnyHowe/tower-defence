import pygame
from window import Window
from game import Game
from event_handler import EventHandler
from clock import Clock


def main():
    pygame.init()

    game = Game()

    while True:
        EventHandler.update()
        Clock.update()
        Window.surface.fill((100, 100, 100))
        game.update()
        game.draw()

        
if __name__ == "__main__":
    main()
