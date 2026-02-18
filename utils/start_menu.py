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
    small_font = pygame.font.Font(None, 24)

    buttons = [
        {"text": "1 Spieler (Testing)", "rect": pygame.Rect(400, 240, 400, 60), "players": 1},
        {"text": "2 Spieler", "rect": pygame.Rect(400, 320, 400, 60), "players": 2},
        {"text": "3 Spieler", "rect": pygame.Rect(400, 400, 400, 60), "players": 3},
        {"text": "4 Spieler", "rect": pygame.Rect(400, 480, 400, 60), "players": 4},
        {"text": "Beenden", "rect": pygame.Rect(400, 560, 400, 60), "players": 0},
    ]

    # AI-Toggle-States (False = Human, True = AI)
    # Index 0 = Player 2, Index 1 = Player 3, Index 2 = Player 4
    ai_toggles = [False, False, False]

    # Toggle-Button-Rects (rechts neben 2/3/4-Spieler Buttons)
    toggle_rects = [
        pygame.Rect(820, 325, 80, 50),  # Neben "2 Spieler"
        pygame.Rect(820, 405, 80, 50),  # Neben "3 Spieler"
        pygame.Rect(820, 485, 80, 50),  # Neben "4 Spieler"
    ]

    while game_instance.running:
        game_instance.mouse_pos = pygame.mouse.get_pos()

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                game_instance.running = False
                return

            if event.type == pygame.MOUSEBUTTONDOWN:
                # Toggle-Button-Klick-Erkennung
                for i, toggle_rect in enumerate(toggle_rects):
                    if toggle_rect.collidepoint(game_instance.mouse_pos):
                        ai_toggles[i] = not ai_toggles[i]

                # Spielstart-Button-Klick
                for button in buttons:
                    if button["rect"].collidepoint(game_instance.mouse_pos):
                        if button["players"] == 0:
                            game_instance.running = False
                            return
                        else:
                            # Bestimme welche Spieler KI-gesteuert sind
                            ai_enabled = []
                            player_count = button["players"]

                            if player_count >= 2 and ai_toggles[0]:
                                ai_enabled.append(1)  # Player 2 (Index 1)
                            if player_count >= 3 and ai_toggles[1]:
                                ai_enabled.append(2)  # Player 3 (Index 2)
                            if player_count >= 4 and ai_toggles[2]:
                                ai_enabled.append(3)  # Player 4 (Index 3)

                            # Starte Spiel mit KI-Konfiguration
                            game_instance.game = Game(player_count, ai_enabled_players=ai_enabled)
                            game_instance.game.start_game()
                            return

        # Zeichne Menü
        game_instance.screen.fill(BACKGROUND)

        # Titel
        title = font.render("Carat", True, BLACK)
        title_rect = title.get_rect(center=(WINDOW_WIDTH // 2, 150))
        game_instance.screen.blit(title, title_rect)

        # Buttons
        for idx, button in enumerate(buttons):
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

        # AI-Toggle-Buttons (nur für 2/3/4-Spieler)
        for i, toggle_rect in enumerate(toggle_rects):
            # Toggle-Label
            label = small_font.render(f"P{i+2} AI", True, BLACK)
            label_rect = label.get_rect(midtop=(toggle_rect.centerx, toggle_rect.top - 25))
            game_instance.screen.blit(label, label_rect)

            # Toggle-Button
            if toggle_rect.collidepoint(game_instance.mouse_pos):
                border_color = (100, 100, 100)
            else:
                border_color = BLACK

            # Background: Grün wenn ON, Grau wenn OFF
            if ai_toggles[i]:
                bg_color = (100, 200, 100)  # Grün
                text_str = "ON"
            else:
                bg_color = (180, 180, 180)  # Grau
                text_str = "OFF"

            pygame.draw.rect(game_instance.screen, bg_color, toggle_rect)
            pygame.draw.rect(game_instance.screen, border_color, toggle_rect, 2)

            # Toggle-Text
            toggle_text = small_font.render(text_str, True, BLACK)
            toggle_text_rect = toggle_text.get_rect(center=toggle_rect.center)
            game_instance.screen.blit(toggle_text, toggle_text_rect)

        pygame.display.flip()
        game_instance.clock.tick(FPS)
