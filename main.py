import pygame
from window import Window


def main():

    pygame.init()

    game_grid_size = (10, 5)
    
    while True:

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                quit()
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_ESCAPE:
                    quit()
            if event.type == pygame.VIDEORESIZE:
                Window.update_size((event.w, event.h))

        Window.surface.fill((100, 100, 100))

        scale = min(Window.size[0] / game_grid_size[0], Window.size[1] / (game_grid_size[1] + 1))
        
        game_display_size = game_grid_size[0] * scale, game_grid_size[1] * scale
        game_display_position = ((Window.size[0] - game_display_size[0]) / 2, (Window.size[1] - game_display_size[1] - scale) / 2)
        pygame.draw.rect(Window.surface, (255, 255, 255), game_display_position + game_display_size)

        selector_display_size = (game_display_size[0], scale)
        selector_display_position = (game_display_position[0], game_display_position[1] + game_display_size[1])
        pygame.draw.rect(Window.surface, (200, 200, 200), selector_display_position + selector_display_size)

        pygame.display.update()


if __name__ == "__main__":
    main()