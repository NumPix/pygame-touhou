from __future__ import annotations
import numpy as np


class Vector2:
    def __init__(self, x: float = None, y: float = None, coords: np.ndarray = None):
        if x is not None and y is not None:
            self.coords = np.array([x, y])
        elif coords is not None:
            self.coords = coords

    def x(self):
        return self.coords[0]

    def y(self):
        return self.coords[1]

    def __add__(self, other: float | Vector2):
        if type(other) == Vector2:
            return Vector2(coords=self.coords + other.coords)
        return Vector2(coords=self.coords + other)

    def __sub__(self, other: float | Vector2):
        if type(other) == Vector2:
            return Vector2(coords=self.coords - other.coords)
        return Vector2(coords=self.coords - other)

    def __mul__(self, other: float | Vector2):
        if type(other) == Vector2:
            return Vector2(coords=self.coords * other.coords)
        return Vector2(coords=self.coords * other)

    def __truediv__(self, other: float | Vector2):
        if type(other) == Vector2:
            return Vector2(coords=self.coords / other.coords)
        return Vector2(coords=self.coords / other)

    def __repr__(self):
        return f"Vector2({self.x()}, {self.y()})"

    def dot(self, other) -> float:
        return self.x() * other.x() + self.y() * other.y()

    def length(self) -> float:
        return np.sqrt(np.sum(self.coords * self.coords))

    def sqr_length(self) -> float:
        return self.coords * self.coords

    def normalize(self) -> Vector2:
        return Vector2(coords=self.coords / self.length())

    def angle_between(self, other: Vector2) -> float:
        return np.arccos(self.dot(other) / (self.length() * other.length()))

    def to_tuple(self) -> (float, float):
        return self.x(), self.y()

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
        return Vector2(0, 1)

    @staticmethod
    def down() -> Vector2:
        return Vector2(0, -1)
