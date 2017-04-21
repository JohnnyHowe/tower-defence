import menu
import game

window_size = (600, 400)

# Delete this to make game start at menu
import pygame
s = pygame.Surface(window_size)
game.run(1, 1, window_size, s)
# End of delete portion

menu.run(window_size)
