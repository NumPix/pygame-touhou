import pygame

from assets.scripts.classes.game_logic.Entity import Entity
from assets.scripts.math_and_data.characters_data import *
from assets.scripts.math_and_data.Vector2 import Vector2

from assets.scripts.math_and_data.functions import *
from dotenv import load_dotenv
import os

load_dotenv(".env")
GAME_ZONE = tuple(map(int, os.getenv("GAME_ZONE").split(', ')))


class Player(Entity):
    def __init__(self, id: int):
        super().__init__()
        self.name: str = characters[id]['name']
        self.sprite_sheet: pygame.sprite = characters[id]['sprite-sheet']
        self.attack_function: callable = characters[id]['attack-function']

        self.position = Vector2((GAME_ZONE[2] + GAME_ZONE[0] + self.sprite_sheet.x) // 2, 700)
        self.speed = characters[id]['speed']

        self.sprite_size = Vector2(self.sprite_sheet.x, self.sprite_sheet.y)

        self.change_sprite_timer = 0
        self.slow = False

        self.attack_timer = 0
        self.power = 0
        self.bullets = []

    def update(self):
        self.power = clamp(self.power + 1 / 6000, 0, 4)
        self.attack_timer += 1
        self.change_sprite_timer += 1
        self.next_sprite(5)

    def move(self, direction_vector: Vector2) -> None:
        sprite = self.get_sprite()
        self.position = (self.position + direction_vector.normalize() * self.speed * (.5 if self.slow else 1))\
            .clamp(GAME_ZONE[0] + sprite.rect.w // 2, (GAME_ZONE[2] + GAME_ZONE[0]) - sprite.rect.w // 2,
                   GAME_ZONE[1] + sprite.rect.h // 2, (GAME_ZONE[3] + GAME_ZONE[1]) - sprite.rect.h // 2)

    def shoot(self) -> None:
        if self.attack_timer >= 3:
            self.bullets += self.attack_function(self.position + Vector2.up() * 10, int(self.power))
            self.attack_timer = 0

