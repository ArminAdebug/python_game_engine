from source.components.component import Component
from typing import *
from source.math import Vector3, Quaternion


class Transform(Component):
    type = "transform"

    def __init__(self):
        super().__init__()

        self.position = Vector3.zero()
        self.rotation = Quaternion()
        self.scale = Vector3(1, 1, 1)

    def move(self, by_vector: Vector3):
        if not isinstance(by_vector, Vector3):
            raise TypeError("move expects Vector3")

        new_position = self.position + by_vector

        self.position = new_position

    def rotate(self,
               x: int | float,
               y: int | float,
               z: int | float):

        q = Quaternion.euler(x, y, z)
        self.rotation = self.rotation * q

    def __repr__(self):
        return f"Transform(pos={self.position}, rotation={self.rotation}, scale={self.scale})"
