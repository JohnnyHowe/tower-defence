from bad_square import BadSquare

from engine.clock import Clock


class EnemyController:

    round: list
    round_timer: float
    round_running: bool
    round_enemy_index: int
    round_enemy_cumulative_delay: float
    enemies: list
    path: list

    def __init__(self):
        self.enemies = []
        self.round = [
            # (type, delay)
            (BadSquare, 1) for i in range(10)
        ]

        self.round_running = False
        self.round_timer = 0

    def start_round(self, path):
        self.round_running = True
        self.round_timer = 0
        self.round_enemy_index = 0
        self.round_enemy_cumulative_delay = 0
        self.path = path

    def update(self):
        self.update_enemies()
        self.update_round()

    def update_round(self):
        if self.round_running:
            self.round_timer += Clock.dt
            while len(self.round) > self.round_enemy_index and self.round[self.round_enemy_index][1] + self.round_enemy_cumulative_delay < self.round_timer:
                self.enemies.append(self.round[self.round_enemy_index][0](self.path))
                self.round_enemy_cumulative_delay += self.round[self.round_enemy_index][1]
                self.round_enemy_index += 1

    def update_enemies(self):
        new_enemies = []
        for enemy in self.enemies:
            enemy.update()
            if not enemy.is_dead():
                new_enemies.append(enemy)
        self.enemies = new_enemies

    def draw(self):
        for enemy in self.enemies:
            enemy.draw()

    def get_first_enemy(self):
        """ Get the enemy who has travelled the furthurest through the world. """
        if len(self.enemies) > 0:
            return max(self.enemies, key=lambda x: x.get_distance())
        else:
            return None

    def has_enemy_finished(self):
        enemy = self.get_first_enemy()
        return enemy is not None and enemy.has_finished() 

    def is_round_complete(self):
        """ Have all the enemies been destroyed and are we finished spawning them? """
        return len(self.round) <= self.round_enemy_index and len(self.enemies) == 0
