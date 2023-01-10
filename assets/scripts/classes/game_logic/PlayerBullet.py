from assets.scripts.classes.game_logic.Bullet import Bullet


class PlayerBullet(Bullet):
    def __init__(self, *args, damage: int):
        super().__init__(*args)
        self.damage: int = damage
