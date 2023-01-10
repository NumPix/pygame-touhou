from copy import copy

import pygame.transform

from assets.scripts.classes.game_logic.BulletData import BulletData
from assets.scripts.math_and_data.Vector2 import Vector2
from assets.scripts.math_and_data.enviroment import *


class Bullet:
    def __init__(self, bullet_data: BulletData,  position: Vector2, angle: float, speed: float, angular_speed=0):

        self.sprite_sheet = bullet_data.sprite_sheet

        sprite_sheet = []
        for i in range(len(self.sprite_sheet)):
            sprite = self.sprite_sheet[i]
            new_sprite = pygame.sprite.Sprite()
            new_sprite.image = pygame.transform.rotate(sprite, angle)
            new_sprite.rect = new_sprite.image.get_rect()
            sprite_sheet.append(new_sprite)

        self.sprite_sheet = sprite_sheet

        self.position: Vector2 = position
        self.collider = copy(bullet_data.collider)

        self.angle: float = angle
        self.speed: float = speed
        self.angular_speed: float = angular_speed

        self.current_sprite = 0
        self.change_sprite_timer = 0
        self.animation_speed = bullet_data.animation_speed

    def velocity(self) -> Vector2:
        return (Vector2.up() * self.speed).rotate(self.angle)

    def move(self, delta_time) -> bool:
        self.position += self.velocity() * delta_time

        self.collider.position = self.position + self.collider.offset.rotate(self.angle)

        self.angle += self.angular_speed * delta_time
        sprite = self.get_sprite()
        if (self.position.x() - sprite.rect.w // 2 < GAME_ZONE[0] - 50 or
            self.position.y() - sprite.rect.h // 2 < GAME_ZONE[1] - 50) or \
                (self.position.x() + sprite.rect.w // 2 > GAME_ZONE[0] + GAME_ZONE[2] + 50 or
                 self.position.y() + sprite.rect.h // 2 > GAME_ZONE[1] + GAME_ZONE[3] + 50):
            del self
            return False
        return True

    def next_sprite(self) -> None:
        self.change_sprite_timer += 1
        if self.change_sprite_timer == FPS - self.animation_speed:
            self.current_sprite = (self.current_sprite + 1) % self.sprite_sheet.length
            self.change_sprite_timer = 0

    def get_sprite(self) -> pygame.sprite.Sprite:
        sprite = self.sprite_sheet[self.current_sprite]
        sprite.rect = sprite.image.get_rect()
        sprite.rect.center = self.position.to_tuple()

        return sprite
