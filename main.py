import pygame
import sys
import random
import configparser
from moviepy.editor import VideoFileClip
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

# Chemins des fichiers
video_path = config['Paths']['menu_background']
font_path = config['Paths']['font']
menu_music_path = config['Music']['menu_music']
boss_music_path = config['Music']['boss_music']

# Création de la fenêtre de jeu
screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
pygame.display.set_caption("Bullet Hell Game")

# Initialisation du module de mixage
pygame.mixer.init()

def draw_text(screen, text, font, color, x, y):
    text_surface, text_rect = font.render(text, color)
    screen.blit(text_surface, (x, y))

def change_background_color(timer):
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
    ratio = current_health / max_health
    pygame.draw.rect(screen, RED, (x, y, width, height))
    pygame.draw.rect(screen, GREEN, (x, y, width * ratio, height))

# Boucle principale du jeu
def main():
    clock = pygame.time.Clock()
    trophies = 0

    # Charger la vidéo de fond et réduire sa taille
    clip = VideoFileClip(video_path)
    clip = clip.resize((SCREEN_WIDTH, SCREEN_HEIGHT))
    video_frames = [pygame.image.frombuffer(frame.tobytes(), frame.shape[1::-1], "RGB") for frame in clip.iter_frames()]

    while True:
        pygame.mixer.music.load(menu_music_path)
        pygame.mixer.music.play(-1)
        if main_menu(screen):
            if boss_selection_menu(screen, trophies):
                pygame.mixer.music.load(boss_music_path)
                pygame.mixer.music.play(-1)

                # Initialisation du joueur, du boss et des objets de soin
                player = Player(SCREEN_WIDTH // 2, SCREEN_HEIGHT - 50)
                boss = Cerberus(SCREEN_WIDTH // 2, 50)
                player_bullets = []
                boss_bullets = []
                health_items = [HealthItem(random.randint(50, SCREEN_WIDTH - 50), random.randint(50, SCREEN_HEIGHT - 50)) for _ in range(3)]

                # Variables pour le changement de couleur de fond
                timer = 0

                # Liste pour le texte de fond dynamique
                background_texts = [BackgroundText(SCREEN_WIDTH, SCREEN_HEIGHT, font_path) for _ in range(3)]

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
                            boss.health -= 25
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
                    background_color = change_background_color(timer)
                    timer += 1

                    # Mettre à jour et dessiner le texte de fond dynamique
                    for text in background_texts[:]:
                        text.update()
                        if text.is_faded():
                            background_texts.remove(text)
                            background_texts.append(BackgroundText(SCREEN_WIDTH, SCREEN_HEIGHT, font_path))
                        text.draw(screen)

                    # Afficher la vidéo de fond
                    frame = video_frames[timer % len(video_frames)]
                    screen.blit(frame, (0, 0))

                    player.draw(screen)
                    boss.draw(screen)
                    
                    for bullet in player_bullets:
                        bullet.draw(screen)

                    for bullet in boss_bullets:
                        bullet.draw(screen)

                    for item in health_items:
                        item.draw(screen)
                    
                    # Affichage des PV du joueur
                    font = pygame.freetype.Font(font_path, 36)
                    draw_text(screen, f'Player HP: {player.health}', font, WHITE, 10, 10)

                    # Affichage de la barre de PV du boss
                    #draw_health_bar(screen, SCREEN_WIDTH - 310, 10, 200, 10, boss.health, boss.max_health)

                    pygame.display.flip()
                    clock.tick(FPS)

                    # Vérifier les conditions de victoire et de défaite
                    if player.health <= 0:
                        game_active = False
                        pygame.mixer.music.stop()
                        if not game_over_screen(screen):
                            pygame.quit()
                            sys.exit()
                    elif boss.health <= 0:
                        game_active = False
                        pygame.mixer.music.stop()
                        trophies += 1
                        if not victory_screen(screen):
                            pygame.quit()
                            sys.exit()
        else:
            pygame.quit()
            sys.exit()

if __name__ == "__main__":
    main()
