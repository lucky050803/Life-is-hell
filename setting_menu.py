import pygame
import pygame.freetype
from config import load_config

config = load_config()
font_path = config['Paths']['font']
font_size = 24

pygame.freetype.init()
font = pygame.freetype.Font(font_path, font_size)

def draw_text_centered(screen, text, font, color, x, y):
    text_surface, text_rect = font.render(text, color)
    text_rect.center = (x, y)
    screen.blit(text_surface, text_rect)

def settings_menu(screen, current_volume, video_frames):
    button_font = pygame.freetype.Font(font_path, font_size)

    button_text = "Back"
    button_color = (0, 255, 255)
    button_rect = pygame.Rect(0, 0, 200, 50)
    button_rect.center = (screen.get_width() // 2, screen.get_height() // 2 + 100)

    plus_button_rect = pygame.Rect(0, 0, 50, 50)
    plus_button_rect.center = (screen.get_width() // 2 + 75, screen.get_height() // 2+20)

    minus_button_rect = pygame.Rect(0, 0, 50, 50)
    minus_button_rect.center = (screen.get_width() // 2 - 75, screen.get_height() // 2+20)

    running = True
    volume = current_volume
    frame_index = 0

    while running:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                return volume
            if event.type == pygame.MOUSEBUTTONDOWN:
                if button_rect.collidepoint(event.pos):
                    return volume
                if plus_button_rect.collidepoint(event.pos):
                    volume = min(volume + 0.1, 1.0)
                if minus_button_rect.collidepoint(event.pos):
                    volume = max(volume - 0.1, 0.0)

        screen.blit(video_frames[frame_index % len(video_frames)], (0, 0))
        frame_index += 1
        
        draw_text_centered(screen, "Settings", font, (0, 255, 255), screen.get_width() // 2, screen.get_height() // 2 - 50)
        draw_text_centered(screen, f"Volume: {volume:.1f}", font, (0, 255, 255), screen.get_width() // 2, screen.get_height() // 2 - 20)
        
        pygame.draw.rect(screen, button_color, button_rect)
        draw_text_centered(screen, button_text, button_font, (0, 0, 0), button_rect.centerx, button_rect.centery)
        
        pygame.draw.rect(screen, button_color, plus_button_rect)
        draw_text_centered(screen, "+", button_font, (0, 0, 0), plus_button_rect.centerx, plus_button_rect.centery)
        
        pygame.draw.rect(screen, button_color, minus_button_rect)
        draw_text_centered(screen, "-", button_font, (0, 0, 0), minus_button_rect.centerx, minus_button_rect.centery)

        pygame.display.flip()
