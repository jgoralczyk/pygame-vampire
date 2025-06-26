import pygame

RED = (255, 0, 0)

class Projectile(pygame.sprite.Sprite):
    def __init__(self, x, y, target_x, target_y, color=RED, radius=10, speed=10):
        super().__init__()
        self.color = color
        self.radius = radius
        self.map_x = x
        self.map_y = y
        self.speed = speed

        # Oblicz kierunek
        dx = target_x - x
        dy = target_y - y
        distance = max((dx**2 + dy**2) ** 0.5, 0.01)
        self.dx = dx / distance
        self.dy = dy / distance

        self.rect = pygame.Rect(x, y, radius * 2, radius * 2)

    def update(self):
        self.map_x += self.dx * self.speed
        self.map_y += self.dy * self.speed
        self.rect.center = (self.map_x, self.map_y)

    def draw(self, surface, camera_x, camera_y):
        pygame.draw.circle(
            surface,
            self.color,
            (int(self.rect.x - camera_x), int(self.rect.y - camera_y)),
            self.radius
        )
