import pygame


class SpriteSheet:

    full_image: pygame.Surface
    full_image_size: tuple
    sheet_size: tuple
    sprite_size: tuple
    sprites: list

    def __init__(self, filename, size):
        self.full_image = pygame.image.load(filename)
        full_rect = self.full_image.get_rect()
        self.full_image_size = full_rect.w, full_rect.h

        self.sheet_size = size
        self.sprite_size = int(self.full_image_size[0] / size[0]), int(self.full_image_size[1] / size[1])

        self.create_sprites()

    def create_sprites(self):
        self.sprites = []
        for row in range(self.sheet_size[1]):
            for col in range(self.sheet_size[0]):
                surf = pygame.Surface(self.sprite_size, pygame.SRCALPHA, 32)
                surf.fill((1, 0, 0, 0))
                surf.blit(self.full_image, (0, 0), (col * self.sprite_size[0], row * self.sprite_size[1]) + self.sprite_size)
                self.sprites.append(surf)

    def get_sprite_at(self, position):
        if not self.is_on_grid(position): return None
        return self.sprites[self.get_index(position)]

    def is_on_grid(self, position: tuple) -> bool:
        return 0 <= position[0] < self.sheet_size[0] and 0 <= position[1] < self.sheet_size[1]

    def get_index(self, position: tuple) -> int:
        return position[0] + position[1] * self.sheet_size[0]
