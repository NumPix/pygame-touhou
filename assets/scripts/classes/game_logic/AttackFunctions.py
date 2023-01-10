from assets.scripts.classes.game_logic.Bullet import Bullet
from assets.scripts.classes.game_logic.BulletData import BulletData
from assets.scripts.math_and_data.Vector2 import Vector2


class AttackFunctions:
    delta_angle = 0

    @staticmethod
    def ring(center: Vector2, number_of_bullets: int, bullet_data: BulletData, speed: float, delta_angle: float = 0):
        bullets = []
        for n in range(number_of_bullets):
            angle: float = (360 * n / number_of_bullets + delta_angle) % 360
            bullets.append(Bullet(bullet_data, center, angle, speed))

        return bullets

    @staticmethod
    def wide_ring(center: Vector2, number_of_bullets: int, number_of_rings: int, bullet_data: BulletData, speed: float,
                  start_time: float, delay: float, delta_angle: float = 0):
        attacks = []
        for n in range(number_of_rings):
            attacks.append(
                (
                    lambda: AttackFunctions.ring(center, number_of_bullets, bullet_data, speed, delta_angle * n),
                    start_time + delay * n
                )
            )

        return attacks
