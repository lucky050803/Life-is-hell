import pygame
import sys
import random
from menus import main_menu, boss_selection_menu
from player import Player
from boss import Cerberus
from item import HealthItem

# Initialisation de Pygame
pygame.init()

# Définition des constantes
SCREEN_WIDTH = 800
SCREEN_HEIGHT = 600
FPS = 60

# Couleurs
WHITE = (255, 255, 255)
RED = (255, 0, 0)
GREEN = (0, 255, 0)
BLUE = (0, 0, 255)

# Création de la fenêtre de jeu
screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
pygame.display.set_caption("Bullet Hell Game")

def draw_text(screen, text, font, color, x, y):
    text_surface, text_rect = font.render(text, color)
    screen.blit(text_surface, (x, y))

def change_background_color(current_color, timer):
    if timer % 120 < 10:  # Flashe entre bleu, rouge et vert
        if timer % 30 < 10:
            return BLUE
        elif timer % 30 < 20:
            return RED
        else:
            return GREEN
    elif timer % 240 < 120:
        return (50, 50, 50)  # Gris
    else:
        return (0, 0, 0)  # Noir

# Boucle principale du jeu
def main():
    clock = pygame.time.Clock()
    
    if main_menu(screen):
        if boss_selection_menu(screen):
            # Initialisation du joueur, du boss et des objets de soin
            player = Player(SCREEN_WIDTH // 2, SCREEN_HEIGHT - 50)
            boss = Cerberus(SCREEN_WIDTH // 2, 50)
            player_bullets = []
            boss_bullets = []
            health_items = [HealthItem(random.randint(50, 750), random.randint(50, 550)) for _ in range(3)]

            # Variables pour le changement de couleur de fond
            background_color = (0, 0, 0)
            timer = 0

            # Boucle de jeu principale
            while True:
                for event in pygame.event.get():
                    if event.type == pygame.QUIT:
                        pygame.quit()
                        sys.exit()
                    if event.type == pygame.MOUSEBUTTONDOWN:
                        if event.button == 1:
                            player_bullets.append(player.shoot(pygame.mouse.get_pos()))

                keys = pygame.key.get_pressed()
                player.update(keys)
                
                # Mettre à jour les balles du joueur
                for bullet in player_bullets[:]:
                    bullet.update()
                    if bullet.rect.colliderect(boss.rect):
                        boss.health -= 10
                        player_bullets.remove(bullet)
                    elif bullet.rect.left < 0 or bullet.rect.right > SCREEN_WIDTH or bullet.rect.top < 0 or bullet.rect.bottom > SCREEN_HEIGHT:
                        player_bullets.remove(bullet)

                # Mettre à jour le boss et obtenir les projectiles créés
                boss_projectiles = boss.update()
                if boss_projectiles:
                    boss_bullets.extend(boss_projectiles)

                # Mettre à jour les balles du boss
                for bullet in boss_bullets[:]:
                    bullet.update()
                    if bullet.rect.colliderect(player.rect):
                        player.health -= 20  # Augmentation des dégâts de Cerberus
                        boss_bullets.remove(bullet)
                    elif bullet.rect.left < 0 or bullet.rect.right > SCREEN_WIDTH or bullet.rect.top < 0 or bullet.rect.bottom > SCREEN_HEIGHT:
                        boss_bullets.remove(bullet)

                # Mettre à jour les objets de soin
                for item in health_items[:]:
                    if player.rect.colliderect(item.rect):
                        player.health = min(player.health + 10, 100)  # Le joueur regagne 10 HP
                        health_items.remove(item)

                # Mettre à jour la couleur de fond
                background_color = change_background_color(background_color, timer)
                timer += 1

                screen.fill(background_color)

                player.draw(screen)
                boss.draw(screen)
                
                for bullet in player_bullets:
                    bullet.draw(screen)

                for bullet in boss_bullets:
                    bullet.draw(screen)

                for item in health_items:
                    item.draw(screen)
                
                # Affichage des PV
                font = pygame.freetype.Font("OpenSans-Regular.ttf", 36)
                draw_text(screen, f'Player HP: {player.health}', font, WHITE, 10, 10)
                draw_text(screen, f'Boss HP: {boss.health}', font, WHITE, SCREEN_WIDTH - 150, 10)

                pygame.display.flip()
                clock.tick(FPS)
    else:
        pygame.quit()
        sys.exit()

if __name__ == "__main__":
    main()
