from assets.scripts.classes.SpriteSheet import SpriteSheet
from assets.scripts.classes.Vector2 import Vector2
from assets.scripts.classes.game_logic.Entity import Entity


class Enemy(Entity):
    def __init__(self, position: Vector2, sprite_sheet: SpriteSheet, hp: int, attack_functions: [callable, ...],
                 bullet_pool):
        super().__init__()
        self.position: Vector2 = position

        self.max_hp = hp
        self.current_hp = self.max_hp

        self.attack_functions = attack_functions

        self.sprite_sheet = sprite_sheet
        self.current_sprite = 0
        self.change_sprite_timer = 10

        self.bullets = bullet_pool

    def move(self, velocity: Vector2):
        self.position += velocity

    def update(self):
        self.change_sprite_timer += 1
        self.next_sprite(8)