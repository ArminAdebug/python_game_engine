import math
from source.logging import *


class Vector3:
    def __init__(self, x: float, y: float, z: float):
        self.x = x
        self.y = y
        self.z = z

    def __repr__(self):
        return f"Vector3({self.x}, {self.y}, {self.z})"

    def __add__(self, other):
        if not isinstance(other, Vector3):
            raise TypeError(
                f"unsupported operand type(s) for +: 'Vector3' and '{type(other).__name__}'"
            )
        return Vector3(
            self.x + other.x,
            self.y + other.y,
            self.z + other.z
        )

    def __sub__(self, other):
        if not isinstance(other, Vector3):
            raise TypeError(
                f"unsupported operand type(s) for -: 'Vector3' and '{type(other).__name__}'"
            )
        return Vector3(
            self.x - other.x,
            self.y - other.y,
            self.z - other.z
        )

    def __mul__(self, value):
        if not isinstance(value, (int, float)):
            raise TypeError(
                f"unsupported operand type(s) for *: 'Vector3' and '{type(value).__name__}'")

        return Vector3(
            self.x * value,
            self.y * value,
            self.z * value
        )

    def length(self):
        return math.sqrt(self.x**2 + self.y**2 + self.z**2)

    def normalized(self):
        l = self.length()
        if l == 0:
            raise ValueError("Cannot normalize a zero vector")
        return Vector3(
            self.x / l,
            self.y / l,
            self.z / l
        )

    def dot(self, other):
        if not isinstance(other, Vector3):
            raise TypeError("dot product requires another Vector3")
        return self.x * other.x + self.y * other.y + self.z * other.z

    def zero() -> "Vector3":
        """
        returns a Vector3 with zero vallues
        """
        return Vector3(0, 0, 0)


# test
if __name__ == "__main__":
    a = Vector3(1, 2, 3)
    b = Vector3(4, 5, 6)

    log_info(a + b)       # جمع
    log_info(a - b)       # تفریق
    log_info(a * 3)       # ضرب در عدد
    log_info(a.length())  # طول بردار
    log_info(a.dot(b))
