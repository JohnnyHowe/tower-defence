import abc
from a_projectile import AProjectile


class AEnemy:

    path: list

    def __init__(self, path):
        self.path = path

    @abc.abstractmethod
    def draw(self):
        pass

    @abc.abstractmethod
    def update(self):
        pass

    @abc.abstractmethod
    def get_position(self):
        pass

    @abc.abstractmethod
    def get_distance(self):
        pass

    @abc.abstractmethod
    def is_dead(self):
        pass

    @abc.abstractmethod
    def take_damage(self, projectile: AProjectile):
        pass
