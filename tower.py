import abc


class Tower(abc.ABC):
    def __init__(self, position, projectile_list):
        self.position = position
        self.projectile_list = projectile_list
        self.__init_subclass__()

    @abc.abstractmethod
    def get_icon(self):
        pass

    @abc.abstractmethod
    def draw(self):
        pass
    
    def update(self, first_enemy):
        pass
