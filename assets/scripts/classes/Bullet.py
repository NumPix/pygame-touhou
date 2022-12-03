import pygame.transform

from assets.scripts.classes.SpriteSheet import SpriteSheet
from assets.scripts.classes.Vector2 import Vector2

class Bullet:
    def __init__(self, sprite_sheet: SpriteSheet, position: Vector2, angle: float, speed: float, angular_speed=0, animation_speed = 0):
        self.sprite_sheet = sprite_sheet

        self.position: Vector2 = position

        self.angle: float = angle
        self.speed: float = speed
        self.angular_speed: float = angular_speed

        self.current_sprite = 0
        self.change_sprite_timer = 0
        self.animation_speed = animation_speed

    def velocity(self):
        return Vector2(self.speed, 0).rotate(-self.angle - 90)

    def move(self):
        self.position += self.velocity()
        self.angle += self.angular_speed

    def next_sprite(self):
        self.change_sprite_timer += 1
        if self.change_sprite_timer == 60 - self.animation_speed:
            self.current_sprite = (self.current_sprite + 1) % self.sprite_sheet.length
            self.change_sprite_timer = 0

    def get_sprite(self):
        sprite = self.sprite_sheet[self.current_sprite]
        sprite.rect = sprite.image.get_rect()
        sprite.rect.center = self.position.to_tuple()
        sprite.image = pygame.transform.rotate(sprite.image, self.angle).convert_alpha()

        return sprite