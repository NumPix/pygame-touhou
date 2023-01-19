from __future__ import annotations
import numpy as np

from assets.scripts.math_and_data.functions import *


class Vector2:
    def __init__(self, x: float = None, y: float = None, coords: np.ndarray = None):
        if x is not None and y is not None:
            self.coords = np.array([x, y])
        elif coords is not None:
            self.coords = coords

    def x(self) -> float:
        return self.coords.item(0)

    def y(self) -> float:
        return self.coords.item(1)

    def __add__(self, other: float | Vector2) -> Vector2:
        if type(other) == Vector2:
            return Vector2(coords=self.coords + other.coords)
        return Vector2(coords=self.coords + other)

    def __sub__(self, other: float | Vector2) -> Vector2:
        if type(other) == Vector2:
            return Vector2(coords=self.coords - other.coords)
        return Vector2(coords=self.coords - other)

    def __mul__(self, other: float | Vector2) -> Vector2:
        if type(other) == Vector2:
            return Vector2(coords=self.coords * other.coords)
        return Vector2(coords=self.coords * other)

    def __truediv__(self, other: float | Vector2) -> Vector2:
        if type(other) == Vector2:
            return Vector2(coords=self.coords / other.coords)
        return Vector2(coords=self.coords / other)

    def __floordiv__(self, other: float | Vector2) -> Vector2:
        if type(other) == Vector2:
            return Vector2(coords=self.coords // other.coords)
        return Vector2(coords=self.coords // other)

    def __mod__(self, other: float | Vector2) -> Vector2:
        if type(other) == Vector2:
            return Vector2(coords=self.coords % other.coords)
        return Vector2(coords=self.coords % other)

    def __repr__(self) -> str:
        return f"Vector2({self.x()}, {self.y()})"

    def dot(self, other) -> float:
        return self.x() * other.x() + self.y() * other.y()

    def length(self) -> float:
        return np.sqrt(np.sum(self.coords * self.coords))

    def sqr_length(self) -> float:
        return sum(self.coords * self.coords)

    def normalize(self) -> Vector2:
        if self.to_tuple() == (0, 0):
            return Vector2.zero()
        return Vector2(coords=self.coords / self.length())

    def angle_between(self, other: Vector2) -> float:
        return np.arccos(self.dot(other) / (self.length() * other.length()))

    def to_tuple(self) -> (float, float):
        return self.x(), self.y()

    def clamp(self, min_vx, max_vx, min_vy=None, max_vy=None) -> Vector2:
        if min_vy is None:
            min_vy = min_vx
        if max_vy is None:
            max_vy = max_vx

        return Vector2(clamp(self.x(), min_vx, max_vx), clamp(self.y(), min_vy, max_vy))

    def rotate(self, angle: float) -> Vector2:
        angle = np.deg2rad(angle)
        rotor = np.array([[np.cos(angle), -np.sin(angle)],
                          [np.sin(angle), np.cos(angle)]])
        return Vector2(coords=np.matmul(self.coords, rotor))

    def tan(self):
        return self.y() / self.x()

    def cot(self):
        return self.x() / self.y()

    @staticmethod
    def random_int(min_x, max_x, min_y, max_y):
        return Vector2(np.random.randint(min_x, max_x), np.random.randint(min_y, max_y))

    @staticmethod
    def one() -> Vector2:
        return Vector2(1, 1)

    @staticmethod
    def zero() -> Vector2:
        return Vector2(0, 0)

    @staticmethod
    def right() -> Vector2:
        return Vector2(1, 0)

    @staticmethod
    def left() -> Vector2:
        return Vector2(-1, 0)

    @staticmethod
    def up() -> Vector2:
        return Vector2(0, -1)

    @staticmethod
    def down() -> Vector2:
        return Vector2(0, 1)
