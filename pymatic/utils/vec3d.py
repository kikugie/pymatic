from pymatic.utils.base_vector import BaseVector


class Vec3d(BaseVector):
    """
    Simple 3d vector class.
    """

    def __new__(cls, x, y, z):
        return tuple.__new__(cls, (x, y, z))

    @property
    def x(self):
        return self[0]

    @property
    def y(self):
        return self[1]

    @property
    def z(self):
        return self[2]

    @classmethod
    def from_unsafe_dict(cls, dct: dict, /) -> 'Vec3d':
        return cls(dct['x'], dct['y'], dct['z'])
