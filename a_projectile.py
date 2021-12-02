import abc


class AProjectile(abc.ABC):
    """ Abstract base class for all projectiles.
    Projectiles can be implimented really in any way you want, as long as they
    have the update, draw, and is_expired methods. """

    @abc.abstractmethod
    def draw(self):
        pass

    @abc.abstractmethod
    def update(self):
        pass

    def is_expired(self) -> bool:
        pass
