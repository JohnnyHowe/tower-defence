

class Vector2():

    def __init__(self, x, y):
        self.x = x
        self.y = y

    def get_copy(self):
        return Vector2(self.x, self.y)

    def __round__(self):
        return Vector2(round(self.x), round(self.y))

    def get_rounded_tuple(self):
        return round(self.x), round(self.y)

    def __repr__(self):
        return "engine.Vector2({}, {})".format(self.x, self.y)

    def __add__(self, other):
        return Vector2(self.x + other.x, self.y + other.y)

    def __sub__(self, other):
        return Vector2(self.x - other.x, self.y - other.y)

    def __iter__(self):
        return iter([self.x, self.y])
