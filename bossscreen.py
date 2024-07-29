        
import pygame
from moviepy.editor import VideoFileClip
import numpy as np
from config import load_config, save_config

config = load_config()

BaseScreen = config['cinematic']['Screen']
BaseMusicP = config['cinematic']['musicBase']


def Hades_intermediate_screen(screen, clock, font):
    # Charger la vidéo de fond de Charon
    clip = VideoFileClip(BaseScreen)
    clip = clip.resize((screen.get_width(), screen.get_height()))  # Redimensionner la vidéo à la taille de l'écran

    # Charger et jouer la musique de Charon
    pygame.mixer.music.load(BaseMusicP)
    pygame.mixer.music.play(-1)  # -1 pour jouer en boucle

    # Définir le texte
    text = "YOU... SHOULD NOT BE HERE !"
    text_surface = font.render(text, True, (0, 255, 255))  # Blanc
    text_rect = text_surface.get_rect(center=(screen.get_width() // 2, screen.get_height() // 2))

    # Afficher l'écran intermédiaire pendant la durée de la vidéo
    running = True
    for frame in clip.iter_frames(fps=30, dtype='uint8'):
        # Convertir l'image de la vidéo en surface Pygame
        frame_surface = pygame.surfarray.make_surface(np.transpose(frame, (1, 0, 2)))
        
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                return

        # Dessiner la surface de la vidéo et le texte
        screen.blit(frame_surface, (0, 0))
        screen.blit(text_surface, text_rect)
        pygame.display.flip()
        clock.tick(30)  # Contrôler le taux de rafraîchissement pour correspondre à la vidéo

        # Quitter la boucle après que la vidéo ait terminé
        if not clip.is_playing:
            running = False

    pygame.mixer.music.stop()

def Prom_intermediate_screen(screen, clock, font):
    # Charger la vidéo de fond de Charon
    clip = VideoFileClip(BaseScreen)
    clip = clip.resize((screen.get_width(), screen.get_height()))  # Redimensionner la vidéo à la taille de l'écran

    # Charger et jouer la musique de Charon
    pygame.mixer.music.load(BaseMusicP)
    pygame.mixer.music.play(-1)  # -1 pour jouer en boucle

    # Définir le texte
    text = "Who are you... Cursed...?"
    text_surface = font.render(text, True, (0, 255, 255))  # Blanc
    text_rect = text_surface.get_rect(center=(screen.get_width() // 2, screen.get_height() // 2))

    # Afficher l'écran intermédiaire pendant la durée de la vidéo
    running = True
    for frame in clip.iter_frames(fps=30, dtype='uint8'):
        # Convertir l'image de la vidéo en surface Pygame
        frame_surface = pygame.surfarray.make_surface(np.transpose(frame, (1, 0, 2)))
        
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                return

        # Dessiner la surface de la vidéo et le texte
        screen.blit(frame_surface, (0, 0))
        screen.blit(text_surface, text_rect)
        pygame.display.flip()
        clock.tick(30)  # Contrôler le taux de rafraîchissement pour correspondre à la vidéo

        # Quitter la boucle après que la vidéo ait terminé
        if not clip.is_playing:
            running = False

    pygame.mixer.music.stop()

def Cerb_intermediate_screen(screen, clock, font):
    # Charger la vidéo de fond de Charon
    clip = VideoFileClip(BaseScreen)
    clip = clip.resize((screen.get_width(), screen.get_height()))  # Redimensionner la vidéo à la taille de l'écran

    # Charger et jouer la musique de Charon
    pygame.mixer.music.load(BaseMusicP)
    pygame.mixer.music.play(-1)  # -1 pour jouer en boucle

    # Définir le texte
    text = "NONE SHALL ENTER !"
    text_surface = font.render(text, True, (0, 255, 255))  # Blanc
    text_rect = text_surface.get_rect(center=(screen.get_width() // 2, screen.get_height() // 2))

    # Afficher l'écran intermédiaire pendant la durée de la vidéo
    running = True
    for frame in clip.iter_frames(fps=30, dtype='uint8'):
        # Convertir l'image de la vidéo en surface Pygame
        frame_surface = pygame.surfarray.make_surface(np.transpose(frame, (1, 0, 2)))
        
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                return

        # Dessiner la surface de la vidéo et le texte
        screen.blit(frame_surface, (0, 0))
        screen.blit(text_surface, text_rect)
        pygame.display.flip()
        clock.tick(30)  # Contrôler le taux de rafraîchissement pour correspondre à la vidéo

        # Quitter la boucle après que la vidéo ait terminé
        if not clip.is_playing:
            running = False

    pygame.mixer.music.stop()
    
def Thanatos_intermediate_screen(screen, clock, font) :
     # Charger la vidéo de fond de Charon
    clip = VideoFileClip(BaseScreen)
    clip = clip.resize((screen.get_width(), screen.get_height()))  # Redimensionner la vidéo à la taille de l'écran

    # Charger et jouer la musique de Charon
    pygame.mixer.music.load(BaseMusicP)
    pygame.mixer.music.play(-1)  # -1 pour jouer en boucle

    # Définir le texte
    text = "YOU ARE NOTHING... BUT A MISTAKE !"
    text_surface = font.render(text, True, (0, 255, 255))  # Blanc
    text_rect = text_surface.get_rect(center=(screen.get_width() // 2, screen.get_height() // 2))

    # Afficher l'écran intermédiaire pendant la durée de la vidéo
    running = True
    for frame in clip.iter_frames(fps=30, dtype='uint8'):
        # Convertir l'image de la vidéo en surface Pygame
        frame_surface = pygame.surfarray.make_surface(np.transpose(frame, (1, 0, 2)))
        
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                return

        # Dessiner la surface de la vidéo et le texte
        screen.blit(frame_surface, (0, 0))
        screen.blit(text_surface, text_rect)
        pygame.display.flip()
        clock.tick(30)  # Contrôler le taux de rafraîchissement pour correspondre à la vidéo

        # Quitter la boucle après que la vidéo ait terminé
        if not clip.is_playing:
            running = False

    pygame.mixer.music.stop()
    
    
    
    
def TheS_intermediate_screen(screen, clock, font) :
     # Charger la vidéo de fond de Charon
    clip = VideoFileClip(BaseScreen)
    clip = clip.resize((screen.get_width(), screen.get_height()))  # Redimensionner la vidéo à la taille de l'écran

    # Charger et jouer la musique de Charon
    pygame.mixer.music.load(BaseMusicP)
    pygame.mixer.music.play(-1)  # -1 pour jouer en boucle

    # Définir le texte
    text = "You killed our brothers, we will avenge them." 
    text_surface = font.render(text, True, (0, 255, 255))  # Blanc
    text_rect = text_surface.get_rect(center=(screen.get_width() // 2, screen.get_height() // 2))
    # Afficher l'écran intermédiaire pendant la durée de la vidéo
    running = True
    for frame in clip.iter_frames(fps=30, dtype='uint8'):
        # Convertir l'image de la vidéo en surface Pygame
        frame_surface = pygame.surfarray.make_surface(np.transpose(frame, (1, 0, 2)))
        
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                return

        # Dessiner la surface de la vidéo et le texte
        screen.blit(frame_surface, (0, 0))
        screen.blit(text_surface, text_rect)
        pygame.display.flip()
        clock.tick(30)  # Contrôler le taux de rafraîchissement pour correspondre à la vidéo

        # Quitter la boucle après que la vidéo ait terminé
        if not clip.is_playing:
            running = False


def TheS_intermediate_screen_B(screen, clock, font) :
     # Charger la vidéo de fond de Charon
    clip = VideoFileClip(BaseScreen)
    clip = clip.resize((screen.get_width(), screen.get_height()))  # Redimensionner la vidéo à la taille de l'écran

    # Définir le texte
    text = "None Shall escape Death, None shall escape us."
    text_surface = font.render(text, True, (0, 255, 255))  # Blanc
    text_rect = text_surface.get_rect(center=(screen.get_width() // 2, screen.get_height() // 2))
    # Afficher l'écran intermédiaire pendant la durée de la vidéo
    running = True
    for frame in clip.iter_frames(fps=30, dtype='uint8'):
        # Convertir l'image de la vidéo en surface Pygame
        frame_surface = pygame.surfarray.make_surface(np.transpose(frame, (1, 0, 2)))
        
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                return

        # Dessiner la surface de la vidéo et le texte
        screen.blit(frame_surface, (0, 0))
        screen.blit(text_surface, text_rect)
        pygame.display.flip()
        clock.tick(30)  # Contrôler le taux de rafraîchissement pour correspondre à la vidéo

        # Quitter la boucle après que la vidéo ait terminé
        if not clip.is_playing:
            running = False

    pygame.mixer.music.stop()