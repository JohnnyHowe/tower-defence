import pygame
from window import Window
from game import Game


def main():
    pygame.init()

    game = Game()

    while True:
        Window.surface.fill((100, 100, 100))
        game.update()
        game.draw()

        
if __name__ == "__main__":
    main()
