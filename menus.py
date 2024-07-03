import pygame
import pygame.freetype

# Initialisation de Pygame
pygame.init()

# Définition des couleurs
WHITE = (255, 255, 255)
BLACK = (0, 0, 0)
LIGHT_GRAY = (200, 200, 200)
DARK_GRAY = (50, 50, 50)
RED = (255, 0, 0)
GREEN = (0, 255, 0)
BLUE = (0, 0, 255)

# Charger la police
FONT_PATH = "data/OpenSans-Regular.ttf"
FONT_SIZE = 36

# Définir la police en utilisant pygame.freetype
pygame.freetype.init()
font = pygame.freetype.Font(FONT_PATH, FONT_SIZE)

# Dessiner du texte
def draw_text(screen, text, font, color, pos):
    text_surface, _ = font.render(text, color)
    screen.blit(text_surface, pos)

# Créer un bouton
def create_button(screen, text, font, color, rect, hover_color):
    mouse_pos = pygame.mouse.get_pos()
    if rect.collidepoint(mouse_pos):
        pygame.draw.rect(screen, hover_color, rect)
    else:
        pygame.draw.rect(screen, color, rect)
    draw_text(screen, text, font, WHITE, (rect.x + 20, rect.y + 10))

# Menu principal
def main_menu(screen):
    clock = pygame.time.Clock()
    button_start = pygame.Rect(300, 200, 200, 50)
    button_quit = pygame.Rect(300, 300, 200, 50)

    while True:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                return False
            if event.type == pygame.MOUSEBUTTONDOWN:
                if button_start.collidepoint(event.pos):
                    return True
                if button_quit.collidepoint(event.pos):
                    return False

        screen.fill(BLACK)
        draw_text(screen, "Bullet Hell Game", font, WHITE, (230, 100))
        create_button(screen, "Start Game", font, DARK_GRAY, button_start, LIGHT_GRAY)
        create_button(screen, "Quit", font, DARK_GRAY, button_quit, LIGHT_GRAY)

        pygame.display.flip()
        clock.tick(60)

# Menu de sélection des boss
def boss_selection_menu(screen):
    clock = pygame.time.Clock()
    button_boss1 = pygame.Rect(300, 200, 200, 50)
    button_back = pygame.Rect(300, 300, 200, 50)

    while True:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                return False
            if event.type == pygame.MOUSEBUTTONDOWN:
                if button_boss1.collidepoint(event.pos):
                    return True
                if button_back.collidepoint(event.pos):
                    return False

        screen.fill(BLACK)
        draw_text(screen, "Select Boss", font, WHITE, (300, 100))
        create_button(screen, "Cerberus", font, DARK_GRAY, button_boss1, LIGHT_GRAY)
        create_button(screen, "Back", font, DARK_GRAY, button_back, LIGHT_GRAY)

        pygame.display.flip()
        clock.tick(60)
