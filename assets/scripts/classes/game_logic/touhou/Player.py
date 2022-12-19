import pygame

from assets.scripts.classes.game_logic.touhou.Entity import Entity
from assets.scripts.math_and_data.touhou.characters_data import *
from assets.scripts.math_and_data.Vector2 import Vector2

from assets.scripts.math_and_data.functions import *
from assets.scripts.math_and_data.enviroment import *
from assets.scripts.scenes.touhou.TitleScene import TitleScene


class Player(Entity):
    def __init__(self, id: int, scene):
        super().__init__()
        self.name: str = characters[id]['name']
        self.sprite_sheet: pygame.sprite = characters[id]['sprite-sheet']
        self.attack_function: callable = characters[id]['attack-function']

        self.position: Vector2 = Vector2((GAME_ZONE[2] + GAME_ZONE[0] + self.sprite_sheet.x) // 2, GAME_ZONE[1] + GAME_ZONE[3] - 100)
        self.speed: int = characters[id]['speed']

        self.collider = Collider(5)

        self.points = 0
        self.hp = 2
        self.reviving = False
        self.invincibility_timer = 0

        self.sprite_size = Vector2(self.sprite_sheet.x, self.sprite_sheet.y)

        self.change_sprite_timer = 0
        self.slow: bool = False

        self.attack_timer = 0
        self.power = 0
        self.bullets = []

        self.scene = scene

    def update(self) -> None:
        delta_time = self.scene.delta_time

        if not self.reviving:
            for bullet in self.scene.enemy_bullets:
                if bullet.collider.check_collision(self.collider):
                    self.get_damage()
                    break

            for enemy in self.scene.enemies:
                if enemy.collider.check_collision(self.collider):
                    self.get_damage()
                    break

        self.attack_timer += 2.5 * 60 * delta_time
        self.change_sprite_timer += 1 * 60 * delta_time
        self.next_sprite(5)

    def move(self, direction_vector: Vector2) -> None:
        sprite_rect = self.get_sprite().rect

        delta_time = self.scene.delta_time

        if self.reviving:
            self.invincibility_timer += 1 * 60 * delta_time
            self.position += Vector2.up() * 2 * 60 * delta_time
            if self.position.y() <= GAME_ZONE[3] + GAME_ZONE[1] - 100:
                self.reviving = False
                self.invincibility_timer = 0
        else:
            self.position = (self.position + direction_vector.normalize() * self.speed * delta_time * (.5 if self.slow else 1)) \
                .clamp(GAME_ZONE[0] + sprite_rect.w // 2, (GAME_ZONE[2] + GAME_ZONE[0]) - sprite_rect.w // 2,
                       GAME_ZONE[1] + sprite_rect.h // 2, (GAME_ZONE[3] + GAME_ZONE[1]) - sprite_rect.h // 2)

        self.collider.position = self.position

    def shoot(self) -> None:
        if self.attack_timer >= 3:
            self.bullets += self.attack_function(self.position + Vector2.up() * 10, int(self.power))
            self.attack_timer = 0

    def get_damage(self):
        self.hp -= 1
        self.reviving = True
        self.position = Vector2((GAME_ZONE[2] + GAME_ZONE[0]) // 2, HEIGHT + 80)
        if self.hp < 0:
            self.scene.switch_to_scene(TitleScene())