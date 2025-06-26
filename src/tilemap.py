import pygame
import random

TILE_SIZE = 32

def load_tile_images(images_dict):
    return {
        0: images_dict['Tile_01'],
        1: images_dict['Tile_02'],
        2: images_dict['Tile_03'],
    }

# Generowanie mapy
def generate_tile_map(width=200, height=200, tile_variants=3):
    return [
        [random.randint(0, tile_variants - 1) for _ in range(width)]
        for _ in range(height)
    ]

def draw_tile_map(surface, tile_map, tile_images, camera_x, camera_y, screen_width, screen_height):
    rows = len(tile_map)
    cols = len(tile_map[0])

    start_col = camera_x // TILE_SIZE
    offset_x = -(camera_x % TILE_SIZE)

    start_row = camera_y // TILE_SIZE
    offset_y = -(camera_y % TILE_SIZE)

    for j in range(screen_height // TILE_SIZE + 2):
        y = (start_row + j) % rows
        for i in range(screen_width // TILE_SIZE + 2):
            x = (start_col + i) % cols
            tile = tile_map[y][x]
            tile_img = tile_images[tile]
            surface.blit(tile_img, (i * TILE_SIZE + offset_x, j * TILE_SIZE + offset_y))
