import pygame
import sys
import random
import configparser
from menus import main_menu, boss_selection_menu, game_over_screen, victory_screen
from player import Player
from boss import Cerberus
from item import HealthItem
from background_text import BackgroundText

# Initialisation de Pygame
pygame.init()

# Charger la configuration
config = configparser.ConfigParser()
config.read('config.ini')

# Définition des constantes à partir de la configuration
SCREEN_WIDTH = config.getint('Screen', 'width')
SCREEN_HEIGHT = config.getint('Screen', 'height')
FPS = 60

# Couleurs
WHITE = tuple(map(int, config.get('Colors', 'white').split(',')))
RED = tuple(map(int, config.get('Colors', 'red').split(',')))
GREEN = tuple(map(int, config.get('Colors', 'green').split(',')))
BLUE = tuple(map(int, config.get('Colors', 'blue').split(',')))

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

def draw_health_bar(screen, x, y, width, height, current_health, max_health):
    pass
    #ratio = current_health / max_health
    #pygame.draw.rect(screen, RED, (x, y, width, height))
    #pygame.draw.rect(screen, GREEN, (x, y, width * ratio, height))

# Boucle principale du jeu
def main():
    clock = pygame.time.Clock()
    trophies = 0

    while True:
        if main_menu(screen):
            if boss_selection_menu(screen, trophies):
                # Initialisation du joueur, du boss et des objets de soin
                player = Player(SCREEN_WIDTH // 2, SCREEN_HEIGHT - 50)
                boss = Cerberus(SCREEN_WIDTH // 2, 50)
                player_bullets = []
                boss_bullets = []
                health_items = [HealthItem(random.randint(50, SCREEN_WIDTH - 50), random.randint(50, SCREEN_HEIGHT - 50)) for _ in range(3)]

                # Variables pour le changement de couleur de fond
                background_color = (0, 0, 0)
                timer = 0

                # Liste pour le texte de fond dynamique
                background_texts = [BackgroundText(SCREEN_WIDTH, SCREEN_HEIGHT, config['Paths']['font']) for _ in range(5)]

                # Boucle de jeu principale
                game_active = True
                while game_active:
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

                    # Mettre à jour et dessiner le texte de fond dynamique
                    for text in background_texts[:]:
                        text.update()
                        if text.is_faded():
                            background_texts.remove(text)
                            background_texts.append(BackgroundText(SCREEN_WIDTH, SCREEN_HEIGHT, config['Paths']['font']))
                        text.draw(screen)

                    screen.fill(background_color)

                    player.draw(screen)
                    boss.draw(screen)
                    
                    for bullet in player_bullets:
                        bullet.draw(screen)

                    for bullet in boss_bullets:
                        bullet.draw(screen)

                    for item in health_items:
                        item.draw(screen)
                    
                    # Affichage des PV du joueur
                    font = pygame.freetype.Font(config['Paths']['font'], 14)
                    draw_text(screen, f'HP: {player.health}', font, WHITE, 10, 10)

                    # Affichage de la barre de PV du boss
                    draw_health_bar(screen, SCREEN_WIDTH - 310, 10, 300, 25, boss.health, boss.max_health)

                    pygame.display.flip()
                    clock.tick(FPS)

                    # Vérifier les conditions de victoire et de défaite
                    if player.health <= 0:
                        game_active = False
                        if not game_over_screen(screen):
                            pygame.quit()
                            sys.exit()
                    elif boss.health <= 0:
                        game_active = False
                        trophies += 1
                        if not victory_screen(screen):
                            pygame.quit()
                            sys.exit()
        else:
            pygame.quit()
            sys.exit()

if __name__ == "__main__":
    main()
