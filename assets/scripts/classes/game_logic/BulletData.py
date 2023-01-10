from assets.scripts.classes.game_logic.Collider import Collider
from assets.scripts.classes.hud_and_rendering.SpriteSheet import SpriteSheet


class BulletData:
    def __init__(self, sprite_sheet: SpriteSheet, collider: Collider, animation_speed: int = 0):
        self.sprite_sheet = sprite_sheet
        self.collider = collider
        self.animation_speed = animation_speed

    def __repr__(self):
        return f"BulletData({self.sprite_sheet}, {self.collider}, {self.animation_speed})"