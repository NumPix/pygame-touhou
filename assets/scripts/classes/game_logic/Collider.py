from __future__ import annotations

from assets.scripts.math_and_data.Vector2 import Vector2


class Collider:
    def __init__(self, radius: float, position: Vector2 = Vector2.zero(), offset: Vector2 = Vector2.zero()):
        self.radius = radius
        self.position = position
        self.offset = offset

    def check_collision(self, target: Collider) -> bool:
        return ((target.position - self.position) * (target.position - self.position)).length() < (self.radius + target.radius) ** 2

    def __repr__(self):
        return f"Collider({self.radius}, {self.position}, {self.offset})"
