import abc


class Tower(abc.ABC):
    def __init__(self, position):
        self.position = position

    @abc.abstractmethod
    def get_icon(self):
        pass

    @abc.abstractmethod
    def draw(self):
        pass
    
    def update(self, first_enemy):
        pass
