import pygame
import pygame.freetype
import configparser

config = configparser.ConfigParser()
config.read('config.ini')

font_path = config['Paths']['font']
background_path = config['Paths']['menu_background']

def draw_text_centered(screen, text, font, color, center_x, center_y):
    text_surface, rect = font.render(text, color)
    rect.center = (center_x, center_y)
    screen.blit(text_surface, rect.topleft)

def main_menu(screen):
    font = pygame.freetype.Font(font_path, 48)
    background = pygame.image.load(background_path)
    background = pygame.transform.scale(background, (screen.get_width(), screen.get_height()))

    button_font = pygame.freetype.Font(font_path, 36)
    button_text = "Start Game"
    button_color = (0, 255, 255)
    button_rect = pygame.Rect(0, 0, 300, 50)
    button_rect.center = (screen.get_width() // 2, screen.get_height() // 2 + 50)

    running = True
    while running:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                return False
            if event.type == pygame.MOUSEBUTTONDOWN:
                if button_rect.collidepoint(event.pos):
                    return True

        screen.blit(background, (0, 0))
        draw_text_centered(screen, "Bullet Hell Game", font, (0, 255, 255), screen.get_width() // 2, screen.get_height() // 2 - 50)
        pygame.draw.rect(screen, button_color, button_rect)
        draw_text_centered(screen, button_text, button_font, (0, 0, 0), button_rect.centerx, button_rect.centery)

        pygame.display.flip()

def boss_selection_menu(screen, trophies):
    font = pygame.freetype.Font(font_path, 36)
    background = pygame.image.load(background_path)
    background = pygame.transform.scale(background, (screen.get_width(), screen.get_height()))

    button_font = pygame.freetype.Font(font_path, 36)
    button_text = "Cerberus"
    button_color = (0, 255, 255)
    button_rect = pygame.Rect(0, 0, 300, 50)
    button_rect.center = (screen.get_width() // 2, screen.get_height() // 2)

    running = True
    while running:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                return False
            if event.type == pygame.MOUSEBUTTONDOWN:
                if button_rect.collidepoint(event.pos):
                    return True

        screen.blit(background, (0, 0))
        draw_text_centered(screen, "Select a Boss to Fight", font, (0, 255, 255), screen.get_width() // 2, screen.get_height() // 2 - 50)
        pygame.draw.rect(screen, button_color, button_rect)
        draw_text_centered(screen, button_text, button_font, (0, 0, 0), button_rect.centerx, button_rect.centery)
        draw_text_centered(screen, f"Trophies: {trophies}", font, (0, 255, 255), screen.get_width() // 2, screen.get_height() // 2 + 100)

        pygame.display.flip()

def game_over_screen(screen):
    font = pygame.freetype.Font(font_path, 48)
    background = pygame.image.load(background_path)
    background = pygame.transform.scale(background, (screen.get_width(), screen.get_height()))

    button_font = pygame.freetype.Font(font_path, 36)
    button_text = "Retry"
    button_color = (255, 0, 0)
    button_rect = pygame.Rect(0, 0, 300, 50)
    button_rect.center = (screen.get_width() // 2, screen.get_height() // 2 + 50)

    running = True
    while running:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                return False
            if event.type == pygame.MOUSEBUTTONDOWN:
                if button_rect.collidepoint(event.pos):
                    return True

        screen.blit(background, (0, 0))
        draw_text_centered(screen, "Game Over", font, (255, 0, 0), screen.get_width() // 2, screen.get_height() // 2 - 50)
        pygame.draw.rect(screen, button_color, button_rect)
        draw_text_centered(screen, button_text, button_font, (0, 0, 0), button_rect.centerx, button_rect.centery)

        pygame.display.flip()

def victory_screen(screen):
    font = pygame.freetype.Font(font_path, 48)
    background = pygame.image.load(background_path)
    background = pygame.transform.scale(background, (screen.get_width(), screen.get_height()))

    button_font = pygame.freetype.Font(font_path, 36)
    button_text = "Continue"
    button_color = (0, 255, 0)
    button_rect = pygame.Rect(0, 0, 300, 50)
    button_rect.center = (screen.get_width() // 2, screen.get_height() // 2 + 50)

    running = True
    while running:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                return False
            if event.type == pygame.MOUSEBUTTONDOWN:
                if button_rect.collidepoint(event.pos):
                    return True

        screen.blit(background, (0, 0))
        draw_text_centered(screen, "Victory!", font, (0, 255, 0), screen.get_width() // 2, screen.get_height() // 2 - 50)
        pygame.draw.rect(screen, button_color, button_rect)
        draw_text_centered(screen, button_text, button_font, (0, 0, 0), button_rect.centerx, button_rect.centery)

        pygame.display.flip()
