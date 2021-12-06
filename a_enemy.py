import abc
from a_projectile import AProjectile
from engine.vector2 import Vector2


class AEnemy:

    path: list

    def __init__(self, path):
        self.path = path

    def get_path(self) -> list:
        return self.path

    def has_finished(self) -> bool:
        return self.get_distance() >= len(self.get_path()) - 1

    @abc.abstractmethod
    def draw(self) -> None:
        pass

    @abc.abstractmethod
    def update(self) -> None:
        pass

    @abc.abstractmethod
    def get_position(self) -> Vector2:
        pass

    @abc.abstractmethod
    def get_distance(self) -> float:
        pass

    @abc.abstractmethod
    def is_dead(self) -> bool:
        pass

    @abc.abstractmethod
    def take_damage(self, projectile: AProjectile) -> None:
        pass
