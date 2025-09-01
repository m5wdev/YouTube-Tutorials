import pygame
import random


WIDTH, HEIGHT = 1920, 1080

ASSETS_PATH = 'assets/'
ASSETS = {
    'road': ASSETS_PATH + 'road.jpg',
    'car': ASSETS_PATH + 'car.png',
    'enemy': ASSETS_PATH + 'enemy.png',
    'explosion': ASSETS_PATH + 'explosion.png',
}


# Road
road_img = pygame.image.load(ASSETS['road'])
# resize road imge
road_img = pygame.transform.smoothscale(road_img, ((WIDTH // 2) - 600, HEIGHT))

road_y1 = 0
road_y2 = -road_img.get_height()
ROAD_SCROLL_SPEED = 5 # px\per frame


# Player
player_img = pygame.image.load(ASSETS['car'])
player_img = pygame.transform.smoothscale(player_img, (player_img.get_width() * 1.5, player_img.get_height() * 1.5))

player_pos_x = WIDTH // 2
player_pos_y = (HEIGHT - player_img.get_height()) - 30

player_rect = player_img.get_rect()


# Enemies
ENEMIES_SPAWN_INTERVAL = 1500 # ms
ENEMY_SPEED = 6 # px/frame
last_spawn_time = pygame.time.get_ticks()

enemy_img = pygame.image.load(ASSETS['enemy'])
enemy_img = pygame.transform.smoothscale(enemy_img, (enemy_img.get_width() * 1.5, enemy_img.get_height() * 1.5))

enemies = []


# Explosion
explosion_img = pygame.image.load(ASSETS['explosion'])
explosion_img = pygame.transform.smoothscale(explosion_img, (120, 120))


pygame.init()

display = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption('Racing Game \\ dev-ed.ru')
clock = pygame.time.Clock()

running = True

while running:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False

    if event.type == pygame.KEYDOWN:
        if event.key == pygame.K_ESCAPE:
            running = False

    display.fill((0, 0, 0))

    # Scroll Road
    road_y1 += ROAD_SCROLL_SPEED
    road_y2 += ROAD_SCROLL_SPEED
    if road_y1 > HEIGHT:
        road_y1 = road_y2 - road_img.get_height()
    if road_y2 > HEIGHT:
        road_y2 = road_y1 - road_img.get_height()

    display.blit(road_img, ((WIDTH // 2) - (road_img.get_width() // 2), road_y1))
    display.blit(road_img, ((WIDTH // 2) - (road_img.get_width() // 2), road_y2))
    # END Scroll Road


    # Player
    keys = pygame.key.get_pressed()
    if keys[pygame.K_LEFT]:
        player_pos_x -= 10
    if keys[pygame.K_RIGHT]:
        player_pos_x += 10
    if keys[pygame.K_UP]:
        player_pos_y -= 5
    if keys[pygame.K_DOWN]:
        player_pos_y += 5

    player_rect = player_img.get_rect(x=player_pos_x, y=player_pos_y)
    pygame.draw.rect(display, (0, 255, 0), player_rect, 4)
    display.blit(player_img, (player_pos_x, player_pos_y))
    # END Player


    # Enemies
    now = pygame.time.get_ticks()
    if now - last_spawn_time >= ENEMIES_SPAWN_INTERVAL:
        enemy_rect = enemy_img.get_rect(topleft=(WIDTH // 2, - enemy_img.get_height()))
        # random enemies position
        enemy_rect.x = random.randint(
            (WIDTH // 2) - (road_img.get_width() // 2) + player_img.get_width(),
            (WIDTH // 2) + (road_img.get_width() // 2) - player_img.get_width()
        )
        enemies.append(enemy_rect)
        last_spawn_time = now

    # make enemies move
    for enemy in enemies:
        enemy.y += ENEMY_SPEED
    enemies = [enemy for enemy in enemies if enemy.y < HEIGHT + enemy_img.get_height()]

    # Draw enemies
    for enemy in enemies:
        pygame.draw.rect(display, (255, 0, 0), enemy, 4)
        display.blit(enemy_img, enemy)
    # END Enemies


    # Game over conditions
    crash_into = None
    for enemy in enemies:
        if player_rect.colliderect(enemy):
            crash_into = enemy
            break

    if crash_into:
        impact_x = (player_rect.centerx + crash_into.centerx) // 2
        impact_y = (player_rect.centery + crash_into.centery) // 2
        display.blit(explosion_img, explosion_img.get_rect(center=(impact_x, impact_y)))
        pygame.display.flip()

        pause = True
        while pause:
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    running = False
                    pause = False

                if event.type == pygame.KEYDOWN:
                    if event.key == pygame.K_ESCAPE:
                        running = False
                        pause = False

                    if event.key == pygame.K_SPACE:
                        pause = False

                        enemies = []
                        player_pos_x = WIDTH // 2
                        player_pos_y = (HEIGHT - player_img.get_height()) - 30

    pygame.display.flip()
    clock.tick(60)

pygame.quit()
