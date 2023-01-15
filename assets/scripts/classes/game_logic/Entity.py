import pygame
from typing import Union

from assets.scripts.classes.hud_and_rendering.SpriteSheet import SpriteSheet
from assets.scripts.math_and_data.Vector2 import Vector2


class Entity:
    def __init__(self):
        self.position: Vector2
        self.sprite_sheet: Union[SpriteSheet, list[pygame.sprite.Sprite, ...]]
        self.name: str

        self.current_sprite = 0
        self.change_sprite_timer = 0

        self.sprite = pygame.sprite.Sprite()

    def update(self) -> None:
        pass

    def next_sprite(self, delay: int) -> None:
        if self.change_sprite_timer >= delay:
            self.current_sprite = (self.current_sprite + 1) % len(self.sprite_sheet)
            self.change_sprite_timer = 0

    def get_sprite(self) -> pygame.sprite.Sprite:
        self.sprite.image = self.sprite_sheet[self.current_sprite]

        self.sprite.rect = self.sprite.image.get_rect()
        self.sprite.rect.center = self.position.to_tuple()

        return self.sprite
