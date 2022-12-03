from assets.scripts.classes.Bullet import Bullet


class PlayerBullet(Bullet):
    def __init__(self, *args, damage):
        super().__init__(*args)
        self.damage = damage
