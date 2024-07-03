import pygame
import math
from bullet import Bullet

class Player:
    def __init__(self, x, y):
        self.image = pygame.Surface((20, 20), pygame.SRCALPHA)  # Réduire la taille du joueur et ajouter la transparence
        pygame.draw.circle(self.image, (0, 255, 0), (10, 10), 10)  # Dessiner un cercle vert pour le joueur
        self.rect = self.image.get_rect(center=(x, y))
        self.speed = 5
        self.health = 100
    
    def update(self, keys):
        if keys[pygame.K_LEFT] and self.rect.left > 0:
            self.rect.x -= self.speed
        if keys[pygame.K_RIGHT] and self.rect.right < 800:
            self.rect.x += self.speed
        if keys[pygame.K_UP] and self.rect.top > 0:
            self.rect.y -= self.speed
        if keys[pygame.K_DOWN] and self.rect.bottom < 600:
            self.rect.y += self.speed

    def draw(self, screen):
        screen.blit(self.image, self.rect.topleft)

    def shoot(self, target_pos):
        return Bullet(self.rect.center, target_pos)

