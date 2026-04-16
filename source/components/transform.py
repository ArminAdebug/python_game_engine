"""
Module of Transform component
"""
from source.components.component import Component
from source.math import Vector3, Quaternion


class Transform(Component):
    """
    Transform Component for Object 3d position, rotation, scale
    """
    type = "transform"

    def __init__(self):
        """setup values
        """
        super().__init__()

        self.position = Vector3.zero()
        self.rotation = Quaternion()
        self.scale = Vector3(1, 1, 1)

    def move(self, by_vector: Vector3):
        """
        Gets one Vector3 and move current position by that
        """
        if not isinstance(by_vector, Vector3):
            raise TypeError("move expects Vector3")

        new_position = self.position + by_vector

        self.position = new_position

    def rotate(self,
               x: int | float,
               y: int | float,
               z: int | float):
        """
        Gets 3axis Euler Angles and rotate current rotation by that
        """

        q = Quaternion.euler(x, y, z)
        self.rotation = self.rotation * q

    def __repr__(self) -> str:
        """
        used for logging and debuging.
        """
        return f"Transform(pos={self.position}, rotation={self.rotation}, scale={self.scale})"
