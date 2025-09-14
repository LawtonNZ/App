import pygame
import random
import sys

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

# Bird settings
bird_x = 50
bird_y = HEIGHT // 2
bird_radius = 20  # Add bird radius for collision and drawing
gravity = 0.5
bird_velocity = 0
jump_strength = -8

# Pipe settings
pipe_width = 70
pipe_gap = 150
pipes = []
pipe_speed = 3

# Power-up settings
POWERUP_TYPES = ['shield', 'double_points', 'jump_boost']
powerups = []
powerup_radius = 15
powerup_duration = 180  # frames (~3 seconds)
active_powerup = None
powerup_timer = 0

# Score
score = 0
font = pygame.font.SysFont("Arial", 30)

def draw_bird(x, y):
    pygame.draw.circle(screen, BLACK, (x, int(y)), bird_radius)

def draw_pipes(pipes):
    for pipe in pipes:
        pygame.draw.rect(screen, GREEN, pipe[0])  # top pipe
        pygame.draw.rect(screen, GREEN, pipe[1])  # bottom pipe

def check_collision(bird_y, pipes):
    if bird_y - bird_radius <= 0 or bird_y + bird_radius >= HEIGHT:
        return True
    for pipe in pipes:
        if pipe[0].colliderect((bird_x - bird_radius, bird_y - bird_radius, bird_radius*2, bird_radius*2)) or \
           pipe[1].colliderect((bird_x - bird_radius, bird_y - bird_radius, bird_radius*2, bird_radius*2)):
            return True
    return False

def show_score(score):
    text = font.render(f"Score: {score}", True, BLACK)
    screen.blit(text, (10, 10))

# Game loop
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
                bird_velocity = jump_strength if active_powerup != 'jump_boost' else jump_strength * 1.5

    # Bird movement
    bird_velocity += gravity
    bird_y += bird_velocity

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
        powerups.append({'type': powerup_type, 'rect': pygame.Rect(WIDTH, powerup_y, powerup_radius*2, powerup_radius*2)})

    # Move pipes and power-ups
    new_pipes = []
    for pipe in pipes:
        top, bottom = pipe
        top.x -= pipe_speed
        bottom.x -= pipe_speed
        if top.x + pipe_width > 0:
            new_pipes.append((top, bottom))
        else:
            score += 2 if active_powerup == 'double_points' else 1
    pipes = new_pipes

    new_powerups = []
    for p in powerups:
        p['rect'].x -= pipe_speed
        if p['rect'].x + powerup_radius*2 > 0:
            new_powerups.append(p)
    powerups = new_powerups

    # Draw
    draw_bird(bird_x, bird_y)
    draw_pipes(pipes)
    for p in powerups:
        color = (255, 215, 0) if p['type'] == 'double_points' else (0, 255, 255) if p['type'] == 'shield' else (255, 0, 255)
        pygame.draw.circle(screen, color, (p['rect'].x + powerup_radius, p['rect'].y + powerup_radius), powerup_radius)
    show_score(score)
    if active_powerup:
        effect_text = font.render(f"Powerup: {active_powerup}", True, (255,0,0))
        screen.blit(effect_text, (10, 50))

    # Power-up collision
    if not active_powerup:
        for p in powerups:
            bird_rect = pygame.Rect(bird_x - bird_radius, bird_y - bird_radius, bird_radius*2, bird_radius*2)
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
        if active_powerup != 'shield' and check_collision(bird_y, pipes):
            # Write score to file before closing
            with open("score.txt", "w") as f:
                f.write(str(score))
            pygame.quit()
            sys.exit()

    # Update display
    pygame.display.flip()
    clock.tick(FPS)
