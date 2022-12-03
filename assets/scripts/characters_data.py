from assets.scripts.classes.SpriteSheet import SpriteSheet
from assets.scripts.classes.Bullet import Bullet
from assets.scripts.classes.Bullet import Vector2


def marisa_base_attack(fire_point: Vector2, power: int):
    bullets = []

    power_levels = [2, 3, 4, 6, 8]
    delta_angle = 10

    current_power = power_levels[int((len(power_levels) - 1) * power / 100)]

    for i in range(-current_power, current_power):
        i /= 2
        bullet = Bullet(characters[0]["bullet-sprite-sheet"], fire_point, delta_angle * i, 20)
        bullets.append(bullet)

    return bullets

characters = {
    0: {
        "name": "Marisa",
        "speed": 7,
        "sprite-sheet": SpriteSheet("assets/sprites/marisa_forward.png").crop((50, 100)),
        "bullet-sprite-sheet": SpriteSheet("assets/sprites/marisa_bullet.png").crop((32, 32)),
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



