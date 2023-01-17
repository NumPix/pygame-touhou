import pygame
from os.path import join as path_join

from assets.scripts.classes.game_logic.Collider import Collider
from assets.scripts.math_and_data.Vector2 import Vector2
from assets.scripts.math_and_data.enviroment import *
from assets.scripts.math_and_data.functions import clamp


class BulletCleaner:
    def __init__(self, position: Vector2, increase_speed: int = 1000, give_points: bool = False, show_sprite: bool = True):
        self.collider = Collider(
            0,
            position
        )

        self.sprite = pygame.image.load(path_join("assets", "sprites", "effects", "player_death_effect.png")).convert_alpha()

        self.increase_speed = increase_speed
        self.give_points = give_points

        self.kill = False
        self.show_sprite = show_sprite

    def update(self, bullets, scene, delta_time):
        self.collider.radius += self.increase_speed * delta_time

        i = 0
        while i < len(bullets):
            if bullets[i].collider.check_collision(self.collider):
                bullet = bullets.pop(i)
                if self.give_points:
                    point_item = self.spawn_point_item(bullet.position)
                    scene.items.append(point_item)
                del bullet
                i -= 1
            i += 1

        if self.collider.radius ** 2 >= GAME_ZONE[2] ** 2 + GAME_ZONE[3] ** 2:
            self.kill = True

    def get_sprite(self):
        if not self.show_sprite:
            return pygame.Surface((0, 0))
        image = pygame.transform.scale(self.sprite, (self.collider.radius * 2, self.collider.radius * 2))
        image.set_alpha(clamp(255 - self.collider.radius ** 2 / (GAME_ZONE[2] ** 2 + GAME_ZONE[3] ** 2) * 1000, 0, 255))

        return image
    def spawn_point_item(self, position: Vector2):
        from assets.scripts.classes.game_logic.Item import StarItem
        return StarItem(position)
