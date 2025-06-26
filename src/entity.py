# entity.py
import pygame

class Entity(pygame.sprite.Sprite):
    def __init__(self, image, x, y):
        super().__init__()
        self.image = image.convert_alpha()
        self.map_x = x
        self.map_y = y
        self.rect = self.image.get_rect(center=(self.map_x, self.map_y))
        self.mask = pygame.mask.from_surface(self.image)

    def draw(self, surface, camera_x, camera_y):
        surface.blit(self.image, (self.rect.x - camera_x, self.rect.y - camera_y))

    def sync_rect(self, camera_x, camera_y):
        self.rect.centerx = self.map_x - camera_x
        self.rect.centery = self.map_y - camera_y

    def get_mask_topleft(self):
        return (self.map_x - self.rect.width // 2, self.map_y - self.rect.height // 2)
