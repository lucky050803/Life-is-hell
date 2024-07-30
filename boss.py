import pygame
import random
import math
from bullet import *
from bossscreen import *

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
        self.attack_interval = 140  # Réduire l'intervalle d'attaque
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
        self.health = 800
        self.max_health = 800
        self.move_timer = 0
        self.move_interval = 50
        self.target_pos = self.get_new_position()
        self.attack_timer = 0
        self.attack_interval = 70
        self.phase = 1
        self.phase_health_thresholds = [500, 300]
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
    
    def shoot_rebounding_bullets(self):
        bullets = []
        for _ in range(8):  # 8 balles qui rebondissent
            target_pos = self.get_new_position()
            bullets.append(ReboundingBullet(self.rect.center, target_pos, color=(255, 0, 0)))  # Les projectiles sont bleus
        return bullets
    
    
    def place_damage_line(self):
        if len(self.line_timers) < self.phase:
            if self.phase == 1 or (self.phase == 3 and random.choice([True, False])):
                # Vertical line
                start_x = random.randint(1, 5)
                bullets = [DamageLineBullet((start_x*100, 0), (start_x*100, 600), 180)]
            else:
                # Horizontal line
                start_y = random.randint(1, 5)
                bullets = [DamageLineBullet((0, start_y*100), (600, start_y*100), 180)]
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
            test=random.random()
            if  test< 0.1:
                return self.fire_exploding_bullets()
            if test > 0.1 and test < 0.3:
                return self.shoot_rebounding_bullets()
            return self.place_damage_line()

        return []

    def draw(self, screen):
        pygame.draw.circle(screen, self.color, self.rect.center, 30)

