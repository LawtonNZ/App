import pygame
import random
import sys
import os
from weather import WeatherSystem  # Import the weather module

# Initialize pygame
pygame.init()

# Screen settings
WIDTH, HEIGHT = 400, 600
screen = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("Flappy Bird")

# Colors
WHITE = (255, 255, 255)
BLACK = (0, 0, 0)
GREEN = (0, 200, 0)

# Clock
clock = pygame.time.Clock()
FPS = 60

# Fonts
font = pygame.font.SysFont("Arial", 30)

# Initialize Weather System with a 30-second cycle
weather = WeatherSystem(WIDTH, HEIGHT, FPS, cycle_seconds=30)

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

running = True
frame = 0
while running:
    # Update weather system
    weather.update()

    # Fill background with dynamic weather color
    screen.fill(weather.get_background_color())

    # Draw weather effects (clouds, rain)
    weather.draw(screen)

    # Event loop
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            pygame.quit()
            sys.exit()
        if event.type == pygame.KEYDOWN:


    # Draw everything
    draw_bird(bird_x, bird_y)
    draw_pipes(pipes)
    for p in powerups:


    # Update display
    pygame.display.flip()
    clock.tick(FPS)
