from assets.scripts.classes.game_logic.Bullet import Bullet
from assets.scripts.classes.game_logic.BulletData import BulletData
from assets.scripts.math_and_data.Vector2 import Vector2


class AttackFunctions:
    delta_angle = 0

    @staticmethod
    def ring(center: Vector2, number_of_bullets: int, bullet_data: BulletData, speed: float, angular_speed: float = 0, delta_angle: float = 0):
        bullets = [
            Bullet(
                bullet_data,
                center,
                (360 * n / number_of_bullets + delta_angle) % 360,
                speed,
                angular_speed
            )
            for n in range(number_of_bullets)
        ]

        return bullets

    @staticmethod
    def wide_ring(number_of_bullets: int, number_of_rings: int, bullet_data: BulletData, speed: float,
                  start_time: float, delay: float, angular_speed: float = 0, delta_angle: float = 0):
        center = Vector2.zero()

        attacks = [
            (
                AttackFunctions.ring,
                start_time + delay * n,
                [center, number_of_bullets, bullet_data, speed, angular_speed, n * delta_angle]
            )
            for n in range(number_of_rings)
        ]

        return attacks
