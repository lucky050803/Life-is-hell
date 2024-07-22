import pygame
import random
import math
from bullet import *
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
        self.attack_interval = 120  # Réduire l'intervalle d'attaque
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
        self.max_health = 800
        self.move_timer = 0
        self.move_interval = 50
        self.target_pos = self.get_new_position()
        self.attack_timer = 0
        self.attack_interval = 100
        self.phase = 1
        self.phase_health_thresholds = [600, 300]
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

class Hades:
    def __init__(self, x, y):
        self.rect = pygame.Rect(x - 30, y - 30, 60, 60)
        self.health = 4000
        self.max_health = 800
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

    def fire_flame_projectiles(self):
        bullets = []
        for angle in range(0, 360, 30):
            target_x = self.rect.centerx + 150 * math.cos(math.radians(angle))
            target_y = self.rect.centery + 150 * math.sin(math.radians(angle))
            bullets.append(Bullet(self.rect.center, (target_x, target_y), color=(255, 69, 0)))  # Orange-red projectiles
        return bullets

    def summon_fire_circles(self):
        circles = []
        for _ in range(2):
            pos = (random.randint(50, 550), random.randint(50, 550))
            circles.append(DamageCircle(pos, 50, duration=180))  # 3 seconds duration
        return circles

    def summon_souls(self):
        souls = []
        for _ in range(5):
            target_pos = self.get_new_position()
            souls.append(HomingBullet(self.rect.center, target_pos, speed=5, color=(0, 0, 139)))  # Dark blue projectiles
        return souls

    def cast_dark_winds(self):
        winds = []
        for _ in range(3):
            pos = (random.randint(50, 550), random.randint(50, 550))
            winds.append(SlowingZone(pos, 150, duration=180))  # 3 seconds duration
        return winds

    def summon_lava_geysers(self):
        geysers = []
        for _ in range(3):
            pos = (random.randint(50, 550), random.randint(50, 550))
            geysers.append(LavaGeyser(pos, duration=180))  # 3 seconds duration
        return geysers

    def create_lava_zones(self):
        zones = []
        for _ in range(2):
            pos = (random.randint(50, 550), random.randint(50, 550))
            zones.append(PersistentLavaZone(pos, 200, duration=300))  # 5 seconds duration
        return zones

    def fire_spiral_projectiles(self):
        bullets = []
        for angle in range(0, 360, 15):
            target_x = self.rect.centerx + 200 * math.cos(math.radians(angle))
            target_y = self.rect.centery + 200 * math.sin(math.radians(angle))
            bullets.append(Bullet(self.rect.center, (target_x, target_y), color=(255, 0, 0)))  # Red projectiles
        return bullets

    def create_moving_fire_lines(self):
        lines = []
        for _ in range(2):
            start_x = random.randint(50, 550)
            lines.append(MovingFireLine((start_x, 0), (start_x, 600), 180))  # 3 seconds duration
        return lines

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
                if random.random() < 0.5:
                    return self.fire_flame_projectiles()
                return self.summon_fire_circles()
            elif self.phase == 2:
                if random.random() < 0.5:
                    return self.summon_souls()
                return self.cast_dark_winds()
            elif self.phase == 3:
                if random.random() < 0.5:
                    return self.summon_lava_geysers()
                return self.create_lava_zones()
            elif self.phase == 4:
                if random.random() < 0.5:
                    return self.fire_spiral_projectiles()
                return self.create_moving_fire_lines()

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

class HomingBullet(Bullet):
    def update(self, player_pos):
        angle = math.atan2(player_pos[1] - self.rect.centery, player_pos[0] - self.rect.centerx)
        self.velocity = self.speed * math.cos(angle), self.speed * math.sin(angle)
        super().update()

