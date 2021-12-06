from bad_square import BadSquare


class EnemyController:

    enemies = []

    def start_round(self, path):
        self.enemies.append(BadSquare(path))

    def update(self):
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
            return max(self.enemies, key=lambda x: x.get_position())
        else:
            return None

    def has_enemy_finished(self):
        enemy = self.get_first_enemy()
        return enemy is not None and enemy.get_distance() >= len(enemy.path) - 1
