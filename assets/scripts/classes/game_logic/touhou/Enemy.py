import numpy as np

from assets.scripts.classes.hud_and_rendering.SpriteSheet import SpriteSheet
from assets.scripts.math_and_data.Vector2 import Vector2
from assets.scripts.classes.game_logic.touhou.Entity import Entity
from assets.scripts.math_and_data.enviroment import FPS
from assets.scripts.math_and_data.touhou.Splines import BasisSpline

BSpline = BasisSpline()


class Enemy(Entity):
    def __init__(self, position: Vector2, trajectory: [np.ndarray, ...], sprite_sheet: SpriteSheet, hp: int,
                 attack_functions: [callable, ...],
                 bullet_pool):
        super().__init__()
        self.start_position: Vector2 = position
        self.position: Vector2 = position
        self.trajectory = trajectory
        self.t = 0

        self.max_hp: int = hp
        self.current_hp: int = self.max_hp

        self.attack_functions: [callable, ...] = attack_functions

        self.sprite_sheet = sprite_sheet
        self.current_sprite = 0
        self.change_sprite_timer = 10

        self.bullets: list = bullet_pool

        self.speed = .5

    def move(self) -> None:
        self.position = self.start_position + Vector2(coords=BSpline.curve(self.trajectory, self.t))
        self.t += self.speed / FPS
        if self.t > len(self.trajectory) - 1:
            self.t = 0

    def update(self) -> None:
        self.change_sprite_timer += 1
        self.next_sprite(4)
