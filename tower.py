import abc


class Tower(abc.ABC):
    def __init__(self, position):
        self.position = position

    @abc.abstractmethod
    def get_image(self, board):
        pass