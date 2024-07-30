import pygame
import math
from bullet import PlayerBullet

class Player:
    def __init__(self, x, y, stats):
        self.image = pygame.Surface((20, 20), pygame.SRCALPHA)  # Réduire la taille du joueur et ajouter la transparence
        pygame.draw.circle(self.image, (0, 255, 0), (10, 10), 10)  # Dessiner un cercle vert pour le joueur
        self.rect = self.image.get_rect(center=(x, y))
        self.speed = 5
        self.base_health = 100
        self.base_damage = 10
        self.base_projectiles = 1

        self.stats = stats
        self.health = self.base_health + (self.stats['health'] * 20)  # Par exemple, chaque amélioration ajoute 20 HP
        self.damage = self.base_damage + (self.stats['damage'] * 5)  # Chaque amélioration ajoute 5 dégâts
        self.projectiles = self.base_projectiles + self.stats['projectiles']  # Chaque amélioration ajoute un projectile

    def update(self, keys):
        if keys[pygame.K_LEFT] and self.rect.left > 0:
            self.rect.x -= self.speed
        if keys[pygame.K_RIGHT] and self.rect.right < 600:
            self.rect.x += self.speed
        if keys[pygame.K_UP] and self.rect.top > 0:
            self.rect.y -= self.speed
        if keys[pygame.K_DOWN] and self.rect.bottom < 600:
            self.rect.y += self.speed

    def draw(self, screen):
        screen.blit(self.image, self.rect.topleft)

    def shoot(self, target_pos):
        bullets = []
        angle_step = 15  # Définir un angle entre chaque projectile (par exemple 15 degrés)
        start_angle = - (angle_step * (self.projectiles - 1)) / 2  # Centrer les projectiles

        for i in range(self.projectiles):
            angle = math.radians(start_angle + i * angle_step)
            dx = math.cos(angle)
            dy = math.sin(angle)
            new_target_pos = (target_pos[0] + dx * 100, target_pos[1] + dy * 100)  # Ajuster la position cible pour chaque projectile
            bullets.append(PlayerBullet(self.rect.center, new_target_pos))
        return bullets
