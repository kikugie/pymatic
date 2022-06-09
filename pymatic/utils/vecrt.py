from pymatic.utils.base_vector import BaseVector


class VecRt(BaseVector):
    """
    Simple rotation vector class.
    """

    def __new__(cls, yaw, pitch):
        return tuple.__new__(cls, (yaw, pitch))

    @property
    def yaw(self):
        return self[0]

    @property
    def pitch(self):
        return self[1]

    @classmethod
    def from_unsafe_dict(cls, dct: dict, /) -> 'VecRt':
        return cls(dct['yaw'], dct['pitch'])