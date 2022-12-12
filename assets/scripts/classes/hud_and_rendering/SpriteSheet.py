from __future__ import annotations
import pygame


class SpriteSheet:
    def __init__(self, filename):
        self.sheet = pygame.image.load(filename).convert_alpha()
        self.sprite_size: (int, int) = (0, 0)
        self.x: int = 0
        self.y: int = 0
        self.length = 0

    def crop(self, box_size: (int, int)) -> SpriteSheet:
        self.sprite_size = box_size
        self.x = self.sheet.get_size()[0] // self.sprite_size[0]
        self.y = self.sheet.get_size()[1] // self.sprite_size[1]
        self.length = self.x * self.y

        return self

    def __getitem__(self, index) -> pygame.sprite.Sprite:
        ind_y = index // self.x
        ind_x = index % self.x

        image = pygame.Surface(self.sprite_size, pygame.SRCALPHA).convert_alpha()
        new_sprite = pygame.sprite.Sprite()
        rect = pygame.Rect(ind_x * self.sprite_size[0], ind_y * self.sprite_size[1], self.sprite_size[0], self.sprite_size[1])
        image.blit(self.sheet, (0, 0), rect)

        new_sprite.image = image

        return new_sprite

    def __len__(self):
        return self.length
