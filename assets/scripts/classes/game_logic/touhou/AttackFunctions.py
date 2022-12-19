from assets.scripts.classes.game_logic.touhou.Bullet import Bullet
from assets.scripts.classes.game_logic.touhou.BulletData import BulletData
from assets.scripts.math_and_data.Vector2 import Vector2

import asyncio


class AttackFunctions:
    @staticmethod
    def ring(center: Vector2, number_of_bullets: int, bullet_data: BulletData, speed: float):
        bullets = []
        for n in range(number_of_bullets):
            angle: float = 360 * n / number_of_bullets
            bullets.append(Bullet(bullet_data, center, angle, speed))

        return bullets

    @staticmethod
    async def wide_ring(center: Vector2, number_of_bullets: int, number_of_rings: int, delay: float, bullet_data: BulletData, speed: float, delta_speed: float = 0):
        for n in range(number_of_rings):
            yield AttackFunctions.ring(center, number_of_bullets, bullet_data, speed)
            print("!")
            speed += delta_speed
            await asyncio.sleep(delay)
        return



