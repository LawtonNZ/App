import pygame
import random

# Colors
DAY_COLOR = (135, 206, 235)      # Sky blue (day)
SUNSET_COLOR = (252, 100, 45)    # Orange-ish (sunset)
NIGHT_COLOR = (15, 15, 40)       # Dark blue (night)
RAIN_COLOR = (100, 100, 130)     # Greyish (rain)

WEATHER_STATES = ['day', 'sunset', 'night', 'rain']

class Cloud:
    def __init__(self, x, y, scale, speed):
        self.x = x
        self.y = y
        self.scale = scale
        self.speed = speed
        self.width = 60 * scale
        self.height = 40 * scale

    def update(self):
        self.x -= self.speed
        if self.x < -self.width:
            self.x = 400 + random.randint(10, 100)  # Screen width hardcoded here; change if needed
            self.y = random.randint(20, 150)

    def draw(self, surface, color):
        pygame.draw.ellipse(surface, color, (self.x, self.y, self.width, self.height))
        pygame.draw.ellipse(surface, color, (self.x + self.width * 0.3, self.y - self.height*0.3, self.width*0.7, self.height))
        pygame.draw.ellipse(surface, color, (self.x + self.width * 0.5, self.y, self.width*0.5, self.height*0.7))

class Raindrop:
    def __init__(self, screen_width, screen_height):
        self.screen_width = screen_width
        self.screen_height = screen_height
        self.reset()

    def reset(self):
        self.x = random.randint(0, self.screen_width)
        self.y = random.randint(-self.screen_height, 0)
        self.length = random.randint(10, 20)
        self.speed = random.uniform(4, 7)

    def update(self):
        self.y += self.speed
        if self.y > self.screen_height:
            self.reset()

    def draw(self, surface):
        end_y = self.y + self.length
        pygame.draw.line(surface, RAIN_COLOR, (self.x, self.y), (self.x, end_y), 1)

def lerp_color(color1, color2, t):
    """Linearly interpolate between two colors"""
    return tuple(int(c1 + (c2 - c1) * t) for c1, c2 in zip(color1, color2))

class WeatherSystem:
    def __init__(self, screen_width, screen_height, fps, cycle_seconds=30):
        self.screen_width = screen_width
        self.screen_height = screen_height
        self.fps = fps
        self.weather_duration = fps * cycle_seconds
        self.weather_timer = 0
        self.weather_index = 0
        self.current_weather = WEATHER_STATES[0]
        self.next_weather = WEATHER_STATES[1]
        self.t = 0

        # Clouds
        self.clouds_far = [Cloud(random.randint(0, screen_width), random.randint(20, 150), 0.6, 0.3) for _ in range(5)]
        self.clouds_near = [Cloud(random.randint(0, screen_width), random.randint(50, 180), 1.0, 0.6) for _ in range(7)]

        # Raindrops
        self.raindrops = [Raindrop(screen_width, screen_height) for _ in range(100)]

    def update(self):
        self.weather_timer += 1
        if self.weather_timer >= self.weather_duration:
            self.weather_timer = 0
            self.weather_index = (self.weather_index + 1) % len(WEATHER_STATES)
        self.current_weather = WEATHER_STATES[self.weather_index]
        self.next_weather = WEATHER_STATES[(self.weather_index + 1) % len(WEATHER_STATES)]
        self.t = self.weather_timer / self.weather_duration

        # Update clouds if they should be visible
        if self.should_draw_clouds():
            for cloud in self.clouds_far:
                cloud.update()
            for cloud in self.clouds_near:
                cloud.update()

        # Update rain if needed
        if self.should_draw_rain():
            for drop in self.raindrops:
                drop.update()

    def get_background_color(self):
        colors = {
            'day': DAY_COLOR,
            'sunset': SUNSET_COLOR,
            'night': NIGHT_COLOR,
            'rain': (100, 100, 120)
        }
        return lerp_color(colors[self.current_weather], colors[self.next_weather], self.t)

    def should_draw_clouds(self):
        # Clouds visible during day, sunset, and rain (dimmed), none at night
        if self.current_weather == 'day':
            return True
        if self.current_weather == 'sunset':
            return True
        if self.current_weather == 'rain':
            return True
        return False

    def get_cloud_color(self):
        if self.current_weather == 'day' or (self.current_weather == 'rain' and self.t < 0.5):
            return (255, 255, 255)  # white clouds
        elif self.current_weather == 'sunset':
            return lerp_color((255, 165, 100), (180, 180, 180), self.t)
        elif self.current_weather == 'rain':
            return (180, 180, 180)
        else:
            return None

    def should_draw_rain(self):
        # Draw rain if rain weather or transitioning close to rain
        if self.current_weather == 'rain':
            return True
        if self.current_weather == 'sunset' and self.next_weather == 'rain' and self.t > 0.7:
            return True
        if self.current_weather == 'rain' and self.next_weather == 'night' and self.t < 0.3:
            return True
        return False

    def draw(self, surface):
        cloud_color = self.get_cloud_color()
        if cloud_color and self.should_draw_clouds():
            for cloud in self.clouds_far:
                cloud.draw(surface, cloud_color)
            for cloud in self.clouds_near:
                cloud.draw(surface, cloud_color)

        if self.should_draw_rain():
            for drop in self.raindrops:
                drop.draw(surface)
