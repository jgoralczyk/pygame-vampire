import pygame
from settings import WIDTH, HEIGHT, WHITE, FONT

def draw_start_screen(screen):
    screen.fill((0, 0, 0))
    title = FONT.render("WAMPIRUCHY - Press SPACE to start", True, WHITE)
    screen.blit(title, (WIDTH // 2 - title.get_width() // 2, HEIGHT // 2))
    pygame.display.flip()

def draw_end_screen(screen, kills, coins):
    screen.fill((0, 0, 0))
    text1 = FONT.render("Game Over", True, WHITE)
    text2 = FONT.render(f"Kills: {kills}", True, WHITE)
    text3 = FONT.render(f"Coins: {coins}", True, WHITE)
    text4 = FONT.render("Press R to Restart or ESC to Quit", True, WHITE)
    screen.blit(text1, (WIDTH // 2 - text1.get_width() // 2, HEIGHT // 2 - 80))
    screen.blit(text2, (WIDTH // 2 - text2.get_width() // 2, HEIGHT // 2 - 30))
    screen.blit(text3, (WIDTH // 2 - text3.get_width() // 2, HEIGHT // 2 + 20))
    screen.blit(text4, (WIDTH // 2 - text4.get_width() // 2, HEIGHT // 2 + 70))
    pygame.display.flip()
