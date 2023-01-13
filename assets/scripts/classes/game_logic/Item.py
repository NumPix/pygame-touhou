import pygame
from os.path import join as path_join

from assets.scripts.classes.game_logic.Collider import Collider
from assets.scripts.classes.game_logic.Player import Player
from assets.scripts.math_and_data.Vector2 import Vector2
from assets.scripts.math_and_data.enviroment import GAME_ZONE, music_module


class Item:
    def __init__(self, position: Vector2, sprite: pygame.Surface, collider: Collider, on_collect: callable, homing: bool = False):
        self.position = position
        self.start_position = position
        self.sprite: pygame.Surface = sprite
        self.collider: Collider = collider
        self.on_collect: callable = on_collect

        self.homing = homing

        self.t = -10

    def move(self, delta_time, player: Player) -> bool:
        if not self.homing:
            self.t += 10 * delta_time
            self.position = Vector2(self.start_position.x(), self.start_position.y() + (self.t ** 2 - 100))
        else:
            self.t += 60 * delta_time
            if self.t > 1.5:
                player_pos = player.position
                direction = player_pos - self.position
                self.position += direction.normalize() * 500 * delta_time

        self.collider.position = self.position
        if self.position.y() > GAME_ZONE[1] + GAME_ZONE[3]:
            del self
            return False
        return True

    def get_sprite(self) -> pygame.sprite.Sprite:
        sprite = pygame.sprite.Sprite()
        sprite.image = self.sprite
        sprite.rect = self.sprite.get_rect()
        sprite.rect.center = self.position.to_tuple()

        return sprite


class PowerItem(Item):
    def __init__(self, position: Vector2, large: bool, homing: bool = False):
        if large:
            sprite = pygame.image.load(path_join("assets", "sprites", "projectiles_and_items", "power_item_large.png"))
            collider = Collider(12)
            on_collect = self.on_collect_large
        else:
            sprite = pygame.image.load(path_join("assets", "sprites", "projectiles_and_items", "power_item_small.png"))
            collider = Collider(10)
            on_collect = self.on_collect_small

        super().__init__(position, sprite, collider, on_collect, homing)

    def on_collect_large(self, player: Player):
        music_module.sounds[20](.1)
        player.add_power(0.02)
        player.points += 10

    def on_collect_small(self, player: Player):
        music_module.sounds[20](.2)
        player.add_power(0.005)
        player.points += 10


class PointItem(Item):
    def __init__(self, position: Vector2, homing: bool = False):
        sprite = pygame.image.load(path_join("assets", "sprites", "projectiles_and_items", "point_item.png"))
        collider = Collider(10)
        on_collect = self.on_collect

        super().__init__(position, sprite, collider, on_collect, homing)

    def on_collect(self, player: Player):
        player.points += 30000 + int(70000 * (GAME_ZONE[3] + GAME_ZONE[1] - self.position.y()) / GAME_ZONE[3])


class FullPowerItem(Item):
    def __init__(self, position: Vector2, homing: bool = False):
        sprite = pygame.image.load(path_join("assets", "sprites", "projectiles_and_items", "full_power_item.png"))
        collider = Collider(12)
        on_collect = self.on_collect

        super().__init__(position, sprite, collider, on_collect, homing)
    def on_collect(self, player: Player):
        player.add_power(4)

class OneUpItem(Item):
    def __init__(self, position: Vector2, homing: bool = False):
        sprite = pygame.image.load(path_join("assets", "sprites", "projectiles_and_items", "1up_item.png"))
        collider = Collider(12)
        on_collect = self.on_collect

        super().__init__(position, sprite, collider, on_collect, homing)
    def on_collect(self, player: Player):
        music_module.sounds[5](.1)
        player.hp += 1


class StarItem(Item):
    def __init__(self, position: Vector2):
        sprite = pygame.image.load(path_join("assets", "sprites", "projectiles_and_items", "star_item.png"))
        collider = Collider(10)
        on_collect = self.on_collect

        super().__init__(position, sprite, collider, on_collect, True)

    def on_collect(self, player: Player):
        player.points += 200
