import pygame

class HealthItem:
    def __init__(self, x, y):
        self.image = pygame.Surface((15, 15))
        self.image.fill((0, 255, 0))  # Les objets de soin sont verts
        self.rect = self.image.get_rect(center=(x, y))

    def draw(self, screen):
        screen.blit(self.image, self.rect.topleft)
