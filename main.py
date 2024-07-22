import pygame
import sys
import random
import configparser
from moviepy.editor import VideoFileClip
from menus import main_menu, boss_selection_menu, game_over_screen, victory_screen, credits_menu, shop_menu
from setting_menu import settings_menu
from player import Player
from boss import Hades, Cerberus, Prometheus, Charon, Thanatos
from item import HealthItem
from config import load_config, save_config
from bossscreen import *


# Initialisation de Pygame
pygame.init()




# Charger la configuration
config = load_config()

# Définition des constantes à partir de la configuration
SCREEN_WIDTH = 600
SCREEN_HEIGHT = 600
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
volume = float(config['Music']['volume'])

# Initialisation du module de mixage
pygame.mixer.init()
pygame.mixer.music.set_volume(volume)

# Création de la fenêtre de jeu
screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
pygame.display.set_caption("Life Is Hell")

font = pygame.font.Font(font_path, 24)

def draw_text(screen, text, font, color, x, y):
    text_surface = font.render(text, True, color)
    screen.blit(text_surface, (x, y))

def draw_text_bottom_right(screen, text, font, color, x_offset, y_offset):
    text_surface = font.render(text, True, color)
    text_rect = text_surface.get_rect()
    text_rect.bottomright = (SCREEN_WIDTH - x_offset, SCREEN_HEIGHT - y_offset)
    screen.blit(text_surface, text_rect.topleft)

def draw_trophies(screen, trophies, font):
    text_surface, _ = font.render(f"Trophies: {trophies}", (255, 255, 255))
    screen.blit(text_surface, (screen.get_width() - text_surface.get_width() - 10, 10))

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

def load_game():
    trophies = config.getint('Save', 'trophies')
    bosses_defeated = config.get('Save', 'bosses_defeated').split(',')
    volume = config.getfloat('Music', 'volume')

    player_stats = {
        'health': config.getint('Player', 'health', fallback=0),
        'damage': config.getint('Player', 'damage', fallback=0),
        'projectiles': config.getint('Player', 'projectiles', fallback=0),
    }
    
    return trophies, bosses_defeated, volume, player_stats

def save_game(trophies, bosses_defeated, volume, player_stats):
    config['Save']['trophies'] = str(trophies)
    config['Save']['bosses_defeated'] = ','.join(bosses_defeated)
    config['Music']['volume'] = str(volume)

    config['Player'] = {
        'health': str(player_stats['health']),
        'damage': str(player_stats['damage']),
        'projectiles': str(player_stats['projectiles']),
    }

    save_config(config)

def load_boss_assets(boss_name):
    boss_section = f'Boss_{boss_name}'
    background_path = config[boss_section]['background']
    music_path = config[boss_section]['music']
    
    # Charger la vidéo de fond et réduire sa taille
    clip = VideoFileClip(background_path)
    clip = clip.resize((SCREEN_WIDTH, SCREEN_HEIGHT))
    video_frames = [pygame.image.frombuffer(frame.tobytes(), frame.shape[1::-1], "RGB") for frame in clip.iter_frames()]
    
    return video_frames, music_path

