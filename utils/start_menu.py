"""
Startmenü-Funktion für das Carat Spiel
"""
import pygame
from constants import *
from game import Game


def start_menu(game_instance):
    """
    Zeigt das Startmenü

    Args:
        game_instance: CaratGame-Instanz
    """
    font = pygame.font.Font(None, TITLE_FONT_SIZE)
    button_font = pygame.font.Font(None, FONT_SIZE)

    buttons = [
        {"text": "2 Spieler", "rect": pygame.Rect(400, 300, 400, 60), "players": 2},
        {"text": "3 Spieler", "rect": pygame.Rect(400, 380, 400, 60), "players": 3},
        {"text": "4 Spieler", "rect": pygame.Rect(400, 460, 400, 60), "players": 4},
        {"text": "Beenden", "rect": pygame.Rect(400, 540, 400, 60), "players": 0},
    ]

    while game_instance.running:
        game_instance.mouse_pos = pygame.mouse.get_pos()

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                game_instance.running = False
                return

            if event.type == pygame.MOUSEBUTTONDOWN:
                for button in buttons:
                    if button["rect"].collidepoint(game_instance.mouse_pos):
                        if button["players"] == 0:
                            game_instance.running = False
                            return
                        else:
                            # Starte Spiel mit gewählter Spielerzahl
                            game_instance.game = Game(button["players"])
                            game_instance.game.start_game()
                            return

        # Zeichne Menü
        game_instance.screen.fill(BACKGROUND)

        # Titel
        title = font.render("Carat", True, BLACK)
        title_rect = title.get_rect(center=(WINDOW_WIDTH // 2, 150))
        game_instance.screen.blit(title, title_rect)

        # Buttons
        for button in buttons:
            # Button-Farbe (hover-effekt)
            if button["rect"].collidepoint(game_instance.mouse_pos):
                color = BUTTON_HOVER
            else:
                color = BUTTON_COLOR

            pygame.draw.rect(game_instance.screen, color, button["rect"])
            pygame.draw.rect(game_instance.screen, BLACK, button["rect"], 2)

            # Text
            text = button_font.render(button["text"], True, BLACK)
            text_rect = text.get_rect(center=button["rect"].center)
            game_instance.screen.blit(text, text_rect)

        pygame.display.flip()
        game_instance.clock.tick(FPS)
