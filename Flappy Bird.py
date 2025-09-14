import pygame
import random
import sys
import os

# Initialize pygame
pygame.init()

# Screen settings
WIDTH, HEIGHT = 400, 600
screen = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("Flappy Bird")

# Colors
WHITE = (255, 255, 255)
BLACK = (0, 0, 0)
SKY = (135, 206, 235)
GREEN = (0, 200, 0)

# Clock
clock = pygame.time.Clock()
FPS = 60

# Fonts
font = pygame.font.SysFont("Arial", 30)

# --- Bird sprite ---
bird_file = "bird.png"  # make sure this file is in the same folder
if not os.path.exists(bird_file):
    print(f"ERROR: {bird_file} not found in {os.getcwd()}")
    pygame.quit()
    sys.exit()

bird_img = pygame.image.load(bird_file).convert_alpha()
bird_img = pygame.transform.scale(bird_img, (40, 30))  # resize to fit game
bird_x = 50
bird_y = HEIGHT // 2
bird_velocity = 0
gravity = 0.5
jump_strength = -8

# Pipe settings
pipe_width = 70
pipe_gap = 200
pipes = []
pipe_speed = 3

# Power-up settings

POWERUP_TYPES = ['shield', 'double_points', 'gravity_plus', 'no_points']
NEGATIVE_POWERUPS = ['gravity_plus', 'no_points']

powerups = []
powerup_radius = 15
powerup_duration = 180  # frames (~3 seconds)
active_powerup = None
powerup_timer = 0

# Score
score = 0

# --- Functions ---
def draw_bird(x, y):
    screen.blit(bird_img, (x - bird_img.get_width()//2, y - bird_img.get_height()//2))

def draw_pipes(pipes):
    for pipe in pipes:
        pygame.draw.rect(screen, GREEN, pipe[0])  # top pipe
        pygame.draw.rect(screen, GREEN, pipe[1])  # bottom pipe

def check_collision(bird_rect, pipes):
    if bird_rect.top <= 0 or bird_rect.bottom >= HEIGHT:
        return True
    for pipe in pipes:
        if bird_rect.colliderect(pipe[0]) or bird_rect.colliderect(pipe[1]):
            return True
    return False

def show_score(score):
    text = font.render(f"Score: {score}", True, BLACK)
    screen.blit(text, (10, 10))

# --- Game loop ---
running = True
frame = 0
while running:
    screen.fill(SKY)

    # Event loop
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            pygame.quit()
            sys.exit()
        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_SPACE:
                if active_powerup == 'jump_boost':
                    bird_velocity = jump_strength * 1.5
                else:
                    bird_velocity = jump_strength


    # Bird movement
    current_gravity = gravity * 1.5 if active_powerup == 'gravity_plus' else gravity
    bird_velocity += current_gravity

    bird_y += bird_velocity
    bird_rect = bird_img.get_rect(center=(bird_x, bird_y))

    # Pipes
    frame += 1
    if frame % 90 == 0:
        gap_y = random.randint(100, HEIGHT - 100)
        top_pipe = pygame.Rect(WIDTH, 0, pipe_width, gap_y - pipe_gap//2)
        bottom_pipe = pygame.Rect(WIDTH, gap_y + pipe_gap//2, pipe_width, HEIGHT - gap_y)
        pipes.append((top_pipe, bottom_pipe))

    # Power-up spawn
    if frame % 300 == 0:
        powerup_type = random.choice(POWERUP_TYPES)
        powerup_y = random.randint(100, HEIGHT - 100)
        powerups.append({
            'type': powerup_type,
            'rect': pygame.Rect(WIDTH, powerup_y, powerup_radius*2, powerup_radius*2)
        })

    # Move pipes
    new_pipes = []
    for pipe in pipes:
        top, bottom = pipe
        top.x -= pipe_speed
        bottom.x -= pipe_speed
        if top.x + pipe_width > 0:
            new_pipes.append((top, bottom))
        else:
            if active_powerup == 'no_points':
                score += 0
            elif active_powerup == 'double_points':
                score += 2
            else:
                score += 1
    pipes = new_pipes

    # Move power-ups
    new_powerups = []
    for p in powerups:
        p['rect'].x -= pipe_speed
        if p['rect'].x + powerup_radius*2 > 0:
            new_powerups.append(p)
    powerups = new_powerups

    # Draw everything
    draw_bird(bird_x, bird_y)
    draw_pipes(pipes)
    for p in powerups:
        if p['type'] == 'double_points':
            color = (255, 215, 0)
        elif p['type'] == 'shield':
            color = (0, 255, 255)
        elif p['type'] == 'gravity_plus':
            color = (255, 0, 0)  # Negative powerup: red
        elif p['type'] == 'no_points':
            color = (128, 0, 128)  # Negative powerup: purple
        pygame.draw.circle(screen, color, (p['rect'].x + powerup_radius, p['rect'].y + powerup_radius), powerup_radius)
    show_score(score)
    if active_powerup:
        effect_text = font.render(f"Powerup: {active_powerup}", True, (255,0,0) if active_powerup in NEGATIVE_POWERUPS else (0,128,0))

        screen.blit(effect_text, (10, 50))

    # Power-up collision
    if not active_powerup:
        for p in powerups:
            if p['rect'].colliderect(bird_rect):
                active_powerup = p['type']
                powerup_timer = powerup_duration
                powerups.remove(p)
                break

    # Power-up timer
    if active_powerup:
        powerup_timer -= 1
        if powerup_timer <= 0:
            active_powerup = None

    # Collision
    if active_powerup != 'shield' and check_collision(bird_rect, pipes):
        pygame.quit()
        sys.exit()

    # Update display
    pygame.display.flip()
    clock.tick(FPS)
 
