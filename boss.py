import pygame
import random
import math
from bullet import Bullet, ReboundingBullet, TriangleBullet
from bullet import Bullet, ExplodingBullet, DamageLineBullet
class Cerberus:
    def __init__(self, x, y):
        self.image = pygame.Surface((60, 60), pygame.SRCALPHA)  # Réduire la taille de Cerberus
        pygame.draw.polygon(self.image, (255, 0, 0), [(30, 0), (0, 60), (60, 60)])  # Dessiner un triangle pour Cerberus
        self.rect = self.image.get_rect(center=(x, y))
        self.health = 500  # Augmentation des PV
        self.max_health = 500
        self.move_timer = 0
        self.move_interval = 60  # Réduire l'intervalle de mouvement
        self.target_pos = self.get_new_position()
        self.attack_timer = 0
        self.attack_interval = 90  # Réduire l'intervalle d'attaque
        self.attack_types = [self.explode, self.shoot_rebounding_bullets, self.shoot_triangle_bullets]
        self.phase_two = False
        self.dying = False
        self.fade_alpha = 255

    def get_new_position(self):
        return (random.randint(100, 700), random.randint(100, 500))
    
    def explode(self):
        bullets = []
        for angle in range(0, 360, 30):  # Crée des projectiles dans toutes les directions
            bullets.append(Bullet(self.rect.center, (
                self.rect.centerx + 100 * math.cos(math.radians(angle)), 
                self.rect.centery + 100 * math.sin(math.radians(angle))
            ), color=(0, 0, 255)))  # Les projectiles sont bleus
        return bullets
    
    def shoot_rebounding_bullets(self):
        bullets = []
        for _ in range(8):  # 8 balles qui rebondissent
            target_pos = self.get_new_position()
            bullets.append(ReboundingBullet(self.rect.center, target_pos, color=(0, 0, 255)))  # Les projectiles sont bleus
        return bullets

    def shoot_triangle_bullets(self):
        bullets = []
        for angle in range(0, 360, 45):  # Crée des triangles dans toutes les directions
            bullets.append(TriangleBullet(self.rect.center, (
                self.rect.centerx + 200 * math.cos(math.radians(angle)), 
                self.rect.centery + 200 * math.sin(math.radians(angle))
            ), color=(0, 0, 255)))  # Les triangles sont bleus
        return bullets

    def phase_two_attack(self):
        bullets = []
        for angle in range(0, 360, 15):  # Crée des projectiles dans toutes les directions plus fréquents
            bullets.append(Bullet(self.rect.center, (
                self.rect.centerx + 150 * math.cos(math.radians(angle)), 
                self.rect.centery + 150 * math.sin(math.radians(angle))
            ), color=(0, 0, 255)))  # Les projectiles sont bleus
        return bullets

    def start_dying(self):
        self.dying = True

    def update(self):
        if self.dying:
            self.fade_alpha -= 5
            self.image.set_alpha(self.fade_alpha)
            if self.fade_alpha <= 0:
                self.fade_alpha = 0
            return []

        self.move_timer += 1
        self.attack_timer += 1

        if self.health <= 250 and not self.phase_two:  # Vérifie si Cerberus est à la moitié de sa vie
            self.phase_two = True
            self.attack_interval = 60  # Réduit encore plus l'intervalle d'attaque

        if self.move_timer >= self.move_interval:
            self.move_timer = 0
            self.target_pos = self.get_new_position()
            return self.explode()
        
        if self.rect.center != self.target_pos:
            self.rect = self.rect.move(
                (self.target_pos[0] - self.rect.centerx) // self.move_interval, 
                (self.target_pos[1] - self.rect.centery) // self.move_interval
            )

        if self.attack_timer >= self.attack_interval:
            self.attack_timer = 0
            if self.phase_two:
                return self.phase_two_attack()
            return random.choice(self.attack_types)()
        
        return []

    def draw(self, screen):
        screen.blit(self.image, self.rect.topleft)



class Prometheus:
    def __init__(self, x, y):
        self.rect = pygame.Rect(x - 30, y - 30, 60, 60)
        self.health = 600
        self.max_health = 600
        self.move_timer = 0
        self.move_interval = 50
        self.target_pos = self.get_new_position()
        self.attack_timer = 0
        self.attack_interval = 100
        self.phase = 1
        self.phase_health_thresholds = [400, 200]
        self.dying = False
        self.fade_alpha = 255
        self.color = (255, 0, 0)
        self.line_timers = []
        self.line_duration = 500

    def get_new_position(self):
        return random.randint(50, 550), random.randint(50, 550)

    def fire_exploding_bullets(self):
        bullets = []
        for angle in range(0, 360, 45):
            target_x = self.rect.centerx + 150 * math.cos(math.radians(angle))
            target_y = self.rect.centery + 150 * math.sin(math.radians(angle))
            bullets.append(ExplodingBullet(self.rect.center, (target_x, target_y)))
        return bullets

    def place_damage_line(self):
        if len(self.line_timers) < self.phase:
            if self.phase == 1 or (self.phase == 3 and random.choice([True, False])):
                # Vertical line
                start_x = random.randint(50, 550)
                bullets = [DamageLineBullet((start_x, 0), (start_x, 600), 180)]
            else:
                # Horizontal line
                start_y = random.randint(50, 550)
                bullets = [DamageLineBullet((0, start_y), (600, start_y), 180)]
            self.line_timers.append(180)
            return bullets
        return []

    def start_dying(self):
        self.dying = True

    def update(self):
        if self.dying:
            self.fade_alpha -= 5
            if self.fade_alpha < 0:
                self.fade_alpha = 0
            return []

        self.move_timer += 1
        self.attack_timer += 1
        self.line_timers = [timer - 1 for timer in self.line_timers if timer > 0]

        if self.health <= self.phase_health_thresholds[2 - self.phase] and self.phase < 3:
            self.phase += 1
            self.attack_interval -= 20  # Increase attack frequency
            self.color = (255 // self.phase, 0, 255 // self.phase)

        if self.move_timer >= self.move_interval:
            self.move_timer = 0
            self.target_pos = self.get_new_position()

        if self.rect.center != self.target_pos:
            self.rect = self.rect.move(
                (self.target_pos[0] - self.rect.centerx) // self.move_interval,
                (self.target_pos[1] - self.rect.centery) // self.move_interval
            )

        if self.attack_timer >= self.attack_interval:
            self.attack_timer = 0
            if random.random() < 0.5:
                return self.fire_exploding_bullets()
            return self.place_damage_line()

        return []

    def draw(self, screen):
        pygame.draw.circle(screen, self.color, self.rect.center, 30)

