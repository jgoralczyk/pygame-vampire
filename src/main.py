import pygame, os, random


pygame.font.init()

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
        self.map_x = cx
        self.map_y = cy
        self.speed = 4

        self.rect = self.image.get_rect()

    def draw(self, surface):
        surface.blit(self.image, self.rect)

    def update(self, keys):
        if keys[pygame.K_LEFT]:
            self.map_x -= self.speed
        if keys[pygame.K_RIGHT]:
            self.map_x += self.speed
        if keys[pygame.K_UP]:
            self.map_y -= self.speed
        if keys[pygame.K_DOWN]:
            self.map_y += self.speed
    
    def _get_event(self, key_pressed):
        pass

    # liczymy ekranową pozycje gracza
    def sync_rect(self, camera_x, camera_y):
        self.rect.centerx = self.map_x - camera_x
        self.rect.centery = self.map_y - camera_y

class Enemy(pygame.sprite.Sprite):
    def __init__(self,image,x,y):
        super().__init__()
        self.image = image
        self.rect = self.image.get_rect(center=(x,y))
        self.speed = 1.5
        
    def draw(self,surface, camera_x, camera_y):
        surface.blit(self.image,(self.rect.x - camera_x, self.rect.y - camera_y))

    def update(self, player_pos):
        dx = player_pos[0] - self.rect.centerx
        dy = player_pos[1] - self.rect.centery
        distance = (dx**2 + dy**2) ** 0.5

        if distance != 0:
            dx /= distance
            dy /= distance
        
        self.rect.x += dx * self.speed
        self.rect.y += dy * self.speed

TILE_SIZE = 32
tile_images = {
    0: IMAGES['Tile_01'],
    1: IMAGES['Tile_02'],
    2: IMAGES['Tile_03'],
}

#przygotowanie macierzy mapy
tile_map = [
    [random.randint(0,2) for _ in range(200)]
    for _ in range(200)
]

MAP_WIDTH = len(tile_map[0])
MAP_HEIGHT = len(tile_map)

#przygotowanie przeciwników
enemies = pygame.sprite.Group()
for _ in range(11):
    x = random.randint(0,MAP_WIDTH * TILE_SIZE)
    y = random.randint(0,MAP_HEIGHT * TILE_SIZE)
    enemies.add(Enemy(IMAGES['enemy3'], x, y))

def draw_tile_map(surface, camera_x, camera_y):
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
#enemy = Enemy(IMAGES['enemy3'],100,100)

camera_x = player.map_x - WIDTH // 2
camera_y = player.map_y - HEIGHT // 2

my_font = pygame.font.SysFont('Comic Sans MS', 30)

window_open = True
while window_open:
    
    #petla zdarzen
    for event in pygame.event.get():
        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_ESCAPE:
                window_open = False
        if event.type == pygame.QUIT:
            window_open = False
    
    #chodzenie stworow
    for enemy in enemies:
        enemy.update((player.map_x, player.map_y))

    key_pressed = pygame.key.get_pressed()
    player.update(key_pressed)

    player.sync_rect(camera_x, camera_y)
    
    # Przesunięcie kamery by "dogonić" gracza
    camera_x += player.rect.centerx - WIDTH // 2
    camera_y += player.rect.centery - HEIGHT // 2
    
    # Po zmianie kamery przeliczamy pozycje gracza względem nowego widoku
    player.sync_rect(camera_x, camera_y)

    text_surface = my_font.render(f'x: {player.map_x}, y: {player.map_y}', False, (0, 0, 0))

    screen.fill((0, 0, 0))
    draw_tile_map(screen, camera_x, camera_y)
    screen.blit(text_surface, (0,0))
    player.draw(screen)
    for enemy in enemies:
        enemy.draw(screen, camera_x, camera_y)

    #aktualizacja okna
    pygame.display.flip()
    clock.tick(60)

pygame.quit()
