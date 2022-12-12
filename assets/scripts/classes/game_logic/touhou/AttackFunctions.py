from assets.scripts.classes.game_logic.touhou.Bullet import Bullet
from assets.scripts.classes.game_logic.touhou.BulletData import BulletData
from assets.scripts.math_and_data.Vector2 import Vector2


class AttackFunctions:
    @staticmethod
    def ring(center: Vector2, number_of_bullets: int, bullet_data: BulletData, speed: float):
        bullets = []
        for n in range(number_of_bullets):
            angle: float = 360 * n / number_of_bullets
            bullets.append(Bullet(bullet_data, center, angle, speed))

        return bullets