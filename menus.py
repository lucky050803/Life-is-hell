import pygame
import pygame.freetype
from config import load_config
import sys 

config = load_config()
font_path = config['Paths']['font']
font_size = 24
SCREEN_HEIGHT = int(config['Screen']['height'])
SCREEN_WIDTH = int(config['Screen']['width'])
pygame.freetype.init()
font = pygame.freetype.Font(font_path, font_size)

def draw_text_centered(screen, text, font, color, x, y):
    text_surface, text_rect = font.render(text, color)
    text_rect.center = (x, y)
    screen.blit(text_surface, text_rect)

def main_menu(screen, video_frames):
    button_font = pygame.freetype.Font(font_path, font_size)

    button_texts = ["Play", "Settings", "Credits", "Quit"]
    button_rects = [pygame.Rect(0, 0, 200, 50) for _ in button_texts]
    for i, rect in enumerate(button_rects):
        rect.center = (screen.get_width() // 2, screen.get_height() // 2 + i * 60)

    running = True
    frame_index = 0
    while running:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
            if event.type == pygame.MOUSEBUTTONDOWN:
                for i, rect in enumerate(button_rects):
                    if rect.collidepoint(event.pos):
                        return button_texts[i].lower()

        screen.blit(video_frames[frame_index % len(video_frames)], (0, 0))
        frame_index += 1
        
        draw_text_centered(screen, "", font, (0, 255, 255), screen.get_width() // 2, screen.get_height() // 2 - 100)
        
        for i, rect in enumerate(button_rects):
            pygame.draw.rect(screen, (0, 255, 255), rect)
            draw_text_centered(screen, button_texts[i], button_font, (0, 0, 0), rect.centerx, rect.centery)

        pygame.display.flip()



import pygame
import sys

def boss_selection_menu(screen, trophies, bosses_defeated, video_frames, font):
    clock = pygame.time.Clock()
    selected_boss = None

    boss_options = ["Cerberus"]
    if "Cerberus" in bosses_defeated:
        boss_options.append("Prometheus")

    dropdown_active = False
    dropdown_rect = pygame.Rect(200, 150, 200, 50)
    option_rects = [pygame.Rect(200, 200 + 50 * i, 200, 50) for i in range(len(boss_options))]
    back_button_rect = pygame.Rect(50, SCREEN_HEIGHT - 100, 100, 50)  # Bouton "Retour"

    while True:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
            if event.type == pygame.MOUSEBUTTONDOWN:
                if dropdown_rect.collidepoint(event.pos):
                    dropdown_active = not dropdown_active
                else:
                    for i, rect in enumerate(option_rects):
                        if rect.collidepoint(event.pos):
                            selected_boss = boss_options[i]
                            dropdown_active = False
                if back_button_rect.collidepoint(event.pos):
                    return None  # Retourner au menu principal

        frame = video_frames[pygame.time.get_ticks() // 100 % len(video_frames)]
        screen.blit(frame, (0, 0))

        pygame.draw.rect(screen, (0, 0, 0), dropdown_rect)
        text_surface = font.render("Select Boss", True, (255, 255, 255))
        screen.blit(text_surface, (dropdown_rect.x + 10, dropdown_rect.y + 10))

        if dropdown_active:
            for i, rect in enumerate(option_rects):
                pygame.draw.rect(screen, (0, 0, 0), rect)
                text_surface = font.render(boss_options[i], True, (255, 255, 255))
                screen.blit(text_surface, (rect.x + 10, rect.y + 10))

        # Dessiner le bouton "Retour"
        pygame.draw.rect(screen, (0, 0, 0), back_button_rect)
        text_surface = font.render("Back", True, (255, 255, 255))
        screen.blit(text_surface, (back_button_rect.x + 10, back_button_rect.y + 10))

        pygame.display.flip()
        clock.tick(30)

        if selected_boss:
            return selected_boss







def game_over_screen(screen, video_frames):
    button_font = pygame.freetype.Font(font_path, font_size)

    button_text = "Back to Boss Selection"
    button_rect = pygame.Rect(0, 0, 300, 50)
    button_rect.center = (screen.get_width() // 2, screen.get_height() // 2 + 100)

    running = True
    frame_index = 0
    while running:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
            if event.type == pygame.MOUSEBUTTONDOWN:
                if button_rect.collidepoint(event.pos):
                    return True

        screen.blit(video_frames[frame_index % len(video_frames)], (0, 0))
        frame_index += 1
        
        draw_text_centered(screen, "Game Over", font, (255, 0, 0), screen.get_width() // 2, screen.get_height() // 2 - 50)
        pygame.draw.rect(screen, (0, 255, 255), button_rect)
        draw_text_centered(screen, button_text, button_font, (0, 0, 0), button_rect.centerx, button_rect.centery)

        pygame.display.flip()
        
        
def credits_menu(screen, video_frames):
    button_font = pygame.freetype.Font(font_path, font_size)
    button_text = "Back"
    button_rect = pygame.Rect(0, 0, 200, 50)
    button_rect.center = (screen.get_width() // 2, screen.get_height() - 100)

    running = True
    frame_index = 0
    while running:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
            if event.type == pygame.MOUSEBUTTONDOWN:
                if button_rect.collidepoint(event.pos):
                    return
        
        screen.blit(video_frames[frame_index % len(video_frames)], (0, 0))
        frame_index += 1
        
        draw_text_centered(screen, "Credits", font, (0, 255, 255), screen.get_width() // 2, screen.get_height() // 2 - 100)
        draw_text_centered(screen, "Game Developer: Lucca Masi", font, (0, 255, 255), screen.get_width() // 2, screen.get_height() // 2)
        draw_text_centered(screen, "Graphics: Lucca Masi", font, (0, 255, 255), screen.get_width() // 2, screen.get_height() // 2 + 40)
        #draw_text_centered(screen, "Music: Your Name", font, (0, 255, 255), screen.get_width() // 2, screen.get_height() // 2 + 80)
        
        pygame.draw.rect(screen, (0, 255, 255), button_rect)
        draw_text_centered(screen, button_text, button_font, (0, 0, 0), button_rect.centerx, button_rect.centery)
        
        pygame.display.flip()


def victory_screen(screen, video_frames, cerberus_first_defeat=False, font=None):
    clock = pygame.time.Clock()
    if not font:
        font = pygame.font.Font(None, 48)

    timer = 0
    while timer < 300:  # Afficher l'écran de victoire pendant 5 secondes
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()

        frame = video_frames[pygame.time.get_ticks() // 100 % len(video_frames)]
        screen.blit(frame, (0, 0))

        text_surface = font.render("Victory!", True, (255, 255, 255))
        screen.blit(text_surface, (SCREEN_WIDTH // 2 - text_surface.get_width() // 2, SCREEN_HEIGHT // 2 - text_surface.get_height() // 2))

        if cerberus_first_defeat:
            unlock_surface = font.render("Prometheus Unlocked!", True, (255, 255, 0))
            screen.blit(unlock_surface, (SCREEN_WIDTH // 2 - unlock_surface.get_width() // 2, SCREEN_HEIGHT // 2 + text_surface.get_height() // 2 + 10))

        pygame.display.flip()
        clock.tick(60)
        timer += 1

