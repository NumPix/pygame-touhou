from assets.scripts.classes.game_logic.touhou.BulletData import BulletData
from assets.scripts.classes.game_logic.touhou.Collider import Collider
from assets.scripts.classes.hud_and_rendering.SpriteSheet import SpriteSheet
from assets.scripts.classes.game_logic.touhou.PlayerBullet import PlayerBullet
from assets.scripts.classes.game_logic.touhou.Bullet import Vector2


def marisa_base_attack(fire_point: Vector2, power: int):
    bullets = []

    power_levels = [0, 1, 2, 3]
    delta_angle = 10

    current_power = power_levels[int((len(power_levels) - 1) * power * 20 / 100)]

    bullet_data = BulletData(characters[0]["bullet-sprite-sheet"], Collider(5, offset=Vector2.up() * 40))

    for i in range(-current_power, current_power + 1):
        i /= 2
        bullet = PlayerBullet(bullet_data ,fire_point, delta_angle * i, 30, damage=1)
        bullets.append(bullet)

    return bullets


characters = {
    0: {
        "name": "Marisa",
        "speed": 7,
        "sprite-sheet": SpriteSheet("assets/sprites/touhou/entities/marisa_forward.png").crop((25, 50)),
        "bullet-sprite-sheet": SpriteSheet("assets/sprites/touhou/bullets/marisa_bullet.png").crop((32, 32)),
        "attack-function": marisa_base_attack
    },
    1: {
        "name": "Reimu",
        "speed": 5,
        "sprite-sheet": None,
        "bullet-sprite-sheet": None,
        "attack-function": None
    },
    2: {
        "name": "Remilia",
        "speed": 6,
        "sprite-sheet": None,
        "bullet-sprite-sheet": None,
        "attack-function": None
    },
    3: {
        "name": "Koishi",
        "speed": 6,
        "sprite-sheet": None,
        "bullet-sprite-sheet": None,
        "attack-function": None
    }
}
