import pygame
import random
import string

class BackgroundText:
    def __init__(self, screen_width, screen_height, font_path):
        self.screen_width = screen_width
        self.screen_height = screen_height
        self.font = pygame.freetype.Font(font_path, 30)
        self.text = self.generate_random_text()
        self.color = self.generate_random_color()
        self.alpha = 255
        self.rect = self.font.get_rect(self.text)
        self.rect.topleft = (random.randint(0, self.screen_width - self.rect.width), random.randint(0, self.screen_height - self.rect.height))
        self.speed = random.randint(1, 3)
        self.direction = random.choice(['left', 'right', 'up', 'down'])

    def generate_random_text(self):
        return ''.join(random.choices(string.ascii_uppercase + string.digits, k=5))

    def generate_random_color(self):
        return (random.randint(0, 255), random.randint(0, 255), random.randint(0, 255))

    def update(self):
        if self.direction == 'left':
            self.rect.x -= self.speed
        elif self.direction == 'right':
            self.rect.x += self.speed
        elif self.direction == 'up':
            self.rect.y -= self.speed
        elif self.direction == 'down':
            self.rect.y += self.speed

        if self.alpha > 0:
            self.alpha -= 5
        else:
            self.alpha = 0

    def draw(self, screen):
        text_surface, _ = self.font.render(self.text, self.color)
        text_surface.set_alpha(self.alpha)
        screen.blit(text_surface, self.rect.topleft)

    def is_faded(self):
        return self.alpha == 0
