import numpy as np
import pygame.surface

from os.path import join as path_join

from assets.scripts.classes.game_logic.Collider import Collider
from assets.scripts.classes.hud_and_rendering.SpriteSheet import SpriteSheet
from assets.scripts.math_and_data.Vector2 import Vector2
from assets.scripts.classes.game_logic.Entity import Entity
from assets.scripts.math_and_data.functions import scale_sprite, set_alpha_sprite
from assets.scripts.math_and_data.Splines import BasisSpline

BSpline = BasisSpline()


class Enemy(Entity):
    def __init__(self,
                 position: Vector2,
                 trajectory: [np.ndarray, ...],
                 speed,
                 sprite_sheet: SpriteSheet,
                 collider: Collider,
                 hp: int,
                 attack_data: [(callable, float), ...],
                 bullet_pool,
                 scene):

        super().__init__()
        self.start_position: Vector2 = position
        self.position: Vector2 = position
        self.trajectory = trajectory
        self.t = 0

        self.max_hp: int = hp
        self.current_hp: int = self.max_hp

        self.attack_data: [(callable, float), ...] = attack_data
        self.attack_count = 0

        self.sprite_sheet = sprite_sheet
        self.current_sprite = 0
        self.change_sprite_timer = 10

        self.death_effect_sprite = pygame.sprite.Sprite()
        self.death_effect_sprite.image = pygame.image.load(path_join("assets", "sprites", "effects", "fairy_death_0.png")).convert_alpha()
        self.death_effect_sprite.rect = self.death_effect_sprite.image.get_rect()

        self.bullets: list = bullet_pool

        self.collider: Collider = collider

        self.scene = scene
        self.target = scene.player

        self.alive = True

        self.speed = speed

    def move(self) -> None:
        if not self.alive:
            return

        self.collider.position = self.position + self.collider.offset

        delta_time = self.scene.delta_time

        self.position = self.start_position + Vector2(coords=BSpline.curve(self.trajectory, self.t))
        self.t += self.speed * delta_time
        if self.t > len(self.trajectory) - 1:
            self.death()

    def update(self) -> None:
        self.change_sprite_timer += 1 * 60 * self.scene.delta_time

        if self.attack_data and self.attack_count < len(self.attack_data):
            if self.t >= self.attack_data[self.attack_count][1]:
                bullets = self.attack_data[self.attack_count][0]()
                for bullet in bullets:
                    bullet.position += self.position
                self.bullets.extend(bullets)
                self.attack_count += 1

        if self.alive:
            self.next_sprite(4)
        else:
            if self.change_sprite_timer >= 2:
                self.current_sprite += 1
                if self.current_sprite == len(self.sprite_sheet):
                    self.death()

                self.change_sprite_timer = 0

        for bullet in self.target.bullets:
            if self.collider.check_collision(bullet.collider):
                self.target.points += 100
                self.get_damage(bullet.damage)
                self.target.bullets.remove(bullet)
                del bullet

    def get_damage(self, damage: int) -> None:
        self.current_hp -= damage
        if self.current_hp <= 0 and self.alive:
            self.alive = False
            self.current_sprite = 0
            self.sprite_sheet = [set_alpha_sprite(scale_sprite(self.death_effect_sprite, 1 + n / 2), 255 - n * 51).image for n in range(5)]

    def death(self):
        if self.current_hp <= 0:
            self.target.points += 10000
        self.scene.enemies.remove(self)
        del self