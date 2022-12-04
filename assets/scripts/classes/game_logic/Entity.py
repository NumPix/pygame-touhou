import pygame


class Entity:
    def __init__(self):
        self.name: str
        self.sprite_sheet: pygame.sprite

        self.current_sprite = 0
        self.change_sprite_timer = 0

    def update(self):
        pass

    def next_sprite(self, delay: int) -> None:
        if self.change_sprite_timer >= delay:
            self.current_sprite = (self.current_sprite + 1) % self.sprite_sheet.length
            self.change_sprite_timer = 0

    def get_sprite(self) -> pygame.sprite.Sprite:
        sprite = self.sprite_sheet[self.current_sprite]
        sprite.rect = sprite.image.get_rect()
        sprite.rect.center = self.position.to_tuple()

        return sprite
