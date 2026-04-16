import math


class Quaternion:
    def __init__(self, x: int = 0, y: int = 0, z: int = 0, w: int = 1):
        """making new Quaternion

        Args:
            x (int, optional): _description_. Defaults to 0.
            y (int, optional): _description_. Defaults to 0.
            z (int, optional): _description_. Defaults to 0.
            w (int, optional): _description_. Defaults to 1.
        """
        self.x = x
        self.y = y
        self.z = z
        self.w = w

    def __repr__(self):
        """
        used for logging and debuging.
        """
        return f"Quaternion({self.x}, {self.y}, {self.z}, {self.w})"

    def __mul__(self, other : "Quaternion") -> "Quaternion":
        if not isinstance(other, Quaternion):
            raise TypeError(
                f"unsupported operand type(s) for *: 'Quaternion' and '{type(other).__name__}'"
            )

        x = self.w*other.x + self.x*other.w + self.y*other.z - self.z*other.y
        y = self.w*other.y - self.x*other.z + self.y*other.w + self.z*other.x
        z = self.w*other.z + self.x*other.y - self.y*other.x + self.z*other.w
        w = self.w*other.w - self.x*other.x - self.y*other.y - self.z*other.z

        return Quaternion(x, y, z, w)

    @staticmethod
    def euler(x : int, y : int, z: int) -> "Quaternion":
        """returns a Quaternion from Euler Anglse

        Args:
            x (int): x rotation
            y (int): y rotation
            z (int): z rotation

        Returns:
            Quaternion: Quaternion from Euler Angles
        """

        # convert degrees to radians
        x = math.radians(x)
        y = math.radians(y)
        z = math.radians(z)

        cx = math.cos(x/2)
        sx = math.sin(x/2)
        cy = math.cos(y/2)
        sy = math.sin(y/2)
        cz = math.cos(z/2)
        sz = math.sin(z/2)

        qw = cx * cy * cz + sx * sy * sz
        qx = sx * cy * cz - cx * sy * sz
        qy = cx * sy * cz + sx * cy * sz
        qz = cx * cy * sz - sx * sy * cz

        return Quaternion(qx, qy, qz, qw)
