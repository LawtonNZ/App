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
bird_radius = 15
gravity = 0.5
bird_velocity = 0
jump_strength = -8

# Pipe settings
pipe_width = 70
pipe_gap = 150
pipes = []
pipe_speed = 3

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

# Score saving logic
def save_score(new_score, filename="scores.txt", top_n=5):
    try:
        with open(filename, "r") as f:
            scores = [int(line.strip()) for line in f if line.strip().isdigit()]
    except FileNotFoundError:
        scores = []
    scores.append(new_score)
    scores = sorted(scores, reverse=True)[:top_n]
    with open(filename, "w") as f:
        for s in scores:
            f.write(f"{s}\n")
 
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
                bird_velocity = jump_strength

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

    new_pipes = []
    for pipe in pipes:
        top, bottom = pipe
        top.x -= pipe_speed
        bottom.x -= pipe_speed
        if top.x + pipe_width > 0:
            new_pipes.append((top, bottom))
        else:
            score += 1
    pipes = new_pipes

    # Draw
    draw_bird(bird_x, bird_y)
    draw_pipes(pipes)
    show_score(score)

    # Collision
    if check_collision(bird_y, pipes):
        save_score(score)
        pygame.quit()
        sys.exit()

    # Update display
    pygame.display.flip()
    clock.tick(FPS)
