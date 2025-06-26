import pygame, os, sys, random


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

def draw_start_screen():
    screen.fill((0, 0, 0))
    title = my_font.render("WAMPIRUCHY - Press SPACE to start", True, WHITE)
    screen.blit(title, (WIDTH // 2 - title.get_width() // 2, HEIGHT // 2))
    pygame.display.flip()

def draw_end_screen(kills, coins):
    screen.fill((0, 0, 0))
    text1 = my_font.render("Game Over", True, WHITE)
    text2 = my_font.render(f"Kills: {kills}", True, WHITE)
    text3 = my_font.render(f"Coins: {coins}", True, WHITE)
    text4 = my_font.render("Press R to Restart or ESC to Quit", True, WHITE)
    screen.blit(text1, (WIDTH//2 - text1.get_width()//2, HEIGHT//2 - 80))
    screen.blit(text2, (WIDTH//2 - text2.get_width()//2, HEIGHT//2 - 30))
    screen.blit(text3, (WIDTH//2 - text3.get_width()//2, HEIGHT//2 + 20))
    screen.blit(text4, (WIDTH//2 - text4.get_width()//2, HEIGHT//2 + 70))
    pygame.display.flip()


class Player(pygame.sprite.Sprite):
    def __init__(self, image, cx, cy):
        super().__init__()
        self.image = image.convert_alpha()
        self.rect = self.image.get_rect(center=(cx, cy))
        self.mask = pygame.mask.from_surface(self.image)
        self.map_x = cx
        self.map_y = cy
        self.speed = 4
        self.maxhp = 80
        self.curhp = self.maxhp
        self.armor = 0
        self.inventory = []
        #strzały
        self.last_shot_time = 0
        self.shoot_cooldown = 2000

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

    def auto_shoot(self, enemies, projectiles):
        now = pygame.time.get_ticks()
        if now - self.last_shot_time < self.shoot_cooldown:
            return

        if not enemies:
            return

        # znajdź najbliższego wroga
        nearest_enemy = min(enemies, key=lambda e: (e.map_x - self.map_x)**2 + (e.map_y - self.map_y)**2)
        bullet = Projectile(self.map_x, self.map_y, nearest_enemy.map_x, nearest_enemy.map_y)
        projectiles.add(bullet)
        self.last_shot_time = now
    
class Enemy(pygame.sprite.Sprite):
    def __init__(self,image,x,y):
        super().__init__()
        self.image = image
        self.map_x = x
        self.map_y = y
        self.rect = self.image.get_rect(center=(self.map_x, self.map_y))
        self.mask = pygame.mask.from_surface(self.image)
        self.speed = 2
        
    def draw(self,surface, camera_x, camera_y):
        surface.blit(self.image,(self.rect.x - camera_x, self.rect.y - camera_y))

    def update(self, player_pos, enemies):
        dx = player_pos[0] - self.map_x
        dy = player_pos[1] - self.map_y
        distance = max((dx**2 + dy**2) ** 0.5, 0.01)

        # Kierunek do gracza
        move_x = (dx / distance) * self.speed
        move_y = (dy / distance) * self.speed

        # Odepchnięcie od innych przeciwników
        push_x = 0
        push_y = 0
        for other in enemies:
            if other == self:
                continue
            offset_x = self.map_x - other.map_x
            offset_y = self.map_y - other.map_y
            dist = (offset_x ** 2 + offset_y ** 2) ** 0.5
            if dist < 40 and dist > 0:  # tylko bliscy przeciwnicy
                force = (40 - dist) / 40  # im bliżej, tym silniejsze odepchnięcie
                push_x += (offset_x / dist) * force
                push_y += (offset_y / dist) * force

        # Dodaj wektor odepchnięcia (można go zmniejszyć, np. * 0.5)
        self.map_x += move_x + push_x * 0.5
        self.map_y += move_y + push_y * 0.5

        self.rect.centerx = self.map_x
        self.rect.centery = self.map_y



    def get_mask_topleft(self):
        return (self.map_x - self.rect.width // 2, self.map_y - self.rect.height // 2)


class Projectile(pygame.sprite.Sprite):
    def __init__(self, x, y, target_x, target_y, color= RED, radius = 10, speed = 10):
        super().__init__()
        self.color = color
        self.radius = radius
        self.map_x = x
        self.map_y = y
        self.speed = speed
        
        # Oblicz kierunek do celu
        dx = target_x - x
        dy = target_y - y
        distance = max((dx ** 2 + dy ** 2) ** 0.5, 0.01)
        self.dx = dx / distance
        self.dy = dy / distance
        
        self.rect = pygame.Rect(x, y, radius*2, radius*2)
    
    def update(self):
        self.map_x += self.dx * self.speed
        self.map_y += self.dy * self.speed
        self.rect.center = (self.map_x, self.map_y)
    
    def draw(self,surface, camera_x, camera_y):
        pygame.draw.circle(surface, self.color, (int(self.rect.x - camera_x), int(self.rect.y - camera_y)), self.radius)


class Item(pygame.sprite.Sprite):
    def __init__(self, type_or_color, x, y):
        super().__init__()
        self.map_x = x
        self.map_y = y
        self.size = 30
        self.type = "item"

        if isinstance(type_or_color, str) and type_or_color == "coin":
            self.type = "coin"
            self.color = (255, 215, 0)
            self.image = pygame.Surface((self.size, self.size), pygame.SRCALPHA)
            pygame.draw.circle(self.image, self.color, (self.size // 2, self.size // 2), self.size // 2)
        else:
            self.color = type_or_color
            self.image = pygame.Surface((self.size, self.size), pygame.SRCALPHA)
            self.image.fill(self.color)

        self.rect = self.image.get_rect(center=(self.map_x, self.map_y))

    def update(self):
        self.rect.center = (self.map_x, self.map_y)

    def draw(self, surface, camera_x, camera_y):
        surface.blit(self.image, (self.rect.x - camera_x, self.rect.y - camera_y))
    

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
projectiles = pygame.sprite.Group()
fire_counter = 0



def mask_collision(s1, s2):
    x1, y1 = s1.get_mask_topleft()
    x2, y2 = s2.get_mask_topleft()
    offset = (int(x2 - x1), int(y2 - y1))
    return s1.mask.overlap(s2.mask, offset) is not None


camera_x = player.map_x - WIDTH // 2
camera_y = player.map_y - HEIGHT // 2

my_font = pygame.font.SysFont('Comic Sans MS', 30)

items = pygame.sprite.Group()
item_colors = [RED, GREEN, BLUE]

#dodawanie itemków
for _ in range(10):
    x = random.randint(0, MAP_WIDTH * TILE_SIZE)
    y = random.randint(0, MAP_HEIGHT * TILE_SIZE)
    color = random.choice(item_colors)
    item = Item(color, x, y)
    items.add(item)

#dodawanie monet
for _ in range(10):
    x = random.randint(0, MAP_WIDTH * TILE_SIZE)
    y = random.randint(0, MAP_HEIGHT * TILE_SIZE)
    items.add(Item("coin", x, y))


test_item = Item(GREEN, player.map_x - 100, player.map_y)
items.add(test_item)

#przygotowanie przeciwników
enemies = pygame.sprite.Group()
def spawn_wave(wave_number):
    num_enemies = 50 + wave_number * 2
    for _ in range(num_enemies):
        x = random.randint(0, MAP_WIDTH * TILE_SIZE)
        y = random.randint(0, MAP_HEIGHT * TILE_SIZE)
        enemy = Enemy(IMAGES['enemy3'], x, y)
        enemies.add(enemy)













kills = 0
coins = 0

wave_number = 1
time_between_waves = 15000  # 15 sekund
last_wave_time = pygame.time.get_ticks()
spawn_wave(1)

game_state = "start"  # może być: "start", "playing", "game_over"
window_open = True

while window_open:
    
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            window_open = False
        elif event.type == pygame.KEYDOWN:
            if event.key == pygame.K_ESCAPE:
                window_open = False
            
            if game_state == "start":
                if event.key == pygame.K_SPACE:
                    game_state = "playing"

            elif game_state == "game_over":
                if event.key == pygame.K_r:
                    pygame.quit()
                    os.execl(sys.executable, sys.executable, *sys.argv)

    
    # Obsługa startu gry
    if game_state == "start":
        draw_start_screen()
        if pygame.key.get_pressed()[pygame.K_SPACE]:
            game_state = "playing"
        continue

    # Obsługa końca gry
    if game_state == "game_over":
        draw_end_screen(kills, coins)
        continue

    key_pressed = pygame.key.get_pressed()
    player.update(key_pressed)  

    now = pygame.time.get_ticks()
    if now - last_wave_time > time_between_waves:
        wave_number += 1
        spawn_wave(wave_number)
        last_wave_time = now

    
    player.auto_shoot(enemies, projectiles)

    player.sync_rect(camera_x, camera_y)
    
    # Zanim zaktualizujesz kamerę: kolizje
    collided_enemies = pygame.sprite.spritecollide(player, enemies, False, pygame.sprite.collide_mask)

    for enemy in enemies:
        if mask_collision(player, enemy):
            enemy.update((player.map_x, player.map_y), enemies)
            print("przeciwnik kolizja")
            player.curhp -= 0.1
            if player.curhp <= 0:
                game_state = "game_over"

        else:
            enemy.update((player.map_x, player.map_y), enemies)

    for item in list(items):
        distance = ((player.map_x - item.map_x)**2 + (player.map_y - item.map_y)**2)**0.5
        if distance < 50:
            if item.type == "coin":
                coins += 1
            else:
                # obsługa ulepszania itemu (jeśli masz)
                for inv_item in player.inventory:
                    if inv_item['color'] == item.color:
                        inv_item['level'] += 1
                        break
                else:
                    player.inventory.append({'color': item.color, 'level': 1})
            items.remove(item)
  



    
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
        
    projectiles.update()
    
    # Rysowanie itemów
    for item in items:
        item.update()
        item.draw(screen, camera_x, camera_y)


    for projectile in projectiles:
        projectile.draw(screen, camera_x, camera_y)
        for enemy in enemies:
            if pygame.Rect.colliderect(projectile.rect, enemy.rect):
                enemies.remove(enemy)
                projectiles.remove(projectile)
                kills += 1
                break
    
  
    #wyświetlanie paska życia
    pygame.draw.rect(screen, "red", (player.rect.centerx - 40, player.rect.centery + 20, 80, 10))
    pygame.draw.rect(screen, "green", (player.rect.centerx - 40, player.rect.centery + 20, player.curhp , 10))

    #wyświetlanie licznika fali
    wave_text = my_font.render(f'Wave: {wave_number}', False, (255, 255, 255))
    screen.blit(wave_text, (500, 0))

    #wyświetlanie licznika monet
    coin_text = my_font.render(f'Coins: {coins}', False, (255, 215, 0))
    screen.blit(coin_text, (WIDTH - 120, 0))


    
    #wyświetlanie inventory
    for idx, item in enumerate(player.inventory):
        color = item['color']
        level = item['level']
        x = 10 + idx * 40
        y = 10
        pygame.draw.rect(screen, color, (x, y, 30, 30))
    
        # Napis z poziomem
        text = my_font.render(str(level), True, WHITE)
        screen.blit(text, (x + 8, y + 20))

        if idx >= 9:
            break




    #aktualizacja okna
    pygame.display.flip()
    clock.tick(60)

pygame.quit()
