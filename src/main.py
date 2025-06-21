import pygame, os, random


pygame.font.init()

SIZESCREEN = WIDTH, HEIGHT = 1920, 1080
screen = pygame.display.set_mode(SIZESCREEN)
clock = pygame.time.Clock()

#define colours
BG = (0, 0, 0)
GREEN = (0, 255, 0)
RED = (255, 0, 0)
BLUE = (0, 0, 255)
WHITE = (255, 255, 255)

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
        self.image = image.convert_alpha()
        self.rect = self.image.get_rect(center=(cx, cy))
        self.mask = pygame.mask.from_surface(self.image)
        self.map_x = cx
        self.map_y = cy
        self.speed = 6
        self.maxhp = 80
        self.curhp = self.maxhp
        self.armor = 0

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
    
    def get_mask_topleft(self):
        return (self.map_x - self.rect.width // 2, self.map_y - self.rect.height // 2)

class Enemy(pygame.sprite.Sprite):
    def __init__(self,image,x,y):
        super().__init__()
        self.image = image
        self.map_x = x
        self.map_y = y
        self.rect = self.image.get_rect(center=(self.map_x, self.map_y))
        self.mask = pygame.mask.from_surface(self.image)
        self.speed = 3
        
    def draw(self,surface, camera_x, camera_y):
        surface.blit(self.image,(self.rect.x - camera_x, self.rect.y - camera_y))

    def update(self, player_pos):
        dx = player_pos[0] - self.rect.centerx
        dy = player_pos[1] - self.rect.centery
        distance = (dx**2 + dy**2) ** 0.5

        if distance != 0:
            dx /= distance
            dy /= distance
        
        self.map_x += dx * self.speed
        self.map_y += dy * self.speed
        self.rect.centerx = self.map_x
        self.rect.centery = self.map_y
    
    def sync_rect(self, camera_x, camera_y):
        self.rect.centerx = self.map_x - camera_x
        self.rect.centery = self.map_y - camera_y

    def get_mask_topleft(self):
        return (self.map_x - self.rect.width // 2, self.map_y - self.rect.height // 2)

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

players = pygame.sprite.Group()
player = Player(IMAGES['player'],WIDTH//2,HEIGHT//2)
players.add(player)
#enemy = Enemy(IMAGES['enemy3'],100,100)


def mask_collision(s1, s2):
    x1, y1 = s1.get_mask_topleft()
    x2, y2 = s2.get_mask_topleft()
    offset = (int(x2 - x1), int(y2 - y1))
    return s1.mask.overlap(s2.mask, offset) is not None


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

    key_pressed = pygame.key.get_pressed()
    player.update(key_pressed)

    player.sync_rect(camera_x, camera_y)
    
    # Zanim zaktualizujesz kamerę: kolizje
    collided_enemies = pygame.sprite.spritecollide(player, enemies, False, pygame.sprite.collide_mask)

    for enemy in enemies:
        if mask_collision(player, enemy):
            enemy.update((player.map_x, player.map_y))
            print("przeciwnik kolizja")
        else:
            enemy.update((player.map_x, player.map_y))



    
    # Przesunięcie kamery by "dogonić" gracza
    camera_x += player.rect.centerx - WIDTH // 2
    camera_y += player.rect.centery - HEIGHT // 2
    
    # Po zmianie kamery przeliczamy pozycje gracza względem nowego widoku
    player.sync_rect(camera_x, camera_y)

    text_surface = my_font.render(f'x: {player.map_x}, y: {player.map_y}', False, (0, 0, 0))
    text_surface2 = my_font.render(f'enemies: {len(enemies)}', False, (0, 0, 0))


    screen.fill((0, 0, 0))
    draw_tile_map(screen, camera_x, camera_y)
    screen.blit(text_surface, (0,0))
    screen.blit(text_surface2, (250,0))
    player.draw(screen)

    for enemy in enemies:
        enemy.draw(screen, camera_x, camera_y)
    
    pygame.draw.rect(screen, "red", (player.rect.centerx - 40, player.rect.centery + 20, 80, 10))
    pygame.draw.rect(screen, "green", (player.rect.centerx - 40, player.rect.centery + 20, player.curhp , 10))
    if player.curhp != 0:
        player.curhp -= 0.1


    #aktualizacja okna
    pygame.display.flip()
    clock.tick(60)

pygame.quit()
