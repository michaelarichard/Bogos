import pygame

import pygame
import random

# Initialize Pygame
pygame.init()
pygame.font.init() # Initialize the font module

# Screen dimensions
SCREEN_WIDTH = 800
SCREEN_HEIGHT = 600
screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
pygame.display.set_caption("Space Invaders")

# Colors
WHITE = (255, 255, 255)
BLACK = (0, 0, 0)
RED = (255, 0, 0)
GREEN = (0, 255, 0)
YELLOW = (255, 255, 0) # For score text

# Score
score = 0
score_font_size = 30
score_font = None # Will be initialized after pygame.init()
try:
    score_font = pygame.font.SysFont('arial', score_font_size)
except Exception as e:
    print(f"Could not load system font 'arial', using default font: {e}")
    score_font = pygame.font.Font(None, score_font_size + 10) # Pygame's default font, adjust size if needed

# Game Over properties
game_over_font_size = 72
game_over_font = None
try:
    game_over_font = pygame.font.SysFont('arial', game_over_font_size)
except Exception as e:
    print(f"Could not load system font 'arial' for game over, using default font: {e}")
    game_over_font = pygame.font.Font(None, game_over_font_size + 10)

final_score_font_size = 48
final_score_font = None
try:
    final_score_font = pygame.font.SysFont('arial', final_score_font_size)
except Exception as e:
    print(f"Could not load system font 'arial' for final score, using default font: {e}")
    final_score_font = pygame.font.Font(None, final_score_font_size + 10)

# Game state
game_state = "playing" # Can be "playing" or "game_over"

# Player properties
player_width = 50
player_height = 50
player_x = (SCREEN_WIDTH - player_width) // 2
player_y = SCREEN_HEIGHT - player_height - 10
player_speed = 5

# Bullet properties
bullet_width = 5
bullet_height = 15
bullet_speed = 10
bullet_color = WHITE
bullets = []

# Enemy bullet properties
enemy_bullet_width = 5
enemy_bullet_height = 15
enemy_bullet_speed = 5
enemy_bullet_color = (255, 100, 0) # Orange-ish Red
enemy_bullets = []
enemy_shoot_chance = 0.001 # Chance for an enemy to shoot per frame (e.g., 0.1%)

# Enemy properties
enemy_width = 50
enemy_height = 50
enemy_initial_speed_x = 1 # Horizontal speed
enemy_speed_x = enemy_initial_speed_x
enemy_speed_y = 5 # How much they drop when hitting the edge
enemies = []
enemy_rows = 3
enemy_cols = 10
enemy_padding = 10 # Padding between enemies
enemy_offset_x = 50 # Offset from the left edge of the screen
enemy_offset_y = 50 # Offset from the top edge of the screen

for row in range(enemy_rows):
    for col in range(enemy_cols):
        enemy_x = enemy_offset_x + col * (enemy_width + enemy_padding)
        enemy_y = enemy_offset_y + row * (enemy_height + enemy_padding)
        enemies.append(pygame.Rect(enemy_x, enemy_y, enemy_width, enemy_height))

# Game loop
running = True
clock = pygame.time.Clock()

while running:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
        if game_state == "playing": # Only allow shooting if playing
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_SPACE:
                    # Create a new bullet
                    bullet_x = player_x + player_width // 2 - bullet_width // 2
                    bullet_y = player_y
                    bullets.append(pygame.Rect(bullet_x, bullet_y, bullet_width, bullet_height))

    if game_state == "playing":
        # Player movement
        keys = pygame.key.get_pressed()
        if keys[pygame.K_LEFT] and player_x > 0:
            player_x -= player_speed
        if keys[pygame.K_RIGHT] and player_x < SCREEN_WIDTH - player_width:
            player_x += player_speed

        # Update player rectangle for current frame
        player_rect = pygame.Rect(player_x, player_y, player_width, player_height)

        # Enemy movement
        move_down = False
        for enemy in enemies:
            enemy.x += enemy_speed_x

            # Enemy shooting logic
            if random.random() < enemy_shoot_chance and len(enemies) > 0:
                enemy_bullet_x = enemy.centerx - enemy_bullet_width // 2
                enemy_bullet_y = enemy.bottom
                enemy_bullets.append(pygame.Rect(enemy_bullet_x, enemy_bullet_y, enemy_bullet_width, enemy_bullet_height))
            
            # Check if enemy reached bottom
            if enemy.bottom >= SCREEN_HEIGHT:
                game_state = "game_over"
                # No break here, let all enemies move for the frame, then game over screen takes over

        # Check if enemies hit the screen boundaries
        if game_state == "playing": # Only do this if still playing
            for enemy in enemies:
                if enemy.right > SCREEN_WIDTH or enemy.left < 0:
                    move_down = True
                    break 

            if move_down:
                enemy_speed_x *= -1 
                for enemy in enemies:
                    enemy.y += enemy_speed_y 
                    if enemy.right > SCREEN_WIDTH:
                        enemy.right = SCREEN_WIDTH
                    if enemy.left < 0:
                        enemy.left = 0
                    # Check again if enemy reached bottom after being moved down
                    if enemy.bottom >= SCREEN_HEIGHT:
                        game_state = "game_over"


        # Player Bullet movement
        for bullet in bullets[:]: 
            bullet.y -= bullet_speed
            if bullet.bottom < 0:
                bullets.remove(bullet)
                continue 

            for enemy in enemies[:]: 
                if bullet.colliderect(enemy):
                    bullets.remove(bullet)
                    enemies.remove(enemy)
                    score += 10 
                    break 

        # Enemy Bullet movement
        for e_bullet in enemy_bullets[:]:
            e_bullet.y += enemy_bullet_speed
            if e_bullet.top > SCREEN_HEIGHT:
                enemy_bullets.remove(e_bullet)
                continue

            if e_bullet.colliderect(player_rect):
                game_state = "game_over" # Set game state to game_over
                # enemy_bullets.remove(e_bullet) # Optional: remove the bullet that hit
                break 


    # Drawing
    screen.fill(BLACK)

    if game_state == "playing":
        # Draw player
        pygame.draw.rect(screen, GREEN, player_rect)

        # Draw enemies
        for enemy in enemies:
            pygame.draw.rect(screen, RED, enemy)

        # Draw bullets
        for bullet in bullets:
            pygame.draw.rect(screen, bullet_color, bullet)

        # Draw enemy bullets
        for e_bullet in enemy_bullets:
            pygame.draw.rect(screen, enemy_bullet_color, e_bullet)

        # Draw score
        if score_font:
            score_text_surface = score_font.render(f"Score: {score}", True, YELLOW)
            screen.blit(score_text_surface, (10, 10))

    elif game_state == "game_over":
        # Display Game Over message and final score
        if game_over_font:
            game_over_text = game_over_font.render("GAME OVER", True, RED)
            text_rect = game_over_text.get_rect(center=(SCREEN_WIDTH // 2, SCREEN_HEIGHT // 2 - 50))
            screen.blit(game_over_text, text_rect)
        
        if final_score_font:
            final_score_text = final_score_font.render(f"Final Score: {score}", True, YELLOW)
            score_rect = final_score_text.get_rect(center=(SCREEN_WIDTH // 2, SCREEN_HEIGHT // 2 + 50))
            screen.blit(final_score_text, score_rect)

    pygame.display.flip()

    # Control frame rate
    clock.tick(60)

pygame.font.quit()
pygame.quit()