class Hades:
    def __init__(self, x, y):
        self.rect = pygame.Rect(x - 30, y - 30, 60, 60)
        self.health = 3000
        self.max_health = 3000
        self.move_timer = 0
        self.move_interval = 60
        self.target_pos = self.get_new_position()
        self.attack_timer = 0
        self.attack_interval = 100
        self.phase = 1
        self.phase_health_thresholds = [3000, 2000, 1000]
        self.dying = False
        self.fade_alpha = 255
        self.color = (255, 69, 0)  # Initial color: orange-red
        self.special_timers = []

    def get_new_position(self):
        return random.randint(50, 550), random.randint(50, 550)

    def summon_fire_circles(self):
        circles = []
        for _ in range(2):
            pos = (random.randint(50, 550), random.randint(50, 550))
            circles.append(DamageCircle(pos, 50, duration=180))  # 3 seconds duration
        return circles
    
    def fire_exploding_bullets(self):
        bullets = []
        for angle in range(0, 360, 45):
            target_x = self.rect.centerx + 150 * math.cos(math.radians(angle))
            target_y = self.rect.centery + 150 * math.sin(math.radians(angle))
            bullets.append(ExplodingBullet(self.rect.center, (target_x, target_y)))
        return bullets
    
    def shoot_rebounding_bullets(self):
        bullets = []
        for _ in range(8):  # 8 balles qui rebondissent
            target_pos = self.get_new_position()
            bullets.append(ReboundingBullet(self.rect.center, target_pos, color=(255, 0, 0)))  # Les projectiles sont bleus
        return bullets
    
    def fire_spiral_projectiles(self):
        bullets = []
        for angle in range(0, 360, 15):
            target_x = self.rect.centerx + 200 * math.cos(math.radians(angle))
            target_y = self.rect.centery + 200 * math.sin(math.radians(angle))
            bullets.append(Bullet(self.rect.center, (target_x, target_y), color=(255, 0, 0)))  # Red projectiles
        return bullets

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
        self.special_timers = [timer - 1 for timer in self.special_timers if timer > 0]

        if self.health <= self.phase_health_thresholds[3 - self.phase] and self.phase < 4:
            self.phase += 1
            self.attack_interval -= 20  # Increase attack frequency
            self.color = (255 // self.phase, 69, 0)  # Change color at each phase

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
            if self.phase == 1:
                test=random.random()
                if  test< 0.1:
                    return self.fire_exploding_bullets()
                if test > 0.1 and test < 0.3:
                    return self.shoot_rebounding_bullets()
                else:
                    return self.summon_fire_circles()
            if self.phase == 2:
                test=random.random()
                if  test< 0.1:
                    return self.fire_exploding_bullets()
                if test > 0.1 and test < 0.3:
                    return self.shoot_rebounding_bullets()
                else:
                    return self.fire_spiral_projectiles()
            if self.phase == 2:
                test=random.random()
                if  test< 0.1:
                    return self.fire_exploding_bullets()
                if test > 0.1 and test < 0.3:
                    return self.shoot_rebounding_bullets()
                if test > 0.3 and test <0.65 :
                    return self.fire_spiral_projectiles()
                else :
                    return self.summon_fire_circles()
        return []

    def draw(self, screen):
        pygame.draw.circle(screen, self.color, self.rect.center, 30)

class DamageCircle:
    def __init__(self, pos, radius, duration):
        self.rect = pygame.Rect(pos[0] - radius, pos[1] - radius, radius * 2, radius * 2)
        self.radius = radius
        self.color = (255, 0, 0)
        self.duration = duration

    def update(self):
        self.duration -= 1
        if self.duration <= 0:
            return False
        return True

    def draw(self, screen):
        pygame.draw.circle(screen, self.color, self.rect.center, self.radius)

class Thanatos:
    def __init__(self, x, y):
        self.rect = pygame.Rect(x - 30, y - 30, 60, 60)
        self.health = 1
        self.max_health = 1
        self.move_timer = 0
        self.move_interval = 35
        self.target_pos = self.get_new_position()
        self.attack_timer = 0
        self.attack_interval = 100
        self.phase = 1
        self.phase_health_thresholds = [1000, 600, 300]
        self.dying = False
        self.fade_alpha = 255
        self.color = (255, 0, 0)  # Initial color: red
        self.attack_types = [self.phase_one_attack, self.phase_two_attack, self.phase_three_attack, self.phase_four_attack]
        self.split = False  # Indicates if Thanatos is split
        self.split_parts = []

        self.ring_size = 50  # Initial size of the bullet ring
        self.bullet_ring = self.create_bullet_ring()

    def create_bullet_ring(self):
        bullets = []
        for angle in range(0, 360, 30):
            rad = math.radians(angle)
            x = self.rect.centerx + self.ring_size * math.cos(rad)
            y = self.rect.centery + self.ring_size * math.sin(rad)
            bullets.append(Bullet((x, y), (self.rect.centerx, self.rect.centery), speed=0))
        return bullets

    def update_bullet_ring(self):
        for i, bullet in enumerate(self.bullet_ring):
            angle = (pygame.time.get_ticks() / 10 + i * 30) % 360
            rad = math.radians(angle)
            bullet.rect.centerx = self.rect.centerx + self.ring_size * math.cos(rad)
            bullet.rect.centery = self.rect.centery + self.ring_size * math.sin(rad)

    def get_new_position(self):
        return random.randint(50, 550), random.randint(50, 550)

    def phase_one_attack(self):
        bullets = []
        for angle in range(0, 360, 45):
            target_x = self.rect.centerx + 100 * math.cos(math.radians(angle))
            target_y = self.rect.centery + 100 * math.sin(math.radians(angle))
            bullets.append(BossBullet(self.rect.centerx, self.rect.centery))
        return bullets

    def phase_two_attack(self):
        bullets = []
        for angle in range(0, 360, 30):
            target_x = self.rect.centerx + 150 * math.cos(math.radians(angle))
            target_y = self.rect.centery + 150 * math.sin(math.radians(angle))
            bullets.append(Bullet(self.rect.center, (target_x, target_y), color=(0, 255, 255)))
        return bullets

    def phase_three_attack(self):
        bullets = []
        for angle in range(0, 360, 20):
            target_x = self.rect.centerx + 200 * math.cos(math.radians(angle))
            target_y = self.rect.centery + 200 * math.sin(math.radians(angle))
            bullets.append(ExplodingBullet(self.rect.center, (target_x, target_y)))
        return bullets

    def phase_four_attack(self):
        bullets = []
        for angle in range(0, 360, 45):
            target_x = self.rect.centerx + 250 * math.cos(math.radians(angle))
            target_y = self.rect.centery + 250 * math.sin(math.radians(angle))
            bullets.append(SelfExplodingBullet(self.rect.center, (target_x, target_y)))
        return bullets

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

        if self.phase < 4 and self.health <= self.phase_health_thresholds[self.phase - 1] and self.health > 0:
            self.phase += 1
            self.attack_interval -= 10  # Increase attack frequency
            self.ring_size += 50  # Increase the size of the bullet ring
            self.color = (255 // self.phase, 0, 255 // self.phase)  # Change color at each phase

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
            return self.attack_types[self.phase - 1]()

        self.update_bullet_ring()
        return []

    def draw(self, screen):
        pygame.draw.circle(screen, self.color, self.rect.center, 30)
        for bullet in self.bullet_ring:
            bullet.draw(screen)

class TheSisters:
    def __init__(self, x, y):
        self.sister1 = {
            'shape': 'triangle',
            'rect': pygame.Rect(x - 30, y - 30, 60, 60),
            'health': 400,
            'max_health': 400,
            'color': (255, 0, 0),
        }
        self.sister2 = {
            'shape': 'circle',
            'rect': pygame.Rect(x + 30, y - 30, 60, 60),
            'health': 400,
            'max_health': 400,
            'color': (0, 0, 255),
        }
        self.health = 800  # Total health
        self.phase = 1
        self.phase_health_thresholds = [200, 100]  # Health thresholds for phases
        self.attack_timer = 0
        self.attack_interval = 70
        self.move_timer = 0
        self.move_interval = 50
        self.target_pos1 = self.get_new_position()
        self.target_pos2 = self.get_new_position()
        self.dying = False
        self.fade_alpha = 255
        self.quadrants_restricted = [False, False, False, False]  # To restrict access to quadrants

    def get_new_position(self):
        return random.randint(50, 550), random.randint(50, 550)

    def fire_exploding_bullets(self):
        bullets = []
        for angle in range(0, 360, 45):
            target_x = self.sister1['rect'].centerx + 150 * math.cos(math.radians(angle))
            target_y = self.sister1['rect'].centery + 150 * math.sin(math.radians(angle))
            bullets.append(ExplodingBullet(self.sister1['rect'].center, (target_x, target_y)))
        return bullets

    def shoot_rebounding_bullets(self):
        bullets = []
        for _ in range(8):
            target_pos = self.get_new_position()
            bullets.append(ReboundingBullet(self.sister2['rect'].center, target_pos, color=(0, 0, 255)))
        return bullets

    def restrict_quadrant(self):
        quadrant = random.choice([i for i, restricted in enumerate(self.quadrants_restricted) if not restricted])
        self.quadrants_restricted[quadrant] = True
        return quadrant

    def shoot_triangle_bullets(self):
        bullets = []
        for angle in range(0, 360, 45):  # Crée des triangles dans toutes les directions
            bullets.append(TriangleBullet(self.sister1["rect"].center, (
                self.sister1["rect"].centerx + 200 * math.cos(math.radians(angle)), 
                self.sister1["rect"].centery + 200 * math.sin(math.radians(angle))
            ), color=(255, 0, 0)))  # Les triangles sont bleus
        return bullets
    
    def create_restriction_lines(self, quadrant):
        lines = []
        if quadrant == 0:  # Top-left
            lines.append(DamageLineBullet((0, SCREEN_HEIGHT // 2), (SCREEN_WIDTH // 2, SCREEN_HEIGHT // 2), duration=500))
            lines.append(DamageLineBullet((SCREEN_WIDTH // 2, 0), (SCREEN_WIDTH // 2, SCREEN_HEIGHT // 2), duration=500))
        elif quadrant == 1:  # Top-right
            lines.append(DamageLineBullet((SCREEN_WIDTH // 2, SCREEN_HEIGHT // 2), (SCREEN_WIDTH, SCREEN_HEIGHT // 2), duration=500))
            lines.append(DamageLineBullet((SCREEN_WIDTH // 2, 0), (SCREEN_WIDTH // 2, SCREEN_HEIGHT // 2), duration=500))
        elif quadrant == 2:  # Bottom-left
            lines.append(DamageLineBullet((0, SCREEN_HEIGHT // 2), (SCREEN_WIDTH // 2, SCREEN_HEIGHT // 2), duration=500))
            lines.append(DamageLineBullet((SCREEN_WIDTH // 2, SCREEN_HEIGHT // 2), (SCREEN_WIDTH // 2, SCREEN_HEIGHT), duration=500))
        elif quadrant == 3:  # Bottom-right
            lines.append(DamageLineBullet((SCREEN_WIDTH // 2, SCREEN_HEIGHT // 2), (SCREEN_WIDTH, SCREEN_HEIGHT // 2), duration=500))
            lines.append(DamageLineBullet((SCREEN_WIDTH // 2, SCREEN_HEIGHT // 2), (SCREEN_WIDTH // 2, SCREEN_HEIGHT), duration=500))
        return lines

    def transfer_signature_attack(self):
        if self.sister1['health'] <= 0:
            return self.shoot_rebounding_bullets()
        elif self.sister2['health'] <= 0:
            return self.fire_exploding_bullets()
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

        if self.health <= self.phase_health_thresholds[2 - self.phase] and self.phase < 3:
            self.phase += 1
            self.attack_interval -= 20

        if self.move_timer >= self.move_interval:
            self.move_timer = 0
            self.target_pos1 = self.get_new_position()
            self.target_pos2 = self.get_new_position()

        if self.sister1['rect'].center != self.target_pos1:
            self.sister1['rect'] = self.sister1['rect'].move(
                (self.target_pos1[0] - self.sister1['rect'].centerx) // self.move_interval,
                (self.target_pos1[1] - self.sister1['rect'].centery) // self.move_interval
            )

        if self.sister2['rect'].center != self.target_pos2:
            self.sister2['rect'] = self.sister2['rect'].move(
                (self.target_pos2[0] - self.sister2['rect'].centerx) // self.move_interval,
                (self.target_pos2[1] - self.sister2['rect'].centery) // self.move_interval
            )

        bullets = []
        if self.attack_timer >= self.attack_interval:
            self.attack_timer = 0
            if self.sister1['health'] > 0 and self.sister2['health'] > 0:
                bullets += self.shoot_triangle_bullets() if random.random() < 0.5 else self.shoot_rebounding_bullets()
            elif self.sister1['health'] <= 0:
                bullets += self.shoot_rebounding_bullets() + self.transfer_signature_attack()
                quadrant = self.restrict_quadrant()
                bullets += self.create_restriction_lines(quadrant)
            elif self.sister2['health'] <= 0:
                bullets += self.fire_exploding_bullets() + self.transfer_signature_attack()
                quadrant = self.restrict_quadrant()
                bullets += self.create_restriction_lines(quadrant)

        return bullets

    def draw(self, screen):
        if self.sister1['health'] > 0:
            pygame.draw.polygon(screen, self.sister1['color'], [
                (self.sister1['rect'].centerx, self.sister1['rect'].centery - 30),
                (self.sister1['rect'].centerx - 30, self.sister1['rect'].centery + 30),
                (self.sister1['rect'].centerx + 30, self.sister1['rect'].centery + 30)
            ])
        if self.sister2['health'] > 0:
            pygame.draw.circle(screen, self.sister2['color'], self.sister2['rect'].center, 30)


class Thanatos_B:
    def __init__(self, x, y):
        self.rect = pygame.Rect(x - 30, y - 30, 60, 60)
        self.health = 500
        self.max_health = 500
        self.move_timer = 0
        self.move_interval = 50
        self.target_pos = self.get_new_position()
        self.attack_timer = 0
        self.attack_interval = 70
        self.phase = 1
        self.phase_health_thresholds = [500, 300]
        self.dying = False
        self.fade_alpha = 255
        self.color = (255, 0, 0)
        self.line_timers = []
        self.line_duration = 500
        self.ring_size = 150  # Initial size of the bullet ring
        self.bullet_ring = self.create_bullet_ring()
        
    def get_new_position(self):
        return random.randint(50, 550), random.randint(50, 550)

    def create_bullet_ring(self):
        bullets = []
        for angle in range(0, 360, 30):
            rad = math.radians(angle)
            x = self.rect.centerx + self.ring_size * math.cos(rad)
            y = self.rect.centery + self.ring_size * math.sin(rad)
            bullets.append(Bullet((x, y), (self.rect.centerx, self.rect.centery), speed=0))
        return bullets
    
    def fire_exploding_bullets(self):
        bullets = []
        for angle in range(0, 360, 45):
            target_x = self.rect.centerx + 250 * math.cos(math.radians(angle))
            target_y = self.rect.centery + 250 * math.sin(math.radians(angle))
            bullets.append(SelfExplodingBullet(self.rect.center, (target_x, target_y)))
        return bullets
    
    def update_bullet_ring(self):
        for i, bullet in enumerate(self.bullet_ring):
            angle = (pygame.time.get_ticks() / 10 + i * 30) % 360
            rad = math.radians(angle)
            bullet.rect.centerx = self.rect.centerx + self.ring_size * math.cos(rad)
            bullet.rect.centery = self.rect.centery + self.ring_size * math.sin(rad)

    def start_dying(self):
        self.dying = True
        
    def shoot_rebounding_bullets(self):
        bullets = []
        for _ in range(8):  # 8 balles qui rebondissent
            target_pos = self.get_new_position()
            bullets.append(ReboundingBullet(self.rect.center, target_pos, color=(0, 0, 255)))  # Les projectiles sont bleus
        return bullets
    
    def update(self):
        if self.dying:
            self.fade_alpha -= 5
            if self.fade_alpha < 0:
                self.fade_alpha = 0
            return []

        self.move_timer += 1
        self.attack_timer += 1
        self.line_timers = [timer - 1 for timer in self.line_timers if timer > 0]

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
            test=random.random()
            if  test< 0.5:
                return self.fire_exploding_bullets()
            else:
                return self.shoot_rebounding_bullets()
            
        self.update_bullet_ring()
        return []

    def draw(self, screen):
        pygame.draw.circle(screen, self.color, self.rect.center, 30)
        for bullet in self.bullet_ring:
            bullet.draw(screen)