class SlowingZone:
    def __init__(self, pos, radius, duration):
        self.rect = pygame.Rect(pos[0] - radius, pos[1] - radius, radius * 2, radius * 2)
        self.radius = radius
        self.color = (0, 0, 139)
        self.duration = duration

    def update(self):
        self.duration -= 1
        if self.duration <= 0:
            return False
        return True

    def draw(self, screen):
        pygame.draw.circle(screen, self.color, self.rect.center, self.radius)

class LavaGeyser:
    def __init__(self, pos, duration):
        self.rect = pygame.Rect(pos[0] - 15, pos[1] - 15, 30, 30)
        self.color = (255, 69, 0)
        self.duration = duration

    def update(self):
        self.duration -= 1
        if self.duration <= 0:
            return False
        return True

    def draw(self, screen):
        pygame.draw.rect(screen, self.color, self.rect)

class PersistentLavaZone:
    def __init__(self, pos, size, duration):
        self.rect = pygame.Rect(pos[0] - size // 2, pos[1] - size // 2, size, size)
        self.color = (255, 69, 0)
        self.duration = duration

    def update(self):
        self.duration -= 1
        if self.duration <= 0:
            return False
        return True

    def draw(self, screen):
        pygame.draw.rect(screen, self.color, self.rect)

class MovingFireLine(DamageLineBullet):
    def __init__(self, start_pos, end_pos, duration):
        super().__init__(start_pos, end_pos, duration)
        self.speed = 2
        self.velocity = self.calculate_velocity(start_pos, end_pos)

    def calculate_velocity(self, start_pos, end_pos):
        angle = math.atan2(end_pos[1] - start_pos[1], end_pos[0] - start_pos[0])
        return self.speed * math.cos(angle), self.speed * math.sin(angle)

    def update(self):
        self.rect.x += self.velocity[0]
        self.rect.y += self.velocity[1]
        return super().update()

class Charon:
    def __init__(self, x, y):
        self.rect = pygame.Rect(x - 30, y - 30, 60, 60)
        self.health = 1000
        self.max_health = 1000
        self.move_timer = 0
        self.move_interval = 50
        self.target_pos = self.get_new_position()
        self.attack_timer = 0
        self.attack_interval = 100
        self.phase = 1
        self.phase_health_thresholds = [750, 500, 250]
        self.dying = False
        self.fade_alpha = 255
        self.color = (128, 0, 128)  # Initial color: purple
        self.attack_types = [self.phase_one_attack, self.phase_two_attack, self.phase_three_attack, self.phase_four_attack]

    def get_new_position(self):
        return random.randint(50, 550), random.randint(50, 550)

    def phase_one_attack(self):
        bullets = []
        for _ in range(8):
            target_pos = self.get_new_position()
            bullets.append(BossBullet(self.rect.centerx, self.rect.centery))
        return bullets

    def phase_two_attack(self):
        bullets = []
        for angle in range(0, 360, 45):
            target_x = self.rect.centerx + 150 * math.cos(math.radians(angle))
            target_y = self.rect.centery + 150 * math.sin(math.radians(angle))
            bullets.append(Bullet(self.rect.center, (target_x, target_y), color=(255, 255, 0)))
        return bullets

    def phase_three_attack(self):
        bullets = []
        for angle in range(0, 360, 30):
            target_x = self.rect.centerx + 200 * math.cos(math.radians(angle))
            target_y = self.rect.centery + 200 * math.sin(math.radians(angle))
            bullets.append(ExplodingBullet(self.rect.center, (target_x, target_y)))
        return bullets

    def phase_four_attack(self):
        bullets = []
        for angle in range(0, 360, 15):
            target_x = self.rect.centerx + 250 * math.cos(math.radians(angle))
            target_y = self.rect.centery + 250 * math.sin(math.radians(angle))
            bullets.append(DamageLineBullet(self.rect.center, (target_x, target_y), 180))
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

        return []

    def draw(self, screen):
        pygame.draw.circle(screen, self.color, self.rect.center, 30)
        
        
