import pygame, os, random

SIZESCREEN = WIDTH, HEIGHT = 1920, 1080
screen = pygame.display.set_mode(SIZESCREEN)
clock = pygame.time.Clock()

path = os.path.join(os.getcwd(), 'assets/images')
file_names = os.listdir(path)
BACKGROUND = pygame.image.load(os.path.join(path, 'background.jpg')).convert()
file_names.remove('background.jpg')
IMAGES = {}
for file_name in file_names:
    image_name = file_name[:-4]
    IMAGES[image_name] = pygame.image.load(os.path.join(path, file_name)).convert_alpha(BACKGROUND)


class Player(pygame.sprite.Sprite):
    def __init__(self, image, cx, cy):
        super().__init__()
        self.image = image
        self.rect = self.image.get_rect(center=(cx, cy))
        self.speed = 4
    
    def draw(self, surface):
        surface.blit(self.image, self.rect)

    def update(self, key_pressed):
        self._get_event(key_pressed)

    
    def _get_event(self, key_pressed):
        if key_pressed[pygame.K_LEFT]:
            self.rect.x -= self.speed
        if key_pressed[pygame.K_RIGHT]:
            self.rect.x += self.speed
        if key_pressed[pygame.K_UP]:
            self.rect.y -= self.speed
        if key_pressed[pygame.K_DOWN]:
            self.rect.y += self.speed

TILE_SIZE = 32
tile_images = {
    0: IMAGES['Tile_01'],
    1: IMAGES['Tile_02'],
    2: IMAGES['Tile_03'],
}

tile_map = [
    [random.randint(0,2) for _ in range(200)]
    for _ in range(200)
]

MAP_WIDTH = len(tile_map[0])
MAP_HEIGHT = len(tile_map)

def draw_tile_map(sruface, camera_x, camera_y):
    rows = len(tile_map)
    cols = len(tile_map[0])
    
    start_col = camera_x // TILE_SIZE
    offset_x = -(camera_x % TILE_SIZE)

    start_row = camera_y // TILE_SIZE
    offset_y = -(camera_y % TILE_SIZE)
    
    for j in range(HEIGHT // TILE_SIZE + 2):
        y = (start_row + j) % rows
        for i in range(WIDTH // TILE_SIZE + 2):
            x = (start_col + i) % cols
            tile = tile_map[y][x]
            tile_img = tile_images[tile]
            screen.blit(tile_img, (i * TILE_SIZE + offset_x, j * TILE_SIZE + offset_y))

player = Player(IMAGES['player'],WIDTH//2,HEIGHT//2)

camera_x = 0
camera_y = 0

window_open = True
while window_open:
    
    #petla zdarzen
    for event in pygame.event.get():
        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_ESCAPE:
                window_open = False
        if event.type == pygame.QUIT:
            window_open = False

    key_pressed = pygame.key.get_pressed()
    player.update(key_pressed)

    # Kamera przesuwa się razem z graczem w poziomie (endless scroll)
    camera_x += (player.rect.centerx - WIDTH // 2)
    player.rect.centerx = WIDTH // 2  # Trzymaj gracza w środku

    # Kamera pionowa: przesuń tło gdy gracz się rusza
    camera_y += (player.rect.centery - HEIGHT // 2)
    player.rect.centery = HEIGHT // 2  # Trzymaj gracza na środku Y

    screen.fill((0, 0, 0))
    draw_tile_map(screen, camera_x, camera_y)
    player.draw(screen)

    #aktualizacja okna
    pygame.display.flip()
    clock.tick(60)

pygame.quit()
    