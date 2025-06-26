import pygame
from entity import Entity

class Enemy(Entity):
    def __init__(self, image, x, y):
        super().__init__(image, x, y)
        self.speed = 2

    def update(self, player_pos, enemies):
        dx = player_pos[0] - self.map_x
        dy = player_pos[1] - self.map_y
        distance = max((dx**2 + dy**2) ** 0.5, 0.01)

        # Ruch w kierunku gracza
        move_x = (dx / distance) * self.speed
        move_y = (dy / distance) * self.speed

        # Odepchnięcie od innych wrogów
        push_x, push_y = 0, 0
        for other in enemies:
            if other == self:
                continue
            offset_x = self.map_x - other.map_x
            offset_y = self.map_y - other.map_y
            dist = (offset_x ** 2 + offset_y ** 2) ** 0.5
            if 0 < dist < 40:
                force = (40 - dist) / 40
                push_x += (offset_x / dist) * force
                push_y += (offset_y / dist) * force

        self.map_x += move_x + push_x * 0.5
        self.map_y += move_y + push_y * 0.5
        self.rect.center = (self.map_x, self.map_y)
