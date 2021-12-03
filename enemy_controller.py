from bad_square import BadSquare


class EnemyController:

    enemies = []

    def start_round(self, path):
        self.enemies.append(BadSquare(path))

    def update(self):
        for enemy in self.enemies:
            enemy.update()

    def draw(self):
        for enemy in self.enemies:
            enemy.draw()

    def get_first_enemy(self):
        """ Get the enemy who has travelled the furthurest through the world. """
        if len(self.enemies) > 0:
            return max(self.enemies, key=lambda x: x.position)
        else:
            return None

    def has_enemy_finished(self):
        enemy = self.get_first_enemy()
        return enemy is not None and enemy.position >= len(enemy.path) - 1
