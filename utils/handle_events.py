"""
Event-Handler-Funktion für das Carat Spiel
"""
import pygame
from constants import *
from game import Game
from utils.handle_board_click import handle_board_click
from utils.start_menu import start_menu
import utils.render
from utils.update import reset_chip_preview


def handle_events(game_instance):
    """
    Verarbeitet Eingaben

    Args:
        game_instance: CaratGame-Instanz
    """
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            game_instance.running = False

        elif event.type == pygame.MOUSEMOTION:
            game_instance.mouse_pos = event.pos

        elif event.type == pygame.MOUSEBUTTONDOWN:
            if game_instance.game.state == GAME_STATE_PLAYING:
                # Blockiere Input während KI am Zug ist
                if not game_instance.game.ai_animating:
                    handle_board_click(game_instance, event.pos)

        elif event.type == pygame.KEYDOWN:
            # Zoom Toggle (funktioniert immer während des Spiels)
            if event.key == pygame.K_z and game_instance.game:
                game_instance.zoom_active = not game_instance.zoom_active
                game_instance.zoom_animating = True
                game_instance.zoom_animation_start = pygame.time.get_ticks()
                game_instance.zoom_target = 1.0 if game_instance.zoom_active else 0.0
                # Speichere aktuelle Mausposition als Zoom-Zentrum
                game_instance.zoom_center = game_instance.mouse_pos

            if game_instance.game.state == GAME_STATE_PLAYING and not game_instance.game.ai_animating:
                if event.key == pygame.K_r:
                    # Debug: Zeige Status vor Rotation
                    #print(f"\n=== ROTATION CLOCKWISE ===")

                    # Berechne betroffene Chips aus aktueller Mausposition
                    x, y = game_instance.mouse_pos
                    col = (x - BOARD_OFFSET_X) // CELL_SIZE
                    row = (y - BOARD_OFFSET_Y) // CELL_SIZE

                    #print(f"Mouse position: row={row}, col={col}")

                    # Berechne affected chips aus Mausposition
                    if 0 <= row < BOARD_SIZE and 0 <= col < BOARD_SIZE:
                        if game_instance.game.is_valid_placement(row, col):
                            affected_positions = [
                                (row, col),
                                (row, col + 1),
                                (row + 1, col + 1),
                                (row + 1, col)
                            ]

                            # Rotiere Plättchen im Uhrzeigersinn
                            game_instance.game.rotate_current_tile_clockwise()

                            # Setze affected_chips und force refresh
                            utils.render._affected_chips = affected_positions
                            utils.render._force_refresh = True  # Erzwinge Neuberechnung

                            #print(f"Nach Rotation - _affected_chips set to: {utils.render._affected_chips}")
                            #print(f"Nach Rotation - _force_refresh set to True")
                            #print(f"Nach Rotation - color_order: {game_instance.game.selected_tile.color_order}")
                        else:
                            # Ungültige Position, rotiere trotzdem
                            game_instance.game.rotate_current_tile_clockwise()
                    else:
                        # Außerhalb Board, rotiere trotzdem
                        game_instance.game.rotate_current_tile_clockwise()

                    #print("=========================\n")
                elif event.key == pygame.K_e:
                    # Debug: Zeige Status vor Rotation
                    #print(f"\n=== ROTATION COUNTER-CLOCKWISE ===")

                    # Berechne betroffene Chips aus aktueller Mausposition
                    x, y = game_instance.mouse_pos
                    col = (x - BOARD_OFFSET_X) // CELL_SIZE
                    row = (y - BOARD_OFFSET_Y) // CELL_SIZE

                    #print(f"Mouse position: row={row}, col={col}")

                    # Berechne affected chips aus Mausposition
                    if 0 <= row < BOARD_SIZE and 0 <= col < BOARD_SIZE:
                        if game_instance.game.is_valid_placement(row, col):
                            affected_positions = [
                                (row, col),
                                (row, col + 1),
                                (row + 1, col + 1),
                                (row + 1, col)
                            ]

                            # Rotiere Plättchen gegen Uhrzeigersinn
                            game_instance.game.rotate_current_tile_counter_clockwise()

                            # Setze affected_chips und force refresh
                            utils.render._affected_chips = affected_positions
                            utils.render._force_refresh = True  # Erzwinge Neuberechnung

                            #print(f"Nach Rotation - _affected_chips set to: {utils.render._affected_chips}")
                            #print(f"Nach Rotation - _force_refresh set to True")
                            #print(f"Nach Rotation - color_order: {game_instance.game.selected_tile.color_order}")
                        else:
                            # Ungültige Position, rotiere trotzdem
                            game_instance.game.rotate_current_tile_counter_clockwise()
                    else:
                        # Außerhalb Board, rotiere trotzdem
                        game_instance.game.rotate_current_tile_counter_clockwise()

                    #print("=================================\n")

            elif game_instance.game.state == GAME_STATE_GAME_OVER:
                if event.key == pygame.K_SPACE:
                    # Neues Spiel starten
                    player_count = game_instance.game.player_count
                    game_instance.game = Game(player_count)
                    game_instance.game.start_game()
                elif event.key == pygame.K_ESCAPE:
                    # Zurück zum Menü
                    game_instance.game = None
                    start_menu(game_instance)
