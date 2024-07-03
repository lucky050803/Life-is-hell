import pygame
import math

SCREEN_WIDTH = 800
SCREEN_HEIGHT = 600

class Bullet:
    def __init__(self, start_pos, target_pos, color=(255, 255, 255)):
        self.image = pygame.Surface((10, 10))
        self.image.fill(color)
        self.rect = self.image.get_rect(center=start_pos)
        self.speed = 10
        self.velocity = self.calculate_velocity(start_pos, target_pos)

    def calculate_velocity(self, start_pos, target_pos):
        angle = math.atan2(target_pos[1] - start_pos[1], target_pos[0] - start_pos[0])
        return (self.speed * math.cos(angle), self.speed * math.sin(angle))
    
    def update(self):
        self.rect.x += self.velocity[0]
        self.rect.y += self.velocity[1]

    def draw(self, screen):
        screen.blit(self.image, self.rect.topleft)

class ReboundingBullet(Bullet):
    def update(self):
        self.rect.x += self.velocity[0]
        self.rect.y += self.velocity[1]

        if self.rect.left <= 0 or self.rect.right >= SCREEN_WIDTH:
            self.velocity = (-self.velocity[0], self.velocity[1])
        if self.rect.top <= 0 or self.rect.bottom >= SCREEN_HEIGHT:
            self.velocity = (self.velocity[0], -self.velocity[1])

class TriangleBullet(Bullet):
    def __init__(self, start_pos, target_pos, color=(0, 0, 255)):
        self.image = pygame.Surface((20, 20), pygame.SRCALPHA)
        pygame.draw.polygon(self.image, color, [(10, 0), (0, 20), (20, 20)])  # Dessiner un triangle
        self.rect = self.image.get_rect(center=start_pos)
        self.speed = 5
        self.velocity = self.calculate_velocity(start_pos, target_pos)
        self.returning = False
        self.start_pos = start_pos

    def update(self):
        self.rect.x += self.velocity[0]
        self.rect.y += self.velocity[1]

        distance_to_target = math.hypot(self.rect.centerx - self.start_pos[0], self.rect.centery - self.start_pos[1])
        if distance_to_target > 200:
            self.returning = True
            self.velocity = self.calculate_velocity(self.rect.center, self.start_pos)
        
        if self.returning:
            if self.rect.colliderect(pygame.Rect(self.start_pos[0] - 5, self.start_pos[1] - 5, 10, 10)):
                self.rect.center = self.start_pos
                self.velocity = (0, 0)