def show_loading_screen(screen, font):
    screen.fill((0, 0, 0))
    draw_text(screen, "Loading...", font, WHITE, SCREEN_WIDTH // 2 - 50, SCREEN_HEIGHT // 2 - 25)
    pygame.display.flip()

# Boucle principale du jeu
def main():
    clock = pygame.time.Clock()
    trophies, bosses_defeated, volume, player_stats = load_game()
    pygame.mixer.music.set_volume(volume)

    # Charger la vidéo de fond et réduire sa taille
    clip = VideoFileClip(video_path)
    clip = clip.resize((SCREEN_WIDTH, SCREEN_HEIGHT))
    video_frames = [pygame.image.frombuffer(frame.tobytes(), frame.shape[1::-1], "RGB") for frame in clip.iter_frames()]

    while True:
        pygame.mixer.music.load(menu_music_path)
        pygame.mixer.music.play(-1)
        choice = main_menu(screen, video_frames, trophies)
        if choice == "play":
            boss_name = boss_selection_menu(screen, trophies, bosses_defeated, video_frames, font)
            if boss_name:
                if boss_name == "Charon":
                    Charon_intermediate_screen(screen, clock, font)
                elif boss_name == "Hades":
                    Hades_intermediate_screen(screen, clock, font)
                elif boss_name == "Prometheus":
                    Prom_intermediate_screen(screen, clock, font)
                elif boss_name == "Cerberus":
                    Cerb_intermediate_screen(screen, clock, font)
                elif boss_name == "Thanatos":
                    Thanatos_intermediate_screen(screen, clock, font)  # Ajouter un écran intermédiaire pour Thanatos
                    
                show_loading_screen(screen, font)
                pygame.time.wait(2000)  # Temps d'attente simulé pour le chargement
                boss_video_frames, boss_music_path = load_boss_assets(boss_name)
                pygame.mixer.music.load(boss_music_path)
                pygame.mixer.music.play(-1)

                # Initialisation du joueur, du boss et des objets de soin
                player = Player(SCREEN_WIDTH // 2, SCREEN_HEIGHT - 50, player_stats)
                if boss_name == "Cerberus":
                    boss = Cerberus(SCREEN_WIDTH // 2, 50)
                elif boss_name == "Prometheus":
                    boss = Prometheus(SCREEN_WIDTH // 2, 50)
                elif boss_name == "Hades":
                    boss = Hades(SCREEN_WIDTH // 2, 50)
                elif boss_name == "Charon":
                    boss = Charon(SCREEN_WIDTH // 2, 50)  # Add Charon initialization
                elif boss_name == "Thanatos":
                    boss = Thanatos(SCREEN_WIDTH // 2, 50)  # Initialisation de Thanatos



                player_bullets = []
                boss_bullets = []
                health_items = [HealthItem(random.randint(50, SCREEN_WIDTH - 50), random.randint(50, SCREEN_HEIGHT - 50)) for _ in range(3)]

                # Variables pour le changement de couleur de fond
                timer = 0

                
                

                # Boucle de jeu principale
                game_active = True
                while game_active:
                    for event in pygame.event.get():
                        if event.type == pygame.QUIT:
                            pygame.quit()
                            sys.exit()
                        if event.type == pygame.MOUSEBUTTONDOWN:
                            if event.button == 1:
                                player_bullets.extend(player.shoot(pygame.mouse.get_pos()))

                    keys = pygame.key.get_pressed()
                    player.update(keys)
                    
                    # Mettre à jour les balles du joueur
                    for bullet in player_bullets[:]:
                        bullet.update()
                        if bullet.rect.colliderect(boss.rect):
                            boss.health -= player.damage
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
                            player.health -= 20
                            boss_bullets.remove(bullet)
                        elif bullet.rect.left < 0 or bullet.rect.right > SCREEN_WIDTH or bullet.rect.top < 0 or bullet.rect.bottom > SCREEN_HEIGHT:
                            boss_bullets.remove(bullet)
                        if bullet.update()==False:
                            boss_bullets.remove(bullet)

                    # Mettre à jour les objets de soin
                    for item in health_items[:]:
                        if player.rect.colliderect(item.rect):
                            player.health = min(player.health + 10, 100)
                            health_items.remove(item)

                    # Mettre à jour la couleur de fond
                    timer += 1

                    # Afficher la vidéo de fond
                    frame = boss_video_frames[timer % len(boss_video_frames)]
                    screen.blit(frame, (0, 0))

                    player.draw(screen)
                    boss.draw(screen)

                    for bullet in player_bullets:
                        bullet.draw(screen)

                    for bullet in boss_bullets:
                        bullet.draw(screen)

                    for item in health_items:
                        item.draw(screen)

                    # Afficher le texte des PV du joueur
                    draw_text_bottom_right(screen, f"HP: {player.health}", font, WHITE, 10, 10)

                    # Afficher le texte des trophées
                    #draw_trophies(screen, trophies, font)

                    pygame.display.flip()
                    clock.tick(FPS)

                    if player.health <= 0:
                        game_active = False
                        game_over_screen(screen, video_frames)
                    elif boss.health <= 0:
                        boss.start_dying()
                        boss.update()
                        boss.draw(screen)
                        pygame.display.flip()
                        pygame.time.wait(2000)  # Attendre que l'animation de mort se termine
                        game_active = False
                        if boss_name not in bosses_defeated:
                            trophies += 1
                            bosses_defeated.append(boss_name)
                        save_game(trophies, bosses_defeated, volume, player_stats)
                        victory_screen(screen, video_frames, boss_name == "Cerberus" and boss_name not in bosses_defeated, font)

        if choice == "settings":
            volume = settings_menu(screen, volume, video_frames)
            config['Music']['volume'] = str(volume)  # Mettre à jour le volume dans la config
            save_config(config)
        elif choice == "quit":
            pygame.quit()
            sys.exit()
        elif choice == "credits":
            credits_menu(screen, video_frames)
        elif choice == "shop":
            trophies, player_stats = shop_menu(screen, trophies, player_stats, video_frames, font)


main()
