import pygame

from engine.mouse import Mouse, MouseButton
from engine.window import Window
from engine.event_handler import EventHandler
from engine.clock import Clock
from engine.camera import Camera

from engine.vector2 import Vector2
from engine.rect import Rect

from game import Game


def main():
    pygame.init()
    game = Game()

    while True:
        EventHandler.update()
        Mouse.update()
        Clock.update()

        # cam zoom controls
        for event in EventHandler.get_events(pygame.MOUSEWHEEL):
            zoom_speed = 1.1
            if event.y < 0:
                Camera.size *= zoom_speed 
            else:
                Camera.size /= zoom_speed 

        dp = Mouse.get_position_change()
        if Mouse.get_pressed(MouseButton.MIDDLE):
            speed_scale = 1 / Camera.get_pixels_per_unit()
            Camera.position.x -= dp.x * speed_scale
            Camera.position.y += dp.y * speed_scale

        Window.surface.fill((100, 100, 100))

        game.draw()
        game.update()

        pygame.display.update()

        
if __name__ == "__main__":
    main()
