import abc


class AProjectile(abc.ABC):
    """ Abstract base class for all projectiles.
    Projectiles can be implimented really in any way you want, as long as they
    have the update, draw, and is_expired methods. """

    allowed_out_of_bounds = False

    @abc.abstractmethod
    def draw(self):
        pass

    @abc.abstractmethod
    def update(self):
        pass

    @abc.abstractmethod
    def is_expired(self) -> bool:
        pass
