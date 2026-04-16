"""standard Vector3 class"""
import math

from source.logging import Logger


class Vector3:
    """standard Vector3 class"""

    def __init__(self, x: float, y: float, z: float):
        """setup values

        Args:
            x (float): x axis value
            y (float): y axis value
            z (float): z axis value
        """
        self.x = x
        self.y = y
        self.z = z

    def __repr__(self) -> str:
        return f"Vector3({self.x}, {self.y}, {self.z})"

    def __add__(self, other: "Vector3") -> "Vector3":
        """add two vector3

        Args:
            other (Vector3): other vector to add

        Raises:
            TypeError: if other is nor Vector3

        Returns:
            Vector3: output Vector3
        """
        if not isinstance(other, Vector3):
            raise TypeError(
                f"unsupported operand type(s) for +: 'Vector3' and '{type(other).__name__}'"
            )
        return Vector3(
            self.x + other.x,
            self.y + other.y,
            self.z + other.z
        )

    def __sub__(self, other: "Vector3") -> "Vector3":
        """sub self Vector by other Vector

        Args:
            other (Vector3): other vector for sub

        Raises:
            TypeError: if other is not Vector3

        Returns:
            Vector3: output Vector3
        """
        if not isinstance(other, Vector3):
            raise TypeError(
                f"unsupported operand type(s) for -: 'Vector3' and '{type(other).__name__}'"
            )
        return Vector3(
            self.x - other.x,
            self.y - other.y,
            self.z - other.z
        )

    def __mul__(self, value: int | float) -> "Vector3":
        """multiply by number

        Args:
            value (int | float): multiply vector by that

        Raises:
            TypeError: if value is not int | float

        Returns:
            Vector3: multiply output
        """

        if not isinstance(value, (int, float)):
            raise TypeError(
                f"unsupported operand type(s) for *: 'Vector3' and '{type(value).__name__}'")

        return Vector3(
            self.x * value,
            self.y * value,
            self.z * value
        )

    def length(self) -> int:
        """returns vector3 line length

        Returns:
            int: return length
        """
        return math.sqrt(self.x**2 + self.y**2 + self.z**2)

    def normalized(self) -> "Vector3":
        """returns normalized Vector3

        Raises:
            ValueError: if Vector3 was zero it returns ValueError

        Returns:
            Vector3: normalized Vector3
        """
        l = self.length()
        if l == 0:
            raise ValueError("Cannot normalize a zero vector")
        return Vector3(
            self.x / l,
            self.y / l,
            self.z / l
        )

    def dot(self, other: "Vector3") -> int:
        """
        Args:
            other (Vector3): other Vector

        Raises:
            TypeError: if other is not Vector3

        Returns:
            int: _description_
        """
        if not isinstance(other, Vector3):
            raise TypeError("dot product requires another Vector3")
        return self.x * other.x + self.y * other.y + self.z * other.z

    @staticmethod
    def zero() -> "Vector3":
        """
        returns a Vector3 with zero vallues
        """
        return Vector3(0, 0, 0)


# test Vector3
if __name__ == "__main__":
    a = Vector3(1, 2, 3)
    b = Vector3(4, 5, 6)

    Logger.log_info(a + b)
    Logger.log_info(a - b)
    Logger.log_info(a * 3)
    Logger.log_info(a.length())
    Logger.log_info(a.dot(b))
