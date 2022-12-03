import pygame
from assets.scripts.characters_data import *
from assets.scripts.classes.Vector2 import Vector2


class Player:
    def __init__(self, id: int):
        self.name: str = characters[id]['name']
        self.sprite_sheet: pygame.sprite = characters[id]['sprite-sheet']
        self.attack_function: callable = characters[id]['attack-function']

        self.position = Vector2(100, 100)
        self.speed = characters[id]['speed']

        self.sprite_size = Vector2(self.sprite_sheet.x, self.sprite_sheet.y)
        self.current_sprite = 0

        self.change_sprite_timer = 0

        self.attack_timer = 0
        self.power = 0
        self.bullets = []

        self.slow: bool = True

    def update(self):
        self.power += 1 / 60
        self.attack_timer += 1
        self.change_sprite_timer += 1
        self.next_sprite()

    def move(self, direction_vector: Vector2) -> None:
        self.position += direction_vector.normalize() * self.speed * (.5 if self.slow else 1)

    def next_sprite(self) -> None:
        if self.change_sprite_timer >= 8:
            self.current_sprite = (self.current_sprite + 1) % self.sprite_sheet.length
            self.change_sprite_timer = 0

    def get_sprite(self) -> pygame.sprite.Sprite:
        sprite = self.sprite_sheet[self.current_sprite]
        sprite.rect = sprite.image.get_rect()
        sprite.rect.center = self.position.to_tuple()

        return sprite

    def attack(self) -> None:
        if self.attack_timer >= 5:
            self.bullets += self.attack_function(self.position + Vector2.up() * 5, int(self.power))
            self.attack_timer = 0

