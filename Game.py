
import pygame
import random

pygame.init()

# Screen
screen = pygame.display.set_mode((600, 700))
pygame.display.set_caption("SPACE SHOOTER")
clock = pygame.time.Clock()
font = pygame.font.Font(None, 35)

# Colors
WHITE = (255, 255, 255)
BLUE = (50, 150, 255)
RED = (255, 70, 70)
YELLOW = (255, 220, 0)
BLACK = (10, 10, 25)

# Recursion: create background stars
def make_stars(n):
    if n == 0:
        return []
    return [(random.randint(0, 600), random.randint(0, 700))] + make_stars(n - 1)

stars = make_stars(60)

# Main game function
def game():
    player = pygame.Rect(275, 620, 50, 40)
    bullets = []
    enemies = []

    score = 0
    lives = 3
    enemy_timer = 0
    fire_timer = 0
    running = True

    while running:
        screen.fill(BLACK)

        # Background stars
        for x, y in stars:
            pygame.draw.circle(screen, WHITE, (x, y), 2)

        # Events
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False
                return

        keys = pygame.key.get_pressed()

        # Player movement
        if keys[pygame.K_LEFT] and player.x > 0:
            player.x -= 5
        if keys[pygame.K_RIGHT] and player.x < 550:
            player.x += 5

        # Unlimited bullets (automatic firing while space is held)
        fire_timer += 1
        if keys[pygame.K_SPACE] and fire_timer >= 10:
            bullets.append(pygame.Rect(player.centerx - 3, player.y, 6, 15))
            fire_timer = 0

        # Move bullets
        for bullet in bullets[:]:
            bullet.y -= 8
            if bullet.y < 0:
                bullets.remove(bullet)

        # Create enemies
        enemy_timer += 1
        if enemy_timer >= 40:
            enemies.append(pygame.Rect(random.randint(20, 550), 0, 35, 35))
            enemy_timer = 0

        # Move enemies
        for enemy in enemies[:]:
            enemy.y += 3

            if enemy.y > 700:
                enemies.remove(enemy)
                lives -= 1

        # Bullet-enemy collision
        for bullet in bullets[:]:
            for enemy in enemies[:]:
                if bullet.colliderect(enemy):
                    bullets.remove(bullet)
                    enemies.remove(enemy)
                    score += 10
                    break

        # Enemy-player collision
        for enemy in enemies[:]:
            if enemy.colliderect(player):
                enemies.remove(enemy)
                lives -= 1

        # Draw player spaceship
        pygame.draw.polygon(screen, BLUE, [
            (player.centerx, player.y),
            (player.x, player.bottom),
            (player.centerx, player.bottom - 10),
            (player.right, player.bottom)
        ])

        # Draw bullets
        for bullet in bullets:
            pygame.draw.rect(screen, YELLOW, bullet)

        # Draw enemies
        for enemy in enemies:
            pygame.draw.rect(screen, RED, enemy, border_radius=8)
            pygame.draw.circle(screen, WHITE, (enemy.centerx - 8, enemy.y + 12), 4)
            pygame.draw.circle(screen, WHITE, (enemy.centerx + 8, enemy.y + 12), 4)

        # Score and lives
        screen.blit(font.render("Score: " + str(score), True, WHITE), (10, 10))
        screen.blit(font.render("Lives: " + str(lives), True, WHITE), (470, 10))

        # Game over
        if lives <= 0:
            screen.blit(font.render("GAME OVER", True, RED), (210, 300))
            screen.blit(font.render("Press R to Restart", True, WHITE), (170, 350))
            pygame.display.update()

            waiting = True
            while waiting:
                for event in pygame.event.get():
                    if event.type == pygame.QUIT:
                        pygame.quit()
                        return
                    if event.type == pygame.KEYDOWN:
                        if event.key == pygame.K_r:
                            game()  # Recursion: restart game
                            return
                        if event.key == pygame.K_ESCAPE:
                            pygame.quit()
                            return
            return

        pygame.display.update()
        clock.tick(60)

game()
pygame.quit()
