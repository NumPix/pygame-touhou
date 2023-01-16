import random

import numpy as np

from assets.scripts.classes.game_logic.Bullet import Bullet
from assets.scripts.classes.game_logic.BulletData import BulletData
from assets.scripts.classes.game_logic.Enemy import Enemy
from assets.scripts.classes.game_logic.Player import Player
from assets.scripts.math_and_data.Vector2 import Vector2


class AttackFunctions:
    delta_angle = 0

    @staticmethod
    def ring(center: Vector2, number_of_bullets: int, bullet_data: BulletData, speed: float, angular_speed: float = 0,
             delta_angle: float = 0):
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
    def random(center: Vector2, number_of_bullets: int, bullet_data: BulletData, speed: float,
               angular_speed: float = 0):
        bullets = [
            Bullet(
                bullet_data,
                center,
                random.randint(0, 360),
                speed,
                angular_speed
            )
            for _ in range(number_of_bullets)
        ]

        return bullets

    @staticmethod
    def cone(center: Vector2, angle, number_of_bullets: int, bullet_data: BulletData, speed: float, delta_angle: int, angular_speed=0, player: Player=None, enemy: Enemy=None):
        bullets = [
            Bullet(
                bullet_data,
                center,
                (angle if angle != "player" else np.rad2deg(Vector2.angle_between(enemy.position - player.position, Vector2.right())) + 90) + i * delta_angle * 0.5,
                speed,
                angular_speed
            )

            for i in range(-number_of_bullets + 1, number_of_bullets, 2)
        ]

        return bullets

    @staticmethod
    def wide_cone(number_of_bullets: int, number_of_cones: int, bullet_data: BulletData, angle: int, speed: float, delta_angle: int,
                  start_time: float, delay: float, angular_speed=0, player: Player=None, enemy: Enemy=None):
        center = Vector2.zero()

        attacks = [
            (
                AttackFunctions.cone,
                round(start_time + delay * n, 3),
                [center, angle, number_of_bullets, bullet_data, speed, delta_angle, angular_speed, player, enemy]
            )
            for n in range(number_of_cones)
        ]

        return attacks

    @staticmethod
    def wide_ring(number_of_bullets: int, number_of_rings: int, bullet_data: BulletData, speed: float,
                  start_time: float, delay: float, angular_speed: float = 0, delta_angle: float = 0, rand_center=False):

        attacks = [
            (
                AttackFunctions.ring,
                round(start_time + delay * n, 3),
                [Vector2.zero() if not rand_center else\
            Vector2.one().rotate(random.randint(0, 360)) * 25, number_of_bullets, bullet_data, speed, angular_speed, n * delta_angle]
            )
            for n in range(number_of_rings)
        ]

        return attacks

    @staticmethod
    def long_random(number_of_bullets: int, number_of_randoms: int, bullet_data: BulletData, speed: float,
                    start_time: float, delay: float, angular_speed: float = 0, rand_center=False):
        attacks = [
            (
                AttackFunctions.random,
                round(start_time + delay * n, 3),
                [Vector2 if not rand_center else\
            Vector2.one().rotate(random.randint(0, 360)) * 25, number_of_bullets, bullet_data, speed, angular_speed]
            )
            for n in range(number_of_randoms)
        ]

        return attacks


