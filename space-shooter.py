import pygame
import sys
import random

# Initialize Pygame
pygame.init()

# Load and play background music
pygame.mixer.music.load('music.wav')
pygame.mixer.music.play(-1)  # -1 means the music will loop indefinitely

# Set screen dimensions
screen_width = 800
screen_height = 600
screen = pygame.display.set_mode((screen_width, screen_height))

# Set screen title
pygame.display.set_caption("Space Shooter")

# Colors
BLACK = (0, 0, 0)
WHITE = (255, 255, 255)
RED = (255, 0, 0)
GREEN = (0, 255, 0)

# Spaceship settings
ship_width = 50
ship_height = 30
ship_x = screen_width // 2 - ship_width // 2
ship_y = screen_height - ship_height - 10
ship_speed = 5

# Bullet settings
bullet_width = 5
bullet_height = 10
bullet_speed = 9
bullets = []

# Enemy settings
enemy_width = 50
enemy_height = 30
enemy_speed = 4
enemies = []
for i in range(10):  # Increased number of enemies
    enemy_x = random.randint(0, screen_width - enemy_width)
    enemy_y = random.randint(-300, -50)
    enemies.append([enemy_x, enemy_y])

# Player lives
player_lives = 3

# Score
score = 0

# Clock/FPS settings
clock = pygame.time.Clock()
FPS = 75

# Main game loop
running = True

while running:
    # Fill the screen with black (background)
    screen.fill(BLACK)

    # Handle events
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_SPACE:
                # Create a bullet
                bullet_x = ship_x + ship_width // 2 - bullet_width // 2
                bullet_y = ship_y
                bullets.append([bullet_x, bullet_y])

    # Handle key presses
    keys = pygame.key.get_pressed()
    if keys[pygame.K_LEFT] and ship_x > 0:
        ship_x -= ship_speed
    if keys[pygame.K_RIGHT] and ship_x < screen_width - ship_width:
        ship_x += ship_speed

    # Move bullets
    for bullet in bullets:
        bullet[1] -= bullet_speed
        if bullet[1] < 0:
            bullets.remove(bullet)

    # Move enemies
    for enemy in enemies:
        enemy[1] += enemy_speed
        if enemy[1] > screen_height:
            enemy[0] = random.randint(0, screen_width - enemy_width)
            enemy[1] = random.randint(-300, -50)

    # Check for collisions (bullet and enemy)
    for bullet in bullets:
        for enemy in enemies:
            if (enemy[0] < bullet[0] < enemy[0] + enemy_width or enemy[0] < bullet[0] + bullet_width < enemy[0] + enemy_width) and (enemy[1] < bullet[1] < enemy[1] + enemy_height):
                bullets.remove(bullet)
                enemies.remove(enemy)
                score += 10
                break

    # Check for collisions (enemy and spaceship)
    for enemy in enemies:
        if (enemy[0] < ship_x < enemy[0] + enemy_width or enemy[0] < ship_x + ship_width < enemy[0] + enemy_width) and (enemy[1] + enemy_height > ship_y):
            enemies.remove(enemy)
            player_lives -= 1
            score -= 40
            if player_lives == 0:
                running = False
                game_over = True

    # Check if all enemies are destroyed
    if not enemies:
        running = False
        game_over = True

    # Draw spaceship
    pygame.draw.rect(screen, WHITE, (ship_x, ship_y, ship_width, ship_height))

    # Draw bullets
    for bullet in bullets:
        pygame.draw.rect(screen, WHITE, (bullet[0], bullet[1], bullet_width, bullet_height))

    # Draw enemies
    for enemy in enemies:
        pygame.draw.rect(screen, RED, (enemy[0], enemy[1], enemy_width, enemy_height))

    # Draw lives on screen
    lives_text = pygame.font.SysFont(None, 36).render(f'Lives: {player_lives}', True, GREEN)
    screen.blit(lives_text, (10, 10))

    # Draw score on screen
    score_text = pygame.font.SysFont(None, 36).render(f'Score: {score}', True, GREEN)
    screen.blit(score_text, (screen_width - 150, 10))

    # Update the screen
    pygame.display.flip()

    # FPS control
    clock.tick(FPS)

if player_lives > 0:
    # Load and play lose sound
    pygame.mixer.music.stop()
    pygame.mixer.Sound('lose.wav').play()
else:
    # Load and play win sound
    pygame.mixer.music.stop()
    pygame.mixer.Sound('win.wav').play()

# Game over screen
screen.fill(BLACK)
game_over_text = pygame.font.SysFont(None, 72).render('Game Over!', True, RED)
text_rect = game_over_text.get_rect(center=(screen_width // 2, screen_height // 2 - 60))
screen.blit(game_over_text, text_rect)

# Display final score
game_score_text = pygame.font.SysFont(None, 48).render(f'Your score: {score}', True, WHITE)
score_rect = game_score_text.get_rect(center=(screen_width // 2, screen_height // 2))
screen.blit(game_score_text, score_rect)

if player_lives > 0:
    # Display win message
    win_text = pygame.font.SysFont(None, 48).render('You won!', True, GREEN)
    win_rect = win_text.get_rect(center=(screen_width // 2, screen_height // 2 + 60))
    screen.blit(win_text, win_rect)
else:
    # Display lose message
    lose_text = pygame.font.SysFont(None, 48).render('You lost!', True, RED)
    lose_rect = lose_text.get_rect(center=(screen_width // 2, screen_height // 2 + 60))
    screen.blit(lose_text, lose_rect)

pygame.display.flip()

# Keep the game over screen displayed until the user decides to quit
while game_over:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            pygame.quit()
            sys.exit()
