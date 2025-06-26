import pygame

COIN_COLOR = (255, 215, 0)

class Item(pygame.sprite.Sprite):
    def __init__(self, type_or_color, x, y):
        super().__init__()
        self.map_x = x
        self.map_y = y
        self.size = 30
        self.type = "item"

        if isinstance(type_or_color, str) and type_or_color == "coin":
            self.type = "coin"
            self.color = COIN_COLOR
            self.image = pygame.Surface((self.size, self.size), pygame.SRCALPHA)
            pygame.draw.circle(
                self.image,
                self.color,
                (self.size // 2, self.size // 2),
                self.size // 2
            )
        else:
            self.color = type_or_color
            self.image = pygame.Surface((self.size, self.size), pygame.SRCALPHA)
            self.image.fill(self.color)

        self.rect = self.image.get_rect(center=(self.map_x, self.map_y))

    def update(self):
        self.rect.center = (self.map_x, self.map_y)

    def draw(self, surface, camera_x, camera_y):
        surface.blit(self.image, (self.rect.x - camera_x, self.rect.y - camera_y))
