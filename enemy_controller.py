from bad_square import BadSquare

from engine.clock import Clock


class EnemyController:

    wave: list
    wave_number: int
    wave_timer: float
    wave_running: bool
    wave_enemy_index: int
    wave_enemy_cumulative_delay: float
    enemies: list
    path: list

    def __init__(self):
        self.enemies = []
        self.waves = [
            # [(type, delay)]
            [(BadSquare, 1) for i in range(10)],
            [(BadSquare, 0.75) for i in range(10)]
        ]

        self.wave_running = False
        self.wave_timer = 0
        self.wave_number = 0

    def start_wave(self, path):
        self.wave_running = True
        self.wave_timer = 0
        self.wave_enemy_index = 0
        self.wave_enemy_cumulative_delay = 0
        self.path = path

    def update(self):
        self.update_enemies()
        self.update_wave()

    def update_wave(self):
        if self.wave_running:
            self.wave_timer += Clock.dt
            this_wave = self.waves[self.wave_number]
            while len(this_wave) > self.wave_enemy_index and this_wave[self.wave_enemy_index][1] + self.wave_enemy_cumulative_delay < self.wave_timer:
                self.enemies.append(this_wave[self.wave_enemy_index][0](self.path))
                self.wave_enemy_cumulative_delay += this_wave[self.wave_enemy_index][1]
                self.wave_enemy_index += 1

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

    def is_wave_complete(self):
        """ Have all the enemies been destroyed and are we finished spawning them? """
        return len(self.waves[self.wave_number]) <= self.wave_enemy_index and len(self.enemies) == 0

    def is_game_complete(self):
        return self.wave_number >= len(self.waves)
