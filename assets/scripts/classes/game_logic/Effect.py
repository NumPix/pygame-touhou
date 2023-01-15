import pygame

from assets.scripts.math_and_data.Vector2 import Vector2


class Effect:
    def __init__(self, position: Vector2, sprite_sheet: [pygame.Surface, ...], delay: float):
        self.position: Vector2 = position

        self.sprite_sheet = sprite_sheet
        self.current_sprite = 0
        self.sprite_timer = 0

        self.delay = delay

    def update(self, delta_time) -> bool:
        self.sprite_timer += delta_time * 60 * 2
        if self.sprite_timer >= self.delay:
            self.current_sprite += 1

            self.sprite_timer = 0

            if self.current_sprite >= len(self.sprite_sheet):
                return False

        return True

    def get_sprite(self) -> pygame.sprite.Sprite:
        sprite = pygame.sprite.Sprite()

        sprite.image = self.sprite_sheet[self.current_sprite]
        sprite.rect = sprite.image.get_rect()
        sprite.rect.center = self.position.to_tuple()

        return sprite
