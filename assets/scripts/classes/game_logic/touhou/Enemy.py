from assets.scripts.classes.hud_and_rendering.SpriteSheet import SpriteSheet
from assets.scripts.math_and_data.Vector2 import Vector2
from assets.scripts.classes.game_logic.touhou.Entity import Entity


class Enemy(Entity):
    def __init__(self, position: Vector2, sprite_sheet: SpriteSheet, hp: int, attack_functions: [callable, ...],
                 bullet_pool):
        super().__init__()
        self.position: Vector2 = position

        self.max_hp: int = hp
        self.current_hp: int = self.max_hp

        self.attack_functions: [callable, ...] = attack_functions

        self.sprite_sheet = sprite_sheet
        self.current_sprite = 0
        self.change_sprite_timer = 10

        self.bullets: list = bullet_pool

    def move(self, velocity: Vector2) -> None:
        self.position += velocity

    def update(self) -> None:
        self.change_sprite_timer += 1
        self.next_sprite(8)