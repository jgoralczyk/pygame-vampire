import pygame

# Ekran
WIDTH, HEIGHT = 1920, 1080
SIZESCREEN = (WIDTH, HEIGHT)
TILE_SIZE = 32

# Kolory
BG = (0, 0, 0)
GREEN = (0, 255, 0)
RED = (255, 0, 0)
BLUE = (0, 0, 255)
WHITE = (255, 255, 255)
YELLOW = (255, 215, 0)

# Czcionka
pygame.font.init()
FONT_NAME = 'Comic Sans MS'
FONT_SIZE = 30
FONT = pygame.font.SysFont(FONT_NAME, FONT_SIZE)

# Kamera
CAMERA_SPEED = 1  # ewentualnie do wykorzystania

# Inne
FPS = 60
