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
bird_radius = 20
gravity = 0.5
bird_velocity = 0
jump_strength = -8

# Pipe settings
pipe_width = 70
pipe_gap = 150
pipes = []
pipe_speed = 3

# Power-up settings
POWERUP_TYPES = ['shield', 'double_points']
powerups = []
powerup_radius = 15
powerup_duration = 180  # frames (~3 seconds)
active_powerup = None
powerup_timer = 0

# Score
score = 0
font = pygame.font.SysFont("Arial", 30)
game_over_font = pygame.font.SysFont("Arial", 24)  # 小一号的字体

# Game state
game_over = False

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

def reset_game():
    global bird_y, bird_velocity, pipes, score, active_powerup, powerups, frame, game_over
    bird_y = HEIGHT // 2
    bird_velocity = 0
    pipes = []
    score = 0
    active_powerup = None
    powerups = []
    frame = 0
    game_over = False

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
            if event.key == pygame.K_SPACE and not game_over:
                bird_velocity = jump_strength
            if game_over and event.key == pygame.K_r:
                reset_game()

    if not game_over:
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

        # Move pipes
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

        # Move powerups
        new_powerups = []
        for p in powerups:
            p['rect'].x -= pipe_speed
            if p['rect'].x + powerup_radius*2 > 0:
                new_powerups.append(p)
        powerups = new_powerups

        # Collision
        if active_powerup != 'shield' and check_collision(bird_y, pipes):
            game_over = True

    # Draw everything
    draw_bird(bird_x, bird_y)
    draw_pipes(pipes)
    for p in powerups:
        color = (255, 215, 0) if p['type'] == 'double_points' else (0, 255, 255)
        pygame.draw.circle(screen, color, (p['rect'].x + powerup_radius, p['rect'].y + powerup_radius), powerup_radius)
    show_score(score)

    # Game Over text
    if game_over:
        over_text = game_over_font.render("Game Over! Press R to restart", True, (255, 0, 0))
        screen.blit(over_text, (
            WIDTH // 2 - over_text.get_width() // 2,
            HEIGHT // 2 - over_text.get_height() // 2
        ))

    # Update display
    pygame.display.flip()
    clock.tick(FPS)
