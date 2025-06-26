import pygame, sys, os, random

from settings import WIDTH, HEIGHT, WHITE, RED, GREEN, BLUE, TILE_SIZE, FONT
from screens import draw_start_screen, draw_end_screen
from player import Player
from enemy import Enemy
from projectile import Projectile
from item import Item
from tilemap import draw_tile_map, generate_tile_map, load_tile_images

pygame.init()
screen = pygame.display.set_mode((WIDTH, HEIGHT))
clock = pygame.time.Clock()


# Ładowanie obrazów
path = os.path.join(os.getcwd(), 'assets\images')
file_names = os.listdir(path)
IMAGES = {}
for file_name in file_names:
    image_name = file_name[:-4]
    IMAGES[image_name] = pygame.image.load(os.path.join(path, file_name)).convert_alpha()


# Generowanie mapy
tile_images = load_tile_images(IMAGES)
tile_map = generate_tile_map()
MAP_WIDTH = len(tile_map[0])
MAP_HEIGHT = len(tile_map)


# Inicjalizacja obiektów
player = Player(IMAGES['player'], WIDTH // 2, HEIGHT // 2)
enemies = pygame.sprite.Group()
projectiles = pygame.sprite.Group()
items = pygame.sprite.Group()


# Dodawanie monet
item_colors = [RED, GREEN, BLUE]
for _ in range(50):
    x = random.randint(0, MAP_WIDTH * TILE_SIZE)
    y = random.randint(0, MAP_HEIGHT * TILE_SIZE)
    items.add(Item("coin", x, y))

item_colors = [RED, GREEN, BLUE]

#dodawanie itemków
for _ in range(1000):
    x = random.randint(0, MAP_WIDTH * TILE_SIZE)
    y = random.randint(0, MAP_HEIGHT * TILE_SIZE)
    color = random.choice(item_colors)
    item = Item(color, x, y)
    items.add(item)


# Inicjacja kamery
camera_x = player.map_x - WIDTH // 2
camera_y = player.map_y - HEIGHT // 2


# Zmienne gry
kills = 0
coins = 0
wave_number = 1
time_between_waves = 15000
last_wave_time = pygame.time.get_ticks()
game_state = "start"
window_open = True


# generator fal
def spawn_wave(wave_number):
    num_enemies = 50 + wave_number * 2
    for _ in range(num_enemies):
        x = random.randint(0, MAP_WIDTH * TILE_SIZE)
        y = random.randint(0, MAP_HEIGHT * TILE_SIZE)
        enemy = Enemy(IMAGES['enemy3'], x, y)
        enemies.add(enemy)

spawn_wave(1)

def mask_collision(s1, s2):
    x1, y1 = s1.get_mask_topleft()
    x2, y2 = s2.get_mask_topleft()
    offset = (int(x2 - x1), int(y2 - y1))
    return s1.mask.overlap(s2.mask, offset) is not None


while window_open:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            window_open = False
        elif event.type == pygame.KEYDOWN:
            if event.key == pygame.K_ESCAPE:
                window_open = False

            if game_state == 'start' and event.key == pygame.K_SPACE:
                game_state = 'playing'

            elif game_state == 'game_over' and event.key == pygame.K_r:
                pygame.quit()
                os.execl(sys.executable, sys.executable, *sys.argv)

    if game_state == 'start':
        draw_start_screen(screen)
        continue

    if game_state == 'game_over':
        draw_end_screen(screen, kills, coins)
        continue

    keys= pygame.key.get_pressed()
    player.update(keys)

    now = pygame.time.get_ticks()
    if now - last_wave_time > time_between_waves:
        wave_number += 1
        spawn_wave(wave_number)
        last_wave_time = now

    player.auto_shoot(enemies, projectiles)


    # Synchronizacja kamery z graczem
    player.sync_rect(camera_x, camera_y)
    camera_x += player.rect.centerx - WIDTH // 2
    camera_y += player.rect.centery - HEIGHT // 2
    player.sync_rect(camera_x, camera_y)


    # Kolizje z przeciwnikami i aktualizacja wrogów
    for enemy in enemies:
        enemy.update((player.map_x, player.map_y), enemies)
    
        if mask_collision(player, enemy):
            player.curhp -= 0.1
            print(f"Kolizja! HP gracza: {player.curhp:.1f}")
            if player.curhp <= 0:
                game_state = "game_over"

    
    enemy.draw(screen, camera_x, camera_y)


    # Podnoszenie itemów
    for item in list(items):
        distance = ((player.map_x - item.map_x) ** 2 + (player.map_y - item.map_y) ** 2) ** 0.5
        if distance < 50:
            if item.type == 'coin':
                coins += 1
                item.kill()
            else:
                # obsługa ulepszania itemu (jeśli masz)
                for inv_item in player.inventory:
                    if inv_item['color'] == item.color:
                        inv_item['level'] += 1
                        item.kill()
                        break
                else:
                    player.inventory.append({'color': item.color, 'level': 1})
                    item.kill()

    # Pociski + kolizje
    projectiles.update()
    for projectile in list(projectiles):
        for enemy in list(enemies):
            if projectile.rect.colliderect(enemy.rect):
                enemies.remove(enemy)
                projectiles.remove(projectile)
                kills += 1
                break
    

    # Renderowanko
    screen.fill((0,0,0))
    draw_tile_map(screen, tile_map, tile_images, camera_x, camera_y, WIDTH, HEIGHT)
    player.draw(screen)


    for enemy in enemies:
        enemy.draw(screen,camera_x,camera_y)
    for item in items:
        item.draw(screen,camera_x,camera_y)
    for projectile in projectiles:
        projectile.draw(screen,camera_x,camera_y)
    

    # HUD: hp, fale, coins, inventory
    pygame.draw.rect(screen, (255,0,0), (player.rect.centerx - 40, player.rect.centery + 20, 80,10))
    pygame.draw.rect(screen, (0,255,0), (player.rect.centerx - 40, player.rect.centery + 20, player.curhp, 10))

    wave_text = FONT.render(f'Wave: {wave_number}', True, (255, 255, 255))
    screen.blit(wave_text, (500, 0))

    coin_text = FONT.render(f'Coins: {coins}', True, (255, 215, 0))
    screen.blit(coin_text, (WIDTH - 120, 0))

    for idx, item in enumerate(player.inventory):
        color = item['color']
        level = item['level']
        x = 10 + idx * 40
        y = 10
        pygame.draw.rect(screen, color, (x,y, 30, 30))
        text = FONT.render(str(level), True, WHITE)
        screen.blit(text, (x + 8, y + 20))
        if idx >= 9:
            break

    pygame.display.flip()
    clock.tick(60)

pygame.quit()