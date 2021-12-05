from .vector2 import Vector2


class Rect:
    """ Slightly modified version of the regular pygame rect. """

    def __init__(self, x: float, y: float, w: float, h: float) -> None:
        self.x = x
        self.y = y
        self.w = w
        self.h = h

    def get_center(self) -> Vector2:
        return Vector2(self.x, self.y)

    def get_top_left(self) -> Vector2:
        return Vector2(self.x - self.w / 2, self.y + self.h / 2)

    def get_bottom_left(self) -> Vector2:
        return Vector2(self.x - self.w / 2, self.y - self.h / 2)

    def get_size(self) -> Vector2:
        return Vector2(self.w, self.h)

    def get_pygame_tuple(self, flip_y=False):
        if not flip_y:
            return self.get_top_left().get_rounded_tuple() + self.get_size().get_rounded_tuple()
        else:
            return self.get_bottom_left().get_rounded_tuple() + self.get_size().get_rounded_tuple()

    def contains(self, position: Vector2):
        return (
            self.x - self.w / 2 <= position.x <= self.x + self.w / 2 and
            self.y - self.h / 2 <= position.y <= self.y + self.h / 2
        )
    
    def touching(self, other):
        return (
            self.x + self.w / 2 >= other.x - other.w / 2 and
            self.x - self.w / 2 <= other.x + other.w / 2 and
            self.y + self.h / 2 >= other.y - other.h / 2 and
            self.y - self.h / 2 <= other.y + other.h / 2
        )

    def __repr__(self, n=5):
        return "Rect({}, {}, {}, {})".format(round(self.x, n), round(self.y, n), round(self.w, n), round(self.h, n))
