import pygame
import pygame.freetype
from config import load_config
import sys 

config = load_config()
font_path = config['Paths']['font']
font_size = 24

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
        
        draw_text_centered(screen, "Main Menu", font, (0, 255, 255), screen.get_width() // 2, screen.get_height() // 2 - 100)
        
        for i, rect in enumerate(button_rects):
            pygame.draw.rect(screen, (0, 255, 255), rect)
            draw_text_centered(screen, button_texts[i], button_font, (0, 0, 0), rect.centerx, rect.centery)

        pygame.display.flip()


def boss_selection_menu(screen, trophies, video_frames):
    button_font = pygame.freetype.Font(font_path, font_size)

    button_texts = ["Cerberus", "Back"]
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
                        if button_texts[i] == "Back":
                            return False
                        else:
                            return True

        screen.blit(video_frames[frame_index % len(video_frames)], (0, 0))
        frame_index += 1
        
        draw_text_centered(screen, f"Trophies: {trophies}", font, (0, 255, 255), screen.get_width() // 2, screen.get_height() // 2 - 100)
        
        for i, rect in enumerate(button_rects):
            pygame.draw.rect(screen, (0, 255, 255), rect)
            draw_text_centered(screen, button_texts[i], button_font, (0, 0, 0), rect.centerx, rect.centery)

        pygame.display.flip()

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
        draw_text_centered(screen, "Game Developer: Your Name", font, (0, 255, 255), screen.get_width() // 2, screen.get_height() // 2)
        draw_text_centered(screen, "Graphics: Your Name", font, (0, 255, 255), screen.get_width() // 2, screen.get_height() // 2 + 40)
        draw_text_centered(screen, "Music: Your Name", font, (0, 255, 255), screen.get_width() // 2, screen.get_height() // 2 + 80)
        
        pygame.draw.rect(screen, (0, 255, 255), button_rect)
        draw_text_centered(screen, button_text, button_font, (0, 0, 0), button_rect.centerx, button_rect.centery)
        
        pygame.display.flip()


def victory_screen(screen, video_frames):
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
        
        draw_text_centered(screen, "Victory!", font, (0, 255, 0), screen.get_width() // 2, screen.get_height() // 2 - 50)
        pygame.draw.rect(screen, (0, 255, 255), button_rect)
        draw_text_centered(screen, button_text, button_font, (0, 0, 0), button_rect.centerx, button_rect.centery)

        pygame.display.flip()
