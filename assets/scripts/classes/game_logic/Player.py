import pygame.transform

from assets.scripts.classes.game_logic.BulletCleaner import BulletCleaner
from assets.scripts.classes.game_logic.Entity import Entity
from assets.scripts.math_and_data.characters_data import *
from assets.scripts.math_and_data.Vector2 import Vector2

from assets.scripts.math_and_data.functions import *
from assets.scripts.math_and_data.enviroment import *


class Player(Entity):
    def __init__(self, id: int, scene, hp: int):
        super().__init__()
        self.name: str = characters[id]['name']
        self.sprite_sheet: pygame.sprite = characters[id]['sprite-sheet']
        self.attack_function: callable = characters[id]['attack-function']

        self.position: Vector2 = Vector2((GAME_ZONE[2] + GAME_ZONE[0] + self.sprite_sheet.x) // 2, GAME_ZONE[1] + GAME_ZONE[3] - 100)
        self.speed: int = characters[id]['speed']

        self.collider = Collider(3)

        self.hitbox_sprite = pygame.image.load(path_join("assets", "sprites", "effects", "player_hitbox.png")).convert_alpha()
        self.hitbox_sprites = [pygame.transform.rotate(self.hitbox_sprite, n) for n in range(360)]
        self.change_hitbox_sprite_timer = 0

        self.default_sprites = [self.sprite_sheet[i] for i in range(len(self.sprite_sheet))]
        self.right_slope_sprites = [pygame.transform.rotate(self.sprite_sheet[i], 7) for i in range(len(self.sprite_sheet))]
        self.left_slope_sprites = [pygame.transform.flip(sprite, flip_x=True, flip_y=False) for sprite in self.right_slope_sprites]

        self.points = 0
        self.hp = hp
        self.reviving = False
        self.invincibility_timer = 0

        self.sprite_size = Vector2(self.sprite_sheet.x, self.sprite_sheet.y)

        self.change_sprite_timer = 0
        self.slow: bool = False

        self.attack_timer = 0
        self.power = 4

        self.bullets = []

        self.slowRate = Vector2.zero()

        self.scene = scene

    def update(self) -> None:
        delta_time = self.scene.delta_time

        if self.slow:
            self.slowRate += Vector2.one() * delta_time
        else:
            self.slowRate += Vector2.right() * delta_time

        if not self.reviving:
            for bullet in self.scene.enemy_bullets:
                if bullet.collider.check_collision(self.collider):
                    self.get_damage()
                    break

            for enemy in self.scene.enemies:
                if enemy.collider.check_collision(self.collider):
                    self.get_damage()
                    break

        for item in self.scene.items:
            if item.collider.check_collision(self.collider):
                item.on_collect(self)
                music_module.sounds[8](.1)
                self.scene.items.remove(item)
                del item

        self.attack_timer += 2.5 * 60 * delta_time
        self.change_sprite_timer += 1 * 60 * delta_time
        self.change_hitbox_sprite_timer += 1 * 60 * delta_time
        self.next_sprite(5)

    def move(self, direction_vector: Vector2) -> None:
        sprite_rect = self.get_sprite().rect

        self.sprite_sheet = self.default_sprites \
            if direction_vector.x() == 0\
            else self.right_slope_sprites if direction_vector.x() < 0\
            else self.left_slope_sprites

        delta_time = self.scene.delta_time

        if self.reviving:
            self.invincibility_timer += 1 * 60 * delta_time
            self.position += Vector2.up() * 2 * 60 * delta_time

            # If no HP left
            if self.hp < 0 and self.position.y() <= GAME_ZONE[3] + GAME_ZONE[1] + 40:
                self.switch_to_scoreboard()

            if self.position.y() <= GAME_ZONE[3] + GAME_ZONE[1] - 100:
                self.reviving = False
                self.invincibility_timer = 0
        else:
            self.position = (self.position + direction_vector.normalize() * self.speed * delta_time * (.5 if self.slow else 1)) \
                .clamp(GAME_ZONE[0] + sprite_rect.w // 2, (GAME_ZONE[2] + GAME_ZONE[0]) - sprite_rect.w // 2,
                       GAME_ZONE[1] + sprite_rect.h // 2, (GAME_ZONE[3] + GAME_ZONE[1]) - sprite_rect.h // 2)

        self.collider.position = self.position

    def shoot(self) -> None:
        if self.attack_timer >= 16:
            music_module.sounds[17](.1)
            self.bullets += self.attack_function(self.position + Vector2.up() * 10, int(self.power))
            self.attack_timer = 0

    def get_damage(self):
        music_module.sounds[16](.2)
        self.scene.bullet_cleaner = BulletCleaner(self.position)
        self.hp -= 1
        self.reviving = True
        self.position = Vector2(50 + (GAME_ZONE[2] - GAME_ZONE[0]) // 2, HEIGHT + 80)

    def add_power(self, power: float):
        self.power += power
        if power > 4:
            self.power = 4

    def switch_to_scoreboard(self):
        from assets.scripts.scenes.ScoreboardScene import ScoreboardScene
        self.scene.switch_to_scene(ScoreboardScene(self))

    def get_hitbox_sprite(self):
        return self.hitbox_sprites[clamp(int(self.change_hitbox_sprite_timer % 360), 0, len(self.hitbox_sprites) - 1)]