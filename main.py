import pygame


def main():

    pygame.init()

    screen_size = (500, 500)
    screen = pygame.display.set_mode(screen_size, pygame.RESIZABLE)

    game_grid_size = (10, 5)
    

    while True:

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                quit()
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_ESCAPE:
                    quit()
            if event.type == pygame.VIDEORESIZE:
                screen_size = (event.w, event.h)
                screen = pygame.display.set_mode(screen_size, pygame.RESIZABLE)

        screen.fill((100, 100, 100))

        scale = min(screen_size[0] / game_grid_size[0], screen_size[1] / (game_grid_size[1] + 1))
        
        game_display_size = game_grid_size[0] * scale, game_grid_size[1] * scale
        game_display_position = ((screen_size[0] - game_display_size[0]) / 2, (screen_size[1] - game_display_size[1] - scale) / 2)
        pygame.draw.rect(screen, (255, 255, 255), game_display_position + game_display_size)

        selector_display_size = (game_display_size[0], scale)
        selector_display_position = (game_display_position[0], game_display_position[1] + game_display_size[1])
        pygame.draw.rect(screen, (200, 200, 200), selector_display_position + selector_display_size)

        pygame.display.update()


if __name__ == "__main__":
    main()