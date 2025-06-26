from entity import Entity
from projectile import Projectile

import pygame

class Player(Entity):
    def __init__(self, image, cx, cy):
        super().__init__(image, cx, cy)
        self.speed = 4
        self.maxhp = 80
        self.curhp = self.maxhp
        self.armor = 0
        self.inventory = []
        self.last_shot_time = 0
        self.shoot_cooldown = 2000

    def update(self, keys):
        if keys[pygame.K_LEFT]:
            self.map_x -= self.speed
        if keys[pygame.K_RIGHT]:
            self.map_x += self.speed
        if keys[pygame.K_UP]:
            self.map_y -= self.speed
        if keys[pygame.K_DOWN]:
            self.map_y += self.speed

    def auto_shoot(self, enemies, projectiles):
        now = pygame.time.get_ticks()
        if now - self.last_shot_time < self.shoot_cooldown:
            return

        if not enemies:
            return

        nearest_enemy = min(enemies, key=lambda e: (e.map_x - self.map_x)**2 + (e.map_y - self.map_y)**2)
        bullet = Projectile(self.map_x, self.map_y, nearest_enemy.map_x, nearest_enemy.map_y)
        projectiles.add(bullet)
        self.last_shot_time = now
    
    def draw(self, surface):
        surface.blit(self.image, self.rect)

